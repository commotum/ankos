# Goal 8: Canonical Family Space Audit

Shorthand: **Space Envelope**

Status: **SCAFFOLDED — NOT STARTED**

## Big-Picture Objective

Review every one of the 60 canonical executable families in
[`ref/types.csv`](../ref/types.csv), recover every construction-relevant
reference and variant from the canonical *A New Kind of Science* corpus, and
determine the complete evidence-backed range of `SPACE` specifications that
each family requires or admits.

The result must answer more than "what dimension is the displayed example?"
For each family it must distinguish:

- the Space directly demonstrated by the Book;
- additional Spaces explicitly stated by the Book;
- additional Spaces genuinely entailed by dimension- or topology-parametric
  mechanics;
- encodings or simulations that do not count as native family Spaces;
- merely plausible extensions that remain unsupported; and
- Spaces that are incompatible with the defining mechanic.

For example, SPF030 `mobile-head-grid-rewrite` must not be summarized as
"grid" or assigned a guessed maximum dimension. The audit must separately
resolve evidence for `[t,x]`, `[t,x,y]`, `[t,x,y,z]`, other coordinate
signatures, topology variants, and any limit on dimensional generalization.
"Probably 3D" is a hypothesis, not a supported result.

This is an evidence and architecture research goal. It does not implement
family builders, redesign the runtime, or change `ref/types.csv` while the
audit is in progress.

## Settled Meaning of Space

The current user-authorized model supersedes previous decisions that left
time implicit in rollout metadata or treated geometry as Seed-owned Carrier
data.

The top-level concept is `SPACE`. A Space describes admissible coordinates,
their structural relations, support law, and boundary law. A Coordinate is
one address in that Space. `Domain` is reserved, when useful, for the concrete
subset of coordinates realized by one episode.

For ordinary discrete Cartesian systems:

```text
t-only   coordinate: [t]
t+1D     coordinate: [t,x]
t+2D     coordinate: [t,x,y]
t+3D     coordinate: [t,x,y,z]
```

These logical coordinates may be serialized in a fixed-width representation,
but unused axes are representation details rather than semantic dimensions.
Time is never implicit.

For every discrete dynamic variant, application has immutable full-history
semantics:

1. preserve every existing coordinate through time `t`;
2. add a complete new state slice at `t+1`;
3. copy every location outside the Frontier into that new slice unchanged;
4. apply the Frontier/Neighborhood/Rule effects only in the new slice; and
5. never overwrite a coordinate at time `t`.

Continuous-time families must still make time an explicit coordinate, but
must record the actual time set and evolution/relation semantics instead of
pretending that a continuous flow advances by integer `t+1`. One-shot
relations, multiway evolution, event time, and non-Cartesian supports likewise
require explicit honest treatment during Stage 1.

The audit must use the following deciding principle:

> If something must be independently addressed, read, written, or related,
> it belongs in Space. If it is an inseparable attribute of one addressed
> location, it belongs in the Alphabet or value schema.

Accordingly, graph adjacency, tree parenthood, order, incidence, and topology
may be relations over coordinates rather than semantic Space subclasses.
Product/record structure usually belongs to values. `INTENSIONAL` describes a
presentation by predicate or relation, not a coordinate-space category.

## Source Authority and Required Reading

Use sources in this order. A lower item may locate evidence or expose a
conflict, but cannot silently override a higher item.

1. The settled Space semantics and objective in this plan.
2. [`ref/types.csv`](../ref/types.csv) for the exact 60-family roster,
   `book_index`, SPF/F join, home, slug, first appearance, initial source
   anchors, parameters, and name relations.
3. [`ref/A-New-Kind-of-Science/Contents.md`](../ref/A-New-Kind-of-Science/Contents.md)
   and its 29 linked canonical documents for primary source evidence. The
   actual passages, captions, Notes, and cross-references are authoritative;
   summaries are not substitutes.
4. [`goal-5/11-FAMILIES.md`](../goal-5/11-FAMILIES.md) for the authoritative
   60-family semantic partition and candidate membership.
5. [`goal-5/candidates.md`](../goal-5/candidates.md) for each candidate's prior
   Carrier/domain, initialization, acting loci, reads, effects, variants,
   representative sources, and distinguishing test.
