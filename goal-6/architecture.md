# Goal 6 Architecture

Status: **IN PROGRESS — APPLICATION CONTRACT UNDER SPECIFICATION**

This is the evolving canonical architecture specification for Goal 6. It
records settled decisions and points to later-stage artifacts rather than
duplicating the completed taxonomy.

## Purpose

Remaster the frozen Goal 2 implementation plan around one ordinary program
value:

```python
SimpleProgram(
    seed=...,
    alphabet=...,
    frontier=...,
    neighborhood=...,
    rule=...,
)
```

Goal 6 specifies this architecture and the mechanics-first implementation plan.
It does not change runtime behavior. Goal 7 will implement the result only
after separate authorization.

## Source Authority

| Priority | Source | Governing responsibility |
|---:|---|---|
| 1 | `goal-5/taxonomy-census.md` | Final counts and catalog scope |
| 1 | `goal-5/11-FAMILIES.md` | Family identities, boundaries, sources, and mechanics |
| 2 | `goal-5/api-pressure.md` | Five-field fit and family-by-family pressure |
| 3 | `goal-5/integration-handoff.md` | Remaster boundary and Goal 2 preserve/replace decisions |
| 4 | `goal-5/10-RECONCILE.md` | Exact T01–T45 dispositions |
| 5 | `goal-5/source-decision-matrix.csv` | Source traceability only when a decision needs it |
| 6 | `simple_programs.md`, `api.md`, `ref/notes/ca-scaffold.py` | Design inputs to clarify during Goal 6 |
| 7 | `goal-2/goal-2-handoff.md` | Frozen details for conclusions explicitly preserved by Goal 5 |

When sources conflict, the more authoritative Goal 5 result wins. A newly
identified canonical-source contradiction is escalated; implementation
convenience, current code, old plan detail, or naming preference cannot
override the completed audit.

Goal 4's plans, tools, ledgers, searches, and verification machinery have no
role in this architecture. No Book rediscovery is required.

## Settled Program Boundary

`SimpleProgram` stores exactly:

1. `seed`
2. `alphabet`
3. `frontier`
4. `neighborhood`
5. `rule`

`C`, `V`, `W`, and `R` are relationships among component types, not stored
axes. Configuration structure, support, topology, geometry, boundary behavior,
control, schedule, and visible entropy are data produced by `Seed` and
interpreted by the five components. Run horizon, query/solver strategy,
realization, replay key, resources, tracing, observation, rendering, and export
are invocation or tooling concerns.

Frontier is the complete possible-write envelope. Neighborhood is the readable
region. Rule is the closed relation that owns applicability, scheduling,
conflict, stochastic, result, and update semantics. Generic application
validates and atomically commits Rule results; it does not supply a sixth policy
axis.

These decisions are fixed by Goal 5. Their detailed protocols are the work of
Stages 2 and 3.

## Document Ownership

| Artifact | Role |
|---|---|
| `goal-6/0-plan.md` | Completion contract and staged strategy |
| `goal-6/0-loop.md` | Execution protocol and stage template |
| `goal-6/architecture.md` | Canonical internal architecture and ownership decisions |
| `api.md` | Stage 4 target: clean public API contract; currently a design input |
| `simple_programs.md` | Stage 4 target: conceptual specification/rationale without a competing API |
| `ref/notes/ca-scaffold.py` | Stage 4 target: one compact code-shaped architecture walkthrough |
| `goal-6/catalog-migration.md` | Stage 5 canonical 60-family/T01–T45 catalog mapping |
| `goal-6/conformance.md` | Stage 6 paper fixtures and Goal 7 test obligations |
| `goal-6/goal-7-handoff.md` | Stage 7 file-level implementation plan |
| `goal-2/` | Frozen historical comparison baseline; never current instructions |
| `GOALS.md` | Live status and execution sequence only |

Stage reports record evidence. They do not become competing specifications.

## Goal 2 Decision Ledger

The Goal 5 integration handoff already resolved the old plan's architecture.
This ledger makes every major Goal 2 concern explicit without importing its
obsolete stage machinery.

### Preserve

| Goal 2 conclusion | Goal 6 disposition |
|---|---|
| Closed structural descriptors with explicit validation and versions | Preserve across all five components and their codecs |
| No unrestricted callbacks, `Any`, `eval`, formula text, host CAS objects, generators, or iterator escape hatches | Preserve as a public semantic-data invariant |
| Exact integers, rationals, algebraic/declared representations, and no silent float fallback | Preserve in Alphabet/configuration structures and Rule data/results |
| Visible head, control, instruction, phase, schedule, and stored-program state | Preserve as ordinary tagged configuration/program data |
| Visible and replayable randomness | Preserve as explicit Seed laws or Rule probability/draw evidence |
| One generic branch-free application path | Preserve and generalize to every executable family |
| Typed cardinality, outcomes, failures, witnesses, lineage, and provenance | Preserve in the Rule codomain and application result |
| Derivation witnesses before successor deduplication | Preserve exactly |
| Raw structural traces before coordinate/tensor/rendered views | Preserve at the run/tooling boundary |
| Representation inverse-on-image and one-step full-result commutation | Preserve as conformance obligations |
| Versioned lossless codecs, unknown-tag failure, and derived rather than authoritative IDs/digests | Preserve in root `serialization.py` |
| Presets construct ordinary program data and never register executors | Preserve; named whole-program constructors move to `catalog/` |
| In-place migration with no second executor or fallback semantic path | Preserve for Goal 7 cutover planning |
| Typed unsupported/undefined results instead of invented defaults | Preserve and refine in Stages 2–3 |
| Canonical Book sources for preset claims and fixtures | Preserve for provenance; do not redo discovery |

### Replace

| Goal 2 element | Goal 6 replacement |
|---|---|
| Public `DOMAIN` axis | Carrier/support/topology/geometry descriptors in Seed-produced configuration and shared loci structures |
| Public `CONFIGURATION_SCHEMA` axis | Type relationship `C` and validated configuration data produced by `Seed`, not a sixth field |
| Fixed or scalar-centric value/carrier assumptions | Structural Alphabet/configuration schemas spanning words, trees, graphs, products, fields, and intensional objects |
| Firing-source `FRONTIER` | Complete writable capability envelope, including possible destinations and fresh/deleted components |
| Offset/snapshot-only `NEIGHBORHOOD` | Arbitrary typed readable region, local or nonlocal, structural or differential |
| Rule as proposal producer without commit semantics | Closed Rule relation returning complete atomic replacements and typed results |
| Public `UPDATE`/`UpdatePolicy` axis | Rule-owned scheduling/conflict/update semantics plus one invariant generic atomic commit |
| Separate sibling ontology for constraints, functions, constants, and PDEs | Ordinary five-field one-shot or iterated programs; query/realization policy remains outside the program |
| Fixed `Z4`, finite coordinates, one scalar per cell, and mandatory synchronous steps | General structural/intensional loci and configuration carriers |
| Construction-named runtime classes and family registry execution | Structural constructors returning ordinary `SimpleProgram` values; metadata never dispatches |
| T08 initial-condition “family” | `Seed` constructors/laws/realizations |
| Observers, renderers, properties, and representations treated as families | Tooling, views, metadata, or separate transforms when they have their own mechanics |
| Hidden solver behavior or untyped empty successor sets | Explicit run policy, evidence, cardinality, outcome, and terminal/undefined distinctions |
| Goal 2's 45-row implementation scope | All 60 executable families, two close-role boundaries, and the exact T01–T45 migration |
| Goal 2's chapter/type-oriented stage plan | Mechanics-first Goal 7 dependency plan |

### Defer Without Losing the Decision

| Question | Destination |
|---|---|
| Exact five component protocols and cross-field validation | Stage 2 |
| Lazy/intensional writable and readable regions, including how Rule exposes actual applicability inside the writable envelope | Stages 2–3 |
| Complete Rule result algebra and application pseudocode | Stage 3 |
| Fresh-identity allocation, overlapping-write ordering, and validation before/after commit | Stage 3 |
| Entropy authority across Seed laws, stochastic Rule laws, replay evidence, and external run requests | Stages 2–3 |
| Final ownership of helper/result types without public module inflation | Stage 4 |
| Root exports, alias spelling, and `ca.rollout` surface | Stage 4 |
| Stable catalog IDs, canonical constructor names, and six-module placement | Stage 5 |
| Legacy source/capability boundaries for adaptive subdivision, sequential network schedules, weak PDEs, and exact transcendental execution | Stages 5–6 |
| Pressure fixtures, codec/replay/commutation tests, and hostile review | Stage 6 |
| Compatibility, the optional `Dynamics` façade, deprecation, serialization cutover, and exact file migration | Stage 7 |
| Generation, datasets, streams, RNG-helper placement, visualization, and export internals | Goal 7 or later, except for stable public boundaries |
| Numerical/solver backend selection and performance strategy | Goal 7 implementation; exactness and evidence contracts are already fixed |

### Old Module-Area Coverage

This table proves that no Goal 2 subsystem is silently unreviewed.

| Goal 2 area | Disposition |
|---|---|
| `domains.py` | Public area rejected; structural responsibility moves under Seed/configuration/loci |
| `alphabets.py`, `values.py` | Semantic work preserved and generalized; final public ownership is `alphabets.py` plus structural values |
| `configurations.py` | Public axis/module not presumed; semantic work belongs to Seed outputs and shared structures |
| `loci.py` | Preserved and generalized as the common locus/region algebra |
| `frontiers.py` | Preserved file, replaced firing-source contract |
| `neighborhoods.py` | Preserved file, generalized read contract |
| `rules.py`, `updates.py` | Rule descriptors preserved; update semantics absorbed into Rule/results and generic commit |
| `seeds.py` | Preserved and generalized from event-zero data to configuration sources/laws |
| `outcomes.py`, `traces.py` | Semantics preserved; Stage 4 decides minimal ownership without presuming public files |
| `expressions.py`, `relations.py`, `queries.py` | Closed data strengths preserved; sibling ontology rejected in favor of five-field programs and external run/query policy |
| `serialization.py` | Preserved as a root cross-cutting codec boundary |
| `specs.py` | Replaced by `program.py` and `SimpleProgram` |
| `rollout.py` | Generic traversal intent preserved; exact file/public ownership settled in Stage 4 |
| `datasets.py`, `rng.py`, `viz/` | Downstream behavior preserved until Goal 7; internal reorganization deferred |
| `tests/conformance/` | One-obligation rigor preserved, expanded and reorganized around reusable mechanics and 60-family coverage |

Goal 2's original deferred list is also resolved: stochastic and native
continuous mechanics are now required by the 60-family inventory; specific
unsupported source profiles remain typed rather than guessed; weak/approximate
PDE and transcendental backends remain exactness/evidence questions; and the
old “outside the 45 rows” boundary is replaced by the completed 60-family
census.

