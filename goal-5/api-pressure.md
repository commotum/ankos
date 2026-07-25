# Minimal API Pressure Test

## Result

The five-part API survives the whole-book taxonomy:

```python
class SimpleProgram:
    seed: Seed
    alphabet: Alphabet
    frontier: WritableRegion
    neighborhood: ReadableRegion
    rule: Rule
```

All 60 executable semantic families fit these five components. The other two
mechanics groups are interface or analysis roles, not additional programs. No
family supplies a counterexample that requires a sixth top-level component,
and none requires a configurable `UpdatePolicy`.

This conclusion applies to the *minimal conceptual API*. The current
`simple_programs.md` contract cannot cover the inventory unchanged: it fixes a
finite `Z4` coordinate model, finite selectors, per-coordinate scalar rule
results, and one synchronous discrete copy-through step. Those restrictions
must be generalized, but the public component list does not need to grow.

## Precise Five-Component Contract

### `Seed`

`Seed` is a source of typed initial configurations, not merely one materialized
array. It may denote:

- one exact configuration;
- a constructive family of configurations;
- a probability law with explicit replayable entropy;
- partial data such as a boundary, input, or constraint assignment; or
- a finite or intensional presentation of an infinite or continuous object.

The generated configuration carries its support, topology, geometry, defaults,
invariants, and any visible control state. This is why `Domain`, `Shape`,
`Boundary`, and `ConfigurationSchema` do not need to be additional top-level
program components.

### `Alphabet`

`Alphabet` is a closed structural value schema. It is not restricted to a
finite palette of cell colors. It may contain tagged and product values,
numbers, words, records, ports, graph elements, fields, instructions,
probabilities, or symbolic expressions. Book names and semantic family names
remain data, aliases, or preset constructors over these schemas.

### `Frontier`

`Frontier` is the complete writable region for the application under
consideration: every existing or fresh component that the rule may replace in
that application. It may be finite, intensional, continuous, structured, or
dynamically derived from the current configuration.

It is not a second, narrower list of rule-firing sources. Applicability can be
encoded by alphabet tags and tested by the rule. For a mobile automaton or
Turing machine, for example, the writable frontier includes the tagged source
and every possible destination; the rule identifies the active tag and returns
the coupled source/destination replacement.

### `Neighborhood`

`Neighborhood` is the readable region supplied to the rule. It may be a local
stencil, a span, a graph path, a complete prefix, a whole configuration, a
boundary field, a history, a metric index, or differential data. “Neighborhood”
therefore describes read capability, not geometric locality.

### `Rule`

`Rule` is a closed, serializable relation from readable data to complete atomic
replacements of the writable region:

```text
ReadableRegion
    -> zero, one, or many frontier replacements
    -> or a probability measure over replacements
```

Its result distinguishes advancement, quiescence, termination, invalidity,
undefined or divergent evaluation, and alternative derivation witnesses.
Replacements may be scalar assignments, words or spans, graph edits, bags of
children, fields, or symbolic solution sets. Scheduling, conflict resolution,
emission, stopping, and construction-specific commit choices are rule
semantics expressed as closed data—not separate public policies.

The framework supplies only universal application semantics:

1. obtain one immutable input configuration;
2. resolve its writable frontier and readable neighborhood;
3. evaluate the rule relation;
4. validate that every returned write lies within the frontier;
5. commit each complete replacement atomically while preserving everything
   outside the frontier; and
6. retain outcome, branch, probability, and witness information.

A practical solver need not enumerate an infinite relation. It may return or
query an intensional solution set. A stochastic runner may sample a
probability-bearing result using an explicit run key. Horizons, solver choices,
realization bounds, observers, renderers, and trace requests belong to the run
or tooling layer, not to `SimpleProgram`.

## Family-by-Family Mapping

The table below tests mechanics, not Book terminology. A construction name is
not promoted to a public class merely because its preset is useful.

