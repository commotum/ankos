"""Literal Goal 6/7 expectations for the CT11 catalog-expansion gate.

This module deliberately imports no production ``ca`` module.  The rows are a
compact transcription of ``goal-6/catalog-migration.md`` and the reconciled
inventory in ``goal-7/5-CATALOG.md``.  Runtime catalog metadata is always the
subject under test, never the source of these expectations.
"""

from __future__ import annotations


def _tab_rows(data: str, width: int) -> tuple[tuple[str, ...], ...]:
    rows = tuple(
        tuple(line.split("\t"))
        for line in data.strip().splitlines()
        if line.strip()
    )
    if any(len(row) != width for row in rows):
        raise AssertionError("malformed literal CT11 manifest row")
    return rows


CANONICAL_ROWS = _tab_rows(
    """
SPF001	F001	alternating-partition-local-evolution	automata	addition	seed;partition;block_law;boundary;phase	CH08:L155-165;N08:L107,L124-126;CH09:L303-321
SPF002	F002	append-only-sequence-generation	substitua	covered	seed;emitter;control_schema;support	BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L203-210,L569-599
SPF003	F003	asynchronous-local-state-automaton	automata	addition	seed;local_law;schedule;boundary	N09:L407-443
SPF004	F004	event-provenance-causal-network	media	addition	event_trace;read_sets;initial_provenance	CH09:L655-707;N09:L347-355,L378-384
SPF005	F005	context-dependent-substitution	substitua	covered	seed;productions;context_shape;boundary	CH03:L333-337
SPF006	F006	continuous-event-dynamics	dynamica	addition	seed;geometry;flow_law;reset_law;terminal_condition	BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L60-61
SPF007	F007	coupled-field-mobile-locus-evolution	automata	addition	seed;field_law;mobile_law;boundary	CH08:L131-138
SPF008	F008	digit-emitting-register-transduction	media	covered	seed;register_law;base;digit_projection	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L303-308,L343-350
SPF009	F009	driven-relaxation	automata	addition	seed;drive_law;toppling_law;boundary;relaxation_form	BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L665-676
SPF010	F011	enumerative-semidecision	machina	addition	query;enumeration;predicate;start	CH10:L975-989;N10:L5-15;N11:L829-855
SPF011	F012	error-diffusion-transform	media	addition	input;palette;diffusion_kernel;scan	N10:L348-360
SPF012	F013	maximal-run-record-transduction	media	addition	input;record_grammar;direction;scan;feedback	CH10:L163-187;N10:L83-85,L171-175;N04:L193-202
SPF013	F014	finite-gate-circuit	machina	addition	inputs;wiring;gates;schedule;measurement	N10:L904;N12:L331-347,L560-574
SPF014	F015	finite-model-satisfaction	criteria	addition	axioms;finite_domain;signatures;fixed_tables	CH12:L1073-1095;N12:L1189-1203,L1245-1257
SPF015	F016	first-passage-aggregation	substitua	addition	seed;walk_law;contact;release;boundary;target	N08:L50;BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L359-360
SPF016	F017	front-delete-rear-append-system	substitua	covered	seed;deletion_width;productions;phase_cycle	CH03:L423-445,L447-471
SPF017	F018	geometric-embedding-relation	criteria	addition	mesh;growth;metric_constraints;boundary_embedding	CH08:L563-569;N08:L226
SPF018	F019	global-equation-relation	criteria	addition	equation;domain;known_assignments;witness_schema	CH12:L885-905;N12:L901-966
SPF019	F020	global-score-sequential-placement	substitua	addition	seed;score_expression;placement_shape;depletion_kernel;tie_law	CH08:L531-547;N08:L223-225
SPF020	F021	hash-index-transform	media	addition	key;table;hash_fold;collision;operation	CH10:L829-839;N10:L976-980
SPF021	F022	history-dependent-agent-game	automata	addition	agents;histories;payoff;action_schema;round_control	N10:L1081-1085
SPF022	F023	history-dependent-growth-rewrite	substitua	addition	seed;eligibility;provenance_law;boundary	BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md:L130-151
SPF023	F024	indexed-history-recurrence	substitua	covered	prefix;recurrence;index_law;invalidity	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L169-186
SPF024	F025	inverse-local-system-reconstruction	criteria	addition	observations;local_law;boundary;unknown_schema;search_order	CH10:L575-633;N10:L531-544,L608-624
SPF025	F026	iterated-erasure-process	substitua	covered	seed;erasure_predicate;rank_convention	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L211-214
SPF026	F027	iterated-map	automata	covered	seed;map_expression;guards;terminal_condition	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L53-54,L111-118,L472-491
SPF027	F028	local-factor-weighted-relation	criteria	addition	seed;factors;reduction;normalization;objective	N10:L493-494
SPF028	F029	local-graph-rewrite	substitua	addition	seed;patterns;replacements;match_schedule;interface_schema	CH09:L901-965;N09:L495-528,L552-556,L594-600
SPF029	F030	local-satisfaction-relation	criteria	covered	partial_assignment;templates;boundary;obligations	CH09:L595-615;N09:L324-330
SPF030	F031	mobile-head-grid-rewrite	machina	covered	tape;transitions;head;stencil;boundary	CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L127-131
SPF031	F032	moving-frontier-shell-accretion	substitua	addition	seed;strip_constructor;rim_law;geometry;terminal_condition	CH08:L581-591;N08:L234-246
SPF032	F033	multi-active-local-rewrite	automata	covered	seed;local_law;collision_law;schedule	CH03:L231-247
SPF033	F034	multiway-rewrite	substitua	covered	seed;rewrites;match_semantics;quotient	CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L355-369
SPF034	F035	mutable-rule-local-automaton	automata	addition	seed;rule_program;interpreter;mutation_law	CH08:L319-329
SPF035	F036	nearest-neighbor-retrieval	machina	addition	items;query;metric;index;traversal	N10:L988-996
SPF036	F037	ordinary-differential-flow	dynamica	addition	seed;rhs;parameters;duration_or_event	BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L901-902,L953-980
SPF037	F038	parallel-independent-substitution	substitua	covered	seed;productions;schedule;geometry	CH03:L299-307,L343-363
SPF038	F040	parallel-network-rewrite	substitua	covered	seed;patches;port_schema;overlap_law	CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L241,L287-331
SPF039	F041	partial-differential-relation	dynamica	covered	domain;coefficients;differential_relation;side_data	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L625-674;N08:L84-105,L322-328
SPF040	F043	population-evolutionary-search	automata	addition	population;fitness_expression;selection;recombination;mutation;size	BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:L556-560
SPF041	F044	probabilistic-transition-model-fitting	media	addition	observations;topology;estimator;generation_law;generation_request	CH10:L441-459;N10:L495-501
SPF042	F045	program-randomization-test	criteria	addition	observed;surrogate_law;program;statistic;replicates;calibration	CH10:L515-533
SPF043	F046	random-functional-graph-construction	substitua	addition	nodes;successor_measure	BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md:L589-590
SPF044	F047	recursive-function-evaluator	machina	covered	call;definitions;evaluation_order;cache	BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L237-268,L316-364
SPF045	F048	register-machine	machina	covered	program;registers;entry	CH03:L473-509,L519-525
SPF046	F049	sampled-causal-order-network	media	addition	region;causal_order;density;event_measure	N09:L816-818
SPF047	F050	stochastic-local-search	criteria	addition	incumbent;objective;constraints;proposal;acceptance	CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L553-596
SPF048	F051	stored-program-random-access-machine	machina	addition	memory;entry;instruction_set	N11:L15-23
SPF049	F052	structural-pattern-rewrite	substitua	covered	expression;patterns;replacements;scan;nonoverlap	CH03:L531-537;N03:L823-835;CH10:L909-915
SPF050	F053	synchronous-local-state-transform	automata	covered	seed;stencil;local_law;boundary;feedback	CH10:L323-347;N10:L328-347;N03:L135-150,L190,L192-225
SPF051	F054	weighted-history-sum-relation	criteria	addition	domain;side_data;histories;action;measure;observables	N09:L880,L955-957
SPF052	F055	weighted-network-state-update	automata	covered	network;seed;weights;schedule;learning_law	N10:L1021-1023
SPF053	F056	priority-dovetailed-oracle-construction	machina	addition	approximations;machines;requirements;priority;fair_schedule	N12:L80-92
SPF054	F057	weighted-prefix-block-transduction	media	addition	input;block_partition;weights_or_tree;direction	CH10:L189-205,L235-249;N10:L87-106
SPF055	F058	nested-interval-symbol-transduction	media	addition	input;probability_model;precision;direction	N10:L108-121
SPF056	F059	history-reference-record-transduction	media	addition	input;match_policy;dictionary;record_grammar;direction	CH10:L209-267;N10:L123-153
SPF057	F060	recursive-uniform-region-decomposition	media	addition	input;root_region;split;uniformity;cutoff;direction	CH10:L233-239,L269-279;N10:L154-168
SPF058	F061	orthogonal-basis-coefficient-transform	media	addition	input;basis;ordering;retention;quantization;direction	CH10:L281-305;N10:L181-288
SPF059	F062	predictive-residual-transduction	media	addition	input;predictor;history;fitting;residual_code;direction	N10:L424
SPF060	F063	aligned-xor-stream-transduction	media	addition	input;keystream;alignment;generator	CH10:L539-565,L599-605
""",
    7,
)