## Contract Vocabulary

The architecture distinguishes four things that older documents sometimes
collapsed:

- A **descriptor** is immutable, closed, versioned structural data.
- A **denotation** is the mathematical object or relation that descriptor
  means.
- **Resolution** applies a descriptor to a validated configuration to obtain a
  typed writable capability or read view.
- A **realization** is a finite, sampled, encoded, numerical, or otherwise
  operational presentation requested by a run or tool.

A realization never silently replaces the denotation as program identity.
Finite arrays may realize fields, graphs may have canonical encodings, and
probability laws may be sampled, but those are explicit representation
relations with their own evidence and limits.

“Closed” does not mean “finite.” A descriptor may denote an infinite set,
continuous field, probability measure, recursive structure, or symbolic
relation through a versioned AST whose primitives and binding rules are
known. It may not contain a Python callback, iterator, generator, opaque
solver, host CAS object, or executable formula string.

Closed extensibility is also fail-closed. Satisfying a Python protocol is not
enough to admit a semantic descriptor: every node must be a recognized,
versioned structural variant, or an explicitly registered extension carrying
the same schema, codec, validation, and exactness obligations. Duck typing may
serve implementation internals, but it cannot define program identity.

## Five-Field Type Algebra

The conceptual signature is:

```python
@dataclass(frozen=True)
class SimpleProgram(Generic[C, V, W, R]):
    seed: Seed[C]
    alphabet: Alphabet[V]
    frontier: WritableRegion[C, W]
    neighborhood: ReadableRegion[C, R]
    rule: Rule[R, W, C]
```

The type variables mean:

| Type | Meaning |
|---|---|
| `C` | One immutable, invariant-bearing configuration |
| `V` | The closed universe of semantic values admitted inside `C` and in writes |
| `W` | A resolved writable capability/envelope for one application |
| `R` | A resolved, identity-preserving read view supplied to Rule |

Locus/key types are associated structural types inside `C`, `W`, and `R`.
They need not become another public generic parameter or program field.

The denotational flow is:

```text
Seed[C]                       denotes initial C values, sets, or laws
Alphabet[V]                   validates semantic values within C
WritableRegion[C, W](C)       resolves W
ReadableRegion[C, R](C)       resolves R from the same immutable C
Rule[R, W, C](R, W)           denotes typed results/replacements of C
```

Equivalently, for a realized initial configuration `c`:

```text
c ∈ support(⟦seed⟧)
valid_C(c)
values(c) ⊆ ⟦alphabet⟧
w = ⟦frontier⟧(c)
r = ⟦neighborhood⟧(c)
q ∈ ⟦rule⟧(r, w)
```

Rule does not receive unrestricted access to `c`. Every semantic state
dependency it uses must be present in `r`; `w` supplies writable identities and
capabilities, not an implicit read channel. The generic application operation
retains `c` only to validate and commit `q`; the result-and-commit algebra
below fixes that boundary.

Frontier and Neighborhood may reuse the same closed locus/anchor descriptor,
and Rule may require their resolved views to have compatible indexing. Neither
resolver consumes the other resolver's output. This preserves their
orthogonality: both resolve independently from the same immutable `C`.

Independent resolution is still one typed join. Both resolvers bind to the
same immutable snapshot identity, and their locus/occurrence references use
the same canonical identities. Rule declares the required `R`-to-`W`
join/index shape; construction validates that shape structurally, and
application validates the resolved binding before Rule denotation.

Generic parameters, validation evidence, codec versions, digests, catalog
names, and provenance are not extra `SimpleProgram` fields. Catalog entries and
serialization envelopes may describe a program externally; the semantic
program value is still the five components.

## Configuration Ownership

`C` is a semantic contract shared by all five components, not a sixth
component named `ConfigurationSchema`.

Every configuration must provide closed structural meaning for the portions
its program uses:

| Concern | Configuration responsibility |
|---|---|
| Carrier/support | Existing discrete, continuous, structural, or intensional components |
| Topology/incidence | Adjacency, order, parent/child, ports, links, products, or named addressing |
| Geometry | Coordinates, metrics, regions, orientations, embeddings, or differential domains when relevant |
| Values | Exact assignments, fields, symbolic values, or explicit unresolved roles validated by Alphabet |
| Defaults/boundaries | Total-default laws, exterior values, periodic/reflective identifications, side data, or absence semantics |
| Invariants | Closed predicates such as exactly-one head, well-formed word/tree/graph, compatible ports, or valid field side data |
| Visible state | Cursor, phase, time, schedule, program counter, mutable program text, and any cache, provenance, or draw state that the mechanics itself reads or writes |
| Identity | Stable structural identities and explicit alpha-equivalence/canonicalization rules |

These are semantic obligations, not a required monolithic record layout. A
finite lattice, a default-plus-overrides tape, a word, a tree, a port graph, a
product of named registers, a continuous field, and an intensional solution
object can all be `C` through closed sum/product/carrier descriptors.

The division between carrier and value is explicit:

- carrier structure and locus identity live in `C` and the loci algebra;
- labels and payloads stored in that structure conform to `Alphabet[V]`; and
- a word, graph, field, or expression may also occur as one composite `V` in a
  higher-level configuration.

Representation relations distinguish these choices. Packing a graph into one
opaque object cell or flattening a field into a tensor is not automatically
semantic equivalence.

`Seed` owns the source and initial structural commitments for `C`; successors
remain the same configuration type because Rule results also produce `C`.
Fixed transition data normally belongs to `Rule`. Program text belongs inside
`C` only when the construction makes it readable or writable state, as in F035
and F051.

Representation-changing media and transductions still have type `C -> C`.
Their carrier is a tagged phase state or a product with explicit input,
workspace, and output slots; Rule changes which slots are populated or
authoritative. A Rule never escapes the contract by returning an unrelated
configuration type `C2`.

## Component Contracts

### Seed

`Seed[C]` is a closed source of initial configurations. Its denotation may be:

| Form | Contract |
|---|---|
| Exact | One fully specified valid `C` |
| Constructive | A closed constructor from explicit parameters to valid `C` |
| Partial | A valid `C` with explicit unresolved roles, constraints, defaults, or boundary/initial data |
| Law | A probability measure over `C` with an explicit entropy/replay interface |
| Intensional | A finite closed presentation of an infinite, continuous, or symbolic initial object |

A “constructive” Seed is structural recipe data, not a host-language
generator. A partial Seed does not smuggle in missing values: unknowns,
obligations, and admissible completions are explicit values or relations that
Rule can read. An intensional Seed is not forced to enumerate its support.

For a probability-law Seed:

- the law and its parameters are part of the Seed descriptor;
- a run supplies a replay key or realization request externally;
- the initialization result or trace records draw evidence; if later Rule
  applications semantically read that evidence, it is instead visible state
  inside `C`; and
- no ambient/global RNG or hidden mutable generator contributes semantics.

Seed must declare enough associated output structure to unify its `C` with the
other four components. That declaration is embedded contract data, not a
separate program axis.

Seed composition returns one Seed:

- products combine named or provably disjoint structural components and do
  not imply probabilistic independence;
- overlays combine disjoint or explicitly resolved assignments;
- mixtures form an explicit probability law;
- product-law constructors state independence explicitly, while coupled joint
  laws remain representable;
- refinements add closed constraints or invariants; and
- constructive/intensional combinators preserve exact source and replay
  provenance.

### Alphabet

`Alphabet[V]` is a closed schema for semantic values, equality, and any
declared order or algebra. It is not required to be finite or enumerable.

Required structural constructors include:

- finite enums and ordered finite sets;
- naturals, integers, reduced rationals, modular values, algebraic values, and
  explicitly represented or certified reals/complex values;
- tagged sums and optional/unresolved roles;
- products, records, tuples, finite sequences, words, and maps;
- node, edge, port, instruction, address, gate, probability, and control
  records;
- bound symbolic expression, pattern, equation, and differential syntax; and
- field, tensor, distribution, or other composite values when used as a
  payload.

Infinite and continuous Alphabets provide validation and exact representation
contracts, not enumeration. Machine floats are permitted only as an explicitly
named represented-number profile; they never impersonate exact reals.

Alphabet owns value validity and canonical value equality. It does not own
carrier support, topology, geometry, scheduling, or a program-family name.
Product/tag/union/refinement constructors yield one composed Alphabet.

Absence and deletion are carrier states unless a construction explicitly
stores an absence token as a value. Likewise, `Unknown` is admitted only by an
explicit Alphabet variant; partiality never appears implicitly. Address,
node, edge, and port records may be values when stored as labels or payloads,
but actual locus identity and topology remain in `C` and the loci algebra.
Value-level algebra can support Rule expressions without absorbing the
transition relation into Alphabet.

### WritableRegion

`WritableRegion[C, W]` is a closed resolver from an immutable `C` to the
complete capability envelope `W` for one Rule application.

`W` must express:

- every existing locus that any permitted result may replace, relabel, or
  delete;
- every fresh locus, component, edge, child, span, field region, or result slot
  that any permitted result may create;
- the structural kinds and value contracts permitted at those targets;
- stable identity/namespace rules for existing and potential fresh components;
- ordering, grouping, interface, or multiplicity where replacement meaning
  depends on it; and
- finite or intensional membership sufficient to reject unauthorized writes.

Frontier is an envelope, not the actual changed set. It may over-approximate
which authorized member a Rule selects, but it must not omit any possible
target. For unresolved stochastic or branching choices it contains the union
of all permitted targets. It may be a whole field, all unknown variables, a
noncontiguous prefix/tail pair, a matched graph interface plus fresh namespace,
or a continuous region.

Frontier does not:

- identify which locus fires;
- supply readable values;
- choose a match, schedule, branch, destination, collision outcome, or
  stochastic draw; or
- prescribe how overlapping effects commit.

Those are Rule semantics. A tagged active cell may help Frontier resolve the
small complete envelope around it, but the tag and Rule still determine actual
applicability and choice.

A deletion targets an existing writable structural component. Every resulting
incident-edge, interface, default-fill, repair, or rewire effect must also be
authorized by `W` and stated by the Rule replacement. Generic commit never
silently cascades a deletion, repairs topology, fills a gap, or rewires an
interface. A creation targets an authorized fresh capability. Neither
operation requires pre-existing coordinates for every future component.

Union, product, relative/dilated, matched-interface, dynamic-address,
fresh-child, whole-region, and intensional combinators return one composed
WritableRegion.

Application validation additionally derives a closed reconstruction plan from
the configuration/frontier contracts and the resolved `W`. That plan is
application-private resolution evidence: Rule receives only the writable
capability view and cannot inspect snapshot/rebuild internals as a covert read
channel. It is not a sixth field or a user-selected update policy. Its exact
laws are fixed by the universal application contract below.