6. [`goal-5/source-decision-matrix.csv`](../goal-5/source-decision-matrix.csv)
   for the exhaustive lead-to-candidate-to-family trace and full canonical
   source anchors. Every family-bound `SERIOUS` lead must receive a Space-audit
   disposition.
7. [`goal-5/taxonomy-census.md`](../goal-5/taxonomy-census.md),
   [`goal-5/coverage.md`](../goal-5/coverage.md),
   [`goal-5/9-SATURATION.md`](../goal-5/9-SATURATION.md), and
   [`goal-5/13-HOSTILE-REVIEW.md`](../goal-5/13-HOSTILE-REVIEW.md) for census,
   omission, source-coverage, and hostile-review controls.
8. [`goal-1/evidence-index.md`](../goal-1/evidence-index.md),
   [`goal-1/architecture-audit.md`](../goal-1/architecture-audit.md), and the
   relevant Goal 1 T01-T45 stage/source-oracle files for deep legacy-family
   searches, candidate dispositions, dimensional variants, and source
   excerpts. Translate historical `t+0D` to `t-only` and re-evaluate every
   conclusion under explicit immutable time.
9. [`goal-6/catalog-migration.md`](../goal-6/catalog-migration.md) for the
   exact SPF001-SPF060 crosswalk, canonical homes, source anchors, and legacy
   name relationships.
10. [`goal-6/conformance.md`](../goal-6/conformance.md),
    [`goal-6/architecture.md`](../goal-6/architecture.md), and Goal 7 records
    only as historical Carrier/runtime and pressure-test inputs. They are not
    authority over the new Space model, and a canonical Goal 7 wrapper is not
    evidence that a family or Space was implemented.

[`goal-3/12-RELEASE.md`](../goal-3/12-RELEASE.md) establishes the corrected
29-document corpus as canonical. Goal 4 is retired and must not be used as a
live source.

## Current Facts

- `ref/types.csv` contains exactly 60 canonical family rows and 18 columns.
- `book_index`, `family_id`, `audit_family_id`, and `slug` are unique.
- Coverage is 19 `covered` and 41 `addition` families.
- Home counts are exactly 11 `automata`, 15 `substitua`, 8 `machina`, 14
  `media`, 9 `criteria`, and 3 `dynamica`.
- Every row has a first-appearance anchor and catalog source reference, but
  those fields are representative starting points rather than exhaustive
  evidence.
- Goal 5 records 190 `SERIOUS` anchored leads covering all 60 executable
  families, with one to seventeen serious leads per family.
- Goal 5 is the current semantic-family authority. Goal 6 is a historical
  architecture/crosswalk baseline. Goal 7's 60 canonical names are progress
  stubs rather than completed family implementations.
- Existing Carrier kinds combine coordinate geometry, value structure,
  topology, concrete support, and representation choices. The audit must
  decompose those concerns rather than mechanically rename each Carrier kind.
- `ref/types.csv` deliberately has no single `domain` column. A family may
  admit multiple Space variants, so the authoritative result must be
  normalized one family x one Space claim per row.

## Assumptions to Test, Not Presume

- One semantic family may admit several coordinate signatures without
  becoming several families.
- Changing concrete shape, horizon, Seed realization, or finite observation
  window ordinarily does not change the family Space, but fixed topology or
  support constraints may provide counterexamples.
- A dimension-independent local rule may admit higher rank, but only explicit
  source language or a complete mechanical derivation can establish that.
- A graph, tree, record, word, field, or product may often be expressed using
  generic coordinates plus relations or structured values, but this must be
  decided case by case.
- Static topology belongs to Space; evolving topology may instead be
  immutable state at each explicit time.
- A rendering, trajectory plot, causal graph, or emulation may use coordinates
  different from the native state and must not be confused with native Space.
- Every family has at least one precise Space account. If the Book genuinely
  underdetermines the maximum range, the honest result may be a bounded set of
  proved variants plus a precisely stated unresolved limit.

## Non-Negotiable Constraints and No-Cheating Rules

1. Audit exactly the 60 `family_id` values in `ref/types.csv`; do not audit by
   SPF numeric order, old T count, current exports, or stub presence.
2. Preserve `book_index` as final presentation order. Home stages may group
   related families, but must process their members in `book_index` order.