| Family | Seed | Alphabet | Frontier (write) | Neighborhood (read) | Rule | Verdict | Residual pressure |
|---|---|---|---|---|---|---|---|
| F001 `alternating-partition-local-evolution` | Complete lattice or spin field with initial block alignment/checkerboard phase and boundary data | Cell, spin, particle, or amplitude values plus an explicit phase marker | All members of the active disjoint blocks or parity class, plus the phase locus | Old contents of each active block, or each active site and its local spin neighborhood | One joint deterministic, unitary, or distributed replacement of active blocks followed by phase toggle | fits-five | Partition schedule is configuration and Rule data; no separate update-policy field. |
| F002 `append-only-sequence-generation` | Initial word, counter or aggregate state, end marker, and native support | Symbols, register values, and append-frontier/control tags | The end marker, changing registers, and every fresh suffix position that may be created | Counter or aggregate inputs, optionally the complete existing prefix | Atomically replace the append frontier with a finite emitted block, updated control, and a new end marker | fits-five | Growing support is an intensional writable frontier and typed replacement. |
| F003 `asynchronous-local-state-automaton` | Complete lattice state with initial scan, readiness, or synchronization control | Cell values plus cursor, readiness, or synchronization tags | The selected writable stencil and control loci; for unresolved random choice, the union of all selectable stencils | Current values visible to the selected locus and scheduler/readiness state | Choose or recognize one locus, replace its stencil immediately, and advance control; stochastic choice is a replacement distribution | fits-five | One API step is one asynchronous commit, so later steps naturally read the write. |
| F004 `event-provenance-causal-network` | Ordered update-event history or active-cell trace with initial producer provenance | Event IDs, source positions, producer records, dependency edges, and cursor/end tags | Every event-node and dependency-edge slot the trace can create, plus accumulated producer records | Each event's read positions and the current producer record for every supplied value | Create the event node, emit its direct producer-dependency edges, update producer provenance, and advance | fits-five | A derived one-shot graph is still an executable transform; it differs from sampled geometric causal order by consuming explicit producer history. |
| F005 `context-dependent-substitution` | Initial word or array with dimensional support and boundary state | Symbol values and any boundary markers | The complete old structure and all output blocks that may replace it | Each locus's bounded contextual neighborhood from the old generation | Jointly choose rule-supplied context-indexed blocks and atomically assemble one new word or array | fits-five | Variable length and dimension change replacement shape, not the five contracts. |
| F006 `continuous-event-dynamics` | Table geometry, initial continuous position, velocity, clock, and stopping horizon | Real position, velocity, time, and boundary labels | The continuous trajectory state and optional next-hit record | Current position and velocity plus the geometry needed to find the next intersection | Flow to the earliest boundary hit, then atomically reflect velocity and advance time | fits-five | Event time is calculated by Rule from a nonlocal readable geometry, not by an update-policy field. |
| F007 `coupled-field-mobile-locus-evolution` | Initial field lattice with exactly one crack marker and complete boundary state | Product values carrying field state, occupancy, and mobile-marker role | The whole next field slice plus every possible crack source, destination, and destructive-write locus | Local field stencils and the marker's readable destination region | One joint replacement updates the distributed field and moves the marker while destroying the rule-selected destination | fits-five | Heterogeneous all-field and single-marker effects are one structured frontier replacement. |
| F008 `digit-emitting-register-transduction` | Initial register tuple, control state, output stream, and end marker | Integer registers, comparison/control tags, base digits, and stream markers | Every register that may change plus the next output slot and moved end marker | The complete register tuple and algorithm-specific comparisons | Atomically update registers and emit exactly one digit, or return no replacement at termination | fits-five | The emitted stream is ordinary writable state rather than a separate output axis. |
| F009 `driven-relaxation` | Stable height field with boundaries and initial drive/relax phase | Nonnegative heights plus drive, unstable, and phase tags | The drive locus and every site and neighbor that an avalanche may alter, possibly the whole finite field | The height field through local toppling stencils and the current drive/relax phase | Select and apply a drive, then return the conservative toppling closure or equivalent phase-tagged microsteps; random drive is distributed | fits-five | Nested relaxation is Rule closure or visible control state, not a sixth scheduler field. |
| F010 `encode-evolve-decode-interface` | Source input together with the wrapped target's initial configuration | Tagged source, encoded-target, target-state, and decoded-output values | Encoded target initialization and decoded result slots | The source input and whichever target trajectory features the stop and decoder read | Relationally compose rule-supplied encoding, unchanged target evolution, stopping, and decoding into zero, one, or many outputs | close-role | This polymorphic wrapper is representable but is not an independent executable mechanics family. |
| F011 `enumerative-semidecision` | Query with the initial candidate-generator state and index | Candidates, indices, query values, control states, and witness/terminal tags | Next-candidate and control slots plus the possible witness output | The query, current candidate, enumeration state, and predicate inputs | Apply the supplied predicate; on failure generate the next candidate, and on success write the witness and halt applicability | fits-five | Undefinedness is an infinite trajectory with no witness, so no separate termination field is needed. |
| F012 `error-diffusion-transform` | Input raster with scan cursor and zeroed error state | Intensity, accumulated error, palette value, and cursor/control tags | The current pixel, every future error recipient, and the cursor positions that may change | Current intensity plus incoming error and the rule-selected future-neighbor stencil | Quantize once and atomically write the palette value, weighted future errors, and advanced cursor | fits-five | Scan order and causal error state live visibly in Seed, Alphabet, Frontier, and Rule. |
| F013 `maximal-run-record-transduction` | Input carrier, scan state, extent-record grammar, and empty output; the look-and-say preset feeds output back as the next input | Symbols, lengths, tagged records, cursor, and end markers | Output record positions and cursor; inverse mode writes expanded symbols | The maximal equal extent beginning at the cursor and its symbol | Emit or expand one extent record and advance, or atomically map all extents | fits-five | Maximal-run boundaries are Rule-readable structure; variable output and optional feedback need no update field. |
| F014 `finite-gate-circuit` | Input wire values with ancillas where needed, visible gate or layer cursor, and optional measurement output | Ordered values, bits, or complex amplitudes plus gate-control and result tags | Every wire addressed by the current comparator, reversible gate, or unitary gate, plus control and terminal output loci | The current gate descriptor and its addressed wire values; the whole amplitude vector where the representation requires it | Apply the next fixed gate or disjoint layer atomically and advance control; compare-exchange emits ordered values, reversible gates permute bits, and terminal quantum measurement returns a squared-magnitude distribution | fits-five | Non-reversible comparison, reversible Boolean, and unitary gates share fixed wiring and schedule; gate algebra is Rule data, not a sixth field. |
| F015 `finite-model-satisfaction` | Axioms, finite domain, operator signatures, and fixed or unknown table entries | Domain elements, unresolved/table values, expression values, and assignment tags | All unknown operator-table entries or the candidate-model output | The axioms, complete candidate tables, and every variable assignment | Return exactly the zero, one, or many table completions for which all assignments satisfy all axioms | fits-five | Universal model satisfaction is a global relational Rule; solver order is not semantic state. |
| F016 `first-passage-aggregation` | Aggregate, one released walker, boundary state, release control, and target size | Empty, aggregate, walker, boundary, and release-control states | Current walker site, every possible next site, possible attachment site, and all possible relaunch loci | Local move choices and aggregate contact, plus any nonlocal release or escape boundary information | A rule-supplied distribution moves the walker; first contact replaces it by aggregate and atomically relaunches or terminates | fits-five | The unbounded first-passage micro-schedule is ordinary repeated five-field evolution. |
| F017 `front-delete-rear-append-system` | Initial word with cyclic phase and end markers | Symbols plus prefix, tail, phase, and terminal markers | The rule-sized consumed prefix, appendable tail/fresh suffix, and phase marker | The removed prefix symbols, phase, and tail boundary needed to assemble the result | Atomically delete the rule-specified prefix, append its selected block, advance phase, or return no replacement | fits-five | A noncontiguous structural frontier can denote the complete possible-write envelope. |
| F018 `geometric-embedding-relation` | Mesh topology, intrinsic growth profile, known boundary embedding, and unknown-coordinate initialization | Real coordinates, intrinsic metrics, cell labels, and unresolved values | Added material and every mesh coordinate allowed to move in the completed embedding | The whole mesh geometry and adjacent-cell metrics, potentially globally readable | Return zero, one, or many embedded meshes satisfying the growth and equal-cell relation | fits-five | Continuous nonlocal completion is a relational Rule; a particular relaxation solver is separate. |
| F019 `global-equation-relation` | Equation or word relation, coefficients and domain, known variables, and optional witness generator | Integers or finite symbols plus variable, term, and assignment tags | The complete unknown tuple, word witness, or answer slots | All terms, coefficients, chosen indices, and known assignments needed for exact equality | Return every assignment or witness whose two globally constructed sides are exactly equal | fits-five | Zero/one/many global solutions fit a joint Rule; enumeration and nontermination belong to a solver program. |
| F020 `global-score-sequential-placement` | Initial score field or geometry with existing objects, empty support, selection parameters, and any sampling law. | Score or field values plus empty, occupied, object, and geometric records. | Union of every eligible placement locus and every field or support locus that any candidate placement or depletion kernel may change. | Complete current field or geometry, occupancy, eligibility, contact, and scoring inputs. | Score all candidates, choose one maximum or eligible winner deterministically or stochastically, and atomically add it with all induced field changes; return none if no winner exists. | fits-five | Global selection and a coupled one-object write require a nonlocal Neighborhood and structured Frontier, not a sixth field. |
| F021 `hash-index-transform` | Initial table or index, input key or query, hash fold state, collision policy, and result slots. | Key symbols, hash accumulators, bucket or link records, stored items, control markers, and results. | Hash and control slots, result slots, and every bucket, probe, or chain slot that the collision policy could alter. | All input symbols plus every current bucket or chain record reachable by hashing, probing, or exact comparison. | Fold the key, select an address path, resolve collisions by equality, and atomically insert, return a value, or return miss. | fits-five | Dynamic addressing and variable collision chains are readable and writable envelopes; they do not require an address-policy field. |
| F022 `history-dependent-agent-game` | Agent programs, initial joint histories, payoff matrix, score accumulators, and round state. | Action symbols, program and control states, history entries, scores, and round markers. | Both next-action or history-append positions and every score or round accumulator that either outcome may change. | Both complete prior histories, both programs, and the payoff matrix from one shared snapshot. | Run both programs, emit their moves simultaneously, append both histories, and atomically add the corresponding payoffs; stochastic programs return a distribution. | fits-five | Unbounded shared-history reads and coupled multiagent commits fit a nonlocal Neighborhood and distributed Rule. |
| F023 `history-dependent-growth-rewrite` | Occupied support with retained birth or parent provenance, growth rules, and initial round state. | Empty or occupied site records, birth labels, parent references, provenance edges, and round markers. | Every currently eligible growth site plus every provenance record or edge that any admitted birth may create. | Current occupancy and all retained ancestry needed to decide eligibility, including nonlocal provenance queries. | Add all eligible sites and their provenance in one atomic growth-round replacement; return none at a fixed point. | fits-five | History is explicit configuration state, while dynamic support and provenance creation are structural Frontier writes. |
| F024 `indexed-history-recurrence` | A finite initial term prefix, recurrence and index-selection data, and one end or next-index marker. | Numeric terms, indices, unwritten slots, and end-marker or invalid-dependency roles. | The next term slot together with the current and newly advanced end or index marker. | Every retained term addressable by the recurrence, including value-selected and arbitrarily distant indices. | Compute the next indexed term, replace the end marker by the term plus a new marker, or return none for an invalid dependency. | fits-five | Value-dependent unbounded reads require a nonlocal Neighborhood but no history-specific top-level field. |
| F025 `inverse-local-system-reconstruction` | Observed trace or target outputs, boundary and width data, unknown-variable slots, constraints, and initial solver state. | Observed symbols, unknown or assigned variables, equations, branch-stack records, contradiction markers, and solutions. | Every unknown, branch-stack, solver-work, and solution slot that solving or branching may assign, clear, or emit. | The full observed output, current partial assignment, and all modular or light-cone dependency constraints relevant to each branch. | Solve algebraically or branch on partial assignments, prune contradictions, and return zero, one, or many reconstructed assignments. | fits-five | Constraint propagation and branching live in solver-state Alphabet plus relational Rule; no separate solver or update field is forced. |
| F026 `iterated-erasure-process` | The initial ordered population or support, deletion predicate, rank convention, and round state. | Item values, survivor or deleted roles, order or rank metadata, and round markers. | Every current survivor that the round's divisibility or rank predicate could delete, plus round metadata. | The complete ordered survivor set and any divisibility or current-rank data used by the predicate. | Delete the selected subset atomically, preserve unselected survivors in order, and return none when stable or exhausted. | fits-five | Global rank reads and shrinking support are ordinary Neighborhood and structural Frontier semantics. |
| F027 `iterated-map` | Initial scalar or finite tuple with map parameters, guards, and optional terminal condition. | Numeric component values plus optional control, branch, and terminal roles. | The whole current scalar or tuple slot, including every component any branch may replace. | The complete current tuple and all guards, parameters, digits, derivatives, or gradients read by the selected map. | Select the applicable branch and return exactly one atomic image of the tuple, or none on halt or undefined input. | fits-five | Whole-tuple atomic replacement is a typed Frontier result; fast-forward evaluation remains an external close role. |
| F028 `local-factor-weighted-relation` | Candidate or partial configuration, boundary data, local factors, reduction algebra, normalization data, and output slots. | Configuration labels plus factor values, aggregate weights, decisions, and objective or probability results. | Every unknown configuration locus and every weight, decision, or distribution slot that any valid result may fill. | All overlapping factor scopes and any global normalization, comparison, or reduction domain. | Combine local factors under the supplied reduction and return weighted, normalized, feasible, or optimizing frontier assignments as zero, one, many, or a distribution. | fits-five | Global normalization or argmin is a nonlocal read and relational Rule cardinality, not a separate objective or solver field. |
| F029 `local-graph-rewrite` | Initial labeled graph, rewrite patterns and replacements, match schedule, and optional active or age marker. | Node, edge, port, interface, active, and scheduling labels for a variable-cardinality graph. | The union of every selectable matched subgraph, its writable attachment edges, and all nodes or edges any replacement may create. | Each candidate match, its labels and internal structure, its dangling external interface, and schedule metadata. | Choose the permitted match set and atomically replace each match by zero, one, or many interface-preserving subgraphs. | fits-five | Graph identity, dangling interfaces, and variable cardinality require typed graph replacements but no UpdatePolicy. |
| F030 `local-satisfaction-relation` | Boundary or partial assignment, local templates, optional required occurrences, and the unknown configuration region. | Site or node labels plus unknown or assigned roles and optional obligation markers. | The complete unknown region whose labels may vary across satisfying completions. | Every bounded overlapping predicate scope plus any global seed or occurrence obligation. | Return every joint frontier assignment satisfying all local predicates and global obligations, possibly zero, one, or many terminal answers. | fits-five | Joint consistency must be one distributed Rule over the whole Frontier; a concrete solver is not a sixth semantic field. |
| F031 `mobile-head-grid-rewrite` | A fixed grid or tape with default support, exactly one tagged head, its control state, and transition data. | Plain symbols or Head(control-state, underlying-symbol), with any bounded local state carried in the tag. | The head source plus every cell in the bounded write stencil and every possible movement destination. | Head data, the readable local stencil, and all possible destination labels needed to preserve underlying contents. | Choose a transition, atomically rewrite the complete stencil, retag the selected destination, and return none on halt; stochastic choices may form a distribution. | fits-five | Activity is an Alphabet role and destination choice belongs to Rule; complete possible destinations in Frontier eliminate any active-source or update field. |
| F032 `moving-frontier-shell-accretion` | Initial surface and open rim with geometry, orientation, growth rates, clipping data, and target extent. | Surface patches, rim vertices or edges, geometric attributes, and empty or not-yet-created support. | The full current rim plus every new strip element and attachment that this rim step could create or relabel. | Current rim geometry and any accumulated surface or clipping information needed to construct the next strip. | Atomically append the new strip, connect it to the rim, advance rim roles, or return none when growth ends. | fits-five | Continuous geometry and expanding support are carried by configuration types and a structural Frontier replacement, not a geometry axis. |
| F033 `multi-active-local-rewrite` | A lattice or graph state with a finite tagged active set and movement, split, deletion, and collision rules. | Passive local values and active markers carrying state, particle, branch, or stream roles. | The union over all active loci of every source, destination, offspring, collision, and local-write site any outcome may affect. | All active loci's old-snapshot local neighborhoods and destination occupancy needed for collision handling. | Atomically move, split, delete, coalesce, or annihilate active markers and apply local writes; return zero, one, many, or a distribution of replacements. | fits-five | Changing active-set cardinality and collision resolution are distributed Rule results over the complete write envelope. |
| F034 `multiway-rewrite` | One or more initial carrier states with rewrite relations, match semantics, and optional deduplication data. | Carrier symbols, terms, arrays, machine configurations, and identity metadata needed to compare whole states. | The union of every applicable match region and every support locus that any alternative replacement may create or delete. | All match contents, required context, and rule data for every current state being expanded. | Return one successor for each permitted single rewrite, deduplicate where specified, return none when terminal, and repeat independently from every successor. | fits-five | Branching is zero-to-many Rule cardinality over alternative structural replacements, not an update-policy dimension. |
| F035 `mutable-rule-local-automaton` | Initial local configuration together with an explicit finite rule program, mutation policy, and event state. | Cell values, program entries, rule-table records, mutation triggers, and control or terminal markers. | Every evolving cell plus every program entry or program-support slot that any mutation event may add, replace, or clear. | Local cell neighborhoods, the currently selected program entries, and all mutation-trigger state needed by a step. | Jointly compute the next local configuration and zero, one, or many program-table mutations as one atomic replacement. | fits-five | Code is configuration state in Alphabet and program mutation is an ordinary Frontier write; no meta-rule field is required. |
| F036 `nearest-neighbor-retrieval` | Stored metric items, index structure, query, initial incumbent, traversal state, and result slot. | Point coordinates, item payloads, index nodes or links, query and incumbent records, distances, and result roles. | All traversal, incumbent, and result slots that any search path may update; stored points remain read-only. | The query and every stored point or index node reachable for distance comparison, pruning, or descent. | Traverse or descend, update the incumbent, and finally return every globally nearest item and distance, none for an empty store, or several for ties. | fits-five | Nonlocal metric access and a variable search trajectory fit Neighborhood plus explicit search-state writes, without a retrieval-policy field. |
| F037 `ordinary-differential-flow` | Initial continuous time and finite state vector, right-hand side, parameters or driving function, and event or terminal data. | Real or vector components with time, parameter, sample, and optional event or terminal roles. | The complete continuously evolving state vector and any trajectory-sample or event slots the flow may write. | The current vector, explicit time, parameters, driving function, and event predicates read by the derivative relation. | Relate the state to a continuous flow satisfying dx/dt=f(t,x), returning zero, one, or many admissible flow segments until an event or singularity. | fits-five | Continuous time is Rule semantics and run horizon or numerical integration is execution machinery, not a sixth top-level field. |
| F038 `parallel-independent-substitution` | Initial item collection or geometry plus generation phase and production schedule | Item types, phase tags, and finite offspring-block constructors | Disjoint union of every current item and every support position any offspring replacement may create | Each item label together with the readable generation phase and schedule | For each item, map the readable view to zero, one, many, or a distribution over finite offspring structures; commit the complete generation as one coupled replacement | fits-five | Variable-length support belongs to structured Frontier and Rule; synchronous commit needs no UpdatePolicy |
| F040 `parallel-network-rewrite` | Initial labeled graph plus node-type, port, geometry, and threshold data | Node and edge labels, ports, absence markers, and constructible node types | All old graph elements plus every node, edge, and port that any permitted local patch may create, delete, or reroute | Each node's bounded readable connection structure, labels, and local paths | Map local graph views to zero, one, many, or distributed interface-compatible graph patches; resolve overlaps as one graph-level replacement | fits-five | Dynamic topology requires typed graph patches and intensional created support, not a sixth field |
| F041 `partial-differential-relation` | Continuous domain, coefficients, and initial, boundary, or partial field data | Continuous scalar, vector, tensor, or metric field values | The unknown interior or evolving field over the complete spatial or spacetime solution region | Differential germs or stencils plus all readable boundary and constraint dependencies | Return zero, one, or many complete field replacements satisfying the differential relation and side data, or the corresponding distributed law | fits-five | Existence and nonuniqueness are Rule cardinality; solver or integrator choice is not an API field |
| F042 `percolation-connectivity-analysis` | Occupation configuration or occupation law plus domain and boundary convention | Occupied and unoccupied site or edge states | No construction frontier; at most a designated observation-result slot | The global connectivity relation, components, and boundary-to-boundary reachability | Observe spanning or cluster properties without replacing the sampled configuration | close-role | This is a property observer over a completed sample, not a distinct executable transition family |
| F043 `population-evolutionary-search` | Initial population plus fitness, selection, recombination, mutation, and size parameters | Candidate genomes or programs, fitness records, lineage tags, and phase roles | Every slot and auxiliary record that may occur in the complete next-generation population | The whole current population and fitness data, including each readable parent group | Map the population view to one or a distribution over complete selected, recombined, and mutated next-population replacements | fits-five | Global selection and multi-parent coupling fit a nonlocal Neighborhood and structured atomic Frontier |
| F044 `probabilistic-transition-model-fitting` | Observed histories plus model topology, fitting convention, generation request, and random seed | Observed and generated states, probability-table entries, counts, and fit or sample phase tags | Every fitted parameter entry and generated-state slot that either phase may write | Training transition counts and histories during fitting; fitted local context and current state during sampling | Map observations to fitted transition distributions, then map each fitted context to a distributed next-state replacement, with phase encoded in state | fits-five | Fitting and sampling share one phase-tagged state relation; no UpdatePolicy or estimator field is forced |
| F045 `program-randomization-test` | Observed input plus surrogate law, embedded program or statistic, replicate budget, and calibration convention | Data values, surrogate instances, program results, ranks, scores, and phase tags | All surrogate, result, aggregate-score, and final-decision slots that the test may write | The complete observed or surrogate input and the resulting program outputs needed by the global comparison | Distribute over surrogate replacements, evaluate the embedded program, and replace aggregate slots with the calibrated comparison result | fits-five | Nested evaluation and global calibration remain Rule behavior over phase-tagged state |
| F046 `random-functional-graph-construction` | Labeled node set or node count plus successor-sampling law and random seed | Node labels, successor values, and edge-presence states | Every node's successor slot, equivalently the complete envelope of possible outgoing arcs | The complete readable destination-label set together with the source node and its random draw | For each node, distribute over exactly one successor and atomically replace all successor slots to construct the graph | fits-five | One-shot parallel random construction is a distributed Rule, not an update-scheduling field |
| F047 `recursive-function-evaluator` | Requested call plus function definitions, base cases, evaluation strategy, and optional cache | Values, expressions, call frames, continuations, cache entries, and halt or divergence markers | The reducible call or frame plus every subcall, result, continuation, and cache slot its reduction may create or change | The dynamic call tree, arguments, definitions, continuation context, and readable cache | Expand or reduce the selected call to an atomic structural patch; return zero at undefined or terminal states and one or many permitted reductions otherwise | fits-five | Evaluation order is state and Rule data; recursive stack and cache need no independent field |
| F048 `register-machine` | Instruction sequence, initial program counter, and initial integer registers | Nonnegative integers, opcodes, addresses, program-counter values, and halt state | The program counter and every register the current instruction may possibly write | The fetched instruction, branch condition, and all dynamically addressed readable registers | Map the decoded view to one atomic register-and-counter patch, or zero replacements at halt or undefined execution | fits-five | Dynamic addressing is an intensional Frontier and Neighborhood, not a sixth contract axis |
| F049 `sampled-causal-order-network` | Spacetime region, causal metric or order, sampling density, and random seed | Event coordinates, causal-edge presence, and construction-phase tags | Every event slot and every causal edge that sampling or transitive reduction may create or delete | All sampled event pairs plus intervening-event and reachability information needed to test covers | Distribute over event samples, then replace the edge relation with the causal cover graph as one coupled construction | fits-five | Global pairwise comparison and transitive reduction fit a nonlocal Neighborhood and graph-valued Rule |
| F050 `stochastic-local-search` | Initial incumbent plus objective, constraints, proposal law, acceptance convention, and random seed | Candidate components, objective or cache values, locus tags, and acceptance state | Every candidate locus and auxiliary cost field that the sampled single-locus move may write | The whole incumbent and global objective data together with the proposed local change | Distribute over proposals; on rejection return an explicit identity/quiescent successor that advances proposal control, and on acceptance return one atomic incumbent-and-cache patch | fits-five | Rejection continues the search and must not be conflated with termination; proposal randomness and identity continuation remain Rule results. |
| F051 `stored-program-random-access-machine` | Writable program-and-data memory image plus entry counter and machine configuration | Words, bits, opcodes, addresses, program-counter values, device roles, and halt state | The counter, instruction state, and every memory or device location the decoded opcode may possibly write | The fetched opcode and every dynamically addressed operand, memory cell, or device value it reads | Map fetch-decode state to one atomic memory, device, and counter patch, or zero replacements on halt | fits-five | Self-modifying code is ordinary writable state; indirect addressing uses intensional read and write regions |
| F052 `structural-pattern-rewrite` | Initial expression plus ordered patterns, replacements, scan convention, and match constraints | Operator, atom, variable, binder, and match-marker node labels | Every matched subtree plus every node position any permitted replacement forest may create | Each candidate subtree and required structural context, plus the readable expression context used for scan order and nonoverlap | Map the readable structure to zero, one, or many compatible nonoverlapping replacement forests and commit the chosen forest atomically | fits-five | Variable-size trees and match conflicts live in structured Frontier and relational Rule |
| F053 `synchronous-local-state-transform` | Layered fixed-domain input and optional feedback state, boundary data, local rule or template, locus metadata, and empty output layer where one-shot | Finite or continuous local states plus input/output, threshold, template, site, phase, and rule tags | Every output locus and any coupled destination position the shared pass may write | The bounded immutable old-state window plus fixed threshold, template, or phase metadata | Emit one value per locus and commit the complete shared pass atomically; feedback of the output layer yields ordinary automaton evolution | fits-five | Feature extraction and ordered dithering are one-step presets of the same old-snapshot local transform, not new output-defined families. |
| F054 `weighted-history-sum-relation` | Domain, boundary conditions, admissible-history specification, action, measure, and cutoff data | Field or path values, history labels, and complex amplitudes | The amplitude, correlation, or observable output slots produced by the history aggregate | The complete admissible history space and all globally readable action and observable values | Sum or integrate the complex contribution of every admissible history and atomically replace the requested aggregate outputs | fits-five | Extreme nonlocality still fits global Neighborhood; the measure and action are Seed and Rule data |
| F055 `weighted-network-state-update` | Network topology, initial activations and weights, examples or targets, and layer, recurrence, or training phase | Activation values, weights, gradients, unit roles, targets, and phase tags | Every unit, weight, gradient, or auxiliary slot the current inference or learning phase may write | Incoming weighted sources plus any readable recurrent state, target, error, or global criterion | Map the readable network state to one or a distribution over coupled activation and optional weight replacements for the current phase | fits-five | Mutable weights and layer schedules are state and Rule data rather than an UpdatePolicy |
| F056 `priority-dovetailed-oracle-construction` | Monotone shared approximations, enumerated suspended machine runs, diagonal requirements, fair scheduler state, and optional query | Oracle bits, registers, program counters, work/output markers, requirement/restraint roles, row/address tags, and stage control | Every work/output slot advanced this stage, every shared cell that may be enumerated, and every scheduler or requirement slot that may be updated or injured | Selected private machine states, their shared finite approximation, displayed agreements, and priority bookkeeping | Fairly advance selected runs, record outputs, enumerate required diagonal cells, and atomically update or invalidate affected work and requirements | fits-five | Shared nonlocal input, dovetailing, priority, and injury are visible state plus Rule semantics; no scheduler or update field is required. |
| F057 `weighted-prefix-block-transduction` | Input, fixed block partition, weights or prefix tree, tree-building state, and output | Blocks, weights, tree nodes, bits, codewords, and cursor | Tree/preamble, output bits, cursor, and decoded output blocks | Candidate weighted nodes during construction; then current block and tree, or next bits and tree | Combine least-weight nodes, map a block to its leaf word, or parse bits to one leaf | fits-five | Tree construction and block emission are visible phases of one closed Rule, not a codec policy field. |
| F058 `nested-interval-symbol-transduction` | Input, probability model, interval `[0,1]`, precision state, and cursor | Symbols, probabilities, exact or finite endpoints, digits, and cursor | Current interval, final tag, cursor, and decoded-symbol slots | Next symbol, current interval, and cumulative partition | Replace the interval by the selected subinterval, finalize a tag, or invert refinements | fits-five | One message-wide interval is ordinary structured writable state. |
| F059 `history-reference-record-transduction` | Input, cursor, consumed-prefix or dictionary state, match policy, and record grammar | Symbols or regions, literals, pointer tags, offsets, lengths, dictionary entries, and cursor | Record stream, cursor, dictionary, and reconstructed output | Remaining input plus eligible prior matches or dictionary entries | Select a literal or reference, append it, advance, update history state, or copy from reconstructed history | fits-five | History-dependent reads and variable records fit a nonlocal Neighborhood and structured replacement. |
| F060 `recursive-uniform-region-decomposition` | Array, root region, pending work/tree, split geometry, tolerance, and cutoff | Samples, bounds, leaf/split tags, tree nodes, and work entries | Current node and every possible child; inverse mode writes its output region | All samples in the current region plus split and uniformity data | Make a leaf or create child regions; inverse mode fills a leaf region | fits-five | Dynamic hierarchical support is carried by Frontier and Rule, not a tree-update component. |
| F061 `orthogonal-basis-coefficient-transform` | Numeric block, basis operator, coefficient ordering, retention or quantization policy, and inverse data | Exact or quantized samples, coefficients, basis indices, and selection tags | Coefficient vector and optional reconstructed block | Complete input block, basis operator, and coefficient-selection data | Project globally, select or quantize coefficients, and optionally invert as one replacement | fits-five | A global linear read still fits Neighborhood; lossy output cardinality adds no field. |
| F062 `predictive-residual-transduction` | Samples, initial history, predictor order/window/objective, model state, residual code, and cursor | Samples, coefficients, residuals, code indices, history, and cursor | Model state, residual stream, reconstruction, and cursor | Current sample, retained preceding samples, and current or fitted coefficients | Fit or update the predictor, emit residual, reconstruct if requested, and advance | fits-five | Causal history and model fitting are visible state and Rule semantics. |
| F063 `aligned-xor-stream-transduction` | Input stream, supplied keystream or generator seed/state, alignment policy, and cursor | Bits, generator state, phase, and cursor tags | Output bit plus cursor and generator state, or the whole output in one-shot form | Next input bit, aligned keystream bit, and generator state when online | XOR aligned bits and advance or generate; applying the same transform decrypts | fits-five | Pointwise involution and online generator state require no output or encryption component. |