CANONICAL_NAME_RELATIONS = {
    "SPF002": ("T40 split branch", "P constant_digit_sequence"),
    "SPF005": ("neighbor_dependent_substitution", "T28 2-D preset"),
    "SPF008": ("T40 split branch", "P constant_digit_register"),
    "SPF012": (
        "P look_and_say feedback preset",
        "flat export",
        "preset source N04:L193-202",
    ),
    "SPF016": ("tag_system", "T18 cyclic_tag_system preset"),
    "SPF023": ("T38 variable-index preset",),
    "SPF025": ("number_theoretic_filtering preset",),
    "SPF026": (
        "T34 arithmetic, T35 piecewise, and T36 digit-reversal presets",
    ),
    "SPF029": ("T31", "T32 template name", "T33 seeded-template preset"),
    "SPF030": (
        "turing_machine",
        "T09 mobile, T10 repaired neighbor-updating, T25 2-D presets",
    ),
    "SPF032": ("generalized_mobile_automaton preset",),
    "SPF033": ("multiway_system true alias",),
    "SPF037": (
        "T15 merge",
        "T26/T27/T42 presets",
        "neighbor_independent_substitution",
    ),
    "SPF038": ("network_rewrite", "broad network_system is not exported"),
    "SPF039": ("T45 canonical constructor", "pde true alias"),
    "SPF044": (
        "Repaired T41",
        "function_combination_system retained only as deprecated metadata",
    ),
    "SPF045": ("register_machine",),
    "SPF046": ("Distinct from F004 producer-history transform",),
    "SPF049": ("symbolic_system", "T16 sequential-substitution preset"),
    "SPF050": (
        "eca, elementary_cellular_automaton",
        "T02–T07, T21–T24 presets",
        "T44 family-level alias implemented as a preset",
    ),
    "SPF052": (
        "Normalizes C045 legacy coverage",
        "no T01–T45 owner",
        "never alias network_system",
    ),
}