3. Do not edit `ref/types.csv` during research and do not force a one-to-many
   Space envelope into one delimited `domain` cell.
4. Do not accept a Goal 1/5/6 summary as primary evidence. Resolve its anchor
   into the canonical Book document and inspect enough context to support the
   claim.
5. Disposition every relevant Goal 5 `SERIOUS` lead, every listed candidate
   variant, every `catalog_source_refs` span, and every followed dimensional or
   topological cross-reference. Leave no silent remainder.
6. Do not infer Space from a family name, home, current `CarrierKind`, class,
   constructor signature, or present runtime limitation.
7. Do not count an encoding, simulation, renderer, observer, dataset layout,
   or derived causal/history graph as a native Space without a proved
   one-step/full-state equivalence and an explicit reason.
8. Do not promote "possible", "natural", "probably", or "could be 3D" to
   supported. Keep conjectural claims visibly separate.
9. A mechanically entailed dimension requires a written closure argument:
   identify the invariant mechanic, parameter being generalized, unchanged
   read/write law, topology requirement, and any new boundary obligation.
10. Keep Space separate from Alphabet/value roles, concrete shape, Seed,
    Frontier, Neighborhood, Rule, realization, horizon, and presentation.
    Record compatibility dependencies without moving them into Space by
    convenience.
11. Time must be explicit in every admitted Space. For discrete dynamics,
    verify the immutable full-new-slice and copy-outside-Frontier law. For
    continuous/event/relational cases, record the exact honest analogue.
12. Do not assume `GRID`, `FIELD`, `GRAPH`, `TREE`, `WORD`, `RECORD`,
    `PRODUCT`, or `INTENSIONAL` must survive as semantic Space classes.
13. Tests, parsers, row counts, and green checks prove ledger integrity, not
    the truth of a source claim. Every semantic conclusion needs evidence and
    reasoning.
14. Preserve contradictions and source underdetermination. Resolve them or
    report a sharply bounded unknown; never manufacture closure.
15. Do not implement runtime/catalog changes or delete/replace tests as part
    of this research goal.

## Evidence and Classification Contract

Every Space claim must receive exactly one evidence status:

| Status | Meaning | Counts as admitted? |
|---|---|---:|
| `DEMONSTRATED` | A Book construction, trace, figure, or executable Notes form actually uses the Space | yes |
| `STATED` | Book text explicitly says the family supports the Space/variant | yes |
| `ENTAILED` | Source-defined mechanics contain an explicit parameter/general law and a complete recorded derivation proves this Space instance | yes |
| `ENCODING_ONLY` | The Space belongs to a simulation, representation, renderer, observer, or derived artifact rather than the native family | no |
| `CONJECTURAL` | Architecturally plausible but not proved by source or mechanics | no |
| `EXCLUDED` | Contradicts a defining mechanic or belongs to another family | no |
| `UNDERDETERMINED` | Available evidence cannot decide the claim; the exact missing fact and bounded alternatives are recorded | no |

`DEMONSTRATED`, `STATED`, and `ENTAILED` together form the supported family
Space envelope. They must remain separately visible so a reader can tell what
the Book shows from what the family definition logically generalizes.

Every source candidate must also be dispositioned as `NATIVE`, `VARIANT`,
`RELATION`, `ENCODING`, `OBSERVER`, `DUPLICATE`, `CONTROL`, `FALSE_POSITIVE`,
or `UNRESOLVED`.

## Required Goal Artifacts

The execution stages must create these research artifacts inside `goal-8/`:

### `space-vocabulary.md`

The frozen generic vocabulary and coordinate grammar. It must define explicit
time; Cartesian, continuous, nominal/keyed, path, tagged, and relational
coordinates without turning them into family classes; relations/topology;
support and shape; boundary; value structure; dynamic support; one-shot and
continuous cases; and native versus encoded Space.

### `source-ledger.csv`

One row per family/source candidate or followed cross-reference, with at least:

```text
family_id, audit_family_id, candidate_id, lead_id, source_path,
line_start, line_end, context, disposition, claim_ids, fact_established,
prior_goal_refs, notes
```

### `family-space-claims.csv`

The authoritative normalized ledger: one row per family x distinct Space
claim. Required fields are:

```text
book_index, family_id, audit_family_id, home, slug, space_claim_id,
evidence_status, family_admissibility, native_or_encoding,
coordinate_signature, time_domain, spatial_rank, coordinate_components,
axis_domains, addressed_entity_sorts, relations_topology, support_policy,
boundary_policy, shape_role, explicit_time_semantics, evidence_refs,
candidate_ids, legacy_or_named_variants, reasoning,
counterevidence_or_limit, open_question
```

Stage 1 may refine names or add fields, but it may not collapse distinct
claims or weaken the evidence distinctions.

### `family-space-summary.csv`

Exactly one row per `ref/types.csv` family, sorted by `book_index`, containing
the exact demonstrated, stated, entailed, encoding-only, excluded,
conjectural, and underdetermined claim IDs plus the family's primary evidence
and stage status. This is a coverage projection; it never replaces the
normalized claim ledger.

### `synthesis.md`

A readable final account of the coordinate vocabulary, every family envelope,
cross-family patterns, Carrier-to-Space dispositions, remaining bounded
underdetermination, and a recommendation for any later stable `ref/` artifact.
Publishing a new `ref/spaces.csv` or changing the library is a separate
user-authorized action.

### `verify_space_audit.py`

A deterministic read-only verifier for exact joins, counts, enums, source
paths/ranges, claim/source references, coverage, sorting, and explicit-time
fields. It must not encode semantic answers merely to make the ledger pass.

## Success Metrics and Final Verification

The goal is complete only when:

- the summary family set equals the exact 60-family set from `ref/types.csv`;
- every family has at least one precise coordinate witness and one completed
  Space-envelope conclusion;
- all six home counts agree exactly with the source CSV;
- every family-bound Goal 5 `SERIOUS` lead and every relevant candidate
  variant has an explicit source-ledger disposition;
- every `DEMONSTRATED` or `STATED` claim cites a canonical Book passage;
- every `ENTAILED` claim cites its source mechanics and contains a complete
  dimensional/topological closure argument;
- all encoding-only, conjectural, excluded, and underdetermined claims remain
  visibly outside the supported range;
- every source path exists and every cited line range is valid;
- every dynamic discrete claim states and satisfies explicit immutable-time,
  full-new-slice, and copy-outside-Frontier semantics;
- continuous, event-driven, one-shot, multiway, growing-support, graph, tree,
  product, and intensional cases survive targeted hostile review;
- the normalized claims ledger and one-row summary agree mechanically;
- the final synthesis is sorted by `book_index` while also reporting coherent
  home/family groupings;
- no source candidate or classification question remains silently unresolved;
- any genuine `UNDERDETERMINED` result records the exact missing evidence and
  proves the stated bounds rather than using uncertainty as a shortcut;
- `uv run python goal-8/verify_space_audit.py` passes;
- focused repository checks affected by any final reference artifact pass;
- `git diff --check` passes; and
- final scope inspection shows no accidental runtime, catalog, test, or Book
  corpus changes.

## Stage Index

### 1-GUARDRAILS

#### Big Picture Objective

Freeze the Space vocabulary, evidence statuses, ledger schemas, authority
order, and verification rules before making family conclusions.

#### Detailed Implementation Plan

- Re-read the current files named under Source Authority and record any drift
  from this scaffold.
- Define one generic `Space` data model based on coordinates, relations,
  support, and boundary rather than semantic family classes.
- Resolve the vocabulary for discrete/continuous time, Cartesian axes,
  nominal IDs, paths, tagged coordinates, topology relations, dynamic support,
  one-shot relations, multiway traces, and intensional presentation.
- Freeze the difference between concrete shape/domain and the admissible
  program Space.
- Create the five required artifact shells and the structural verifier.
- Use SPF030 only as a schema pressure test; do not pre-judge its 3D range.

#### Completion Requirements

- `space-vocabulary.md` answers every vocabulary ambiguity listed above.
- All CSV schemas parse and have documented enums and uniqueness keys.
- The verifier detects duplicate/missing families, unsupported statuses,
  broken references, and absent explicit-time semantics.
- No family claim is counted as completed during this guardrail stage.

### 2-SOURCE-MAP

#### Big Picture Objective