### ReadableRegion

`ReadableRegion[C, R]` is a closed resolver of one immutable input
configuration into the complete read view `R`.

`R` must retain every semantic distinction Rule needs:

- locus/component identity;
- value and structural type;
- order, orientation, grouping, multiplicity, and masks;
- absence, defaults, and boundary-extension results;
- paths, incidence, dangling interfaces, provenance, or history references;
- metric/global aggregates and dynamically addressed data; and
- continuous restrictions, differential germs, symbolic dependencies, or
  other intensional views.

ReadableRegion may describe a local stencil, indexed family of stencils,
matched span, graph path, complete prefix, whole configuration, global metric
relation, history, boundary field, differential neighborhood, or symbolic
solution context. “Neighborhood” never promises geometric locality.

Boundary/default data is carried by `C`; Neighborhood states what is observed
and resolves that observation without silently inventing an exterior
convention. Differential reads name exact derivatives/germs or an explicit
represented approximation relation—they do not silently select a numerical
stencil.

Rule may read only `R`. If a writable member's old value is required, the
Neighborhood must include it. Frontier grants write capability but never
grants read capability.

Product, keyed, relative, path, span, match-context, global, historical,
metric, differential, and intensional combinators return one composed
ReadableRegion. Their resolution can remain lazy; neither the contract nor
generic application requires flattening `R` into a finite list. Here “lazy”
means a closed, serializable intensional view or AST with defined membership
and traversal semantics—not a Python iterator, generator, callback, or
one-shot host object.

### Rule

`Rule[R, W, C]` is one closed, serializable relation over the supplied read
view and writable capability:

```text
(R, W) -> RuleResult[C, W]
```

At the contract level, `RuleResult` must be capable of denoting zero, one, or
many alternatives, with finite or intensional presentation. A probability
measure may weight those alternatives. An alternative's replacement may
itself contain a continuous field, flow segment, symbolic solution, or other
intensional structure; “continuous” describes that semantic object or its
measure, not a separate result cardinality.

The result/application sections below fix the concrete semantic variants,
witness/deduplication rules, outcomes, failure boundaries, fresh binding, and
commit law. Stage 2 fixed their denotational minimum: each alternative is a total
disposition over `W`. Every existing writable capability is explicitly
`Preserve`, `Replace`, or `Delete`; every fresh capability is explicitly
`Absent` or `Create`. A sparse encoding is valid only when it declares one of
those closed defaults for every omitted capability. Everything outside `W` is
universally preserved.

Consequently:

- every actual target is authorized by `W`, and every member of `W` has a
  disposition;
- every written semantic value conforms to Alphabet;
- Rule declares all read requirements satisfied by `R`;
- Rule owns applicability, clause priority, match selection, schedule,
  simultaneous/sequential meaning within one application, collision/conflict
  resolution, stopping, stochastic law, and actual changed set;
- Rule preserves configuration type `C` and states its invariant obligations;
  and
- no catalog ID, semantic-family name, callback, solver object, or executor
  appears in its denotation.

Closed Rule constructors may include tables, ordered clauses, expression ASTs,
patterns/templates, substitutions, instruction/gate networks, relational
constraints, equations, differential laws, probability kernels, and structural
composition. These are reusable mechanics, not semantic-family subclasses.

Conditional, ordered-choice, product, parallel, relational-union,
phase-controlled, and distribution combinators return one Rule. Any ordering,
priority, overlap, or conflict behavior is explicit in that Rule descriptor;
combining rules never creates an external update policy.

Composition also cannot conceal a second engine. One Rule application denotes
one closed macro-relation over the original `(R, W)` binding. A composed Rule
may calculate intermediate terms from that old view, but it may not commit and
reread intermediate configurations, consume an unrecorded draw, or expose a
hidden schedule. If intermediate state, event order, or draw history is
semantically observable, it appears as visible `C` across applications or as
an explicit result witness/trace.

Neither the contract nor generic application requires “run the Rule once per
cell.” A local synchronous transform can contain a closed map-over-region
Rule; a constraint can consume one global `R`; a graph rewrite can return
alternative structural replacements. Conceptually the Rule relation is applied
once to the structured `(R, W)` for the program application.

## Rule-Result Algebra

The result contract separates four questions that a bare successor list
collapses:

1. Did Rule denotation produce a complete semantic outcome space, or was the
   application rejected/incomplete?
2. How many derivation atoms does that space denote?
3. Which atoms produce replacements, and what progress/continuation outcome
   does each one carry?
4. After atomic commit and semantic equality, how many distinct successors
   remain?

These are contract terms, not decisions to create public `results.py` or
`replacement.py` modules. Stage 4 assigns their smallest cohesive code
ownership.

### Conceptual sum

One generic envelope is used before and after commit:

```text
ResultEnvelope[P] =
    Complete(P)
  | Rejected(Fault)

RuleResult[C, W] =
    ResultEnvelope[OutcomeSpace[RuleAtom[C, W]]]

ApplicationResult[C] =
    ResultEnvelope[ApplicationComplete[C]]

RuleAtom[C, W] =
    Derivation(
        replacement: TotalDisposition[W],
        progress: Advanced | Quiescent,
        continuation: Continue | Stop(TerminalReason),
        witness: Witness,
        provenance: Provenance,
    )
  | NoSuccessor(
        outcome: Terminal | Undefined | DeclaredFailure | Divergent,
        reason: Reason,
        witness: Witness,
        provenance: Provenance,
    )

AppliedAtom[C] =
    AppliedDerivation(
        successor: C,
        source: Derivation,
        fresh_bindings,
        output_trace_lineage,
        evidence,
    )
  | AppliedNoSuccessor(source: NoSuccessor, output_trace_lineage, evidence)

ApplicationComplete[C] = {
    source_outcomes: OutcomeSpace[RuleAtom],
    applied_atoms: SupportSpace[AppliedAtom],
    no_successor_partition: SupportSpace[AppliedNoSuccessor],
    outcome_atom_cardinality: Cardinality,
    derivation_cardinality: Cardinality,
    successor_cardinality: Cardinality,
    successor_quotient_with_derivation_fibers: SuccessorSpace[C],
    applied_atom_measure: MeasureView[AppliedAtom],
    successor_submeasure: MeasureView[SuccessorGroup[C]],
    no_successor_submeasure: MeasureView[AppliedNoSuccessor],
    evidence: ApplicationEvidence,
}

MeasureView[P] =
    Absent
  | Available(Measure[P])
  | Unavailable(reason, retained_source_law_and_mapping_evidence)

SuccessorSpace[C] = SupportSpace[SuccessorGroup[C]]
SuccessorGroup[C] = semantic_equivalence_class_or_intensional_point
                    + complete_applied_derivation_fiber
```

The derived `no_successor_partition` may of course be empty; it is a typed
projection of a validated Rule support—possibly intensional and of
undetermined cardinality—not a standalone claim that an exact empty Rule
result is meaningful.

`MeasureView` has exact invariants. With no source probability law, all three
views are `Absent`. With a source law and `Complete` application, the full
applied-atom measure and its tagged no-successor submeasure are `Available`.
The successor-group submeasure is also `Available` when the quotient is
measurable; only that derived view may be `Unavailable` when quotient
measurability cannot be established. An invalid source law or applied mapping
rejects the application rather than producing `Unavailable`.

`Complete` means that its payload is authoritative at that boundary.
For a Rule result, the represented atoms are both sound in and covering of the
specialized denotation `⟦Rule⟧(R, W)`, up to the descriptor's declared exact
equivalence. For an application result, every generic phase has completed and
the payload above retains both the pre-quotient derivations and every derived
view. An intensional presentation can be complete while its cardinality is
undecidable; completeness is coverage, not enumerability.

`Rejected` means there is no authoritative denotation or successor space to
commit or expose at that boundary. `RuleResult` can originate Rule-denotation
or result-schema faults; `ApplicationResult` can additionally originate
earlier program/input/region faults or later fresh/commit/successor/quotient
faults. Denotational Rule/application faults are closed invalid-data/result,
unsupported-exactness/capability, or evaluation-failure variants with phase,
reason, and evidence. `ResourceExhausted` belongs only to an explicitly
bounded external query, realization, or rollout result; it is not a base
Rule/Application fault.

The successful semantic outcomes are distinct:

| Outcome | Replacement? | Meaning |
|---|---:|---|
| `Advanced` | Yes | A semantic event occurred; the resulting `C` may still equal the input |
| `Quiescent` | Yes, identity | No configuration change; Rule declares no construction event |
| `Terminal` | No, or `Stop` after one | The relation completed and declares no continuation |
| `Undefined` | No | The valid input lies outside the mathematical relation's domain |
| `DeclaredFailure` | No | The construction itself denotes a typed failure rather than a successor |
| `Divergent` | No | Noncompletion is part of the denotation and is supported by a closed certificate |

`Invalid` is a rejected contract/input/result, not a mathematical empty
relation. `Unsupported` says the requested exactness or capability is not
implemented; it cannot be promoted to `Undefined`. `ResourceExhausted` says a
bounded attempt did not establish the full result; it cannot be promoted to
`Divergent`, `Terminal`, or exact zero. An unbounded semidecision that has not
halted simply remains unevaluated; only a semantic divergence certificate may
produce `Divergent`. Resource exhaustion originates only from an explicit
bounded realization, query, or rollout request; it is not an atom invented by
the denotational Rule.

`Quiescent` is deliberately an identity derivation rather than an empty
outcome space. It may retain a witness or external draw evidence without
pretending the configuration changed. If a same-state branch records a
construction event, advances visible control, or changes future applicability,
it is `Advanced`. Likewise, a one-shot function can return an `Advanced` derivation with
`Stop(Completed)`: it produces a successor/result once without inventing a
second application.

### Cardinality and presentation

`OutcomeSpace[P]` keeps support and measure separate:

```text
OutcomeSpace[P] = {
    support: SupportSpace[P],
    probability_law: Absent | ProbabilityLaw[P],
}

SupportSpace[P] = {
    presentation: Finite[P] | Intensional[P],
    cardinality: Cardinality,
    completeness_evidence: CompletenessEvidence,
}
```

| Presentation | Contract |
|---|---|
| `Finite` | Canonical finite atoms with exact order-insensitive or declared ordered/bag semantics |
| `Intensional` | A versioned relation AST with binding, membership/construction, validation, and universal conformance obligations |

An optional `ProbabilityLaw[P]` is a closed normalized measure over either
support presentation. It changes neither the support presentation nor its
cardinality and is never inferred from weights, multiplicity, amplitudes, or
enumeration.

Every support or quotient carries a cardinality claim:

```text
ExactlyZero
ExactlyOne
Many(exact_finite_size | countably_infinite | uncountable)
Undetermined(closed_reason_or_obligation)
```

