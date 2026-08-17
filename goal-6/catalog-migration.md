# Canonical Catalog Migration

Status: **Stage 5 design contract**

This is the implementation-facing catalog map for Goal 7. It normalizes the
completed [Goal 5 census](../goal-5/taxonomy-census.md), [family
definitions](../goal-5/11-FAMILIES.md), [API pressure
map](../goal-5/api-pressure.md), and [T01–T45
reconciliation](../goal-5/10-RECONCILE.md) into the six catalog modules fixed
by [the Goal 6 architecture](architecture.md).

It does not create a second taxonomy. Goal 5 remains authoritative for family
identity and source interpretation; this file assigns stable catalog identity,
constructor spelling, module ownership, five-field construction, and migration
treatment.

## Frozen totals

| Obligation | Exact result |
|---|---:|
| Canonical executable family entries | 60 |
| Currently covered families | 19 |
| Family additions | 41 |
| Close non-family roles | 2 |
| Legacy T entries retained | 45 |
| Canonical modules | 6 |

The executable research IDs are F001–F009, F011–F038, F040–F041, and
F043–F063. F010 and F042 are the two close roles. F039 is not an omission; it
did not survive Goal 5 consolidation.

## Identity and entry policy

### Three identities, three jobs

- A **normalized family ID** (`SPFnnn`) is the immutable library identity of
  exactly one executable semantic family.
- A **Goal 5 family ID** (`Fnnn`) is immutable provenance back to the research
  census. It is metadata, not a public Python type or an execution key.
- A **legacy entry ID** (`Tnn`) preserves the heterogeneous T01–T45 catalog
  history. A T entry can have zero targets (T08), one target, or two named
  targets (T40); it is never overloaded as normalized family identity.

A canonical path such as
`ca.catalog.automata.synchronous_local_state_transform` is the preferred
callable spelling, not a fourth stable identity. It may acquire a compatibility
alias without changing its SPF, F, or T relations.

SPF001–SPF060 are assigned once in ascending executable Goal 5 family-ID order,
skipping close roles F010/F042 and unused F039. That initial issuance order is
now frozen; IDs are never recomputed from row position, sorting, module,
constructor, slug, or class. Future families begin at SPF061, and retired IDs
become tombstones rather than being reused.

This uniform axis resolves two legacy normalization holes without exceptions:
T40 points explicitly to SPF002/F002 and SPF008/F008, while represented F055
has SPF052 and no invented T owner. All 41 additions therefore receive fresh
stable SPF IDs, all 19 covered families use the same family-ID type, and every
T01–T45 identity remains unchanged.

### Entry kinds

`catalog/entries.py` owns immutable SPF family entries and T legacy-entry
metadata with these closed kinds:

| Kind | Callable? | Meaning |
|---|---|---|
| `family` | Canonical category constructor | Exactly one of the 60 mechanics |
| `preset` | Delegating constructor | Closed parameter restriction of one family |
| `alias` | Delegating constructor | Alternate name with the same normalized arguments and expansion as its declared canonical or preset delegate |
| `compatibility` | Delegating constructor when named by this migration | Retained legacy spelling, normally deprecated |
| `merged` | No independent constructor | Former row absorbed as family parameters; a compatibility delegate may remain |
| `retired` | No | Permanent tombstone for a non-program role |
| `split` | No | Permanent one-to-many migration record with explicit branch names |

Each metadata value contains only strings, enums, exact closed arguments,
source anchors, and ID/path relations. It never contains a Python callable,
component instance, registry hook, or executor. Category modules do not import
`entries.py`; `catalog/__init__.py` is the one join point.

### Constructor and re-export rules

1. Each canonical constructor is the exact Goal 5 family slug converted to
   `snake_case`. These 60 names are unique and source-traceable.
2. Every canonical constructor accepts keyword-only closed values or
   recognized component descriptors and returns one validated, expanded
   `SimpleProgram(seed, alphabet, frontier, neighborhood, rule)`.
3. “Law”, “predicate”, “metric”, “program”, “estimator”, and similar
   parameters below mean closed structural tables/ASTs/descriptors—never
   unrestricted callbacks, `Any`, hidden solvers, or ambient entropy.
4. Familiar Book names such as `eca`, `turing_machine`, and `tag_system` are
   presets or aliases. They delegate to category-owned canonical constructors;
   they own no component or execution logic.
5. Every unique canonical name is explicitly available both category-qualified
   and flat under `ca.catalog`. Every `P` and `A` spelling named by this
   contract is likewise an explicit flat export. Generic names such as
   `rewrite`, `network`, `machine`, `relation`, `transform`, `search`, and
   `flow` are forbidden flat exports.
6. Any future collision removes the contested flat spelling from all but one
   explicitly preferred owner. Category-qualified paths never collide.
7. Lookup by SPF, T, or F ID returns metadata only. There is no public
   `construct(id, **kwargs)` dispatcher. Users call the recorded canonical
   path.
8. Canonical serialization stores only the expanded five-field semantic
   payload plus ordinary codec-envelope data. It neither preserves nor
   recovers SPF/F/T identity, invoked spelling, or constructor arguments.
   Applications that need invocation history keep a separate user manifest.

## Home precedence

The primary home follows dominant mechanics, not purpose or Book vocabulary:

| Module | Primary test |
|---|---|
| `automata` | A persistent carrier is updated in place or by a shared generation |
| `substitua` | Structure is matched, replaced, grown, deleted, or branched |
| `machina` | A visible head, instruction, stack, traversal, or controller drives the step |
| `media` | Information is transformed between distinct representations |
| `criteria` | Admissibility, solutions, witnesses, objectives, or weighted alternatives define the result |
| `dynamica` | A continuous differential, field, event, or flow law defines the result |

Secondary traits remain metadata. In particular:

- F007 is `automata`: the defining operation is a discrete coupled field
  generation; its mobile marker is subordinate.
- F011 is `machina`: ordered enumeration and divergence, not the supplied
  predicate, define its mechanics.
- F016, F020, and F024 are `substitua`: irreversible attachment, placement, or
  append growth dominates their walker, scorer, or index control.
- F036 is `machina`: its indexed traversal is construction-bearing; a bare
  nearest-point relation would be a different criteria construction.
- F044 and F049 are `media`: they transform observations/events into a model
  or causal-cover representation.
- F046 is `substitua`: it constructs graph structure instead of encoding an
  existing object.
- F050 is `criteria`: the global acceptance objective distinguishes it from an
  ordinary stochastic automaton.
- F041 is `dynamica` despite relational cardinality; F054 is `criteria`
  because it aggregates completed histories rather than evolving a
  differential state.

