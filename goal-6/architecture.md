# Goal 6 Architecture

Status: **IN PROGRESS — CONTRACTS COMPLETE; APPLICATION NEXT**

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
retains `c` only to validate and commit `q`. Stage 3 defines that result and
commit algebra.

Frontier and Neighborhood may reuse the same closed locus/anchor descriptor,
and Rule may require their resolved views to have compatible indexing. Neither
resolver consumes the other resolver's output. This preserves their
orthogonality: both resolve independently from the same immutable `C`.

Independent resolution is still one typed join. Both resolvers bind to the
same immutable snapshot identity, and their locus/occurrence references use
the same canonical identities. Rule declares the required `R`-to-`W`
join/index shape; construction validates that shape structurally, and
application validates the resolved binding before Rule evaluation.

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

The exact result variants, compact encodings, witness/deduplication rules,
outcomes, failures, fresh allocation, and commit algorithm are Stage 3 work.
Stage 2 fixes this denotational minimum: each alternative is a total
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
or materialization order. A fresh reference is scoped by validated input
lineage, Rule derivation/witness identity, parent or interface, and a closed
local namespace/key supplied by the replacement. Stage 3 fixes collision and
cross-branch rules; codecs must already represent the reference losslessly
without first enumerating an intensional result set.

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

Stage 3 specifies the algorithm, but its contract must check:

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
exactness, and missing entropy/replay evidence. Stage 3 integrates these with
outcomes; Stage 4 assigns their minimal code ownership.

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
- probability laws separately from concrete draw/replay evidence; and
- representation relations and provenance needed for inverse-on-image and
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
rule(r, w) = Q : RuleResult[C, W]
q ∈ Q  =>  targets(q) ⊆ W ∧ total_disposition(q, W)
          ∧ valid_C(commit(c, q))
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
alternatives, not an invalid sparse successor.

Solver order, resource limit, realization bound, and query policy remain
external. No Solver, ResultPolicy, or special relation-program class is needed.

### Continuous flow — F037

| Type | Binding |
|---|---|
| `C` | Continuous state with domain/geometry, parameters, explicit time, and result/event slots |
| `V` | Exact, certified, or explicitly represented scalar/vector/tensor and flow-segment values |
| `W` | Evolving state, time, and any event/result slots for one flow application |
| `R` | Current state/time, geometry, parameters, event surfaces, and required global data |

- Seed supplies the initial continuous state, time, side data, and exactness
  profile.
- Alphabet prevents represented numerics from impersonating exact values.
- Frontier intensionally denotes every state, time, and event/result slot the
  flow may update.
- Neighborhood exposes the vector field inputs and event dependencies in a
  closed view.
- Rule denotes zero, one, or many admissible flow-segment/endpoint
  replacements.

Judgment: for every valid continuous `c`, represented values conform to `V`;
`frontier(c) = w` and `neighborhood(c) = r` share the same state/time binding.
A representative alternative writes an exact or qualified flow segment,
endpoint state, advanced time, and event result into their declared slots,
targets only `w`, gives every other writable slot an explicit disposition,
and commits to a valid `C`.

Time is visible state or a Rule variable, while horizon and numerical
realization strategy are run policy.

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