`Undetermined` is not a guessed `Many` and not an operational failure. It is an
exact intensional relation whose emptiness, uniqueness, or multiplicity is not
established by the descriptor. A finite presentation may not use it.

When a complete result **establishes** `ExactlyZero` replacement derivations,
it still carries a typed `NoSuccessor` atom explaining terminality,
undefinedness, declared failure, or certified divergence. A bare finite or
claimed-exact empty outcome container is invalid; certified zero is never left
semantically untyped. This does not decide the emptiness of an intensional
relation whose cardinality is `Undetermined`: that relation remains the
complete result and must not invent `Terminal` or any other `NoSuccessor`
atom. If emptiness is later certified, coverage evidence and the typed
no-successor outcome must be supplied together.

Results report three cardinalities rather than conflating them:

- outcome-atom cardinality, including terminal or other no-successor atoms;
- replacement-derivation cardinality before deduplication; and
- distinct-successor cardinality after commit and semantic quotient.

Thus an epsilon word is one successor whose value is empty, not zero
successors; a quiescent identity is one replacement derivation; a terminal
no-match is zero replacement derivations with a typed terminal atom; and a
diamond may have many derivations but one distinct successor. For a rejected
application or resource-exhausted external request, semantic cardinality is
**not established**; the number of candidates observed so far is only
diagnostic evidence.

An intensional space is never a Python generator or an opaque solver result.
It must support both:

- **soundness**: every represented atom belongs to the specialized
  `⟦Rule⟧(R, W)` relation and satisfies totality, authorization, and invariant
  obligations; and
- **coverage**: every atom in that specialized Rule relation is represented,
  up to its declared exact equivalence.

The intensional AST may discharge coverage by being the specialized Rule
relation itself together with its closed equivalence and conformance
contracts. A finite claim such as “the solutions of `x² = 1` are `{+1}`” is
not `Complete`, even though its sole member is sound. Likewise,
`Terminal(NoSolution)` requires a closed emptiness/coverage certificate, not
merely the absence of a found member. If soundness or coverage cannot be
validated, the boundary returns a typed unsupported/incomplete rejection.

A solver may return verified members, samples, or a certified complete finite
realization, but a partial enumeration never masquerades as the complete
outcome space.

### Closed Rule denotation

The core Rule operation is denotational:

```text
Rule.denote(R, W) -> RuleResult[C, W]
```

It constructs or interprets only recognized closed structural data. It may
return a finite support or an intensional relation descriptor, but it does not
draw randomness, invoke a solver, numerically integrate, conduct partial
search, consume a resource budget, or consult host callbacks. Those actions
belong to explicit external realization/query requests over the retained
denotation. Consequently base `apply` has no resource request and cannot
originate `ResourceExhausted`; bounded external operations may do so without
changing the Rule result. A `Divergent` atom is permitted only when the closed
Rule data itself supplies a valid semantic certificate.

### Total replacements and outcome invariants

Each `Derivation` contains one already resolved, conflict-free
`TotalDisposition[W]`:

```text
existing capability -> Preserve | Replace(payload) | Delete
fresh capability    -> Absent   | Create(payload)
outside W           -> Preserve
```

The payload is typed by the writable capability. It may be an
Alphabet-conforming stored value, a whole component, edge/incidence record,
order relation, span, field restriction, or other closed structural
replacement validated by `C`. Thus rerouting an existing edge or changing
stored order is explicit without pretending topology is an Alphabet value.

Sparse wire/storage form is permitted only with a closed default that makes
this total meaning recoverable. Duplicate or contradictory dispositions,
overlapping structural edits without one resolved meaning, unauthorized
incident/interface effects, and out-of-`W` targets reject the whole
`RuleResult`; generic application never chooses a winner or drops a bad
alternative.

All semantic schedule, match, priority, overlap, collision, newborn deferral,
projection, deletion closure, and stochastic choice have therefore already
been resolved by Rule data into the atom space. Commit performs no such
choice. `Quiescent` must commit to a configuration semantically equal to the
input and contain no create/delete or eventful effect. `Advanced` may commit to
an equal configuration when the witness records a meaningful identity event.

### Witnesses, lineage, and successor quotient

A `Witness` is closed structural evidence identifying a derivation independently
of enumeration:

- Rule clause, match, addressed occurrence, branch parameter, and semantic
  choice are explicit;
- its canonical identity is stable across serialization, traversal, parallel
  realization, finite materialization, and presentation order; and
- together with the program, old snapshot, `R`, and `W`, it is sufficient to
  verify the atom and reproduce its complete disposition.

Application captures an `AppliedDerivation` before any successor
canonicalization. It retains the Rule witness, input trace lineage, raw
replacement, fresh bindings, progress/continuation, source provenance, and
any realization evidence. It also carries
`output_trace_lineage = derive(input_trace_lineage,
canonical_application_identity, witness, outcome)`. The canonical application
identity is constructed once from canonical program identity, input
configuration identity, and resolved readable/writable binding identities, as
shown below. Trace lineage is evidence, not hidden configuration: it cannot
change the denotational Rule result, structural fresh identities, or semantic
successor equality. If ancestry affects later mechanics, it is visible state
in `C`.

Only then may successors be grouped. Deduplication uses the configuration
contract's exact semantic equality or an explicitly declared sound
canonicalization/alpha-equivalence. It never uses storage order, rendering,
coordinates, hashes alone, approximate numeric equality, or a catalog name.
When equality or quotient construction is undecidable, the result retains a
derivation-indexed/intensional successor space and states that the quotient is
undetermined rather than guessing.

Each successor group retains its complete derivation fiber. Equal successors
therefore do not erase different matches, parents, probabilities, terminal
flags, or event histories. The denotational transition relation uses unique
semantic successors; if multiplicity must affect later mechanics, it must be
represented in `C` or in the probability measure, not recovered from a lossy
branch count.

### Probability and replay

A stochastic Rule denotes a probability measure over the complete
`RuleAtom` space. The measure may include replacement, terminal, undefined,
declared-failure, or divergent atoms. Before commit, application validates the
law's support, outcome/provenance tags, normalization evidence, and measurable
atom space. Any missing mass must be assigned an explicit semantic atom rather
than silently discarded. Arbitrary scores, complex amplitudes, objective
weights, and unnormalized factors are distinct value/annotation algebras and
grant no sampling authority until a Rule explicitly constructs a probability
measure.

Atomic application first pushes the measure to the full tagged
`AppliedAtom` space, preserving all replacement, terminal, undefined,
declared-failure, divergence, progress, and continuation mass. Successor
grouping is a second projection of the replacement-atom portion only. It
produces an **unnormalized successor submeasure** and a separate no-successor
submeasure; neither is renormalized when the other has positive mass. Mixed
`Continue`/`Stop` fibers likewise retain their tagged mass. In a finite space,
equal successor mass is the exact sum of its derivation masses.

For an intensional or continuous law, the atom/configuration spaces and the
validation, reconstruction, and quotient maps must carry closed measurable
contracts. If the full applied-atom pushforward is valid but measurability of
the semantic successor quotient cannot be established, application retains
the source law and applied mapping, marks `successor_submeasure` as
`Unavailable`, and never fabricates a pushforward. Finite closed spaces are
measurable by construction.

A probability law is never a draw. A realization request outside
`SimpleProgram` supplies a replay key and representation/profile request. A
realized atom records:

- the canonical law and application identities;
- the structurally derived subkey/coordinate;
- sampler and numeric-representation schema versions;
- the selected witness/atom or represented sample; and
- enough evidence to replay and revalidate the full application result.

The current draw's subkey derives from root realization evidence, the current
application's **input** trace lineage, canonical law/application identity, and
semantic draw labels—not loop order, worker scheduling, or the atom not yet
selected. After selection, the chosen witness/outcome determines the
derivation's output trace lineage; rollout uses that as the next application's
input lineage. Ambient RNG state is forbidden. Draw evidence remains
result/trace metadata unless later Rule mechanics reads it, in which case the
relevant state is explicitly stored in `C`.

### Fresh identity binding

Rule replacements name fresh components with closed local keys. Generic
application validates and binds them by the semantic structural scope:

```text
FreshIdentity(
    input_configuration_identity,
    canonical_rule_identity,
    derivation_witness,
    parent_or_interface,
    namespace,
    local_key,
)
```

Repeated references to one local key denote one component; distinct authorized
keys must not collide. Binding is independent of UUIDs, process state, global
counters, branch indices, traversal, or materialization order. The fresh
component plus every created incident/interface relation must be present in
`W` and in the total disposition. If `C` declares those identities
alpha-renamable, canonical successor equality may later quotient the names;
the raw binding, witness, and separate trace lineage remain available for
replay. Two semantically equal inputs cannot acquire different semantic
successors merely because they arrived through different external trace paths.

## Shared Loci and Region Algebra

`loci.py` supplies structural identity and selection vocabulary shared by
configuration carriers, Frontier, and Neighborhood. Sharing an algebra does
not merge read and write capabilities.

### Locus forms

The algebra must represent, compositionally:

- rank-independent coordinates and named/register/wire keys;
- ordered sequence occurrences, indices, spans, prefix/tail boundaries, and
  end markers;
- tree paths, nodes, child slots, binders, and subtrees;
- graph vertices, edges, ports, dangling interfaces, paths, and reachability
  references;
- product/record field paths and dynamically addressed components;
- regions, intervals, cells, points, field components, and differential germs;
- event/history identities, parents, producers, and provenance references; and
- potential fresh components with structural birth namespaces.

Identity is semantic where mechanics require it. Occurrences are not collapsed
to equal values, bags retain multiplicity, ordered structures retain order, and
graphs state alpha-equivalence/canonicalization explicitly.

Fresh identities are stable semantic local keys, never ambient UUIDs, object
addresses, global counters, traversal positions, branch-enumeration indices,
or materialization order. A fresh reference is scoped by the validated input
configuration's semantic identity, canonical Rule identity,
derivation/witness identity, parent or interface, and a closed local
namespace/key supplied by the replacement.
External trace lineage remains evidence and cannot alter the semantic
reference. The result/application contract above fixes collision and
cross-branch rules; codecs must represent the reference losslessly without
first enumerating an intensional result set.

### Selector and region forms

Reusable closed selectors include:

- literal, named, all-support, tagged, and value-role regions;
- relative offsets, dilation, metric regions, shells, and boundary-aware
  restrictions;
- spans, prefixes, suffixes, extents, cursor-relative regions, and match
  regions;
- graph incidence, ports, paths, reachability, and matched interfaces;
- product, projection, image, union, intersection, difference, and disjoint
  union;
