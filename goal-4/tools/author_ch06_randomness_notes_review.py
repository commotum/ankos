#!/usr/bin/env python3
"""Author the sealed Stage 10 Chapter 6 Notes blind-review output.

The semantic decisions below are deliberately data, while the surrounding
code enforces allocation, ordering, linkage, and deterministic serialization.
The script reads only the sealed worker bundle passed on the command line.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


FIELDS = [
    "object_kind",
    "native_time",
    "carrier",
    "support",
    "topology",
    "structural_invariants",
    "alphabet_or_value_schema",
    "complete_state",
    "visible_history",
    "control_state",
    "seed",
    "input",
    "boundary",
    "external_data",
    "frontier_or_activation",
    "schedule",
    "read_dependencies_or_neighborhood",
    "law_kind",
    "rule_relation_constraint_function_or_probability_law",
    "write_replacement_assembly_or_commit",
    "result_kind",
    "successor_cardinality",
    "determinism_branching_or_measure",
    "termination_completion_failure",
    "witness_semantics",
    "parameters_and_variants",
    "excluded_observers_and_representations",
    "evidence_limit",
]

PROFILES: dict[str, dict[str, str]] = {
    "ca1d": {
        "object_kind": "one-dimensional cellular automaton",
        "native_time": "discrete evolution steps",
        "carrier": "a one-dimensional line of cells",
        "support": "a cell-color configuration",
        "topology": "one-dimensional cellular adjacency",
        "alphabet_or_value_schema": "finite cell colors",
        "complete_state": "the complete cell-color configuration",
        "frontier_or_activation": "all cells updated each step",
        "schedule": "synchronous",
        "law_kind": "local deterministic transition rule",
        "write_replacement_assembly_or_commit": "one successor color is committed per cell",
        "result_kind": "a successor cell-color configuration",
        "successor_cardinality": "one",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "unbounded iteration unless an external observation horizon is chosen",
        "excluded_observers_and_representations": "density, entropy, plots, and rendered histories are not native state",
    },
    "ca2d": {
        "object_kind": "two-dimensional cellular automaton",
        "native_time": "discrete evolution steps",
        "carrier": "a two-dimensional lattice of cells",
        "support": "a cell-color configuration",
        "topology": "two-dimensional lattice adjacency",
        "alphabet_or_value_schema": "finite cell colors",
        "complete_state": "the complete cell-color configuration",
        "frontier_or_activation": "all cells updated each step",
        "schedule": "synchronous",
        "law_kind": "local deterministic transition rule",
        "write_replacement_assembly_or_commit": "one successor color is committed per cell",
        "result_kind": "a successor cell-color configuration",
        "successor_cardinality": "one",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "unbounded iteration unless an external observation horizon is chosen",
        "excluded_observers_and_representations": "rendered histories and structure names are not native state",
    },
    "map": {
        "object_kind": "iterated map",
        "native_time": "discrete iterations",
        "carrier": "the map's value domain",
        "complete_state": "the current value",
        "frontier_or_activation": "the current value",
        "schedule": "one map application per iteration",
        "law_kind": "deterministic function",
        "write_replacement_assembly_or_commit": "replace the current value by the function result",
        "result_kind": "a successor value",
        "successor_cardinality": "one",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "unbounded iteration unless an external observation horizon is chosen",
    },
    "stochastic": {
        "object_kind": "stochastic dynamical process",
        "native_time": "discrete steps",
        "complete_state": "the current system state",
        "schedule": "one stochastic transition per step",
        "law_kind": "probability law over successor states",
        "result_kind": "a probability measure over successor states",
        "determinism_branching_or_measure": "stochastic measure",
        "termination_completion_failure": "unbounded iteration unless an external observation horizon is chosen",
    },
    "generator": {
        "object_kind": "one-shot generator or static ensemble",
        "native_time": "not applicable to one-shot generation",
        "input": "generation parameters",
        "law_kind": "deterministic or probabilistic generation law",
        "result_kind": "a generated object or probability measure over generated objects",
        "successor_cardinality": "not applicable",
        "determinism_branching_or_measure": "fixed, parameterized, or probabilistic as stated",
        "termination_completion_failure": "generation completes when an object or ensemble measure is produced",
        "excluded_observers_and_representations": "statistics and rendered samples are not part of the generated object's native state",
    },
    "seed": {
        "object_kind": "initial-condition generator or preset family",
        "native_time": "not applicable to seed generation",
        "complete_state": "a generated or selected initial state",
        "seed": "the generated initial state is supplied to a separate evolution law",
        "law_kind": "generation, selection, or preset relation",
        "result_kind": "an initial state or probability measure over initial states",
        "determinism_branching_or_measure": "fixed preset, parameterized family, or probability measure as stated",
        "termination_completion_failure": "generation completes when an initial state is produced",
        "excluded_observers_and_representations": "subsequent evolved behavior is not part of the seed law",
    },
    "observer": {
        "object_kind": "observer, analyzer, or derived relation",
        "native_time": "not applicable unless the analyzer itself is iterated",
        "input": "a source object, history, configuration, or parameter tuple",
        "law_kind": "deterministic analysis or derived relation",
        "result_kind": "a derived value, decision, set, or representation",
        "successor_cardinality": "not applicable",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "returns a result when its stated computation or limit is defined",
        "excluded_observers_and_representations": "the analyzed system remains distinct from the analyzer",
    },
    "constraint": {
        "object_kind": "constraint, relation, or model set",
        "native_time": "not applicable",
        "law_kind": "declarative acceptance relation",
        "result_kind": "a satisfying model set, truth value, or accepted object",
        "successor_cardinality": "not applicable",
        "determinism_branching_or_measure": "all satisfying answers are admitted",
        "termination_completion_failure": "a query succeeds on a witness and fails when nonexistence is established",
        "witness_semantics": "a witness is any object satisfying the stated relation",
        "excluded_observers_and_representations": "enumeration order and display are not part of the relation",
    },
    "representation": {
        "object_kind": "representation or transformation",
        "native_time": "not applicable unless the transformation is explicitly iterated",
        "input": "a source object",
        "law_kind": "deterministic encoding or transformation",
        "result_kind": "a representation or transformed object",
        "successor_cardinality": "one",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "completes when the representation or transform is produced",
        "excluded_observers_and_representations": "the represented object remains distinct from its representation",
    },
}

PROFILE_NA: dict[str, set[str]] = {
    "ca1d": {
        "visible_history",
        "control_state",
        "seed",
        "input",
        "external_data",
        "parameters_and_variants",
        "witness_semantics",
    },
    "ca2d": {
        "visible_history",
        "control_state",
        "seed",
        "input",
        "external_data",
        "parameters_and_variants",
        "witness_semantics",
    },
    "map": {
        "visible_history",
        "control_state",
        "seed",
        "input",
        "boundary",
        "external_data",
        "read_dependencies_or_neighborhood",
        "parameters_and_variants",
        "witness_semantics",
    },
    "stochastic": {
        "visible_history",
        "control_state",
        "boundary",
        "external_data",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "parameters_and_variants",
        "witness_semantics",
    },
    "generator": {
        "native_time",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "parameters_and_variants",
        "witness_semantics",
    },
    "seed": {
        "native_time",
        "visible_history",
        "control_state",
        "input",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
        "parameters_and_variants",
        "witness_semantics",
    },
    "observer": {
        "native_time",
        "carrier",
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "complete_state",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "witness_semantics",
    },
    "constraint": {
        "native_time",
        "visible_history",
        "control_state",
        "seed",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
    },
    "representation": {
        "native_time",
        "carrier",
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "complete_state",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
        "parameters_and_variants",
        "witness_semantics",
    },
}


def ev(
    unit: str,
    modality: str,
    strength: str,
    claim: str,
    fields: list[str],
    image: str | None = None,
) -> dict[str, Any]:
    return {
        "unit": unit,
        "modality": modality,
        "strength": strength,
        "claim": claim,
        "fields": fields,
        "image": image,
    }


def spec(
    name: str,
    anchor: str,
    ordinal: int,
    profile: str,
    evidence: list[dict[str, Any]],
    *,
    values: dict[str, str] | None = None,
    aliases: list[str] | None = None,
    parameters: list[tuple[str, str]] | None = None,
    variants: list[tuple[str, str]] | None = None,
    missing: list[str] | None = None,
    status: str = "CLEAR",
    uncertainties: list[str] | None = None,
    image_witnesses: list[str] | None = None,
    related: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "anchor": anchor,
        "ordinal": ordinal,
        "profile": profile,
        "evidence": evidence,
        "values": values or {},
        "aliases": aliases or [],
        "parameters": parameters or [],
        "variants": variants or [],
        "missing": missing or [],
        "status": status,
        "uncertainties": uncertainties or [],
        "image_witnesses": image_witnesses or [],
        "related": related or [],
    }


CA_FIELDS = [
    "object_kind",
    "alphabet_or_value_schema",
    "read_dependencies_or_neighborhood",
    "law_kind",
    "rule_relation_constraint_function_or_probability_law",
    "result_kind",
    "determinism_branching_or_measure",
]
OBS_FIELDS = [
    "object_kind",
    "input",
    "law_kind",
    "rule_relation_constraint_function_or_probability_law",
    "result_kind",
]
CONSTRAINT_FIELDS = [
    "object_kind",
    "input",
    "law_kind",
    "rule_relation_constraint_function_or_probability_law",
    "result_kind",
    "witness_semantics",
]
SEED_FIELDS = [
    "object_kind",
    "carrier",
    "support",
    "complete_state",
    "seed",
    "result_kind",
]
MAP_FIELDS = [
    "object_kind",
    "native_time",
    "carrier",
    "complete_state",
    "rule_relation_constraint_function_or_probability_law",
    "result_kind",
    "determinism_branching_or_measure",
]


def candidate_specs() -> list[dict[str, Any]]:
    p = "BACK-MATTER/NOTES/"
    return [
        spec(
            "fair random cellular-automaton initial-condition ensemble",
            "U006341",
            1,
            "seed",
            [ev("U006341", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A random initial condition is assigned average black-cell density 1/2.", SEED_FIELDS + ["parameters_and_variants"])],
            values={
                "carrier": "a cellular-automaton cell array",
                "support": "random black/white configurations",
                "alphabet_or_value_schema": "black and white cells",
                "complete_state": "one random cell-color configuration",
                "rule_relation_constraint_function_or_probability_law": "the fair random ensemble has expected black-cell density 1/2",
            },
            aliases=["random initial condition"],
            parameters=[("black-cell probability", "1/2 in the stated fair ensemble")],
            missing=["The unit does not explicitly state independence or a finite-versus-infinite sampling boundary."],
        ),
        *[
            spec(
                f"elementary cellular automaton rule {number}",
                "U006344",
                ordinal,
                "ca1d",
                [ev("U006344", "FORMULA", "DIRECT_COMPLETE_MECHANICS", f"The algebraic local transition formula for rule {number} is stated explicitly.", CA_FIELDS)],
                values={
                    "alphabet_or_value_schema": "binary values modulo 2",
                    "read_dependencies_or_neighborhood": "left, center, and right values p, q, r",
                    "rule_relation_constraint_function_or_probability_law": formula,
                },
                aliases=[f"rule {number}"],
            )
            for ordinal, (number, formula) in enumerate(
                [
                    (22, "Mod[p+q+r+p q r, 2]"),
                    (126, "Mod[(p+q)(q+r)+(p+r), 2]"),
                    (150, "Mod[p+q+r, 2]"),
                    (182, "Mod[p r (1+q)+(p+q+r), 2]"),
                ],
                1,
            )
        ],
        spec(
            "cellular automaton with continual center-cell randomness injection",
            "U006346",
            1,
            "stochastic",
            [ev("U006346", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Starting from all white, a definite cellular-automaton step is accompanied at every step by a random change to the center cell.", ["object_kind", "native_time", "seed", "frontier_or_activation", "schedule", "law_kind", "rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure"])],
            values={
                "carrier": "a cellular-automaton cell array",
                "seed": "all cells white",
                "frontier_or_activation": "the ordinary CA frontier plus the center cell selected for random change",
                "rule_relation_constraint_function_or_probability_law": "apply a definite CA rule and randomly change the center-cell color at each step",
            },
            missing=["The probability distribution for the center-cell random change and its ordering relative to the deterministic update are not stated."],
            image_witnesses=[p + "_page_962_Picture_7.jpeg"],
        ),
        spec(
            "elementary-rule bit-pattern selector",
            "U006348",
            1,
            "constraint",
            [ev("U006348", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Accepted elementary rule numbers are exactly those whose eight base-2 digits match {_, i, _, j, i, _, j, 0}.", CONSTRAINT_FIELDS)],
            values={
                "input": "an elementary cellular-automaton rule number n",
                "rule_relation_constraint_function_or_probability_law": "IntegerDigits[n, 2, 8] matches {_, i, _, j, i, _, j, 0}",
            },
        ),
        spec(
            "three-color one-dimensional totalistic class-4 preset family",
            "U006348",
            2,
            "ca1d",
            [ev("U006348", "PROSE", "DIRECT_IDENTITY", "The note enumerates three-color totalistic rule codes that exhibit class-4 behavior.", ["object_kind", "alphabet_or_value_schema", "law_kind", "parameters_and_variants"])],
            values={
                "alphabet_or_value_schema": "three cell colors",
                "law_kind": "one-dimensional totalistic cellular-automaton rule",
                "parameters_and_variants": "codes 357, 438, 600, 792, 924, 1038, 1041, 1086, 1329, 1572, 1599, 1635, 1662, 1815, 2007, and 2049",
            },
            aliases=["1D totalistic class-4 rules"],
            missing=["The totalistic code-decoding convention, neighborhood range, and transition tables are not restated in this unit."],
        ),
        spec(
            "one-dimensional totalistic rule-class frequency survey",
            "U006348",
            3,
            "observer",
            [
                ev("U006348", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The survey groups one-dimensional totalistic cellular automata by behavior class for varying color count k and range r.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006349", "IMAGE", "CONTEXTUAL", "The original-resolution pie charts render the surveyed class frequencies for the displayed k and r cases.", ["result_kind", "parameters_and_variants"], p + "_page_963_Frequencies_of_Classes_Four_Pie_Charts.jpeg"),
            ],
            values={
                "input": "the finite one-dimensional totalistic rule space for specified color count k and range r",
                "rule_relation_constraint_function_or_probability_law": "classify each rule by observed behavior class and count the class proportions",
                "result_kind": "a bounded survey of behavior-class frequencies",
                "parameters_and_variants": "the k and r cases displayed in the four source pie charts",
            },
            missing=["The precise classification procedure and numeric chart values are not transcribed in prose."],
            image_witnesses=[p + "_page_963_Frequencies_of_Classes_Four_Pie_Charts.jpeg"],
        ),
        spec(
            "class-1 no-surviving-pattern decision query",
            "U006350",
            1,
            "constraint",
            [
                ev(
                    "U006350",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "A proposed class-1 test checks that no initial pattern of any size can survive; borderline cases can take arbitrarily long and the general classification problem can be undecidable.",
                    [
                        "object_kind",
                        "input",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                        "result_kind",
                        "termination_completion_failure",
                        "witness_semantics",
                    ],
                )
            ],
            values={
                "input": "a cellular-automaton rule",
                "rule_relation_constraint_function_or_probability_law": "accept the class-1 hypothesis only if no initial pattern of any size can survive",
                "result_kind": "a class-1 classification decision or an unresolved borderline case",
                "termination_completion_failure": "the search can take arbitrarily long and the general classification problem can be undecidable",
                "witness_semantics": "a surviving initial pattern refutes the no-surviving-pattern condition",
            },
            missing=["The source gives the decision criterion but no terminating general algorithm or formal survival threshold."],
        ),
        spec(
            "continuously parameterized cellular automaton family",
            "U006350",
            2,
            "ca1d",
            [ev("U006350", "PROSE", "DIRECT_IDENTITY", "Continuous cellular automata are delimited by rules whose parameters can be varied smoothly.", ["object_kind", "parameters_and_variants", "law_kind"])],
            values={
                "alphabet_or_value_schema": "continuous cell values",
                "parameters_and_variants": "smoothly variable rule parameters",
            },
            aliases=["continuous cellular automata"],
            missing=["The local state domain and transition formula are deferred to page 922."],
        ),
        spec(
            "larger-range cellular-automaton rule embedding transform",
            "U006350",
            3,
            "representation",
            [ev("U006350", "PROSE", "DIRECT_COMPLETE_MECHANICS", "A range-r rule is embedded at any larger range by making all cells farther than r irrelevant.", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"])],
            values={
                "input": "a range-r cellular-automaton rule and a larger target range",
                "rule_relation_constraint_function_or_probability_law": "extend the transition table so cells at distances greater than r have no effect",
                "result_kind": "an equivalent rule expressed at the larger target range",
                "parameters_and_variants": "the source range r and the larger target range",
            },
        ),
        spec(
            "edge-local cellular-automaton rule-nearness relation",
            "U006350",
            4,
            "constraint",
            [ev("U006350", "PROSE", "DIRECT_PARTIAL_MECHANICS", "At a common enlarged range, nearby rules are defined by differences involving only cells close to the neighborhood edge.", CONSTRAINT_FIELDS)],
            values={
                "input": "two cellular-automaton rules represented at a common enlarged range",
                "rule_relation_constraint_function_or_probability_law": "the rules differ only through cells close to the edge of that common range",
                "result_kind": "whether the two rules satisfy the stated edge-local nearness relation",
                "witness_semantics": "a witness identifies the rule-table differences and shows that their dependencies are confined near the range edge",
                "parameters_and_variants": "common representation range and the source's qualitative edge-nearness threshold",
            },
            missing=["The source does not quantify how many cells count as close to the edge."],
            related=["larger-range cellular-automaton rule embedding transform"],
        ),
        spec(
            "nine-neighbor outer-totalistic two-dimensional class-4 preset family",
            "U006350",
            5,
            "ca2d",
            [ev("U006350", "PROSE", "DIRECT_IDENTITY", "The note identifies nine-neighbor outer-totalistic codes 224, 226, 4320, 5344, 6248, 6752, 6754, and 8416 as class-4 examples.", ["object_kind", "topology", "read_dependencies_or_neighborhood", "parameters_and_variants"])],
            values={
                "topology": "two-dimensional lattice",
                "read_dependencies_or_neighborhood": "nine-neighbor outer-totalistic neighborhood",
                "parameters_and_variants": "codes 224, 226, 4320, 5344, 6248, 6752, 6754, and 8416",
            },
            aliases=["2D class 4 outer-totalistic rules"],
            variants=[("HighLife", "the source's name for member preset code 4320")],
            missing=["The code-to-transition-table convention is not restated in this unit."],
        ),
        spec(
            "Game of Life cellular automaton",
            "U006351",
            1,
            "ca2d",
            [
                ev("U006351", "PROSE", "DIRECT_IDENTITY", "The Life two-dimensional cellular automaton is named and its step implementation introduced.", ["object_kind", "carrier", "topology", "alphabet_or_value_schema", "complete_state"]),
                ev("U006352", "CODE", "DIRECT_COMPLETE_MECHANICS", "LifeStep counts the 3x3 neighborhood including self and returns black for a live cell at total 4 or any cell at total 3.", ["frontier_or_activation", "schedule", "read_dependencies_or_neighborhood", "rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit", "result_kind", "determinism_branching_or_measure"]),
                ev("U006353", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The same Life state can be represented sparsely as the list of live-cell positions.", ["complete_state", "parameters_and_variants"]),
                ev("U006354", "CODE", "CORROBORATING", "The sparse implementation produces births at multiplicity 3 and retains live positions at multiplicity 4.", ["rule_relation_constraint_function_or_probability_law"]),
                ev("U006355", "PROSE", "CORROBORATING", "A further implementation variant finds runs of length 3 and 4 in the sorted sparse-neighborhood list.", ["parameters_and_variants"]),
            ],
            values={
                "alphabet_or_value_schema": "binary live/dead cells",
                "complete_state": "the complete binary lattice configuration, represented densely or by the list of live-cell positions",
                "read_dependencies_or_neighborhood": "the 3x3 Moore neighborhood including self",
                "rule_relation_constraint_function_or_probability_law": "live survives with 2 or 3 live neighbors; dead is born with 3 live neighbors",
                "parameters_and_variants": "dense-array, sparse live-position, and sorted-run implementations",
            },
            aliases=["Life", "code 224"],
            variants=[
                ("dense array", "count the 3x3 neighborhood at every array position"),
                ("sparse live-position list", "count coincident translated live positions"),
                ("sorted-run optimization", "find runs of multiplicity 3 and 4 in the sorted sparse list"),
            ],
        ),
        spec(
            "three-dimensional Life-like cellular automaton family",
            "U006356",
            1,
            "ca2d",
            [
                ev("U006356", "PROSE", "DIRECT_IDENTITY", "A cubic-lattice three-dimensional Life-like family is introduced.", ["object_kind", "carrier", "topology"]),
                ev("U006357", "CODE", "DIRECT_COMPLETE_MECHANICS", "LifeStep3D counts the 26 neighboring cells and applies survival interval p..q or birth count r synchronously.", ["alphabet_or_value_schema", "complete_state", "schedule", "read_dependencies_or_neighborhood", "law_kind", "rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit", "result_kind"]),
                ev("U006358", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source enumerates {5,7,6}, {4,5,5}, and {5,6,5}, and identifies the pictured moving structure with the second preset.", ["parameters_and_variants"]),
            ],
            values={
                "object_kind": "three-dimensional cellular automaton",
                "carrier": "a cubic lattice of cells",
                "topology": "three-dimensional cubic-lattice adjacency",
                "alphabet_or_value_schema": "binary live/dead cells",
                "read_dependencies_or_neighborhood": "the 26 cells in the surrounding 3x3x3 cube",
                "rule_relation_constraint_function_or_probability_law": "a live cell survives when p <= neighbor count <= q; any cell is live when neighbor count == r",
                "parameters_and_variants": "{p,q,r}, including {5,7,6}, {4,5,5}, and {5,6,5}",
            },
            parameters=[
                ("p", "minimum neighbor count for survival"),
                ("q", "maximum neighbor count for survival"),
                ("r", "neighbor count for birth"),
            ],
            variants=[
                ("{5,7,6}", "source-enumerated three-dimensional Life-like preset"),
                ("{4,5,5}", "source-enumerated preset used by the pictured moving structure"),
                ("{5,6,5}", "source-enumerated three-dimensional Life-like preset"),
            ],
            image_witnesses=[p + "_page_964_Picture_11.jpeg"],
        ),
        spec(
            "random infinite-sequence initial-condition generator",
            "U006360",
            1,
            "seed",
            [ev("U006360", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Systems whose initial states contain an infinite element sequence can take that sequence at random, while a mobile head retains a definite initial location.", SEED_FIELDS + ["parameters_and_variants"])],
            values={
                "carrier": "an infinite sequence of cells, symbols, or digits",
                "support": "infinite initial sequences compatible with the target system",
                "alphabet_or_value_schema": "the target system's cell, symbol, or digit alphabet",
                "complete_state": "a sampled infinite sequence plus any required definite active location",
                "rule_relation_constraint_function_or_probability_law": "choose the sequence elements at random while preserving required finite control data",
            },
            variants=[
                ("random tape colors", "mobile automata and Turing machines keep a definite active-cell location"),
                ("random substitution input", "ordinary substitution systems can consume an infinite random sequence"),
                ("random real-number digits", "continuous-number systems expose an infinite random digit sequence"),
            ],
            missing=["No single probability distribution is specified for the general family."],
        ),
        spec(
            "cellular-automaton difference-pattern observer",
            "U006364",
            1,
            "representation",
            [
                ev("U006364", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A difference region records cells affected by an initial change, and its edge can move by at most the underlying cellular-automaton range per step.", ["object_kind", "input", "result_kind", "structural_invariants"]),
                ev("U006365", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source compares two cellular-automaton evolutions through their cellwise pattern of differences.", ["law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind"]),
            ],
            values={
                "input": "two initial conditions or histories of a cellular automaton",
                "structural_invariants": "the difference-region edge can propagate no faster than r cells per step for a range-r rule",
                "rule_relation_constraint_function_or_probability_law": "compare the two evolutions cell by cell and mark where their colors differ",
                "result_kind": "a spacetime pattern of changed cells",
            },
            related=["two-k-color cellular-automaton difference-emulation lift"],
        ),
        spec(
            "two-k-color cellular-automaton difference-emulation lift",
            "U006365",
            1,
            "representation",
            [
                ev(
                    "U006365",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "For a k-color rule, the difference pattern between two initial conditions can be reproduced by one initial condition of a suitable 2k-color cellular automaton.",
                    [
                        "object_kind",
                        "input",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                        "result_kind",
                        "parameters_and_variants",
                    ],
                )
            ],
            values={
                "input": "a k-color cellular automaton and a pair of its initial conditions",
                "rule_relation_constraint_function_or_probability_law": "encode the pair into one initial condition of a suitable 2k-color rule whose evolution reproduces their difference pattern",
                "result_kind": "a 2k-color cellular automaton and encoded initial state reproducing the pairwise difference history",
                "parameters_and_variants": "source alphabet size k and lifted alphabet size 2k",
            },
            parameters=[("k", "number of colors in the source cellular automaton; the lifted rule has 2k colors")],
            missing=["The source asserts existence but does not give the state-pair encoding or the lifted transition table."],
            related=["cellular-automaton difference-pattern observer"],
        ),
        spec(
            "cellular-automaton perturbation-growth Lyapunov analyzer",
            "U006367",
            1,
            "observer",
            [ev("U006367", "PROSE", "DIRECT_COMPLETE_MECHANICS", "The speed at which the region of differences expands is taken as a Lyapunov exponent characterizing instability.", OBS_FIELDS)],
            values={
                "input": "a cellular automaton and a localized initial perturbation",
                "rule_relation_constraint_function_or_probability_law": "measure the asymptotic speed of the expanding difference-region edge",
                "result_kind": "a perturbation-growth speed interpreted as a Lyapunov exponent",
            },
        ),
        spec(
            "cyclic addition dot system",
            "U006369",
            1,
            "map",
            [
                ev("U006369", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "After t steps the dot is at Mod[m t,n], with repetition period n/GCD[m,n].", MAP_FIELDS + ["structural_invariants"]),
                ev("U006370", "PROSE", "CORROBORATING", "The period is maximal exactly when m/n is in lowest terms.", ["structural_invariants"]),
            ],
            values={
                "carrier": "n cyclic positions",
                "complete_state": "the current dot position",
                "structural_invariants": "the repetition period is n/GCD[m,n], and it is maximal at n exactly when GCD[m,n]=1",
                "rule_relation_constraint_function_or_probability_law": "x -> Mod[x+m,n]",
                "parameters_and_variants": "n positions and step size m",
            },
            image_witnesses=[p + "_page_965_Figure_8.jpeg"],
        ),
        spec(
            "cyclic multiplication dot system",
            "U006372",
            1,
            "map",
            [ev("U006372", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "After t steps the dot is at Mod[k^t,n]; coprime k,n give return period MultiplicativeOrder[k,n], while powers n=k^s reach the absorbing state 0 after s steps.", MAP_FIELDS + ["structural_invariants"])],
            values={
                "carrier": "n cyclic residue positions",
                "complete_state": "the current dot position",
                "structural_invariants": "when GCD[k,n]=1 the return period is MultiplicativeOrder[k,n], which divides EulerPhi[n], and position 0 is unreachable; when n=k^s, 0 is reached after s steps and is absorbing",
                "rule_relation_constraint_function_or_probability_law": "x -> Mod[k x,n], starting from 1",
                "parameters_and_variants": "modulus n and multiplier k",
            },
        ),
        spec(
            "primitive spatial-period state-count function",
            "U006373",
            1,
            "observer",
            [
                ev("U006373", "PROSE", "DIRECT_IDENTITY", "The number s[m,k] counts k-color states of minimum spatial period m.", ["object_kind", "input", "result_kind"]),
                ev("U006374", "CODE", "DIRECT_COMPLETE_MECHANICS", "s[m,k] is defined recursively by subtracting counts for proper divisors from k^m.", ["law_kind", "rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure"]),
                ev("U006375", "PROSE", "CORROBORATING", "The source introduces an equivalent closed divisor-sum form for the same primitive-period count.", ["rule_relation_constraint_function_or_probability_law"]),
                ev("U006376", "CODE", "DIRECT_COMPLETE_MECHANICS", "The equivalent implementation sums MoebiusMu[m/d] k^d over divisors d of m.", ["rule_relation_constraint_function_or_probability_law"]),
                ev("U006377", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For an n-cell cyclic system the count s[n,k] bounds the maximum temporal cycle and is divisible by n; for prime n it equals k^n-k.", ["structural_invariants", "result_kind"]),
            ],
            values={
                "input": "spatial period m and alphabet size k",
                "structural_invariants": "s[m,k] counts states of primitive spatial period m; s[n,k] is divisible by n, and for prime n equals k^n-k",
                "rule_relation_constraint_function_or_probability_law": "s[m,k] = k^m - Sum[s[d,k] for proper divisors d of m], equivalently Sum[MoebiusMu[m/d] k^d for d dividing m]",
                "result_kind": "the number of states with minimum spatial period m",
            },
        ),
        spec(
            "finite cyclic rule-60 polynomial cellular automaton",
            "U006378",
            1,
            "ca1d",
            [
                ev("U006378", "PROSE", "DIRECT_IDENTITY", "Finite cyclic rule 60 is represented by binary state polynomials.", ["object_kind", "topology", "alphabet_or_value_schema", "boundary", "read_dependencies_or_neighborhood"]),
                ev("U006379", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The t-step state is PolynomialMod[(1+x)^t z,{x^n-1,2}], fixing binary cyclic evolution.", ["native_time", "complete_state", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "determinism_branching_or_measure"]),
            ],
            values={
                "topology": "a cyclic one-dimensional lattice of n cells",
                "alphabet_or_value_schema": "binary coefficients modulo 2",
                "boundary": "cyclic, encoded by x^n-1",
                "read_dependencies_or_neighborhood": "the current cell and one adjacent cell, represented by multiplication by 1+x",
                "rule_relation_constraint_function_or_probability_law": "z -> PolynomialMod[(1+x) z,{x^n-1,2}]",
            },
            aliases=["rule 60 with cyclic boundary conditions"],
        ),
        spec(
            "finite cyclic rule-60 repetition-period bound function",
            "U006380",
            1,
            "observer",
            [
                ev("U006380", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "For odd n the repetition period divides p[n]=2^MultiplicativeOrder[2,n]-1, which is at most 2^(n-1)-1.", OBS_FIELDS + ["structural_invariants"]),
                ev("U006381", "TABLE", "DIRECT_PARTIAL_MECHANICS", "The table gives ratios by which actual periods fall below p[n] for ten stated sizes.", ["parameters_and_variants", "result_kind"]),
                ev("U006382", "PROSE", "CORROBORATING", "The note reports no n>5 case attaining the absolute maximum 2^(n-1)-1.", ["structural_invariants"]),
            ],
            values={
                "input": "an odd cyclic ring size n for rule 60",
                "structural_invariants": "the actual repetition period divides p[n], and p[n] is at most 2^(n-1)-1",
                "rule_relation_constraint_function_or_probability_law": "p[n]=2^MultiplicativeOrder[2,n]-1",
                "result_kind": "a source-stated divisibility bound for the repetition period",
                "parameters_and_variants": "the source table records actual-period divisors for n=11,13,19,25,27,29,37,41,43,53",
            },
            parameters=[("n", "odd cyclic ring size")],
            related=["finite cyclic rule-60 polynomial cellular automaton"],
        ),
        spec(
            "finite cyclic rule-90 polynomial cellular automaton",
            "U006383",
            1,
            "ca1d",
            [ev("U006383", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The rule-60 polynomial analysis is repeated with 1/x+x at each step for cyclic rule 90.", CA_FIELDS)],
            values={
                "topology": "a cyclic one-dimensional lattice of odd n cells in the stated analysis",
                "alphabet_or_value_schema": "binary coefficients modulo 2",
                "boundary": "cyclic",
                "read_dependencies_or_neighborhood": "left and right neighbors, represented by 1/x+x",
                "rule_relation_constraint_function_or_probability_law": "multiply the state polynomial by 1/x+x modulo x^n-1 and 2",
            },
            aliases=["rule 90 with cyclic boundary conditions"],
        ),
        spec(
            "finite cyclic rule-90 repetition-period bound function",
            "U006384",
            1,
            "observer",
            [
                ev("U006383", "PROSE", "DIRECT_IDENTITY", "The cyclic rule-90 period analysis replaces the rule-60 factor 1+x by 1/x+x.", ["object_kind", "input"]),
                ev("U006384", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "For odd n the rule-90 repetition period divides q[n]=2^MultiplicativeOrder[2,n,{1,-1}]-1.", ["law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "structural_invariants"]),
                ev("U006385", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The exponent is bounded above by (n-1)/2, and the period usually equals q[n], with the first stated exception at n=37.", ["structural_invariants", "parameters_and_variants"]),
            ],
            values={
                "input": "an odd cyclic ring size n for rule 90",
                "structural_invariants": "the actual period divides q[n]; its exponent is at most (n-1)/2, with equality only possible for prime n",
                "rule_relation_constraint_function_or_probability_law": "q[n]=2^MultiplicativeOrder[2,n,{1,-1}]-1",
                "result_kind": "a source-stated divisibility bound and typical period prediction",
                "parameters_and_variants": "period usually equals q[n]; the first stated exception is n=37",
            },
            parameters=[("n", "odd cyclic ring size")],
            related=["finite cyclic rule-90 polynomial cellular automaton"],
        ),
        spec(
            "finite-ring cellular-automaton repetition-period comparison survey",
            "U006386",
            1,
            "observer",
            [
                ev("U006386", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The survey compares finite-ring repetition periods for rules 45, 30, and 60 and their conjugates/reflections as the ring size n varies.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006387", "IMAGE", "CONTEXTUAL", "The original-resolution figure renders the stated period comparison as a function of n.", ["result_kind", "parameters_and_variants"], p + "_page_966_Figure_12.jpeg"),
            ],
            values={
                "input": "a selected elementary cellular-automaton rule and finite cyclic size n",
                "rule_relation_constraint_function_or_probability_law": "measure or compute the repetition period and compare it across the displayed rules as n varies",
                "result_kind": "a bounded rule-by-size repetition-period comparison",
                "parameters_and_variants": "rules 45, 30, and 60 together with conjugates and reflections",
            },
            missing=["The figure's numeric series are not independently transcribed in the adjacent prose."],
            image_witnesses=[p + "_page_966_Figure_12.jpeg"],
        ),
        spec(
            "finite cellular-automaton boundary implementation codec",
            "U006388",
            1,
            "representation",
            [ev("U006388", "CODE", "DIRECT_PARTIAL_MECHANICS", "Fixed-width zero boundaries are implemented by BitAnd[a,2^n-1] after each bitwise step, while cyclic boundaries use cyclic-shift instructions.", ["object_kind", "input", "boundary", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"])],
            values={
                "input": "a bitwise cellular-automaton state integer a, width n, and boundary mode",
                "boundary": "fixed outside-zero or cyclic finite boundary",
                "rule_relation_constraint_function_or_probability_law": "mask each fixed-zero step with BitAnd[a,2^n-1], or implement cyclic neighbor access with cyclic shifts",
                "result_kind": "a finite-width state representation with the selected boundary semantics",
                "parameters_and_variants": "fixed-width outside-zero masking and cyclic-shift boundary implementation",
            },
            missing=["The assembler instruction sequence for cyclic boundaries is not supplied."],
            related=["finite cyclic rule-60 polynomial cellular automaton", "finite cyclic rule-90 polynomial cellular automaton"],
        ),
        spec(
            "rule-22 randomness-producing seed family",
            "U006390",
            1,
            "seed",
            [
                ev(
                    "U006390",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "Rule 22 yields randomness from two black cells separated by 4^m positions for m>=2 and from the binary digit sequences of an enumerated integer family.",
                    SEED_FIELDS + ["parameters_and_variants"],
                )
            ],
            values={
                "carrier": "a one-dimensional binary rule-22 configuration",
                "support": "two-black-cell separation seeds and the source's enumerated binary-integer seeds",
                "alphabet_or_value_schema": "black and white cells",
                "complete_state": "one selected finite rule-22 initial pattern on a white background",
                "rule_relation_constraint_function_or_probability_law": "choose either two black cells 4^m positions apart for m>=2 or the base-2 digit sequence of a listed integer",
                "parameters_and_variants": "m>=2; listed integers begin 19,25,37,39,41,45,47,51,57,61,...",
            },
            parameters=[("m", "integer exponent m>=2 in the two-cell separation 4^m")],
            variants=[
                ("power-of-four separation", "two black cells 4^m positions apart for m>=2"),
                ("binary-integer presets", "base-2 digit sequences for 19,25,37,39,41,45,47,51,57,61,..."),
            ],
            missing=["The integer list is explicitly open-ended, and the source does not state a fixed-width or leading-zero convention for its binary seed encoding."],
            related=["elementary cellular automaton rule 22"],
        ),
        spec(
            "elementary cellular automaton rule 225",
            "U006390",
            2,
            "ca1d",
            [ev("U006390", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Rule 225 is stated as not-p XOR (q OR r), with explicit finite seed variants.", CA_FIELDS + ["parameters_and_variants"])],
            values={
                "alphabet_or_value_schema": "binary values",
                "read_dependencies_or_neighborhood": "left, center, and right values p,q,r",
                "rule_relation_constraint_function_or_probability_law": "not p XOR (q OR r)",
            },
            variants=[
                ("single-black-cell seed", "yields a regular nested pattern"),
                ("■■□■ seed", "yields a complicated pattern"),
                ("white defect in repeated ■□ background", "yields an expanding random region"),
            ],
            image_witnesses=[p + "_page_966_Figure_17.jpeg"],
        ),
        spec(
            "elementary cellular automaton rule 94",
            "U006392",
            1,
            "ca1d",
            [ev("U006392", "PROSE", "DIRECT_IDENTITY", "Rule 94 is a finite rule-number specification whose appropriate initial conditions yield nested and random behavior.", ["object_kind", "parameters_and_variants"])],
            values={
                "parameters_and_variants": "the note distinguishes initial conditions yielding nested behavior from those yielding random behavior",
            },
            aliases=["rule 94"],
            missing=["The local transition formula and the pictured initial-condition encodings are not transcribed in prose."],
            image_witnesses=[p + "_page_966_Figure_19.jpeg"],
        ),
        spec(
            "elementary cellular automaton rule 218",
            "U006394",
            1,
            "ca1d",
            [ev("U006394", "PROSE", "DIRECT_IDENTITY", "Rule 218 is identified by rule number and its response to initial conditions with or without adjacent black pairs.", ["object_kind", "parameters_and_variants"])],
            values={
                "parameters_and_variants": "initial conditions with adjacent black pairs versus initial conditions without them",
            },
            aliases=["rule 218"],
            missing=["The local transition formula is not stated."],
        ),
        spec(
            "weighted additive cellular automaton family",
            "U006395",
            1,
            "ca1d",
            [
                ev("U006394", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source enumerates the eight additive elementary rules {0,60,90,102,150,170,204,240} and groups them as trivial or equivalent to rules 90 or 150.", ["parameters_and_variants", "structural_invariants"]),
                ev("U006395", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Every k-color range-r additive rule sums neighborhood values modulo k using position weights.", ["object_kind", "alphabet_or_value_schema", "read_dependencies_or_neighborhood", "law_kind", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"]),
                ev("U006397", "PROSE", "CONTEXTUAL", "The source introduces the implementation of one complete weighted-additive step.", []),
                ev("U006398", "CODE", "DIRECT_COMPLETE_MECHANICS", "One synchronous step is Mod[ListCorrelate[w,list,Ceiling[Length[w]/2]],k].", ["complete_state", "schedule", "rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit", "result_kind", "determinism_branching_or_measure"]),
            ],
            values={
                "alphabet_or_value_schema": "values modulo k",
                "structural_invariants": "the eight additive elementary rules are 0, 60, 90, 102, 150, 170, 204, and 240; each is trivial or essentially equivalent to rule 90 or 150",
                "read_dependencies_or_neighborhood": "2r+1 cells with weights w",
                "rule_relation_constraint_function_or_probability_law": "new cell = Mod[weighted sum of neighborhood values,k]",
                "parameters_and_variants": "alphabet size k, range r, and weights w in 0..k-1",
            },
            parameters=[
                ("k", "number of cell colors and modulus"),
                ("r", "cellular-automaton range"),
                ("w", "the 2r+1 position weights, each in 0..k-1"),
            ],
            variants=[("additive elementary rules", "{0,60,90,102,150,170,204,240}")],
            image_witnesses=[p + "_page_967_Picture_4.jpeg"],
        ),
        spec(
            "generalized-additive monoid cellular automaton family",
            "U006400",
            1,
            "ca1d",
            [
                ev("U006400", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Generalized additivity combines evolution histories using an operation ⊕.", ["object_kind", "law_kind"]),
                ev("U006401", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Generalized additivity requires phi[u⊕v] == phi[u]⊕phi[v].", ["rule_relation_constraint_function_or_probability_law"]),
                ev("U006402", "PROSE", "CORROBORATING", "The property is a homomorphism condition and ordinary modulo-k addition supplies the standard Xor example.", ["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"]),
                ev("U006404", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Rule 250 supplies the Max/Or generalized-additive variant.", ["parameters_and_variants"]),
                ev("U006406", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source requires an associative, commutative operation with identity to obtain the familiar additive construction from basic histories.", ["structural_invariants"]),
                ev("U006407", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source enumerates counts of inequivalent commutative monoids by color count k.", ["parameters_and_variants"]),
                ev("U006409", "TABLE", "DIRECT_PARTIAL_MECHANICS", "The source tabulates numbers of rules additive over each commutative monoid for stated k and r cases.", ["parameters_and_variants"]),
                ev("U006410", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Every such local rule applies monoid endomorphisms sigma to neighborhood cells and combines the results with ⊕.", ["alphabet_or_value_schema", "read_dependencies_or_neighborhood", "write_replacement_assembly_or_commit", "parameters_and_variants"]),
            ],
            values={
                "structural_invariants": "⊕ is associative, commutative, and has an identity element",
                "alphabet_or_value_schema": "elements of a commutative monoid",
                "read_dependencies_or_neighborhood": "a finite neighborhood with a monoid endomorphism at each position",
                "rule_relation_constraint_function_or_probability_law": "phi combines sigma_i[cell_i] using ⊕ and obeys phi[u⊕v]=phi[u]⊕phi[v]",
            },
            parameters=[
                ("k", "number of monoid elements or cell colors"),
                ("r", "cellular-automaton range"),
                ("⊕", "commutative-monoid operation"),
                ("σ", "position-specific monoid endomorphisms"),
            ],
            variants=[("Xor-additive", "ordinary addition modulo k"), ("Or-additive", "Max/Or, exemplified by rule 250")],
            image_witnesses=[
                p + "_page_967_Rule_90_Generalized_Additivity_Four_Panel_Row.jpeg",
                p + "_page_967_Rule_250_Generalized_Additivity_Four_Panel_Row.jpeg",
                p + "_page_967_Picture_22.jpeg",
            ],
        ),
        spec(
            "integer- or real-valued linear cellular automaton family",
            "U006412",
            1,
            "ca1d",
            [ev("U006412", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "For integer or real cell values, ordinary-additive cellular-automaton rules are linear forms such as ax+by.", CA_FIELDS + ["parameters_and_variants"])],
            values={
                "alphabet_or_value_schema": "integer or real cell values",
                "read_dependencies_or_neighborhood": "the finite set of cells appearing in the linear form",
                "rule_relation_constraint_function_or_probability_law": "a linear form such as a x + b y",
                "parameters_and_variants": "integer-valued or real-valued cells with coefficients such as a and b",
            },
            parameters=[("linear coefficients", "coefficients such as a and b in the local linear form")],
            variants=[
                ("integer-valued linear CA", "cell values and the linear form are over integers"),
                ("real-valued linear CA", "cell values and coefficients are real"),
            ],
            related=["Cauchy-additive function constraint"],
        ),
        spec(
            "Cauchy-additive function constraint",
            "U006412",
            2,
            "constraint",
            [
                ev(
                    "U006412",
                    "FORMULA",
                    "DIRECT_PARTIAL_MECHANICS",
                    "A real function sigma is admitted when sigma[x+y]=sigma[x]+sigma[y]; continuity forces sigma[x]=c x, while the source describes nonconstructive discontinuous possibilities under the Axiom of Choice.",
                    CONSTRAINT_FIELDS + ["parameters_and_variants", "termination_completion_failure"],
                )
            ],
            values={
                "carrier": "real-valued functions sigma",
                "input": "a candidate function sigma over real values",
                "rule_relation_constraint_function_or_probability_law": "sigma[x+y] == sigma[x] + sigma[y] for all real x and y",
                "result_kind": "the class of Cauchy-additive functions",
                "witness_semantics": "a satisfying function obeys the additive equation for every pair x,y",
                "parameters_and_variants": "continuous solutions sigma[x]=c x; discontinuous solutions require nonconstructive choices across rational-equivalence classes",
                "termination_completion_failure": "the source states that the exotic discontinuous solutions are not explicitly constructible by a real computational system",
            },
            parameters=[("c", "constant slope for each continuous solution sigma[x]=c x")],
            variants=[
                ("continuous solution", "sigma[x]=c x"),
                ("discontinuous Axiom-of-Choice solution", "different slopes on distinct rational-equivalence classes; source gives no explicit construction"),
            ],
            missing=["No explicit discontinuous solution or computational construction is supplied."],
            related=["integer- or real-valued linear cellular automaton family"],
        ),
        spec(
            "irrational-modulus additive cellular automaton",
            "U006413",
            1,
            "ca1d",
            [ev("U006413", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "A cellular automaton based on Mod[x+y,pi] is explicitly given as additive over numbers modulo an irrational.", CA_FIELDS)],
            values={
                "alphabet_or_value_schema": "real values modulo pi",
                "read_dependencies_or_neighborhood": "two neighboring values x and y",
                "rule_relation_constraint_function_or_probability_law": "Mod[x+y,pi]",
            },
        ),
        spec(
            "local linear differential-operator function evolution",
            "U006413",
            2,
            "map",
            [ev("U006413", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For states that are continuous functions of position, a continuous local linear mapping must be a linear differential operator involving Derivative[n].", MAP_FIELDS)],
            values={
                "carrier": "continuous functions of position",
                "complete_state": "one continuous spatial function",
                "rule_relation_constraint_function_or_probability_law": "apply a local linear differential operator built from derivatives Derivative[n]",
                "result_kind": "a successor continuous function",
            },
            missing=["The operator coefficients, derivative orders, domain, and boundary conditions are not fixed."],
        ),
        spec(
            "independent-cell mean-field density map for cellular automata",
            "U006414",
            1,
            "observer",
            [
                ev("U006414", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "Assuming independent cell colors at density p gives product probabilities for every neighborhood.", ["object_kind", "input", "law_kind", "parameters_and_variants"]),
                ev("U006415", "CODE", "DIRECT_COMPLETE_MECHANICS", "The code constructs the eight three-cell neighborhood probabilities as products of p and 1-p.", ["rule_relation_constraint_function_or_probability_law"]),
                ev("U006416", "PROSE", "CORROBORATING", "The next density is obtained by weighting the rule table with those neighborhood probabilities.", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
                ev("U006417", "CODE", "DIRECT_COMPLETE_MECHANICS", "The next density is probs . IntegerDigits[m,2,8], and repeated application gives the approximation trajectory.", ["rule_relation_constraint_function_or_probability_law", "result_kind", "determinism_branching_or_measure"]),
                ev("U006418", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Rule 22 gives 3p(1-p)^2 at one-step order, with larger-block multi-step approximations accounting for correlations.", ["parameters_and_variants", "result_kind"]),
            ],
            values={
                "native_time": "discrete iterations of the density approximation",
                "input": "current density p and elementary rule number m",
                "rule_relation_constraint_function_or_probability_law": "form independent neighborhood probabilities and dot them with the rule table",
                "result_kind": "the approximated next-step density",
                "parameters_and_variants": "approximation order controls the neighborhood-block size and number of cellular-automaton steps used to retain correlations",
            },
            parameters=[("approximation order", "one-step independence or a larger-block multi-step correlation approximation")],
            variants=[("one-step independence", "8 neighborhoods"), ("multi-step correlation approximation", "larger blocks over two or more CA steps")],
            image_witnesses=[p + "_page_968_Figure_9.jpeg", p + "_page_968_Figure_10.jpeg"],
        ),
        spec(
            "rule-90 density evolution function",
            "U006424",
            1,
            "observer",
            [
                ev("U006424", "PROSE", "DIRECT_IDENTITY", "An exact density-after-t function for rule 90 is introduced.", ["object_kind", "input", "result_kind"]),
                ev("U006425", "FORMULA", "DEFECT_LIMITED", "The extracted formula has a parenthesis placement that does not preserve the prose dependence on DigitCount in the expected way.", ["law_kind", "rule_relation_constraint_function_or_probability_law"]),
            ],
            values={
                "input": "initial density p and step t",
                "rule_relation_constraint_function_or_probability_law": "the source prints 1/2 (1-(1-2p))^(2^DigitCount[t,2,1]), but the grouping is defective",
                "result_kind": "black-cell density after t rule-90 steps",
            },
            status="DEFECTIVE",
            uncertainties=["The bundled extraction does not determine the intended parenthesization of the density formula."],
            missing=["A trustworthy transcription of the intended exponent and outer parentheses is required."],
        ),
        spec(
            "cellular-automaton density-response raster analyzer",
            "U006426",
            1,
            "observer",
            [
                ev("U006426", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For each initial density, the analyzer follows density on successive steps and encodes it by gray level, with initial density across and time down.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006428", "IMAGE", "CONTEXTUAL", "The original-resolution figure renders the stated density-response rasters for rules 236, 126, and 30.", ["result_kind", "parameters_and_variants"], p + "_page_969_Figure_2.jpeg"),
            ],
            values={
                "input": "a cellular-automaton rule, a range of initial densities, and an evolution horizon",
                "rule_relation_constraint_function_or_probability_law": "for each initial-density ensemble, measure density at successive steps and encode each density as a gray level",
                "result_kind": "a density-response raster indexed horizontally by initial density and vertically by step",
                "parameters_and_variants": "the source displays rule 236, rule 126, and rule 30",
            },
            image_witnesses=[p + "_page_969_Figure_2.jpeg"],
        ),
        spec(
            "rule-73 fair-random initial-condition ensemble",
            "U006429",
            1,
            "seed",
            [ev("U006429", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source applies rule 73 to completely random binary initial conditions.", SEED_FIELDS)],
            values={
                "carrier": "a one-dimensional binary cellular-automaton configuration",
                "support": "completely random binary initial conditions",
                "alphabet_or_value_schema": "black and white cells",
                "complete_state": "one random rule-73 initial configuration",
                "rule_relation_constraint_function_or_probability_law": "sample a completely random binary initial configuration for rule 73",
            },
            missing=["The source does not separately restate independence, finite extent, or the black-cell probability of the completely random ensemble."],
            related=["fair random cellular-automaton initial-condition ensemble", "rule-73 period-3 density-oscillation analyzer"],
        ),
        spec(
            "rule-73 no-even-black-block initial-condition filter",
            "U006429",
            2,
            "constraint",
            [ev("U006429", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The restricted rule-73 initial-condition class forbids blocks containing even numbers of black cells; under this restriction the density oscillation disappears.", CONSTRAINT_FIELDS)],
            values={
                "carrier": "one-dimensional binary initial configurations",
                "alphabet_or_value_schema": "black and white cells",
                "input": "a binary rule-73 initial configuration",
                "rule_relation_constraint_function_or_probability_law": "accept only configurations containing no block of an even number of black cells in the source's stated sense",
                "result_kind": "membership in the restricted initial-condition class, or that constrained class itself",
                "witness_semantics": "an accepted configuration has no forbidden even-black block",
            },
            missing=["The prose does not formalize block boundaries or provide a constructive sampler for the restricted class."],
            related=["rule-73 fair-random initial-condition ensemble", "rule-73 period-3 density-oscillation analyzer"],
        ),
        spec(
            "rule-73 period-3 density-oscillation analyzer",
            "U006429",
            3,
            "observer",
            [
                ev("U006429", "PROSE", "DIRECT_PARTIAL_MECHANICS", "From completely random initial conditions, rule 73 forms independent regions containing period-3 patterns and its aggregate density continues to oscillate with period 3.", OBS_FIELDS + ["structural_invariants", "excluded_observers_and_representations"]),
                ev("U006430", "IMAGE", "CONTEXTUAL", "The original-resolution picture renders the region structure accompanying the stated period-3 density behavior.", ["result_kind", "excluded_observers_and_representations"], p + "_page_969_Picture_4.jpeg"),
            ],
            values={
                "input": "a rule-73 history generated from the stated random initial-condition ensemble",
                "structural_invariants": "the observed density response has temporal period 3 for the unrestricted random ensemble",
                "rule_relation_constraint_function_or_probability_law": "measure black-cell density on successive steps and detect the persistent three-step oscillation",
                "result_kind": "the period-3 density response and its region-based explanation",
                "excluded_observers_and_representations": "density and the rendered region picture are derived observations, not the native cellular-automaton state",
            },
            image_witnesses=[p + "_page_969_Picture_4.jpeg"],
            related=["rule-73 fair-random initial-condition ensemble", "rule-73 no-even-black-block initial-condition filter"],
        ),
        spec(
            "exact-period-p repeating-configuration constraint for one-dimensional cellular automata",
            "U006432",
            1,
            "constraint",
            [
                ev("U006432", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The target is strict first return at p steps, not merely return at a time divisible by a smaller period, and a repeating-block witness has bounded length.", CONSTRAINT_FIELDS + ["parameters_and_variants"]),
                ev("U006434", "PROSE", "CONTEXTUAL", "The bounded survey distinguishes obtainable exact periods and records working block sizes up to 25.", ["result_kind", "parameters_and_variants"]),
                ev("U006439", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For a non-one-sided-additive rule, inspect all blocks of length 2pr+1 whose center returns after p steps and concatenate compatible blocks; this constructs p-return configurations and needs a lower-period exclusion for strict exactness.", ["input", "rule_relation_constraint_function_or_probability_law", "result_kind", "witness_semantics"]),
            ],
            values={
                "input": "a 1D cellular-automaton rule, range r, and requested period p",
                "carrier": "bi-infinite one-dimensional configurations",
                "alphabet_or_value_schema": "the cellular automaton's finite colors",
                "rule_relation_constraint_function_or_probability_law": "CA^p(configuration)=configuration and the configuration does not return at any smaller positive step",
                "result_kind": "the set of configurations whose exact temporal period is p",
                "witness_semantics": "a repeating sequence of compatible local blocks, with a spatial block-length witness bounded by 2^(2pr), whose first temporal return is p",
                "parameters_and_variants": "strict exact period p is distinguished from periods merely dividing p",
            },
            parameters=[
                ("p", "requested strict temporal period"),
                ("r", "cellular-automaton range; local test blocks have length 2pr+1"),
            ],
            missing=["The local p-return block construction must additionally exclude every smaller positive return period to enumerate strict exact-period configurations."],
            image_witnesses=[p + "_page_969_Picture_7.jpeg"],
        ),
        spec(
            "rule-90 repeating-block seed preset survey for periods 1 through 10",
            "U006435",
            1,
            "seed",
            [
                ev("U006435", "PROSE", "DIRECT_IDENTITY", "Rule 90 admits every temporal period and the note supplies repeating-block seed examples for periods through 10.", ["object_kind", "carrier", "support", "alphabet_or_value_schema", "law_kind", "result_kind", "parameters_and_variants"]),
                ev("U006436", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "Ten integers are listed as encodings of period-indexed repeating blocks for periods 1 through 10, but widths and leading-zero handling are not printed with the list.", ["complete_state", "seed", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"]),
                ev("U006437", "PROSE", "CORROBORATING", "The source spells out multiple working period-1 and period-2 blocks.", ["complete_state", "parameters_and_variants"]),
            ],
            values={
                "carrier": "a one-dimensional cyclic repetition of a finite binary block",
                "support": "the source's listed rule-90 blocks for requested periods 1 through 10",
                "alphabet_or_value_schema": "black and white cells",
                "complete_state": "the bi-infinite configuration formed by repeating the selected finite block",
                "rule_relation_constraint_function_or_probability_law": "decode the period-indexed integer as a binary block and repeat that block as the rule-90 initial condition",
                "parameters_and_variants": "ten period-indexed presets for p=1 through 10, with multiple examples explicitly stated for p=1 and p=2",
            },
            parameters=[
                ("p", "requested period, from 1 through 10 in the listed survey"),
                ("integer block encoding", "one source-listed integer whose binary digits represent a repeating block"),
            ],
            missing=["The list does not state the block width or leading-zero convention needed to decode each integer unambiguously."],
            related=["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"],
        ),
        spec(
            "period-dividing cellular-automaton configuration count function",
            "U006437",
            1,
            "observer",
            [
                ev("U006437", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "For rule 90 the number of configurations whose temporal period divides p is 4^p.", OBS_FIELDS),
                ev("U006438", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "For rule 30 the note gives the period-dividing counts for p=1 through 10 and states the one-sided-additive asymptotic growth law.", ["rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
            ],
            values={
                "input": "a supported cellular-automaton rule and positive period p",
                "rule_relation_constraint_function_or_probability_law": "for rule 90 return 4^p; for rule 30 use the source's listed values for p=1..10",
                "result_kind": "the number of configurations whose temporal period divides p",
                "parameters_and_variants": "rule 90 exact formula; rule 30 values {3,3,15,10,8,99,18,14,30,163} for p=1..10; one-sided-additive asymptotic growth k^(h_tx p)",
            },
            parameters=[("p", "positive return time; the function counts configurations with period dividing p")],
            related=["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"],
        ),
        spec(
            "two-dimensional repeating-configuration constraint",
            "U006441",
            1,
            "constraint",
            [
                ev(
                    "U006441",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "The two-dimensional repeating-configuration problem lacks the one-dimensional guarantee of a repetitive fixed-block witness; satisfying configurations may be arbitrarily complex, while infinite stripes reduce to the one-dimensional case.",
                    [
                        "object_kind",
                        "carrier",
                        "input",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                        "result_kind",
                        "witness_semantics",
                        "parameters_and_variants",
                    ],
                )
            ],
            values={
                "carrier": "two-dimensional cellular-automaton configurations",
                "input": "a two-dimensional cellular-automaton rule and requested return period",
                "rule_relation_constraint_function_or_probability_law": "accept configurations that return to themselves after the requested number of cellular-automaton steps",
                "result_kind": "the satisfying two-dimensional repeating configurations, or their existence",
                "witness_semantics": "a witness may be arbitrarily complex; unlike in one dimension, no periodic fixed-block array is guaranteed",
                "parameters_and_variants": "the infinite-stripe restriction reduces the problem to the one-dimensional case",
            },
            variants=[("infinite-stripe restriction", "configurations made only of infinite stripes reduce to a one-dimensional repeating-configuration problem")],
            missing=["The note gives no finite complete search bound or general constructive procedure for two-dimensional witnesses."],
            related=["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"],
        ),
        spec(
            "modular multiplication circle map",
            "U006442",
            1,
            "map",
            [ev("U006442", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The iterated map is x -> Mod[a x,1], with rational initial states yielding repetitive behavior for rational a.", MAP_FIELDS + ["seed", "parameters_and_variants"])],
            values={
                "carrier": "real values modulo 1",
                "complete_state": "the current residue x",
                "rule_relation_constraint_function_or_probability_law": "x -> Mod[a x,1]",
                "parameters_and_variants": "multiplier a",
                "seed": "a rational initial value yields repetitive behavior when a is rational",
            },
            parameters=[("a", "rational multiplier in the stated repetitive-behavior case"), ("initial x", "rational initial value in the stated repetitive-behavior case")],
            variants=[("rational repetitive orbit", "rational a together with rational initial x yields repetitive behavior")],
        ),
        spec(
            "Anosov torus map family",
            "U006442",
            2,
            "map",
            [ev("U006442", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "A higher-dimensional map is explicitly given as {x,y} -> Mod[m.{x,y},1], with rational initial states stated to be repetitive.", MAP_FIELDS + ["seed", "parameters_and_variants"])],
            values={
                "carrier": "pairs of real values modulo 1",
                "complete_state": "the current pair {x,y}",
                "rule_relation_constraint_function_or_probability_law": "{x,y} -> Mod[m.{x,y},1]",
                "parameters_and_variants": "matrix m",
                "seed": "a rational initial vector yields repetitive behavior in the stated rational setting",
            },
            parameters=[("m", "matrix defining the torus map"), ("initial {x,y}", "rational initial vector in the stated repetitive-behavior case")],
            variants=[("rational repetitive orbit", "a rational initial vector yields repetitive behavior under the stated map family")],
            missing=["The admissible matrices m are not constrained in the unit."],
        ),
        spec(
            "continued-fraction map",
            "U006442",
            3,
            "map",
            [ev("U006442", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The continued-fraction map is x -> Mod[1/x,1] and becomes repetitive when its initial value solves a quadratic equation.", MAP_FIELDS + ["seed", "parameters_and_variants"])],
            values={
                "carrier": "real values modulo 1, excluding undefined division at zero",
                "complete_state": "the current value x",
                "rule_relation_constraint_function_or_probability_law": "x -> Mod[1/x,1]",
                "seed": "an initial value satisfying a quadratic equation yields repetitive behavior",
                "parameters_and_variants": "quadratic-irrational initial values are the stated repetitive-orbit family",
            },
            parameters=[("initial x", "a solution of a quadratic equation in the stated repetitive-orbit family")],
            variants=[("quadratic repetitive orbit", "an initial value solving a quadratic equation yields repetitive behavior")],
        ),
        spec(
            "polynomial iterated-map family",
            "U006443",
            1,
            "map",
            [ev("U006443", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "A map x -> f[x] with polynomial f, including f[x]=a x(1-x), is explicitly delimited.", MAP_FIELDS + ["parameters_and_variants"])],
            values={
                "carrier": "real values",
                "complete_state": "the current real value x",
                "rule_relation_constraint_function_or_probability_law": "x -> f[x] for polynomial f",
                "parameters_and_variants": "polynomial coefficients; logistic-map parameter a",
            },
            variants=[("logistic map", "f[x]=a x(1-x)")],
        ),
        spec(
            "p-return point query for an iterated map",
            "U006443",
            2,
            "constraint",
            [ev("U006444", "CODE", "DIRECT_COMPLETE_MECHANICS", "Real period-p return points are selected from solutions of Nest[f,x,p]==x.", CONSTRAINT_FIELDS + ["parameters_and_variants"])],
            values={
                "input": "an iterated function f and requested period p",
                "carrier": "real candidate initial values x",
                "rule_relation_constraint_function_or_probability_law": "Nest[f,x,p] == x and Im[x] == 0",
                "result_kind": "the set of real points whose period divides p",
            },
            parameters=[("p", "positive return time; lower periods are included")],
            missing=["The code does not remove solutions with a smaller positive return period, so it is a p-return/period-dividing query rather than a strict exact-period query."],
        ),
        spec(
            "Sarkovskii period-implication relation",
            "U006446",
            1,
            "constraint",
            [ev("U006446", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For a continuous iterated map, existence of period m entails periods n in the stated Sarkovskii order.", CONSTRAINT_FIELDS), ev("U006447", "CODE", "DIRECT_COMPLETE_MECHANICS", "OrderedQ over odd parts and powers of two implements the period-order test for {m,n}.", ["rule_relation_constraint_function_or_probability_law"])],
            values={
                "input": "two positive periods m and n for a continuous iterated map",
                "rule_relation_constraint_function_or_probability_law": "the explicit OrderedQ expression on odd parts and powers of two",
                "result_kind": "whether period m forces period n",
            },
        ),
        spec(
            "renormalization-group blocking transformation",
            "U006449",
            1,
            "representation",
            [ev("U006449", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A blocking transform replaces lattice blocks by individual elements and maps averaged configuration weights to effective parameters whose scale dependence follows differential equations.", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"])],
            values={
                "input": "a lattice rule or weighted configuration ensemble and a block scale",
                "rule_relation_constraint_function_or_probability_law": "replace each element block by one effective element and derive scale-dependent effective couplings",
                "result_kind": "a coarse-grained rule or parameter flow",
                "parameters_and_variants": "block scale, blocking map, and the resulting scale-dependent effective parameters",
            },
            missing=["The blocking kernel and effective-parameter equations are not specified."],
        ),
        spec(
            "prime-modulus additive-CA scale self-emulation transform",
            "U006451",
            1,
            "representation",
            [ev("U006451", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Interspersing k-1 zeros, evolving k steps, and retaining every kth row and column reproduces the additive rule when k is prime.", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"])],
            values={
                "input": "a history of a modulo-k additive cellular automaton",
                "rule_relation_constraint_function_or_probability_law": "insert k-1 zeros between cells, evolve k steps, then keep every kth row and column",
                "result_kind": "a rescaled copy of the original history",
                "parameters_and_variants": "prime modulus k; composite k yields a superposition rather than strict invariance",
            },
        ),
        spec(
            "additive-cellular-automaton fractal-dimension analyzer",
            "U006451",
            2,
            "observer",
            [
                ev("U006452", "CODE", "DIRECT_PARTIAL_MECHANICS", "g[w,k,t] counts nonzero cells in the first t rows generated from one initial 1.", OBS_FIELDS),
                ev("U006453", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The fractal dimension is introduced as a large-m scaling limit of the nonzero-cell count.", ["law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
                ev("U006454", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The dimension is the large-m limit Log[k,g(w,k,k^(m+1))/g(w,k,k^m)].", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
                ev("U006455", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For prime k, the source introduces an exact eigenvalue computation of the dimension.", ["parameters_and_variants", "result_kind"]),
                ev("U006456", "CODE", "DIRECT_COMPLETE_MECHANICS", "d[w,k] computes the prime-modulus dimension from the largest absolute eigenvalue of the constructed finite matrix.", ["rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
                ev("U006458", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "The source supplies exact algebraic dimensions for two additional binary weight vectors.", ["parameters_and_variants", "result_kind"]),
                ev("U006460", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "The source supplies a general rule-90 formula in k and exact rule-150 examples for k=3,5,7.", ["parameters_and_variants", "result_kind"]),
            ],
            values={
                "input": "additive-rule weights w, modulus k, and the single-1 seed",
                "rule_relation_constraint_function_or_probability_law": "compute nonzero-cell growth g at successive powers of k and take the logarithmic ratio limit",
                "result_kind": "the fractal dimension of the generated spacetime pattern",
                "parameters_and_variants": "weights w and modulus k; the exact eigenvalue implementation is stated for prime k, with explicit rule-90, rule-150, and longer-weight examples",
            },
            parameters=[("w", "additive cellular-automaton weight vector"), ("k", "cell-color modulus, prime for the exact eigenvalue implementation")],
            variants=[
                ("rule 90", "w={1,0,1}, including d=Log[2,3] for k=2"),
                ("rule 150", "w={1,1,1}, with explicit k=2,3,5,7 values"),
                ("longer binary weights", "explicit values for {1,1,0,1,0} and {1,1,0,1,1}"),
            ],
        ),
        spec(
            "associative-operation cellular automaton family",
            "U006461",
            1,
            "ca1d",
            [
                ev("U006461", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "The new cell is f[a1,a2], with f associative.", ["object_kind", "alphabet_or_value_schema", "read_dependencies_or_neighborhood", "law_kind", "rule_relation_constraint_function_or_probability_law", "structural_invariants"]),
                ev("U006462", "CODE", "DIRECT_COMPLETE_MECHANICS", "NestList starts from {a}; each synchronous row applies f to adjacent cells after explicit zero padding on both ends.", ["native_time", "carrier", "support", "complete_state", "seed", "boundary", "schedule", "write_replacement_assembly_or_commit", "result_kind", "determinism_branching_or_measure"]),
                ev("U006463", "PROSE", "CONTEXTUAL", "The source introduces the explicit first-step expansions used to expose the associative structure.", ["structural_invariants"]),
                ev("U006464", "CODE", "CORROBORATING", "The first four symbolic rows expand the binary operation before associativity is imposed.", ["rule_relation_constraint_function_or_probability_law"]),
                ev("U006465", "PROSE", "CONTEXTUAL", "The source then imposes Flat associativity on those expansions.", ["structural_invariants"]),
                ev("U006466", "CODE", "CORROBORATING", "The flattened rows display the resulting n-ary operation terms.", ["structural_invariants"]),
                ev("U006467", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Binomial multiplicities and finite values force Pascal-triangle-modulo behavior under the stated commutative or identity conditions.", ["structural_invariants", "parameters_and_variants"]),
                ev("U006468", "PROSE", "CORROBORATING", "Associative and commutative f yields nested behavior for multiple nonzero initial elements; noncommutative f can yield non-nested patterns.", ["structural_invariants", "parameters_and_variants"]),
            ],
            values={
                "carrier": "a finite one-dimensional row expanded by zero padding",
                "support": "a finite row over the operation's value set",
                "complete_state": "the current finite row",
                "seed": "the singleton row {a}",
                "boundary": "one zero is prepended and appended before each adjacent-pair update",
                "alphabet_or_value_schema": "a finite set closed under binary operation f",
                "structural_invariants": "f is associative; commutativity and identity are optional stated variants",
                "read_dependencies_or_neighborhood": "two adjacent values a1,a2",
                "rule_relation_constraint_function_or_probability_law": "new cell = f[a1,a2]",
                "parameters_and_variants": "associative-commutative operations yield nested behavior; noncommutative associative operations can yield non-nested behavior",
            },
        ),
        spec(
            "rule-45 nested-background seed preset",
            "U006469",
            1,
            "seed",
            [
                ev(
                    "U006469",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "A single black cell placed on a background of repeated ■■□ blocks is stated to yield a slanted rule-90-like nested pattern under rule 45.",
                    SEED_FIELDS + ["parameters_and_variants"],
                )
            ],
            values={
                "carrier": "a one-dimensional binary rule-45 configuration",
                "support": "a single black defect on an infinite period-3 background",
                "alphabet_or_value_schema": "black and white cells",
                "complete_state": "one black cell on a background formed by repeating ■■□",
                "rule_relation_constraint_function_or_probability_law": "repeat ■■□ as the background and insert one black cell as the rule-45 seed",
                "parameters_and_variants": "the source fixes the period-3 ■■□ background and a single black insertion",
            },
            variants=[("■■□ background", "single black cell on the repeated period-3 background")],
            related=["finite cyclic rule-90 polynomial cellular automaton"],
        ),
        spec(
            "elementary-rule pattern-uniqueness analyzer",
            "U006469",
            2,
            "observer",
            [
                ev("U006469", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Starting every elementary rule from one black cell, the analyzer sorts successive configurations and counts distinct configurations and complete patterns across all 256 rules.", OBS_FIELDS + ["parameters_and_variants", "excluded_observers_and_representations"]),
                ev("U006470", "IMAGE", "CONTEXTUAL", "The original-resolution figure renders the sorted configuration comparison across the 256 elementary rules.", ["result_kind", "excluded_observers_and_representations"], p + "_page_971_Figure_11.jpeg"),
            ],
            values={
                "input": "all 256 elementary cellular-automaton rules, each started from a single black cell, and an observation horizon",
                "rule_relation_constraint_function_or_probability_law": "sort and deduplicate the configurations at each step and the resulting complete finite histories",
                "result_kind": "counts and equivalence classes of distinct configurations and complete patterns",
                "parameters_and_variants": "after many steps the source reports 94–105 distinct configurations and 143 distinct complete patterns",
                "excluded_observers_and_representations": "the sorted comparison and uniqueness counts are derived observations, not native rule state",
            },
            image_witnesses=[p + "_page_971_Figure_11.jpeg"],
        ),
        spec(
            "three-state cellular-automaton square roots of rule 30",
            "U006471",
            1,
            "ca1d",
            [ev("U006471", "PROSE", "DIRECT_IDENTITY", "Three k=3, r=1/2 rules numbered 11736, 11739, and 11742 square to rule 30.", ["object_kind", "alphabet_or_value_schema", "read_dependencies_or_neighborhood", "parameters_and_variants"])],
            values={
                "alphabet_or_value_schema": "three colors",
                "read_dependencies_or_neighborhood": "range 1/2",
                "parameters_and_variants": "rule numbers 11736, 11739, and 11742",
            },
            missing=["The rule-number decoding convention and tables are not restated."],
        ),
        spec(
            "nested-sequence initial-condition family for rule 90",
            "U006471",
            2,
            "seed",
            [ev("U006471", "PROSE", "DIRECT_IDENTITY", "Nested sequences from page 83 are identified as initial conditions for rule 90, with three variants pictured immediately below.", ["object_kind", "seed", "result_kind", "parameters_and_variants"]), ev("U006472", "IMAGE", "CONTEXTUAL", "Three resulting rule-90 histories visually distinguish three nested-sequence variants.", ["parameters_and_variants"], p + "_page_971_Nested_Initial_Conditions_Three_Panel_Row.jpeg")],
            values={
                "carrier": "one-dimensional binary sequences",
                "support": "the nested sequence family referenced on page 83",
                "complete_state": "one nested binary initial sequence",
                "rule_relation_constraint_function_or_probability_law": "select one of the referenced nested sequences as the rule-90 initial condition",
                "parameters_and_variants": "three pictured nested-sequence initial-condition variants",
            },
            missing=["The three nested sequence generators are not specified in this bundle."],
            image_witnesses=[p + "_page_971_Nested_Initial_Conditions_Three_Panel_Row.jpeg"],
        ),
        spec(
            "finite-automaton path recognizer",
            "U006475",
            1,
            "constraint",
            [
                ev("U006475", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A finite labeled transition network represents allowed value sequences by paths.", ["object_kind", "carrier", "alphabet_or_value_schema", "complete_state", "input", "law_kind", "result_kind"]),
                ev("U006476", "CODE", "DIRECT_COMPLETE_MECHANICS", "NetStep advances a node set through all arcs carrying one input label.", ["rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure"]),
                ev("U006477", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A list is accepted when it labels a path beginning at at least one network node.", ["input", "result_kind", "witness_semantics"]),
                ev("U006478", "CODE", "DIRECT_COMPLETE_MECHANICS", "Fold[NetStep,...] accepts exactly when at least one starting-node path remains after consuming the input list.", ["rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure", "witness_semantics"]),
            ],
            values={
                "carrier": "a finite set of nodes with labeled arcs",
                "alphabet_or_value_schema": "arc labels",
                "complete_state": "the current set of reachable nodes",
                "input": "a finite sequence of labels",
                "rule_relation_constraint_function_or_probability_law": "advance the reachable node set along every arc bearing the next label; accept iff the final set is nonempty",
                "result_kind": "accept/reject plus possible paths",
                "witness_semantics": "a path whose labels equal the input sequence",
            },
            aliases=["finite automaton", "finite state machine", "NFA"],
        ),
        spec(
            "cellular-automaton image-set network transform",
            "U006479",
            1,
            "representation",
            [
                ev("U006479", "PROSE", "DIRECT_IDENTITY", "The source asks for the sequence set obtained after one cellular-automaton step from a set represented by a finite network.", ["object_kind", "input", "result_kind"]),
                ev("U006480", "CODE", "DIRECT_COMPLETE_MECHANICS", "NetCAStep constructs a labeled network for the one-step cellular-automaton image of a sequence set.", ["law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
                ev("U006481", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source gives the explicit {k,r,rtab} encoding for elementary rule 126 and introduces the all-sequences starting network.", ["input", "parameters_and_variants"]),
                ev("U006482", "CODE", "DIRECT_COMPLETE_MECHANICS", "AllNet[k] constructs the one-node network accepting every sequence over k labels.", ["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"]),
                ev("U006483", "PROSE", "CONTEXTUAL", "The source introduces the concrete rule-126 output network produced by the transform.", []),
                ev("U006484", "CODE", "CORROBORATING", "The explicit four-node rule-126 image network is printed.", ["result_kind", "parameters_and_variants"]),
            ],
            values={
                "input": "a finite network for a sequence set and a CA specification {k,r,rtab}",
                "rule_relation_constraint_function_or_probability_law": "lift network states to length-2r contexts and relabel transitions by rtab",
                "result_kind": "a finite network accepting sequences obtainable after one CA step",
                "parameters_and_variants": "alphabet size k, cellular-automaton range r, and transition table rtab",
            },
            parameters=[
                ("k", "alphabet size"),
                ("r", "cellular-automaton range"),
                ("rtab", "transition table"),
            ],
            variants=[
                ("all-sequences input", "AllNet[k] is the one-node source network accepting every k-symbol sequence"),
                ("rule-126 example", "{2,1,Reverse[IntegerDigits[126,2,8]]} yields the printed four-node network"),
            ],
        ),
        spec(
            "deterministic finite-automaton minimizer",
            "U006485",
            1,
            "representation",
            [
                ev("U006485", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A nondeterministic network is determinized and equivalent nodes are combined to obtain a unique minimal DFA.", ["object_kind", "input", "law_kind", "result_kind"]),
                ev("U006486", "CODE", "DIRECT_COMPLETE_MECHANICS", "MinNet, DSets, and ISets give the subset construction and equivalence-class reduction.", ["rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure", "parameters_and_variants"]),
                ev("U006487", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source states the 2^q-1 worst-case state count, the implementation's approximate n^2 work, a known n Log[n] alternative, and the concrete minimized rule-126 network.", ["structural_invariants", "result_kind", "parameters_and_variants"]),
            ],
            values={
                "input": "a finite labeled nondeterministic network",
                "rule_relation_constraint_function_or_probability_law": "subset-determinize, partition equivalent states, and quotient the transition graph",
                "result_kind": "an equivalent minimal deterministic finite automaton",
                "structural_invariants": "a q-node source can yield as many as 2^q-1 determinized states",
                "parameters_and_variants": "the printed MinNet can take about n^2 steps for an n-node result; an n Log[n] method is known; a rule-126 result is supplied",
            },
            aliases=["MinNet"],
            parameters=[("k", "number of arc labels, default 2"), ("q", "number of source-network nodes")],
            variants=[("rule-126 result", "{{1->3},{0->2,1->1},{0->2,1->3}}")],
        ),
        spec(
            "trimmed sequence-network transformer",
            "U006488",
            1,
            "representation",
            [ev("U006489", "CODE", "DIRECT_COMPLETE_MECHANICS", "TrimNet intersects forward-reachable node sets and renumbers the surviving subnetwork so paths may start at any retained node.", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind"])],
            values={
                "input": "a finite labeled sequence network",
                "rule_relation_constraint_function_or_probability_law": "retain the intersection of nodes reachable from every node and renumber induced transitions",
                "result_kind": "a trimmed network with paths allowed to start at any node",
            },
            aliases=["TrimNet"],
        ),
        spec(
            "regular language",
            "U006492",
            1,
            "constraint",
            [
                ev("U006492", "PROSE", "DIRECT_COMPLETE_MECHANICS", "A regular language is the set of label sequences obtained by following possible paths through a finite network.", CONSTRAINT_FIELDS),
                ev("U006493", "PROSE", "CONTEXTUAL", "The historical note records sofic systems as the dynamical-systems name for regular-language systems.", []),
            ],
            values={
                "carrier": "finite or infinite sequences over a finite alphabet as delimited by the accepting convention",
                "input": "a symbol sequence and a finite labeled network",
                "rule_relation_constraint_function_or_probability_law": "the sequence belongs iff it labels an allowed network path",
                "result_kind": "the set of accepted sequences",
            },
            aliases=["sofic system", "sofic systems"],
        ),
        spec(
            "regular-expression sequence denotation",
            "U006492",
            2,
            "constraint",
            [ev("U006492", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Regular-language sequences are identified with those matched by Mathematica patterns without explicit pattern names, with concrete pattern examples.", CONSTRAINT_FIELDS)],
            values={
                "input": "a sequence and a regular pattern without explicit pattern names",
                "rule_relation_constraint_function_or_probability_law": "the sequence is accepted exactly when it matches the pattern",
                "result_kind": "the pattern's denoted sequence set",
            },
            aliases=["regular expression"],
        ),
        spec(
            "rational generating-function representation of a regular language",
            "U006492",
            3,
            "representation",
            [ev("U006492", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Words are mapped to products of noncommuting variables and collected as coefficients of a rational formal power series.", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind"])],
            values={
                "input": "a regular language over a finite alphabet",
                "rule_relation_constraint_function_or_probability_law": "map each word to the corresponding product of noncommuting symbol variables and sum",
                "result_kind": "a rational formal generating function",
            },
        ),
        spec(
            "cellular-automaton image-network growth and maximum-size analyzer",
            "U006493",
            1,
            "observer",
            [
                ev("U006493", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The note gives node and edge growth formulas or finite sequences for the image networks of rules 108, 128, 132, 160, 184, and 126.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006494", "FORMULA", "CORROBORATING", "The source gives the first five rule-110 node/edge count pairs.", ["result_kind", "parameters_and_variants"]),
                ev("U006495", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The maximum node count after t steps is 2^(k^(2 r t))-1, with stated extremal examples and edge counts.", ["rule_relation_constraint_function_or_probability_law", "result_kind", "structural_invariants", "parameters_and_variants"]),
            ],
            values={
                "input": "a k-color range-r cellular-automaton rule and image-network step t",
                "structural_invariants": "the source's universal maximum node count after t steps is 2^(k^(2 r t))-1",
                "rule_relation_constraint_function_or_probability_law": "construct the finite network for the t-step image set, then count its nodes and labeled arcs and compare with the maximum-size bound",
                "result_kind": "node/edge counts, growth laws, and maximum-size comparisons",
                "parameters_and_variants": "explicit cases include rules 108, 128, 132, 160, 184, 126, 110, rule 22 at t=2, and k=2 r=2 totalistic code 20",
            },
            parameters=[
                ("k", "number of cellular-automaton colors"),
                ("r", "cellular-automaton range"),
                ("t", "number of image-set evolution steps"),
            ],
        ),
        spec(
            "finite-complement language",
            "U006496",
            1,
            "constraint",
            [ev("U006496", "PROSE", "DIRECT_COMPLETE_MECHANICS", "A finite-complement language is characterized by excluding a finite set of finite blocks from otherwise admissible sequences.", CONSTRAINT_FIELDS)],
            values={
                "carrier": "sequences over a finite alphabet",
                "input": "a sequence and a finite forbidden-block set",
                "rule_relation_constraint_function_or_probability_law": "accept iff no forbidden block occurs",
                "result_kind": "the subshift of sequences avoiding all listed blocks",
            },
            aliases=["subshift of finite type"],
        ),
        spec(
            "spatial topological-entropy analyzer",
            "U006497",
            1,
            "observer",
            [
                ev("U006497", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The number s_n of length-n paths is obtained from powers of the network adjacency matrix.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006498", "CODE", "DIRECT_COMPLETE_MECHANICS", "The path-count implementation sums all entries of MatrixPower[m,n].", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
                ev("U006499", "PROSE", "CONTEXTUAL", "The source introduces the network adjacency matrix used by the path-count formula.", ["input"]),
                ev("U006500", "CODE", "DIRECT_COMPLETE_MECHANICS", "The adjacency matrix code increments m[i,j] for each network arc from node i to node j.", ["input", "rule_relation_constraint_function_or_probability_law"]),
                ev("U006504", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Spatial entropy is h=Log[2,kappa], where kappa is the adjacency matrix's largest eigenvalue.", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
            ],
            values={
                "input": "a finite sequence network or its adjacency matrix",
                "rule_relation_constraint_function_or_probability_law": "count length-n paths and take the exponential growth rate Log[2,kappa]",
                "result_kind": "spatial/topological entropy h",
            },
            parameters=[("n", "sequence length for finite path counts")],
        ),
        spec(
            "limiting spatial-entropy bound decision query",
            "U006504",
            1,
            "constraint",
            [
                ev(
                    "U006504",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "The source asks whether the limiting spatial entropy after infinitely many cellular-automaton steps satisfies a given bound, even whether it is nonzero, and states that the problem is undecidable in general.",
                    [
                        "object_kind",
                        "input",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                        "result_kind",
                        "termination_completion_failure",
                        "parameters_and_variants",
                    ],
                )
            ],
            values={
                "input": "a cellular-automaton rule and a proposed bound on its limiting spatial entropy",
                "rule_relation_constraint_function_or_probability_law": "decide whether the infinite-time limiting spatial entropy satisfies the requested bound",
                "result_kind": "a truth value when decidable, including the special query whether the limit is nonzero",
                "termination_completion_failure": "the decision problem is undecidable in general",
            },
            parameters=[("entropy bound", "the proposed limiting bound, including the predicate h>0")],
            missing=["No general terminating decision procedure exists."],
            related=["spatial topological-entropy analyzer"],
        ),
        spec(
            "dynamical zeta function of network cycles",
            "U006506",
            1,
            "observer",
            [
                ev("U006506", "FORMULA", "DIRECT_PARTIAL_MECHANICS", "Cycle counts are traces of matrix powers.", ["object_kind", "input", "law_kind", "result_kind", "determinism_branching_or_measure"]),
                ev("U006507", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The cycle counts are coefficients of x ∂x Log[zeta[m,x]].", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
                ev("U006508", "PROSE", "CONTEXTUAL", "The source introduces the rational zeta function used by that logarithmic derivative.", ["result_kind"]),
                ev("U006509", "CODE", "DIRECT_COMPLETE_MECHANICS", "zeta[m,x] is 1/Det[I-m x].", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
                ev("U006510", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The same zeta function is the product over all cycles of 1/(1-x^n).", ["rule_relation_constraint_function_or_probability_law", "structural_invariants"]),
            ],
            values={
                "input": "a finite network adjacency matrix m and formal variable x",
                "structural_invariants": "the zeta function is rational and factors as a product over network cycles",
                "rule_relation_constraint_function_or_probability_law": "zeta[m,x]=1/Det[I-m x]",
                "result_kind": "a rational generating function whose logarithmic derivative enumerates cycles",
            },
        ),
        spec(
            "hard-square no-adjacent-black constraint model",
            "U006511",
            1,
            "constraint",
            [ev("U006511", "PROSE", "DIRECT_COMPLETE_MECHANICS", "The model set consists of n-by-n binary square grids containing no adjacent pair of black cells.", CONSTRAINT_FIELDS)],
            values={
                "carrier": "two-dimensional n by n square grids",
                "alphabet_or_value_schema": "black and white cells",
                "input": "a finite binary square grid",
                "rule_relation_constraint_function_or_probability_law": "no pair of adjacent cells may both be black",
                "result_kind": "the set of satisfying grids",
            },
        ),
        spec(
            "hard-hexagon lattice-gas model",
            "U006511",
            2,
            "constraint",
            [ev("U006511", "PROSE", "DIRECT_IDENTITY", "The hard-hexagon lattice gas is named as a hexagonal-cell constraint model with a known entropy.", ["object_kind", "carrier", "result_kind"])],
            values={
                "carrier": "a hexagonal lattice",
                "result_kind": "the model's allowed configurations",
            },
            missing=["The occupancy alphabet, adjacency exclusion rule, and boundary convention are not stated in the unit."],
        ),
        spec(
            "square-grid domino-covering constraint",
            "U006511",
            3,
            "constraint",
            [ev("U006511", "PROSE", "DIRECT_COMPLETE_MECHANICS", "Accepted configurations are complete coverings of a square grid by two-cell dominoes.", CONSTRAINT_FIELDS)],
            values={
                "carrier": "a square grid",
                "input": "a placement of two-cell dominoes",
                "rule_relation_constraint_function_or_probability_law": "every grid cell is covered exactly once by a two-cell domino",
                "result_kind": "the set of complete domino tilings",
            },
            aliases=["dimer problem"],
        ),
        spec(
            "measure-entropy analyzer",
            "U006511",
            4,
            "observer",
            [
                ev("U006512", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Measure entropy is the n-to-infinity limit of -Sum[p_i Log_k p_i]/n over k^n blocks.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006513", "PROSE", "DIRECT_IDENTITY", "The source also names the quantity entropy, information, and information dimension.", ["parameters_and_variants"]),
                ev("U006518", "PROSE", "DIRECT_PARTIAL_MECHANICS", "A plug-in measure-entropy estimate can be formed from sampled block probabilities, but it is systematically low; polynomial unbiased estimators around p Log p are proposed as a workaround.", ["input", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
            ],
            values={
                "input": "block probabilities p[i] for k-symbol blocks of length n",
                "rule_relation_constraint_function_or_probability_law": "-Limit[Sum[p[i] Log[k,p[i]]]/n,n->Infinity]",
                "result_kind": "measure entropy",
                "parameters_and_variants": "exact block-probability limit or a sampling plug-in estimate with stated downward bias and polynomial-estimator workaround",
            },
            aliases=["entropy", "information", "information entropy", "information dimension"],
            parameters=[("k", "alphabet size"), ("n", "block length")],
            variants=[("sampled plug-in estimate", "estimate block probabilities from samples; direct substitution is systematically biased downward")],
        ),
        spec(
            "set/topological entropy from block-support growth",
            "U006514",
            1,
            "observer",
            [
                ev("U006514", "FORMULA", "DEFECT_LIMITED", "The extraction prints Limit[Sum[UnitStep[p[i]],{i,k^n}]/n,n->Infinity], which counts supported blocks but omits the logarithm needed for a finite exponential growth rate.", OBS_FIELDS),
                ev("U006515", "PROSE", "DEFECT_LIMITED", "The prose identifies the intended quantity as set entropy, topological entropy, capacity, and fractal dimension, but does not repair the defective printed expression.", ["result_kind", "parameters_and_variants"]),
            ],
            values={
                "input": "block probabilities p[i] for k-symbol blocks of length n",
                "rule_relation_constraint_function_or_probability_law": "the source prints Limit[Sum[UnitStep[p[i]],{i,k^n}]/n,n->Infinity]; for full support this is k^n/n and diverges, so the intended logarithmic support-growth normalization is absent",
                "result_kind": "the source-intended set/topological entropy, with no trustworthy complete formula in the extraction",
                "parameters_and_variants": "also named capacity and fractal dimension in the source",
            },
            aliases=["set entropy", "topological entropy", "capacity", "fractal dimension"],
            status="DEFECTIVE",
            uncertainties=["U006514 omits a logarithm from the support-count growth expression; the exact intended repaired transcription is not printed in the sealed source."],
            missing=["A source-authoritative logarithmic normalization is required before this analyzer can be implemented."],
            related=["spatial topological-entropy analyzer"],
        ),
        spec(
            "generalized q-entropy analyzer",
            "U006516",
            1,
            "observer",
            [
                ev("U006516", "FORMULA", "DEFECT_LIMITED", "The source prints h[q,n]=Log_k Sum_i p_i^q /(n(q-1)); for the stated uniform distribution this evaluates to -1, not the +1 maximum asserted next.", OBS_FIELDS),
                ev("U006517", "PROSE", "DEFECT_LIMITED", "The prose asserts maximum h[q,n]=1 for uniform probabilities, names the q=0, q→1, and q=2 cases, and states monotonicity, contradicting the sign of the printed denominator.", ["result_kind", "parameters_and_variants", "structural_invariants"]),
            ],
            values={
                "input": "block probabilities p[i], alphabet size k, block length n, and order q",
                "structural_invariants": "the prose states h[q+1,n] <= h[q,n] and a uniform-distribution maximum of +1, but those claims conflict with the printed formula's sign",
                "rule_relation_constraint_function_or_probability_law": "the source prints h[q,n]=Log[k,Sum[p[i]^q]]/(n(q-1)); substituting p[i]=k^-n gives -1",
                "result_kind": "a source-intended generalized entropy or dimension whose printed formula is sign-inconsistent",
                "parameters_and_variants": "q=0 set entropy; q->1 measure entropy; q=2 correlation entropy",
            },
            aliases=["Rényi entropy family", "generalized dimensions"],
            parameters=[("k", "alphabet size"), ("n", "block length"), ("q", "generalized-entropy order")],
            variants=[
                ("q=0", "set/topological entropy specialization"),
                ("q→1", "measure-entropy specialization"),
                ("q=2", "correlation entropy"),
            ],
            status="DEFECTIVE",
            uncertainties=["U006516's denominator q-1 reverses the sign relative to U006517's stated uniform-distribution maximum +1."],
            missing=["A source-authoritative sign correction is required before this entropy family can be implemented."],
            related=["set/topological entropy from block-support growth", "measure-entropy analyzer"],
        ),
        spec(
            "sequence-set to Cantor-set encoding",
            "U006518",
            1,
            "representation",
            [
                ev("U006505", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Binary sequences are encoded as Sum[a_i 2^-i], and the resulting Cantor set has Hausdorff dimension equal to the spatial entropy h.", ["object_kind", "input", "rule_relation_constraint_function_or_probability_law", "result_kind", "structural_invariants"]),
                ev("U006518", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "A length-n sequence a[i] over k symbols is encoded as Sum[a[i] k^-i], and the infinite allowed set forms a Cantor set.", ["input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
            ],
            values={
                "input": "a finite or infinite sequence over k symbols",
                "structural_invariants": "for the binary sequence set discussed in U006505, the encoded Cantor set's Hausdorff dimension equals the spatial entropy h",
                "rule_relation_constraint_function_or_probability_law": "map a to Sum[a[i] k^-i]",
                "result_kind": "a real point, or the Cantor set formed by an allowed sequence family",
                "parameters_and_variants": "alphabet size k; k=2 gives the binary encoding Sum[a_i 2^-i], while k=3 with the second color absent gives the middle-thirds Cantor set",
            },
            parameters=[("k", "number of sequence symbols and radix of the encoding"), ("n", "finite prefix length before the infinite-set limit")],
        ),
        spec(
            "finite sequence-network to substitution-system transform",
            "U006518",
            2,
            "representation",
            [
                ev(
                    "U006518",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "For an s-node finite sequence network, assigning one substitution-system element kind to each node makes progressive Cantor-set levels equivalent to successive substitution steps.",
                    [
                        "object_kind",
                        "input",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                        "result_kind",
                        "parameters_and_variants",
                    ],
                )
            ],
            values={
                "input": "a finite s-node network representing an allowed sequence set",
                "rule_relation_constraint_function_or_probability_law": "create s substitution-element kinds corresponding to the network nodes and use network continuations to generate successive allowed-sequence levels",
                "result_kind": "a substitution system generating the nested levels of the encoded Cantor set",
                "parameters_and_variants": "one substitution element kind for each of the s network nodes",
            },
            parameters=[("s", "number of finite-network nodes and resulting substitution element kinds")],
            missing=["The note states the construction principle but does not print the node-to-replacement rule in executable form."],
            related=["sequence-set to Cantor-set encoding", "regular language"],
        ),
        spec(
            "cellular-automaton surjectivity decision query",
            "U006518",
            3,
            "constraint",
            [ev("U006518", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Surjectivity asks whether every possible input state also occurs as output; the stated test constructs the minimal finite automaton.", CONSTRAINT_FIELDS)],
            values={
                "input": "a cellular-automaton rule",
                "rule_relation_constraint_function_or_probability_law": "construct the finite automaton for possible output sequences and test whether it admits every state sequence",
                "result_kind": "whether the global cellular-automaton map is onto",
                "witness_semantics": "for surjectivity, every target state has at least one predecessor",
            },
        ),
        spec(
            "cellular-automaton injectivity, bijectivity, and reversibility decision relation",
            "U006518",
            4,
            "constraint",
            [
                ev("U006518", "PROSE", "DIRECT_IDENTITY", "A cellular automaton is treated as a global endomorphism of its state space, providing the common domain for onto and one-to-one properties.", ["object_kind", "carrier", "input", "law_kind"]),
                ev("U006519", "PROSE", "DIRECT_COMPLETE_MECHANICS", "Injectivity requires distinct inputs to have distinct outputs; a surjective and injective rule is bijective, equivalently reversible.", ["rule_relation_constraint_function_or_probability_law", "result_kind", "witness_semantics", "structural_invariants"]),
                ev("U006520", "PROSE", "DIRECT_PARTIAL_MECHANICS", "In two dimensions these properties are undecidable in general.", ["termination_completion_failure"]),
            ],
            values={
                "carrier": "the complete configuration space of a cellular automaton",
                "input": "a cellular-automaton global map",
                "structural_invariants": "bijectivity is the conjunction of surjectivity and injectivity and is equivalent here to reversibility",
                "rule_relation_constraint_function_or_probability_law": "injective iff distinct input configurations always have distinct successors; bijective iff also every target configuration has a predecessor",
                "result_kind": "whether the map is injective, bijective, and therefore reversible",
                "witness_semantics": "noninjectivity is witnessed by two distinct predecessor configurations with the same successor",
                "termination_completion_failure": "the decision problem is undecidable in general for two-dimensional cellular automata",
            },
            related=["cellular-automaton surjectivity decision query"],
        ),
        spec(
            "full temporal-sequence language for additive cellular automata",
            "U006521",
            1,
            "constraint",
            [
                ev(
                    "U006521",
                    "PROSE",
                    "DIRECT_COMPLETE_MECHANICS",
                    "For additive rules 60 and 90 and partially additive rules 30 and 45, every possible temporal color sequence can occur for a suitable initial condition.",
                    CONSTRAINT_FIELDS + ["parameters_and_variants"],
                )
            ],
            values={
                "carrier": "one-cell temporal color sequences",
                "input": "a temporal color sequence and one of rules 60, 90, 30, or 45",
                "rule_relation_constraint_function_or_probability_law": "accept every sequence; for each one the source asserts existence of a suitable initial condition realizing it at the observed cell",
                "result_kind": "the full temporal shift over the rule's color alphabet",
                "witness_semantics": "a realizing cellular-automaton initial condition exists for every requested temporal sequence",
                "parameters_and_variants": "additive rules 60 and 90; partially additive rules 30 and 45",
            },
            variants=[
                ("additive", "rules 60 and 90"),
                ("partially additive", "rules 30 and 45"),
            ],
            related=["temporal-sequence entropy analyzer"],
        ),
        spec(
            "rule-18 no-adjacent-black temporal-sequence language",
            "U006521",
            2,
            "constraint",
            [
                ev(
                    "U006521",
                    "PROSE",
                    "DIRECT_PARTIAL_MECHANICS",
                    "For rule 18, the source states that every temporal sequence with no adjacent pair of black cells appears to be realizable.",
                    CONSTRAINT_FIELDS,
                )
            ],
            values={
                "carrier": "binary one-cell temporal sequences",
                "alphabet_or_value_schema": "black and white observations",
                "input": "a binary temporal sequence for rule 18",
                "rule_relation_constraint_function_or_probability_law": "accept iff the sequence never contains two adjacent black observations",
                "result_kind": "the stated candidate temporal language of rule 18",
                "witness_semantics": "a suitable rule-18 initial condition realizing the accepted temporal sequence",
            },
            status="AMBIGUOUS",
            uncertainties=["The source qualifies the rule-18 characterization with 'it appears', so completeness is observational rather than proved."],
            related=["temporal-sequence entropy analyzer"],
        ),
        spec(
            "temporal-sequence entropy analyzer",
            "U006521",
            3,
            "observer",
            [ev("U006521", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Temporal sequences follow one cell through successive steps, h_t is defined by analogy with spatial sequence entropy, and directional entropies use sequences at a chosen spacetime slope.", OBS_FIELDS + ["structural_invariants", "parameters_and_variants"])],
            values={
                "input": "the set or distribution of temporal color sequences at one cellular-automaton cell",
                "structural_invariants": "h_t <= 2 lambda h_x; directional entropy can change discontinuously when the observation slope crosses lambda",
                "rule_relation_constraint_function_or_probability_law": "take the exponential growth/information rate of allowed length-n temporal sequences",
                "result_kind": "temporal entropy h_t in bits per unit time",
                "parameters_and_variants": "vertical one-cell temporal entropy or directional entropy at a selected spacetime slope",
            },
            parameters=[("observation slope", "spacetime slope of the sampled sequence; the vertical case follows one fixed cell")],
            variants=[("directional entropy", "entropy of sequences sampled along a chosen spacetime slope")],
            image_witnesses=[p + "_page_975_Picture_7.jpeg"],
        ),
        spec(
            "topological spacetime-entropy analyzer",
            "U006524",
            1,
            "observer",
            [
                ev("U006524", "PROSE", "DIRECT_PARTIAL_MECHANICS", "s[t,x] counts possible x-by-t spacetime patches determined by initial blocks.", OBS_FIELDS + ["parameters_and_variants"]),
                ev("U006525", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "h_tx is the iterated limit of Log_k s[t,x]/t as t then x tend to infinity.", ["rule_relation_constraint_function_or_probability_law", "result_kind"]),
                ev("U006529", "PROSE", "DIRECT_IDENTITY", "The historical note also names spacetime entropy invariant entropy.", ["parameters_and_variants"]),
            ],
            values={
                "input": "counts s[t,x] of possible cellular-automaton spacetime patches",
                "rule_relation_constraint_function_or_probability_law": "Limit[x->Infinity] Limit[t->Infinity] Log[k,s[t,x]]/t",
                "result_kind": "topological spacetime entropy h_tx",
                "parameters_and_variants": "alphabet size k, cellular-automaton range r, patch width x, and patch height t",
            },
            aliases=["invariant entropy"],
            parameters=[("k", "alphabet size"), ("r", "cellular-automaton range"), ("x", "patch width"), ("t", "patch height")],
        ),
        spec(
            "measure spacetime-entropy analyzer",
            "U006526",
            1,
            "observer",
            [ev("U006526", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Measure spacetime entropy replaces patch counts by the probability-weighted p Log p expression.", OBS_FIELDS)],
            values={
                "input": "probabilities of cellular-automaton spacetime patches",
                "rule_relation_constraint_function_or_probability_law": "the spacetime-entropy limit with probability-weighted p Log p in place of set counts",
                "result_kind": "measure spacetime entropy h_tx^mu",
            },
            missing=["The full normalized finite-patch formula is described but not displayed."],
        ),
        spec(
            "full left-shift symbolic dynamical system",
            "U006527",
            1,
            "map",
            [ev("U006527", "PROSE", "DIRECT_COMPLETE_MECHANICS", "A full shift starts with any digit sequence, shifts digits left each step, and emits the leading digit.", MAP_FIELDS)],
            values={
                "carrier": "one-sided digit sequences",
                "complete_state": "the current digit sequence",
                "rule_relation_constraint_function_or_probability_law": "remove/emit the leading digit and shift the remaining digits one place left",
                "result_kind": "the shifted sequence and observed leading digit",
            },
            aliases=["full shift"],
        ),
        spec(
            "finite global-state transition graph",
            "U006531",
            1,
            "representation",
            [
                ev("U006531", "PROSE", "DIRECT_COMPLETE_MECHANICS", "Each complete state of a finite deterministic system becomes a node with one arc to its rule-defined successor.", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "structural_invariants"]),
                ev("U006533", "PROSE", "CORROBORATING", "Cyclic-multiplication examples show pure cycles for odd n and transient trees feeding cycles for even n.", ["structural_invariants"]),
                ev("U006535", "PROSE", "DIRECT_COMPLETE_MECHANICS", "Every deterministic finite-state evolution graph consists of recurrent cycles with possible trees of transient states feeding them.", ["structural_invariants"]),
                ev("U006536", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The rule-254 four-cell graph has 16 nodes and all but one state reaches the all-black fixed point within two steps.", ["parameters_and_variants", "structural_invariants"]),
                ev("U006538", "PROSE", "CORROBORATING", "Larger rule-254 finite systems show the same convergence to a single fixed point.", ["parameters_and_variants", "structural_invariants"]),
                ev("U006540", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Rule-132 state graphs are given as class-2 examples whose number of distinct cycles increases with system size.", ["parameters_and_variants", "structural_invariants"]),
                ev("U006545", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The source warns that infinite-size behavior is recovered only by increasing size while holding the evolution-step horizon fixed.", ["parameters_and_variants"]),
                ev("U006546", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Shift, reflection, and color symmetries produce repeated isomorphic graph pieces and symmetry cosets.", ["structural_invariants"]),
                ev("U006552", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Finite additive-CA graphs have cycle lengths dividing the longest cycle and identical rooted structures at every cycle state, with stated rule-60 and rule-90 tree depths and degrees.", ["structural_invariants", "parameters_and_variants"]),
            ],
            values={
                "input": "a deterministic system with finitely many complete states",
                "structural_invariants": "every node has exactly one outgoing arc; every component contains one recurrent cycle with possible transient trees; underlying spatial or color symmetries can produce repeated isomorphic components",
                "rule_relation_constraint_function_or_probability_law": "create one node per complete state and an arc state -> successor(state)",
                "result_kind": "a functional directed graph of all system states",
                "parameters_and_variants": "for finite additive rules, cycle states carry identical rooted trees; the source states binary tree structure for rule 60 and degree-4 tree structure for rule 90",
            },
            parameters=[
                ("finite state-space size", "number of complete states represented as graph nodes"),
                ("system size", "finite lattice or other size parameter controlling the state space"),
            ],
            variants=[
                ("rule 254", "class-1 convergence to one all-black fixed point"),
                ("rule 132", "class-2 graphs with more cycles at larger sizes"),
                ("rules 60 and 90", "regular additive-rule cycle trees"),
            ],
            image_witnesses=[
                p + "_page_976_Figure_10.jpeg",
                p + "_page_977_Figure_1.jpeg",
                p + "_page_977_Picture_4.jpeg",
                p + "_page_977_Picture_6.jpeg",
                p + "_page_977_Figure_8.jpeg",
                p + "_page_977_Figure_10.jpeg",
                p + "_page_978_Figure_2.jpeg",
                p + "_page_978_Figure_14.jpeg",
                p + "_page_978_Picture_15.jpeg",
            ],
        ),
        spec(
            "left-shift cellular automaton rule 170",
            "U006546",
            1,
            "ca1d",
            [ev("U006546", "PROSE", "DIRECT_COMPLETE_MECHANICS", "Rule 170 shifts every configuration one position to the left at each step; on a cyclic n-cell ring every state lies on a cycle whose length divides n.", CA_FIELDS + ["structural_invariants"])],
            values={
                "structural_invariants": "on a cyclic ring every state is periodic, every cycle length divides n, and cycles correspond to color necklaces",
                "read_dependencies_or_neighborhood": "the right-adjacent source cell for each left-shifted destination",
                "rule_relation_constraint_function_or_probability_law": "new[x] = old[x+1]",
            },
            aliases=["rule 170", "shift rule"],
            image_witnesses=[p + "_page_978_Shift_Rule_170_Size_4_to_8_Five_Panel_Row.jpeg"],
        ),
        spec(
            "shift-rule necklace-cycle count function",
            "U006547",
            1,
            "observer",
            [ev("U006546", "PROSE", "DIRECT_IDENTITY", "Every shift-rule cycle is identified with a distinct k-color necklace of length n.", ["object_kind", "input", "result_kind", "structural_invariants"]), ev("U006547", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The total necklace count is Sum[EulerPhi[n/d] k^d for d dividing n]/n.", ["law_kind", "rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure"])],
            values={
                "input": "cyclic ring length n and alphabet size k",
                "structural_invariants": "shift-rule state cycles are exactly rotation-equivalence classes of k-color length-n strings",
                "rule_relation_constraint_function_or_probability_law": "Sum[EulerPhi[n/d] k^d for d dividing n]/n",
                "result_kind": "the total number of shift-rule cycles, equivalently k-color necklaces",
            },
            related=["left-shift cellular automaton rule 170"],
        ),
        spec(
            "shift-rule exact-cycle-length count function",
            "U006548",
            1,
            "observer",
            [
                ev("U006548", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The number of shift-rule cycles of exact length m is s[m,k]/m.", OBS_FIELDS + ["structural_invariants"]),
                ev("U006549", "CODE", "DIRECT_PARTIAL_MECHANICS", "For prime k the cycles except all-zero correspond to factors of x^(k^n-1)-1 modulo k.", ["structural_invariants", "parameters_and_variants"]),
            ],
            values={
                "input": "requested exact cycle length m and alphabet size k",
                "structural_invariants": "each exact-m cycle contains m primitive-spatial-period states",
                "rule_relation_constraint_function_or_probability_law": "exact_cycle_count(m,k)=s[m,k]/m",
                "result_kind": "the number of shift-rule cycles of exact length m",
                "parameters_and_variants": "for prime k the nonzero cycles correspond to factors of x^(k^n-1)-1 modulo k",
            },
            related=["left-shift cellular automaton rule 170", "primitive spatial-period state-count function"],
        ),
        spec(
            "random functional-digraph ensemble",
            "U006555",
            1,
            "generator",
            [ev("U006555", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For each of n labeled nodes, choose its unique successor at random from the n nodes, yielding n^n possible functional digraphs; the source does not explicitly spell out independence or equal probabilities.", ["object_kind", "carrier", "support", "structural_invariants", "complete_state", "input", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"])],
            values={
                "carrier": "n labeled nodes",
                "support": "all functions from the n-node labeled set to itself",
                "structural_invariants": "every node has exactly one successor and there are exactly n^n labeled outcomes",
                "complete_state": "a directed graph with one successor per node",
                "input": "number of labeled nodes n",
                "rule_relation_constraint_function_or_probability_law": "choose each node's unique successor at random from the n-node set; the source does not further specify the joint probability law",
                "result_kind": "one random functional digraph, or the source's unspecified random ensemble over the n^n possible digraphs",
                "parameters_and_variants": "number of nodes n",
            },
            parameters=[("n", "number of labeled nodes")],
            missing=["The prose does not explicitly state that successor choices are independent or that all n destinations and all n^n graphs are equiprobable."],
            image_witnesses=[p + "_page_979_Figure_1.jpeg"],
            related=["random functional-network statistics analyzer"],
        ),
        spec(
            "random functional-network statistics analyzer",
            "U006555",
            2,
            "observer",
            [ev("U006555", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "For the n-node random functional-digraph ensemble, the source gives average cycle count Sqrt[pi/2] Log[n], average cycle length Sqrt[pi n/8], and mean predecessor-free fraction (1-1/n)^n tending to 1/e.", OBS_FIELDS + ["parameters_and_variants"])],
            values={
                "input": "the source's n-node random functional-digraph ensemble",
                "rule_relation_constraint_function_or_probability_law": "evaluate the source's ensemble-average cycle-count, cycle-length, and predecessor-free-node formulas",
                "result_kind": "associated random-network statistics rather than a generated network",
                "parameters_and_variants": "average distinct cycles Sqrt[pi/2] Log[n]; average cycle length Sqrt[pi n/8]; predecessor-free fraction (1-1/n)^n -> 1/e",
            },
            parameters=[("n", "number of labeled nodes")],
            related=["random functional-digraph ensemble", "finite global-state transition graph"],
        ),
        spec(
            "code-20 initial-condition survival-time analyzer",
            "U006558",
            1,
            "observer",
            [
                ev("U006558", "PROSE", "DIRECT_PARTIAL_MECHANICS", "For the first indexed code-20 initial conditions, the source records steps survived and counts seeds said to lead to persistent structures over stated sample bounds.", OBS_FIELDS + ["parameters_and_variants", "excluded_observers_and_representations"]),
                ev("U006559", "IMAGE", "CONTEXTUAL", "The original-resolution figure renders survival times for the first 1000 initial conditions.", ["result_kind", "excluded_observers_and_representations"], p + "_page_979_Figure_4.jpeg"),
            ],
            values={
                "input": "an indexed collection of code-20 initial conditions and an observation horizon",
                "rule_relation_constraint_function_or_probability_law": "evolve each seed, record its survival time, and count seeds that form persistent structures",
                "result_kind": "per-seed survival data and bounded persistent-structure counts",
                "parameters_and_variants": "first 1000: 72 persistent; first million: 60,171; first billion: 71,079,205",
                "excluded_observers_and_representations": "the survival plot and aggregate counts are observations of code-20 evolution, not native state",
            },
            missing=["The source does not define the initial-condition indexing/decoding convention or the survival/persistence stopping criterion."],
            image_witnesses=[p + "_page_979_Figure_4.jpeg"],
        ),
        spec(
            "rule-110 periodic background field",
            "U006560",
            1,
            "representation",
            [ev("U006560", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The background is a declarative binary spacetime field: repetitions of fixed 14-cell block b with color b[[Mod[x+4t,14]+1]] at coordinate (x,t).", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "structural_invariants", "parameters_and_variants"])],
            values={
                "object_kind": "declarative spacetime field or function",
                "input": "integer spacetime coordinates x and t",
                "structural_invariants": "the row has spatial period 14 and advances by the source's offset 4t modulo 14",
                "rule_relation_constraint_function_or_probability_law": "color(x,t)=b[[Mod[x+4t,14]+1]] for the stated 14-cell b",
                "result_kind": "the binary background color at coordinate (x,t)",
                "parameters_and_variants": "fixed 14-cell block b and integer coordinates x,t",
            },
            parameters=[("x", "integer spatial coordinate"), ("t", "integer time coordinate")],
            aliases=["rule-110 background function"],
            image_witnesses=[p + "_page_979_Picture_6.jpeg"],
            related=["rule-110 persistent-structure seed preset survey", "rule-110 glider-gun initial condition"],
        ),
        spec(
            "rule-110 persistent-structure seed preset survey",
            "U006562",
            1,
            "seed",
            [
                ev("U006562", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Each pictured persistent structure is encoded by inserting IntegerDigits[n,2,w] between repetitions of the rule-110 background block.", SEED_FIELDS),
                ev("U006563", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Fifteen {n,w} seed encodings are enumerated.", ["parameters_and_variants"]),
                ev("U006564", "PROSE", "CONTEXTUAL", "The source introduces the ordered repetition-period and displacement data for those same fifteen presets.", ["parameters_and_variants", "structural_invariants"]),
                ev("U006565", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The corresponding fifteen period/displacement pairs are enumerated in the same order.", ["parameters_and_variants", "structural_invariants"]),
            ],
            values={
                "carrier": "one-dimensional binary rule-110 configurations",
                "support": "finite insertions into the periodic rule-110 background",
                "alphabet_or_value_schema": "binary cells",
                "complete_state": "a background with one encoded insertion",
                "structural_invariants": "each of the fifteen seed presets is paired in order with its stated repetition period and displacement",
                "rule_relation_constraint_function_or_probability_law": "insert IntegerDigits[n,2,w] between repetitions of background block b",
                "parameters_and_variants": "the fifteen ordered {n,w} encodings and period/displacement pairs printed in the note",
            },
            parameters=[
                ("n", "integer whose binary digits form the inserted structure word"),
                ("w", "fixed width of the binary insertion"),
            ],
            related=["rule-110 periodic background field", "rule-110 period/displacement semigroup constraint", "rule-110 extended b/c structure seed generator"],
        ),
        spec(
            "rule-110 period/displacement semigroup constraint",
            "U006566",
            1,
            "constraint",
            [ev("U006566", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "Every rule-110 persistent structure has period/displacement pair {4,-2}r+{3,2}s for nonnegative integers r and s.", CONSTRAINT_FIELDS + ["structural_invariants"])],
            values={
                "carrier": "integer period/displacement pairs",
                "input": "a candidate pair {period, displacement}",
                "structural_invariants": "admissible pairs lie in the nonnegative additive semigroup generated by {4,-2} and {3,2}",
                "rule_relation_constraint_function_or_probability_law": "accept iff {period,displacement}={4,-2}r+{3,2}s for integers r,s>=0",
                "result_kind": "membership in the rule-110 period/displacement semigroup",
                "witness_semantics": "nonnegative integers r and s witnessing the decomposition",
            },
            related=["rule-110 periodic background field", "rule-110 persistent-structure seed preset survey"],
        ),
        spec(
            "rule-110 collision-based structure extension transform",
            "U006566",
            2,
            "representation",
            [
                ev("U006566", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Extended versions of structures (d) through (i) can be obtained by collisions with structure (a).", ["object_kind", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "parameters_and_variants"]),
                ev("U006569", "PROSE", "CONTEXTUAL", "Most persistent structures can also travel in adjacent multiple copies.", ["parameters_and_variants"]),
            ],
            values={
                "input": "one of structures (d) through (i), structure (a), and a collision setup",
                "rule_relation_constraint_function_or_probability_law": "evolve the stated collision with structure (a) to obtain an extended version of the selected structure",
                "result_kind": "an extended persistent rule-110 structure",
                "parameters_and_variants": "targets (d)–(i); adjacent multiple-copy arrangements are also stated",
            },
            missing=["The source does not specify collision phases, separations, or a direct finite seed formula for this transform."],
            related=["rule-110 persistent-structure seed preset survey", "rule-110 collision width-conservation modulo-14 relation"],
        ),
        spec(
            "rule-110 extended b/c structure seed generator",
            "U006566",
            3,
            "seed",
            [
                ev("U006566", "PROSE", "DIRECT_IDENTITY", "Extended versions of structures (b) and (c) are generated by the following parameterized bit concatenation.", ["object_kind", "carrier", "support", "alphabet_or_value_schema", "law_kind", "result_kind"]),
                ev("U006567", "CODE", "DIRECT_COMPLETE_MECHANICS", "The generator concatenates IntegerDigits[1468,2], n copies of IntegerDigits[102524348,2], and IntegerDigits[v,2].", ["complete_state", "seed", "rule_relation_constraint_function_or_probability_law", "determinism_branching_or_measure"]),
                ev("U006568", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The repeat count n is any nonnegative integer and v is one of six enumerated suffix integers.", ["parameters_and_variants"]),
            ],
            values={
                "carrier": "a finite binary insertion for the rule-110 periodic background",
                "support": "the parameterized extended versions of source structures (b) and (c)",
                "alphabet_or_value_schema": "binary cells",
                "complete_state": "the concatenated prefix, n repeated middle words, and selected suffix",
                "rule_relation_constraint_function_or_probability_law": "Flatten[{IntegerDigits[1468,2],Table[IntegerDigits[102524348,2],{n}],IntegerDigits[v,2]}]",
                "parameters_and_variants": "n>=0 and v in {1784,801016,410097400,13304,6406392,3280778648}",
            },
            parameters=[
                ("n", "nonnegative repeat count for the middle word"),
                ("v", "one of the six enumerated suffix integers"),
            ],
            related=["rule-110 periodic background field", "rule-110 persistent-structure seed preset survey"],
        ),
        spec(
            "rule-110 glider-gun initial condition",
            "U006570",
            1,
            "seed",
            [
                ev("U006562", "PROSE", "DIRECT_PARTIAL_MECHANICS", "Rule-110 insertion seeds place IntegerDigits[n,2,w] between repetitions of the periodic background.", ["carrier", "support", "alphabet_or_value_schema", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"]),
                ev("U006570", "FORMULA", "DIRECT_COMPLETE_MECHANICS", "The shown rule-110 glider-gun initial condition is encoded by {n,w}={1339191737336,41}.", ["object_kind", "complete_state", "seed", "law_kind", "result_kind", "determinism_branching_or_measure"]),
            ],
            values={
                "carrier": "a one-dimensional binary rule-110 configuration",
                "support": "a finite 41-cell insertion in the rule-110 background",
                "alphabet_or_value_schema": "binary cells",
                "complete_state": "the encoded rule-110 glider-gun seed",
                "rule_relation_constraint_function_or_probability_law": "insert the 41-bit IntegerDigits representation of 1339191737336 into the rule-110 background",
                "parameters_and_variants": "{n,w}={1339191737336,41}",
            },
            parameters=[("n", "1339191737336"), ("w", "41-bit insertion width")],
            related=["rule-110 periodic background field", "rule-110 persistent-structure seed preset survey", "rule-110 collision width-conservation modulo-14 relation"],
        ),
        spec(
            "rule-110 collision width-conservation modulo-14 relation",
            "U006570",
            2,
            "constraint",
            [ev("U006570", "PROSE", "DIRECT_COMPLETE_MECHANICS", "For every interaction of persistent rule-110 structures, the sum of structure widths is conserved modulo 14.", CONSTRAINT_FIELDS + ["structural_invariants"])],
            values={
                "carrier": "interactions among persistent rule-110 structures",
                "input": "incoming and outgoing persistent structures with their widths",
                "structural_invariants": "total persistent-structure width is conserved modulo the 14-cell background period",
                "rule_relation_constraint_function_or_probability_law": "Sum[incoming widths] == Sum[outgoing widths] modulo 14",
                "result_kind": "whether a proposed collision outcome satisfies width conservation modulo 14",
                "witness_semantics": "the incoming and outgoing width lists with equal sums modulo 14",
            },
            missing=["The width-measurement convention for each structure is not restated in this unit."],
            related=["rule-110 periodic background field", "rule-110 persistent-structure seed preset survey", "rule-110 collision-based structure extension transform", "rule-110 glider-gun initial condition"],
        ),
        *life_structure_specs(p),
    ]


def life_structure_specs(prefix: str) -> list[dict[str, Any]]:
    common_image = prefix + "_page_979_Picture_18.jpeg"
    records: list[dict[str, Any]] = []
    for ordinal, (name, behavior) in enumerate(
        [
            ("Game of Life block still life", "unchanged fixed structure"),
            ("Game of Life beehive still life", "unchanged fixed structure"),
            ("Game of Life blinker oscillator", "periodic oscillator"),
            ("Game of Life glider", "moving periodic structure"),
        ],
        1,
    ):
        records.append(
            spec(
                name,
                "U006571",
                ordinal,
                "seed",
                [
                    ev("U006570", "PROSE", "DIRECT_IDENTITY", "Life persistent structures are introduced as recurring products of random initial conditions.", ["object_kind", "carrier", "alphabet_or_value_schema"]),
                    ev("U006571", "IMAGE", "DIRECT_PARTIAL_MECHANICS", f"The original-resolution labeled panel identifies the {name.removeprefix('Game of Life ')} and shows its {behavior} across frames.", ["complete_state", "seed", "result_kind", "parameters_and_variants"], common_image),
                ],
                values={
                    "carrier": "a finite set of live cells on the infinite Life lattice",
                    "alphabet_or_value_schema": "live/dead cells",
                    "complete_state": f"the pictured {name.removeprefix('Game of Life ')} finite pattern",
                    "rule_relation_constraint_function_or_probability_law": f"use the pictured finite pattern as a Life seed; it exhibits {behavior}",
                    "parameters_and_variants": f"the pictured phases demonstrate the structure's {behavior}",
                },
                missing=["Exact live-cell coordinates are not independently transcribed from the image."],
                image_witnesses=[common_image],
            )
        )
    records.extend(
        [
            spec(
                "Game of Life spaceship",
                "U006572",
                1,
                "seed",
                [ev("U006572", "PROSE", "DIRECT_IDENTITY", "The next most common moving Life structure is named the spaceship.", ["object_kind", "carrier"]), ev("U006573", "IMAGE", "DIRECT_PARTIAL_MECHANICS", "The original-resolution panel shows successive translated phases of the spaceship.", ["complete_state", "seed", "result_kind"], prefix + "_page_979_Picture_20.jpeg")],
                values={
                    "carrier": "a finite set of live cells on the infinite Life lattice",
                    "complete_state": "the pictured spaceship phase",
                    "rule_relation_constraint_function_or_probability_law": "use the pictured finite moving structure as a Life seed",
                },
                missing=["Exact live-cell coordinates and displacement period are not stated."],
                image_witnesses=[prefix + "_page_979_Picture_20.jpeg"],
            ),
            spec(
                "Game of Life still-life catalogue below eight live cells",
                "U006574",
                1,
                "constraint",
                [ev("U006574", "PROSE", "DIRECT_COMPLETE_MECHANICS", "The catalogue is exactly the Life structures with fewer than eight black cells that are unchanged by one evolution step.", CONSTRAINT_FIELDS), ev("U006575", "IMAGE", "CONTEXTUAL", "The original-resolution panel displays the complete finite catalogue.", ["result_kind"], prefix + "_page_979_Picture_22.jpeg")],
                values={
                    "carrier": "finite live-cell subsets of the Life lattice",
                    "input": "a finite Life configuration with fewer than eight live cells",
                    "rule_relation_constraint_function_or_probability_law": "LifeStep[state] == state and live-cell count < 8",
                    "result_kind": "the complete satisfying still-life set",
                },
                missing=["The source asserts that the pictured panel is complete, but the member patterns and live-cell coordinates are not transcribed into the text record."],
                image_witnesses=[prefix + "_page_979_Picture_22.jpeg"],
            ),
            spec(
                "bounded Game of Life exact-period oscillator example survey",
                "U006578",
                1,
                "constraint",
                [ev("U006578", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The bounded survey selects Life oscillator examples by their first-return period and reports examples for every period through 18.", CONSTRAINT_FIELDS + ["parameters_and_variants"]), ev("U006579", "IMAGE", "CONTEXTUAL", "The original-resolution panel labels one or more displayed examples by periods 3 through 18 without claiming a complete catalogue.", ["result_kind", "parameters_and_variants"], prefix + "_page_980_Figure_3.jpeg")],
                values={
                    "carrier": "finite live-cell subsets of the Life lattice",
                    "input": "a finite Life configuration and requested period p<=18",
                    "rule_relation_constraint_function_or_probability_law": "LifeStep^p[state] == state and no smaller positive step returns the state",
                    "result_kind": "bounded, period-indexed example witnesses rather than the complete set of oscillators",
                    "witness_semantics": "a displayed Life structure whose first return occurs after exactly p steps",
                    "parameters_and_variants": "requested exact period p<=18; the displayed panel labels examples for periods 3 through 18",
                },
                parameters=[("p", "requested exact first-return period, with examples stated through 18")],
                image_witnesses=[prefix + "_page_980_Figure_3.jpeg"],
            ),
            spec(
                "bounded Game of Life velocity-class example survey",
                "U006580",
                1,
                "constraint",
                [ev("U006580", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The bounded survey selects persistent Life structures by horizontal and vertical speed.", CONSTRAINT_FIELDS + ["parameters_and_variants"]), ev("U006581", "IMAGE", "CONTEXTUAL", "The panel labels seven direction/speed examples without claiming a complete velocity catalogue.", ["result_kind", "parameters_and_variants"], prefix + "_page_980_Picture_5.jpeg")],
                values={
                    "carrier": "finite persistent Life structures",
                    "input": "a Life structure and requested displacement per period",
                    "rule_relation_constraint_function_or_probability_law": "after p steps the structure equals a spatial translation by the stated horizontal/vertical displacement",
                    "result_kind": "a bounded set of example witnesses grouped by velocity, not the complete satisfying set",
                    "witness_semantics": "a displayed persistent structure with the stated displacement over its period",
                    "parameters_and_variants": "seven pictured horizontal/vertical direction-and-speed classes",
                },
                parameters=[
                    ("period", "number of Life steps before the structure repeats up to translation"),
                    ("displacement", "horizontal and vertical translation over that period"),
                ],
                missing=["The exact seeds and periods behind every pictured velocity label are not transcribed."],
                image_witnesses=[prefix + "_page_980_Picture_5.jpeg"],
            ),
            spec(
                "Gosper Game of Life glider gun",
                "U006582",
                1,
                "seed",
                [ev("U006582", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The glider gun emits a glider every 30 steps and has a known 21-live-cell seed.", SEED_FIELDS), ev("U006583", "IMAGE", "CONTEXTUAL", "The original-resolution composite shows the gun and emitted-glider history.", ["result_kind"], prefix + "_page_980_Picture_7.jpeg")],
                values={
                    "carrier": "a finite live-cell subset of the Life lattice",
                    "support": "a 21-live-cell seed in the simplest stated gun",
                    "alphabet_or_value_schema": "live/dead cells",
                    "complete_state": "a glider-gun initial pattern",
                    "rule_relation_constraint_function_or_probability_law": "use the glider-gun seed under Life; it emits one glider every 30 steps",
                },
                missing=["The 21 live-cell coordinates are not stated."],
                image_witnesses=[prefix + "_page_980_Picture_7.jpeg"],
            ),
            spec(
                "Game of Life switch engine",
                "U006582",
                2,
                "seed",
                [ev("U006582", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The switch engine leaves a trail while moving and can start from 10 live cells, a 5x5 region, or a 39x1 region.", SEED_FIELDS + ["parameters_and_variants"]), ev("U006583", "IMAGE", "CONTEXTUAL", "The original-resolution composite shows switch-engine growth horizontally and vertically.", ["result_kind", "parameters_and_variants"], prefix + "_page_980_Picture_7.jpeg")],
                values={
                    "carrier": "a finite live-cell subset of the Life lattice",
                    "support": "10 live cells, or seeds bounded by 5x5 or 39x1 as stated",
                    "alphabet_or_value_schema": "live/dead cells",
                    "complete_state": "a switch-engine initial pattern",
                    "rule_relation_constraint_function_or_probability_law": "use a switch-engine seed under Life; the moving structure leaves an unbounded trail",
                    "parameters_and_variants": "10-live-cell, 5x5-bounded, and 39x1-bounded seed forms; horizontal and vertical growth are pictured",
                },
                missing=["Exact live-cell coordinates are not stated."],
                image_witnesses=[prefix + "_page_980_Picture_7.jpeg"],
            ),
            spec(
                "Game of Life pulsar puffer",
                "U006584",
                1,
                "seed",
                [ev("U006584", "PROSE", "DIRECT_IDENTITY", "A more elaborate structure similar to a glider gun is shown.", ["object_kind", "carrier"]), ev("U006585", "IMAGE", "DIRECT_IDENTITY", "The original-resolution labeled composite identifies the pulsar puffer.", ["complete_state", "seed"], prefix + "_page_980_Life_Elaborate_Structures_Four_Panel_Group.jpeg")],
                values={
                    "carrier": "a finite live-cell subset of the Life lattice",
                    "complete_state": "the pictured pulsar-puffer seed",
                    "rule_relation_constraint_function_or_probability_law": "use the pictured pulsar puffer as a Life seed",
                },
                missing=["Exact live-cell coordinates and emission behavior are not stated."],
                image_witnesses=[prefix + "_page_980_Life_Elaborate_Structures_Four_Panel_Group.jpeg"],
            ),
            spec(
                "Game of Life spaceship gun",
                "U006584",
                2,
                "seed",
                [ev("U006584", "PROSE", "DIRECT_IDENTITY", "A second elaborate structure similar to a glider gun is shown.", ["object_kind", "carrier"]), ev("U006585", "IMAGE", "DIRECT_IDENTITY", "The original-resolution labeled composite identifies the spaceship gun.", ["complete_state", "seed"], prefix + "_page_980_Life_Elaborate_Structures_Four_Panel_Group.jpeg")],
                values={
                    "carrier": "a finite live-cell subset of the Life lattice",
                    "complete_state": "the pictured spaceship-gun seed",
                    "rule_relation_constraint_function_or_probability_law": "use the pictured spaceship gun as a Life seed",
                },
                missing=["Exact live-cell coordinates, emitted spaceship, and period are not stated."],
                image_witnesses=[prefix + "_page_980_Life_Elaborate_Structures_Four_Panel_Group.jpeg"],
            ),
            spec(
                "infinite-line Game of Life seed",
                "U006586",
                1,
                "seed",
                [ev("U006586", "PROSE", "DIRECT_COMPLETE_MECHANICS", "An infinite straight line of live Life cells reduces the evolution to one dimension and follows elementary rule 22.", SEED_FIELDS)],
                values={
                    "carrier": "the infinite two-dimensional Life lattice",
                    "support": "all cells on one infinite straight lattice line are live",
                    "alphabet_or_value_schema": "live/dead cells",
                    "complete_state": "one infinite live line on an otherwise dead background",
                    "rule_relation_constraint_function_or_probability_law": "select the infinite-line seed; under Life its effective one-dimensional evolution is rule 22",
                },
            ),
            spec(
                "Game of Life spacefiller",
                "U006587",
                1,
                "seed",
                [ev("U006587", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The spacefiller starts from 206 live cells and produces uniform unbounded growth.", SEED_FIELDS), ev("U006588", "IMAGE", "CONTEXTUAL", "The original-resolution panels show step 5, step 50, and the expanding history.", ["result_kind"], prefix + "_page_980_Life_Spacefiller_Three_Panel_Row.jpeg")],
                values={
                    "carrier": "a finite live-cell subset of the Life lattice",
                    "support": "206 live cells",
                    "alphabet_or_value_schema": "live/dead cells",
                    "complete_state": "the spacefiller initial pattern",
                    "rule_relation_constraint_function_or_probability_law": "use the 206-cell seed under Life; it generates uniform unbounded growth",
                },
                missing=["The 206 live-cell coordinates are not stated."],
                image_witnesses=[prefix + "_page_980_Life_Spacefiller_Three_Panel_Row.jpeg"],
            ),
            spec(
                "Game of Life puffer train",
                "U006589",
                1,
                "seed",
                [ev("U006589", "PROSE", "DIRECT_PARTIAL_MECHANICS", "The puffer train starts from 23 live cells and settles after more than 1100 steps to period 140.", SEED_FIELDS), ev("U006590", "IMAGE", "CONTEXTUAL", "The original-resolution panels show steps 200 and 500 during the long transient.", ["result_kind"], prefix + "_page_980_Life_Puffer_Train_Four_Panel_Group.jpeg")],
                values={
                    "carrier": "a finite live-cell subset of the Life lattice",
                    "support": "23 live cells",
                    "alphabet_or_value_schema": "live/dead cells",
                    "complete_state": "the puffer-train initial pattern",
                    "rule_relation_constraint_function_or_probability_law": "use the 23-cell seed under Life; after a transient exceeding 1100 steps it repeats with period 140",
                },
                missing=["The 23 live-cell coordinates are not stated."],
                image_witnesses=[prefix + "_page_980_Life_Puffer_Train_Four_Panel_Group.jpeg"],
            ),
        ]
    )
    return records


def route_specs() -> list[tuple[str, str, str, str, list[str]]]:
    """(source unit, literal target, expected topic, kind, candidate names)."""
    return [
        ("U006341", "page 226", "printed source discussion of random-seed pattern densities", "PAGE", ["fair random cellular-automaton initial-condition ensemble"]),
        ("U006341", "page 953", "method for estimating long-run cellular-automaton densities", "PAGE", ["fair random cellular-automaton initial-condition ensemble"]),
        ("U006343", "page 871", "rule-30 triangle-density analysis", "PAGE", []),
        ("U006344", "page 869", "algebraic representation convention for elementary cellular automata", "PAGE", ["elementary cellular automaton rule 22", "elementary cellular automaton rule 126", "elementary cellular automaton rule 150", "elementary cellular automaton rule 182"]),
        ("U006348", "page 232", "printed elementary-rule examples", "PAGE", ["elementary-rule bit-pattern selector"]),
        ("U006348", "page 235", "printed states-of-matter and class-4 discussion", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006348", "page 236", "three-color totalistic class-4 rule 1815 example", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006348", "page 237", "three-color totalistic class-4 rule 2007 example", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006348", "page 282", "three-color totalistic class-4 rule examples 357 and 1329", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006348", "page 597", "deviations among random initial conditions", "PAGE", ["fair random cellular-automaton initial-condition ensemble"]),
        ("U006348", "pages 944 and 1193", "states-of-matter classification context", "PAGE", []),
        ("U006348", "page 70", "totalistic class-4 rule 1599 example", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006348", "page 67", "totalistic class-4 rule 1635 example", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006348", "page 68", "totalistic class-4 rule 2049 example", "PAGE", ["three-color one-dimensional totalistic class-4 preset family"]),
        ("U006350", "page 240", "printed undecidability discussion", "PAGE", ["class-1 no-surviving-pattern decision query"]),
        ("U006350", "page 1138", "undecidability of cellular-automaton class tests", "PAGE", ["class-1 no-surviving-pattern decision query"]),
        ("U006350", "page 244", "printed continuous-cellular-automaton discussion", "PAGE", ["continuously parameterized cellular automaton family"]),
        ("U006350", "page 922", "continuous cellular-automaton mechanics", "PAGE", ["continuously parameterized cellular automaton family"]),
        ("U006351", "page 249", "printed Game of Life construction", "PAGE", ["Game of Life cellular automaton"]),
        ("U006351", "page 877", "Game of Life historical context", "PAGE", []),
        ("U006351", "page 964", "localized structures in Life", "PAGE", ["Game of Life cellular automaton"]),
        ("U006356", "page 183", "cubic lattice convention", "PAGE", ["three-dimensional Life-like cellular automaton family"]),
        ("U006360", "page 154", "random digit sequences for continuous numbers", "PAGE", ["random infinite-sequence initial-condition generator"]),
        ("U006360", "page 1070", "randomness for finite integer representations", "PAGE", ["random infinite-sequence initial-condition generator"]),
        ("U006360", "pages 963 and 1038", "random networks as initial conditions for network systems", "PAGE", ["random infinite-sequence initial-condition generator"]),
        ("U006360", "page 920", "random initial conditions across other system classes", "PAGE", ["random infinite-sequence initial-condition generator"]),
        ("U006362", "page 251", "printed perturbation-propagation properties", "PAGE", ["cellular-automaton difference-pattern observer", "cellular-automaton perturbation-growth Lyapunov analyzer"]),
        ("U006363", "page 601", "one-sided perturbation propagation in rule 30", "PAGE", ["cellular-automaton difference-pattern observer"]),
        ("U006363", "page 871", "rule-30 nonrepetitive-region growth rate", "PAGE", ["cellular-automaton difference-pattern observer"]),
        ("U006365", "page 976", "two-dimensional difference-region shape and Central Limit context", "PAGE", ["cellular-automaton difference-pattern observer", "two-k-color cellular-automaton difference-emulation lift"]),
        ("U006367", "page 155", "exponential sensitivity analogy", "PAGE", ["cellular-automaton perturbation-growth Lyapunov analyzer"]),
        ("U006367", "page 921", "Lyapunov exponents for number-based dynamical systems", "PAGE", ["cellular-automaton perturbation-growth Lyapunov analyzer"]),
        ("U006369", "page 255", "printed cyclic-addition construction", "PAGE", ["cyclic addition dot system"]),
        ("U006369", "page 613", "full-period cyclic-addition parameter pairs", "PAGE", ["cyclic addition dot system"]),
        ("U006372", "page 257", "printed cyclic-multiplication construction", "PAGE", ["cyclic multiplication dot system"]),
        ("U006372", "page 1093", "multiplicative-order mechanics", "PAGE", ["cyclic multiplication dot system"]),
        ("U006372", "page 912", "digit-sequence repetition-period relation", "PAGE", ["cyclic multiplication dot system"]),
        ("U006373", "page 260", "printed maximum-period discussion", "PAGE", ["primitive spatial-period state-count function"]),
        ("U006377", "page 963", "finite cellular-automaton state-count context", "PAGE", ["primitive spatial-period state-count function"]),
        ("U006385", "page 260", "rule-90 repetition-period figure assumptions", "PAGE", ["finite cyclic rule-90 repetition-period bound function"]),
        ("U006386", "page 962", "finite-size period exceptions", "PAGE", ["finite cyclic rule-60 polynomial cellular automaton", "finite cyclic rule-60 repetition-period bound function", "finite-ring cellular-automaton repetition-period comparison survey"]),
        ("U006386", "page 1087", "longest-period comparison across elementary rules and symmetries", "PAGE", ["finite-ring cellular-automaton repetition-period comparison survey"]),
        ("U006388", "page 865", "bitwise cellular-automaton representation", "PAGE", ["finite cellular-automaton boundary implementation codec"]),
        ("U006390", "page 263", "printed rule-22 and rule-225 discussion", "PAGE", ["elementary cellular automaton rule 22", "rule-22 randomness-producing seed family", "elementary cellular automaton rule 225"]),
        ("U006390", "page 58", "single-cell rule-225 nested pattern", "PAGE", ["elementary cellular automaton rule 225"]),
        ("U006390", "page 949", "rule-22 difference-region spread rate", "PAGE", ["cellular-automaton perturbation-growth Lyapunov analyzer"]),
        ("U006395", "page 955", "nested patterns from modular-additive rules", "PAGE", ["weighted additive cellular automaton family"]),
        ("U006395", "page 870", "algebraic additive-rule analysis", "PAGE", ["weighted additive cellular automaton family"]),
        ("U006399", "page 1087", "partial additivity", "PAGE", ["weighted additive cellular automaton family"]),
        ("U006400", "page 264", "printed generalized-additivity construction", "PAGE", ["generalized-additive monoid cellular automaton family"]),
        ("U006411", "page 886", "associative rule analogs", "PAGE", ["generalized-additive monoid cellular automaton family"]),
        ("U006411", "page 956", "general associative-rule nesting results", "PAGE", ["generalized-additive monoid cellular automaton family", "associative-operation cellular automaton family"]),
        ("U006413", "page 922", "continuous additive cellular automata", "PAGE", ["irrational-modulus additive cellular automaton"]),
        ("U006413", "page 161", "continuous-function local evolution", "PAGE", ["local linear differential-operator function evolution"]),
        ("U006423", "page 949", "difference-pattern growth estimates", "PAGE", ["independent-cell mean-field density map for cellular automata"]),
        ("U006424", "page 870", "rule-90 superposition cell-count derivation", "PAGE", ["rule-90 density evolution function"]),
        ("U006424", "page 602", "rule-90 density relation", "PAGE", ["rule-90 density evolution function"]),
        ("U006427", "page 339", "contrasting cellular-automaton density response", "PAGE", ["cellular-automaton density-response raster analyzer"]),
        ("U006429", "page 699", "rule-73 independent-region mechanics", "PAGE", ["rule-73 fair-random initial-condition ensemble", "rule-73 no-even-black-block initial-condition filter", "rule-73 period-3 density-oscillation analyzer"]),
        ("U006432", "page 267", "printed repeating-block construction", "PAGE", ["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"]),
        ("U006432", "page 211", "constraint construction for repeating configurations", "PAGE", ["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"]),
        ("U006438", "page 960", "spacetime-entropy growth of period-dividing counts", "PAGE", ["period-dividing cellular-automaton configuration count function"]),
        ("U006439", "page 958", "finite-complement language mechanics", "PAGE", ["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"]),
        ("U006440", "page 700", "additional repeating-configuration examples", "PAGE", ["exact-period-p repeating-configuration constraint for one-dimensional cellular automata"]),
        ("U006441", "pages 281 and 1118", "localized-structure construction", "PAGE", []),
        ("U006441", "page 942", "two-dimensional constraint mechanics", "PAGE", ["two-dimensional repeating-configuration constraint"]),
        ("U006441", "page 1139", "complexity of two-dimensional repeating configurations", "PAGE", ["two-dimensional repeating-configuration constraint"]),
        ("U006441", "page 349", "stripe reduction of two-dimensional configurations", "PAGE", ["two-dimensional repeating-configuration constraint"]),
        ("U006442", "page 150", "iterated-map definition", "PAGE", ["modular multiplication circle map"]),
        ("U006442", "page 914", "continued-fraction map mechanics", "PAGE", ["continued-fraction map"]),
        ("U006445", "page 961", "explicit solutions of polynomial-map periodic points", "PAGE", ["p-return point query for an iterated map"]),
        ("U006448", "page 869", "Cantor-set view of cellular automata", "PAGE", ["Sarkovskii period-implication relation"]),
        ("U006449", "page 269", "printed rule-emulation and renormalization discussion", "PAGE", ["renormalization-group blocking transformation"]),
        ("U006449", "pages 702 and 1118", "rule emulations", "PAGE", []),
        ("U006449", "page 981", "critical-point nesting", "PAGE", ["renormalization-group blocking transformation"]),
        ("U006449", "page 983", "renormalization-group universality", "PAGE", ["renormalization-group blocking transformation"]),
        ("U006450", "page 989", "limits of renormalization for cellular automata", "PAGE", ["renormalization-group blocking transformation"]),
        ("U006451", "page 271", "printed additive-rule self-similarity discussion", "PAGE", ["prime-modulus additive-CA scale self-emulation transform", "additive-cellular-automaton fractal-dimension analyzer"]),
        ("U006451", "page 952", "prime-modulus additive rules", "PAGE", ["prime-modulus additive-CA scale self-emulation transform", "additive-cellular-automaton fractal-dimension analyzer"]),
        ("U006451", "page 870", "additive self-similarity", "PAGE", ["prime-modulus additive-CA scale self-emulation transform"]),
        ("U006457", "page 58", "fractal dimensions of rule-90 and rule-150 histories", "PAGE", ["additive-cellular-automaton fractal-dimension analyzer"]),
        ("U006459", "page 870", "other additive-rule dimensions", "PAGE", ["additive-cellular-automaton fractal-dimension analyzer"]),
        ("U006461", "page 886", "associative cellular-automaton rules", "PAGE", ["associative-operation cellular automaton family"]),
        ("U006468", "page 887", "noncommutative associative example", "PAGE", ["associative-operation cellular automaton family"]),
        ("U006468", "page 952", "generalized-additive implication for nested behavior", "PAGE", ["associative-operation cellular automaton family", "generalized-additive monoid cellular automaton family"]),
        ("U006469", "page 701", "rule-45 nested background seed", "PAGE", ["rule-45 nested-background seed preset"]),
        ("U006469", "page 1186", "pattern-equivalence counts", "PAGE", ["elementary-rule pattern-uniqueness analyzer"]),
        ("U006471", "page 272", "printed nested-initial-condition examples", "PAGE", ["nested-sequence initial-condition family for rule 90"]),
        ("U006471", "page 83", "nested sequence generators", "PAGE", ["nested-sequence initial-condition family for rule 90"]),
        ("U006471", "page 1091", "nested initial-condition details", "PAGE", ["nested-sequence initial-condition family for rule 90"]),
        ("U006474", "page 275", "printed discrete-attractor discussion", "PAGE", []),
        ("U006492", "page 939", "regular-language mechanics", "PAGE", ["regular language"]),
        ("U006492", "page 279", "regular expressions for rule-110 sequence sets", "PAGE", ["regular-expression sequence denotation"]),
        ("U006493", "page 278", "printed finite-network growth properties", "PAGE", ["cellular-automaton image-network growth and maximum-size analyzer"]),
        ("U006493", "page 891", "regular-language and substitution-system connections", "PAGE", []),
        ("U006504", "page 1084", "topological entropy", "PAGE", ["spatial topological-entropy analyzer"]),
        ("U006504", "page 1138", "undecidability of limiting entropy bounds", "PAGE", ["spatial topological-entropy analyzer", "limiting spatial-entropy bound decision query"]),
        ("U006518", "page 83", "substitution-system construction of nested Cantor sets", "PAGE", ["sequence-set to Cantor-set encoding", "finite sequence-network to substitution-system transform"]),
        ("U006518", "page 869", "cellular automata as global state-space maps", "PAGE", ["cellular-automaton surjectivity decision query", "cellular-automaton injectivity, bijectivity, and reversibility decision relation"]),
        ("U006518", "pages 601 and 1087", "additivity criteria for surjectivity", "PAGE", ["cellular-automaton surjectivity decision query"]),
        ("U006518", "page 957", "minimal-automaton surjectivity test", "PAGE", ["cellular-automaton surjectivity decision query"]),
        ("U006518", "page 1085", "surjective cellular-automaton rules used as DES S-box input", "PAGE", ["cellular-automaton surjectivity decision query"]),
        ("U006519", "page 1017", "reversible cellular automata", "PAGE", ["cellular-automaton injectivity, bijectivity, and reversibility decision relation"]),
        ("U006520", "page 1138", "two-dimensional undecidability of injectivity and surjectivity", "PAGE", ["cellular-automaton surjectivity decision query", "cellular-automaton injectivity, bijectivity, and reversibility decision relation"]),
        ("U006527", "page 878", "sliding-block codes as cellular automata", "PAGE", ["full left-shift symbolic dynamical system"]),
        ("U006527", "page 869", "locality and continuity analogy", "PAGE", ["full left-shift symbolic dynamical system"]),
        ("U006530", "page 922", "ordinary differential-equation attractors", "PAGE", []),
        ("U006531", "pages 920 and 955", "logistic-map attractor progression", "PAGE", ["polynomial iterated-map family"]),
        ("U006531", "page 938", "Turing-machine accept-state grammars", "PAGE", []),
        ("U006531", "page 255", "cyclic-addition state graphs", "PAGE", ["finite global-state transition graph"]),
        ("U006533", "page 257", "cyclic-multiplication state graphs", "PAGE", ["finite global-state transition graph"]),
        ("U006542", "page 1087", "large finite cellular-automaton state graphs", "PAGE", ["finite global-state transition graph"]),
        ("U006546", "page 950", "spatial-period state counts", "PAGE", ["left-shift cellular automaton rule 170", "shift-rule necklace-cycle count function", "shift-rule exact-cycle-length count function"]),
        ("U006548", "page 950", "primitive spatial-period count used for exact shift cycles", "PAGE", ["shift-rule exact-cycle-length count function", "primitive spatial-period state-count function"]),
        ("U006550", "page 975", "shift-rule cycle factors", "PAGE", ["left-shift cellular automaton rule 170", "shift-rule exact-cycle-length count function"]),
        ("U006552", "page 951", "cycle lengths of finite additive cellular automata", "PAGE", ["finite global-state transition graph"]),
        ("U006558", "page 283", "printed code-20 survival data", "PAGE", ["code-20 initial-condition survival-time analyzer"]),
        ("U006560", "page 290", "rule-110 periodic background", "PAGE", ["rule-110 periodic background field"]),
        ("U006562", "page 292", "printed rule-110 persistent structures", "PAGE", ["rule-110 persistent-structure seed preset survey"]),
        ("U006569", "page 290", "parallel copies of rule-110 persistent structures", "PAGE", ["rule-110 collision-based structure extension transform"]),
        ("U006570", "page 293", "printed rule-110 glider-gun seed", "PAGE", ["rule-110 glider-gun initial condition"]),
        ("U006570", "page 294", "printed rule-110 collision invariant", "PAGE", ["rule-110 collision width-conservation modulo-14 relation"]),
        ("U006570", "page 949", "Game of Life native rule", "PAGE", ["Game of Life cellular automaton"]),
        ("U006586", "page 263", "rule-22 history from an infinite-line Life seed", "PAGE", ["infinite-line Game of Life seed"]),
        ("U006587", "page 287", "code-1329 spacefiller analog", "PAGE", ["Game of Life spacefiller"]),
        ("U006591", "page 888", "persistent structures in Turing machines", "PAGE", []),
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_cell(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", nargs="?", default="/tmp/goal4-stage10-notes")
    parser.add_argument("--output")
    args = parser.parse_args()
    bundle = Path(args.bundle).resolve()
    output_path = Path(args.output).resolve() if args.output else bundle / "output/output.json"

    reading_rows = list(csv.DictReader((bundle / "input/reading-input.csv").open(newline="", encoding="utf-8")))
    asset_rows = list(csv.DictReader((bundle / "input/asset-input.csv").open(newline="", encoding="utf-8")))
    units = [json.loads(line) for line in (bundle / "input/source-units.jsonl").read_text(encoding="utf-8").splitlines()]
    unit_by_id = {unit["id"]: unit for unit in units}
    assert len(reading_rows) == len(units) == 253
    assert len(asset_rows) == 72
    assert [row["source_unit_id"] for row in reading_rows] == [unit["id"] for unit in units]

    specs = candidate_specs()
    for index, item in enumerate(specs, 1):
        item["id"] = f"W{index:04d}"
    assert len(specs) == 120
    by_name = {item["name"]: item for item in specs}
    assert len(by_name) == len(specs)

    routes: list[dict[str, str]] = []
    route_names_by_unit: dict[str, list[str]] = {}
    route_ids_by_candidate: dict[str, list[str]] = {item["id"]: [] for item in specs}
    route_ordinals: dict[str, int] = {}
    for index, (unit, literal, topic, kind, names) in enumerate(route_specs(), 1):
        assert unit in unit_by_id
        route_id = f"WR{index:04d}"
        route_ordinals[unit] = route_ordinals.get(unit, 0) + 1
        page_numbers = [int(part) for part in literal.replace("pages", "page").replace("and", " ").replace(",", " ").split() if part.isdigit()]
        within = bool(page_numbers) and all(221 <= n <= 294 or 962 <= n <= 980 for n in page_numbers)
        routes.append(
            {
                "route_id": route_id,
                "source_unit_id": unit,
                "source_asset_id": "",
                "discovery_epoch": "2",
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": unit,
                "discovery_ordinal": str(route_ordinals[unit]),
                "literal_target": literal,
                "route_kind": kind,
                "expected_topic": topic,
                "owning_stage": "10",
                "closure_scope": "WITHIN_STAGE" if within else "CROSS_RANGE",
                "status": "PENDING",
                "target_unit_ids": json_cell([]),
                "target_asset_ids": json_cell([]),
                "attempts": json_cell(["Target not opened in this isolated sequential-review bundle; coordinator routing required."]),
                "vocabulary_terms": json_cell(list(dict.fromkeys(term for term in topic.replace("-", " ").split() if len(term) > 3))[:8]),
                "defect_boundary": "",
            }
        )
        route_names_by_unit.setdefault(unit, []).append(route_id)
        for name in names:
            route_ids_by_candidate[by_name[name]["id"]].append(route_id)

    candidates: list[dict[str, Any]] = []
    candidate_ids_by_unit: dict[str, list[str]] = {}
    anchor_candidate_ids_by_unit: dict[str, list[str]] = {}
    evidence_claims_by_unit: dict[str, list[str]] = {}
    candidate_ids_by_asset: dict[str, list[str]] = {}
    asset_by_path = {row["physical_path"]: row for row in asset_rows}
    route_by_id = {row["route_id"]: row for row in routes}
    def field_unknown_reason(field: str) -> str:
        label = field.replace("_", " ")
        return f"The in-scope source does not fix the candidate's {label}."

    # Complete provenance first, then allocate WE/WG IDs in the bundle's
    # frozen document-first traversal. Images follow all source units in the
    # sealed bundle's discovery order.
    raw_evidence: list[tuple[int, int, int, dict[str, Any], dict[str, Any]]] = []
    unit_order = {unit["id"]: index for index, unit in enumerate(units, 1)}
    image_order = {
        row["physical_path"]: len(units) + index
        for index, row in enumerate(asset_rows, 1)
    }
    for candidate_index, item in enumerate(specs, 1):
        augmented = [dict(record) for record in item["evidence"]]
        anchor_id = item["anchor"]
        assert anchor_id in unit_by_id
        if anchor_id not in {record["unit"] for record in augmented}:
            augmented.append(
                ev(
                    anchor_id,
                    "PROSE",
                    "DIRECT_IDENTITY",
                    f"The source unit directly introduces {item['name']}.",
                    ["object_kind"],
                )
            )
        for route_id in route_ids_by_candidate[item["id"]]:
            route_unit = route_by_id[route_id]["source_unit_id"]
            if route_unit not in {record["unit"] for record in augmented}:
                augmented.append(
                    ev(
                        route_unit,
                        "CROSS_REFERENCE",
                        "LEAD_ONLY",
                        f"The unit supplies {route_by_id[route_id]['literal_target']} as a route for {item['name']}.",
                        [],
                    )
                )
        for image_path in item["image_witnesses"]:
            assert image_path in asset_by_path
            if image_path not in {record["image"] for record in augmented if record["image"]}:
                image_unit = asset_by_path[image_path]["source_unit_id"]
                assert image_unit in unit_by_id
                augmented.append(
                    ev(
                        image_unit,
                        "IMAGE",
                        "CONTEXTUAL",
                        f"Original-resolution inspection confirms the bundled visual witness for {item['name']}.",
                        [],
                        image_path,
                    )
                )
        for local_index, evidence in enumerate(augmented, 1):
            order = image_order[evidence["image"]] if evidence["image"] else unit_order[evidence["unit"]]
            raw_evidence.append((order, candidate_index, local_index, item, evidence))
        item["evidence"] = augmented

    raw_evidence.sort(key=lambda entry: (entry[0], entry[1], entry[2]))
    group_by_candidate: dict[str, str] = {}
    anchor_ordinal: dict[tuple[str, str], int] = {}
    evidence_by_candidate: dict[str, list[dict[str, Any]]] = {item["id"]: [] for item in specs}
    for evidence_index, (_, _, _, item, evidence) in enumerate(raw_evidence, 1):
        if item["id"] not in group_by_candidate:
            group_by_candidate[item["id"]] = f"WG{len(group_by_candidate) + 1:06d}"
        anchor_kind = "IMAGE" if evidence["image"] else "SOURCE_UNIT"
        anchor_id = evidence["image"] or evidence["unit"]
        key = (anchor_kind, anchor_id)
        anchor_ordinal[key] = anchor_ordinal.get(key, 0) + 1
        evidence["_evidence_id"] = f"WE{evidence_index:06d}"
        evidence["_group_id"] = group_by_candidate[item["id"]]
        evidence["_anchor_kind"] = anchor_kind
        evidence["_anchor_id"] = anchor_id
        evidence["_anchor_ordinal"] = anchor_ordinal[key]
        evidence_by_candidate[item["id"]].append(evidence)
    evidence_counter = len(raw_evidence)
    group_counter = len(group_by_candidate)
    assert group_counter == len(specs)

    for item in specs:
        group_id = group_by_candidate[item["id"]]
        source_evidence: list[dict[str, Any]] = []
        evidence_by_field: dict[str, list[str]] = {field: [] for field in FIELDS}
        source_units: list[str] = []
        for evidence in sorted(
            evidence_by_candidate[item["id"]],
            key=lambda record: record["_evidence_id"],
        ):
            evidence_id = evidence["_evidence_id"]
            source_unit = evidence["unit"]
            assert source_unit in unit_by_id
            if source_unit not in source_units:
                source_units.append(source_unit)
            if evidence["image"]:
                assert evidence["image"] in asset_by_path
                asset_id = asset_by_path[evidence["image"]]["asset_id"]
                candidate_ids_by_asset.setdefault(asset_id, []).append(item["id"])
            record = {
                "evidence_id": evidence_id,
                "evidence_group_id": group_id,
                "discovery_anchor": {
                    "epoch": 2,
                    "kind": evidence["_anchor_kind"],
                    "id": evidence["_anchor_id"],
                    "ordinal": evidence["_anchor_ordinal"],
                },
                "source_unit_id": source_unit,
                "image_path": evidence["image"],
                "strength": evidence["strength"],
                "modality": evidence["modality"],
                "claim": evidence["claim"],
                "fingerprint_fields": list(dict.fromkeys(evidence["fields"])),
            }
            source_evidence.append(record)
            for field in record["fingerprint_fields"]:
                evidence_by_field[field].append(evidence_id)
            candidate_ids_by_unit.setdefault(source_unit, []).append(item["id"])
            evidence_claims_by_unit.setdefault(source_unit, []).append(evidence["claim"])
        anchor_id = item["anchor"]
        assert anchor_id in unit_by_id
        anchor_kind = "SOURCE_UNIT"
        anchor_candidate_ids_by_unit.setdefault(anchor_id, []).append(item["id"])

        values = dict(PROFILES[item["profile"]])
        values.update(item["values"])
        if (item["parameters"] or item["variants"]) and "parameters_and_variants" not in values:
            entries = [
                f"{name}: {description}"
                for name, description in item["parameters"] + item["variants"]
            ]
            values["parameters_and_variants"] = "; ".join(entries)
        na_fields = set(PROFILE_NA.get(item["profile"], set()))
        unsupported_declarations = {
            field
            for record in source_evidence
            for field in record["fingerprint_fields"]
            if field not in values and field not in na_fields
        }
        assert not unsupported_declarations, (
            item["id"],
            item["name"],
            sorted(unsupported_declarations),
        )
        fingerprint: dict[str, dict[str, Any]] = {}
        field_support: dict[str, str] = {}
        missing_mechanics: list[str] = list(item["missing"])
        strength_rank = {
            "DIRECT_COMPLETE_MECHANICS": 0,
            "DIRECT_PARTIAL_MECHANICS": 1,
            "DIRECT_IDENTITY": 2,
            "DEFECT_LIMITED": 3,
            "CORROBORATING": 4,
            "CONTEXTUAL": 5,
        }
        primary_evidence = min(
            source_evidence,
            key=lambda record: (
                record["modality"] == "IMAGE",
                strength_rank.get(record["strength"], 9),
                int(record["evidence_id"][2:]),
            ),
        )
        primary_evidence_id = primary_evidence["evidence_id"]
        for field in FIELDS:
            if field == "evidence_limit":
                fingerprint[field] = {
                    "status": "SUPPORTED",
                    "value": "limited to the sealed Chapter 6 Notes source units and reviewed assets listed on this candidate record",
                    "evidence_ids": [primary_evidence_id],
                    "reason": "",
                }
            elif field in values and evidence_by_field[field]:
                fingerprint[field] = {
                    "status": "SUPPORTED",
                    "value": values[field],
                    "evidence_ids": evidence_by_field[field],
                    "reason": "",
                }
            elif field in na_fields:
                fingerprint[field] = {
                    "status": "NOT_APPLICABLE",
                    "value": None,
                    "evidence_ids": [primary_evidence_id],
                    "reason": f"The {field} field is not part of the native semantics of this source-defined {item['profile']} object.",
                }
            else:
                reason = field_unknown_reason(field)
                fingerprint[field] = {
                    "status": "UNKNOWN_FROM_SOURCE",
                    "value": None,
                    "evidence_ids": [],
                    "reason": reason,
                }
                if reason not in missing_mechanics:
                    missing_mechanics.append(reason)
        # The frozen contract requires both NOT_APPLICABLE judgments and the
        # record-level evidence boundary to be evidence-justified.  Attach
        # those semantic judgments once to the strongest non-image native
        # identity/mechanics row, then rebuild every evidence/field join
        # exactly.  Contextual and lead-in rows remain narrow.
        for record in source_evidence:
            record["fingerprint_fields"] = [
                field
                for field in FIELDS
                if record["evidence_id"] in fingerprint[field]["evidence_ids"]
            ]
        strengths = list(dict.fromkeys(record["strength"] for record in source_evidence))
        parameter_evidence_ids = evidence_by_field["parameters_and_variants"]
        if item["parameters"] or item["variants"]:
            assert parameter_evidence_ids, (
                item["id"],
                item["name"],
                "structured parameters/variants lack source evidence",
            )
        parameters = [
            {"name": name, "source_description": description, "evidence_ids": [parameter_evidence_ids[0]]}
            for name, description in item["parameters"]
        ]
        variants = [
            {"name": name, "source_description": description, "evidence_ids": [parameter_evidence_ids[0]]}
            for name, description in item["variants"]
        ]
        candidates.append(
            {
                "id": item["id"],
                "record_status": "ACTIVE",
                "provisional_name": item["name"],
                "aliases": item["aliases"],
                "discovery_stage": 10,
                "discovery_anchor": {
                    "epoch": 2,
                    "kind": anchor_kind,
                    "id": anchor_id,
                    "ordinal": item["ordinal"],
                },
                "source_unit_ids": source_units,
                "source_evidence": source_evidence,
                "source_status": [item["status"]],
                "image_witnesses": item["image_witnesses"],
                "evidence_strength": strengths,
                "field_support": {field: fingerprint[field]["status"] for field in FIELDS},
                "fingerprint": fingerprint,
                "parameters": parameters,
                "variants": variants,
                "missing_mechanics": missing_mechanics,
                "uncertainties": item["uncertainties"],
                "related_candidate_ids": [
                    {
                        "candidate_id": by_name[name]["id"],
                        "relation": "SOURCE_COMPARE",
                        "proof_kind": "PROVISIONAL_COMPARISON",
                        "evidence_ids": [primary_evidence_id],
                        "before_rationale": "",
                        "after_rationale": "",
                        "uncertainty": "The records are source-linked for comparison but preserve distinct mechanics and result kinds.",
                    }
                    for name in item["related"]
                ],
                "cross_reference_ids": route_ids_by_candidate[item["id"]],
                "evidence_reassignments": [],
            }
        )

    # Link candidate image witnesses even when the image evidence is contextual
    # and its discovery anchor remains the source unit.
    for item in specs:
        for path in item["image_witnesses"]:
            asset = asset_by_path[path]
            candidate_ids_by_asset.setdefault(asset["asset_id"], []).append(item["id"])

    image_unit_to_asset = {
        row["source_unit_id"]: row["asset_id"]
        for row in asset_rows
        if row["reference_status"] == "REFERENCED"
    }
    reading_updates: list[dict[str, str]] = []
    defect_units = {
        "U006425": "The extracted rule-90 density formula has a parenthesis placement that prevents a reliable transcription.",
        "U006514": "The printed set-entropy expression omits a logarithm; with full support it becomes k^n/n and diverges instead of yielding the stated finite topological entropy.",
        "U006516": "The printed generalized q-entropy denominator q-1 gives -1 for the uniform distribution, contradicting the following unit's stated maximum +1.",
        "U006517": "The stated generalized q-entropy maximum +1 and monotonicity conflict with the sign of the formula printed in U006516.",
    }
    historical_units = {"U006527", "U006528", "U006529"}
    cross_only_units = {"U006440", "U006448", "U006520", "U006591"}
    for row, unit in zip(reading_rows, units):
        updated = dict(row)
        unit_id = row["source_unit_id"]
        candidate_ids = list(dict.fromkeys(candidate_ids_by_unit.get(unit_id, [])))
        if unit_id in image_unit_to_asset:
            candidate_ids.extend(candidate_ids_by_asset.get(image_unit_to_asset[unit_id], []))
            candidate_ids = list(dict.fromkeys(candidate_ids))
        route_ids = route_names_by_unit.get(unit_id, [])
        anchor_ids = anchor_candidate_ids_by_unit.get(unit_id, [])
        text = (bundle / "input/sources" / unit["path"]).read_bytes()[unit["byte_start"] : unit["byte_end"]].decode("utf-8")
        if unit_id in defect_units:
            disposition = "SOURCE_DEFECT_OR_AMBIGUITY"
            source_status = "DEFECTIVE"
            uncertainty = defect_units[unit_id]
            roles = ["SOURCE_DEFECT", "OBSERVER_OR_ANALYZER"]
        elif unit["block_kind"] == "heading":
            disposition = "NO_CONSTRUCTION"
            source_status = "CLEAR"
            uncertainty = ""
            roles = []
        elif anchor_ids:
            disposition = "CANDIDATE"
            source_status = "CLEAR"
            uncertainty = ""
            roles = []
        elif candidate_ids:
            disposition = "SUPPORTS_CANDIDATE"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["REPRESENTATION"] if unit["block_kind"] == "image" else (["IMPLEMENTATION_DETAIL"] if unit["block_kind"] in {"fenced_code", "table"} else [])
        elif unit_id in historical_units or text.lstrip().startswith("■ **History.**"):
            disposition = "HISTORICAL_ONLY"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["HISTORICAL_MENTION"]
        elif route_ids and unit_id in cross_only_units:
            disposition = "CROSS_REFERENCE"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["EXTERNAL_ONLY"]
        else:
            disposition = "REPRESENTATION_OR_OBSERVER"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["OBSERVER_OR_ANALYZER"]
        statements = evidence_claims_by_unit.get(unit_id, [])
        if statements:
            evidence_statement = " ".join(dict.fromkeys(statements))
        elif route_ids:
            evidence_statement = "The unit supplies construction-relevant routes for coordinator resolution."
        elif unit["block_kind"] == "heading":
            evidence_statement = "Section heading only; adjacent units carry the construction evidence."
        elif unit["block_kind"] == "image":
            evidence_statement = "The image was inspected as a representation or observer output; it introduces no independently anchored native law."
        elif disposition == "HISTORICAL_ONLY":
            evidence_statement = "The unit records provenance or terminology without adding a native law."
        else:
            evidence_statement = "Complete in-context reading records a property, outcome, implementation note, or observer statement rather than a new native law."
        updated.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "2",
                "review_disposition": disposition,
                "source_status": source_status,
                "uncertainty": uncertainty,
                "secondary_roles": json_cell(roles),
                "candidate_ids": json_cell(candidate_ids),
                "route_ids": json_cell(route_ids),
                "evidence_statement": evidence_statement,
                "review_stage": "10",
                "reviewer": "ch06-notes",
            }
        )
        reading_updates.append(updated)

    text_bearing_assets = {
        "A000589", "A000590", "A000591", "A000592", "A000593", "A000594",
        "A000596", "A000597", "A000599", "A000600", "A000601", "A000602",
        "A000603", "A000604", "A000605", "A000606", "A000607", "A000608",
        "A000610", "A000611", "A000612", "A000613", "A000614", "A000616",
        "A000617", "A000618", "A000619", "A000620", "A000621", "A000622",
        "A000623", "A000624", "A000625", "A000626", "A000627", "A000628",
        "A000629", "A000630", "A000631", "A000632", "A000633", "A000634",
        "A000635", "A000636", "A000637", "A000638", "A000639", "A000640",
        "A000642", "A000644", "A000645", "A000646", "A000647", "A000648",
        "A000649", "A000650", "A000651", "A000652", "A000653", "A000654",
        "A000655", "A000656", "A000657", "A000658", "A000659", "A000660",
    }
    referenced_visual_roles = {
        **{
            asset_id: "NATIVE_EVIDENCE"
            for asset_id in {"A000608", "A000639", "A000640", "A000643", "A000645"}
        },
        **{
            asset_id: "OBSERVER"
            for asset_id in {
                "A000589", "A000590", "A000595", "A000596", "A000597",
                "A000598", "A000599", "A000609", "A000612", "A000613",
                "A000614", "A000615", "A000616", "A000617", "A000618",
                "A000622", "A000638", "A000642", "A000644", "A000646",
                "A000647", "A000658", "A000659",
            }
        },
        **{
            asset_id: "RELATION"
            for asset_id in {
                "A000610", "A000611", "A000623", "A000624", "A000625",
                "A000626", "A000627", "A000628", "A000629", "A000630",
                "A000633", "A000636", "A000637", "A000641",
            }
        },
    }
    assert len(referenced_visual_roles) == 42
    native_asset_statements = {
        "A000590": "Original-resolution inspection checked the four pie charts as a bounded survey of behavior-class frequencies for the displayed one-dimensional totalistic rule spaces.",
        "A000595": "Original-resolution inspection checked the successive evolution frames of the moving structure under the {4,5,5} three-dimensional Life-like rule described by the adjacent source units.",
        "A000597": "Original-resolution inspection checked the plotted finite-ring repetition-period comparison for the elementary-rule families named by the adjacent source unit.",
        "A000598": "Original-resolution inspection checked the figure as a visual history accompanying the rule-225 seed variants and behavior described by the adjacent source unit.",
        "A000609": "Original-resolution inspection checked the pictured nested histories as examples of the weighted modulo-k additive cellular-automaton family described by the adjacent source unit.",
        "A000614": "Original-resolution inspection checked the density-response rasters against the stated initial-density, successive-step, and gray-level axes for rules 236, 126, and 30.",
        "A000615": "Original-resolution inspection checked the pictured region decomposition and repeating behavior accompanying the period-3 density oscillations of rule 73 described by the adjacent source unit.",
        "A000617": "Original-resolution inspection checked the sorted configuration comparison across all 256 elementary rules as the visual witness for the pattern-uniqueness analyzer.",
        "A000638": "Original-resolution inspection checked the survival-time display for the first 1000 code-20 initial conditions against the adjacent source description.",
        "A000641": "Original-resolution inspection checked the displayed catalogue against the stated criterion: fewer than eight live cells and no change under a Life step.",
        "A000642": "Original-resolution inspection checked the labeled Life examples as an observer survey of more complicated repetitive and moving structures; the adjacent prose supplies no coordinate-level seeds or separate mechanics, so the panel remains deliberately noncandidate.",
        "A000643": "Original-resolution inspection checked the pictured rule-110 background against the adjacent source unit's repeated 14-cell block and step-dependent displacement description.",
    }
    asset_updates: list[dict[str, str]] = []
    for row in asset_rows:
        updated = dict(row)
        asset_id = row["asset_id"]
        candidate_ids = list(dict.fromkeys(candidate_ids_by_asset.get(asset_id, [])))
        if row["reference_status"] == "UNREFERENCED_PHYSICAL":
            status = "AMBIGUOUS"
            role = "SOURCE_DEFECT"
            uncertainty = "No live markdown anchor or caption exists; original-resolution comparison shows a crop duplicated from a referenced page composite, but no canonical unit owns it."
            evidence_statement = "Original-resolution inspection identifies an orphaned duplicate/crop fragment; it contributes no independent candidate mechanics."
            risks = ["AMBIGUOUS", "CAPTION_INCOMPLETE"]
        else:
            status = "CLEAR"
            role = referenced_visual_roles[asset_id]
            uncertainty = ""
            evidence_statement = native_asset_statements.get(
                asset_id,
                "Original-resolution inspection checked the complete referenced figure against its bundled prose context.",
            )
            risks = ["CONSTRUCTION_BEARING"]
            if asset_id in text_bearing_assets:
                risks.append("TEXT_BEARING")
            if not row["link_id"]:
                risks.append("CAPTION_INCOMPLETE")
        source_unit = row["source_unit_id"]
        route_ids = route_names_by_unit.get(source_unit, []) if source_unit else []
        updated.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "2",
                "visual_role": role,
                "source_status": status,
                "risk_flags": json_cell(risks),
                "original_resolution_status": "REVIEWED",
                "transcription_status": (
                    "CHECKED"
                    if role == "NATIVE_EVIDENCE" or asset_id in text_bearing_assets
                    else "NOT_REQUIRED"
                ),
                "candidate_ids": json_cell(candidate_ids),
                "route_ids": json_cell(route_ids),
                "evidence_statement": evidence_statement,
                "review_stage": "10",
                "reviewer": "ch06-notes",
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append(updated)

    reading_status_by_unit = {
        row["source_unit_id"]: row["source_status"] for row in reading_updates
    }
    asset_status_by_path = {
        row["physical_path"]: row["source_status"] for row in asset_updates
    }
    status_order = {"CLEAR": 0, "DEFECTIVE": 1, "AMBIGUOUS": 2}
    for candidate in candidates:
        provenance_statuses = {
            reading_status_by_unit[unit_id]
            for unit_id in candidate["source_unit_ids"]
        } | {
            asset_status_by_path[image_path]
            for image_path in candidate["image_witnesses"]
        }
        candidate["source_status"] = sorted(
            provenance_statuses,
            key=lambda status: (status_order.get(status, 99), status),
        )

    # Freeze the semantic repairs that motivated this pass.  These checks are
    # deliberately phrased over the completed worker records so a later edit
    # cannot silently reintroduce candidate-wide evidence stamping, weak-only
    # native support, or observer images promoted to native evidence.
    asset_update_by_path = {
        row["physical_path"]: row for row in asset_updates
    }
    assert {
        role: sum(row["visual_role"] == role for row in asset_updates)
        for role in {"NATIVE_EVIDENCE", "OBSERVER", "RELATION", "SOURCE_DEFECT"}
    } == {
        "NATIVE_EVIDENCE": 5,
        "OBSERVER": 23,
        "RELATION": 14,
        "SOURCE_DEFECT": 30,
    }
    a642 = next(row for row in asset_updates if row["asset_id"] == "A000642")
    assert a642["visual_role"] == "OBSERVER"
    assert json.loads(a642["candidate_ids"]) == []
    weak_strengths = {"CONTEXTUAL", "CORROBORATING", "LEAD_ONLY"}
    for candidate in candidates:
        evidence_by_id = {
            row["evidence_id"]: row for row in candidate["source_evidence"]
        }
        boundary = candidate["fingerprint"]["evidence_limit"]
        assert boundary["status"] == "SUPPORTED"
        assert len(boundary["evidence_ids"]) == 1
        assert sum(
            "evidence_limit" in row["fingerprint_fields"]
            for row in candidate["source_evidence"]
        ) == 1
        for field, value in candidate["fingerprint"].items():
            if value["status"] == "SUPPORTED":
                assert value["evidence_ids"]
                assert not all(
                    evidence_by_id[evidence_id]["strength"] in weak_strengths
                    for evidence_id in value["evidence_ids"]
                ), (candidate["id"], field)
            elif value["status"] == "NOT_APPLICABLE":
                assert len(value["evidence_ids"]) == 1
        for row in candidate["source_evidence"]:
            if row["strength"] == "LEAD_ONLY":
                assert row["fingerprint_fields"] == []
            if row["strength"] == "CONTEXTUAL":
                assert len(row["fingerprint_fields"]) <= 2
            if row["image_path"] and row["strength"].startswith("DIRECT"):
                asset = asset_update_by_path[row["image_path"]]
                assert asset["visual_role"] == "NATIVE_EVIDENCE"
                assert asset["original_resolution_status"] == "REVIEWED"
                assert asset["transcription_status"] == "CHECKED"

    manifest = bundle / "allowed-manifest.json"
    prompt = bundle / "input/brief.md"
    output_schema = bundle / "input/schemas/worker-output.schema.json"
    result = {
        "allowed_manifest_sha256": sha256(manifest),
        "asset_updates": asset_updates,
        "bundle_sha256": "84c3dd2b8cbdfd3162bf5ab974e73e5f71cae0c053334131c139b3228f2dc6ce",
        "candidate_proposals": candidates,
        "prohibited_input_nonuse": True,
        "prompt_sha256": sha256(prompt),
        "reading_updates": reading_updates,
        "route_proposals": routes,
        "schema_sha256": "0dc082f9e1e434ca8c6c1839320044a89a18772c6179d831940fc35dd5955a17",
        "uncertainties": [
            "U006425: the extracted rule-90 density formula is parenthesized inconsistently with its prose description; no page image is present in the sealed bundle.",
            "U006514: the printed set-entropy expression lacks a logarithm; for full support it is k^n/n and diverges instead of yielding the finite set/topological entropy named in U006515.",
            "U006516–U006517: the printed q-entropy denominator q-1 evaluates to -1 for the stated uniform distribution, contradicting the following prose's asserted maximum +1.",
            "U006429: the no-even-black-block restriction is stated semantically, but the source does not formalize the block-boundary convention or a sampler.",
            "All 30 unreferenced physical images are uncaptained crops duplicated from referenced page composites; they were inspected at original resolution but cannot be assigned a canonical source unit.",
            "Several Life structure records have direct identity and behavior anchors but lack coordinate-level seed transcriptions in the source.",
        ],
        "worker_id": "ch06-notes",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "assets": len(asset_updates),
                "candidates": len(candidates),
                "evidence": evidence_counter,
                "groups": group_counter,
                "output": str(output_path),
                "routes": len(routes),
                "sha256": sha256(output_path),
                "units": len(reading_updates),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