## Canonical family matrix

In the table, `S/A/F/N/R` abbreviate Seed, Alphabet, Frontier, Neighborhood,
and Rule. `μ` means an explicit probability law and `I` an intensional result.
Every `R` denotes complete atomic dispositions over the listed `F`; all
unlisted configuration structure is preserved.

### `automata.py` — 11

| ID | Goal 5 family | Canonical constructor | Status | Closed parameters | Five-field skeleton (`S/A/F/N/R`) | Representation/result pressure | Representative sources | Legacy/public relation |
|---|---|---|---|---|---|---|---|---|
| SPF001 | F001 `alternating-partition-local-evolution` | `automata.alternating_partition_local_evolution` | addition | `seed; partition; block_law; boundary; phase` | S lattice/spin field + phase; A cell/particle/amplitude + phase; F active disjoint blocks/parity + phase; N immutable old blocks/stencils; R joint deterministic/unitary/μ replacement + phase toggle | Visible phase schedule; whole partition commits atomically | `CH08:L155-165; N08:L107,L124-126; CH09:L303-321` | — |
| SPF003 | F003 `asynchronous-local-state-automaton` | `automata.asynchronous_local_state_automaton` | addition | `seed; local_law; schedule; boundary` | S lattice + scan/readiness control; A cell/cursor/readiness; F every selectable stencil + control; N selected current view + scheduler state; R choose/recognize one locus and commit immediately, optionally μ | Each write is visible to the next application; random selection exposes its full write union | `N09:L407-443` | — |
| SPF007 | F007 `coupled-field-mobile-locus-evolution` | `automata.coupled_field_mobile_locus_evolution` | addition | `seed; field_law; mobile_law; boundary` | S field + unique mobile marker; A field/occupancy/mobile products; F whole next field + every source/destination/destructive locus; N field stencils + destination view; R one coupled field update and marker move | Heterogeneous distributed and single-locus effects form one replacement | `CH08:L131-138` | — |
| SPF009 | F009 `driven-relaxation` | `automata.driven_relaxation` | addition | `seed; drive_law; toppling_law; boundary; relaxation_form` | S stable height field + drive/relax phase; A heights/unstable/phase; F drive + complete avalanche envelope; N field through toppling stencils; R drive then closure or visible microsteps, optionally μ | Nested relaxation and random drive remain Rule semantics | `BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L665-676` | — |
| SPF021 | F022 `history-dependent-agent-game` | `automata.history_dependent_agent_game` | addition | `agents; histories; payoff; action_schema; round_control` | S closed agents + joint histories/scores; A actions/program/history/payoff; F both appends + scores/control; N both histories + payoff matrix; R simultaneous moves, appends, and payoff, optionally μ | Unbounded shared-history reads and coupled multi-agent commit | `N10:L1081-1085` | — |
| SPF026 | F027 `iterated-map` | `automata.iterated_map` | covered | `seed; map_expression; guards; terminal_condition` | S exact scalar/tuple + parameters/control; A numeric components + branches; F complete tuple; N tuple + guards/parameters/derivatives; R one exact image or typed halt/undefined | Whole-tuple replacement; terminal and undefined remain distinct | `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L53-54,L111-118,L472-491` | T34 arithmetic, T35 piecewise, and T36 digit-reversal presets |
| SPF032 | F033 `multi-active-local-rewrite` | `automata.multi_active_local_rewrite` | covered | `seed; local_law; collision_law; schedule` | S carrier + finite active set; A passive/active roles; F all sources/destinations/offspring/collisions; N all active old-snapshot views; R joint move/split/delete/coalesce, 0/1/many/μ | Active-set cardinality and collisions are distributed Rule results | `CH03:L231-247` | `generalized_mobile_automaton` preset |
| SPF034 | F035 `mutable-rule-local-automaton` | `automata.mutable_rule_local_automaton` | addition | `seed; rule_program; interpreter; mutation_law` | S carrier + explicit rule-table state; A cells/program entries/triggers/control; F cells + mutable/fresh program slots; N local views + selected program/trigger state; R joint carrier and program mutation | Program text is ordinary writable state under a closed interpreter | `CH08:L319-329` | — |
| SPF040 | F043 `population-evolutionary-search` | `automata.population_evolutionary_search` | addition | `population; fitness_expression; selection; recombination; mutation; size` | S population + fitness/lineage; A genomes/programs/fitness/phase; F complete next population; N whole population + parent groups; R selected/recombined/mutated generation, usually μ | Global selection and multi-parent generational atomicity | `BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L556-560` | — |
| SPF050 | F053 `synchronous-local-state-transform` | `automata.synchronous_local_state_transform` | covered | `seed; stencil; local_law; boundary; feedback` | S fixed-domain input + optional feedback; A local/layer/phase/site values; F all outputs + coupled destinations; N bounded immutable old-state windows; R one shared synchronous pass | No output is readable within its pass; one-shot and feedback are explicit | `CH10:L323-347; N10:L328-347; N03:L135-150,L190,L192-225` | `eca`, `elementary_cellular_automaton`; T02–T07, T21–T24 presets; T44 family-level alias implemented as a preset |
| SPF052 | F055 `weighted-network-state-update` | `automata.weighted_network_state_update` | covered | `network; seed; weights; schedule; learning_law` | S topology + activations/weights/examples/phase; A activations/weights/gradients/targets; F writable units/weights/auxiliaries; N weighted inputs + recurrent/target/criterion data; R coupled activation and optional weight replacement, 1/μ | Mutable weights and layer/recurrence schedules are visible state | `N10:L1021-1023` | Normalizes C045 legacy coverage; no T01–T45 owner; never alias `network_system` |

### `substitua.py` — 15