- dynamic address and configuration-derived selectors;
- history/provenance selectors;
- fresh-child, fresh-edge, and replacement-shape capabilities; and
- continuous, differential, symbolic, and other intensional regions.

Predicates and transformations inside selectors are closed AST nodes. A
selector may resolve to a finite ordered view, a set, a bag, a keyed product, a
hierarchical structure, a field restriction, or an intensional membership
contract. Materialization is an optimization or run request, not part of its
identity.

WritableRegion wraps selector results as capabilities. ReadableRegion wraps
them as observations and may attach values/structure. A raw selector by itself
authorizes neither reading nor writing.

### Dynamic support

Dynamic support is represented without a fixed coordinate universe:

1. `C` describes the current carrier and its identity rules.
2. Frontier resolves existing writable structure plus permitted fresh
   capabilities.
3. Neighborhood exposes the old structure and any interfaces Rule needs.
4. Rule returns a structural replacement that creates, deletes, or relabels
   within those capabilities.
5. The successor `C` carries its new support and still satisfies its
   invariants.

This covers growing words, graph birth/rerouting, tree expansion, moving
surface rims, deletion processes, and continuous unknown/evolving regions
without `Domain`, `Shape`, or `UpdatePolicy` fields.

## Composition and Constructor Progression

Each plural component module is a constructor algebra for one singular program
field:

| Module | Primitive examples | Compound/general examples |
|---|---|---|
| `seeds` | exact, empty, point, literal, law | product, overlay, refinement, mixture, constructive, partial, intensional |
| `alphabets` | boolean, enum, integer, rational, represented real | tagged, product, record, word, instruction, symbolic, field |
| `frontiers` | literal, all, tagged, named | union, product, relative, matched interface, dynamic address, fresh support, intensional |
| `neighborhoods` | self, literal, offsets, named read | product, around, span, path, history, global, metric, differential, intensional |
| `rules` | table, clause, expression, pattern, equation | ordered choice, conditional, product, parallel, relation, distribution, phase control |

The progression inside each module is:

```text
primitives -> compounds -> general constructors -> useful component presets
```

Whole-program constructors and semantic aliases belong in `catalog/`, where
they compose these five component values. `SimpleProgram` never stores tuples
of “multiple alphabets,” “multiple frontiers,” or “multiple rules” merely
because construction used several pieces; the corresponding module combines
them into one value with explicit semantics.

## Cross-Field Validation

Validation has four layers. They must not be collapsed into “the tests passed.”

### 1. Descriptor validity

For each component independently:

- tag and version are known;
- fields are complete, typed, and canonical;
- recursion/references are bound and acyclic where required;
- exactness and representation profiles are explicit;
- no opaque executable object or hidden entropy source is present; and
- local invariants of the descriptor hold.

### 2. Program compatibility

Construction of `SimpleProgram[C, V, W, R]` must verify:

1. Seed's output contract unifies with `C`.
2. Every semantic Seed value conforms to `Alphabet[V]`, including explicit
   unresolved/control roles.
3. Frontier accepts `C` and resolves a `W` whose existing/fresh target kinds
   are valid for the carrier and Alphabet.
4. Neighborhood accepts the same `C` and resolves the `R` shape Rule declares;
   both resolutions share a snapshot binding and canonical locus identities,
   and Rule's declared `R`-to-`W` join/index shape is structurally compatible.
5. Rule accepts exactly that `R` and `W`, emits replacements of `C`, and
   declares write/value/invariant requirements compatible with Frontier and
   Alphabet.
6. The closed requirement/effect judgments prove
   `reads(rule) ⊆ neighborhood` and `effects(rule) ⊆ frontier`; Frontier is
   never counted as a read, and Neighborhood never authorizes an effect.
7. Exact, represented, probabilistic, continuous, and symbolic profiles agree
   across all participating descriptors.
8. Any required initialization or transition entropy interface is explicit
   and replayable.

Compatibility uses structural type unification, capability inclusion, and
closed requirements/effects—not class-name equality or family dispatch.
Provable read, effect, or join mismatches are construction errors. When a
symbolic/intensional inclusion is not decidable, the descriptor must carry a
closed proof or conformance obligation that the implementation can validate;
the application boundary still validates every realized target and resolved
join. “Unknown” never degrades into assumed compatibility.

### 3. Configuration validity

Every realized Seed output and every proposed successor must validate:

- carrier/support/topology/geometry well-formedness;
- Alphabet conformance;
- defaults/boundaries and totality/partiality declarations;
- identity, order, multiplicity, and interface rules; and
- configuration invariants.

### 4. Application validity

The universal application law below checks:

- Frontier and Neighborhood resolve against the same immutable `C`;
- their snapshot binding, locus identities, and declared `R`-to-`W` join
  validate;
- Rule used no undeclared read capability;
- actual replacements lie within `W`;
- fresh identities and structural edits are valid;
- replacement values conform to Alphabet; and
- each committed successor is a valid `C`.

Some invariant-preservation claims are not decidable at construction time.
They remain explicit closed proof/conformance obligations or checked
pre/postconditions; the library may not silently infer them. A structurally
well-formed user Rule can still yield a typed invalid result if a proposed
successor violates its declared contract.

Required error categories include invalid/unknown descriptor, incompatible
configuration type, Alphabet violation, invalid region, missing read
capability, unauthorized write schema, invariant violation, unsupported
exactness, and missing entropy/replay evidence. The result algebra integrates
these with outcomes; Stage 4 assigns their minimal code ownership.

## Universal Atomic Application

One application is the only semantic execution primitive:

```text
apply(
    program: SimpleProgram[C, V, W, R],
    input: ApplicationInput[C],
) -> ApplicationResult[C]
```

`ApplicationInput` supplies one immutable configuration snapshot and validated
trace lineage. Seed realization supplies a root trace lineage; direct
application may derive one canonically for evidence. This lineage scopes raw
events and replay subkeys but does not alter the semantic configuration,
Rule denotation, or fresh component identity. It is invocation data, not a
sixth program component.

`require_valid_program` derives an ephemeral compatibility certificate. Among
its associated evidence is the configuration contract `C` shared by all five
fields; `C` is not stored as `program.C`. Input and successor validation use
that contract and the Alphabet. Successors need not belong to the Seed's
initial support: Seed constrains sources, not the transition codomain.

`ApplicationResult` contains the mapped Rule outcome space, applied
derivations, semantic successor groups or an intensional successor relation,
no-successor outcomes, measures, faults, and replay/provenance evidence.
Stage 4 decides the smallest public spelling and ownership for these contract
records.

The internal `commit` operation is a pure, family-blind structural operation:

```text
commit(
    ReconstructionPlan[C, W],
    C,
    TotalDisposition[W],
    FreshBindings,
) -> C | Fault
```

It is not configurable, public policy, proposal arbitration, or a place to
infer construction mechanics.

### Closed reconstruction plan

Every validated writable resolution yields a sealed, versioned
`ReconstructionPlan[C, W]`: an application-private, snapshot-bound structural
lens assembled from recognized loci, carrier, product, and region primitives.
Rule receives `W`, not this plan. The plan is serializable validation evidence
and contains no host callback, family tag, catalog alias, solver, readable
snapshot values, or semantic choice. Given a validated normalized disposition,
it:

- identifies the unique inside/outside decomposition induced by `W`;
- preserves the entire outside projection;
- covers every existing and fresh target exactly once;
- applies all replacements, creations, and deletions simultaneously;
- rebuilds one `C` while preserving occurrence/interface identity rules; and
- for intensional spaces, denotes the same reconstruction as a closed
  relation/map without forcing enumeration.

The plan must prove or carry obligations for lens laws, unique target
normalization, structural closure, and—when a probability law is present—
measurability of its reconstruction map. It can rebuild a graph reroute,
ordered insertion, field restriction, or symbolic/intensional overlay because
those are typed replacement payloads plus structural lenses. It cannot choose
a match, cascade a deletion, fill an unspecified gap, resolve an overlap, or
select an endpoint. Those construction decisions already belong to Rule.
Thus reconstruction supplies the generic meaning of “apply this explicit
replacement”; it is not `UpdatePolicy`.

### Application law

The normative algorithm is:

```text
apply(program, input):
    p := program
    compatibility := require_valid_program(p)
    C_contract := compatibility.configuration_contract
    s := freeze_and_validate(
        input.configuration,
        input.trace_lineage,
        C_contract,
        p.alphabet,
    )

    writable_resolution := validate_writable(
        p.frontier.resolve(s),
        snapshot=s.identity,
        configuration_contract=C_contract,
    )
    w := writable_resolution.capabilities
    r := validate_readable(
        p.neighborhood.resolve(s),
        snapshot=s.identity,
        configuration_contract=C_contract,
    )
    reconstruction := require_closed_reconstruction_plan(
        writable_resolution,
        C_contract,
    )
    require_same_snapshot_and_declared_join(
        s, r, w, reconstruction, compatibility
    )

    application_identity := CanonicalApplicationIdentity(
        canonical_program_identity=identity(p),
        input_configuration_identity=s.configuration_identity,
        readable_binding_identity=identity(r),
        writable_binding_identity=identity(w),
    )

    rr := p.rule.denote(r, w)

    if rr is Rejected(fault):
        return no_commit_application_result(fault, accumulated_evidence)

    # Phase 1: validate the whole closed Rule outcome space.
    validated := validate_complete_rule_space(
        rr.payload,
        specialized_denotation=denotation_of(p.rule, r, w),
        require_schema_tag_and_version=True,
        require_soundness_and_coverage=True,
        require_cardinality_certificate=True,
        require_witness_provenance_outcome_evidence=True,
        require_total_dispositions_and_authorized_effects=w,
        require_payload_contracts=(C_contract, p.alphabet),
        require_probability_support_normalization_and_measurability=True,
    )

    # Phase 2: bind fresh identities across every derivation.
    fresh_space := bind_all_fresh_closed(
        validated,
        input_configuration_identity=s.configuration_identity,
        canonical_rule_identity=identity(p.rule),
        writable=w,
    )

    # Phase 3: reconstruct every alternative from the same old snapshot.
    candidate_space := reconstruct_all_closed(
        reconstruction,
        s.configuration,
        validated,
        fresh_space,
    )

    # Phase 4: validate every successor and progress/continuation assertion.
    applied_atoms := validate_all_successors_closed(
        candidate_space,
        C_contract,
        p.alphabet,
        source=s.configuration,
        output_lineage_from=(
            input.trace_lineage,
            application_identity,
        ),
    )

    # Phase 5: form exact views only after every witness is retained.
    groups := semantic_successor_quotient_with_derivation_fibers(applied_atoms)
    applied_atom_measure := push_forward_to_full_applied_atom_space(
        validated.probability_law,
        applied_atoms,
    )
    successor_submeasure, no_successor_submeasure := project_submeasures(
        applied_atom_measure,
        groups,
        renormalize=False,
        retain_unavailable_mapping_evidence=True,
    )

    return Complete(ApplicationComplete(
        source_outcomes=validated,
        applied_atoms=applied_atoms,
        no_successor_partition=partition_no_successor(applied_atoms),
        outcome_atom_cardinality=validated.support.cardinality,
        derivation_cardinality=derivation_cardinality(applied_atoms),
        successor_cardinality=cardinality(groups),
        successor_quotient_with_derivation_fibers=groups,
        applied_atom_measure=applied_atom_measure,
        successor_submeasure=successor_submeasure,
        no_successor_submeasure=no_successor_submeasure,
        evidence=accumulated_evidence,
    ))
```

