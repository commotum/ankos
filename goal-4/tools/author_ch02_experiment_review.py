#!/usr/bin/env python3
"""Record the completed, source-grounded Stage 6 Chapter 2 review.

This authoring helper is deliberately bound to the exact sealed epoch-1
Chapter 2 bundle.  It records judgments made only after the paired sources
were read sequentially and every assigned image was inspected at
source-preserving resolution.  It refuses to overwrite anything other than
the pristine nonsemantic worksheet.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

import prepare_review_output
from audit_contract import CANDIDATE_FIELDS, FINGERPRINT_FIELDS, canonical_json_bytes


EXPECTED_CONTENT_SET = (
    "55d8db98f8ae082cc1f605aaead6f8e2c0d5cda16ad4e3867cc1cb1cecf3031d"
)
EXPECTED_WORKER = "ch02-experiment-reader-e1"
EXPECTED_PATHS = [
    "CHAPTERS/02-The-Crucial-Experiment.md",
    "BACK-MATTER/NOTES/02-The-Crucial-Experiment-Notes.md",
]


class AuthoringError(ValueError):
    """The exact Stage 6 assignment or worksheet is not safe to update."""


def compact(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


CandidateSpec = dict[str, Any]
EvidenceSpec = dict[str, Any]
RouteSpec = dict[str, Any]


def add_candidate(
    specs: list[CandidateSpec],
    *,
    key: str,
    name: str,
    anchor: str,
    aliases: list[str],
    facts: dict[str, str],
    missing: str,
    parameters: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    spec: CandidateSpec = {
        "key": key,
        "name": name,
        "anchor": anchor,
        "aliases": aliases,
        "facts": facts,
        "missing": missing,
        "parameters": parameters or [],
        "variants": variants or [],
        "route_keys": route_keys or [],
        "evidence": [],
        "_insertion": len(specs),
    }
    specs.append(spec)
    return spec


def add_evidence(
    candidate: CandidateSpec,
    *,
    label: str,
    unit: str,
    claim: str,
    fields: list[str],
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    modality: str = "PROSE",
    image_path: str | None = None,
) -> None:
    if any(item["label"] == label for item in candidate["evidence"]):
        raise AuthoringError(f"duplicate evidence label {label}")
    candidate["evidence"].append(
        {
            "label": label,
            "unit": unit,
            "image_path": image_path,
            "claim": claim,
            "fields": fields,
            "strength": strength,
            "modality": modality,
            "_insertion": sum(
                len(item["evidence"]) for item in ALL_CANDIDATE_SPECS
            ),
        }
    )


ALL_CANDIDATE_SPECS: list[CandidateSpec] = []


def source_candidate(
    *,
    key: str,
    name: str,
    anchor: str,
    aliases: list[str],
    facts: dict[str, str],
    claim: str,
    missing: str,
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    modality: str = "PROSE",
    parameters: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    spec = add_candidate(
        ALL_CANDIDATE_SPECS,
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases,
        facts=facts,
        missing=missing,
        parameters=parameters,
        variants=variants,
        route_keys=route_keys,
    )
    add_evidence(
        spec,
        label=f"{key}-source",
        unit=anchor,
        claim=claim,
        fields=list(facts),
        strength=strength,
        modality=modality,
    )
    return spec


def ca_preset(
    *,
    key: str,
    name: str,
    anchor: str,
    aliases: list[str],
    rule_text: str,
    seed_text: str,
    result_text: str,
    missing: str,
) -> CandidateSpec:
    facts = {
        "object_kind": "A named one-dimensional binary cellular-automaton preset.",
        "native_time": "Discrete generations, one successive row per step.",
        "carrier": "Cell positions carrying black or white values.",
        "support": "A one-dimensional line of cells.",
        "topology": "Each position has an immediate left and right neighbor.",
        "alphabet_or_value_schema": "Two cell values, black and white.",
        "complete_state": "The current row of black/white cell values.",
        "seed": seed_text,
        "frontier_or_activation": "Every cell position receives a next-step value.",
        "schedule": "All next values are determined from the preceding step.",
        "read_dependencies_or_neighborhood": (
            "The previous values of the immediate left neighbor, the cell "
            "itself, and the immediate right neighbor."
        ),
        "law_kind": "A deterministic local lookup rule.",
        "rule_relation_constraint_function_or_probability_law": rule_text,
        "write_replacement_assembly_or_commit": (
            "The rule replaces each cell value for the next generation from "
            "the old neighborhood values."
        ),
        "result_kind": result_text,
        "successor_cardinality": "Exactly one next row follows from each complete row.",
        "determinism_branching_or_measure": (
            "Deterministic, with no branching or probability in the rule."
        ),
        "parameters_and_variants": (
            "The rule number and initial condition delimit this preset within "
            "the elementary cellular-automaton rule space."
        ),
        "excluded_observers_and_representations": (
            "The retained rows, grids, cropping, visual regularity, and "
            "behavioral descriptions are displays or observations, not extra "
            "native state or laws."
        ),
        "evidence_limit": missing,
    }
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases,
        facts=facts,
        claim=(
            f"The passage delimits {name}, states its local law and its place "
            "in the binary nearest-neighbor cellular-automaton examples."
        ),
        missing=missing,
        parameters=[
            (
                "rule identity",
                f"The source names {name}.",
                [f"{key}-source"],
            )
        ],
        variants=[
            (
                "single-black-cell run",
                seed_text,
                [f"{key}-source"],
            )
        ],
    )


# ---------------------------------------------------------------------------
# Main Chapter 2 candidates, in source discovery order.

experiment = source_candidate(
    key="experiment",
    name="enumerate-and-run simple-program experiment protocol",
    anchor="U000179",
    aliases=["computer experiment on possible simple programs"],
    facts={
        "object_kind": (
            "An experimental protocol that constructs a sequence of possible "
            "simple programs, runs them, and inspects their behavior."
        ),
        "native_time": "Each sampled program is run through successive steps.",
        "carrier": "A collection or sequence of finitely specified programs.",
        "input": "A chosen sequence of possible simple programs.",
        "external_data": "Observed run histories are supplied to the investigator.",
        "law_kind": "Enumeration followed by execution and observation.",
        "result_kind": "A collection of program behaviors for comparison.",
        "parameters_and_variants": (
            "The sampled program class, rule sequence, initial conditions, and "
            "run length are experimental choices."
        ),
        "excluded_observers_and_representations": (
            "The scientific conclusions drawn from the runs are observations, "
            "not part of the programs being sampled."
        ),
        "evidence_limit": (
            "This passage does not give a complete enumeration order, stopping "
            "rule, sampling measure, or classification procedure."
        ),
    },
    claim=(
        "The source explicitly describes setting up a sequence of possible "
        "simple programs, running each, and seeing how it behaves."
    ),
    missing=(
        "This passage does not give a complete enumeration order, stopping "
        "rule, sampling measure, or classification procedure."
    ),
)
add_evidence(
    experiment,
    label="experiment-systematic",
    unit="U005288",
    claim=(
        "The historical account describes a systematic visual survey of a "
        "large collection of cellular automata from random initial conditions."
    ),
    fields=[
        "object_kind",
        "input",
        "external_data",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
)
add_evidence(
    experiment,
    label="experiment-print-series",
    unit="U005289",
    claim=(
        "The source records a high-resolution survey of all k=2, r=1 rules "
        "and particular printed examples, supplying a concrete sampled family."
    ),
    fields=[
        "carrier",
        "input",
        "parameters_and_variants",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
)

eca = source_candidate(
    key="eca-family",
    name="one-dimensional binary nearest-neighbor cellular automaton",
    anchor="U000180",
    aliases=["cellular automaton", "elementary cellular automaton"],
    facts={
        "object_kind": (
            "A parameterized family of one-dimensional binary cellular automata."
        ),
        "native_time": "Discrete synchronous generations.",
        "carrier": "A line of cell positions.",
        "support": "One-dimensional cellular space.",
        "topology": "Immediate left/self/right adjacency.",
        "structural_invariants": (
            "The line of sites and two-value cell schema remain fixed across steps."
        ),
        "alphabet_or_value_schema": "Each cell is black or white.",
        "complete_state": "One complete row of cell colors.",
        "visible_history": (
            "Successive rows can be retained as a visual evolution history."
        ),
        "seed": (
            "The chapter's canonical examples begin with one black center cell "
            "and white elsewhere."
        ),
        "boundary": (
            "The supplied finite implementations use cyclic boundary conditions."
        ),
        "frontier_or_activation": "Every site in the next row is evaluated.",
        "schedule": (
            "All sites read the old generation; sequential implementation must "
            "preserve old values and commits one new generation."
        ),
        "read_dependencies_or_neighborhood": (
            "Old left-neighbor, self, and right-neighbor values."
        ),
        "law_kind": "A uniform local lookup/function applied at every site.",
        "rule_relation_constraint_function_or_probability_law": (
            "A chosen function maps each of the eight binary left/self/right "
            "neighborhoods to one next binary value."
        ),
        "write_replacement_assembly_or_commit": (
            "One replacement value is produced for every site and old values "
            "are preserved until the generation has been determined."
        ),
        "result_kind": "A unique next row and, under iteration, an evolution history.",
        "successor_cardinality": "Exactly one successor row for a fixed rule and state.",
        "determinism_branching_or_measure": (
            "Deterministic; the family varies the lookup but contains no native "
            "branching or probability."
        ),
        "parameters_and_variants": (
            "The binary lookup rule, initial condition, finite/infinite support "
            "profile, cyclic finite boundary, and requested step count vary."
        ),
        "excluded_observers_and_representations": (
            "Raster rows, grids, stored histories, algebraic formulas, Boolean "
            "forms, and implementation optimizations are representations."
        ),
        "evidence_limit": (
            "The conceptual main-text examples do not state an infinite-support "
            "boundary convention or native completion/failure semantics."
        ),
    },
    claim=(
        "The chapter introduces cellular automata as a rule-driven program "
        "class; later adjacent units state the one-dimensional binary "
        "left/self/right schema."
    ),
    missing=(
        "The conceptual main-text examples do not state an infinite-support "
        "boundary convention or native completion/failure semantics."
    ),
    strength="DIRECT_IDENTITY",
)
add_evidence(
    eca,
    label="eca-schema",
    unit="U000185",
    claim=(
        "The source states the line carrier, black/white alphabet, and "
        "left/self/right predecessor dependency for every step."
    ),
    fields=[
        "native_time",
        "carrier",
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "complete_state",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "evidence_limit",
    ],
)
add_evidence(
    eca,
    label="eca-history-seed",
    unit="U000183",
    claim=(
        "The caption states the single-black-cell initial row and successive-row "
        "history convention."
    ),
    fields=[
        "visible_history",
        "seed",
        "result_kind",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CAPTION",
)
add_evidence(
    eca,
    label="eca-old-snapshot",
    unit="U004988",
    claim=(
        "The implementation note explicitly requires every update to read old "
        "neighbor values and describes preserving a snapshot before commit."
    ),
    fields=[
        "schedule",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)
add_evidence(
    eca,
    label="eca-cyclic-boundary",
    unit="U004989",
    claim=(
        "The supplied finite Mathematica and C implementations explicitly use "
        "a cyclic array boundary."
    ),
    fields=[
        "boundary",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)

rule254 = ca_preset(
    key="rule254",
    name="Rule 254 cellular automaton preset",
    anchor="U000183",
    aliases=["cellular automaton rule 254"],
    rule_text=(
        "A cell is black on the next step iff it or either immediate neighbor "
        "was black on the preceding step."
    ),
    seed_text="One black center cell with all other cells white.",
    result_text="A unique expanding evolution uniformly filled with black.",
    missing=(
        "The main source does not state an infinite-support boundary, native "
        "completion/failure, or witness semantics."
    ),
)
add_evidence(
    rule254,
    label="rule254-name-table",
    unit="U000188",
    claim=(
        "The caption identifies the eight-case next-center-cell table as rule 254."
    ),
    fields=[
        "object_kind",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
        "evidence_limit",
    ],
    modality="CAPTION",
)
add_evidence(
    rule254,
    label="rule254-formula",
    unit="U005096",
    claim=(
        "The Notes give the exact binary algebraic expression "
        "1 - (1 - p) (1 - q) (1 - r) for rule 254."
    ),
    fields=[
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="FORMULA",
)

rule250 = ca_preset(
    key="rule250",
    name="Rule 250 cellular automaton preset",
    anchor="U000190",
    aliases=["cellular automaton rule 250"],
    rule_text=(
        "A cell is black iff at least one immediate neighbor was black; the old "
        "self value is ignored."
    ),
    seed_text="One black center cell with white cells elsewhere.",
    result_text="A unique checkerboard-like expanding evolution.",
    missing=(
        "The source does not state an infinite-support boundary, native "
        "completion/failure, or witness semantics."
    ),
)
add_evidence(
    rule250,
    label="rule250-name",
    unit="U000193",
    claim=(
        "The caption repeats the exact neighbor-only law, names rule 250, and "
        "states the single-cell run."
    ),
    fields=list(rule250["facts"]),
    modality="CAPTION",
)
add_evidence(
    rule250,
    label="rule250-formula",
    unit="U005097",
    claim=(
        "The Notes give the exact binary algebraic expression p + r - p r "
        "for rule 250."
    ),
    fields=[
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="FORMULA",
)

rule90 = ca_preset(
    key="rule90",
    name="Rule 90 cellular automaton preset",
    anchor="U000195",
    aliases=["cellular automaton rule 90"],
    rule_text=(
        "A cell is black iff exactly one of its left and right neighbors was "
        "black; equivalently a_i' = Mod[a_(i-1)+a_(i+1),2]."
    ),
    seed_text="One black center cell with white cells elsewhere.",
    result_text="A unique nested triangular evolution.",
    missing=(
        "The source does not state an infinite-support boundary, native "
        "completion/failure, or witness semantics."
    ),
)
add_evidence(
    rule90,
    label="rule90-formula-name",
    unit="U000198",
    claim=(
        "The caption names rule 90, states the exclusive-neighbor law, and gives "
        "its exact modulo-two formula and single-cell run."
    ),
    fields=list(rule90["facts"]),
    modality="CAPTION",
)
add_evidence(
    rule90,
    label="rule90-notes-formula",
    unit="U005094",
    claim=(
        "The Notes independently give the exact modulo-two left-plus-right "
        "formula for rule 90."
    ),
    fields=[
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="FORMULA",
    strength="CORROBORATING",
)

rule30 = ca_preset(
    key="rule30",
    name="Rule 30 cellular automaton preset",
    anchor="U000204",
    aliases=["cellular automaton rule 30"],
    rule_text=(
        "If self and right were both white, copy the old left value; otherwise "
        "write the opposite of the old left value."
    ),
    seed_text="One black center cell with white cells elsewhere.",
    result_text="A unique expanding evolution with an irregular right-hand region.",
    missing=(
        "The source does not state an infinite-support boundary, native "
        "completion/failure, or witness semantics."
    ),
)
add_evidence(
    rule30,
    label="rule30-name-seed",
    unit="U000207",
    claim=(
        "The caption identifies the example as rule 30 and states its "
        "single-black-cell initial condition."
    ),
    fields=[
        "object_kind",
        "seed",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CAPTION",
)
add_evidence(
    rule30,
    label="rule30-algebraic",
    unit="U005098",
    claim=(
        "The Notes give the exact binary algebraic form "
        "Mod[p+q+r+q r,2] for rule 30."
    ),
    fields=[
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="FORMULA",
)

rule110 = ca_preset(
    key="rule110",
    name="Rule 110 cellular automaton preset",
    anchor="U000219",
    aliases=["cellular automaton rule 110"],
    rule_text=(
        "The next cell is black except when left/self/right are all equal, or "
        "when left is black while self and right are white."
    ),
    seed_text="The main run starts from one black cell with white elsewhere.",
    result_text=(
        "A unique evolution containing periodic background and localized structures."
    ),
    missing=(
        "The source does not state an infinite-support boundary, native "
        "completion/failure, or witness semantics."
    ),
)
add_evidence(
    rule110,
    label="rule110-name-seed",
    unit="U000229",
    claim=(
        "The caption names rule 110 and states the single-black-cell 150-step run."
    ),
    fields=[
        "object_kind",
        "seed",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CAPTION",
)
add_evidence(
    rule110,
    label="rule110-algebraic",
    unit="U005099",
    claim=(
        "The Notes give an exact binary algebraic expression for rule 110."
    ),
    fields=[
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="FORMULA",
)


def add_candidate_image(
    candidate: CandidateSpec,
    *,
    label: str,
    unit: str,
    path: str,
    claim: str,
    fields: list[str],
    strength: str = "CORROBORATING",
) -> None:
    add_evidence(
        candidate,
        label=label,
        unit=unit,
        image_path=path,
        claim=claim,
        fields=fields,
        strength=strength,
        modality="IMAGE",
    )


add_candidate_image(
    eca,
    label="eca-neighborhood-image",
    unit="U000184",
    path="CHAPTERS/_page_39_Figure_4.jpeg",
    claim=(
        "Original-resolution inspection confirms a one-dimensional row and "
        "left/self/right neighborhood schematic; the prose supplies semantics."
    ),
    fields=[
        "carrier",
        "support",
        "topology",
        "read_dependencies_or_neighborhood",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)
for candidate, label, unit, path, rule_name in [
    (
        rule254,
        "rule254-table-image",
        "U000187",
        "CHAPTERS/_page_39_Picture_7.jpeg",
        "rule 254",
    ),
    (
        rule250,
        "rule250-table-image",
        "U000192",
        "CHAPTERS/_page_40_Picture_2.jpeg",
        "rule 250",
    ),
    (
        rule90,
        "rule90-table-image",
        "U000197",
        "CHAPTERS/_page_40_Rule_90.jpeg",
        "rule 90",
    ),
    (
        rule30,
        "rule30-table-image",
        "U000206",
        "CHAPTERS/_page_42_Rule_30.jpeg",
        "rule 30",
    ),
    (
        rule110,
        "rule110-table-image",
        "U000228",
        "CHAPTERS/_page_47_Figure_2.jpeg",
        "rule 110",
    ),
]:
    add_candidate_image(
        candidate,
        label=label,
        unit=unit,
        path=path,
        claim=(
            f"Original-resolution inspection confirms the eight-case "
            f"left/self/right next-cell table displayed for {rule_name}; exact "
            "semantics are independently stated in prose."
        ),
        fields=[
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )


# ---------------------------------------------------------------------------
# Notes candidates: generalized rule profiles, seed/boundary forms, and queries.

general_1d = source_candidate(
    key="general-1d-ca",
    name="general one-dimensional range-r cellular automaton rule schema",
    anchor="U004997",
    aliases=["GeneralCARule", "FunctionCARule", "explicit replacement CA rule"],
    facts={
        "object_kind": (
            "A one-dimensional cellular-automaton family whose local rule is "
            "an explicit replacement list or neighborhood function."
        ),
        "native_time": "Discrete cellular-automaton steps.",
        "carrier": "A one-dimensional list of cells.",
        "support": "A cyclic finite list in the supplied implementation.",
        "topology": "A radius-r interval around each cell.",
        "alphabet_or_value_schema": (
            "Cell values are those accepted and returned by the replacement "
            "rules or function."
        ),
        "complete_state": "The current list of cell values.",
        "boundary": "The supplied Partition/rotation forms use cyclic list boundaries.",
        "frontier_or_activation": "Every cell receives a replacement value.",
        "schedule": "One complete next list is produced from the old list.",
        "read_dependencies_or_neighborhood": (
            "The 2r+1-cell block centered on the target cell."
        ),
        "law_kind": "Explicit block replacements or a function of each block.",
        "rule_relation_constraint_function_or_probability_law": (
            "GeneralCARule replaces each radius-r block by its matching output; "
            "FunctionCARule maps a function over every radius-r block."
        ),
        "write_replacement_assembly_or_commit": (
            "One returned value replaces each target cell in the next list."
        ),
        "result_kind": "A unique next configuration when the rule is total.",
        "parameters_and_variants": (
            "Rule representation, range r, value schema, and finite boundary "
            "profile are variable."
        ),
        "excluded_observers_and_representations": (
            "Wrapper names, Mathematica pattern syntax, Compile, Dispatch, and "
            "rotation/partition code are representations or implementations."
        ),
        "evidence_limit": (
            "The source does not state failure behavior for incomplete or "
            "overlapping replacements, non-cyclic infinite support, or native completion."
        ),
    },
    claim=(
        "The Notes define general 1D CA rules as explicit neighborhood "
        "replacements and then give radius-r replacement and function wrappers."
    ),
    missing=(
        "The source does not state failure behavior for incomplete or "
        "overlapping replacements, non-cyclic infinite support, or native completion."
    ),
    route_keys=["general-rule-page60"],
)
add_evidence(
    general_1d,
    label="general-1d-wrapper-code",
    unit="U005006",
    claim=(
        "The code gives exact ElementaryCARule, GeneralCARule, and "
        "FunctionCARule one-step definitions."
    ),
    fields=[
        "alphabet_or_value_schema",
        "complete_state",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
)
add_evidence(
    general_1d,
    label="general-1d-range",
    unit="U005007",
    claim=(
        "The prose explicitly generalizes the replacement/function forms to r "
        "neighbors on each side."
    ),
    fields=[
        "topology",
        "read_dependencies_or_neighborhood",
        "parameters_and_variants",
        "evidence_limit",
    ],
)

# Coverage-bearing seed and boundary classes stated explicitly in the Notes.
centered_seed = source_candidate(
    key="centered-single-seed",
    name="centered single-black-cell cellular-automaton seed",
    anchor="U004964",
    aliases=["CenterList seed", "single black initial cell"],
    facts={
        "object_kind": "A finitely parameterized cellular-automaton seed class.",
        "carrier": "A finite one-dimensional row of cells.",
        "support": "A row of n cells.",
        "alphabet_or_value_schema": "Binary values 0 (white) and 1 (black).",
        "complete_state": (
            "n white cells with the middle position replaced by one black cell."
        ),
        "seed": "One black cell centered in a length-n white row.",
        "law_kind": "A deterministic initial-state constructor.",
        "rule_relation_constraint_function_or_probability_law": (
            "Create n zeros and replace position Ceiling[n/2] by 1."
        ),
        "result_kind": "One finite binary initial row.",
        "successor_cardinality": "Exactly one seed for each valid positive n.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": "The row length n.",
        "excluded_observers_and_representations": (
            "The CenterList function name and list syntax are implementation notation."
        ),
        "evidence_limit": (
            "The passage does not define behavior for invalid n or independently "
            "choose the boundary used when the seed is evolved."
        ),
    },
    claim=(
        "The Notes explicitly define the centered single-black-cell initial "
        "condition and its binary value encoding."
    ),
    missing=(
        "The passage does not define behavior for invalid n or independently "
        "choose the boundary used when the seed is evolved."
    ),
)
add_evidence(
    centered_seed,
    label="centered-single-seed-code",
    unit="U004965",
    claim=(
        "The code constructs n zeros and replaces the Ceiling[n/2] position by 1."
    ),
    fields=list(centered_seed["facts"]),
    modality="CODE",
)

cyclic_boundary = source_candidate(
    key="cyclic-boundary",
    name="cyclic cellular-automaton boundary class",
    anchor="U004989",
    aliases=["periodic boundary conditions", "cyclic array"],
    facts={
        "object_kind": "A boundary class for finite cellular arrays.",
        "carrier": "A finite ordered array of cells.",
        "support": "A finite one-dimensional array.",
        "topology": (
            "The leftmost and rightmost positions are adjacent, forming a cycle."
        ),
        "boundary": (
            "The left neighbor of the leftmost cell is the rightmost cell, and "
            "the right neighbor of the rightmost cell is the leftmost cell."
        ),
        "read_dependencies_or_neighborhood": (
            "Boundary neighborhoods wrap to the opposite end of the array."
        ),
        "law_kind": "A deterministic wraparound boundary convention.",
        "rule_relation_constraint_function_or_probability_law": (
            "Resolve every off-end neighbor read by cyclic wraparound."
        ),
        "result_kind": "A closed finite cellular support with no missing edge reads.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": "The finite array length.",
        "excluded_observers_and_representations": (
            "Explicit copying into guard positions is an implementation of the "
            "wraparound relation."
        ),
        "evidence_limit": (
            "The C code notes a guard-cell bug; the boundary class itself does "
            "not determine a cellular transition rule."
        ),
    },
    claim=(
        "The source explicitly defines cyclic boundary conditions by wrapping "
        "each end-neighbor read to the opposite endpoint."
    ),
    missing=(
        "The C code notes a guard-cell bug; the boundary class itself does not "
        "determine a cellular transition rule."
    ),
)
add_evidence(
    cyclic_boundary,
    label="cyclic-boundary-rotate",
    unit="U004992",
    claim=(
        "The implementation explanation confirms that RotateLeft/RotateRight "
        "supply cyclic boundary conditions."
    ),
    fields=[
        "topology",
        "boundary",
        "read_dependencies_or_neighborhood",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CORROBORATING",
)


def profile_candidate(
    *,
    key: str,
    name: str,
    anchor: str,
    description: str,
    support: str,
    neighborhood: str,
    alphabet: str,
    aliases: list[str] | None = None,
    modality: str = "CODE",
) -> CandidateSpec:
    missing = (
        "This compact profile does not independently state the complete rule "
        "number decoding, invalid-input behavior, boundary, completion, or "
        "witness semantics."
    )
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts={
            "object_kind": description,
            "native_time": "Discrete cellular-automaton evolution steps.",
            "carrier": "Cells carrying values from the declared alphabet.",
            "support": support,
            "topology": neighborhood,
            "alphabet_or_value_schema": alphabet,
            "complete_state": "The value at every cell in the current configuration.",
            "frontier_or_activation": "The rule is applied across the cellular support.",
            "read_dependencies_or_neighborhood": neighborhood,
            "law_kind": "A parameterized local cellular-automaton rule profile.",
            "rule_relation_constraint_function_or_probability_law": description,
            "result_kind": "A cellular-automaton evolution under the selected profile.",
            "parameters_and_variants": description,
            "excluded_observers_and_representations": (
                "The rnum syntax and output raster are representations of the "
                "profile rather than extra native mechanics."
            ),
            "evidence_limit": missing,
        },
        claim=(
            f"The built-in-function specification formally delimits {name}: "
            f"{description}"
        ),
        missing=missing,
        modality=modality,
        parameters=[
            (
                "profile parameters",
                description,
                [f"{key}-source"],
            )
        ],
    )


profile_candidate(
    key="k-color-range",
    name="k-color range-r cellular automaton profile",
    anchor="U005013",
    description=(
        "A general rule-number profile with k colors and one-dimensional range r."
    ),
    support="A one-dimensional cellular array.",
    neighborhood="A centered interval of 2r+1 cells.",
    alphabet="Integer colors 0 through k-1.",
)
profile_candidate(
    key="rectangular-dd-ca",
    name="d-dimensional rectangular-neighborhood cellular automaton profile",
    anchor="U005013",
    description=(
        "A k-color d-dimensional rule with a rectangular neighborhood of "
        "side lengths 2r_i+1."
    ),
    support="A d-dimensional cellular array.",
    neighborhood="A rectangular radius vector {r1,...,rd}.",
    alphabet="Integer colors 0 through k-1.",
)
profile_candidate(
    key="offset-ca",
    name="specified-offset-neighborhood cellular automaton profile",
    anchor="U005013",
    description=(
        "A k-color rule whose readable neighbors are the explicitly supplied "
        "coordinate offsets."
    ),
    support="A cellular array compatible with the offset coordinate vectors.",
    neighborhood="An arbitrary finite list of specified offsets.",
    alphabet="Integer colors 0 through k-1.",
)
profile_candidate(
    key="totalistic-ca",
    name="totalistic cellular automaton profile",
    anchor="U005013",
    description=(
        "A k-color local rule indexed by the aggregate total of neighborhood values."
    ),
    support="A one- or higher-dimensional cellular array.",
    neighborhood="A declared finite neighborhood whose cell values are totaled.",
    alphabet="Integer colors 0 through k-1.",
    aliases=["k-color totalistic rule"],
)
profile_candidate(
    key="weighted-ca",
    name="weighted-neighborhood cellular automaton profile",
    anchor="U005013",
    description=(
        "A local rule in which neighbor i is assigned a declared weight wt_i."
    ),
    support="A cellular array.",
    neighborhood="A declared finite neighborhood with one weight per position.",
    alphabet="A declared k-value cell alphabet.",
    aliases=["weighted totalistic cellular automaton"],
)
function_profile = profile_candidate(
    key="function-ca",
    name="function-defined step-aware cellular automaton profile",
    anchor="U005013",
    description=(
        "A profile applying a supplied function to each neighborhood list, "
        "optionally with the current step number as a second argument."
    ),
    support="A cellular array of values accepted by the supplied function.",
    neighborhood="The finite neighborhood declared by rspec.",
    alphabet=(
        "Values need not be integers when a general neighborhood function is used."
    ),
    aliases=["function cellular automaton rule"],
)
function_profile["facts"]["complete_state"] = (
    "The current cellular configuration together with the current step number "
    "when the supplied function depends on that number."
)
function_profile["facts"]["control_state"] = (
    "The current step number, beginning at 0, is exposed to the rule function."
)
function_profile["facts"]["schedule"] = (
    "At each discrete generation the function receives each old neighborhood "
    "and the current step number; the successor advances that number."
)
function_profile["facts"]["write_replacement_assembly_or_commit"] = (
    "The function result supplies each next cell value, after which the step "
    "counter advances with the complete successor configuration."
)
add_evidence(
    function_profile,
    label="function-ca-values",
    unit="U005018",
    claim=(
        "The source explicitly permits non-integer initial and evolution values "
        "when a general neighborhood function is used."
    ),
    fields=[
        "alphabet_or_value_schema",
        "parameters_and_variants",
        "evidence_limit",
    ],
)
add_evidence(
    function_profile,
    label="function-ca-step-number",
    unit="U005019",
    claim=(
        "The source states that the general function receives the step number, "
        "starting at zero, as its second argument."
    ),
    fields=[
        "native_time",
        "complete_state",
        "control_state",
        "schedule",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "parameters_and_variants",
        "evidence_limit",
    ],
)

profile_candidate(
    key="nine-neighbor-totalistic",
    name="two-dimensional nine-neighbor totalistic CA profile",
    anchor="U005016",
    description=(
        "A 2D totalistic rule over the full 3 by 3 neighborhood."
    ),
    support="A two-dimensional square cellular grid.",
    neighborhood="The target cell and all eight cells in its 3 by 3 block.",
    alphabet="Integer colors 0 through k-1.",
)
profile_candidate(
    key="five-neighbor-totalistic",
    name="two-dimensional five-neighbor totalistic CA profile",
    anchor="U005016",
    description=(
        "A 2D totalistic rule over the center and four orthogonal neighbors."
    ),
    support="A two-dimensional square cellular grid.",
    neighborhood="A five-site orthogonal cross including the target cell.",
    alphabet="Integer colors 0 through k-1.",
)
profile_candidate(
    key="outer-totalistic",
    name="two-dimensional five-neighbor outer-totalistic CA profile",
    anchor="U005016",
    description=(
        "A five-neighbor rule that weights the center separately from the four "
        "orthogonal neighbors."
    ),
    support="A two-dimensional square cellular grid.",
    neighborhood="A weighted five-site orthogonal cross.",
    alphabet="Integer colors 0 through k-1.",
    aliases=["outer totalistic rule"],
)
profile_candidate(
    key="growth-profile",
    name="two-dimensional five-neighbor growth CA profile",
    anchor="U005016",
    description=(
        "A five-neighbor weighted rule profile whose encoding isolates a "
        "growth-style update."
    ),
    support="A two-dimensional square cellular grid.",
    neighborhood="A weighted five-site orthogonal cross.",
    alphabet="Integer colors 0 through k-1.",
    aliases=["five-neighbor growth rule"],
)


def seed_or_query_candidate(
    *,
    key: str,
    name: str,
    anchor: str,
    description: str,
    result: str,
    aliases: list[str] | None = None,
    seed_boundary: bool = True,
) -> CandidateSpec:
    missing = (
        "The compact specification does not state invalid-input behavior, "
        "native failure, or an independent witness convention."
    )
    facts = {
        "object_kind": description,
        "input": description,
        "law_kind": "A constructor or projection profile for CA evolution.",
        "rule_relation_constraint_function_or_probability_law": description,
        "result_kind": result,
        "determinism_branching_or_measure": (
            "Deterministic for a fixed specification."
        ),
        "parameters_and_variants": description,
        "excluded_observers_and_representations": (
            "The Mathematica list syntax is a representation of the "
            "constructor or projection."
        ),
        "evidence_limit": missing,
    }
    if seed_boundary:
        facts["seed"] = description
        facts["boundary"] = description
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts=facts,
        claim=f"The specification formally delimits {name}: {description}",
        missing=missing,
        modality="CODE",
        parameters=[
            ("profile", description, [f"{key}-source"]),
        ],
    )


seed_or_query_candidate(
    key="cyclic-explicit-seed",
    name="explicit finite cyclic cellular-automaton state class",
    anchor="U005021",
    description=(
        "An explicit finite list of values used as a cyclic cellular-automaton "
        "configuration."
    ),
    result="A finite cyclic initial configuration.",
)
seed_or_query_candidate(
    key="background-seed",
    name="finite foreground on uniform or periodic CA background",
    anchor="U005021",
    description=(
        "A finite list of foreground values superimposed on either one "
        "background value or a repeating background block."
    ),
    result="An initial configuration with a finite foreground and infinite background.",
)
seed_or_query_candidate(
    key="offset-block-seed",
    name="offset multi-block cellular-automaton initial condition",
    anchor="U005021",
    description=(
        "Several finite value blocks placed at explicit coordinate offsets on "
        "a declared background."
    ),
    result="A composed initial cellular configuration.",
)
seed_or_query_candidate(
    key="dd-padded-seed",
    name="d-dimensional padded cellular-automaton initial condition",
    anchor="U005021",
    description=(
        "A d-dimensional finite array specification embedded using a "
        "d-dimensional padding/background specification."
    ),
    result="A d-dimensional initial cellular configuration.",
)

explicit_cyclic_seed = source_candidate(
    key="explicit-cyclic-seed",
    name="{1,0,0,1,0} cyclic cellular-automaton seed preset",
    anchor="U005043",
    aliases=["five-cell cyclic rule 30 seed"],
    facts={
        "object_kind": "A concrete finite cyclic initial-condition preset.",
        "carrier": "Five ordered cells.",
        "support": "A five-site cyclic array.",
        "topology": "The endpoints are adjacent under cyclic continuation.",
        "alphabet_or_value_schema": "Binary values 0 and 1.",
        "complete_state": "The explicit list {1,0,0,1,0}.",
        "seed": "The explicit five-cell binary list {1,0,0,1,0}.",
        "boundary": "The explicit list continues cyclically.",
        "law_kind": "Use the list as the initial state for rule 30.",
        "result_kind": "A finite cyclic Rule 30 evolution.",
        "parameters_and_variants": "Five cells, rule 30, and a three-step example run.",
        "excluded_observers_and_representations": (
            "The printed four-row output is a finite witness of the preset."
        ),
        "evidence_limit": (
            "The example does not define behavior for malformed lists or a "
            "native stopping condition beyond the requested run length."
        ),
    },
    claim=(
        "The source states that an explicitly supplied finite initial list is "
        "continued cyclically and introduces the five-cell rule 30 example."
    ),
    missing=(
        "The example does not define behavior for malformed lists or a native "
        "stopping condition beyond the requested run length."
    ),
)
add_evidence(
    explicit_cyclic_seed,
    label="explicit-cyclic-seed-run",
    unit="U005044",
    claim=(
        "The exact function call and output fix the five-cell list, rule 30, "
        "three steps, and cyclic finite result."
    ),
    fields=list(explicit_cyclic_seed["facts"]),
    modality="CODE",
)

periodic_patch_seed = source_candidate(
    key="periodic-patch-seed",
    name="{1,1} patch on repeating {1,0,1,1} CA background",
    anchor="U005045",
    aliases=["periodic-background rule 30 seed"],
    facts={
        "object_kind": "A concrete finite-foreground/repeating-background seed preset.",
        "carrier": "A one-dimensional cellular row.",
        "support": "An unbounded repetition background with a finite foreground patch.",
        "topology": "Linear positions on a repeating background.",
        "alphabet_or_value_schema": "Binary values 0 and 1.",
        "complete_state": (
            "Foreground {1,1} superimposed on repetitions of {1,0,1,1}."
        ),
        "seed": "Patch {1,1} on a repeating {1,0,1,1} background.",
        "boundary": "The four-value background repeats beyond the foreground.",
        "law_kind": "Use the composed state as the initial condition for rule 30.",
        "result_kind": (
            "A rule 30 evolution, by default projected to the region affected "
            "by the foreground patch."
        ),
        "parameters_and_variants": (
            "Foreground block, repeating background block, rule, run length, "
            "and output window."
        ),
        "excluded_observers_and_representations": (
            "The affected-region crop is an output projection, not a boundary "
            "or transition change."
        ),
        "evidence_limit": (
            "The example does not state invalid-input, native completion, "
            "failure, or witness semantics."
        ),
    },
    claim=(
        "The source explicitly specifies the {1,1} foreground, repeating "
        "{1,0,1,1} background, and default affected-region projection."
    ),
    missing=(
        "The example does not state invalid-input, native completion, failure, "
        "or witness semantics."
    ),
)
add_evidence(
    periodic_patch_seed,
    label="periodic-patch-seed-call",
    unit="U005046",
    claim=(
        "The function call fixes rule 30, the foreground/background pair, and "
        "the 50-step run."
    ),
    fields=list(periodic_patch_seed["facts"]),
    modality="CODE",
)
add_evidence(
    periodic_patch_seed,
    label="periodic-patch-all-window",
    unit="U005048",
    claim=(
        "The adjacent example distinguishes the native seed from an observer "
        "request for all possibly affected cells."
    ),
    fields=[
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
)

positioned_patch_seed = source_candidate(
    key="positioned-patch-preset",
    name="two positioned Rule 30 foreground blocks preset",
    anchor="U005051",
    aliases=["offset -10 and 20 initial blocks"],
    facts={
        "object_kind": "A concrete multi-patch cellular initial-condition preset.",
        "carrier": "A one-dimensional binary cellular row.",
        "support": "An unbounded zero background with positioned finite blocks.",
        "topology": "Integer-indexed linear cell positions.",
        "alphabet_or_value_schema": "Binary values 0 and 1.",
        "complete_state": (
            "One {1} block at offset -10 and one {1,1} block at offset 20 on "
            "a zero background."
        ),
        "seed": "The two explicitly positioned foreground blocks on background 0.",
        "boundary": "The value-0 background extends outside the finite blocks.",
        "law_kind": "Use the composed state as the initial condition for rule 30.",
        "result_kind": "A unique 50-step Rule 30 evolution.",
        "parameters_and_variants": (
            "Foreground values, offsets -10 and 20, zero background, rule 30, "
            "and 50 steps."
        ),
        "excluded_observers_and_representations": "The raster is an output representation.",
        "evidence_limit": (
            "The example does not state collision/overlap precedence for "
            "arbitrary positioned blocks or invalid-input behavior."
        ),
    },
    claim=(
        "The source explicitly introduces blocks placed at offsets -10 and 20."
    ),
    missing=(
        "The example does not state collision/overlap precedence for arbitrary "
        "positioned blocks or invalid-input behavior."
    ),
)
add_evidence(
    positioned_patch_seed,
    label="positioned-patch-call",
    unit="U005052",
    claim=(
        "The code fixes the two block values and offsets, zero background, "
        "rule 30, and 50-step request."
    ),
    fields=list(positioned_patch_seed["facts"]),
    modality="CODE",
)

# Explicit generalized-rule presets.

def explicit_ca_example(
    *,
    key: str,
    name: str,
    anchor: str,
    description: str,
    alphabet: str,
    support: str,
    neighborhood: str,
    seed: str,
    result: str,
    aliases: list[str] | None = None,
) -> CandidateSpec:
    missing = (
        "The example does not state an infinite-support boundary, invalid-rule "
        "behavior, native completion/failure, or witness semantics."
    )
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts={
            "object_kind": description,
            "native_time": "Discrete cellular-automaton steps.",
            "carrier": "Cells carrying values from the declared alphabet.",
            "support": support,
            "topology": neighborhood,
            "alphabet_or_value_schema": alphabet,
            "complete_state": "The current value at every cell in the retained support.",
            "visible_history": "The example renders successive configurations as rows or rasters.",
            "seed": seed,
            "frontier_or_activation": "Every cell in the cellular support is updated.",
            "schedule": "Generation-synchronous cellular-automaton evolution.",
            "read_dependencies_or_neighborhood": neighborhood,
            "law_kind": "A deterministic local cellular-automaton rule.",
            "rule_relation_constraint_function_or_probability_law": description,
            "write_replacement_assembly_or_commit": (
                "One next value is produced for each cell from its old neighborhood."
            ),
            "result_kind": result,
            "successor_cardinality": "Exactly one successor for a fixed state and rule.",
            "determinism_branching_or_measure": (
                "Deterministic, with no branching or probability stated."
            ),
            "parameters_and_variants": description,
            "excluded_observers_and_representations": (
                "The function call, finite output window, and raster are "
                "implementation or representation choices."
            ),
            "evidence_limit": missing,
        },
        claim=f"The example explicitly specifies {name}: {description}",
        missing=missing,
        parameters=[
            ("rule specification", description, [f"{key}-source"]),
        ],
    )


rule921408 = explicit_ca_example(
    key="rule921408",
    name="k=3, r=1 cellular automaton rule 921408 preset",
    anchor="U005061",
    description="The general three-color range-one rule numbered 921408.",
    alphabet="Three integer colors 0, 1, and 2.",
    support="A one-dimensional cellular array.",
    neighborhood="The target cell and one neighbor on each side.",
    seed="One cell of value 1 on a value-0 background.",
    result="A unique 100-step raster evolution.",
    aliases=["rule 921408"],
)
add_evidence(
    rule921408,
    label="rule921408-call",
    unit="U005062",
    claim=(
        "The function call fixes the rule tuple {921408,3,1}, the one-cell "
        "foreground, zero background, and 100-step request."
    ),
    fields=list(rule921408["facts"]),
    modality="CODE",
)

code867 = explicit_ca_example(
    key="code867",
    name="k=3, r=1 totalistic code 867 preset",
    anchor="U005064",
    description="The three-color range-one totalistic rule with code 867.",
    alphabet="Three integer colors 0, 1, and 2.",
    support="A one-dimensional cellular array.",
    neighborhood="A range-one three-cell neighborhood reduced to its total.",
    seed="One cell of value 1 on a value-0 background.",
    result="A unique 50-step raster evolution.",
    aliases=["totalistic code 867"],
)
add_evidence(
    code867,
    label="code867-call",
    unit="U005065",
    claim=(
        "The function call fixes totalistic code 867, k=3, range 1, a "
        "single-value seed, zero background, and 50 steps."
    ),
    fields=list(code867["facts"]),
    modality="CODE",
)

mod4 = explicit_ca_example(
    key="mod4-function-ca",
    name="modulo-four neighborhood-sum cellular automaton preset",
    anchor="U005067",
    description=(
        "A range-one function rule returning the sum of neighborhood values modulo 4."
    ),
    alphabet="Values generated modulo 4.",
    support="A one-dimensional cellular array.",
    neighborhood="The range-one three-cell neighborhood.",
    seed="One cell of value 1 on a value-0 background.",
    result="A unique 50-step raster evolution.",
    aliases=["Mod[Apply[Plus,#],4] cellular automaton"],
)
add_evidence(
    mod4,
    label="mod4-function-call",
    unit="U005068",
    claim=(
        "The code supplies the exact neighborhood function, range, seed, "
        "background, and requested step count."
    ),
    fields=list(mod4["facts"]),
    modality="CODE",
)

code3702 = explicit_ca_example(
    key="code3702",
    name="two-dimensional nine-neighbor totalistic code 3702 preset",
    anchor="U005070",
    description=(
        "A binary 2D totalistic rule with code 3702 over the full 3 by 3 neighborhood."
    ),
    alphabet="Two integer colors 0 and 1.",
    support="A two-dimensional square cellular grid.",
    neighborhood="The target and all eight neighbors in its 3 by 3 block.",
    seed="One value-1 cell on a value-0 background.",
    result="A unique 25-step evolution, with the last five states selected.",
    aliases=["2D totalistic code 3702"],
)
add_evidence(
    code3702,
    label="code3702-call",
    unit="U005071",
    claim=(
        "The code fixes code 3702, the binary nine-neighbor 2D profile, a "
        "single-cell seed, zero background, 25 steps, and a last-five projection."
    ),
    fields=list(code3702["facts"]),
    modality="CODE",
)


# Exact formulas, static relations, restrictions, and observer/query objects.

rule170 = source_candidate(
    key="rule170",
    name="Rule 170 left-shift cellular automaton preset",
    anchor="U005112",
    aliases=["classic shift map", "Mod[2 x,1] map"],
    facts={
        "object_kind": "A named cellular-automaton shift preset.",
        "native_time": "Discrete cellular-automaton steps.",
        "carrier": "A one-dimensional sequence of cell values.",
        "support": "An infinite or cyclic one-dimensional sequence.",
        "topology": "Each new site reads the adjacent site to its right.",
        "alphabet_or_value_schema": "The displayed interpretation uses binary digits.",
        "complete_state": "The complete current sequence of cell values.",
        "frontier_or_activation": "Every cell position is shifted.",
        "schedule": "All values shift one position together.",
        "read_dependencies_or_neighborhood": "One adjacent source cell.",
        "law_kind": "A deterministic shift map.",
        "rule_relation_constraint_function_or_probability_law": (
            "Shift every cell value one position to the left without changing it; "
            "under the plotted encoding the map is Mod[2 x,1]."
        ),
        "write_replacement_assembly_or_commit": (
            "Each destination receives the unchanged value from its adjacent source."
        ),
        "result_kind": "A uniquely shifted successor configuration.",
        "successor_cardinality": "Exactly one successor configuration.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": (
            "Rule number 170 and the cyclic/rational-number representation."
        ),
        "excluded_observers_and_representations": (
            "The Cantor-set graph and real-number map are mathematical "
            "representations of the cell shift."
        ),
        "evidence_limit": (
            "The passage does not independently settle infinite-support "
            "boundary, completion, failure, or witness semantics."
        ),
    },
    claim=(
        "The source names rule 170 and states its exact native shift action, "
        "along with a separate Mod[2x,1] representation."
    ),
    missing=(
        "The passage does not independently settle infinite-support boundary, "
        "completion, failure, or witness semantics."
    ),
)


def declarative_pattern(
    *,
    key: str,
    name: str,
    anchor: str,
    definition: str,
    support: str,
    values: str,
    result: str,
    aliases: list[str] | None = None,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    missing = (
        "The source does not fully specify domain clipping, coordinate bounds, "
        "invalid arguments, or a separate witness convention."
    )
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts={
            "object_kind": "A declarative integer-indexed pattern or query.",
            "carrier": "Integer coordinate tuples.",
            "support": support,
            "alphabet_or_value_schema": values,
            "complete_state": "The value assigned to every coordinate in the requested domain.",
            "input": "Integer coordinates and any declared modulus or parameter.",
            "law_kind": "A direct function or relation, not an iterated transition.",
            "rule_relation_constraint_function_or_probability_law": definition,
            "result_kind": result,
            "successor_cardinality": (
                "One determined value or membership judgment per valid input."
            ),
            "determinism_branching_or_measure": "Deterministic.",
            "termination_completion_failure": (
                "A finite requested window completes after all requested "
                "coordinate judgments are evaluated."
            ),
            "parameters_and_variants": definition,
            "excluded_observers_and_representations": (
                "Color plots and cellular-automaton comparisons are "
                "representations or relations to the declarative object."
            ),
            "evidence_limit": missing,
        },
        claim=f"The source gives a determinate definition for {name}: {definition}",
        missing=missing,
        modality="FORMULA",
        route_keys=route_keys,
    )


pascal_mod2 = declarative_pattern(
    key="pascal-mod2",
    name="Pascal-triangle modulo-two pattern",
    anchor="U005113",
    definition=(
        "The Rule 90 single-seed pattern equals Pascal's triangle reduced "
        "modulo 2, with black cells corresponding to odd coefficients."
    ),
    support="Integer row and position coordinates.",
    values="Binary parity values.",
    result="A static nested binary array.",
    aliases=["odd binomial-coefficient pattern"],
    route_keys=["pascal-page611"],
)
add_evidence(
    pascal_mod2,
    label="pascal-mod2-formula",
    unit="U005116",
    claim=(
        "The source gives the exact coefficient expression "
        "Mod[Binomial[t,(n+t)/2],2] on parity-compatible coordinates."
    ),
    fields=list(pascal_mod2["facts"]),
    modality="FORMULA",
)

rule60 = declarative_pattern(
    key="rule60",
    name="Rule 60 binomial-modulo-two pattern preset",
    anchor="U005117",
    definition=(
        "The static array value at row t and position n is "
        "Mod[Binomial[t,n],2], identified as the single-seed pattern of rule 60."
    ),
    support="Nonnegative integer row and position coordinates.",
    values="Binary parity values.",
    result="A uniquely determined distorted nested binary pattern.",
    aliases=["cellular automaton rule 60"],
    route_keys=["rule60-page58"],
)

rule90_background = source_candidate(
    key="rule90-background-seed",
    name="Rule 90 single-cell-on-striped-background seed class",
    anchor="U005120",
    aliases=["another initial condition for rule 90"],
    facts={
        "object_kind": "A coverage-bearing initial-condition class for rule 90.",
        "carrier": "A one-dimensional Rule 90 cell row.",
        "support": "One finite foreground cell embedded in a repeating background.",
        "alphabet_or_value_schema": "Black/white cell values.",
        "complete_state": (
            "One black cell together with the repeated striped background block."
        ),
        "seed": (
            "A single black cell inserted into a background of repetitions of "
            "the pictured striped black-to-white block."
        ),
        "boundary": "The background repeats outside the finite foreground.",
        "law_kind": "Rule 90 evolution from the declared patterned seed.",
        "result_kind": (
            "A Rule 90 evolution with white and striped nested regions."
        ),
        "parameters_and_variants": "The repeated background block is the varying seed profile.",
        "excluded_observers_and_representations": (
            "The displayed fractal dimensions and raster are outcome/representation."
        ),
        "evidence_limit": (
            "The inline artwork establishes the source's seed symbols, but the "
            "text does not give a numeric transcription or finite boundary."
        ),
    },
    claim=(
        "The note explicitly isolates another Rule 90 initial condition: one "
        "black cell in a repeated striped-block background."
    ),
    missing=(
        "The inline artwork establishes the source's seed symbols, but the text "
        "does not give a numeric transcription or finite boundary."
    ),
    variants=[
        (
            "patterned repeating background",
            "The source distinguishes the single foreground cell from the "
            "repeated striped block.",
            ["rule90-background-seed-source"],
        )
    ],
)
add_candidate_image(
    rule90_background,
    label="rule90-background-black-cell",
    unit="U005120",
    path="BACK-MATTER/NOTES/_page_885_inline_black_cell.jpeg",
    claim=(
        "Original-resolution inspection confirms the inline single black-cell "
        "symbol used by the seed description."
    ),
    fields=[
        "alphabet_or_value_schema",
        "complete_state",
        "seed",
        "parameters_and_variants",
        "evidence_limit",
    ],
)
add_candidate_image(
    rule90_background,
    label="rule90-background-block",
    unit="U005120",
    path=(
        "BACK-MATTER/NOTES/_page_885_inline_black_gradient_white_block.jpeg"
    ),
    claim=(
        "Original-resolution inspection confirms the inline striped "
        "black-to-white background-block symbol; no numeric row is inferred."
    ),
    fields=[
        "support",
        "complete_state",
        "seed",
        "boundary",
        "parameters_and_variants",
        "evidence_limit",
    ],
)

k_rule90 = source_candidate(
    key="k-color-rule90",
    name="k-color additive Rule 90 generalization",
    anchor="U005123",
    aliases=["more-colors Rule 90"],
    facts={
        "object_kind": "A k-color additive cellular-automaton family.",
        "native_time": "Discrete synchronous generations.",
        "carrier": "A one-dimensional row of cells.",
        "support": "A one-dimensional cyclic list in the supplied implementation.",
        "topology": "Immediate left and right neighbors; self has coefficient zero.",
        "alphabet_or_value_schema": "Residues modulo k.",
        "complete_state": "One row of modulo-k cell values.",
        "frontier_or_activation": "Every cell receives a next value.",
        "schedule": "All positions are updated together from the old row.",
        "read_dependencies_or_neighborhood": "Immediate left and right neighbors.",
        "law_kind": "A deterministic additive modulo-k local rule.",
        "rule_relation_constraint_function_or_probability_law": (
            "a_i' = Mod[a_(i-1)+a_(i+1), k]."
        ),
        "write_replacement_assembly_or_commit": (
            "The modulo-k sum replaces each target cell."
        ),
        "result_kind": "A unique k-color cellular evolution.",
        "successor_cardinality": "Exactly one successor row.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": "The number of colors k.",
        "excluded_observers_and_representations": (
            "ListCorrelate syntax, counts of non-white cells, and raster patterns "
            "are implementation, analysis, or representation."
        ),
        "evidence_limit": (
            "The note does not separately state infinite boundary, completion, "
            "failure, or witness semantics."
        ),
    },
    claim=(
        "The note introduces generalizations of rule 90 to k colors and the "
        "following code gives the exact modulo-k neighbor-sum update."
    ),
    missing=(
        "The note does not separately state infinite boundary, completion, "
        "failure, or witness semantics."
    ),
)
add_evidence(
    k_rule90,
    label="k-color-rule90-code",
    unit="U005124",
    claim=(
        "The code exactly defines the successor as the modulo-k sum of rotated "
        "left and right neighbor lists."
    ),
    fields=list(k_rule90["facts"]),
    modality="CODE",
)

additive = source_candidate(
    key="additive-ca",
    name="additive cellular automaton restriction",
    anchor="U005127",
    aliases=["additive rules"],
    facts={
        "object_kind": (
            "A named restriction of cellular-automaton rules to additive local laws."
        ),
        "carrier": "Cell values acted on by an additive local rule.",
        "alphabet_or_value_schema": "Finite modular value systems in the examples.",
        "law_kind": "Local updates formed by addition in the value algebra.",
        "rule_relation_constraint_function_or_probability_law": (
            "The adjacent k-color Rule 90 family adds left and right values modulo k."
        ),
        "result_kind": "A cellular evolution satisfying the additive restriction.",
        "parameters_and_variants": (
            "The modulus/color count and additive coefficients can vary."
        ),
        "excluded_observers_and_representations": (
            "Nesting, fractal dimension, and binomial-coefficient formulas are "
            "properties or representations of additive evolutions."
        ),
        "evidence_limit": (
            "The complete additive-rule parameterization is deferred to page 952."
        ),
    },
    claim=(
        "The source explicitly identifies the preceding k-color rules as "
        "examples of the named additive-rule class and routes fuller treatment."
    ),
    missing=(
        "The complete additive-rule parameterization is deferred to page 952."
    ),
    route_keys=["additive-page952"],
)

def pictured_integer_pattern(
    *,
    key: str,
    name: str,
    unit: str,
    path: str,
    definition: str,
    support: str,
) -> CandidateSpec:
    missing = (
        "The image and caption identify the function and modulo-two display, "
        "but do not state the function's full arithmetic definition, domain "
        "clipping, invalid arguments, or witness semantics."
    )
    facts = {
        "object_kind": "A declarative integer-function modulo-two pattern.",
        "carrier": "Integer coordinate tuples.",
        "support": support,
        "alphabet_or_value_schema": "Binary residues modulo 2.",
        "input": "The integer arguments of the named function.",
        "law_kind": "Direct integer-function evaluation followed by reduction modulo 2.",
        "rule_relation_constraint_function_or_probability_law": definition,
        "result_kind": "A static binary lattice pattern.",
        "successor_cardinality": "One residue for each valid coordinate tuple.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": "The named integer function and its arity.",
        "excluded_observers_and_representations": (
            "Black/white pixels and page layout represent the modular values."
        ),
        "evidence_limit": missing,
    }
    spec = add_candidate(
        ALL_CANDIDATE_SPECS,
        key=key,
        name=name,
        anchor=path,
        aliases=[],
        facts=facts,
        missing=missing,
    )
    add_evidence(
        spec,
        label=f"{key}-context",
        unit="U005134",
        claim=(
            "The caption states that the preceding pictures are made by "
            "reducing their named integer functions modulo 2."
        ),
        fields=[
            "object_kind",
            "carrier",
            "support",
            "alphabet_or_value_schema",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        modality="CAPTION",
    )
    add_candidate_image(
        spec,
        label=f"{key}-image",
        unit=unit,
        path=path,
        claim=(
            f"Original-resolution inspection confirms the source label and "
            f"binary lattice rendering for {name}; pixels are not used to "
            "invent the arithmetic definition."
        ),
        fields=list(facts),
    )
    return spec


pictured_integer_pattern(
    key="binomial-mod2-array",
    name="Binomial modulo-two array",
    unit="U005130",
    path="BACK-MATTER/NOTES/_page_885_Picture_23.jpeg",
    definition="Reduce Binomial's integer values modulo 2 over its argument lattice.",
    support="A two-dimensional integer-coordinate array.",
)
pictured_integer_pattern(
    key="multinomial-mod2-array",
    name="Multinomial modulo-two array family",
    unit="U005131",
    path="BACK-MATTER/NOTES/_page_885_Picture_24.jpeg",
    definition=(
        "Reduce a d-argument Multinomial value modulo 2 at each integer tuple."
    ),
    support="A d-dimensional integer-coordinate array.",
)
pictured_integer_pattern(
    key="stirling1-mod2-array",
    name="StirlingS1 modulo-two array",
    unit="U005132",
    path="BACK-MATTER/NOTES/_page_885_Picture_25.jpeg",
    definition="Reduce StirlingS1's integer values modulo 2 over its argument lattice.",
    support="A two-dimensional integer-coordinate array.",
)
pictured_integer_pattern(
    key="stirling2-mod2-array",
    name="StirlingS2 modulo-two array",
    unit="U005133",
    path="BACK-MATTER/NOTES/_page_885_Picture_26.jpeg",
    definition="Reduce StirlingS2's integer values modulo 2 over its argument lattice.",
    support="A two-dimensional integer-coordinate array.",
)

gcd_pattern = declarative_pattern(
    key="gcd-pattern",
    name="GCD modulo-two lattice pattern",
    anchor="U005134",
    definition="Evaluate GCD[m,n] over integer pairs and reduce the values modulo 2.",
    support="A two-dimensional integer-coordinate lattice.",
    values="Binary residues modulo 2.",
    result="A static binary pattern.",
    route_keys=["gcd-page613"],
)
jacobi_pattern = declarative_pattern(
    key="jacobi-pattern",
    name="JacobiSymbol modulo-two lattice pattern",
    anchor="U005134",
    definition=(
        "Evaluate JacobiSymbol[m,2n-1] over integer pairs and reduce/display "
        "the resulting values."
    ),
    support="A two-dimensional integer-coordinate lattice.",
    values="Values derived from the JacobiSymbol integer function.",
    result="A static lattice pattern.",
    route_keys=["jacobi-page1081"],
)


def bitwise_function_candidate(
    key: str,
    display_name: str,
    relation: str,
) -> CandidateSpec:
    missing = (
        "The source names and relates the bitwise function but does not give a "
        "complete bit-by-bit definition, signed-integer convention, domain "
        "boundary, or witness semantics."
    )
    spec = source_candidate(
        key=key,
        name=f"{display_name} integer function",
        anchor="U005135",
        aliases=[display_name],
        facts={
            "object_kind": "A deterministic binary integer function.",
            "carrier": "Pairs of integers represented by digit sequences.",
            "input": "Two integer arguments x and y.",
            "law_kind": "A direct bitwise function.",
            "rule_relation_constraint_function_or_probability_law": relation,
            "result_kind": "One integer result.",
            "successor_cardinality": "Exactly one result per valid input pair.",
            "determinism_branching_or_measure": "Deterministic.",
            "parameters_and_variants": "Choice of bitwise operation.",
            "excluded_observers_and_representations": (
                "Nested black/white plots are representations of function values."
            ),
            "evidence_limit": missing,
        },
        claim=(
            f"The source names {display_name} as a bitwise integer function and "
            f"states the exact cross-function relation {relation}."
        ),
        missing=missing,
        modality="FORMULA",
    )
    add_candidate_image(
        spec,
        label=f"{key}-plot",
        unit="U005136",
        path="BACK-MATTER/NOTES/_page_886_Picture_4.jpeg",
        claim=(
            f"Original-resolution inspection confirms the labelled nested "
            f"function plot including {display_name}; it is a representation."
        ),
        fields=[
            "object_kind",
            "carrier",
            "input",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    return spec


bitwise_function_candidate(
    "bitand-function",
    "BitAnd",
    "BitOr[x,y] + BitAnd[x,y] == x+y.",
)
bitwise_function_candidate(
    "bitor-function",
    "BitOr",
    "BitOr[x,y] - BitAnd[x,y] == BitXor[x,y].",
)
bitwise_function_candidate(
    "bitxor-function",
    "BitXor",
    "BitOr[x,y] - BitAnd[x,y] == BitXor[x,y].",
)

munching = declarative_pattern(
    key="munching-squares",
    name="munching-squares BitXor relation",
    anchor="U005137",
    definition=(
        "For each successive integer t, select the integer-coordinate points "
        "(x,y) satisfying BitXor[x,y] == t."
    ),
    support="A two-dimensional integer-coordinate grid indexed by t.",
    values="Boolean membership in the equality relation.",
    result="A sequence of relation-defined grid patterns.",
    aliases=["munching squares", "munching foos"],
    route_keys=[],
)
add_candidate_image(
    munching,
    label="munching-squares-image",
    unit="U005138",
    path="BACK-MATTER/NOTES/_page_886_Picture_6.jpeg",
    claim=(
        "Original-resolution inspection confirms the successive labelled "
        "BitXor equality patterns; the source formula supplies the relation."
    ),
    fields=[
        "support",
        "alphabet_or_value_schema",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)


def unary_bitwise_curve(key: str, operation: str) -> CandidateSpec:
    spec = declarative_pattern(
        key=key,
        name=f"{operation}[n,2n] successive-index curve",
        anchor="U005139",
        definition=(
            f"For successive n, evaluate {operation}[n,2n] and use the values "
            "to form the displayed curve."
        ),
        support="Successive integer indices mapped into a plotted curve.",
        values=f"Integer values of {operation}.",
        result="A deterministic nested curve.",
        aliases=[f"{operation} n and 2n curve"],
    )
    add_candidate_image(
        spec,
        label=f"{key}-image",
        unit="U005140",
        path="BACK-MATTER/NOTES/_page_886_Picture_8.jpeg",
        claim=(
            f"Original-resolution inspection confirms the labelled "
            f"{operation}[n,2n] curve among the successive-index plots."
        ),
        fields=[
            "object_kind",
            "support",
            "alphabet_or_value_schema",
            "input",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    return spec


unary_bitwise_curve("bitand-curve", "BitAnd")
unary_bitwise_curve("bitor-curve", "BitOr")
unary_bitwise_curve("bitxor-curve", "BitXor")

center_column = source_candidate(
    key="rule30-center-column",
    name="Rule 30 center-column sequence query",
    anchor="U005145",
    aliases=["Rule 30 center column", "Rule 30 random sequence"],
    facts={
        "object_kind": "An observer/query over a Rule 30 evolution.",
        "native_time": "One output symbol is taken from each successive generation.",
        "carrier": "The center spatial column of the evolution history.",
        "alphabet_or_value_schema": "Binary black/white values.",
        "input": "A requested prefix length n.",
        "law_kind": "Project the Rule 30 history to its center cell at each step.",
        "rule_relation_constraint_function_or_probability_law": (
            "Return the first n center-column values of the single-seed Rule 30 run."
        ),
        "result_kind": "A finite binary sequence prefix.",
        "determinism_branching_or_measure": (
            "Deterministic; randomness is an observed statistical property."
        ),
        "termination_completion_failure": (
            "The query completes after n output symbols."
        ),
        "parameters_and_variants": "The requested prefix length n.",
        "excluded_observers_and_representations": (
            "Excess counts, run lengths, plots, and randomness-test results are "
            "analyses of the sequence."
        ),
        "evidence_limit": (
            "The passage does not define a cryptographic keying/encryption "
            "interface or prove statistical randomness."
        ),
    },
    claim=(
        "The source isolates the center-column binary sequence and reports "
        "finite-prefix statistics; the following code computes its first n values."
    ),
    missing=(
        "The passage does not define a cryptographic keying/encryption interface "
        "or prove statistical randomness."
    ),
)
add_evidence(
    center_column,
    label="rule30-center-column-code",
    unit="U005146",
    claim=(
        "The code gives a finite deterministic procedure returning the first n "
        "center-column values."
    ),
    fields=list(center_column["facts"]),
    modality="CODE",
)


# ---------------------------------------------------------------------------
# Explicit ornamental and assembly procedures.

def procedure_candidate(
    *,
    key: str,
    name: str,
    anchor: str,
    description: str,
    carrier: str,
    support: str,
    state: str,
    result: str,
    missing: str,
    aliases: list[str] | None = None,
) -> CandidateSpec:
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts={
            "object_kind": "A finite geometric or physical construction procedure.",
            "native_time": "Discrete construction stages or assembly operations.",
            "carrier": carrier,
            "support": support,
            "complete_state": state,
            "frontier_or_activation": (
                "The next designated geometric or assembly component is added "
                "or transformed."
            ),
            "schedule": "The stated construction operations are performed in order.",
            "read_dependencies_or_neighborhood": (
                "Each operation uses the previously constructed geometry or assembly."
            ),
            "law_kind": "A deterministic drawing, deformation, or assembly procedure.",
            "rule_relation_constraint_function_or_probability_law": description,
            "write_replacement_assembly_or_commit": description,
            "result_kind": result,
            "successor_cardinality": (
                "One next construction stage when every stated choice is fixed."
            ),
            "determinism_branching_or_measure": (
                "Deterministic to the level specified by the source."
            ),
            "termination_completion_failure": (
                "The depicted or stated finite operation sequence ends in the ornament."
            ),
            "parameters_and_variants": description,
            "excluded_observers_and_representations": (
                "Historical provenance, material, page layout, and visual "
                "similarity to cellular automata are contextual."
            ),
            "evidence_limit": missing,
        },
        claim=f"The source delimits {name} and states or diagrams its procedure: {description}",
        missing=missing,
        parameters=[
            ("construction profile", description, [f"{key}-source"]),
        ],
    )


def attach_procedure_images(
    candidate: CandidateSpec,
    *,
    label_prefix: str,
    entries: list[tuple[str, str]],
) -> None:
    for index, (unit, path) in enumerate(entries, 1):
        add_candidate_image(
            candidate,
            label=f"{label_prefix}-{index}",
            unit=unit,
            path=path,
            claim=(
                "Original-resolution inspection confirms this source-ordered "
                "construction stage; the image is used only for visibly "
                "unambiguous geometry."
            ),
            fields=[
                "carrier",
                "support",
                "complete_state",
                "frontier_or_activation",
                "schedule",
                "read_dependencies_or_neighborhood",
                "write_replacement_assembly_or_commit",
                "result_kind",
                "termination_completion_failure",
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            ],
            strength="DIRECT_PARTIAL_MECHANICS",
        )


pylos = procedure_candidate(
    key="pylos-labyrinth",
    name="Pylos labyrinth drawing procedure",
    anchor="U005172",
    aliases=["classical seven-circuit labyrinth", "Troy maze"],
    description=(
        "Apply the finite source-ordered drawing procedure shown in five stages "
        "to produce the square or rounded labyrinth design."
    ),
    carrier="Planar line segments, bends, and guide marks.",
    support="A bounded planar drawing region.",
    state="The partial line drawing after each depicted stage.",
    result="A completed classical labyrinth drawing.",
    missing=(
        "The prose does not verbalize every stroke, orientation, scaling rule, "
        "or behavior for malformed intermediate drawings."
    ),
)
attach_procedure_images(
    pylos,
    label_prefix="pylos-stage",
    entries=[
        ("U005173", "BACK-MATTER/NOTES/_page_888_Picture_5.jpeg"),
        ("U005174", "BACK-MATTER/NOTES/_page_888_Picture_6.jpeg"),
        ("U005175", "BACK-MATTER/NOTES/_page_888_Picture_7.jpeg"),
        ("U005176", "BACK-MATTER/NOTES/_page_888_Picture_8.jpeg"),
        ("U005177", "BACK-MATTER/NOTES/_page_888_Picture_9.jpeg"),
    ],
)

triangle_circles = procedure_candidate(
    key="triangular-circle-array",
    name="triangular-array centered-circle ornament",
    anchor="U005178",
    aliases=["Phoenician triangular circle pattern"],
    description=(
        "Arrange holes in a triangular array and draw a circle centered at each hole."
    ),
    carrier="Circle centers and circular arcs.",
    support="A planar triangular lattice of holes.",
    state="The fixed center array together with circles already drawn.",
    result="A repeated overlapping-circle ornament.",
    missing=(
        "The passage omits array extent, circle radius, edge clipping, and a "
        "formal completion convention."
    ),
)

celtic_circles = procedure_candidate(
    key="celtic-touching-circles",
    name="Desborough tangent-circle ornament construction",
    anchor="U005179",
    aliases=["Desborough Mirror circle construction"],
    description=(
        "Assemble the engraved pattern from portions of circles arranged to "
        "touch one another as shown in the staged diagrams."
    ),
    carrier="Circular arcs and tangency points.",
    support="A bounded planar ornament region.",
    state="The partial collection of touching circular arcs.",
    result="The Desborough-style tangent-circle pattern.",
    missing=(
        "The source does not give exact centers, radii, arc-selection rules, "
        "scale, or a textual step order."
    ),
)
attach_procedure_images(
    celtic_circles,
    label_prefix="celtic-circle-stage",
    entries=[
        ("U005180", "BACK-MATTER/NOTES/_page_888_Picture_12.jpeg"),
        ("U005181", "BACK-MATTER/NOTES/_page_888_Picture_13.jpeg"),
        ("U005182", "BACK-MATTER/NOTES/_page_888_Picture_14.jpeg"),
        ("U005183", "BACK-MATTER/NOTES/_page_888_Picture_15.jpeg"),
    ],
)

roman_rosette = procedure_candidate(
    key="roman-rosette",
    name="48-spoke Roman rosette construction",
    anchor="U005184",
    aliases=["Roman mosaic rosette procedure"],
    description=(
        "Construct 48 regularly spaced spokes by repeated angle bisection, draw "
        "semicircles centered at the spoke ends, then add concentric circles "
        "through the intersection points."
    ),
    carrier="Spokes, semicircles, intersections, and concentric circles.",
    support="A planar circular construction region.",
    state="The accumulated straight and circular construction lines.",
    result="A completed 48-fold rosette pattern.",
    missing=(
        "The passage does not specify the initial radius, compass orientation, "
        "which semicircle side to retain, or degeneracy handling."
    ),
)
attach_procedure_images(
    roman_rosette,
    label_prefix="roman-rosette-stage",
    entries=[
        ("U005185", "BACK-MATTER/NOTES/_page_888_Picture_17.jpeg"),
        ("U005186", "BACK-MATTER/NOTES/_page_888_Picture_18.jpeg"),
        ("U005187", "BACK-MATTER/NOTES/_page_888_Picture_19.jpeg"),
        ("U005188", "BACK-MATTER/NOTES/_page_888_Picture_20.jpeg"),
    ],
)

cosmati = procedure_candidate(
    key="cosmati-triangles",
    name="Cosmati nested-equilateral-triangle construction",
    anchor="U005193",
    aliases=["Cosmati triangle nesting"],
    description=(
        "Recursively place the same equilateral-triangle structure at smaller "
        "scales inside the available triangular regions, as shown in the "
        "construction diagrams."
    ),
    carrier="Equilateral triangular tiles or regions.",
    support="A bounded equilateral-triangle region.",
    state="The collection of triangles present at each nesting level.",
    result="A finite approximately nested Cosmati mosaic pattern.",
    missing=(
        "The source does not provide an exact recursion depth, triangle-choice "
        "order, size ratios for every branch, or treatment of material gaps."
    ),
)
attach_procedure_images(
    cosmati,
    label_prefix="cosmati-stage",
    entries=[
        ("U005194", "BACK-MATTER/NOTES/_page_889_Picture_3.jpeg"),
        ("U005195", "BACK-MATTER/NOTES/_page_889_Picture_4.jpeg"),
        ("U005196", "BACK-MATTER/NOTES/_page_889_Picture_5.jpeg"),
        ("U005197", "BACK-MATTER/NOTES/_page_889_Picture_6.jpeg"),
        ("U005198", "BACK-MATTER/NOTES/_page_889_Picture_7.jpeg"),
    ],
)

triangle_push = procedure_candidate(
    key="triangle-grid-push",
    name="triangle-grid push-in/push-out ornament construction",
    anchor="U005203",
    aliases=["Alcázar triangular-grid pattern"],
    description=(
        "Start from a grid of triangles and consistently push each triangle "
        "side inward or outward."
    ),
    carrier="Triangular grid edges.",
    support="A two-dimensional triangular tiling.",
    state="The current placement/deformation of every triangle side.",
    result="A repeated interlocking tiled ornament.",
    missing=(
        "The source does not state the exact push assignment, displacement "
        "magnitude, boundary handling, or consistency rule at shared sides."
    ),
)

rope = procedure_candidate(
    key="nested-rope",
    name="nested twisted-strand rope assembly",
    anchor="U005209",
    aliases=["7 x 7 x 7 wire-rope preset"],
    description=(
        "Twist strands together, with each strand itself formed by twisting "
        "smaller strands; one explicit wire-rope preset uses 7 x 7 x 7 units."
    ),
    carrier="Strands recursively grouped into larger strands or rope.",
    support="A finite hierarchical cross-section and longitudinal twist.",
    state="The nested grouping and twist orientation of all component strands.",
    result="A multilevel rope or wire-rope assembly.",
    missing=(
        "The source does not state handedness, pitch, exact geometric placement, "
        "material constraints, or failure/completion tolerances."
    ),
)
attach_procedure_images(
    rope,
    label_prefix="rope-stage",
    entries=[
        ("U005210", "BACK-MATTER/NOTES/_page_889_Picture_19.jpeg"),
        ("U005211", "BACK-MATTER/NOTES/_page_889_Picture_20.jpeg"),
        ("U005212", "BACK-MATTER/NOTES/_page_889_Picture_21.jpeg"),
    ],
)

truchet = source_candidate(
    key="truchet-pattern-space",
    name="Truchet four-tile planar pattern space",
    anchor="U005225",
    aliases=["Truchet tiles"],
    facts={
        "object_kind": "A finite-alphabet planar tiling/pattern space.",
        "carrier": "Square tile positions.",
        "support": "A two-dimensional square grid.",
        "topology": "Orthogonally adjacent square tile sites.",
        "structural_invariants": "Every site is occupied by one congruent square tile.",
        "alphabet_or_value_schema": (
            "Four square tiles distinguished by which triangular half is filled: "
            "◣, ◥, ◤, or ◢."
        ),
        "complete_state": "One choice of the four tile values at every grid site.",
        "frontier_or_activation": "A tile value is chosen for each site.",
        "law_kind": "Free combination over a four-tile alphabet.",
        "rule_relation_constraint_function_or_probability_law": (
            "Form two-dimensional patterns by combining the four stated tile types "
            "in all or selected possible ways."
        ),
        "write_replacement_assembly_or_commit": "Place the chosen tile at each grid site.",
        "result_kind": "A completed planar tile pattern.",
        "successor_cardinality": (
            "Four local choices per unconstrained site; the source does not impose a measure."
        ),
        "determinism_branching_or_measure": (
            "Nondeterministic/enumerative unless a separate tile-selection rule is supplied."
        ),
        "parameters_and_variants": "Grid extent and tile choice at each position.",
        "excluded_observers_and_representations": (
            "Leonardo/Truchet history and artistic use are contextual."
        ),
        "evidence_limit": (
            "The passage does not specify a selection measure, adjacency "
            "constraint, enumeration order, or completion boundary."
        ),
    },
    claim=(
        "The source explicitly gives the four-tile alphabet and describes "
        "forming 2D patterns by combining those tiles."
    ),
    missing=(
        "The passage does not specify a selection measure, adjacency constraint, "
        "enumeration order, or completion boundary."
    ),
)


# ---------------------------------------------------------------------------
# Historically identified systems with enough identity-bearing mechanics to
# survive blind discovery.  The routes deliberately retain the limits of these
# passages instead of filling in omitted transition tables from outside the
# assigned Chapter 2 pair.

life = source_candidate(
    key="game-of-life",
    name="Conway's Game of Life cellular automaton preset",
    anchor="U000301",
    aliases=["Game of Life", "Life"],
    facts={
        "object_kind": "A specifically named two-dimensional cellular automaton preset.",
        "native_time": "Discrete cellular-automaton evolution.",
        "carrier": "Cells in a two-dimensional cellular array.",
        "support": "A two-dimensional cellular space.",
        "complete_state": "The value of every cell in the two-dimensional array.",
        "law_kind": "A fixed two-dimensional cellular-automaton rule set.",
        "result_kind": "An evolution that can contain repetitive and other structures.",
        "parameters_and_variants": (
            "The passage distinguishes the specific rules of Life from the "
            "variety of 2D rules Conway tested."
        ),
        "excluded_observers_and_representations": (
            "Recreational use, engineering interpretations of structures, "
            "popularity, and observed complexity are context rather than native mechanics."
        ),
        "evidence_limit": (
            "Neither Chapter 2 passage states the Life birth/survival table, "
            "cell alphabet, neighborhood, boundary, seed, or commit convention."
        ),
    },
    claim=(
        "The main text identifies Game of Life as a specific two-dimensional "
        "cellular automaton and distinguishes its structures and behavior from "
        "the one-dimensional examples."
    ),
    missing=(
        "Neither Chapter 2 passage states the Life birth/survival table, cell "
        "alphabet, neighborhood, boundary, seed, or commit convention."
    ),
    strength="DIRECT_IDENTITY",
    route_keys=["life-page249"],
)
add_evidence(
    life,
    label="game-of-life-history",
    unit="U005233",
    claim=(
        "The Notes identify Conway's 1970 fixed Life rule set, distinguish it "
        "from the other 2D rules tested, and route the omitted mechanics to page 249."
    ),
    fields=[
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "complete_state",
        "law_kind",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="DIRECT_IDENTITY",
)

von_neumann_ca = source_candidate(
    key="von-neumann-29color-ca",
    name="von Neumann 29-color self-reproduction cellular automaton",
    anchor="U005229",
    aliases=["von Neumann self-reproducing automaton"],
    facts={
        "object_kind": (
            "A particular two-dimensional cellular automaton designed to model "
            "self-reproduction and computer/mechanical components."
        ),
        "native_time": "Discrete cellular-automaton evolution.",
        "carrier": "Cells in a two-dimensional cellular array.",
        "support": "A two-dimensional cellular space.",
        "alphabet_or_value_schema": "Twenty-nine possible colors for each cell.",
        "complete_state": "A color assignment to the two-dimensional cell array.",
        "seed": (
            "An outlined approximately 200,000-cell configuration intended to "
            "reproduce itself."
        ),
        "law_kind": "A fixed, complicated local cellular-automaton rule.",
        "result_kind": (
            "A cellular evolution intended to emulate components and support "
            "a self-reproducing configuration."
        ),
        "parameters_and_variants": (
            "The source fixes two dimensions, 29 colors, and the historical "
            "1952–3 construction."
        ),
        "excluded_observers_and_representations": (
            "The earlier factory, differential-equation, robotics, and toy-set "
            "ideas are historical antecedents, not state of this cellular automaton."
        ),
        "evidence_limit": (
            "The local transition table, neighborhood, exact 200,000-cell seed, "
            "boundary, and reproduction witness are not supplied in this range."
        ),
    },
    claim=(
        "The source delimits von Neumann's 1952–3 construction as a 2D "
        "29-color cellular automaton and states its intended component and "
        "self-reproduction roles."
    ),
    missing=(
        "The local transition table, neighborhood, exact 200,000-cell seed, "
        "boundary, and reproduction witness are not supplied in this range."
    ),
    strength="DIRECT_PARTIAL_MECHANICS",
    route_keys=[
        "von-neumann-self-reproduction-page1179",
        "von-neumann-universality-page1115",
    ],
)
add_evidence(
    von_neumann_ca,
    label="von-neumann-followup-routes",
    unit="U005230",
    claim=(
        "The historical continuation routes later self-reproducing and "
        "universal cellular-automaton constructions while supplying no missing "
        "transition table for the 29-color preset."
    ),
    fields=[
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
    modality="CROSS_REFERENCE",
)

ulam_objects = source_candidate(
    key="ulam-recursive-2d-ca",
    name="Ulam recursively defined geometrical-object cellular automata",
    anchor="U005232",
    aliases=["recursively defined geometrical objects"],
    facts={
        "object_kind": (
            "A small historical collection of generalized two-dimensional "
            "cellular-automaton presets."
        ),
        "native_time": "Discrete evolution from an initial cellular configuration.",
        "carrier": "Cells in a two-dimensional array.",
        "support": "A two-dimensional cellular space.",
        "alphabet_or_value_schema": (
            "At least black and non-black cell values are distinguished."
        ),
        "complete_state": "The cellular values across the two-dimensional support.",
        "seed": "A single black cell.",
        "law_kind": "Generalized two-dimensional local cellular-automaton growth rules.",
        "result_kind": "Recursively generated geometrical growth patterns.",
        "parameters_and_variants": "A handful of different unspecified rules were simulated.",
        "excluded_observers_and_representations": (
            "Computer model, picture size, biological speculation, and observed "
            "complexity are contextual."
        ),
        "evidence_limit": (
            "The individual rule tables, alphabet, neighborhoods, boundary, and "
            "exact correspondence among the historical examples are omitted."
        ),
    },
    claim=(
        "The passage explicitly identifies Ulam's objects as generalized 2D "
        "cellular automata evolved from single black cells."
    ),
    missing=(
        "The individual rule tables, alphabet, neighborhoods, boundary, and "
        "exact correspondence among the historical examples are omitted."
    ),
    strength="DIRECT_PARTIAL_MECHANICS",
    route_keys=["ulam-page928"],
)

fredkin_rule90 = source_candidate(
    key="fredkin-2d-rule90",
    name="Fredkin two-dimensional analog of Rule 90",
    anchor="U005232",
    aliases=["2D analog of rule 90"],
    facts={
        "object_kind": "A particular two-dimensional cellular-automaton preset.",
        "native_time": "Discrete cellular-automaton evolution.",
        "carrier": "Cells in a two-dimensional array.",
        "support": "A two-dimensional cellular space.",
        "law_kind": "A two-dimensional analog of the Rule 90 local law.",
        "result_kind": "A cellular evolution with reported self-reproduction properties.",
        "parameters_and_variants": (
            "The source fixes the historical 1961 PDP-1 simulation and its "
            "stated relationship to Rule 90."
        ),
        "excluded_observers_and_representations": (
            "The PDP-1 implementation and reported self-reproduction are not "
            "substitutes for the omitted native rule."
        ),
        "evidence_limit": (
            "The meaning of '2D analog', neighborhood, alphabet, transition "
            "table, seed, boundary, and reproduction witness are not stated."
        ),
    },
    claim=(
        "The same historical passage delimits Fredkin's 1961 simulation as a "
        "two-dimensional analog of Rule 90 and records its intended property."
    ),
    missing=(
        "The meaning of '2D analog', neighborhood, alphabet, transition table, "
        "seed, boundary, and reproduction witness are not stated."
    ),
    strength="DIRECT_IDENTITY",
    route_keys=["fredkin-page1179"],
)

code20 = source_candidate(
    key="code20",
    name="binary range-2 totalistic code 20 cellular automaton",
    anchor="U005233",
    aliases=["k=2 r=2 totalistic code 20", "Millen one-dimensional Life analog"],
    facts={
        "object_kind": "A named one-dimensional totalistic cellular-automaton preset.",
        "native_time": "Discrete cellular-automaton evolution.",
        "carrier": "Cells in a one-dimensional array.",
        "support": "A one-dimensional cellular space.",
        "topology": "A centered range-2 neighborhood of five cells.",
        "alphabet_or_value_schema": "Two cell values.",
        "complete_state": "The value at every one-dimensional cell position.",
        "frontier_or_activation": "The totalistic rule applies across the cellular support.",
        "read_dependencies_or_neighborhood": "Two neighbors on each side plus the cell itself.",
        "law_kind": "A deterministic totalistic local cellular-automaton rule.",
        "result_kind": "A uniquely determined next configuration once code 20 is decoded.",
        "parameters_and_variants": "k = 2, r = 2, totalistic code 20.",
        "excluded_observers_and_representations": (
            "Its historical motivation as a one-dimensional analog of Life is contextual."
        ),
        "evidence_limit": (
            "The passage names the code but does not expand its totalistic "
            "lookup, seed, boundary, code-number convention, or completion semantics."
        ),
    },
    claim=(
        "The source identifies Millen's example exactly as the k=2, r=2 "
        "totalistic code 20 preset and routes its omitted rule to page 283."
    ),
    missing=(
        "The passage names the code but does not expand its totalistic lookup, "
        "seed, boundary, code-number convention, or completion semantics."
    ),
    strength="DIRECT_IDENTITY",
    route_keys=["code20-page283"],
)

lfsr = source_candidate(
    key="linear-feedback-shift-register",
    name="linear feedback shift-register construction class",
    anchor="U005236",
    aliases=["LFSR", "finite one-dimensional additive cellular automaton"],
    facts={
        "object_kind": (
            "A finite shift-register sequence generator identified with "
            "one-dimensional additive cellular automata."
        ),
        "native_time": "Discrete register shifts and feedback steps.",
        "carrier": "A finite ordered register of digital cells.",
        "support": "A finite one-dimensional register.",
        "alphabet_or_value_schema": "Digital values such as binary digits.",
        "complete_state": "The current value stored in every register cell.",
        "visible_history": "Successive output digits form a generated sequence.",
        "law_kind": "A linear feedback/shift law, equivalently an additive CA law.",
        "result_kind": "A deterministic output sequence for a fixed register and seed.",
        "determinism_branching_or_measure": (
            "Deterministic; apparent complexity is generated without a stated probability law."
        ),
        "parameters_and_variants": (
            "Register length, feedback relation, seed, and output convention vary."
        ),
        "excluded_observers_and_representations": (
            "Communications use, cryptography, repetition-period analysis, and "
            "hardware realization are applications or observations."
        ),
        "evidence_limit": (
            "No particular tap set, shift direction, feedback polynomial, seed, "
            "output cell, or finite-boundary correspondence is specified here."
        ),
    },
    claim=(
        "The history passage identifies linear feedback shift registers as "
        "finite one-dimensional additive cellular automata and as deterministic "
        "sequence generators."
    ),
    missing=(
        "No particular tap set, shift direction, feedback polynomial, seed, "
        "output cell, or finite-boundary correspondence is specified here."
    ),
    strength="DIRECT_PARTIAL_MECHANICS",
    route_keys=["lfsr-page974", "lfsr-page259"],
)

shift_block_maps = source_candidate(
    key="shift-commuting-block-map",
    name="shift-commuting block-map cellular-automaton class",
    anchor="U005237",
    aliases=["symbolic-dynamics block map"],
    facts={
        "object_kind": (
            "A mapping class on infinite binary sequences stated to be exactly "
            "the class of one-dimensional cellular automata."
        ),
        "native_time": "One application of a sequence-to-sequence map.",
        "carrier": "Positions in an infinite binary sequence.",
        "support": "A one-dimensional infinite sequence.",
        "topology": "The integer shift on sequence positions.",
        "alphabet_or_value_schema": "Binary values 0 and 1.",
        "complete_state": "An infinite sequence of 0s and 1s.",
        "frontier_or_activation": "The block map determines an output at every position.",
        "schedule": "The complete output sequence is determined from the input sequence.",
        "read_dependencies_or_neighborhood": "A finite local block around each output position.",
        "law_kind": "A shift-commuting finite-block map.",
        "rule_relation_constraint_function_or_probability_law": (
            "Apply the same finite-block mapping equivariantly at every sequence position."
        ),
        "result_kind": "One output binary sequence.",
        "parameters_and_variants": "The finite block radius and local mapping vary.",
        "excluded_observers_and_representations": (
            "Symbolic-dynamics terminology, cryptographic use, and global theorem "
            "statements are representations, applications, or analysis."
        ),
        "evidence_limit": (
            "The passage states exact class identity but supplies no particular "
            "block map, radius, boundary issue, or proof of the correspondence."
        ),
    },
    claim=(
        "The source states that shift-commuting block maps on binary sequences "
        "are exactly one-dimensional cellular automata."
    ),
    missing=(
        "The passage states exact class identity but supplies no particular "
        "block map, radius, boundary issue, or proof of the correspondence."
    ),
    strength="DIRECT_PARTIAL_MECHANICS",
    route_keys=["shift-maps-page960", "shift-maps-page961"],
)

code10 = source_candidate(
    key="code10",
    name="binary range-2 totalistic code 10 cellular automaton",
    anchor="U005316",
    aliases=["k=2 r=2 totalistic code 10"],
    facts={
        "object_kind": "A named one-dimensional totalistic cellular-automaton preset.",
        "native_time": "Discrete cellular-automaton evolution.",
        "carrier": "Cells in a one-dimensional array.",
        "support": "A one-dimensional cellular space.",
        "topology": "A centered range-2 neighborhood of five cells.",
        "alphabet_or_value_schema": "Two values, black and white.",
        "complete_state": "The black/white value at every cell position.",
        "frontier_or_activation": "Every cell receives a next-step value.",
        "schedule": "The five-cell totalistic rule is applied for each discrete step.",
        "read_dependencies_or_neighborhood": "The cell and two neighbors on each side.",
        "law_kind": "A deterministic totalistic local lookup rule.",
        "rule_relation_constraint_function_or_probability_law": (
            "The next cell is black iff exactly 1 or 3 of its five neighborhood "
            "cells are black; otherwise it is white."
        ),
        "write_replacement_assembly_or_commit": (
            "One black or white replacement value is produced for every cell."
        ),
        "result_kind": "A uniquely determined next configuration and iterated evolution.",
        "successor_cardinality": "Exactly one successor for each complete configuration.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": "k = 2, r = 2, totalistic code 10.",
        "excluded_observers_and_representations": (
            "The two displayed evolution images and randomness comparison are "
            "observer evidence, not additional native state or law."
        ),
        "evidence_limit": (
            "The passage does not state the seed used in the displayed images, "
            "boundary, code-number convention, completion, or witness semantics."
        ),
    },
    claim=(
        "The source gives the complete five-cell totalistic transition law for "
        "binary range-2 code 10."
    ),
    missing=(
        "The passage does not state the seed used in the displayed images, "
        "boundary, code-number convention, completion, or witness semantics."
    ),
    strength="DIRECT_PARTIAL_MECHANICS",
)


# Candidate-bearing routes whose source sentences are already candidate
# provenance.  Two generalized profiles gain contextual evidence here because
# U005008 is the sentence that points to their missing implementations.
rule170["route_keys"].append("rule170-page153")
totalistic_profile = next(
    item for item in ALL_CANDIDATE_SPECS if item["key"] == "totalistic-ca"
)
totalistic_profile["route_keys"].append("totalistic-page886")
add_evidence(
    totalistic_profile,
    label="totalistic-implementation-route",
    unit="U005008",
    claim=(
        "The Notes explicitly route implementation of totalistic cellular "
        "automata to page 886 without adding a second native rule."
    ),
    fields=[
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
    modality="CROSS_REFERENCE",
)
rectangular_profile = next(
    item for item in ALL_CANDIDATE_SPECS if item["key"] == "rectangular-dd-ca"
)
rectangular_profile["route_keys"].append("higher-dimensional-page927")
add_evidence(
    rectangular_profile,
    label="higher-dimensional-implementation-route",
    unit="U005008",
    claim=(
        "The same sentence routes fuller higher-dimensional cellular-automaton "
        "implementation mechanics to page 927."
    ),
    fields=[
        "support",
        "topology",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
    modality="CROSS_REFERENCE",
)


# ---------------------------------------------------------------------------
# Construction-relevant cross-reference obligations.  Behavior-only page
# mentions and ordinary display continuations are left as observer/context
# dispositions; these routes are the ones that can complete, distinguish, or
# independently discover a construction-bearing object.

ALL_ROUTE_SPECS: list[RouteSpec] = []


def add_route(
    *,
    key: str,
    unit: str,
    literal: str,
    topic: str,
    vocabulary: list[str],
    scope: str = "CROSS_RANGE",
    kind: str = "PAGE",
) -> None:
    if any(item["key"] == key for item in ALL_ROUTE_SPECS):
        raise AuthoringError(f"duplicate route key {key}")
    ALL_ROUTE_SPECS.append(
        {
            "key": key,
            "unit": unit,
            "literal": literal,
            "topic": topic,
            "vocabulary": vocabulary,
            "scope": scope,
            "kind": kind,
            "_insertion": len(ALL_ROUTE_SPECS),
        }
    )


add_route(
    key="rule-numbering-page53",
    unit="U004966",
    literal="The numbering of rules is discussed on page 53.",
    topic="elementary cellular-automaton rule-number decoding",
    vocabulary=["numbering of rules", "elementary rule", "page 53"],
)
add_route(
    key="built-in-ca-page867",
    unit="U004984",
    literal="the built-in CellularAutomaton function ... discussed on page 867",
    topic="built-in cellular-automaton evolution interface and semantics",
    vocabulary=["CellularAutomaton", "built-in function", "page 867"],
    scope="WITHIN_STAGE",
)
add_route(
    key="bitwise-formulas-page869",
    unit="U004996",
    literal="Boolean expressions ... can be quite complicated (see page 869)",
    topic="Boolean and algebraic representations of cellular-automaton rules",
    vocabulary=["Boolean expressions", "bitwise", "cellular automaton rules"],
    scope="WITHIN_STAGE",
)
add_route(
    key="general-rule-page60",
    unit="U004997",
    literal="explicit replacements for all possible blocks ... (see page 60)",
    topic="general one-dimensional cellular-automaton rule schema",
    vocabulary=["explicit replacements", "blocks", "neighborhood"],
)
add_route(
    key="totalistic-page886",
    unit="U005008",
    literal="implementation of totalistic cellular automata on page 886",
    topic="totalistic cellular-automaton rule decoding and implementation",
    vocabulary=["totalistic cellular automata", "implementation", "page 886"],
)
add_route(
    key="higher-dimensional-page927",
    unit="U005008",
    literal="higher-dimensional cellular automata on page 927",
    topic="higher-dimensional cellular-automaton native mechanics",
    vocabulary=["higher-dimensional", "cellular automata", "page 927"],
)
add_route(
    key="built-in-profile-page886",
    unit="U005009",
    literal="see also page 886",
    topic="general built-in cellular-automaton profile semantics",
    vocabulary=["CellularAutomaton", "general function", "page 886"],
)
add_route(
    key="cantor-map-page959",
    unit="U005110",
    literal="Compare page 959.",
    topic="cellular automata as continuous maps on Cantor sequence space",
    vocabulary=["Cantor set", "continuous mapping", "cellular automaton"],
)
add_route(
    key="rule170-page153",
    unit="U005112",
    literal="compare page 153",
    topic="Rule 170 shift-map mechanics and correspondence",
    vocabulary=["rule 170", "shift map", "Mod[2 x, 1]"],
)
add_route(
    key="pascal-page611",
    unit="U005113",
    literal="As shown on page 611",
    topic="Pascal-triangle parity construction",
    vocabulary=["Pascal's triangle", "binomial coefficients", "modulo 2"],
)
add_route(
    key="rule60-page58",
    unit="U005117",
    literal="the one produced by rule 60 (see page 58)",
    topic="Rule 60 cellular-automaton mechanics",
    vocabulary=["rule 60", "Binomial", "modulo 2"],
)
add_route(
    key="rule60-bit-page583",
    unit="U005117",
    literal="or (see page 583)",
    topic="direct bitwise formula for the Rule 60 pattern",
    vocabulary=["BitAnd", "rule 60", "digit sequences"],
)
add_route(
    key="additive-page952",
    unit="U005127",
    literal="additive rules, discussed further on page 952",
    topic="additive cellular-automaton restriction and mechanics",
    vocabulary=["additive rules", "cellular automata", "page 952"],
)
add_route(
    key="additive-continuous-page922",
    unit="U005127",
    literal="See also page 922 for the continuous case.",
    topic="continuous analog of the additive-rule construction",
    vocabulary=["additive", "continuous case", "page 922"],
)
add_route(
    key="gcd-page613",
    unit="U005134",
    literal="GCD[m, n] yields a more complicated pattern (see page 613)",
    topic="greatest-common-divisor function and its pattern",
    vocabulary=["GCD", "integer function", "page 613"],
)
add_route(
    key="jacobi-page1081",
    unit="U005134",
    literal="JacobiSymbol[m, 2 n - 1] (see page 1081)",
    topic="Jacobi-symbol function and its modulo-two pattern",
    vocabulary=["JacobiSymbol", "integer function", "page 1081"],
)
add_route(
    key="function-combinations-page747",
    unit="U005134",
    literal="various combinations of functions (see page 747)",
    topic="compositions of integer functions that generate patterns",
    vocabulary=["combinations of functions", "integer functions", "page 747"],
)
add_route(
    key="rule30-completeness-page725",
    unit="U005144",
    literal="All possible blocks appear to occur eventually (see page 725).",
    topic="Rule 30 block-occurrence property and supporting definition",
    vocabulary=["rule 30", "all possible blocks", "page 725"],
)
add_route(
    key="rule30-column-page1087",
    unit="U005148",
    literal="the arguments on page 1087",
    topic="Rule 30 center-column nonrepetition evidence",
    vocabulary=["rule 30", "center column", "repeat"],
)
add_route(
    key="rule110-page229",
    unit="U005149",
    literal="details of rule 110 ... on page 229",
    topic="Rule 110 detailed mechanics and behavior",
    vocabulary=["rule 110", "details", "page 229"],
)
add_route(
    key="rule110-page675",
    unit="U005149",
    literal="details of rule 110 ... on page 675",
    topic="Rule 110 detailed mechanics and computation",
    vocabulary=["rule 110", "details", "page 675"],
)
add_route(
    key="rule110-structures-page292",
    unit="U005149",
    literal="Localized structures ... are shown on page 292.",
    topic="Rule 110 localized-structure definitions",
    vocabulary=["rule 110", "localized structures", "page 292"],
)
add_route(
    key="cosmati-apollonian-page986",
    unit="U005193",
    literal="Compare the Apollonian packing of page 986.",
    topic="Apollonian circle-packing construction",
    vocabulary=["Apollonian packing", "nested", "page 986"],
)
add_route(
    key="paperfolding-page892",
    unit="U005214",
    literal="the nested form on page 892",
    topic="nested paperfolding construction",
    vocabulary=["paperfolding", "nested form", "page 892"],
)
add_route(
    key="logic-page1099",
    unit="U005216",
    literal="See page 1099.",
    topic="logic-rule generators and constraints",
    vocabulary=["logic", "rules", "page 1099"],
)
add_route(
    key="grammar-page1103",
    unit="U005217",
    literal="See page 1103.",
    topic="formal grammar construction mechanics",
    vocabulary=["grammar", "generating structures", "page 1103"],
)
add_route(
    key="firing-squad-page1035",
    unit="U005220",
    literal="the firing squad problem on page 1035",
    topic="firing-squad synchronization cellular automaton",
    vocabulary=["firing squad", "synchronization", "page 1035"],
)
add_route(
    key="cryptography-page1085",
    unit="U005223",
    literal="See page 1085.",
    topic="rule-based cryptographic constructions",
    vocabulary=["cryptography", "rules", "page 1085"],
)
add_route(
    key="maze-page873",
    unit="U005224",
    literal="the one shown on page 873",
    topic="classical labyrinth construction procedure",
    vocabulary=["maze designs", "labyrinth", "page 873"],
    scope="WITHIN_STAGE",
)
add_route(
    key="von-neumann-self-reproduction-page1179",
    unit="U005230",
    literal="cellular automata capable of self-reproduction (see page 1179)",
    topic="self-reproducing cellular-automaton construction mechanics",
    vocabulary=["self-reproduction", "cellular automata", "page 1179"],
)
add_route(
    key="von-neumann-universality-page1115",
    unit="U005230",
    literal="universal computation (see page 1115)",
    topic="universal cellular-automaton construction mechanics",
    vocabulary=["universal computation", "cellular automata", "page 1115"],
)
add_route(
    key="garden-of-eden-page961",
    unit="U005230",
    literal="Garden of Eden result ... see page 961",
    topic="Garden-of-Eden cellular-automaton property and configuration class",
    vocabulary=["Garden of Eden", "initial conditions", "page 961"],
)
add_route(
    key="historical-firing-squad-page1035",
    unit="U005230",
    literal="firing squad synchronization, as on page 1035",
    topic="firing-squad synchronization construction",
    vocabulary=["firing squad", "synchronization", "page 1035"],
)
add_route(
    key="ulam-page928",
    unit="U005232",
    literal="generalized 2D cellular automata ... (see page 928)",
    topic="Ulam generalized two-dimensional growth automata",
    vocabulary=["Ulam", "2D cellular automata", "single black cells"],
)
add_route(
    key="ulam-number-sequence-page908",
    unit="U005232",
    literal="sequences based on numbers discussed on page 908",
    topic="Ulam's non-cellular one-dimensional number-sequence construction",
    vocabulary=["Ulam", "sequences based on numbers", "page 908"],
)
add_route(
    key="fredkin-page1179",
    unit="U005232",
    literal="the 2D analog of rule 90 ... (see page 1179)",
    topic="Fredkin's two-dimensional Rule 90 analog and self-reproduction",
    vocabulary=["Fredkin", "2D analog", "rule 90"],
)
add_route(
    key="life-page249",
    unit="U005233",
    literal="The Game of Life ... (see page 249)",
    topic="Conway Life transition, neighborhood, and seed mechanics",
    vocabulary=["Game of Life", "Conway", "page 249"],
)
add_route(
    key="code20-page283",
    unit="U005233",
    literal="code 20 k = 2, r = 2 totalistic rule from page 283",
    topic="binary range-2 totalistic code 20 lookup and code convention",
    vocabulary=["code 20", "totalistic", "k=2", "r=2"],
)
add_route(
    key="lfsr-page974",
    unit="U005236",
    literal="linear feedback shift registers (see page 974)",
    topic="linear feedback shift-register native update mechanics",
    vocabulary=["linear feedback shift register", "LFSR", "page 974"],
)
add_route(
    key="lfsr-page259",
    unit="U005236",
    literal="limited number of cells (compare page 259)",
    topic="finite additive cellular-automaton correspondence",
    vocabulary=["additive cellular automata", "limited number of cells", "page 259"],
)
add_route(
    key="nonlinear-feedback-page1088",
    unit="U005236",
    literal="ones surprisingly close to rule 30 (see page 1088)",
    topic="nonlinear feedback shift-register constructions near Rule 30",
    vocabulary=["nonlinear feedback shift register", "rule 30", "page 1088"],
)
add_route(
    key="shift-maps-page960",
    unit="U005237",
    literal="symbolic dynamics (see page 960)",
    topic="symbolic-dynamics sequence space and shift map",
    vocabulary=["symbolic dynamics", "infinite sequences", "page 960"],
)
add_route(
    key="shift-maps-page961",
    unit="U005237",
    literal="exactly 1D cellular automata (see page 961)",
    topic="shift-commuting block-map equivalence with one-dimensional cellular automata",
    vocabulary=["shift-commuting block maps", "1D cellular automata", "page 961"],
)

# The explicit historical checklist is retained as discovery routing, not
# multiplied into duplicate candidates in this chapter.
for key, unit, literal, topic, vocabulary, scope in [
    ("primes-perfect-page132", "U005242", "pages 132 and 910", "prime-number generation", ["primes", "simple problems", "page 132"], "CROSS_RANGE"),
    ("perfect-numbers-page910", "U005242", "pages 132 and 910", "perfect-number construction", ["perfect numbers", "simple problems", "page 910"], "CROSS_RANGE"),
    ("leonardo-constraints-page875", "U005244", "page 875", "Leonardo geometrical-constraint constructions", ["Leonardo da Vinci", "geometrical constraints", "page 875"], "WITHIN_STAGE"),
    ("continued-fractions-page143", "U005245", "pages 143 and 915", "continued-fraction construction from simple formulas", ["continued fractions", "simple formulas", "page 143"], "CROSS_RANGE"),
    ("continued-fractions-page915", "U005245", "pages 143 and 915", "continued-fraction construction details", ["continued fractions", "Euler", "page 915"], "CROSS_RANGE"),
    ("pi-digits-page136", "U005246", "page 136", "digit-sequence construction for pi", ["digits of pi", "transcendental numbers", "page 136"], "CROSS_RANGE"),
    ("three-body-page972", "U005248", "page 972", "three-body dynamical-system construction", ["three-body problem", "dynamics", "page 972"], "CROSS_RANGE"),
    ("thue-substitution-page893", "U005250", "page 893", "Thue substitution-system construction", ["Axel Thue", "substitution systems", "page 893"], "CROSS_RANGE"),
    ("combinators-page1121", "U005252", "page 1121", "combinator reduction systems", ["Schönfinkel", "combinators", "page 1121"], "CROSS_RANGE"),
    ("post-tag-page894", "U005253", "page 894", "Post tag-system mechanics", ["Emil Post", "tag system", "page 894"], "CROSS_RANGE"),
    ("godel-page782", "U005255", "page 782", "Gödel construction used in incompleteness", ["Gödel", "construction", "page 782"], "CROSS_RANGE"),
    ("three-n-plus-one-page904", "U005257", "page 904", "3 n + 1 iteration", ["3 n + 1", "iteration", "page 904"], "CROSS_RANGE"),
    ("prng-page974", "U005258", "page 974", "pseudorandom number-generator constructions", ["pseudorandom number generators", "page 974"], "CROSS_RANGE"),
    ("iterated-maps-page918", "U005264", "page 918", "iterated-map construction class", ["iterated maps", "simulation", "page 918"], "CROSS_RANGE"),
    ("neural-networks-page1099", "U005266", "page 1099", "idealized neural-network update mechanics", ["neural networks", "simulation", "page 1099"], "CROSS_RANGE"),
    ("hard-spheres-page999", "U005267", "page 999", "hard-sphere molecular dynamics", ["hard sphere", "molecules", "page 999"], "CROSS_RANGE"),
    ("close-nonlinear-feedback-page1088", "U005268", "page 1088", "Golomb nonlinear feedback shift registers", ["Golomb", "feedback shift register", "page 1088"], "CROSS_RANGE"),
    ("munching-foos-page871", "U005271", "page 871", "MIT munching-foos program mechanics", ["munching foos", "small computer programs", "page 871"], "WITHIN_STAGE"),
    ("minsky-tm-page81", "U005272", "page 81", "Minsky simple Turing-machine mechanics", ["Minsky", "Turing machines", "page 81"], "CROSS_RANGE"),
    ("lorenz-pde-page971", "U005273", "page 971", "Lorenz differential-equation relation", ["Lorenz", "differential equation", "page 971"], "CROSS_RANGE"),
    ("random-boolean-page936", "U005274", "page 936", "random Boolean-network construction", ["random Boolean networks", "page 936"], "CROSS_RANGE"),
    ("paterson-worms-page930", "U005276", "page 930", "Paterson two-dimensional Turing-machine worms", ["Paterson", "worms", "2D Turing machines"], "CROSS_RANGE"),
    ("restricted-2d-ca-page864", "U005277", "page 864", "property-restricted two-dimensional cellular automata", ["2D cellular automata", "forced properties", "page 864"], "CROSS_RANGE"),
    ("fractals-page934", "U005278", "page 934", "fractal generation constructions", ["Mandelbrot", "fractals", "page 934"], "CROSS_RANGE"),
    ("hofstadter-sequence-page907", "U005280", "page 907", "Hofstadter recursive-sequence construction", ["Hofstadter", "recursive sequence", "page 907"], "CROSS_RANGE"),
    ("mandelbrot-page934", "U005281", "page 934", "Mandelbrot-set iteration", ["Mandelbrot set", "page 934"], "CROSS_RANGE"),
    ("early-ca-experiment-page19", "U005286", "page 19", "1981 elementary-cellular-automaton experiment", ["computer experiments", "cellular automata", "page 19"], "CROSS_RANGE"),
    ("ca-classes-page231", "U005288", "page 231", "four cellular-automaton behavior classes", ["four basic classes", "random initial conditions", "page 231"], "CROSS_RANGE"),
    ("irreducibility-page737", "U005290", "page 737", "computational-irreducibility property", ["computational irreducibility", "page 737"], "CROSS_RANGE"),
    ("ca-fluid-page378", "U005292", "page 378", "cellular-automaton fluid construction", ["fluid mechanics", "cellular automata", "page 378"], "CROSS_RANGE"),
]:
    add_route(
        key=key,
        unit=unit,
        literal=literal,
        topic=topic,
        vocabulary=vocabulary,
        scope=scope,
    )