| ID | Goal 5 family | Canonical constructor | Status | Closed parameters | Five-field skeleton (`S/A/F/N/R`) | Representation/result pressure | Representative sources | Legacy/public relation |
|---|---|---|---|---|---|---|---|---|
| SPF002 | F002 `append-only-sequence-generation` | `substitua.append_only_sequence_generation` | covered | `seed; emitter; control_schema; support` | S word/control/end marker; A symbols/registers/end roles; F changing control + end + fresh suffix; N control/aggregate + optional prefix; R append finite block + update control/end | Intensional fresh support while preserving the complete existing prefix | `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L203-210,L569-599` | T40 split branch; P `constant_digit_sequence` |
| SPF005 | F005 `context-dependent-substitution` | `substitua.context_dependent_substitution` | covered | `seed; productions; context_shape; boundary` | S word/array + boundary; A symbols/boundary markers; F old structure + all output blocks; N bounded old-generation context; R assemble all selected blocks atomically | Variable-length and multidimensional structural replacement | `CH03:L333-337` | `neighbor_dependent_substitution`; T28 2-D preset |
| SPF015 | F016 `first-passage-aggregation` | `substitua.first_passage_aggregation` | addition | `seed; walk_law; contact; release; boundary; target` | S aggregate + walker + release control; A empty/aggregate/walker/boundary; F walker + every destination/attachment/relaunch; N move choices + contact; R μ walk, first-contact attach, relaunch/stop | Replayable unbounded microtrajectory before irreversible growth | `N08:L50; BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L359-360` | — |
| SPF016 | F017 `front-delete-rear-append-system` | `substitua.front_delete_rear_append_system` | covered | `seed; deletion_width; productions; phase_cycle` | S word + phase/end; A symbol/prefix/tail/phase; F consumed prefix + fresh suffix + phase; N removed prefix + phase/tail; R delete, append, advance, or terminal | Noncontiguous write envelope with shrinking and growing support | `CH03:L423-445,L447-471` | `tag_system`; T18 `cyclic_tag_system` preset |
| SPF019 | F020 `global-score-sequential-placement` | `substitua.global_score_sequential_placement` | addition | `seed; score_expression; placement_shape; depletion_kernel; tie_law` | S field/geometry + objects; A scores/empty/occupied/geometric records; F all candidates + induced field writes; N complete scoring/occupancy geometry; R choose winner and add one object, 0/1/μ | Global selection followed by one coupled structural addition | `CH08:L531-547; N08:L223-225` | — |
| SPF022 | F023 `history-dependent-growth-rewrite` | `substitua.history_dependent_growth_rewrite` | addition | `seed; eligibility; provenance_law; boundary` | S occupied support + birth/parent history; A occupancy/provenance/round; F eligible sites + fresh provenance; N occupancy + ancestry; R add all eligible sites and provenance | Equal occupancy can differ because provenance is semantic state | `BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md:L130-151` | — |
| SPF023 | F024 `indexed-history-recurrence` | `substitua.indexed_history_recurrence` | covered | `prefix; recurrence; index_law; invalidity` | S term prefix + next-index marker; A terms/indices/unwritten/end; F fresh next term + moved marker; N all value-addressable history; R compute/append or typed invalid dependency | Value-selected nonlocal reads and append-only support | `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L169-186` | T38 variable-index preset |
| SPF025 | F026 `iterated-erasure-process` | `substitua.iterated_erasure_process` | covered | `seed; erasure_predicate; rank_convention` | S ordered support + round; A item/survivor/rank; F every deletable survivor + round; N complete ordered survivors; R delete selected subset and preserve order | Global current-rank reads and strictly shrinking support | `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L211-214` | `number_theoretic_filtering` preset |
| SPF028 | F029 `local-graph-rewrite` | `substitua.local_graph_rewrite` | addition | `seed; patterns; replacements; match_schedule; interface_schema` | S graph + schedule; A node/edge/port/interface; F every selectable match/attachment/fresh element; N match + dangling interface; R 0/1/many interface-preserving patches | Stable identities, fresh nodes, dangling links, overlap selection | `CH09:L901-965; N09:L495-528,L552-556,L594-600` | — |
| SPF031 | F032 `moving-frontier-shell-accretion` | `substitua.moving_frontier_shell_accretion` | addition | `seed; strip_constructor; rim_law; geometry; terminal_condition` | S surface + open rim; A patch/rim/geometric records; F rim + all possible fresh strip elements; N rim + accumulated geometry; R append/connect/advance or stop | Expanding geometric support without geometry/update axes | `CH08:L581-591; N08:L234-246` | — |
| SPF033 | F034 `multiway-rewrite` | `substitua.multiway_rewrite` | covered | `seed; rewrites; match_semantics; quotient` | S initial carrier states; A carrier values + identity; F union of all applicable matches/outputs; N all matches/context; R one witnessed successor per rewrite, then quotient | Witnesses and multiplicity survive before equal-successor deduplication | `CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L355-369` | `multiway_system` true alias |
| SPF037 | F038 `parallel-independent-substitution` | `substitua.parallel_independent_substitution` | covered | `seed; productions; schedule; geometry` | S items + generation phase; A item/phase/offspring; F all old items + possible offspring support; N each old item + phase; R independent 0/1/many/μ offspring assembled atomically | Empty/variable offspring and generation-wide commit | `CH03:L299-307,L343-363` | T15 merge; T26/T27/T42 presets; `neighbor_independent_substitution` |
| SPF038 | F040 `parallel-network-rewrite` | `substitua.parallel_network_rewrite` | covered | `seed; patches; port_schema; overlap_law` | S labeled graph + ports; A node/edge/port/absence; F all old/constructible elements; N bounded connections/paths; R compatible parallel patches with overlap resolution | Dynamic topology and graph-level atomic commit | `CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L241,L287-331` | `network_rewrite`; broad `network_system` is not exported |
| SPF043 | F046 `random-functional-graph-construction` | `substitua.random_functional_graph_construction` | addition | `nodes; successor_measure` | S labeled node domain + successor law; A node/successor/edge; F every successor slot; N source + complete destination domain; R product μ over complete graph replacements with exactly one successor per node | One-shot distributed stochastic structure creation; external realization performs any draw | `BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md:L589-590` | — |
| SPF049 | F052 `structural-pattern-rewrite` | `substitua.structural_pattern_rewrite` | covered | `expression; patterns; replacements; scan; nonoverlap` | S expression + ordered rewrite data; A operator/atom/variable/binder; F matches + possible replacement nodes; N subtree + structural/scan context; R compatible nonoverlapping forest, 0/1/many | Variable trees, binding context, scan order, and conflicts | `CH03:L531-537; N03:L823-835; CH10:L909-915` | `symbolic_system`; T16 sequential-substitution preset |

### `machina.py` — 8