Each numbered operation is a **phase-wide closed pass**. No later phase runs
when an earlier phase has any fault, and no successor becomes authoritative
until its entire phase succeeds. A finite phase reports a canonical nonempty
set of faults (or its canonical structurally least member), never the
traversal-first failure. For an intensional space, each pass is a closed
relation composition with a universal phase conformance obligation; every
realized member is checked again at that boundary. This defines “the first
failing phase” without implying enumeration order.

Validated `NoSuccessor` atoms pass through fresh binding and reconstruction
without allocating or committing anything; the successor-validation phase
maps them to `AppliedNoSuccessor` while deriving their output trace lineage and
retaining their witness, reason, provenance, and probability mass.

Result-space validation includes exact schema/tag/version checks;
soundness-and-coverage equivalence to the specialized Rule denotation;
cardinality evidence; atom witness, provenance, outcome reason, and certificate
validation; total disposition/effect/payload conformance; probability support,
normalization, and measurable-space evidence; and canonical serialized fault
tags/reasons. `Terminal(NoSolution)` and semantic divergence therefore require
their own closed evidence. A partial solver enumeration cannot pass this
phase.

All derivations read the same old snapshot and reconstruct independently as
alternative possible worlds. No derivation observes another's output. A finite
result containing any invalid derivation rejects the complete result; valid
branches are not silently kept while invalid branches are discarded. An
intensional result without adequate universal obligations is rejected as
unsupported/incomplete rather than trusted.

The semantic commit law for every successful derivation `d` is:

```text
successor(d) | outside(W) = input | outside(W)
successor(d) | inside(W)  = reconstruction(
    input,
    total_disposition(d),
    fresh(d),
)
valid_C(successor(d))
```

There is no mutation before all checks for the phase succeed, and the immutable
input is never modified. Failure evidence may report a proposed target or
candidate, but no partial candidate becomes an authoritative successor.

### Failure phases and no-commit rule

Every rejected/incomplete application names the first failing generic phase:

| Phase | Representative faults |
|---|---|
| Program | Unknown descriptor/version, incompatible five-field contracts |
| Input | Invalid carrier/value/invariant or invalid/forged trace lineage |
| Frontier | Invalid capability, target kind, or snapshot binding |
| Neighborhood | Invalid read view, missing dependency, or snapshot binding |
| Join | Mismatched identities/index shape or unresolved obligation |
| Rule denotation | Invalid/unsupported closed Rule result or denotation failure |
| Result validation | Unsound/incomplete support, invalid cardinality/law, incomplete disposition, unauthorized effect, invalid payload, malformed witness/evidence |
| Fresh binding | Unauthorized namespace, collision, invalid parent/interface |
| Commit | Structural operation cannot realize the already specified replacement |
| Successor | Carrier, Alphabet, identity, interface, or invariant violation |
| Quotient/measure | Unsound canonicalization or invalid probability law/pushforward |

Application stops after the first failing phase; later semantic phases do not
execute. In particular, resolution failure prevents Rule denotation, and any
result/fresh/commit/successor fault yields no authoritative successor space.
This phase ordering is testable with instrumented closed structural
descriptors and does not depend on a family or traversal order.

Application may dispatch on the sealed generic sum variants above and invoke
recognized structural descriptor operations. It may not inspect catalog
metadata, family IDs, constructor names, Book sources, semantic classes,
carrier labels, locus kinds, or Rule tags to choose a different algorithm.

## Application, Realization, and Rollout Boundary

The denotational `apply` operation returns the complete finite or intensional
application result. It does not choose a horizon, solver, sample, branch,
projection, or rendering.

External operations have separate responsibilities:

| Concern | Boundary |
|---|---|
| Seed realization | Select one or more initial `C` values from a Seed law with root replay evidence |
| Finite/intensional query | Ask a scoped question of an application result and return verified complete, partial, sample, unknown, or resource-limited evidence |
| Stochastic realization | Draw from the retained probability law with an explicit replay key |
| Rollout | Reapply the same family-blind `apply` relation to continuing successors |
| Resource limits | Bound query/realization/traversal and report truncation without changing denotation |
| Trace | Retain raw configurations, application records, edges, witnesses, lineage, outcomes, and draw evidence |
| Observer/render/export | Produce downstream views that do not redefine configuration or result identity |

Repeated rollout is derived relational traversal:

1. realize or bind the Seed's initial outcome space;
2. apply the program to each continuing
   `(semantic successor C, output trace lineage)` derivation fiber;
3. retain the raw application graph, including all incoming derivation fibers
   for equal successor configurations;
4. propagate exact measures or derive replay subkeys structurally for sampled
   paths; and
5. stop a branch on its Rule-declared `Stop`/terminal atom or report a
   request-bound truncation.

For a many-successor result, an exhaustive rollout yields a branching or
intensional path space. A request may sample, select, bound, or project it, but
that request cannot masquerade as the full transition relation. Raw and
sampled rollout expands every continuing `(C, output trace lineage)` fiber so
that replay keys and path evidence remain distinct. The unique-`C` successor
quotient is an aggregation/reporting view, not the default place to erase
branches.

An executor may memoize or expand one representative of equal `C` values only
after proving lineage independence of the denotational application, and it
must reinstantiate each path's output lineage, continuation, evidence, and
draw coordinates. If multiplicity or ancestry affects future mechanics, that
information is already semantic state in `C` or an explicit measure rather
than hidden lineage.

Continuation remains attached to each derivation fiber. If equal successor
configurations have both `Continue` and `Stop` derivations, rollout records the
stopped paths and expands the continuing fiber; grouping equal `C` values
never selects one continuation for the other.

A horizon is never a terminal reason. Reaching one returns a typed truncated
run with still-continuing leaves. Likewise, stopping early on a quiescent
identity is a run choice unless the derivation itself declares `Stop`.
Resource exhaustion, cancellation, pruning, and approximate realization never
prove terminality, undefinedness, divergence, unsatisfiability, or exact
cardinality.

One-shot relations normally return an `Advanced + Stop` derivation,
`Terminal`, `Undefined`, or an intensional answer space from one application.
They are complete without `rollout`. A continuous Rule may commit an endpoint
only when a selector/duration is closed Rule data or visible in `C`/`R`, or an
intrinsic event or singularity determines it. An event-free ordinary flow with
no such semantic selector instead writes or returns its maximal flow/solution
object, normally as `Advanced + Stop`, which an external horizon can query
without changing the denotation. PDEs likewise may return an intensional
solution relation. Numerical stepping, endpoint selection, or solver search is
a qualified external realization/query or a separately seeded work program,
not hidden application semantics.

The intended `ca.rollout` surface is therefore tooling over `apply`, not a
stored component and not the definition of a program. Stage 4 settles its
public request/result spelling without reopening this semantic boundary.

## Serialization Contract

Serialization is cross-cutting infrastructure, not a component, semantic axis,
or execution registry.

Every semantic node must have:

- a stable schema tag and version independent of Python class/module names;
- an exact allowed-field set with missing/extra/duplicate fields rejected;
- a canonical structural encoding;
- a fail-closed decoder for unknown tags, versions, primitives, and migration
  paths; and
- a lossless round trip preserving all distinctions that can affect a later
  application.

The canonical program payload contains exactly:

```text
seed
alphabet
frontier
neighborhood
rule
```

Canonical program serialization always contains the validated, expanded five
fields. An outer envelope may carry schema version, provenance, derived
digest, and an optional catalog construction receipt, but none changes
semantic identity or substitutes for that payload. A receipt is retained only
after verifying that its alias and arguments reconstruct the same canonical
five-field value. An alias-only recipe may be accepted as noncanonical
construction input, but it is never an authoritative lossless encoding.
Execution never dispatches on an alias.

Exact encoding obligations include:

- arbitrary-size signed integers and normalized rationals;
- algebraic, certified, represented-real, complex, probability, and symbolic
  profiles without numeric collapse;
- tagged sums and product/record field identity;
- order, multiplicity, absence, default, boundary, and partial/unknown roles;
- graph/tree/word identities, interfaces, alpha-equivalence rules, and fresh
  structural references;
- continuous/intensional ASTs without forced enumeration;
- probability laws separately from concrete draw/replay evidence;
- Rule/Application result sum tags, typed reasons/phases, progress,
  continuation, all three cardinality claims, and soundness/coverage evidence;
- total dispositions, pre-quotient witnesses/derivations, fresh bindings,
  output trace lineages, successor fibers, and intensional conformance
  obligations;
- reconstruction plans/lens obligations and `Absent`/`Available`/`Unavailable`
  measure views, including unrenormalized successor/no-successor submeasures;
- and representation relations and provenance needed for inverse-on-image and
  one-step commutation.

Maps, sets, bags, graphs, and symbolic binders require explicit canonical
ordering or equivalence rules. Object identity, memory address, Python hash,
ambient locale, NumPy dtype defaults, and machine floating behavior cannot
enter semantic identity.

Version migration is accepted only when total, validated, and lossless for the
claimed semantic profile. Otherwise decoding returns a typed unsupported or
invalid result; it never fills old fields with convenient defaults.

Program IDs and digests are derived from validated canonical structure. They
are cache/provenance aids, never authority. Mutating payload under a retained
ID or retaining payload under a forged ID must fail or rederive the ID.

## Stage 2 Paper Type-Checks

These examples test the contracts, not final constructor spelling.
Each fixture must discharge the same judgment:

```text
seed : Seed[C]
c ∈ support(seed)  =>  valid_C(c) ∧ values(c) ⊆ V
frontier(c) = w : W
neighborhood(c) = r : R
same_snapshot(c, r, w) ∧ valid_join(r, w)
reconstruction(c, w) = plan : ReconstructionPlan[C, W]
rule.denote(r, w) = Complete(Q) : RuleResult[C, W]
q ∈ support(Q) ∧ q is Derivation
    => targets(q) ⊆ W ∧ total_disposition(q, W)
       ∧ valid_C(commit(plan, c, total_disposition(q), fresh(q)))
q ∈ support(Q) ∧ q is NoSuccessor
    => valid_outcome_reason_witness_and_coverage(q) ∧ no_commit(q)
```