LEGACY_ROWS = _tab_rows(
    """
T01	Elementary Cellular Automata	retain-family	C090	CH03:L29-56
T02	Multi-Color Nearest-Neighbor Cellular Automata	retain-preset	C090	N03:L135-150
T03	Totalistic Cellular Automata	retain-preset	C090	CH03:L91-96
T04	Three-Color Totalistic Cellular Automata	retain-preset	C090	CH03:L89-96,L109-110
T05	Higher-Color Totalistic Cellular Automata	merge	C090	N03:L164-185
T06	Quiescent-Background-Preserving Cellular Automata	retain-preset	C090	Goal 2-preserved T(b,…,b)=b;CH03:L101,L649;CH06:L101;goal-1/25-T06-QUIESCENT.md
T07	Left-Right Symmetric Cellular Automata	retain-preset	C090	N03:L7-10;N05:L89-100
T08	Initial-Condition Classes	retire-role		Goal 5 Seed-role decision;no executable construction source
T09	Mobile Automata	retain-preset	C047	CH03:L169-185
T10	Extended Mobile Automata	repair	C056	CH03:L197-207
T11	Generalized Mobile Automata	retain-family	C030	CH03:L231-247
T12	Turing Machines	retain-family	C049	N03:L294-333
T13	Neighbor-Independent Substitution Systems	retain-family	C061	CH03:L299-307
T14	Neighbor-Dependent Substitution Systems	retain-family	C011,C055	CH03:L333-337;CH05:L211-227;N05:L360-367
T15	Creation-Destruction Substitution Systems	merge	C061	CH03:L343-363
T16	Sequential Substitution Systems	retain-preset	C080	CH03:L369-379
T17	Tag Systems	retain-family	C091	CH03:L423-445
T18	Cyclic Tag Systems	retain-preset	C091	CH03:L447-471
T19	Register Machines	retain-family	C073	CH03:L473-509,L519-525
T20	Symbolic Systems	retain-family	C089	CH03:L531-537;N03:L823-835;CH10:L909-915
T21	Two-Dimensional Cellular Automata	retain-preset	C090	CH05:L27-34
T22	Moore-Neighborhood Cellular Automata	retain-preset	C090	CH05:L67-86
T23	Three-Dimensional Cellular Automata	retain-preset	C090	CH05:L95-123;N06:L55-66
T24	Higher-Dimensional Lattice Cellular Automata	retain-preset	C090	N05:L36-58,L66-88
T25	Two-Dimensional Turing Machines	retain-preset	C049	CH05:L127-131;N05:L211-217
T26	Two-Dimensional Substitution Systems	retain-preset	C061	CH05:L173-190
T27	Geometric Replacement And Fractal Systems	repair	C061	CH05:L191-214;N05:L286-337
T28	Neighbor-Dependent Two-Dimensional Substitution Systems	retain-preset	C055	CH05:L211-227;N05:L360-367
T29	Network Systems	retain-family	C062	CH05:L239-248,L287-331
T30	Multiway Systems	retain-family	C051	CH05:L355-369;N05:L527-528,L549-578
T31	Local Constraint Systems	retain-family	C043	CH05:L433-479;CH09:L595-615;N09:L324-330
T32	Template Constraint Systems	alias	C043	CH05:L475-488
T33	Seeded Template Constraint Systems	retain-preset	C042,C043	CH05:L475-498,L535-536
T34	Arithmetic Iteration Systems	retain-preset	C037	CH04:L53-54
T35	Piecewise Integer Maps	retain-preset	C037	CH04:L111-118
T36	Digit-Reversal Arithmetic Systems	retain-preset	C037	CH04:L153-162;N04:L170-179
T37	Recursive Sequences	retain-family	C078	CH04:L169-186
T38	Variable-Index Recursive Sequences	retain-preset	C078	CH04:L179-186
T39	Number-Theoretic Filtering Systems	retain-family	C035	CH04:L211-214;N04:L418-430
T40	Mathematical-Constant Digit Systems	split	C003,C017	sequence N04:L203-210,L569-599;register CH04:L303-308,L343-350;N04:L561-562
T41	Function-Combination Systems	repair	C072	N04:L237-268,L316-364
T42	Continued-Fraction-Driven Substitution Systems	retain-preset	C061	CH04:L454-461;N04:L753-754
T43	Iterated Maps	retain-family	C037	CH04:L53-54,L111-118,L472-491
T44	Continuous Cellular Automata	alias	C090	CH04:L546-562,L565-616
T45	Partial Differential Equation Systems	retain-family	C063	CH04:L625-674;N04:L933-940
""",
    5,
)