## Cross-Cutting Pressure Results

| Pressure case | Five-part representation | Outcome |
|---|---|---|
| Dynamic or growing support | Seed produces the typed support; Frontier may name fresh components; Rule returns structural replacement | Contract generalization only |
| Mobile source plus destination writes | Frontier contains every possible writable source/destination; tags identify the active source; Rule returns the coupled replacement | No firing-frontier split |
| Asynchronous or scheduled action | Visible schedule/phase is configuration data; Rule chooses and commits the scheduled replacement | No scheduler field |
| Multi-target and variable-size writes | Rule returns one complete region replacement rather than one scalar per coordinate | No `UpdatePolicy` |
| Multiway evolution | Rule returns one replacement per applicable rewrite with derivation witnesses | No multiway executor |
| Constraint satisfaction | Seed supplies known/partial data; Neighborhood exposes dependencies; Frontier is the unknown region; Rule denotes all satisfying completions | Same API, relational rule |
| Uniterated function | Input is seeded, output is writable, and Rule returns the function value once; feedback is an explicit preset when iteration is desired | No trajectory flag |
| General PDE relation | Boundary/initial data are seeded/readable; the unknown field is writable; Rule denotes all compatible fields | Same API, intensional relation |
| Continuous flow or event dynamics | Configuration holds continuous state; Neighborhood exposes state/geometry; Rule denotes a flow segment or next event replacement | No time component |
| Stochastic construction | Seed or Rule denotes a probability law; sampling consumes explicit replayable run entropy | No hidden RNG or RNG field |
| Termination, failure, or divergence | Rule result has typed outcome and zero successors where appropriate | No result-policy field |
| Mutable rules or stored programs | Program text is tagged writable configuration data interpreted by a closed outer Rule | No mutable API object |
| Analysis, rendering, or encoding wrapper | Keep as observer/tool when it does not change source transition mechanics; make it an ordinary program only when it has its own state transition | No observer field |