Construct the exact 60-family evidence queue by joining the current CSV to
Goal 5 candidates/leads, Goal 6 SPF rows, Goal 1 legacy audits, and canonical
Book paths.

#### Detailed Implementation Plan

- Join by `family_id` and `audit_family_id`, never by row position or name
  similarity.
- Expand every `first_appearance_anchor` and `catalog_source_refs` shorthand.
- Join all family-bound `SERIOUS` Goal 5 leads and candidate memberships.
- Attach relevant Goal 1 source-oracle/stage evidence and all named variants,
  dimensional cross-references, Notes implementations, captions, and Index
  routes.
- Populate `source-ledger.csv` with an auditable queue; family audit stages
  will fill final dispositions and claim links.

#### Completion Requirements

- Exactly 60 families join one-to-one across the current roster and semantic
  family authority.
- Every family has a nonempty canonical source queue and candidate set.
- All starting paths/ranges parse and resolve in the 29-document corpus.
- Every serious lead is assigned to exactly one family audit queue or has a
  documented cross-family reason.
- No Space conclusion is accepted merely from the metadata join.

### 3-AUTOMATA

Families, in `book_index` order: SPF050, SPF032, SPF026, SPF007, SPF001,
SPF034, SPF040, SPF009, SPF003, SPF052, SPF021.

#### Big Picture Objective

Close the Space envelope for all 11 `automata` families, including synchronous
and asynchronous lattices, moving loci, tuple/scalar maps, mutable rules,
populations, relaxation, weighted networks, and shared-history games.

#### Detailed Implementation Plan

- Inspect and disposition every queued source and variant for each family.
- Separate lattice rank from value channels, schedules, populations, network
  relations, and history stored in explicit time.
- Record every demonstrated/stated/entailed coordinate signature and all
  excluded or underdetermined variants.
- Add normalized claims and update the 11 corresponding summary rows.

#### Completion Requirements

- All 11 exact SPF IDs have complete claim/source joins.
- Every dimensional closure beyond a displayed example has a written proof.
- Static versus evolving topology and discrete versus continuous coordinates
  are explicit where applicable.
- No Automata source candidate or family Space question remains silently open.

### 4-SUBSTITUA-I

Families, in `book_index` order: SPF037, SPF005, SPF049, SPF016, SPF023,
SPF025, SPF038, SPF033.

#### Big Picture Objective

Audit the first eight `substitua` families: parallel/contextual/structural
replacement, delete-append systems, indexed histories, erasure, parallel
network rewriting, and multiway rewriting.

#### Detailed Implementation Plan

- Determine when sequence position is a `t+1D` address versus explicit time
  or a structured Alphabet value.
- Treat generation replacement as creation of a full immutable new slice,
  including copied or structurally preserved content.
- Separate word/array rank, tree/path addressing, graph incidence, dynamic
  support, branch structure, and intensional presentation.
- Close every source and variant claim for the listed families.

#### Completion Requirements

- All eight exact SPF IDs have complete source dispositions and claim rows.
- Growing/shrinking support never masquerades as a new spatial dimension.
- Multiway branch structure is distinguished from the coordinates of each
  immutable trajectory.
- Native structural Spaces are separated from grid/CA encodings.

### 5-SUBSTITUA-II

Families, in `book_index` order: SPF019, SPF031, SPF028, SPF002, SPF022,
SPF043, SPF015.

#### Big Picture Objective

Audit the remaining seven `substitua` families: global placement, moving-rim
accretion, local graph rewrite, append-only generation, history-dependent
growth, random functional graphs, and first-passage aggregation.

#### Detailed Implementation Plan

- Resolve geometric coordinates versus graph/node identities and relations.
- Record fixed, sparse, growing, accreting, and probabilistic support laws.
- Determine when history is explicit time, provenance-valued state, or an
  independently addressed relation.
- Distinguish native movement/growth Space from paths and aggregate renderings.

#### Completion Requirements

- All seven exact SPF IDs have complete source and claim closure.
- Every fresh-coordinate claim identifies its address and birth time.
- Graph adjacency and geometric embedding are not conflated.
- Random walks, contact events, and final aggregates have their native versus
  observer coordinates explicitly separated.

### 6-MACHINA