| ID | Goal 5 family | Canonical constructor | Status | Closed parameters | Five-field skeleton (`S/A/F/N/R`) | Representation/result pressure | Representative sources | Legacy/public relation |
|---|---|---|---|---|---|---|---|---|
| SPF010 | F011 `enumerative-semidecision` | `machina.enumerative_semidecision` | addition | `query; enumeration; predicate; start` | S query + candidate generator/index; A candidates/control/witness; F next candidate/control + witness; N query/candidate/predicate inputs; R advance on failure or emit first witness and stop | Absence is divergence, not a negative answer | `CH10:L975-989; N10:L5-15; N11:L829-855` | — |
| SPF013 | F014 `finite-gate-circuit` | `machina.finite_gate_circuit` | addition | `inputs; wiring; gates; schedule; measurement` | S wires/ancillas + gate/layer cursor; A ordered values/bits/amplitudes/control; F addressed wires + control/output; N gate + wires or amplitude vector; R atomic gate/layer and optional terminal μ | Compare-exchange, reversible Boolean, and unitary algebras stay distinct under fixed wiring | `N10:L904; N12:L331-347,L560-574` | — |
| SPF030 | F031 `mobile-head-grid-rewrite` | `machina.mobile_head_grid_rewrite` | covered | `tape; transitions; head; stencil; boundary` | S grid/tape + one tagged head; A plain symbol or Head(state,symbol); F source + full stencil + every destination; N head/stencil/destination contents; R atomic rewrite/state/move or halt | Source and all possible destinations share one writable frontier | `CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L127-131` | `turing_machine`; T09 mobile, T10 repaired neighbor-updating, T25 2-D presets |
| SPF035 | F036 `nearest-neighbor-retrieval` | `machina.nearest_neighbor_retrieval` | addition | `items; query; metric; index; traversal` | S store/index + query/incumbent/search; A points/index/distance/results; F traversal/incumbent/result; N query + reachable store/index; R advance then return 0/1/many globally nearest items | Dynamic metric traversal, empty stores, and tied witnesses | `N10:L988-996` | — |
| SPF044 | F047 `recursive-function-evaluator` | `machina.recursive_function_evaluator` | covered | `call; definitions; evaluation_order; cache` | S call + definitions/frames/cache; A values/expressions/continuations; F reducible frame + subcalls/results/cache; N call tree/definitions/context/cache; R structural reduce/expand or undefined/divergence | Partiality, minimization, order, and unbounded call structure | `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L237-268,L316-364` | Repaired T41; `function_combination_system` retained only as deprecated metadata |
| SPF045 | F048 `register-machine` | `machina.register_machine` | covered | `program; registers; entry` | S instructions + counter/registers; A integers/opcodes/addresses/halt; F counter + possible written registers; N fetched instruction/condition/operands; R atomic register/counter patch or halt | Dynamic addressing without a new address or update policy | `CH03:L473-509,L519-525` | `register_machine` |
| SPF048 | F051 `stored-program-random-access-machine` | `machina.stored_program_random_access_machine` | addition | `memory; entry; instruction_set` | S writable program/data + machine state; A words/opcodes/addresses/devices; F counter/instruction + all possible memory/device writes; N fetched opcode + indirect operands; R atomic fetch-decode-execute or halt | Self-modifying code and indirect reads/writes remain visible state | `N11:L15-23` | — |
| SPF053 | F056 `priority-dovetailed-oracle-construction` | `machina.priority_dovetailed_oracle_construction` | addition | `approximations; machines; requirements; priority; fair_schedule` | S shared approximation + suspended runs/requirements/scheduler; A oracle bits/registers/restraints/control; F advanced work + shared writes + injured requirements; N runs/approximation/priority; R fair advance, diagonal write, injury update | Nonlocal sharing, fairness, priority, and injury are explicit | `N12:L80-92` | — |

### `media.py` — 14

| ID | Goal 5 family | Canonical constructor | Status | Closed parameters | Five-field skeleton (`S/A/F/N/R`) | Representation/result pressure | Representative sources | Legacy/public relation |
|---|---|---|---|---|---|---|---|---|
| SPF004 | F004 `event-provenance-causal-network` | `media.event_provenance_causal_network` | addition | `event_trace; read_sets; initial_provenance` | S ordered events + producer map/cursor; A event IDs/producers/edges/control; F fresh event/edge slots + producer records + cursor/end control; N event reads + current producers; R emit event/direct dependencies, update provenance, and advance or end | Lossless trace-to-causal graph, fresh identity, provenance, and cursor progression | `CH09:L655-707; N09:L347-355,L378-384` | — |
| SPF008 | F008 `digit-emitting-register-transduction` | `media.digit_emitting_register_transduction` | covered | `seed; register_law; base; digit_projection` | S registers/control/output end; A integers/control/digits/stream markers; F changed registers + next output/end; N complete registers/comparisons; R atomic register update + exactly one digit or terminal | Emission is construction-defining writable state | `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L303-308,L343-350` | T40 split branch; P `constant_digit_register` |
| SPF011 | F012 `error-diffusion-transform` | `media.error_diffusion_transform` | addition | `input; palette; diffusion_kernel; scan` | S raster + cursor/error; A intensity/error/palette/control; F pixel + all future error recipients + cursor; N current value/error/future stencil; R quantize + distribute error forward | Ordered causal scan with coupled future writes | `N10:L348-360` | — |
| SPF012 | F013 `maximal-run-record-transduction` | `media.maximal_run_record_transduction` | addition | `input; record_grammar; direction; scan; feedback` | S input/output/cursor or feedback; A symbol/length/record/end; F record/expanded output + cursor; N maximal homogeneous extent; R emit/expand one self-delimiting run | Variable extents/output, inverse direction, and optional feedback | `CH10:L163-187; N10:L83-85,L171-175; N04:L193-202` | P `look_and_say` feedback preset; flat export; preset source `N04:L193-202` |
| SPF020 | F021 `hash-index-transform` | `media.hash_index_transform` | addition | `key; table; hash_fold; collision; operation` | S table/key/fold/control/result; A keys/hash/buckets/links/results; F control/result + alterable collision path; N input + reachable buckets/chains; R insert/hit/miss then stop | Dynamic address path, exact equality, typed miss | `CH10:L829-839; N10:L976-980` | — |
| SPF041 | F044 `probabilistic-transition-model-fitting` | `media.probabilistic_transition_model_fitting` | addition | `observations; topology; estimator; generation_law; generation_request` | S observations + model/counts + fit/generate phase; A states/probabilities/counts/control; F model + generated slots; N training histories or fitted context; R fit parameters then denote explicit μ over generated paths | Lossless two-phase fit/generation state and replayable probability; realization is external | `CH10:L441-459; N10:L495-501` | — |
| SPF046 | F049 `sampled-causal-order-network` | `media.sampled_causal_order_network` | addition | `region; causal_order; density; event_measure` | S spacetime region + construction phase; A event coordinates/causal edges; F every event/edge; N event-set pairs + reachability/interveners; R μ over event sets mapped deterministically to causal cover replacements | Continuous probability law, global comparisons, and transitive reduction; realization is external | `N09:L816-818` | Distinct from F004 producer-history transform |
| SPF054 | F057 `weighted-prefix-block-transduction` | `media.weighted_prefix_block_transduction` | addition | `input; block_partition; weights_or_tree; direction` | S input + tree/output/cursor; A blocks/weights/tree/bits; F tree/preamble/output/cursor/decoded blocks; N weighted nodes or block/tree; R build tree, emit leaf word, or parse leaf | Independently decodable prefix boundaries and tree provenance | `CH10:L189-205,L235-249; N10:L87-106` | — |
| SPF055 | F058 `nested-interval-symbol-transduction` | `media.nested_interval_symbol_transduction` | addition | `input; probability_model; precision; direction` | S input + interval/cursor/tag; A symbols/probabilities/endpoints/digits; F interval/tag/cursor/decoded symbols; N symbol + cumulative partition; R refine shared interval, finalize, or invert | One message-wide interval with exact endpoint semantics | `N10:L108-121` | — |
| SPF056 | F059 `history-reference-record-transduction` | `media.history_reference_record_transduction` | addition | `input; match_policy; dictionary; record_grammar; direction` | S input + cursor/history/output; A literal/pointer/offset/length; F records/cursor/dictionary/reconstruction; N remaining input + prior matches; R emit literal/reference or copy history | Encoding depends on prior history, not only current symbols | `CH10:L209-267; N10:L123-153` | — |
| SPF057 | F060 `recursive-uniform-region-decomposition` | `media.recursive_uniform_region_decomposition` | addition | `input; root_region; split; uniformity; cutoff; direction` | S array + region work tree; A sample/bounds/leaf/split/work; F node + all children or output region; N every sample in region; R leaf or recursive child creation | Dynamic hierarchical support rather than a flat scan | `CH10:L233-239,L269-279; N10:L154-168` | — |
| SPF058 | F061 `orthogonal-basis-coefficient-transform` | `media.orthogonal_basis_coefficient_transform` | addition | `input; basis; ordering; retention; quantization; direction` | S numeric block + basis/selection; A samples/coefficients; F coefficient vector + optional reconstruction; N full block + basis; R global project/select/quantize/invert then stop | Global mixing, exact/lossy representation, one-shot termination | `CH10:L281-305; N10:L181-288` | — |
| SPF059 | F062 `predictive-residual-transduction` | `media.predictive_residual_transduction` | addition | `input; predictor; history; fitting; residual_code; direction` | S samples + history/model/cursor; A samples/coefficients/residuals/codes; F model/residual/reconstruction/cursor; N sample + causal history/model; R fit/update, emit/reconstruct, advance | Representation depends on causal history and model state | `N10:L424` | — |
| SPF060 | F063 `aligned-xor-stream-transduction` | `media.aligned_xor_stream_transduction` | addition | `input; keystream; alignment; generator` | S input + supplied/generated stream/cursor; A bits/generator/control; F output + cursor/generator; N aligned bits + generator state; R XOR and advance | Explicit keystream/replay state and bijective involution | `CH10:L539-565,L599-605` | — |