## Required Contract Generalizations

These are genuine implementation obligations, but none is a new top-level
primitive:

1. Replace fixed finite `Z4` configurations with typed structural carriers that
   can represent discrete, continuous, graph, word, tree, product, and
   intensional supports.
2. Let `Seed` produce exact configurations, constructors, partial
   configurations, and probability laws while keeping entropy explicit.
3. Let writable and readable regions be structured, dynamic, nonlocal,
   continuous, or intensional rather than only finite coordinate sets.
4. Change `Rule` from a scalar per-coordinate function to a closed relation
   returning complete frontier replacements, typed outcomes, derivation
   witnesses, and—where needed—probability measures or symbolic solution sets.
5. Make atomic preserve-outside commit a universal engine invariant. The engine
   must not contain catalog-family dispatch.
6. Preserve exact values, structural codecs, provenance, result cardinality,
   terminal reasons, and replayable stochastic choices.

## Rejected Top-Level Extensions

The taxonomy does not justify public `Domain`, `Shape`, `Boundary`,
`ConfigurationSchema`, `ActiveSelector`, `Scheduler`, `UpdatePolicy`,
`ResultPolicy`, `Solver`, `Observer`, `Trajectory`, `Time`, or `RandomGenerator`
fields. Each is respectively configuration data, rule data, run configuration,
tooling, or universal engine semantics. A future concrete counterexample may
reopen this, but naming convenience is not evidence.

