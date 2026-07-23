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
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
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

integer_patterns = declarative_pattern(
    key="integer-function-patterns",
    name="integer-function modulo-two lattice-pattern family",
    anchor="U005134",
    definition=(
        "Evaluate a selected integer function over its integer argument lattice "
        "and reduce the values modulo 2; d-argument Multinomial yields a "
        "d-dimensional instance."
    ),
    support="A one- or d-dimensional integer-coordinate lattice.",
    values="Function values reduced modulo 2.",
    result="A static modular-value pattern.",
    aliases=["other integer functions"],
    route_keys=[
        "gcd-page613",
        "jacobi-page1081",
        "function-combinations-page747",
    ],
)

bitwise_patterns = declarative_pattern(
    key="bitwise-patterns",
    name="bitwise-function lattice-pattern family",
    anchor="U005135",
    definition=(
        "Evaluate a selected bitwise function on integer coordinates and display "
        "its values or a declared equality relation."
    ),
    support="An integer-coordinate lattice.",
    values="Integer or Boolean values produced by bitwise operations.",
    result="A static or parameter-indexed nested pattern.",
    aliases=["bitwise functions"],
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
    route_keys=["munching-page871"],
)

bitwise_curves = declarative_pattern(
    key="bitwise-curves",
    name="successive-n bitwise curve construction",
    anchor="U005139",
    definition=(
        "Generate curves from values obtained by applying selected bitwise "
        "functions to n and the left-shifted value 2n for successive n."
    ),
    support="Successive integer indices mapped into a plotted curve.",
    values="Integer values of a selected bitwise function.",
    result="A deterministic nested curve.",
    aliases=["bitwise n and 2n curves"],
)

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