### `criteria.py` — 9

| ID | Goal 5 family | Canonical constructor | Status | Closed parameters | Five-field skeleton (`S/A/F/N/R`) | Representation/result pressure | Representative sources | Legacy/public relation |
|---|---|---|---|---|---|---|---|---|
| SPF014 | F015 `finite-model-satisfaction` | `criteria.finite_model_satisfaction` | addition | `axioms; finite_domain; signatures; fixed_tables` | S axioms/domain/partial tables; A domain/table/expression/assignment; F unknown table entries/result; N complete tables + every assignment; R 0/1/many universally satisfying completions | Exact universal witnesses; no-solution distinct from invalidity | `CH12:L1073-1095; N12:L1189-1203,L1245-1257` | — |
| SPF017 | F018 `geometric-embedding-relation` | `criteria.geometric_embedding_relation` | addition | `mesh; growth; metric_constraints; boundary_embedding` | S intrinsic mesh + known/unknown coordinates; A real coordinates/metrics/cell roles; F added material + every movable coordinate; N whole mesh + adjacency metrics; R 0/1/many/I valid embeddings | Continuous nonlocal completion; relaxation solver stays external | `CH08:L563-569; N08:L226` | — |
| SPF018 | F019 `global-equation-relation` | `criteria.global_equation_relation` | addition | `equation; domain; known_assignments; witness_schema` | S equation/domain/partial assignment; A exact values/variables/terms; F unknown tuple/witness; N all terms/coefficients/knowns; R every exact solution, finite or I | Zero/one/many/intensional solutions without solver policy | `CH12:L885-905; N12:L901-966` | — |
| SPF024 | F025 `inverse-local-system-reconstruction` | `criteria.inverse_local_system_reconstruction` | addition | `observations; local_law; boundary; unknown_schema; search_order` | S observations + unknown/constraint work; A observed/unknown/equation/branch/solution; F unknowns/work/solutions; N observations + all dependency constraints; R algebraic or witnessed branch/prune reconstructions | Branching, contradiction pruning, and derivation witnesses | `CH10:L575-633; N10:L531-544,L608-624` | — |
| SPF027 | F028 `local-factor-weighted-relation` | `criteria.local_factor_weighted_relation` | addition | `seed; factors; reduction; normalization; objective` | S partial candidate + factors/results; A labels/factors/weights/decisions; F unknowns + weight/distribution/results; N all overlapping scopes + normalization domain; R weighted/feasible/optimal 0/1/many/μ/I completions | Global normalization or argmin over local factors | `N10:L493-494` | — |
| SPF029 | F030 `local-satisfaction-relation` | `criteria.local_satisfaction_relation` | covered | `partial_assignment; templates; boundary; obligations` | S partial configuration + templates; A unknown/assigned/obligation; F complete unknown region; N every overlapping predicate scope; R all jointly satisfying completions, 0/1/many/I | Joint consistency is not independent per-locus update | `CH09:L595-615; N09:L324-330` | T31; T32 template name; T33 seeded-template preset |
| SPF042 | F045 `program-randomization-test` | `criteria.program_randomization_test` | addition | `observed; surrogate_law; program; statistic; replicates; calibration` | S observed + surrogate/evaluator work/results/phase; A data/results/frames/ranks/scores/control; F surrogates/work/results/aggregate/decision; N current observed/surrogate input + evaluator work + embedded outputs; R μ surrogates, closed evaluator microsteps, calibrated criterion | Replay evidence, visible nested provenance, typed decision; `program`/`statistic` is closed Rule-owned evaluable data, never recursive `apply` | `CH10:L515-533` | — |
| SPF047 | F050 `stochastic-local-search` | `criteria.stochastic_local_search` | addition | `incumbent; objective; constraints; proposal; acceptance` | S incumbent + cost/proposal control; A candidate/cost/locus/acceptance; F all proposal loci + cost/control; N whole incumbent/objective + proposal; R μ proposal then accepted patch or quiescent continuation | Rejection continues and is neither terminal nor no-successor | `CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L553-596` | — |
| SPF051 | F054 `weighted-history-sum-relation` | `criteria.weighted_history_sum_relation` | addition | `domain; side_data; histories; action; measure; observables` | S history domain/action/measure/request; A field/path/history/complex amplitude; F aggregate outputs; N complete admissible history space; R exact weighted sum/integral | Extreme nonlocality, complex interference, intensional integration | `N09:L880,L955-957` | — |