Families, in `book_index` order: SPF030, SPF045, SPF010, SPF013, SPF044,
SPF035, SPF048, SPF053.

#### Big Picture Objective

Close all eight `machina` families, with special emphasis on mobile-head
dimensionality, registers versus coordinates, random access, circuits,
recursive evaluation, retrieval indexes, semidecision, and priority injury.

#### Detailed Implementation Plan

- Fully resolve SPF030 across 1D, 2D, possible 3D/higher-dimensional,
  alternative lattice, and encoding variants from its complete candidate and
  Book evidence chain.
- Put head/control/cell attributes in Alphabet unless independently addressed;
  do not invent separate machine-specific domains.
- Distinguish a t-only product value from independently addressed registers,
  wires, memory addresses, search indexes, oracle approximations, and tapes.
- Record schedule/staging coordinates only when semantically part of Space,
  not merely executor bookkeeping.

#### Completion Requirements

- All eight exact SPF IDs have complete source and claim closure.
- SPF030 has an explicit evidence status for `[t,x]`, `[t,x,y]`, `[t,x,y,z]`,
  any stated higher-rank closure, and all topology variants found.
- Machine storage encodings are not mistaken for family Space changes.
- Divergence, halting, retrieval output, and priority stages do not hide
  implicit time or mutation.

### 7-MEDIA-I

Families, in `book_index` order: SPF008, SPF004, SPF012, SPF054, SPF056,
SPF057, SPF058.

#### Big Picture Objective

Audit the first seven `media` families: digit emission, causal provenance,
maximal runs, weighted prefix blocks, history references, recursive regions,
and basis transforms.

#### Detailed Implementation Plan

- Separate input/output stream position, scan position, record structure,
  recursive region coordinates, coefficient indices, and explicit time.
- Determine whether causal networks are native constructed state, derived
  output, or both in distinct variants.
- Treat records, prefixes, and vector coefficients as value structure unless
  independently addressed by mechanics.
- Close all source and variant claims.

#### Completion Requirements

- All seven exact SPF IDs have complete source and claim closure.
- Stream/scan axes are never silently identified with time.
- Derived causal/provenance coordinates are classified honestly.
- Recursive/nested coordinates and dense array realizations remain distinct.

### 8-MEDIA-II

Families, in `book_index` order: SPF041, SPF060, SPF020, SPF046, SPF055,
SPF011, SPF059.

#### Big Picture Objective

Audit the remaining seven `media` families: transition-model fitting, XOR
streams, hash transforms, sampled causal orders, nested intervals, error
diffusion, and predictive residuals.

#### Detailed Implementation Plan

- Distinguish sample index, stream index, key/address space, event IDs,
  interval paths, image coordinates, scan order, and explicit time.
- Record which coordinate relations are invariant and which are learned or
  produced as state.
- Separate one-shot transforms from iterated feedback variants.
- Close all source and variant claims.

#### Completion Requirements

- All seven exact SPF IDs have complete source and claim closure.
- Each transform states whether output coordinates equal, refine, or differ
  from input coordinates.
- Hash/index and causal-order relations are not mislabeled Cartesian rank.
- Feedback variants obey explicit immutable-time semantics.

### 9-CRITERIA

Families, in `book_index` order: SPF029, SPF047, SPF017, SPF042, SPF024,
SPF018, SPF014, SPF027, SPF051.

#### Big Picture Objective

Close all nine `criteria` families while distinguishing candidate/model
coordinates, local/global relations, solver/search trajectories, and native
state from accepted solution sets.

#### Detailed Implementation Plan

- Determine the Space of the relation itself separately from any external
  enumeration, optimization, sampling, or reconstruction procedure.
- Handle local templates, graph/local factors, geometric embeddings, equation
  tuples, model tables, histories, and stochastic searches without forcing
  them into grid classes.
- Define the honest explicit-time interpretation of one-shot relations and
  separately iterated search variants.
- Close every source and variant claim.

#### Completion Requirements

- All nine exact SPF IDs have complete source and claim closure.
- One-shot relation Space and solver trajectory Space are never conflated.
- Accepted candidate value structure is separated from addressed coordinates.
- Every claimed time axis is semantically justified rather than added as a
  cosmetic tensor dimension.