The concrete bindings and representative result obligation are stated for
every fixture below; a suggestive field mapping alone is not a type-check.

### Ordinary cellular automaton — F053/T01

| Type | Binding |
|---|---|
| `C` | Immutable finite or default-backed lattice field with boundary/default data |
| `V` | Boolean or finite ordered cell value |
| `W` | All output sites for one shared pass |
| `R` | Identity-indexed old-snapshot local stencils |

- Seed supplies an exact or law-generated lattice satisfying carrier and value
  invariants.
- Alphabet validates finite cell values.
- Frontier authorizes the complete next-pass output region.
- Neighborhood exposes every old-snapshot stencil and the boundary reads it
  needs.
- Rule is one closed local table lifted over `W`, returning one complete shared
  replacement.

Judgment: for every valid seeded lattice `c`, `values(c) ⊆ V`,
`frontier(c) = w`, and `neighborhood(c) = r` share site identities and the old
snapshot. `rule(r, w)` returns complete dispositions for all output sites. A
representative result replaces each site from its corresponding old stencil,
targets exactly members of `w`, and commits to another valid lattice `C`.

No `Domain`, `Shape`, `Boundary`, `Time`, or `UpdatePolicy` field is required:
carrier extent and boundary data are in `C`, while synchronous-pass semantics
are in Rule.

### Mobile automaton/Turing machine — F031

| Type | Binding |
|---|---|
| `C` | Default-backed tape/grid with exactly one `Head(control, symbol)` tag |
| `V` | Tagged union of plain symbols and head/control payload |
| `W` | Head source, bounded write stencil, and every possible destination |
| `R` | Head/control data, readable stencil, and old destination contents |

- Seed establishes support, default values, and the exactly-one-head invariant.
- Frontier derives the full possible-write envelope around the tagged head.
- Neighborhood supplies every value the transition needs, including old
  destination contents.
- Rule selects the applicable transition, explicitly preserves or rewrites
  every relevant member, and returns one coupled source/destination result.

Judgment: for every valid exactly-one-head `c`, `values(c) ⊆ V`,
`frontier(c) = w` and `neighborhood(c) = r` resolve from the same head and tape
snapshot, and the transition join maps readable candidate identities to the
same writable identities. In a representative move, the source and selected
destination receive explicit dispositions, every other possible destination
in `w` is explicitly preserved, all targets remain in `w`, and commit restores
a valid exactly-one-head `C`.

The tagged source determines activity inside Rule. There is no firing
frontier, active-selector field, movement policy, or separate atomic update.

### Structural rewrite — F029/F052

| Type | Binding |
|---|---|
| `C` | Labeled graph/tree with stable occurrences, interfaces, and invariants |
| `V` | Tagged node/edge/port/operator/atom records |
| `W` | Union of selectable match regions, affected interfaces, and permitted fresh/deleted structure |
| `R` | Candidate matches, labels, structural context, external interfaces, and scan/schedule state |

- Seed supplies one well-formed structure and any visible scan/active state.
- Frontier authorizes every target any admitted match alternative can affect.
- Neighborhood exposes exact match context and dangling interfaces.
- Rule owns match choice, overlap/order semantics, and the complete
  interface-preserving replacement.

Judgment: for every valid seeded structure `c`, stored labels satisfy `V`;
`frontier(c) = w` includes the matched occurrences, every incident/interface
effect, and stable fresh capabilities, while `neighborhood(c) = r` exposes
those same occurrence identities in the old graph/tree. A representative
result explicitly deletes matched components and affected incident structure,
creates replacements under semantic fresh keys, and reconnects each external
interface. Every delete/create/rewire target is in `w`, the disposition is
total over `w`, and commit yields a well-formed `C`.

Variable size, deletion, graph birth, and fresh identity fit structural `W`
and `C`; no shape or graph-update axis is introduced.

### Constraint completion — F030

| Type | Binding |
|---|---|
| `C` | Partial assignment with explicit unknown roles, boundary data, templates, and obligations |
| `V` | Allowed values plus explicit unknown/obligation tags |
| `W` | The complete unknown assignment region |
| `R` | All overlapping local scopes and global seed/occurrence obligations |

- Seed denotes the partial problem instance rather than a fabricated dynamics.
- Frontier authorizes completion of every unknown.
- Neighborhood exposes all constraints needed to judge a complete assignment.
- Rule denotes zero, one, many, or an intensional set of satisfying complete
  replacements in one application.

Judgment: for every valid partial instance `c`, explicit known, unknown, and
obligation values conform to `V`; `frontier(c) = w` is the complete unknown
region and `neighborhood(c) = r` contains every referenced scope under the
same occurrence identities. `rule(r, w)` denotes an intensional or realized
set of alternatives. Each representative satisfying alternative replaces
every unknown in `w`, is total rather than solver-order-dependent, targets
  only `w`, and commits to a valid completed `C`; unsatisfiability is zero
  replacement derivations plus `Terminal(NoSolution)`, not an invalid sparse
  successor or a bare empty container.

Solver order, resource limit, realization bound, and query policy remain
external. No Solver, ResultPolicy, or special relation-program class is needed.

### Continuous flow — F037

| Type | Binding |
|---|---|
| `C` | Continuous state with domain/geometry, parameters, explicit time, optional endpoint selector, and result/event slots |
| `V` | Exact, certified, or explicitly represented scalar/vector/tensor and flow-segment values |
| `W` | Maximal-flow/result slot, plus state/time/reset slots only when closed Rule data, a visible selector, or an intrinsic event authorizes an endpoint |
| `R` | Current state/time, geometry, parameters, any visible endpoint selector, event surfaces, and required global data |

- Seed supplies the initial continuous state, time, side data, and exactness
  profile.
- Alphabet prevents represented numerics from impersonating exact values.
- Frontier intensionally denotes the maximal-flow/result slot and every
  state/time/reset slot closed Rule data, an intrinsic event, or a visible
  selector may update.
- Neighborhood exposes the vector field inputs and event dependencies in a
  closed view.
- Rule denotes zero, one, or many admissible maximal-flow objects or
  intrinsically/explicitly selected segment-endpoint replacements.

Judgment: for every valid continuous `c`, represented values conform to `V`;
`frontier(c) = w` and `neighborhood(c) = r` share the same state/time binding.
For an event-free ordinary flow with no semantic endpoint selector, a
representative alternative writes a maximal flow/germ/solution object to its
declared result slot, preserves state/time, and normally returns
`Advanced + Stop`; an external horizon may query that object but cannot
silently select a semantic endpoint. For an intrinsic event—or a
selector/duration encoded in closed Rule data or explicitly visible in
`C`/`R`—the alternative may instead write the selected segment, endpoint
state/time, and reset/event record atomically. In either case it targets only
`w`, gives every other writable slot an explicit disposition, and commits to a
valid `C`.

Time is visible state or a Rule variable. A run horizon and numerical
realization strategy are external policy unless the endpoint selector is
itself closed construction data in Rule or visible state.

### General PDE relation — F041

| Type | Binding |
|---|---|
| `C` | Partial continuous field with structural domain, geometry, equations, initial/boundary data, parameters, and explicit unknown roles |
| `V` | Exact, certified, represented-real, vector, tensor, distribution, symbolic, or field values |
| `W` | The complete unknown continuous solution field/parameter region |
| `R` | Geometry, equations, known field restrictions, boundary/side data, differential germs, and global dependencies |

- Seed supplies the partial field problem and exactness profile.
- Alphabet represents known/unknown field roles and prevents approximation
  profiles from masquerading as exact solutions.
- Frontier intensionally denotes the whole unknown solution region.
- Neighborhood supplies every local differential and global side condition.
- Rule denotes zero, one, many, or an intensional family of complete solution
  fields.

Judgment: for every valid PDE instance `c`, all stored data conform to `V`;
`frontier(c) = w` and `neighborhood(c) = r` share domain and field-component
identities. A representative intensional alternative assigns the entire
unknown field region in `w`, satisfies its declared equation and side-data
obligations, targets no exterior component, and commits to a valid solution
`C`. A numerical mesh is a qualified realization of that alternative, not the
denotation silently substituted for it.

Continuous support requires neither a finite coordinate universe nor a
top-level Time or trajectory field.

All five requested construction classes type-check without a sixth component;
the continuous class is deliberately split into flow and PDE fixtures because
their writable/result obligations differ. Together they exercise fixed
support, coupled writes, dynamic support, global relations,
continuous/intensional regions, exactness, and one-shot semantics.

## Stage 3 Application Pressure Executions

These executions test the result/application law rather than catalog
constructor spelling. Stage 6 later turns them and the other Goal 5 pressure
categories into the complete conformance plan.

### Outcome/cardinality distinctions

| Case | Rule result | Replacement derivations | Distinct successors | Required observation |
|---|---|---:|---:|---|
| Deterministic change | One `Advanced + Continue` atom | 1 | 1 | Ordinary application |
| Stable fixed point | One identity `Quiescent` atom | 1 | 1, equal to input | Not an empty result |
| Eventful identity | One identity `Advanced` atom | 1 | 1, equal to input | Witness/event retained; not quiescent |
| Completed one-shot | One `Advanced + Stop(Completed)` atom | 1 | 1 | Result exists; no invented next step |
| No applicable rewrite/halt | One `Terminal(reason)` atom | 0 | 0 | Exact terminal zero |
| Unsatisfiable completion | One `Terminal(NoSolution)` atom | 0 | 0 | Successful exact negative answer |
| Undefined partial function | One `Undefined(reason)` atom | 0 | 0 | Not terminal, invalid, or unsatisfied |
| Declared construction failure | One `DeclaredFailure(reason)` atom | 0 | 0 | Semantic failure remains typed |
| Certified divergence | One `Divergent(certificate)` atom | 0 | 0 | Distinct from timeout |
| Invalid result/input | `Rejected(Invalid(...))` | Not established | Not established | No commit and no exact-zero claim |
| Bounded external resource exhaustion | External `Rejected(ResourceExhausted(...))` | Not established | Not established | Never a Rule/base-application result; partial observations are diagnostic only |
| Diamond rewrite | Multiple witnessed derivations | Many | One or fewer than derivations | Dedup retains the full fiber |
| Empty output value | One replacement containing epsilon/empty carrier | 1 | 1 | Empty value is not empty relation |
| Intensional solution relation | Complete intensional space | Zero/one/many/undetermined | Intensional quotient | No forced enumeration |
| Possibly empty intensional relation | Complete intensional space with `Undetermined` cardinality | Undetermined | Undetermined | No fabricated terminal atom; unknown is not certified zero |
| Stochastic relation | Probability law over typed atoms | Law support | Pushforward support | Law, draw, and successor mass remain distinct |