## Relationship to `simple_programs.md`

The existing document gets two central ideas right: `FRONTIER` denotes
writable coordinates, and writes use one old snapshot with atomic
preserve-outside commit. It becomes too narrow where it requires:

- `DOMAIN`, `SHAPE`, and `BOUNDARY` as independent axes;
- a `0–3D` spatial model embedded in `Z4`;
- finite coordinate universes for frontier and neighborhood selection;
- a scalar next value for every frontier coordinate;
- parallel evaluation of every frontier coordinate; and
- exactly one discrete next-state slice.

The remaster should preserve its algebraic clarity while replacing those
representation restrictions with the contracts above.

## Goal 2 Consequences

Goal 2 must not be implemented from its frozen handoff as written. Its public
`UPDATE` axis and separate declarative relation/function/PDE category conflict
with the five-part result.

The remaster should:

- use only `Seed`, `Alphabet`, `Frontier`, `Neighborhood`, and `Rule` in the
  program specification;
- make constraint, function, and PDE relations ordinary relational rules;
- make one generic engine apply complete replacements atomically;
- represent semantic construction names as preset constructors returning
  ordinary `SimpleProgram` values;
- keep solvers, evaluators, finite realizations, observers, and renderers
  outside the program component list; and
- retain Goal 2's useful work on closed structural descriptors, versioned
  codecs, exact arithmetic, typed results and witnesses, lossless
  representation maps, provenance, and branch-free execution.

The 60 semantic families are an implementation coverage inventory, not a demand
for 60 public classes.