### 10-DYNAMICA

Families, in `book_index` order: SPF039, SPF036, SPF006.

#### Big Picture Objective

Close the three continuous families: partial differential relations, ordinary
differential flows, and continuous event dynamics.

#### Detailed Implementation Plan

- Record explicit time domains, continuous spatial axes, dependent-field value
  schemas, initial/boundary data, event surfaces, and reset relations.
- Distinguish ODE t-only state from vector components, PDE spatial rank from
  field components, and event index from continuous time.
- Separate exact continuous denotation from sampled numerical realization or
  dense trajectory projection.
- Close all source and variant claims without integer-step coercion.

#### Completion Requirements

- All three exact SPF IDs have complete source and claim closure.
- Every admitted continuous Space states its time and spatial coordinate sets.
- Numerical grids and solver steps are classified as realizations unless the
  source defines them natively.
- Initial conditions, spatial boundary conditions, and event resets are placed
  in the correct semantic owner.

### 11-CROSSCUTS

#### Big Picture Objective

Reconcile the home audits into one consistent generic Space algebra and close
all cross-family dimensional, topological, representation, and variant
questions.

#### Detailed Implementation Plan

- Compare families sharing candidate variants, legacy T names, encodings,
  dimensional generalizations, or topology changes.
- Challenge every `ENTAILED` claim against lower/higher-rank edge cases,
  boundary requirements, coordinate addressability, and unchanged mechanics.
- Reconcile `RECORD`, `HISTORY`, `GRID`, `WORD`, `TREE`, `GRAPH`, `FIELD`,
  `PRODUCT`, and `INTENSIONAL` into coordinates, relations, values, support,
  or presentation without preserving accidental categories.
- Resolve or sharply bound all `UNDERDETERMINED` and `CONJECTURAL` claims.
- Ensure the family partition remains semantic: changing Space parameters may
  or may not create a new family, and every decision needs a boundary test.

#### Completion Requirements

- No two families use contradictory vocabulary for equivalent Space facts.
- Every entailed dimensional/topological closure survives adversarial review.
- All cross-family source leads and aliases have one consistent disposition.
- Remaining underdetermination is genuine, bounded, and fully documented.

### 12-HOSTILE-REVIEW

#### Big Picture Objective

Attempt to falsify the completed 60-family matrix independently of the home
audit narrative.

#### Detailed Implementation Plan

- Recompute exact joins, home counts, coverage counts, sort order, enums,
  source paths/ranges, and claim/source references from raw files.
- Sample every evidence status and all high-risk families, including SPF030,
  dynamic graphs, trees/paths, continuous fields, multiway systems, one-shot
  relations, changing support, products, and intensional presentations.
- Search specifically for omitted dimensional variants and false promotions
  of encodings/renderings to native Space.
- Challenge the immutable full-new-slice claim for copied non-Frontier sites.
- Record findings and repair ledgers rather than weakening checks.

#### Completion Requirements

- `verify_space_audit.py` passes from the repository root and a relocated
  working directory where appropriate.
- All hostile findings are resolved or converted into honest bounded
  underdetermination.
- Exact 60-family coverage and every evidence-status total are reproducible.
- No current runtime behavior or prior summary is used as an answer oracle.

### 13-SYNTHESIS

#### Big Picture Objective

Publish the final research result inside `goal-8/` and leave a precise,
resumable recommendation for any later repository/API integration.

#### Detailed Implementation Plan

- Freeze the normalized claim and source ledgers.
- Generate the exact one-row-per-family summary in `book_index` order.
- Write `synthesis.md` with the common Space model, all 60 family envelopes,
  home-group patterns, Carrier dispositions, and bounded unknowns.
- State whether a future normalized `ref/spaces.csv`, program `Space` field,
  or runtime migration is warranted, without performing those changes.
- Run final verifier, relevant focused checks, diff/whitespace checks, and
  scope inspection.

#### Completion Requirements

- Every success metric in this plan is satisfied with recorded evidence.
- The final summary and ledgers answer the original 60-family Space-range
  question constructively and do not hide uncertainty.
- No required work remains except explicitly separate, user-authorized
  publication or implementation goals.
- `0-plan.md` records final facts, results, and any later work without claiming
  that future integration has already occurred.