Every row has a different serialized sum shape or typed field; none relies on
an English message or the length of a returned Python list.

### Coupled source/destination and field writes — F031/F007

For a mobile-head transition, `W` contains the source, complete write stencil,
and every possible destination. For coupled-field evolution it additionally
contains the whole field output and destructive marker target. `R` contains
all old values needed for the joint choice.

Rule returns one `Derivation` whose total disposition:

- rewrites the source and shared field;
- retags exactly the selected destination while explicitly preserving every
  unselected possible destination;
- performs the destructive target write where required; and
- advances or stops control with one witness naming the transition and chosen
  destination.

Application validates one snapshot/join and commits the disposition once. It
does not run a field pass and a mobile pass separately, recover destination
contents, or merge competing writes. Removing any possible target from `W`,
omitting an unselected destination's disposition, or returning two conflicting
values rejects the result before commit.

### Structural birth, deletion, and overlap — F029/F040

`W` contains candidate matched structure, every affected incident/interface
component, and a closed fresh namespace. `R` exposes old match identities,
ports, dangling interfaces, and Rule-owned match/schedule data.

Each permitted match set is one witnessed derivation. Rule has already chosen
compatible nonoverlapping patches or resolved their graph-level overlap.
Every atom explicitly deletes matched nodes/edges, preserves unaffected
writable interface members, creates fresh components under local semantic
keys, and reconnects each interface. Application binds fresh identities from
the input configuration's semantic identity, canonical Rule identity, and the
match witness, validates collisions and totality, commits the whole structural
replacement, then validates graph invariants.

Commit never deletes an incident edge implicitly, chooses among overlapping
patches, invents a port repair, projects reachability, or numbers newborns by
traversal. A missing interface effect, unauthorized fresh parent, or one
invalid alternative rejects the complete extensional Rule result with no
partial successor set.

For sequence deletion or insertion, semantic occurrence identities persist or
are created as declared; derived indices and ranks are recomputed views. If an
index/rank is stored state rather than a view, every induced change belongs in
`W` and the total disposition.

### Multiway branching and diamond merge — F034

Suppose two distinct `(rule, match, parent)` witnesses produce the same child
word:

```text
Rule outcome atoms:       d1 -> replacement1
                          d2 -> replacement2
Applied derivations:      a1 -> child C
                          a2 -> child C
Successor quotient:       child C -> {a1, a2}
```

The derivation cardinality is two and the distinct-successor cardinality is
one. Canonical equality is applied only after both witnesses and replacements
are recorded. Rule/match iteration order cannot change the quotient or its
fiber. Any probability mass is pushed forward to the child while the two
source masses remain recoverable.

An identity rewrite is `Advanced` with successor equal to input because the
rewrite event occurred. A rewrite to the epsilon word is one successor. No
applicable match is `Terminal(NoApplicableRewrite)` with zero replacement
derivations. These four cases cannot be represented by the same empty-list or
state-equality convention.

### Stochastic accept/reject — F050

The Rule denotes a normalized measure over proposal-and-acceptance atoms. `W`
is the union of every possible proposal target plus all control/cache slots;
each atom supplies a total disposition.

- An accepted proposal returns an `Advanced` successor with the incumbent,
  cache, and control updated atomically.
- A rejection that advances visible control is `Advanced`.
- A same-configuration rejection may be `Quiescent + Continue` while retaining
  draw evidence; if the Rule treats the proposal attempt as a construction
  event, it is an eventful identity `Advanced` instead.
- A genuine no-event fixed point may be identity `Quiescent` and may
  independently declare `Stop`.

Denotational application returns the complete law and its pushforward to
successors. A realization request selects an atom with a structurally derived
subkey and records draw evidence; replay reproduces the same full applied
derivation. Equal accepted/rejected successors aggregate probability only in
the successor view—the outcome/witness fiber remains intact. A timeout cannot
renormalize observed branches or claim that unobserved mass is zero.

The same law/realization split covers F016 random-walk motion, F014 terminal
measurement, and F046's one-shot complete random functional graph. F046
returns a law over whole graph replacements, not one engine draw per node in
traversal order. Its factored product law states independence explicitly;
ordinary Seed/Rule product composition does not infer it.

A single finite pressure law can assign positive mass to all three of:

1. an `Advanced + Continue` successor;
2. an `Advanced + Stop(Completed)` successor; and
3. `NoSuccessor(Terminal(...))`.

The applied-atom law remains normalized across all three. The successor and
no-successor views are unrenormalized submeasures, and the continuing and
stopped successor fibers stay distinguishable even if their `C` values are
equal.

### Continuous flow and event reset — F006/F037

`R` contains current time/state and the geometry/vector-field/event data; `W`
contains a maximal-flow/result slot and, when authorized, the state, time,
segment/event records, and every reset slot. Rule returns a finite or
intensional outcome space of complete maximal-flow or selected endpoint
derivations.

For a boundary collision, one atom contains the segment to the earliest
verified hit plus a coupled disposition for hit time, position, reflected
velocity, and event record. Application commits that macro-result atomically.
It does not choose a time step, numerically integrate inside commit, or expose
an intermediate state to another derivation. Nonunique flows remain multiple
or intensional atoms. Simultaneous/corner hits require an explicit Rule
tie/reset convention or multiple witnessed atoms; application supplies no
collision convention. A singularity may be a typed terminal/undefined
outcome. A numerical segment is a represented realization with method/error
evidence, not the exact flow silently replaced by floats.

For an event-free ODE such as `dx/dt = 1` with no semantic endpoint selector,
Rule writes the maximal flow/solution object and normally stops after that
one-shot result. An external time query/realization may inspect its value at a
requested time, but cannot cause base `apply` to commit that endpoint. Only a
selector/duration in closed Rule data or visible in `C`/`R`, an intrinsic
earliest event, or a singularity can determine an endpoint inside the Rule
denotation.

### Intensional PDE and finite completion — F041/F015

For F041, Rule may return a closed intensional relation over complete unknown
fields, with an exact but possibly `Undetermined` cardinality claim. Its
universal conformance obligation proves both that members are total over `W`,
satisfy the declared differential and side-data relation, and produce valid
`C`, and that the presentation covers the complete specialized PDE solution
relation up to its declared exact equivalence. Application maps commit over
that relation intensionally. A solver may later provide a certified member,
emptiness proof, or finite characterization; that query evidence refines what
is known about the retained relation and never mutates the original Rule
denotation. Resource-limited mesh output cannot claim completeness.

For F015, the same boundary can return a finite exact set of table
completions. Each satisfying table is an `Advanced + Stop(Completed)`
derivation; universal satisfaction is in its witness. No model is
`Terminal(NoSolution)`, not `Undefined` or an implementation failure. A
partial solver enumeration is neither the finite Rule result nor proof of
unsatisfiability.

### One-shot transform — F021/F061

Seeded input, table/index state, and result slots form `C`; the hash/index Rule
reads the complete dynamic lookup path and returns one total insertion, hit,
or miss replacement. The result atom is `Advanced + Stop`, even when the
stored table is preserved and only the result slot changes. Direct
`apply` is the complete use of the program. Feedback or repeated requests can
be built explicitly, but no trajectory flag, fake second state, or mandatory
rollout is part of the construction.

F061 applies the same boundary to a global basis projection: one application
writes the complete coefficient vector and stops. `Stop` therefore cannot mean
“no replacement”; terminal continuation and successor cardinality are
independent.

These executions use the same `RuleResult`, validation, commit, quotient, and
evidence path. None requires application to learn the family, carrier, or
catalog home.

## Stage 1 Repository Baseline

Captured before Goal 6 execution edits:

| Evidence | Baseline |
|---|---|
| Git `HEAD` | `318a5383cea0898421db3993257e5aec24b7f7dd` |
| Initial worktree | Clean |
| `src/ca` tree | `6e6b34769d60508c03d0a69fad1ede4fef75e217` |
| `tests` tree | `02ad081e039a46efbf61855fdeae60abb7bb70ad` |
| `goal-2` tree | `48b6309655ec7c1d3aaa1a0ec5dfb700385e16d1` |
| Goal 2 handoff SHA-256 | `5792ac1810dafdd0be6343e1d03c4b1ab20c48551efd73400fea5a1812a9f192` |
| Goal 2 README SHA-256 | `e063609c7a52d32bd0a4d3bb384cd5da233c34f57a169e2db6cce197c76e0c4d` |
| Runtime test command | `uv run pytest -q tests` |
| Runtime test result | `102 passed in 1.10s` |

The tracked runtime has 20 files under `src/ca` and nine test files under
`tests`. The package is `ankos` 0.1.0, exposes module `ca`, requires Python
3.10+, and currently depends on NumPy.

The live API still exports `Dynamics`, `RawEpisode`, and `RawBatch`.
`Dynamics` stores `domain`, `shape`, `rule`, plural `neighborhoods`, `frontier`,
`boundary`, and metadata. `specs.py` decodes a small family registry, and
`rollout.py` provides the current tensor-oriented execution path. Rule-family
branches are present in `rollout.py`, with construction-time family decoding in
`specs.py` and dataset-family selection in `datasets.py`; these are baseline
migration targets, not acceptable parts of the remastered executor.

### Existing Pieces to Evolve In Place

- plural `alphabets.py`, `seeds.py`, `frontiers.py`, `neighborhoods.py`, and
  `rules.py`;
- the shared selector work in `loci.py`;
- the public `rollout` concept;
- `py.typed`; and
- downstream `datasets.py`, `rng.py`, and `viz/`, whose internals are deferred.

### Target Pieces Not Yet Present

- `program.py` and `SimpleProgram`;
- root `serialization.py`;
- `catalog/` and its agreed entry/category modules;
- five-field result/application semantics; and
- the remastered 60-family constructors and conformance coverage.

The current tests do not directly cover Alphabet or Frontier contracts and have
no `SimpleProgram`, catalog, serialization, five-field result-algebra, or
60-family coverage suites. Those omissions become Goal 7 test obligations
after Goal 6 specifies them.

This is expected migration evidence, not a defect to repair during Goal 6.
The final Goal 6 audit compares `src/ca`, `tests`, and Goal 2 against the hashes
above.

## Stage Status

- Stage 1 is complete: source cutover, Goal 2 disposition, and repository
  baselines are recorded.
- Stage 2 is complete: component protocols, shared locus algebra,
  configuration ownership, structural composition, validation, serialization
  constraints, and five paper type-checks are authoritative above.
- Stage 3 is next: result algebra, atomic application, and run/tool boundary;
- Stage 4 — exact file ownership, public imports, documentation, and reference
  scaffold;
- Stage 5 — catalog construction and migration;
- Stage 6 — pressure fixtures and conformance;
- Stage 7 — implementation handoff and final reconciliation.