### `dynamica.py` — 3

| ID | Goal 5 family | Canonical constructor | Status | Closed parameters | Five-field skeleton (`S/A/F/N/R`) | Representation/result pressure | Representative sources | Legacy/public relation |
|---|---|---|---|---|---|---|---|---|
| SPF006 | F006 `continuous-event-dynamics` | `dynamica.continuous_event_dynamics` | addition | `seed; geometry; flow_law; reset_law; terminal_condition` | S position/velocity/time + geometry; A real state/boundary labels; F trajectory state + event record; N current state + geometry; R flow to earliest hit then discontinuous reset | Intrinsic event time and hybrid continuous/discrete result | `BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L60-61` | — |
| SPF036 | F037 `ordinary-differential-flow` | `dynamica.ordinary_differential_flow` | addition | `seed; rhs; parameters; duration_or_event` | S time + finite continuous vector; A real/vector/parameter/event; F evolving vector + semantic event/sample slots; N state/time/parameters/events; R maximal or selected ODE flow segment, 0/1/many/I | Nonunique flows, singularities, solver/horizon separation | `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L901-902,L953-980` | — |
| SPF039 | F041 `partial-differential-relation` | `dynamica.partial_differential_relation` | covered | `domain; coefficients; differential_relation; side_data` | S continuous domain + initial/boundary/partial field; A scalar/vector/tensor/metric fields; F unknown interior/spacetime field; N differential germs + all side dependencies; R 0/1/many/I compatible fields or μ | Nonuniqueness and intensional fields; numerical solver is realization | `CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L625-674; N08:L84-105,L322-328` | T45 canonical constructor; `pde` true alias |

## Close roles outside the family matrix

| Goal 5 role | Catalog treatment | Boundary |
|---|---|---|
| F010 `encode-evolve-decode-interface` | Callable-free `RoleEntry` for an interface role; no SPF ID and no canonical family constructor | A concrete encoder or decoder with its own invariant commit may be an ordinary `media` program, while composition around an unchanged target belongs to run/query tooling |
| F042 `percolation-connectivity-analysis` | Callable-free `RoleEntry` for an observer role; no SPF ID and no canonical family constructor | Occupation may be a Seed law, but spanning/connectivity over the completed sample is an observer or analysis result |

T08 is separately a retired Seed role from the legacy catalog. It is not one of
these two Goal 5 close-role groups.

## T01–T45 migration ledger

Goal 5 disposition and end callable kind are independent. `P` means a closed
parameter preset/refinement, `A` a true alternate spelling with identical
arguments and expansion, `K` a total lossless legacy argument/name adapter,
`C` the exact canonical constructor, and `M` metadata-only with no callable.
A name that binds or validates semantic parameters is `P` even when Goal 5's
family-level disposition is `alias`.

The ledger preserves each row's exact Goal 5 candidate join and the narrowest
source needed to justify its named callable. `F`-level family sources alone are
not presumed to establish a narrower preset. `CHnn` is the repaired chapter
Markdown and `Nnn` its repaired Notes Markdown. T06 uses the completed Goal 2
preset evidence because Goal 5 retained the preset but intentionally did not
promote the property-only passages into a mechanics candidate.