LEGACY_TARGET_ROWS = _tab_rows(
    """
T01	-	SPF050	eca	P	CH03:L29-56
T02	-	SPF050	multicolor_cellular_automaton	P	N03:L135-150
T03	-	SPF050	totalistic_cellular_automaton	P	CH03:L91-96
T04	-	SPF050	three_color_totalistic_cellular_automaton	P	CH03:L89-96,L109-110
T05	-	SPF050	higher_color_totalistic_cellular_automaton	P	N03:L164-185
T06	-	SPF050	quiescent_cellular_automaton	P	Goal 2-preserved T(b,…,b)=b;CH03:L101,L649;CH06:L101;goal-1/25-T06-QUIESCENT.md
T07	-	SPF050	symmetric_cellular_automaton	P	N03:L7-10;N05:L89-100
T09	-	SPF030	mobile_automaton	P	CH03:L169-185
T10	-	SPF030	neighbor_updating_mobile_automaton	P	CH03:L197-207
T11	-	SPF032	generalized_mobile_automaton	P	CH03:L231-247
T12	-	SPF030	turing_machine	P	N03:L294-333
T13	-	SPF037	neighbor_independent_substitution	P	CH03:L299-307
T14	-	SPF005	neighbor_dependent_substitution	P	CH03:L333-337;CH05:L211-227;N05:L360-367
T15	-	SPF037	creation_destruction_substitution	P	CH03:L343-363
T16	-	SPF049	sequential_substitution	P	CH03:L369-379
T17	-	SPF016	tag_system	P	CH03:L423-445
T18	-	SPF016	cyclic_tag_system	P	CH03:L447-471
T19	-	SPF045	register_machine	C	CH03:L473-509,L519-525
T20	-	SPF049	symbolic_system	P	CH03:L531-537;N03:L823-835;CH10:L909-915
T21	-	SPF050	cellular_automaton_2d	P	CH05:L27-34
T22	-	SPF050	moore_cellular_automaton	P	CH05:L67-86
T23	-	SPF050	cellular_automaton_3d	P	CH05:L95-123;N06:L55-66
T24	-	SPF050	lattice_cellular_automaton	P	N05:L36-58,L66-88
T25	-	SPF030	turing_machine_2d	P	CH05:L127-131;N05:L211-217
T26	-	SPF037	substitution_system_2d	P	CH05:L173-190
T27	-	SPF037	geometric_substitution	P	CH05:L191-214;N05:L286-337
T28	-	SPF005	context_dependent_substitution_2d	P	CH05:L211-227;N05:L360-367
T29	-	SPF038	parallel_network_rewrite	C	CH05:L239-248,L287-331
T30	-	SPF033	multiway_system	A	CH05:L355-369;N05:L527-528,L549-578
T31	-	SPF029	local_constraint_system	P	CH05:L433-479;CH09:L595-615;N09:L324-330
T32	-	SPF029	template_constraint_system	P	CH05:L475-488
T33	-	SPF029	seeded_template_constraint_system	P	CH05:L475-498,L535-536
T34	-	SPF026	arithmetic_iteration	P	CH04:L53-54
T35	-	SPF026	piecewise_integer_map	P	CH04:L111-118
T36	-	SPF026	digit_reversal_map	P	CH04:L153-162;N04:L170-179
T37	-	SPF023	recursive_sequence	P	CH04:L169-186
T38	-	SPF023	variable_index_recursive_sequence	P	CH04:L179-186
T39	-	SPF025	number_theoretic_filtering	P	CH04:L211-214;N04:L418-430
T40	sequence	SPF002	constant_digit_sequence	P	N04:L203-210,L569-599
T40	register	SPF008	constant_digit_register	P	CH04:L303-308,L343-350;N04:L561-562
T41	-	SPF044	recursive_function_evaluator	C	N04:L237-268,L316-364
T42	-	SPF037	continued_fraction_substitution	P	CH04:L454-461;N04:L753-754
T43	-	SPF026	iterated_map	C	CH04:L53-54,L111-118,L472-491
T44	-	SPF050	continuous_cellular_automaton	P	CH04:L546-562,L565-616
T45	-	SPF039	partial_differential_relation	C	CH04:L625-674;N04:L933-940
""",
    6,
)


