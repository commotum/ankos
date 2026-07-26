"""Callable-free metadata shells for the audited simple-program catalog.

This module owns immutable records for canonical family identity, close roles,
legacy migration, and public-name relations.  It does not own constructors,
component values, program values, registries, lookup dispatch, or execution.
The six category modules build programs without importing this module;
``ca.catalog`` is the sole eventual join between metadata and callables.

The family and close-role values below are the literal, callable-free
catalog projection of ``goal-6/catalog-migration.md``.  ``closed_parameters``
retains the semantic construction inventory from that authority; it does not
define the Python signature of the canonical five-component constructors.
Legacy and public-name relations use the same inert record discipline below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias


CatalogHome: TypeAlias = Literal[
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
]
Coverage: TypeAlias = Literal["covered", "addition"]
RoleKind: TypeAlias = Literal["interface", "observer"]
LegacyDisposition: TypeAlias = Literal[
    "retain-family",
    "retain-preset",
    "merge",
    "repair",
    "alias",
    "retire-role",
    "split",
]
CallableTreatment: TypeAlias = Literal["C", "P", "A", "K", "M"]
CallableNameKind: TypeAlias = Literal["C", "P", "A", "K"]


@dataclass(frozen=True)
class FamilyEntry:
    """Metadata for exactly one canonical SPF family constructor."""

    family_id: str
    audit_family_id: str
    slug: str
    home: CatalogHome
    constructor_module: str
    constructor_name: str
    coverage: Coverage
    closed_parameters: tuple[str, ...]
    source_refs: tuple[str, ...]
    api_pressure_ref: str
    name_relations: tuple[str, ...]


@dataclass(frozen=True)
class RoleEntry:
    """Metadata for one audited close role with no family constructor."""

    audit_role_id: str
    slug: str
    role_kind: RoleKind
    source_refs: tuple[str, ...]
    boundary: str


@dataclass(frozen=True)
class LegacyEntry:
    """Metadata for one stable T01--T45 migration identity."""

    legacy_id: str
    label: str
    disposition: LegacyDisposition
    candidate_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    targets: tuple["LegacyTarget", ...]


@dataclass(frozen=True)
class LegacyTarget:
    """One normalized target branch retained by a legacy entry."""

    branch_name: str | None
    target_family_id: str
    callable_spelling: str | None
    treatment: CallableTreatment
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class NameEntry:
    """Callable-free metadata for one canonical or delegating spelling."""

    spelling: str
    owner_module: CatalogHome
    kind: CallableNameKind
    target_family_id: str
    delegate_import_name: str
    flat_export: bool
    closed_binding_summary: str
    legacy_entry_ids: tuple[str, ...]
    source_refs: tuple[str, ...]


FAMILY_ENTRIES: tuple[FamilyEntry, ...] = (
    FamilyEntry(
        "SPF001", "F001", "alternating-partition-local-evolution", "automata",
        "ca.catalog.automata", "alternating_partition_local_evolution", "addition",
        ("seed", "partition", "block_law", "boundary", "phase"),
        ("CH08:L155-165", "N08:L107,L124-126", "CH09:L303-321"),
        "goal-5/api-pressure.md:F001",
        (),
    ),
    FamilyEntry(
        "SPF002", "F002", "append-only-sequence-generation", "substitua",
        "ca.catalog.substitua", "append_only_sequence_generation", "covered",
        ("seed", "emitter", "control_schema", "support"),
        (
            "BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:"
            "L203-210,L569-599",
        ),
        "goal-5/api-pressure.md:F002",
        ("T40 split branch", "P constant_digit_sequence"),
    ),
    FamilyEntry(
        "SPF003", "F003", "asynchronous-local-state-automaton", "automata",
        "ca.catalog.automata", "asynchronous_local_state_automaton", "addition",
        ("seed", "local_law", "schedule", "boundary"),
        ("N09:L407-443",),
        "goal-5/api-pressure.md:F003",
        (),
    ),
    FamilyEntry(
        "SPF004", "F004", "event-provenance-causal-network", "media",
        "ca.catalog.media", "event_provenance_causal_network", "addition",
        ("event_trace", "read_sets", "initial_provenance"),
        ("CH09:L655-707", "N09:L347-355,L378-384"),
        "goal-5/api-pressure.md:F004",
        (),
    ),
    FamilyEntry(
        "SPF005", "F005", "context-dependent-substitution", "substitua",
        "ca.catalog.substitua", "context_dependent_substitution", "covered",
        ("seed", "productions", "context_shape", "boundary"),
        ("CH03:L333-337",),
        "goal-5/api-pressure.md:F005",
        ("neighbor_dependent_substitution", "T28 2-D preset"),
    ),
    FamilyEntry(
        "SPF006", "F006", "continuous-event-dynamics", "dynamica",
        "ca.catalog.dynamica", "continuous_event_dynamics", "addition",
        ("seed", "geometry", "flow_law", "reset_law", "terminal_condition"),
        (
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L60-61",
        ),
        "goal-5/api-pressure.md:F006",
        (),
    ),
    FamilyEntry(
        "SPF007", "F007", "coupled-field-mobile-locus-evolution", "automata",
        "ca.catalog.automata", "coupled_field_mobile_locus_evolution", "addition",
        ("seed", "field_law", "mobile_law", "boundary"),
        ("CH08:L131-138",),
        "goal-5/api-pressure.md:F007",
        (),
    ),
    FamilyEntry(
        "SPF008", "F008", "digit-emitting-register-transduction", "media",
        "ca.catalog.media", "digit_emitting_register_transduction", "covered",
        ("seed", "register_law", "base", "digit_projection"),
        ("CHAPTERS/04-Systems-Based-on-Numbers.md:L303-308,L343-350",),
        "goal-5/api-pressure.md:F008",
        ("T40 split branch", "P constant_digit_register"),
    ),
    FamilyEntry(
        "SPF009", "F009", "driven-relaxation", "automata",
        "ca.catalog.automata", "driven_relaxation", "addition",
        ("seed", "drive_law", "toppling_law", "boundary", "relaxation_form"),
        (
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L665-676",
        ),
        "goal-5/api-pressure.md:F009",
        (),
    ),
    FamilyEntry(
        "SPF010", "F011", "enumerative-semidecision", "machina",
        "ca.catalog.machina", "enumerative_semidecision", "addition",
        ("query", "enumeration", "predicate", "start"),
        ("CH10:L975-989", "N10:L5-15", "N11:L829-855"),
        "goal-5/api-pressure.md:F011",
        (),
    ),
    FamilyEntry(
        "SPF011", "F012", "error-diffusion-transform", "media",
        "ca.catalog.media", "error_diffusion_transform", "addition",
        ("input", "palette", "diffusion_kernel", "scan"),
        ("N10:L348-360",),
        "goal-5/api-pressure.md:F012",
        (),
    ),
    FamilyEntry(
        "SPF012", "F013", "maximal-run-record-transduction", "media",
        "ca.catalog.media", "maximal_run_record_transduction", "addition",
        ("input", "record_grammar", "direction", "scan", "feedback"),
        ("CH10:L163-187", "N10:L83-85,L171-175", "N04:L193-202"),
        "goal-5/api-pressure.md:F013",
        (
            "P look_and_say feedback preset",
            "flat export",
            "preset source N04:L193-202",
        ),
    ),
    FamilyEntry(
        "SPF013", "F014", "finite-gate-circuit", "machina",
        "ca.catalog.machina", "finite_gate_circuit", "addition",
        ("inputs", "wiring", "gates", "schedule", "measurement"),
        ("N10:L904", "N12:L331-347,L560-574"),
        "goal-5/api-pressure.md:F014",
        (),
    ),
    FamilyEntry(
        "SPF014", "F015", "finite-model-satisfaction", "criteria",
        "ca.catalog.criteria", "finite_model_satisfaction", "addition",
        ("axioms", "finite_domain", "signatures", "fixed_tables"),
        ("CH12:L1073-1095", "N12:L1189-1203,L1245-1257"),
        "goal-5/api-pressure.md:F015",
        (),
    ),
    FamilyEntry(
        "SPF015", "F016", "first-passage-aggregation", "substitua",
        "ca.catalog.substitua", "first_passage_aggregation", "addition",
        ("seed", "walk_law", "contact", "release", "boundary", "target"),
        (
            "N08:L50",
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L359-360",
        ),
        "goal-5/api-pressure.md:F016",
        (),
    ),
    FamilyEntry(
        "SPF016", "F017", "front-delete-rear-append-system", "substitua",
        "ca.catalog.substitua", "front_delete_rear_append_system", "covered",
        ("seed", "deletion_width", "productions", "phase_cycle"),
        ("CH03:L423-445,L447-471",),
        "goal-5/api-pressure.md:F017",
        ("tag_system", "T18 cyclic_tag_system preset"),
    ),
    FamilyEntry(
        "SPF017", "F018", "geometric-embedding-relation", "criteria",
        "ca.catalog.criteria", "geometric_embedding_relation", "addition",
        ("mesh", "growth", "metric_constraints", "boundary_embedding"),
        ("CH08:L563-569", "N08:L226"),
        "goal-5/api-pressure.md:F018",
        (),
    ),
    FamilyEntry(
        "SPF018", "F019", "global-equation-relation", "criteria",
        "ca.catalog.criteria", "global_equation_relation", "addition",
        ("equation", "domain", "known_assignments", "witness_schema"),
        ("CH12:L885-905", "N12:L901-966"),
        "goal-5/api-pressure.md:F019",
        (),
    ),
    FamilyEntry(
        "SPF019", "F020", "global-score-sequential-placement", "substitua",
        "ca.catalog.substitua", "global_score_sequential_placement", "addition",
        (
            "seed",
            "score_expression",
            "placement_shape",
            "depletion_kernel",
            "tie_law",
        ),
        ("CH08:L531-547", "N08:L223-225"),
        "goal-5/api-pressure.md:F020",
        (),
    ),
    FamilyEntry(
        "SPF020", "F021", "hash-index-transform", "media",
        "ca.catalog.media", "hash_index_transform", "addition",
        ("key", "table", "hash_fold", "collision", "operation"),
        ("CH10:L829-839", "N10:L976-980"),
        "goal-5/api-pressure.md:F021",
        (),
    ),
    FamilyEntry(
        "SPF021", "F022", "history-dependent-agent-game", "automata",
        "ca.catalog.automata", "history_dependent_agent_game", "addition",
        ("agents", "histories", "payoff", "action_schema", "round_control"),
        ("N10:L1081-1085",),
        "goal-5/api-pressure.md:F022",
        (),
    ),
    FamilyEntry(
        "SPF022", "F023", "history-dependent-growth-rewrite", "substitua",
        "ca.catalog.substitua", "history_dependent_growth_rewrite", "addition",
        ("seed", "eligibility", "provenance_law", "boundary"),
        (
            "BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md:"
            "L130-151",
        ),
        "goal-5/api-pressure.md:F023",
        (),
    ),
    FamilyEntry(
        "SPF023", "F024", "indexed-history-recurrence", "substitua",
        "ca.catalog.substitua", "indexed_history_recurrence", "covered",
        ("prefix", "recurrence", "index_law", "invalidity"),
        ("CHAPTERS/04-Systems-Based-on-Numbers.md:L169-186",),
        "goal-5/api-pressure.md:F024",
        ("T38 variable-index preset",),
    ),
    FamilyEntry(
        "SPF024", "F025", "inverse-local-system-reconstruction", "criteria",
        "ca.catalog.criteria", "inverse_local_system_reconstruction", "addition",
        (
            "observations",
            "local_law",
            "boundary",
            "unknown_schema",
            "search_order",
        ),
        ("CH10:L575-633", "N10:L531-544,L608-624"),
        "goal-5/api-pressure.md:F025",
        (),
    ),
    FamilyEntry(
        "SPF025", "F026", "iterated-erasure-process", "substitua",
        "ca.catalog.substitua", "iterated_erasure_process", "covered",
        ("seed", "erasure_predicate", "rank_convention"),
        ("CHAPTERS/04-Systems-Based-on-Numbers.md:L211-214",),
        "goal-5/api-pressure.md:F026",
        ("number_theoretic_filtering preset",),
    ),
    FamilyEntry(
        "SPF026", "F027", "iterated-map", "automata",
        "ca.catalog.automata", "iterated_map", "covered",
        ("seed", "map_expression", "guards", "terminal_condition"),
        ("CHAPTERS/04-Systems-Based-on-Numbers.md:L53-54,L111-118,L472-491",),
        "goal-5/api-pressure.md:F027",
        ("T34 arithmetic, T35 piecewise, and T36 digit-reversal presets",),
    ),
    FamilyEntry(
        "SPF027", "F028", "local-factor-weighted-relation", "criteria",
        "ca.catalog.criteria", "local_factor_weighted_relation", "addition",
        ("seed", "factors", "reduction", "normalization", "objective"),
        ("N10:L493-494",),
        "goal-5/api-pressure.md:F028",
        (),
    ),
    FamilyEntry(
        "SPF028", "F029", "local-graph-rewrite", "substitua",
        "ca.catalog.substitua", "local_graph_rewrite", "addition",
        ("seed", "patterns", "replacements", "match_schedule", "interface_schema"),
        ("CH09:L901-965", "N09:L495-528,L552-556,L594-600"),
        "goal-5/api-pressure.md:F029",
        (),
    ),
    FamilyEntry(
        "SPF029", "F030", "local-satisfaction-relation", "criteria",
        "ca.catalog.criteria", "local_satisfaction_relation", "covered",
        ("partial_assignment", "templates", "boundary", "obligations"),
        ("CH09:L595-615", "N09:L324-330"),
        "goal-5/api-pressure.md:F030",
        ("T31", "T32 template name", "T33 seeded-template preset"),
    ),
    FamilyEntry(
        "SPF030", "F031", "mobile-head-grid-rewrite", "machina",
        "ca.catalog.machina", "mobile_head_grid_rewrite", "covered",
        ("tape", "transitions", "head", "stencil", "boundary"),
        ("CHAPTERS/05-Two-Dimensions-and-Beyond.md:L127-131",),
        "goal-5/api-pressure.md:F031",
        (
            "turing_machine",
            "T09 mobile, T10 repaired neighbor-updating, T25 2-D presets",
        ),
    ),
    FamilyEntry(
        "SPF031", "F032", "moving-frontier-shell-accretion", "substitua",
        "ca.catalog.substitua", "moving_frontier_shell_accretion", "addition",
        ("seed", "strip_constructor", "rim_law", "geometry", "terminal_condition"),
        ("CH08:L581-591", "N08:L234-246"),
        "goal-5/api-pressure.md:F032",
        (),
    ),
    FamilyEntry(
        "SPF032", "F033", "multi-active-local-rewrite", "automata",
        "ca.catalog.automata", "multi_active_local_rewrite", "covered",
        ("seed", "local_law", "collision_law", "schedule"),
        ("CH03:L231-247",),
        "goal-5/api-pressure.md:F033",
        ("generalized_mobile_automaton preset",),
    ),
    FamilyEntry(
        "SPF033", "F034", "multiway-rewrite", "substitua",
        "ca.catalog.substitua", "multiway_rewrite", "covered",
        ("seed", "rewrites", "match_semantics", "quotient"),
        ("CHAPTERS/05-Two-Dimensions-and-Beyond.md:L355-369",),
        "goal-5/api-pressure.md:F034",
        ("multiway_system true alias",),
    ),
    FamilyEntry(
        "SPF034", "F035", "mutable-rule-local-automaton", "automata",
        "ca.catalog.automata", "mutable_rule_local_automaton", "addition",
        ("seed", "rule_program", "interpreter", "mutation_law"),
        ("CH08:L319-329",),
        "goal-5/api-pressure.md:F035",
        (),
    ),
    FamilyEntry(
        "SPF035", "F036", "nearest-neighbor-retrieval", "machina",
        "ca.catalog.machina", "nearest_neighbor_retrieval", "addition",
        ("items", "query", "metric", "index", "traversal"),
        ("N10:L988-996",),
        "goal-5/api-pressure.md:F036",
        (),
    ),
    FamilyEntry(
        "SPF036", "F037", "ordinary-differential-flow", "dynamica",
        "ca.catalog.dynamica", "ordinary_differential_flow", "addition",
        ("seed", "rhs", "parameters", "duration_or_event"),
        (
            "BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:"
            "L901-902,L953-980",
        ),
        "goal-5/api-pressure.md:F037",
        (),
    ),
    FamilyEntry(
        "SPF037", "F038", "parallel-independent-substitution", "substitua",
        "ca.catalog.substitua", "parallel_independent_substitution", "covered",
        ("seed", "productions", "schedule", "geometry"),
        ("CH03:L299-307,L343-363",),
        "goal-5/api-pressure.md:F038",
        ("T15 merge", "T26/T27/T42 presets", "neighbor_independent_substitution"),
    ),
    FamilyEntry(
        "SPF038", "F040", "parallel-network-rewrite", "substitua",
        "ca.catalog.substitua", "parallel_network_rewrite", "covered",
        ("seed", "patches", "port_schema", "overlap_law"),
        ("CHAPTERS/05-Two-Dimensions-and-Beyond.md:L241,L287-331",),
        "goal-5/api-pressure.md:F040",
        ("network_rewrite", "broad network_system is not exported"),
    ),
    FamilyEntry(
        "SPF039", "F041", "partial-differential-relation", "dynamica",
        "ca.catalog.dynamica", "partial_differential_relation", "covered",
        ("domain", "coefficients", "differential_relation", "side_data"),
        (
            "CHAPTERS/04-Systems-Based-on-Numbers.md:L625-674",
            "N08:L84-105,L322-328",
        ),
        "goal-5/api-pressure.md:F041",
        ("T45 canonical constructor", "pde true alias"),
    ),
    FamilyEntry(
        "SPF040", "F043", "population-evolutionary-search", "automata",
        "ca.catalog.automata", "population_evolutionary_search", "addition",
        (
            "population",
            "fitness_expression",
            "selection",
            "recombination",
            "mutation",
            "size",
        ),
        (
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L556-560",
        ),
        "goal-5/api-pressure.md:F043",
        (),
    ),
    FamilyEntry(
        "SPF041", "F044", "probabilistic-transition-model-fitting", "media",
        "ca.catalog.media", "probabilistic_transition_model_fitting", "addition",
        (
            "observations",
            "topology",
            "estimator",
            "generation_law",
            "generation_request",
        ),
        ("CH10:L441-459", "N10:L495-501"),
        "goal-5/api-pressure.md:F044",
        (),
    ),
    FamilyEntry(
        "SPF042", "F045", "program-randomization-test", "criteria",
        "ca.catalog.criteria", "program_randomization_test", "addition",
        (
            "observed",
            "surrogate_law",
            "program",
            "statistic",
            "replicates",
            "calibration",
        ),
        ("CH10:L515-533",),
        "goal-5/api-pressure.md:F045",
        (),
    ),
    FamilyEntry(
        "SPF043", "F046", "random-functional-graph-construction", "substitua",
        "ca.catalog.substitua", "random_functional_graph_construction", "addition",
        ("nodes", "successor_measure"),
        (
            "BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md:"
            "L589-590",
        ),
        "goal-5/api-pressure.md:F046",
        (),
    ),
    FamilyEntry(
        "SPF044", "F047", "recursive-function-evaluator", "machina",
        "ca.catalog.machina", "recursive_function_evaluator", "covered",
        ("call", "definitions", "evaluation_order", "cache"),
        (
            "BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md:"
            "L237-268,L316-364",
        ),
        "goal-5/api-pressure.md:F047",
        (
            "Repaired T41",
            "function_combination_system retained only as deprecated metadata",
        ),
    ),
    FamilyEntry(
        "SPF045", "F048", "register-machine", "machina",
        "ca.catalog.machina", "register_machine", "covered",
        ("program", "registers", "entry"),
        ("CH03:L473-509,L519-525",),
        "goal-5/api-pressure.md:F048",
        ("register_machine",),
    ),
    FamilyEntry(
        "SPF046", "F049", "sampled-causal-order-network", "media",
        "ca.catalog.media", "sampled_causal_order_network", "addition",
        ("region", "causal_order", "density", "event_measure"),
        ("N09:L816-818",),
        "goal-5/api-pressure.md:F049",
        ("Distinct from F004 producer-history transform",),
    ),
    FamilyEntry(
        "SPF047", "F050", "stochastic-local-search", "criteria",
        "ca.catalog.criteria", "stochastic_local_search", "addition",
        ("incumbent", "objective", "constraints", "proposal", "acceptance"),
        ("CHAPTERS/07-Mechanisms-in-Programs-and-Nature.md:L553-596",),
        "goal-5/api-pressure.md:F050",
        (),
    ),
    FamilyEntry(
        "SPF048", "F051", "stored-program-random-access-machine", "machina",
        "ca.catalog.machina", "stored_program_random_access_machine", "addition",
        ("memory", "entry", "instruction_set"),
        ("N11:L15-23",),
        "goal-5/api-pressure.md:F051",
        (),
    ),
    FamilyEntry(
        "SPF049", "F052", "structural-pattern-rewrite", "substitua",
        "ca.catalog.substitua", "structural_pattern_rewrite", "covered",
        ("expression", "patterns", "replacements", "scan", "nonoverlap"),
        ("CH03:L531-537", "N03:L823-835", "CH10:L909-915"),
        "goal-5/api-pressure.md:F052",
        ("symbolic_system", "T16 sequential-substitution preset"),
    ),
    FamilyEntry(
        "SPF050", "F053", "synchronous-local-state-transform", "automata",
        "ca.catalog.automata", "synchronous_local_state_transform", "covered",
        ("seed", "stencil", "local_law", "boundary", "feedback"),
        ("CH10:L323-347", "N10:L328-347", "N03:L135-150,L190,L192-225"),
        "goal-5/api-pressure.md:F053",
        (
            "eca, elementary_cellular_automaton",
            "T02–T07, T21–T24 presets",
            "T44 family-level alias implemented as a preset",
        ),
    ),
    FamilyEntry(
        "SPF051", "F054", "weighted-history-sum-relation", "criteria",
        "ca.catalog.criteria", "weighted_history_sum_relation", "addition",
        ("domain", "side_data", "histories", "action", "measure", "observables"),
        ("N09:L880,L955-957",),
        "goal-5/api-pressure.md:F054",
        (),
    ),
    FamilyEntry(
        "SPF052", "F055", "weighted-network-state-update", "automata",
        "ca.catalog.automata", "weighted_network_state_update", "covered",
        ("network", "seed", "weights", "schedule", "learning_law"),
        ("N10:L1021-1023",),
        "goal-5/api-pressure.md:F055",
        (
            "Normalizes C045 legacy coverage",
            "no T01–T45 owner",
            "never alias network_system",
        ),
    ),
    FamilyEntry(
        "SPF053", "F056", "priority-dovetailed-oracle-construction", "machina",
        "ca.catalog.machina", "priority_dovetailed_oracle_construction", "addition",
        ("approximations", "machines", "requirements", "priority", "fair_schedule"),
        ("N12:L80-92",),
        "goal-5/api-pressure.md:F056",
        (),
    ),
    FamilyEntry(
        "SPF054", "F057", "weighted-prefix-block-transduction", "media",
        "ca.catalog.media", "weighted_prefix_block_transduction", "addition",
        ("input", "block_partition", "weights_or_tree", "direction"),
        ("CH10:L189-205,L235-249", "N10:L87-106"),
        "goal-5/api-pressure.md:F057",
        (),
    ),
    FamilyEntry(
        "SPF055", "F058", "nested-interval-symbol-transduction", "media",
        "ca.catalog.media", "nested_interval_symbol_transduction", "addition",
        ("input", "probability_model", "precision", "direction"),
        ("N10:L108-121",),
        "goal-5/api-pressure.md:F058",
        (),
    ),
    FamilyEntry(
        "SPF056", "F059", "history-reference-record-transduction", "media",
        "ca.catalog.media", "history_reference_record_transduction", "addition",
        ("input", "match_policy", "dictionary", "record_grammar", "direction"),
        ("CH10:L209-267", "N10:L123-153"),
        "goal-5/api-pressure.md:F059",
        (),
    ),
    FamilyEntry(
        "SPF057", "F060", "recursive-uniform-region-decomposition", "media",
        "ca.catalog.media", "recursive_uniform_region_decomposition", "addition",
        ("input", "root_region", "split", "uniformity", "cutoff", "direction"),
        ("CH10:L233-239,L269-279", "N10:L154-168"),
        "goal-5/api-pressure.md:F060",
        (),
    ),
    FamilyEntry(
        "SPF058", "F061", "orthogonal-basis-coefficient-transform", "media",
        "ca.catalog.media", "orthogonal_basis_coefficient_transform", "addition",
        ("input", "basis", "ordering", "retention", "quantization", "direction"),
        ("CH10:L281-305", "N10:L181-288"),
        "goal-5/api-pressure.md:F061",
        (),
    ),
    FamilyEntry(
        "SPF059", "F062", "predictive-residual-transduction", "media",
        "ca.catalog.media", "predictive_residual_transduction", "addition",
        ("input", "predictor", "history", "fitting", "residual_code", "direction"),
        ("N10:L424",),
        "goal-5/api-pressure.md:F062",
        (),
    ),
    FamilyEntry(
        "SPF060", "F063", "aligned-xor-stream-transduction", "media",
        "ca.catalog.media", "aligned_xor_stream_transduction", "addition",
        ("input", "keystream", "alignment", "generator"),
        ("CH10:L539-565,L599-605",),
        "goal-5/api-pressure.md:F063",
        (),
    ),
)


ROLE_ENTRIES: tuple[RoleEntry, ...] = (
    RoleEntry(
        "F010",
        "encode-evolve-decode-interface",
        "interface",
        ("CH11:L15-37", "N11:L674-690"),
        (
            "A concrete encoder or decoder with its own invariant commit may be "
            "an ordinary media program, while composition around an unchanged "
            "target belongs to run/query tooling."
        ),
    ),
    RoleEntry(
        "F042",
        "percolation-connectivity-analysis",
        "observer",
        (
            "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md:"
            "L497-498",
        ),
        (
            "Occupation may be a Seed law, but spanning/connectivity over the "
            "completed sample is an observer or analysis result."
        ),
    ),
)


LEGACY_ENTRIES: tuple[LegacyEntry, ...] = (
    LegacyEntry(
        "T01",
        "Elementary Cellular Automata",
        "retain-family",
        ("C090",),
        ("CH03:L29-56",),
        (
            LegacyTarget(
                None, "SPF050", "eca", "P", ("CH03:L29-56",)
            ),
        ),
    ),
    LegacyEntry(
        "T02",
        "Multi-Color Nearest-Neighbor Cellular Automata",
        "retain-preset",
        ("C090",),
        ("N03:L135-150",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "multicolor_cellular_automaton",
                "P",
                ("N03:L135-150",),
            ),
        ),
    ),
    LegacyEntry(
        "T03",
        "Totalistic Cellular Automata",
        "retain-preset",
        ("C090",),
        ("CH03:L91-96",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "totalistic_cellular_automaton",
                "P",
                ("CH03:L91-96",),
            ),
        ),
    ),
    LegacyEntry(
        "T04",
        "Three-Color Totalistic Cellular Automata",
        "retain-preset",
        ("C090",),
        ("CH03:L89-96,L109-110",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "three_color_totalistic_cellular_automaton",
                "P",
                ("CH03:L89-96,L109-110",),
            ),
        ),
    ),
    LegacyEntry(
        "T05",
        "Higher-Color Totalistic Cellular Automata",
        "merge",
        ("C090",),
        ("N03:L164-185",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "higher_color_totalistic_cellular_automaton",
                "P",
                ("N03:L164-185",),
            ),
        ),
    ),
    LegacyEntry(
        "T06",
        "Quiescent-Background-Preserving Cellular Automata",
        "retain-preset",
        ("C090",),
        (
            "Goal 2-preserved T(b,…,b)=b",
            "CH03:L101,L649",
            "CH06:L101",
            "goal-1/25-T06-QUIESCENT.md",
        ),
        (
            LegacyTarget(
                None,
                "SPF050",
                "quiescent_cellular_automaton",
                "P",
                (
                    "Goal 2-preserved T(b,…,b)=b",
                    "CH03:L101,L649",
                    "CH06:L101",
                    "goal-1/25-T06-QUIESCENT.md",
                ),
            ),
        ),
    ),
    LegacyEntry(
        "T07",
        "Left-Right Symmetric Cellular Automata",
        "retain-preset",
        ("C090",),
        ("N03:L7-10", "N05:L89-100"),
        (
            LegacyTarget(
                None,
                "SPF050",
                "symmetric_cellular_automaton",
                "P",
                ("N03:L7-10", "N05:L89-100"),
            ),
        ),
    ),
    LegacyEntry(
        "T08",
        "Initial-Condition Classes",
        "retire-role",
        (),
        ("Goal 5 Seed-role decision", "no executable construction source"),
        (),
    ),
    LegacyEntry(
        "T09",
        "Mobile Automata",
        "retain-preset",
        ("C047",),
        ("CH03:L169-185",),
        (
            LegacyTarget(
                None, "SPF030", "mobile_automaton", "P", ("CH03:L169-185",)
            ),
        ),
    ),
    LegacyEntry(
        "T10",
        "Extended Mobile Automata",
        "repair",
        ("C056",),
        ("CH03:L197-207",),
        (
            LegacyTarget(
                None,
                "SPF030",
                "neighbor_updating_mobile_automaton",
                "P",
                ("CH03:L197-207",),
            ),
        ),
    ),
    LegacyEntry(
        "T11",
        "Generalized Mobile Automata",
        "retain-family",
        ("C030",),
        ("CH03:L231-247",),
        (
            LegacyTarget(
                None,
                "SPF032",
                "generalized_mobile_automaton",
                "P",
                ("CH03:L231-247",),
            ),
        ),
    ),
    LegacyEntry(
        "T12",
        "Turing Machines",
        "retain-family",
        ("C049",),
        ("N03:L294-333",),
        (
            LegacyTarget(
                None, "SPF030", "turing_machine", "P", ("N03:L294-333",)
            ),
        ),
    ),
    LegacyEntry(
        "T13",
        "Neighbor-Independent Substitution Systems",
        "retain-family",
        ("C061",),
        ("CH03:L299-307",),
        (
            LegacyTarget(
                None,
                "SPF037",
                "neighbor_independent_substitution",
                "P",
                ("CH03:L299-307",),
            ),
        ),
    ),
    LegacyEntry(
        "T14",
        "Neighbor-Dependent Substitution Systems",
        "retain-family",
        ("C011", "C055"),
        ("CH03:L333-337", "CH05:L211-227", "N05:L360-367"),
        (
            LegacyTarget(
                None,
                "SPF005",
                "neighbor_dependent_substitution",
                "P",
                ("CH03:L333-337", "CH05:L211-227", "N05:L360-367"),
            ),
        ),
    ),
    LegacyEntry(
        "T15",
        "Creation-Destruction Substitution Systems",
        "merge",
        ("C061",),
        ("CH03:L343-363",),
        (
            LegacyTarget(
                None,
                "SPF037",
                "creation_destruction_substitution",
                "P",
                ("CH03:L343-363",),
            ),
        ),
    ),
    LegacyEntry(
        "T16",
        "Sequential Substitution Systems",
        "retain-preset",
        ("C080",),
        ("CH03:L369-379",),
        (
            LegacyTarget(
                None,
                "SPF049",
                "sequential_substitution",
                "P",
                ("CH03:L369-379",),
            ),
        ),
    ),
    LegacyEntry(
        "T17",
        "Tag Systems",
        "retain-family",
        ("C091",),
        ("CH03:L423-445",),
        (
            LegacyTarget(
                None, "SPF016", "tag_system", "P", ("CH03:L423-445",)
            ),
        ),
    ),
    LegacyEntry(
        "T18",
        "Cyclic Tag Systems",
        "retain-preset",
        ("C091",),
        ("CH03:L447-471",),
        (
            LegacyTarget(
                None, "SPF016", "cyclic_tag_system", "P", ("CH03:L447-471",)
            ),
        ),
    ),
    LegacyEntry(
        "T19",
        "Register Machines",
        "retain-family",
        ("C073",),
        ("CH03:L473-509,L519-525",),
        (
            LegacyTarget(
                None,
                "SPF045",
                "register_machine",
                "C",
                ("CH03:L473-509,L519-525",),
            ),
        ),
    ),
    LegacyEntry(
        "T20",
        "Symbolic Systems",
        "retain-family",
        ("C089",),
        ("CH03:L531-537", "N03:L823-835", "CH10:L909-915"),
        (
            LegacyTarget(
                None,
                "SPF049",
                "symbolic_system",
                "P",
                ("CH03:L531-537", "N03:L823-835", "CH10:L909-915"),
            ),
        ),
    ),
    LegacyEntry(
        "T21",
        "Two-Dimensional Cellular Automata",
        "retain-preset",
        ("C090",),
        ("CH05:L27-34",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "cellular_automaton_2d",
                "P",
                ("CH05:L27-34",),
            ),
        ),
    ),
    LegacyEntry(
        "T22",
        "Moore-Neighborhood Cellular Automata",
        "retain-preset",
        ("C090",),
        ("CH05:L67-86",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "moore_cellular_automaton",
                "P",
                ("CH05:L67-86",),
            ),
        ),
    ),
    LegacyEntry(
        "T23",
        "Three-Dimensional Cellular Automata",
        "retain-preset",
        ("C090",),
        ("CH05:L95-123", "N06:L55-66"),
        (
            LegacyTarget(
                None,
                "SPF050",
                "cellular_automaton_3d",
                "P",
                ("CH05:L95-123", "N06:L55-66"),
            ),
        ),
    ),
    LegacyEntry(
        "T24",
        "Higher-Dimensional Lattice Cellular Automata",
        "retain-preset",
        ("C090",),
        ("N05:L36-58,L66-88",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "lattice_cellular_automaton",
                "P",
                ("N05:L36-58,L66-88",),
            ),
        ),
    ),
    LegacyEntry(
        "T25",
        "Two-Dimensional Turing Machines",
        "retain-preset",
        ("C049",),
        ("CH05:L127-131", "N05:L211-217"),
        (
            LegacyTarget(
                None,
                "SPF030",
                "turing_machine_2d",
                "P",
                ("CH05:L127-131", "N05:L211-217"),
            ),
        ),
    ),
    LegacyEntry(
        "T26",
        "Two-Dimensional Substitution Systems",
        "retain-preset",
        ("C061",),
        ("CH05:L173-190",),
        (
            LegacyTarget(
                None,
                "SPF037",
                "substitution_system_2d",
                "P",
                ("CH05:L173-190",),
            ),
        ),
    ),
    LegacyEntry(
        "T27",
        "Geometric Replacement And Fractal Systems",
        "repair",
        ("C061",),
        ("CH05:L191-214", "N05:L286-337"),
        (
            LegacyTarget(
                None,
                "SPF037",
                "geometric_substitution",
                "P",
                ("CH05:L191-214", "N05:L286-337"),
            ),
        ),
    ),
    LegacyEntry(
        "T28",
        "Neighbor-Dependent Two-Dimensional Substitution Systems",
        "retain-preset",
        ("C055",),
        ("CH05:L211-227", "N05:L360-367"),
        (
            LegacyTarget(
                None,
                "SPF005",
                "context_dependent_substitution_2d",
                "P",
                ("CH05:L211-227", "N05:L360-367"),
            ),
        ),
    ),
    LegacyEntry(
        "T29",
        "Network Systems",
        "retain-family",
        ("C062",),
        ("CH05:L239-248,L287-331",),
        (
            LegacyTarget(
                None,
                "SPF038",
                "parallel_network_rewrite",
                "C",
                ("CH05:L239-248,L287-331",),
            ),
        ),
    ),
    LegacyEntry(
        "T30",
        "Multiway Systems",
        "retain-family",
        ("C051",),
        ("CH05:L355-369", "N05:L527-528,L549-578"),
        (
            LegacyTarget(
                None,
                "SPF033",
                "multiway_system",
                "A",
                ("CH05:L355-369", "N05:L527-528,L549-578"),
            ),
        ),
    ),
    LegacyEntry(
        "T31",
        "Local Constraint Systems",
        "retain-family",
        ("C043",),
        ("CH05:L433-479", "CH09:L595-615", "N09:L324-330"),
        (
            LegacyTarget(
                None,
                "SPF029",
                "local_constraint_system",
                "P",
                ("CH05:L433-479", "CH09:L595-615", "N09:L324-330"),
            ),
        ),
    ),
    LegacyEntry(
        "T32",
        "Template Constraint Systems",
        "alias",
        ("C043",),
        ("CH05:L475-488",),
        (
            LegacyTarget(
                None,
                "SPF029",
                "template_constraint_system",
                "P",
                ("CH05:L475-488",),
            ),
        ),
    ),
    LegacyEntry(
        "T33",
        "Seeded Template Constraint Systems",
        "retain-preset",
        ("C042", "C043"),
        ("CH05:L475-498,L535-536",),
        (
            LegacyTarget(
                None,
                "SPF029",
                "seeded_template_constraint_system",
                "P",
                ("CH05:L475-498,L535-536",),
            ),
        ),
    ),
    LegacyEntry(
        "T34",
        "Arithmetic Iteration Systems",
        "retain-preset",
        ("C037",),
        ("CH04:L53-54",),
        (
            LegacyTarget(
                None,
                "SPF026",
                "arithmetic_iteration",
                "P",
                ("CH04:L53-54",),
            ),
        ),
    ),
    LegacyEntry(
        "T35",
        "Piecewise Integer Maps",
        "retain-preset",
        ("C037",),
        ("CH04:L111-118",),
        (
            LegacyTarget(
                None,
                "SPF026",
                "piecewise_integer_map",
                "P",
                ("CH04:L111-118",),
            ),
        ),
    ),
    LegacyEntry(
        "T36",
        "Digit-Reversal Arithmetic Systems",
        "retain-preset",
        ("C037",),
        ("CH04:L153-162", "N04:L170-179"),
        (
            LegacyTarget(
                None,
                "SPF026",
                "digit_reversal_map",
                "P",
                ("CH04:L153-162", "N04:L170-179"),
            ),
        ),
    ),
    LegacyEntry(
        "T37",
        "Recursive Sequences",
        "retain-family",
        ("C078",),
        ("CH04:L169-186",),
        (
            LegacyTarget(
                None,
                "SPF023",
                "recursive_sequence",
                "P",
                ("CH04:L169-186",),
            ),
        ),
    ),
    LegacyEntry(
        "T38",
        "Variable-Index Recursive Sequences",
        "retain-preset",
        ("C078",),
        ("CH04:L179-186",),
        (
            LegacyTarget(
                None,
                "SPF023",
                "variable_index_recursive_sequence",
                "P",
                ("CH04:L179-186",),
            ),
        ),
    ),
    LegacyEntry(
        "T39",
        "Number-Theoretic Filtering Systems",
        "retain-family",
        ("C035",),
        ("CH04:L211-214", "N04:L418-430"),
        (
            LegacyTarget(
                None,
                "SPF025",
                "number_theoretic_filtering",
                "P",
                ("CH04:L211-214", "N04:L418-430"),
            ),
        ),
    ),
    LegacyEntry(
        "T40",
        "Mathematical-Constant Digit Systems",
        "split",
        ("C003", "C017"),
        (
            "sequence N04:L203-210,L569-599",
            "register CH04:L303-308,L343-350",
            "N04:L561-562",
        ),
        (
            LegacyTarget(
                "sequence",
                "SPF002",
                "constant_digit_sequence",
                "P",
                ("N04:L203-210,L569-599",),
            ),
            LegacyTarget(
                "register",
                "SPF008",
                "constant_digit_register",
                "P",
                ("CH04:L303-308,L343-350", "N04:L561-562"),
            ),
        ),
    ),
    LegacyEntry(
        "T41",
        "Function-Combination Systems",
        "repair",
        ("C072",),
        ("N04:L237-268,L316-364",),
        (
            LegacyTarget(
                None,
                "SPF044",
                "recursive_function_evaluator",
                "C",
                ("N04:L237-268,L316-364",),
            ),
        ),
    ),
    LegacyEntry(
        "T42",
        "Continued-Fraction-Driven Substitution Systems",
        "retain-preset",
        ("C061",),
        ("CH04:L454-461", "N04:L753-754"),
        (
            LegacyTarget(
                None,
                "SPF037",
                "continued_fraction_substitution",
                "P",
                ("CH04:L454-461", "N04:L753-754"),
            ),
        ),
    ),
    LegacyEntry(
        "T43",
        "Iterated Maps",
        "retain-family",
        ("C037",),
        ("CH04:L53-54,L111-118,L472-491",),
        (
            LegacyTarget(
                None,
                "SPF026",
                "iterated_map",
                "C",
                ("CH04:L53-54,L111-118,L472-491",),
            ),
        ),
    ),
    LegacyEntry(
        "T44",
        "Continuous Cellular Automata",
        "alias",
        ("C090",),
        ("CH04:L546-562,L565-616",),
        (
            LegacyTarget(
                None,
                "SPF050",
                "continuous_cellular_automaton",
                "P",
                ("CH04:L546-562,L565-616",),
            ),
        ),
    ),
    LegacyEntry(
        "T45",
        "Partial Differential Equation Systems",
        "retain-family",
        ("C063",),
        ("CH04:L625-674", "N04:L933-940"),
        (
            LegacyTarget(
                None,
                "SPF039",
                "partial_differential_relation",
                "C",
                ("CH04:L625-674", "N04:L933-940"),
            ),
        ),
    ),
)


__all__ = (
    "CallableNameKind",
    "CallableTreatment",
    "CatalogHome",
    "Coverage",
    "FAMILY_ENTRIES",
    "FamilyEntry",
    "LegacyDisposition",
    "LegacyEntry",
    "LegacyTarget",
    "NameEntry",
    "ROLE_ENTRIES",
    "RoleEntry",
    "RoleKind",
)