| Legacy ID | Legacy label | Goal 5 disposition | Candidate(s) | Normalized target | End callable treatment | Named-construction evidence | Exact migration |
|---|---|---|---|---|---|---|---|
| T01 | Elementary Cellular Automata | retain-family | C090 | SPF050 / F053 | P `eca`; A `elementary_cellular_automaton` | `CH03:L29-56` | Bind binary 1-D radius-one synchronous feedback; family constructor remains `synchronous_local_state_transform` |
| T02 | Multi-Color Nearest-Neighbor Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `multicolor_cellular_automaton` | `N03:L135-150` | Bind finite palette, nearest-neighbor stencil, and feedback |
| T03 | Totalistic Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `totalistic_cellular_automaton` | `CH03:L91-96` | Bind totalistic quotient Rule |
| T04 | Three-Color Totalistic Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `three_color_totalistic_cellular_automaton` | `CH03:L89-96,L109-110` | Bind T03 to three colors and radius one |
| T05 | Higher-Color Totalistic Cellular Automata | merge | C090 | SPF050 / F053 | P `higher_color_totalistic_cellular_automaton` | `N03:L164-185` | T03 parameterization with `colors >= 4`; no family entry |
| T06 | Quiescent-Background-Preserving Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `quiescent_cellular_automaton` | Goal 2-preserved `T(b,…,b)=b`; `CH03:L101,L649; CH06:L101`; `goal-1/25-T06-QUIESCENT.md` | Validate the quiescent-background Rule restriction; no executor change |
| T07 | Left-Right Symmetric Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `symmetric_cellular_automaton` | `N03:L7-10; N05:L89-100` | Validate reflection-invariant local Rule data |
| T08 | Initial-Condition Classes | retire-role | — | none; `ca.seeds` | M | Goal 5 Seed-role decision; no executable construction source | Permanent tombstone linking exact/constructive/probabilistic Seed constructors and laws |
| T09 | Mobile Automata | retain-preset | C047 | SPF030 / F031 | P `mobile_automaton` | `CH03:L169-185` | Bind the single tagged-head, center-write profile |
| T10 | Extended Mobile Automata | repair | C056 | SPF030 / F031 | P `neighbor_updating_mobile_automaton`; K `extended_mobile_automaton` | `CH03:L197-207` | Correctly bind the neighbor-updating fixed-block result; deprecated old name delegates losslessly |
| T11 | Generalized Mobile Automata | retain-family | C030 | SPF032 / F033 | P `generalized_mobile_automaton` | `CH03:L231-247` | Bind multi-active move/split/delete mechanics; do not route through the single-head family |
| T12 | Turing Machines | retain-family | C049 | SPF030 / F031 | P `turing_machine` | `N03:L294-333` | Bind tagged control state, symbol write, and edge movement |
| T13 | Neighbor-Independent Substitution Systems | retain-family | C061 | SPF037 / F038 | P `neighbor_independent_substitution` | `CH03:L299-307` | Bind independent string items and generation concatenation |
| T14 | Neighbor-Dependent Substitution Systems | retain-family | C011, C055 | SPF005 / F005 | P `neighbor_dependent_substitution` | `CH03:L333-337; CH05:L211-227; N05:L360-367` | Bind contextual word neighborhoods |
| T15 | Creation-Destruction Substitution Systems | merge | C061 | SPF037 / F038 | P `creation_destruction_substitution` | `CH03:L343-363` | Bind empty/nonempty offspring data; no separate family or commit law |
| T16 | Sequential Substitution Systems | retain-preset | C080 | SPF049 / F052 | P `sequential_substitution` | `CH03:L369-379` | Bind flat string structure, ordered scan, and one nonoverlapping splice |
| T17 | Tag Systems | retain-family | C091 | SPF016 / F017 | P `tag_system` | `CH03:L423-445` | Bind fixed front deletion and rear production |
| T18 | Cyclic Tag Systems | retain-preset | C091 | SPF016 / F017 | P `cyclic_tag_system` | `CH03:L447-471` | Add visible cyclic production phase |
| T19 | Register Machines | retain-family | C073 | SPF045 / F048 | C `register_machine` | `CH03:L473-509,L519-525` | Exact canonical path `ca.catalog.machina.register_machine` |
| T20 | Symbolic Systems | retain-family | C089 | SPF049 / F052 | P `symbolic_system` | `CH03:L531-537; N03:L823-835; CH10:L909-915` | Bind expression-tree patterns, templates, and scan semantics |
| T21 | Two-Dimensional Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `cellular_automaton_2d` | `CH05:L27-34` | Bind square support and 2-D local stencil |
| T22 | Moore-Neighborhood Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `moore_cellular_automaton` | `CH05:L67-86` | Bind the 2-D Moore stencil |
| T23 | Three-Dimensional Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `cellular_automaton_3d` | `CH05:L95-123; N06:L55-66` | Bind cubic support and 3-D stencil |
| T24 | Higher-Dimensional Lattice Cellular Automata | retain-preset | C090 | SPF050 / F053 | P `lattice_cellular_automaton` | `N05:L36-58,L66-88` | Bind dimension/incidence/stencil descriptors |
| T25 | Two-Dimensional Turing Machines | retain-preset | C049 | SPF030 / F031 | P `turing_machine_2d` | `CH05:L127-131; N05:L211-217` | Bind planar topology, headings, and movement ports |
| T26 | Two-Dimensional Substitution Systems | retain-preset | C061 | SPF037 / F038 | P `substitution_system_2d` | `CH05:L173-190` | Bind compatible 2-D offspring geometry |
| T27 | Geometric Replacement And Fractal Systems | repair | C061 | SPF037 / F038 | P `geometric_substitution`; M old `fractal_system` wording | `CH05:L191-214; N05:L286-337` | Construction is posed geometric substitution; “fractal” remains output/property metadata |
| T28 | Neighbor-Dependent Two-Dimensional Substitution Systems | retain-preset | C055 | SPF005 / F005 | P `context_dependent_substitution_2d` | `CH05:L211-227; N05:L360-367` | Bind 2-D contextual patterns and compatible mosaic commit |
| T29 | Network Systems | retain-family | C062 | SPF038 / F040 | C `parallel_network_rewrite`; A `network_rewrite` | `CH05:L239-248,L287-331` | Restrict to topology rewrite; broad `network_system` is M and cannot also name F055 |
| T30 | Multiway Systems | retain-family | C051 | SPF033 / F034 | A `multiway_system` | `CH05:L355-369; N05:L527-528,L549-578` | Same arguments and expanded fields as canonical `multiway_rewrite` |
| T31 | Local Constraint Systems | retain-family | C043 | SPF029 / F030 | P `local_constraint_system` | `CH05:L433-479; CH09:L595-615; N09:L324-330` | Bind local predicates over an unknown completion region |
| T32 | Template Constraint Systems | alias | C043 | SPF029 / F030 | P `template_constraint_system` | `CH05:L475-488` | Bind allowed-template representation; not a zero-delta callable alias |
| T33 | Seeded Template Constraint Systems | retain-preset | C042, C043 | SPF029 / F030 | P `seeded_template_constraint_system` | `CH05:L475-498,L535-536` | Put fixed/required occurrences in Seed and obligations |
| T34 | Arithmetic Iteration Systems | retain-preset | C037 | SPF026 / F027 | P `arithmetic_iteration` | `CH04:L53-54` | Bind an exact arithmetic map expression |
| T35 | Piecewise Integer Maps | retain-preset | C037 | SPF026 / F027 | P `piecewise_integer_map` | `CH04:L111-118` | Bind integer domain and guarded/residue clauses |
| T36 | Digit-Reversal Arithmetic Systems | retain-preset | C037 | SPF026 / F027 | P `digit_reversal_map` | `CH04:L153-162; N04:L170-179` | Bind positional representation and reversal map |
| T37 | Recursive Sequences | retain-family | C078 | SPF023 / F024 | P `recursive_sequence` | `CH04:L169-186` | Bind fixed-index recurrence and append state |
| T38 | Variable-Index Recursive Sequences | retain-preset | C078 | SPF023 / F024 | P `variable_index_recursive_sequence` | `CH04:L179-186` | Bind value-selected history addresses |
| T39 | Number-Theoretic Filtering Systems | retain-family | C035 | SPF025 / F026 | P `number_theoretic_filtering` | `CH04:L211-214; N04:L418-430` | Bind divisibility/current-rank erasure criteria |
| T40 | Mathematical-Constant Digit Systems | split | C003, C017 | SPF002 / F002 and SPF008 / F008 | M split record; P `constant_digit_sequence` and P `constant_digit_register` branches | sequence `N04:L203-210,L569-599`; register `CH04:L303-308,L343-350; N04:L561-562` | No umbrella callable or `kind=` dispatch; each explicit branch callable has exactly one SPF target |
| T41 | Function-Combination Systems | repair | C072 | SPF044 / F047 | C `recursive_function_evaluator`; M old wording | `N04:L237-268,L316-364` | Replace role-like combination label with executable recursive reduction; no lossy old callable |
| T42 | Continued-Fraction-Driven Substitution Systems | retain-preset | C061 | SPF037 / F038 | P `continued_fraction_substitution` | `CH04:L454-461; N04:L753-754` | Bind a finite visible production schedule obtained from verified continued-fraction data |
| T43 | Iterated Maps | retain-family | C037 | SPF026 / F027 | C `iterated_map` | `CH04:L53-54,L111-118,L472-491` | Exact canonical path `ca.catalog.automata.iterated_map` |
| T44 | Continuous Cellular Automata | alias | C090 | SPF050 / F053 | P `continuous_cellular_automaton` | `CH04:L546-562,L565-616` | Bind continuous-valued Alphabet/local law but remain discrete-time F053; not F041 |
| T45 | Partial Differential Equation Systems | retain-family | C063 | SPF039 / F041 | C `partial_differential_relation`; A `pde` | `CH04:L625-674; N04:L933-940` | Preserve relation-valued 0/1/many/I signature; neither spelling implies a solver |