LEGACY_CALLABLE_ROWS = _tab_rows(
    """
iterated_map	automata	C	SPF026	ca.catalog.automata.iterated_map	1	T43	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L53-54,L111-118,L472-491
parallel_network_rewrite	substitua	C	SPF038	ca.catalog.substitua.parallel_network_rewrite	1	T29	CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L241,L287-331
partial_differential_relation	dynamica	C	SPF039	ca.catalog.dynamica.partial_differential_relation	1	T45	CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L625-674;N08:L84-105,L322-328
recursive_function_evaluator	machina	C	SPF044	ca.catalog.machina.recursive_function_evaluator	1	T41	BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:L237-268,L316-364
register_machine	machina	C	SPF045	ca.catalog.machina.register_machine	1	T19	CH03:L473-509,L519-525
eca	automata	P	SPF050	Bind binary 1-D radius-one synchronous feedback; family constructor remains synchronous_local_state_transform.	1	T01	CH03:L29-56
elementary_cellular_automaton	automata	A	SPF050	ca.catalog.automata.eca	1	T01	CH03:L29-56
multicolor_cellular_automaton	automata	P	SPF050	Bind finite palette, nearest-neighbor stencil, and feedback.	1	T02	N03:L135-150
totalistic_cellular_automaton	automata	P	SPF050	Bind totalistic quotient Rule.	1	T03	CH03:L91-96
three_color_totalistic_cellular_automaton	automata	P	SPF050	Bind T03 to three colors and radius one.	1	T04	CH03:L89-96,L109-110
higher_color_totalistic_cellular_automaton	automata	P	SPF050	T03 parameterization with colors >= 4; no family entry.	1	T05	N03:L164-185
quiescent_cellular_automaton	automata	P	SPF050	Validate the quiescent-background Rule restriction; no executor change.	1	T06	Goal 2-preserved T(b,…,b)=b;CH03:L101,L649;CH06:L101;goal-1/25-T06-QUIESCENT.md
symmetric_cellular_automaton	automata	P	SPF050	Validate reflection-invariant local Rule data.	1	T07	N03:L7-10;N05:L89-100
mobile_automaton	machina	P	SPF030	Bind the single tagged-head, center-write profile.	1	T09	CH03:L169-185
neighbor_updating_mobile_automaton	machina	P	SPF030	Correctly bind the neighbor-updating fixed-block result; deprecated old name delegates losslessly.	1	T10	CH03:L197-207
extended_mobile_automaton	machina	K	SPF030	ca.catalog.machina.neighbor_updating_mobile_automaton	0	T10	CH03:L197-207
generalized_mobile_automaton	automata	P	SPF032	Bind multi-active move/split/delete mechanics; do not route through the single-head family.	1	T11	CH03:L231-247
turing_machine	machina	P	SPF030	Bind tagged control state, symbol write, and edge movement.	1	T12	N03:L294-333
neighbor_independent_substitution	substitua	P	SPF037	Bind independent string items and generation concatenation.	1	T13	CH03:L299-307
neighbor_dependent_substitution	substitua	P	SPF005	Bind contextual word neighborhoods.	1	T14	CH03:L333-337;CH05:L211-227;N05:L360-367
creation_destruction_substitution	substitua	P	SPF037	Bind empty/nonempty offspring data; no separate family or commit law.	1	T15	CH03:L343-363
sequential_substitution	substitua	P	SPF049	Bind flat string structure, ordered scan, and one nonoverlapping splice.	1	T16	CH03:L369-379
tag_system	substitua	P	SPF016	Bind fixed front deletion and rear production.	1	T17	CH03:L423-445
cyclic_tag_system	substitua	P	SPF016	Add visible cyclic production phase.	1	T18	CH03:L447-471
symbolic_system	substitua	P	SPF049	Bind expression-tree patterns, templates, and scan semantics.	1	T20	CH03:L531-537;N03:L823-835;CH10:L909-915
cellular_automaton_2d	automata	P	SPF050	Bind square support and 2-D local stencil.	1	T21	CH05:L27-34
moore_cellular_automaton	automata	P	SPF050	Bind the 2-D Moore stencil.	1	T22	CH05:L67-86
cellular_automaton_3d	automata	P	SPF050	Bind cubic support and 3-D stencil.	1	T23	CH05:L95-123;N06:L55-66
lattice_cellular_automaton	automata	P	SPF050	Bind dimension/incidence/stencil descriptors.	1	T24	N05:L36-58,L66-88
turing_machine_2d	machina	P	SPF030	Bind planar topology, headings, and movement ports.	1	T25	CH05:L127-131;N05:L211-217
substitution_system_2d	substitua	P	SPF037	Bind compatible 2-D offspring geometry.	1	T26	CH05:L173-190
geometric_substitution	substitua	P	SPF037	Construction is posed geometric substitution; fractal remains output/property metadata.	1	T27	CH05:L191-214;N05:L286-337
context_dependent_substitution_2d	substitua	P	SPF005	Bind 2-D contextual patterns and compatible mosaic commit.	1	T28	CH05:L211-227;N05:L360-367
network_rewrite	substitua	A	SPF038	ca.catalog.substitua.parallel_network_rewrite	1	T29	CH05:L239-248,L287-331
multiway_system	substitua	A	SPF033	ca.catalog.substitua.multiway_rewrite	1	T30	CH05:L355-369;N05:L527-528,L549-578
local_constraint_system	criteria	P	SPF029	Bind local predicates over an unknown completion region.	1	T31	CH05:L433-479;CH09:L595-615;N09:L324-330
template_constraint_system	criteria	P	SPF029	Bind allowed-template representation; not a zero-delta callable alias.	1	T32	CH05:L475-488
seeded_template_constraint_system	criteria	P	SPF029	Put fixed/required occurrences in Seed and obligations.	1	T33	CH05:L475-498,L535-536
arithmetic_iteration	automata	P	SPF026	Bind an exact arithmetic map expression.	1	T34	CH04:L53-54
piecewise_integer_map	automata	P	SPF026	Bind integer domain and guarded/residue clauses.	1	T35	CH04:L111-118
digit_reversal_map	automata	P	SPF026	Bind positional representation and reversal map.	1	T36	CH04:L153-162;N04:L170-179
recursive_sequence	substitua	P	SPF023	Bind fixed-index recurrence and append state.	1	T37	CH04:L169-186
variable_index_recursive_sequence	substitua	P	SPF023	Bind value-selected history addresses.	1	T38	CH04:L179-186
number_theoretic_filtering	substitua	P	SPF025	Bind divisibility/current-rank erasure criteria.	1	T39	CH04:L211-214;N04:L418-430
constant_digit_sequence	substitua	P	SPF002	No umbrella callable or kind dispatch; each explicit branch callable has exactly one SPF target.	1	T40	N04:L203-210,L569-599
constant_digit_register	media	P	SPF008	No umbrella callable or kind dispatch; each explicit branch callable has exactly one SPF target.	1	T40	CH04:L303-308,L343-350;N04:L561-562
continued_fraction_substitution	substitua	P	SPF037	Bind a finite visible production schedule obtained from verified continued-fraction data.	1	T42	CH04:L454-461;N04:L753-754
continuous_cellular_automaton	automata	P	SPF050	Bind continuous-valued Alphabet/local law but remain discrete-time F053; not F041.	1	T44	CH04:L546-562,L565-616
pde	dynamica	A	SPF039	ca.catalog.dynamica.partial_differential_relation	1	T45	CH04:L625-674;N04:L933-940
""",
    8,
)


EXPECTED_HOME_COUNTS = {
    "automata": 11,
    "substitua": 15,
    "machina": 8,
    "media": 14,
    "criteria": 9,
    "dynamica": 3,
}
EXPECTED_COVERAGE_COUNTS = {"covered": 19, "addition": 41}
EXPECTED_NAME_KIND_COUNTS = {"C": 60, "P": 40, "A": 4, "K": 1}
METADATA_ONLY_SPELLINGS = (
    "fractal_system",
    "network_system",
    "function_combination_system",
)


__all__ = (
    "CANONICAL_NAME_RELATIONS",
    "CANONICAL_ROWS",
    "EXPECTED_COVERAGE_COUNTS",
    "EXPECTED_HOME_COUNTS",
    "EXPECTED_NAME_KIND_COUNTS",
    "LEGACY_CALLABLE_ROWS",
    "LEGACY_ROWS",
    "LEGACY_TARGET_ROWS",
    "METADATA_ONLY_SPELLINGS",
)