## Metadata and implementation contract

The matrix's `Fxxx` cell is the exact lookup key for both the corresponding
family-definition row in `goal-5/11-FAMILIES.md` and five-field row in
`goal-5/api-pressure.md`. Family anchors and narrower named-construction
anchors are repeated here so Goal 7 can implement presets without reopening
taxonomy. The T ledger and evidence crosswalk are the exact migration join to
`goal-5/10-RECONCILE.md` and `goal-5/candidates.md`.

`catalog/entries.py` should expose frozen values equivalent to:

```python
FamilyEntry(
    family_id,             # SPFnnn
    audit_family_id,       # Fnnn provenance
    slug,
    home,
    constructor_module,    # import-name string
    constructor_name,      # identifier string
    coverage,              # covered | addition
    closed_parameters,
    source_refs,
    api_pressure_ref,
    name_relations,
)

RoleEntry(
    audit_role_id,         # exactly F010 or F042
    slug,
    role_kind,             # interface | observer
    source_refs,
    boundary,
)

LegacyEntry(
    legacy_id,             # Tnn
    label,
    disposition,
    candidate_ids,
    source_refs,
    targets,               # tuple[LegacyTarget, ...], length 0, 1, or 2
)

LegacyTarget(
    branch_name,           # required for a split; absent otherwise
    target_family_id,
    callable_spelling,     # absent for metadata-only relations
    treatment,             # C | P | A | K | M
    source_refs,
)

NameEntry(
    spelling,
    owner_module,
    kind,                  # C | P | A | K
    target_family_id,
    delegate_import_name,
    flat_export,
    closed_binding_summary,
    legacy_entry_ids,
    source_refs,
)
```

These are illustrative closed record shapes, not authorization to add another
public module. Their fields contain no callable, `SimpleProgram`, component
instance, Rule tag, executor key, or dispatch handler.

Category modules explicitly implement their own canonical constructors and
delegators and never import `entries`. `catalog/__init__.py` explicitly imports
the six category modules, the selected symbols, and the metadata values; it
does not synthesize Python functions from the matrix.

### Export and equivalence gates

- All 60 canonical constructors are category-qualified and explicitly flat-
  exported from `ca.catalog`; none is exported from root `ca`.
- Every `C`, `A`, and `P` spelling named in the family matrix or T ledger is
  also an explicit flat catalog export because the names above are unique.
- T40's two explicitly named `P` branch spellings are likewise flat exports;
  the T40 split record itself remains non-callable.
- Deprecated `K` adapters remain category-qualified and are omitted from flat
  `catalog.__all__`. `M` entries have no callable anywhere.
- Reserved flat names are `entries`, `automata`, `substitua`, `machina`,
  `media`, and `criteria`, `dynamica`, plus the root module/operation names
  fixed in `api.md`.
- A canonical constructor wins any future collision. Otherwise no automatic
  runtime precedence exists: one spelling is selected explicitly or every
  contender remains category-qualified.
- For every accepted argument tuple, `A` expansion must equal its declared
  canonical or preset delegate exactly. `P` expansion must equal canonical
  family expansion after its declared closed binding. `K` must be total and
  lossless over its advertised legacy domain.
- Every callable spelling has exactly one SPF target. T40 deliberately has no
  umbrella callable or family-selection parameter.
- T40 is represented by two typed `LegacyTarget` branches, each joining one
  callable spelling to one SPF. No relation is left solely in prose.

### Serialization and invocation-provenance gate

Canonical serialization remains the expanded five-field payload and never
imports the catalog. It does not encode or reconstruct SPF, F, T, category,
invoked spelling, or constructor arguments. Those values remain callable-free
catalog metadata, not program provenance.

An application may separately persist a user manifest containing an invoked
spelling, closed arguments, and the digest of the resulting canonical payload.
That manifest is outside the `ca` semantic and codec contracts: loading a
program neither requires nor returns it, and it cannot participate in
`SimpleProgram` equality, application, or rollout.

## Goal 7 implementation obligations

1. Add the six category modules in dependency order after the five component
   algebras and `program.py` exist.
2. Implement reusable component constructors before any whole-program family;
   a catalog constructor only composes those values.
3. Implement each canonical exact-slug constructor once in its primary module.
4. Add presets/aliases/adapters only after canonical expansion is available,
   with expansion-equivalence tests driven by the T ledger.
5. Populate callable-free SPF/F/T/name metadata and explicit flat exports
   without adding discovery registration or ID dispatch.
6. Test each of the 60 expanded values through the same compatibility
   validation and family-blind `apply`; Stage 6 defines the representative
   semantic pressure fixtures rather than creating 60 executor tests.
7. Verify canonical codecs contain no catalog identity or invocation history;
   test callable expansions directly against their declared family delegates.
8. Remove or adapt current family-string construction only during Goal 7; this
   Stage 5 plan does not change `src/ca`.

## Exact verification contract

- Canonical research IDs equal exactly:
  F001–F009, F011–F038, F040–F041, and F043–F063.
- SPF IDs equal exactly SPF001–SPF060, once each.
- Canonical constructor identifiers and `home.constructor` pairs are unique.
- Home counts are exactly 11 automata, 15 substitua, 8 machina, 14 media,
  9 criteria, and 3 dynamica.
- Coverage is exactly 19 `covered` and 41 `addition`.
- Every family row has a nonempty closed-parameter list, all five labeled
  fields, a pressure/result statement, a direct Book anchor, and its F-keyed
  Goal 5 family/API references.
- Legacy IDs equal T01–T45 exactly once. Dispositions count exactly
  15 retain-family, 21 retain-preset, 2 merge, 3 repair, 2 alias,
  1 retire-role, and 1 split.
- Every T row has the exact Goal 5 candidate join and named-construction source
  evidence; T08 alone has no mechanics candidate or Book construction anchor.
- T08 alone has zero SPF targets; T40 alone has two; every other T row has one.
- The close-role table has exactly F010 and F042, with no SPF or constructor.
- No name maps to multiple SPFs; no `M` entry is callable; no `K` entry is flat.
- Core/application modules never import `catalog`; `entries` contains no
  callables; canonical codecs do not require SPF/F/T/name resolution.
