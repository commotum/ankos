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
    spec = source_candidate(
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
    return spec


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
        "law_kind": "Enumeration followed by execution and observation.",
        "rule_relation_constraint_function_or_probability_law": (
            "Enumerate the chosen program sequence, execute each program, and "
            "inspect the resulting behavior."
        ),
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
eca["evidence"][0]["fields"] = [
    "object_kind",
    "native_time",
    "law_kind",
    "parameters_and_variants",
    "evidence_limit",
]
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
eca["source_status"] = ["DEFECTIVE"]
eca["uncertainties"] = [
    (
        "U004988 contains the defective phrase “tries to updates”; the "
        "surrounding sentence still clearly supports old-snapshot update "
        "semantics without silently repairing the source wording."
    )
]
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
for label, unit, claim, fields, modality in [
    (
        "eca-rule-list-description",
        "U004966",
        "The Notes state the exact eight-entry Rule 30 list representation and "
        "identify rule-number decoding as a family parameterization.",
        [
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "eca-rule-number-code",
        "U004967",
        "The code deterministically decodes an elementary rule number into its "
        "eight binary lookup outputs.",
        [
            "alphabet_or_value_schema",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
    (
        "eca-step-description",
        "U004968",
        "The prose delimits one-step evaluation from a complete rule list and "
        "current cellular state.",
        [
            "native_time",
            "complete_state",
            "schedule",
            "law_kind",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "eca-step-code",
        "U004969",
        "The exact CAStep definition applies the eight-entry rule to every "
        "cyclic left/self/right neighborhood.",
        [
            "topology",
            "complete_state",
            "boundary",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
    (
        "eca-history-description",
        "U004970",
        "The prose defines an evolution result as a list of states for a "
        "requested number of steps.",
        [
            "native_time",
            "complete_state",
            "visible_history",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "eca-history-code",
        "U004971",
        "The exact CAEvolveList definition iterates CAStep t times while "
        "retaining the initial and successive states.",
        [
            "native_time",
            "complete_state",
            "visible_history",
            "schedule",
            "law_kind",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
]:
    add_evidence(
        eca,
        label=label,
        unit=unit,
        claim=claim,
        fields=fields,
        modality=modality,
        strength="DIRECT_PARTIAL_MECHANICS",
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
    label="rule254-direct-law",
    unit="U000186",
    claim=(
        "The prose states the exact Rule 254 transition: the next cell is black "
        "iff self or either immediate neighbor was black."
    ),
    fields=[
        "native_time",
        "alphabet_or_value_schema",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "evidence_limit",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
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
add_evidence(
    rule90,
    label="rule90-main-self-similar-outcome",
    unit="U000201",
    claim=(
        "The main-text caption identifies the displayed Rule 90 outcome as "
        "nested/fractal/self-similar; this supports the result description "
        "without turning the emergent property into native transition state."
    ),
    fields=[
        "result_kind",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
    modality="CAPTION",
)
add_evidence(
    rule90,
    label="rule90-decimation-property",
    unit="U005119",
    claim=(
        "The note gives an exact row/column decimation self-similarity and "
        "Sierpiński identification as behavior/property evidence."
    ),
    fields=[
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
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
add_evidence(
    rule30,
    label="rule30-built-in-single-seed-run",
    unit="U005038",
    claim=(
        "The built-in example states a three-step Rule 30 run from one value-1 "
        "cell surrounded by zeros."
    ),
    fields=[
        "native_time",
        "alphabet_or_value_schema",
        "seed",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)
add_evidence(
    rule30,
    label="rule30-built-in-single-seed-output",
    unit="U005039",
    claim=(
        "The exact call and four returned rows corroborate the named rule, "
        "seed profile, requested steps, and deterministic result."
    ),
    fields=[
        "object_kind",
        "native_time",
        "alphabet_or_value_schema",
        "complete_state",
        "seed",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
    strength="CORROBORATING",
)
add_evidence(
    rule30,
    label="rule30-prng-cryptosystem-application",
    unit="U005291",
    claim=(
        "The historical note records Rule 30 being proposed as a practical "
        "random-sequence generator and cryptosystem; these are applications, "
        "not additional native Rule 30 mechanics."
    ),
    fields=[
        "object_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
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
for label, unit, claim, fields, modality in [
    (
        "eca-formula-description",
        "U005084",
        "The Notes introduce a coordinate-indexed recurrence for the value of "
        "each cellular-automaton cell at each step.",
        [
            "native_time",
            "carrier",
            "support",
            "topology",
            "complete_state",
            "schedule",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "eca-formula-recurrence",
        "U005085",
        "The exact recurrence sets a[t,i] from the three predecessor values at "
        "i-1, i, and i+1 through the chosen function f.",
        [
            "native_time",
            "topology",
            "complete_state",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "FORMULA",
    ),
    (
        "eca-coordinate-query",
        "U005090",
        "The source explains that evaluating a[t,i] returns the requested cell "
        "after recursively computing the required predecessor values.",
        [
            "native_time",
            "complete_state",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "result_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "eca-memoized-recurrence",
        "U005091",
        "The memoized recurrence preserves the same three-cell native law while "
        "caching intermediate coordinate values as an implementation detail.",
        [
            "native_time",
            "schedule",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
]:
    add_evidence(
        eca,
        label=label,
        unit=unit,
        claim=claim,
        fields=fields,
        modality=modality,
        strength="DIRECT_PARTIAL_MECHANICS",
    )
add_evidence(
    rule90,
    label="rule90-formula-introduction",
    unit="U005086",
    claim=(
        "The prose identifies Rule 90 as a particular choice of the "
        "three-predecessor function f."
    ),
    fields=[
        "object_kind",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
        "evidence_limit",
    ],
)
add_evidence(
    rule90,
    label="rule90-pattern-table",
    unit="U005087",
    claim=(
        "The four pattern assignments give the complete Rule 90 lookup after "
        "eliminating the irrelevant self value."
    ),
    fields=[
        "alphabet_or_value_schema",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
    strength="DIRECT_COMPLETE_MECHANICS",
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
for label, unit, claim, fields, modality in [
    (
        "general-rule30-table",
        "U004998",
        "The code expands Rule 30 into all eight explicit three-cell "
        "replacement cases.",
        [
            "alphabet_or_value_schema",
            "topology",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
    (
        "general-step-introduction",
        "U004999",
        "The prose introduces one-step evaluation for explicit replacement rules.",
        [
            "native_time",
            "complete_state",
            "schedule",
            "law_kind",
            "result_kind",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "general-step-transpose",
        "U005000",
        "The exact definition assembles left/self/right blocks and applies the "
        "matching replacement at every position.",
        [
            "topology",
            "complete_state",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
    (
        "general-step-alternative",
        "U005001",
        "The source marks the following Partition definition as an equivalent "
        "one-step implementation.",
        [
            "law_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "general-step-partition",
        "U005002",
        "The exact Partition definition applies replacements to cyclic "
        "three-cell blocks at every position.",
        [
            "boundary",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
    (
        "general-pattern-rule-introduction",
        "U005003",
        "The prose permits pattern-valued replacement cases and introduces "
        "the compact Rule 90 table.",
        [
            "alphabet_or_value_schema",
            "law_kind",
            "parameters_and_variants",
            "evidence_limit",
        ],
        "PROSE",
    ),
    (
        "general-rule90-pattern-table",
        "U005004",
        "The four wildcard replacement cases give the complete Rule 90 law "
        "within the explicit-replacement schema.",
        [
            "alphabet_or_value_schema",
            "topology",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        "CODE",
    ),
]:
    add_evidence(
        general_1d,
        label=label,
        unit=unit,
        claim=claim,
        fields=fields,
        modality=modality,
        strength="DIRECT_PARTIAL_MECHANICS",
    )
add_evidence(
    rule30,
    label="rule30-explicit-replacement-table",
    unit="U004998",
    claim="The code independently expands Rule 30 into all eight neighborhood outputs.",
    fields=[
        "alphabet_or_value_schema",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
    strength="DIRECT_COMPLETE_MECHANICS",
)
add_evidence(
    rule90,
    label="rule90-explicit-pattern-table",
    unit="U005004",
    claim=(
        "The four wildcard cases independently give every Rule 90 output while "
        "showing that the self value is irrelevant."
    ),
    fields=[
        "alphabet_or_value_schema",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
    strength="DIRECT_COMPLETE_MECHANICS",
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
        "input": "A valid positive row length n.",
        "seed": "One black cell centered in a length-n white row.",
        "law_kind": "A deterministic initial-state constructor.",
        "rule_relation_constraint_function_or_probability_law": (
            "Create n zeros and replace position Ceiling[n/2] by 1."
        ),
        "write_replacement_assembly_or_commit": (
            "Assemble the length-n row, then replace its center entry by 1."
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
add_evidence(
    centered_seed,
    label="centered-seed-formula-description",
    unit="U005088",
    claim=(
        "The Notes introduce an explicit coordinate-form initial condition "
        "with one value-1 cell and zero elsewhere."
    ),
    fields=[
        "object_kind",
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "complete_state",
        "seed",
        "law_kind",
        "result_kind",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)
add_evidence(
    centered_seed,
    label="centered-seed-formula-code",
    unit="U005089",
    claim=(
        "The exact assignments set position 0 to 1 and every other position at "
        "step 0 to 0."
    ),
    fields=[
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "complete_state",
        "seed",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
    strength="DIRECT_COMPLETE_MECHANICS",
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
        "complete_state": (
            "A finite array together with an attempted off-end neighbor read."
        ),
        "input": (
            "A nonempty finite array and a neighbor lookup that crosses one endpoint."
        ),
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
        "result_kind": (
            "The uniquely resolved opposite-end source position/value for the "
            "off-end neighbor read."
        ),
        "successor_cardinality": (
            "Exactly one wrapped lookup result for each valid nonempty array and "
            "off-end neighbor query."
        ),
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
    spec = source_candidate(
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
    return spec


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
    "The current cellular configuration; the current step number is separate "
    "control state when the supplied function depends on it."
)
function_profile["facts"]["control_state"] = (
    "The current step number, beginning at 0, is exposed to the rule function."
)
function_profile["facts"]["schedule"] = (
    "At each discrete generation the function receives each old neighborhood "
    "and the current step number."
)
function_profile["facts"]["write_replacement_assembly_or_commit"] = (
    "The supplied function's result provides the value produced for each "
    "neighborhood application."
)
function_profile["evidence"][0]["fields"].append(
    "write_replacement_assembly_or_commit"
)
add_evidence(
    function_profile,
    label="function-ca-evolution-contract",
    unit="U005010",
    claim=(
        "The general built-in contract identifies an initial configuration, "
        "a finite number of discrete steps, and the resulting evolution list."
    ),
    fields=[
        "native_time",
        "complete_state",
        "schedule",
        "result_kind",
        "parameters_and_variants",
        "evidence_limit",
    ],
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
        "control_state",
        "schedule",
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
    carrier: str,
    support: str,
    topology: str,
    result: str,
    aliases: list[str] | None = None,
    seed_boundary: bool = True,
) -> CandidateSpec:
    missing = (
        "The compact specification does not state invalid-input behavior, "
        "native failure, or an independent witness convention."
    )
    facts = {
        "object_kind": "A cellular-automaton initial-state constructor class.",
        "carrier": carrier,
        "support": support,
        "topology": topology,
        "complete_state": result,
        "input": description,
        "seed": description,
        "boundary": description,
        "law_kind": "A deterministic initial-state constructor.",
        "rule_relation_constraint_function_or_probability_law": description,
        "write_replacement_assembly_or_commit": (
            "Assemble or overlay the declared pieces to construct the initial "
            "configuration."
        ),
        "result_kind": result,
        "successor_cardinality": (
            "Exactly one constructed initial configuration for a fixed valid "
            "specification."
        ),
        "determinism_branching_or_measure": (
            "Deterministic as an initial-state constructor."
        ),
        "parameters_and_variants": description,
        "excluded_observers_and_representations": (
            "The Mathematica list syntax is a representation of the "
            "constructor or projection."
        ),
        "evidence_limit": missing,
    }
    if not seed_boundary:
        facts.pop("boundary")
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
    carrier="An ordered finite list of cell values.",
    support="A finite one-dimensional row.",
    topology="Cyclic adjacency joins the two endpoints.",
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
    carrier="Cell positions carrying foreground or background values.",
    support="A one-dimensional line with a finite foreground and unbounded background.",
    topology="Integer-ordered linear positions with an aligned repeating background.",
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
    carrier="Cells grouped into finite blocks with explicit coordinate offsets.",
    support="A cellular coordinate array with a declared background.",
    topology="The coordinate topology implied by the supplied offset vectors.",
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
    carrier="Cells in a d-dimensional finite value array.",
    support="A d-dimensional cellular array embedded in declared padding/background.",
    topology="The d-dimensional rectangular coordinate topology of the array.",
    result="A d-dimensional initial cellular configuration.",
)
for key in {"background-seed", "offset-block-seed", "dd-padded-seed"}:
    seed_spec = next(
        item for item in ALL_CANDIDATE_SPECS if item["key"] == key
    )
    add_evidence(
        seed_spec,
        label=f"{key}-alignment",
        unit="U005022",
        claim=(
            "The source fixes the origin-relative alignment of the finite "
            "foreground array and its background/padding array."
        ),
        fields=[
            "topology",
            "complete_state",
            "input",
            "seed",
            "boundary",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
        strength="CORROBORATING",
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
        "input": "The explicit list {1,0,0,1,0}.",
        "law_kind": "A deterministic cyclic initial-state constructor.",
        "rule_relation_constraint_function_or_probability_law": (
            "Use the supplied five values in their stated order and close the "
            "finite row cyclically."
        ),
        "write_replacement_assembly_or_commit": (
            "Assemble the five ordered values into one cyclic initial configuration."
        ),
        "result_kind": "The finite cyclic initial configuration {1,0,0,1,0}.",
        "successor_cardinality": "Exactly one constructed seed for this preset.",
        "determinism_branching_or_measure": "Deterministic constructor.",
        "parameters_and_variants": "The fixed five values and cyclic continuation.",
        "excluded_observers_and_representations": (
            "Rule 30, the requested three-step run, and its printed four rows "
            "demonstrate the seed but are not part of this constructor."
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
explicit_cyclic_seed["source_status"] = ["DEFECTIVE", "AMBIGUOUS"]
explicit_cyclic_seed["uncertainties"] = [
    (
        "U005043 contains the damaged sentence “The runs rule 30 with 5 cells "
        "for 3 steps”; U005044 resolves the omitted call subject and exact "
        "example without repairing the source prose."
    )
]
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
        "input": "Foreground {1,1} and repeating background block {1,0,1,1}.",
        "law_kind": "A deterministic foreground/background seed constructor.",
        "rule_relation_constraint_function_or_probability_law": (
            "Superimpose the foreground {1,1} on an infinite repetition of "
            "the background block {1,0,1,1}."
        ),
        "write_replacement_assembly_or_commit": (
            "Overlay the finite foreground on the aligned repeating background."
        ),
        "result_kind": "The constructed infinite patterned initial configuration.",
        "successor_cardinality": "Exactly one constructed seed for this preset.",
        "determinism_branching_or_measure": "Deterministic constructor.",
        "parameters_and_variants": (
            "The fixed foreground block and repeating background block."
        ),
        "excluded_observers_and_representations": (
            "Rule 30, its 50-step run, and the affected-region/all-region crop "
            "are downstream evolution and observer choices."
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
        "input": (
            "Block {1} at offset -10, block {1,1} at offset 20, and background 0."
        ),
        "law_kind": "A deterministic positioned-block seed constructor.",
        "rule_relation_constraint_function_or_probability_law": (
            "Place {1} at offset -10 and {1,1} at offset 20 on the zero background."
        ),
        "write_replacement_assembly_or_commit": (
            "Overlay both positioned finite blocks on the unbounded zero background."
        ),
        "result_kind": "The constructed positioned-block initial configuration.",
        "successor_cardinality": "Exactly one constructed seed for this preset.",
        "determinism_branching_or_measure": "Deterministic constructor.",
        "parameters_and_variants": (
            "Foreground values, offsets -10 and 20, and zero background."
        ),
        "excluded_observers_and_representations": (
            "Rule 30, the 50-step request, and the raster are downstream "
            "evolution or representation choices."
        ),
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
    spec = source_candidate(
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
    # The prose anchor names the preset/profile but the following CODE unit
    # carries the full seed, run, and output-window mechanics.  Keep the two
    # evidence claims exact rather than making the prose inherit the call.
    spec["evidence"][0]["fields"] = [
        "object_kind",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    return spec


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


def direct_query_candidate(
    *,
    key: str,
    name: str,
    anchor: str,
    object_kind: str,
    input_text: str,
    law: str,
    result: str,
    parameters_text: str,
    aliases: list[str] | None = None,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    missing = (
        "The assigned passage does not state invalid-input behavior or an "
        "independent witness/certificate convention."
    )
    return source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts={
            "object_kind": object_kind,
            "complete_state": (
                "The complete supplied input together with the requested query selector."
            ),
            "input": input_text,
            "law_kind": "A direct deterministic query/projection.",
            "rule_relation_constraint_function_or_probability_law": law,
            "result_kind": result,
            "successor_cardinality": "Exactly one query result for each valid input.",
            "determinism_branching_or_measure": "Deterministic.",
            "parameters_and_variants": parameters_text,
            "excluded_observers_and_representations": (
                "Formatting, rasterization, and later interpretation of the "
                "query result are representations or observations."
            ),
            "evidence_limit": missing,
        },
        claim=f"The source directly defines {name}: {law}",
        missing=missing,
        modality="FORMULA",
        parameters=[
            (
                "query selector",
                parameters_text,
                [f"{key}-source"],
            )
        ],
        route_keys=route_keys,
    )


time_slice_query = direct_query_candidate(
    key="ca-time-slice-query",
    name="cellular-automaton evolution time-slice selector",
    anchor="U005024",
    object_kind="A direct projection over a requested cellular-automaton evolution.",
    input_text="A cellular-automaton evolution through step t and a time-offset selector.",
    law=(
        "Select all steps 0..t, steps 0..u, only the last step, one named step, "
        "an inclusive step range, or a stepped range according to the exact "
        "All/u/-1/{u}/{u1,u2}/{u1,u2,du} selector forms."
    ),
    result="The uniquely selected row or ordered list of evolution rows.",
    parameters_text="The selector form and its step bounds/stride.",
    aliases=["CellularAutomaton time offset off_t"],
)
add_evidence(
    time_slice_query,
    label="ca-time-slice-history-length",
    unit="U005025",
    claim=(
        "The source states that an unprojected t-step evolution contains t+1 "
        "rows, including the initial condition."
    ),
    fields=[
        "complete_state",
        "input",
        "result_kind",
        "parameters_and_variants",
        "evidence_limit",
    ],
)
add_evidence(
    time_slice_query,
    label="ca-time-slice-last-example",
    unit="U005054",
    claim="The example explicitly requests only the last row after ten steps.",
    fields=[
        "input",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)
add_evidence(
    time_slice_query,
    label="ca-time-slice-stride-example",
    unit="U005058",
    claim=(
        "The example describes selecting every other step as part of a joint "
        "space/time projection."
    ),
    fields=[
        "input",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
)

space_slice_query = direct_query_candidate(
    key="ca-space-slice-query",
    name="cellular-automaton evolution spatial-slice selector",
    anchor="U005028",
    object_kind="A direct spatial projection over a cellular-automaton evolution.",
    input_text="A cellular-automaton evolution and a space-offset selector.",
    law=(
        "Select the affected support, the region differing from background, "
        "the origin-aligned cell, a one-sided extent, one offset, an inclusive "
        "offset range, or a stepped range according to the exact documented forms."
    ),
    result="The uniquely selected fixed-width spatial slice at every retained step.",
    parameters_text="The selector mode, spatial bounds, and optional stride.",
    aliases=["CellularAutomaton space offset off_x"],
)
for label, unit, claim, fields in [
    (
        "ca-space-slice-origin",
        "U005026",
        "The source fixes offset 0 as the initial-condition alignment origin.",
        ["input", "rule_relation_constraint_function_or_probability_law",
         "parameters_and_variants", "evidence_limit"],
    ),
    (
        "ca-space-slice-fixed-width",
        "U005031",
        "Every row returned by one evolution projection has the same size.",
        ["result_kind", "evidence_limit"],
    ),
    (
        "ca-space-slice-affected-width",
        "U005032",
        "The source gives the exact affected-support width w + 2 r t.",
        ["input", "rule_relation_constraint_function_or_probability_law",
         "result_kind", "parameters_and_variants", "evidence_limit"],
    ),
    (
        "ca-space-slice-all-no-background",
        "U005033",
        "The source fixes how All and Automatic include the explicit seed when no background is supplied.",
        ["rule_relation_constraint_function_or_probability_law",
         "parameters_and_variants", "evidence_limit"],
    ),
    (
        "ca-space-slice-all",
        "U005034",
        "All selects every cell that can be affected by the initial condition.",
        ["rule_relation_constraint_function_or_probability_law",
         "result_kind", "parameters_and_variants", "evidence_limit"],
    ),
    (
        "ca-space-slice-automatic",
        "U005035",
        "Automatic trims background cells from the sides of the pattern.",
        ["rule_relation_constraint_function_or_probability_law",
         "result_kind", "parameters_and_variants",
         "excluded_observers_and_representations", "evidence_limit"],
    ),
    (
        "ca-space-slice-time-coupling",
        "U005036",
        "Automatic computes retained width using only the requested time steps.",
        ["input", "rule_relation_constraint_function_or_probability_law",
         "parameters_and_variants", "evidence_limit"],
    ),
    (
        "ca-space-slice-all-example",
        "U005048",
        "The example distinguishes All as every possibly affected cell.",
        ["rule_relation_constraint_function_or_probability_law",
         "result_kind", "parameters_and_variants",
         "excluded_observers_and_representations", "evidence_limit"],
    ),
    (
        "ca-space-slice-center-example",
        "U005056",
        "The example requests the three center columns at every retained step.",
        ["input", "rule_relation_constraint_function_or_probability_law",
         "result_kind", "parameters_and_variants",
         "excluded_observers_and_representations", "evidence_limit"],
    ),
    (
        "ca-space-slice-stride-example",
        "U005058",
        "The example selects every other cell across an explicit spatial range.",
        ["input", "rule_relation_constraint_function_or_probability_law",
         "result_kind", "parameters_and_variants",
         "excluded_observers_and_representations", "evidence_limit"],
    ),
]:
    add_evidence(
        space_slice_query,
        label=label,
        unit=unit,
        claim=claim,
        fields=fields,
        modality="FORMULA" if unit in {"U005032"} else "PROSE",
    )


symbolic_ca_formula = source_candidate(
    key="symbolic-ca-formula-generator",
    name="symbolic cellular-automaton cell-formula generator",
    anchor="U005107",
    aliases=["symbolic CA evolution formula"],
    facts={
        "object_kind": (
            "A symbolic analyzer that derives formulas for cellular-automaton "
            "cell values from a stated rule and symbolic initial values."
        ),
        "carrier": "Symbolic cell variables indexed by time and position.",
        "support": "The dependency cone of the requested cellular-automaton cell.",
        "complete_state": (
            "The algebraic or logical rule, symbolic initial assignments, and "
            "the target cell/time whose value is requested."
        ),
        "input": (
            "An algebraic or logical cellular-automaton rule plus symbolic and "
            "fixed initial-cell assignments."
        ),
        "law_kind": "Symbolic composition of a cellular-automaton transition law.",
        "rule_relation_constraint_function_or_probability_law": (
            "Substitute the symbolic initial assignments through the stated "
            "cellular-automaton rule to derive a formula for a requested cell value."
        ),
        "result_kind": "A symbolic formula valid for all values of the declared variables.",
        "parameters_and_variants": (
            "Rule form, symbolic initial variables, fixed background values, "
            "and requested cell/time."
        ),
        "excluded_observers_and_representations": (
            "Formula simplification, printed syntax, and complexity growth are "
            "analyzer/representation concerns rather than a second CA law."
        ),
        "evidence_limit": (
            "The passage establishes the construction in principle but gives "
            "no canonical simplifier, exact target-selection interface, "
            "invalid-input behavior, or complexity bound."
        ),
    },
    claim=(
        "The source explicitly states that algebraic or logical CA rules can "
        "be composed to generate symbolic formulas for evolution results."
    ),
    missing=(
        "The passage establishes the construction in principle but gives no "
        "canonical simplifier, exact target-selection interface, invalid-input "
        "behavior, or complexity bound."
    ),
    route_keys=["symbolic-ca-formula-page618"],
    parameters=[
        (
            "symbolic initial assignment",
            "The worked profile names three symbolic center cells and fixes all "
            "other initial cells to zero.",
            ["symbolic-ca-formula-initial-values"],
        )
    ],
)
add_evidence(
    symbolic_ca_formula,
    label="symbolic-ca-formula-initial-values",
    unit="U005108",
    claim=(
        "The code assigns p, q, and r to the three center cells and zero to all "
        "other positions at time zero."
    ),
    fields=[
        "carrier",
        "support",
        "complete_state",
        "input",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    modality="CODE",
)
add_evidence(
    symbolic_ca_formula,
    label="symbolic-ca-formula-result",
    unit="U005109",
    claim=(
        "The source states that the construction yields a cell-value formula "
        "valid for every choice of the three symbolic center values."
    ),
    fields=[
        "object_kind",
        "input",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
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
    route_keys=["pascal-page611", "pascal-polynomial-page1091"],
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
pascal_mod2["facts"]["structural_invariants"] = (
    "The odd-coefficient array has a nested self-similar Sierpiński structure."
)
add_evidence(
    pascal_mod2,
    label="pascal-mod2-sierpinski-structure",
    unit="U005119",
    claim=(
        "The source identifies the Rule 90/Pascal parity pattern as a "
        "self-similar Sierpiński pattern and gives its exact decimation relation."
    ),
    fields=[
        "structural_invariants",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CORROBORATING",
)
add_evidence(
    pascal_mod2,
    label="pascal-mod2-history-nesting",
    unit="U005129",
    claim=(
        "The historical note explicitly states that odd binomial coefficients "
        "form a nested geometrical pattern and preserves that as property evidence."
    ),
    fields=[
        "structural_invariants",
        "result_kind",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
)

rule90_row_count = direct_query_candidate(
    key="rule90-row-black-count",
    name="Rule 90 row black-cell count function",
    anchor="U005114",
    object_kind="A direct integer-valued query on the canonical Rule 90 single-seed pattern.",
    input_text="A nonnegative Rule 90 row index t.",
    law="Return 2^DigitCount[t,2,1].",
    result="The number of black cells on row t.",
    parameters_text="The row index t; Rule 90 and base 2 are fixed.",
    aliases=["Rule 90 row population"],
    route_keys=["rule90-count-page902"],
)

rule90_black_positions = direct_query_candidate(
    key="rule90-row-black-positions",
    name="Rule 90 row black-cell position generator",
    anchor="U005114",
    object_kind="A direct list-valued query on the canonical Rule 90 single-seed pattern.",
    input_text="A nonnegative Rule 90 row index t.",
    law=(
        "Compute the 1-bit positions of t, then fold from 0 by replacing each "
        "current position x with x-2^j and x+2^j for every such digit position j."
    ),
    result="The complete list of black-cell positions on row t.",
    parameters_text="The row index t; Rule 90 and base 2 are fixed.",
    aliases=["Rule 90 black positions"],
    route_keys=["rule90-position-page117"],
)
add_evidence(
    rule90_black_positions,
    label="rule90-row-black-positions-code",
    unit="U005115",
    claim=(
        "The exact Fold and DigitPositions definitions construct all black-cell "
        "positions from the 1-bit positions of t."
    ),
    fields=list(rule90_black_positions["facts"]),
    modality="FORMULA",
    strength="DIRECT_COMPLETE_MECHANICS",
)

rule60_pattern = declarative_pattern(
    key="rule60-pattern",
    name="binomial-modulo-two array identified with the Rule 60 single-seed pattern",
    anchor="U005117",
    definition=(
        "The static array value at row t and position n is "
        "Mod[Binomial[t,n],2], identified as the single-seed pattern of rule 60."
    ),
    support="Nonnegative integer row and position coordinates.",
    values="Binary parity values.",
    result="A uniquely determined distorted nested binary pattern.",
    aliases=["Rule 60 binomial pattern"],
    route_keys=["rule60-bit-page583"],
)
add_evidence(
    rule60_pattern,
    label="rule60-pattern-bit-test",
    unit="U005118",
    claim=(
        "The exact digitwise formula returns 1 precisely when no aligned binary "
        "digit of n exceeds the corresponding digit of t."
    ),
    fields=[
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "complete_state",
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
    modality="FORMULA",
    strength="DIRECT_COMPLETE_MECHANICS",
)

rule60_ca = source_candidate(
    key="rule60-ca",
    name="Rule 60 cellular automaton preset",
    anchor="U005117",
    aliases=["cellular automaton rule 60"],
    facts={
        "object_kind": "A named one-dimensional binary cellular-automaton preset.",
        "native_time": "Discrete cellular-automaton generations.",
        "carrier": "Cells in a one-dimensional row.",
        "support": "A one-dimensional cellular space.",
        "alphabet_or_value_schema": "Two cell values represented by parity 0 and 1.",
        "complete_state": "One binary value at every cell position.",
        "seed": (
            "The co-referenced canonical pattern is the single-seed evolution "
            "represented by Mod[Binomial[t,n],2]."
        ),
        "frontier_or_activation": "The named elementary rule applies across the row.",
        "read_dependencies_or_neighborhood": (
            "An elementary left/self/right neighborhood is implied by the rule number."
        ),
        "law_kind": "A deterministic elementary cellular-automaton lookup rule.",
        "result_kind": "A uniquely determined evolution once the Rule 60 lookup is supplied.",
        "parameters_and_variants": "The source fixes elementary rule number 60.",
        "excluded_observers_and_representations": (
            "The binomial formula is a direct denotation of one canonical "
            "evolution, not the complete native transition relation."
        ),
        "evidence_limit": (
            "This passage does not expand the Rule 60 lookup table, state a "
            "boundary convention, or define arbitrary-seed evolution."
        ),
    },
    claim=(
        "The source explicitly identifies the displayed binomial-modulo-two "
        "array as the pattern produced by cellular automaton Rule 60."
    ),
    missing=(
        "This passage does not expand the Rule 60 lookup table, state a "
        "boundary convention, or define arbitrary-seed evolution."
    ),
    strength="DIRECT_IDENTITY",
    modality="FORMULA",
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
        "input": (
            "A single black foreground cell and the pictured repeating striped "
            "background block."
        ),
        "seed": (
            "A single black cell inserted into a background of repetitions of "
            "the pictured striped black-to-white block."
        ),
        "boundary": "The background repeats outside the finite foreground.",
        "law_kind": "A deterministic foreground/background seed constructor.",
        "rule_relation_constraint_function_or_probability_law": (
            "Insert the single black foreground cell into an unbounded repetition "
            "of the pictured striped background block."
        ),
        "write_replacement_assembly_or_commit": (
            "Overlay the foreground cell on the aligned repeating background."
        ),
        "result_kind": "The constructed patterned initial configuration.",
        "successor_cardinality": (
            "Exactly one constructed seed for a fixed foreground and background block."
        ),
        "determinism_branching_or_measure": "Deterministic constructor.",
        "parameters_and_variants": (
            "The single-cell foreground and pictured repeated background block."
        ),
        "excluded_observers_and_representations": (
            "Rule 90 evolution, its white/striped nested regions, fractal "
            "dimensions, and the raster are downstream outcomes or representations."
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
rule90_background["source_status"] = ["AMBIGUOUS"]
rule90_background["uncertainties"] = [
    (
        "The inline striped background symbol is construction-bearing but its "
        "individual binary cells and exact repeated value sequence cannot be "
        "recovered unambiguously at source resolution."
    )
]
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
add_evidence(
    k_rule90,
    label="k-color-rule90-count-relation",
    unit="U005125",
    claim=(
        "The source gives a closed row-population formula and explains "
        "non-prime patterns as superpositions of factor patterns; these are "
        "properties/relations, not extra transition mechanics."
    ),
    fields=[
        "object_kind",
        "alphabet_or_value_schema",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CORROBORATING",
    modality="FORMULA",
)
add_evidence(
    k_rule90,
    label="k-color-rule90-nesting",
    unit="U005127",
    claim=(
        "The source states that all k-color patterns are nested and gives "
        "prime-k counts and dimensions as behavior/property evidence."
    ),
    fields=[
        "object_kind",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="CONTEXTUAL",
)

k_rule90_row_count = direct_query_candidate(
    key="k-color-rule90-row-count",
    name="k-color Rule 90 row nonwhite-cell count function",
    anchor="U005125",
    object_kind=(
        "A direct integer-valued query on the canonical k-color additive "
        "Rule 90 single-seed pattern."
    ),
    input_text="A nonnegative row index t and color modulus k.",
    law="Return Apply[Times, 1 + IntegerDigits[t,k]].",
    result="The number of nonwhite cells on row t.",
    parameters_text="The row index t and color modulus k.",
    aliases=["k-color additive row population"],
)

binomial_k_exponent = direct_query_candidate(
    key="binomial-k-exponent-borrow-count",
    name="Binomial k-exponent borrow-count function",
    anchor="U005125",
    object_kind="A direct integer-valued arithmetic query.",
    input_text="Nonnegative integers t and n together with the base/factor k.",
    law=(
        "Return the number of borrows in the base-k subtraction of n from t; "
        "the source identifies this with IntegerExponent[Binomial[t,n],k]."
    ),
    result="The k-exponent of Binomial[t,n].",
    parameters_text="The integers t and n and the base/factor k.",
    aliases=["binomial valuation by base-k borrows"],
)

binomial_mod_k = declarative_pattern(
    key="binomial-mod-k-prime",
    name="prime-k Binomial modulo-k array",
    anchor="U005125",
    definition=(
        "For prime k, evaluate Mod[Binomial[t,n],k] by multiplying the "
        "digitwise binomial coefficients of the base-k digits of t and n, "
        "then reducing the product modulo k."
    ),
    support="Nonnegative integer row and position coordinates (t,n).",
    values="Residues modulo a prime k.",
    result="A uniquely determined k-valued binomial-coefficient array.",
    aliases=["Lucas digit formula for Binomial modulo k"],
)
add_evidence(
    binomial_mod_k,
    label="binomial-mod-k-code",
    unit="U005126",
    claim=(
        "The exact formula pads the base-k digits, applies Binomial to each "
        "digit pair, multiplies the results, and reduces modulo k."
    ),
    fields=list(binomial_mod_k["facts"]),
    modality="FORMULA",
    strength="DIRECT_COMPLETE_MECHANICS",
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


binomial_mod2_array = pictured_integer_pattern(
    key="binomial-mod2-array",
    name="Binomial modulo-two array",
    unit="U005130",
    path="BACK-MATTER/NOTES/_page_885_Picture_23.jpeg",
    definition="Reduce Binomial's integer values modulo 2 over its argument lattice.",
    support="A two-dimensional integer-coordinate array.",
)
multinomial_mod2_array = pictured_integer_pattern(
    key="multinomial-mod2-array",
    name="Multinomial modulo-two array family",
    unit="U005131",
    path="BACK-MATTER/NOTES/_page_885_Picture_24.jpeg",
    definition=(
        "Reduce a d-argument Multinomial value modulo 2 at each integer tuple."
    ),
    support="A d-dimensional integer-coordinate array.",
)
stirling1_mod2_array = pictured_integer_pattern(
    key="stirling1-mod2-array",
    name="StirlingS1 modulo-two array",
    unit="U005132",
    path="BACK-MATTER/NOTES/_page_885_Picture_25.jpeg",
    definition="Reduce StirlingS1's integer values modulo 2 over its argument lattice.",
    support="A two-dimensional integer-coordinate array.",
)
stirling2_mod2_array = pictured_integer_pattern(
    key="stirling2-mod2-array",
    name="StirlingS2 modulo-two array",
    unit="U005133",
    path="BACK-MATTER/NOTES/_page_885_Picture_26.jpeg",
    definition="Reduce StirlingS2's integer values modulo 2 over its argument lattice.",
    support="A two-dimensional integer-coordinate array.",
)
multinomial_mod2_array["facts"]["structural_invariants"] = (
    "With d arguments the modulo-two Multinomial array is nested in d dimensions."
)
add_evidence(
    multinomial_mod2_array,
    label="multinomial-mod2-dimensional-nesting",
    unit="U005134",
    claim=(
        "The source explicitly states that d-argument Multinomial yields a "
        "nested pattern in d dimensions."
    ),
    fields=[
        "support",
        "structural_invariants",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
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
    spec["facts"]["structural_invariants"] = (
        "The curve has the source-stated nested structure induced by comparing "
        "the digits of n with the one-position-left shift 2n."
    )
    add_evidence(
        spec,
        label=f"{key}-nesting",
        unit="U005139",
        claim=(
            "The source explicitly states that these curves are nested and "
            "relates the structure to the one-digit shift from n to 2n."
        ),
        fields=[
            "support",
            "structural_invariants",
            "input",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
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
        "support": "The first n positions of the center-column output sequence.",
        "topology": "A linearly ordered sequence indexed by generation.",
        "structural_invariants": "Exactly one binary center value is retained per generation.",
        "alphabet_or_value_schema": "Binary black/white values.",
        "complete_state": (
            "For input n, the complete denotation is the ordered prefix of n "
            "center-column symbols."
        ),
        "visible_history": (
            "The returned sequence preserves the center value from each "
            "successive Rule 30 generation."
        ),
        "input": "A requested prefix length n.",
        "law_kind": "Project the Rule 30 history to its center cell at each step.",
        "rule_relation_constraint_function_or_probability_law": (
            "Return the first n center-column values of the single-seed Rule 30 run."
        ),
        "result_kind": "A finite binary sequence prefix.",
        "successor_cardinality": (
            "Exactly one n-symbol prefix is returned for each valid requested length."
        ),
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

rule102 = source_candidate(
    key="rule102",
    name="Rule 102 cellular automaton preset",
    anchor="U005149",
    aliases=["reflection of rule 60"],
    facts={
        "object_kind": "A named one-dimensional binary cellular-automaton preset.",
        "native_time": "Discrete elementary cellular-automaton generations.",
        "carrier": "Cells in a one-dimensional row.",
        "support": "A one-dimensional cellular space.",
        "topology": "An elementary left/self/right neighborhood.",
        "alphabet_or_value_schema": "Two cell values.",
        "complete_state": "One binary value at every cell position.",
        "frontier_or_activation": "The elementary rule applies across the row.",
        "read_dependencies_or_neighborhood": "Left neighbor, self, and right neighbor.",
        "law_kind": "A deterministic elementary cellular-automaton lookup rule.",
        "rule_relation_constraint_function_or_probability_law": (
            "Rule 102 is the spatial reflection of Rule 60; exactly one of its "
            "eight lookup outputs differs from Rule 110."
        ),
        "result_kind": "A unique successor once the eight-case lookup is expanded.",
        "parameters_and_variants": "Elementary rule number 102.",
        "excluded_observers_and_representations": (
            "The comparison with Rule 110 and reflection description are "
            "identity-bearing relations, not a displayed evolution."
        ),
        "evidence_limit": (
            "The passage does not print Rule 102's eight outputs, state a seed "
            "or boundary, or define completion and witness semantics."
        ),
    },
    claim=(
        "The Rule 110 note separately identifies elementary Rule 102 as the "
        "reflection of Rule 60 and distinguishes its eight-case lookup from "
        "Rule 110 in exactly one case."
    ),
    missing=(
        "The passage does not print Rule 102's eight outputs, state a seed or "
        "boundary, or define completion and witness semantics."
    ),
    strength="DIRECT_PARTIAL_MECHANICS",
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
            "law_kind": "A drawing, deformation, or assembly procedure.",
            "rule_relation_constraint_function_or_probability_law": description,
            "write_replacement_assembly_or_commit": description,
            "result_kind": result,
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
                "Original-resolution inspection confirms this source-associated "
                "construction figure; only visibly unambiguous geometry, "
                "grouping, or result structure is used, with no hidden temporal "
                "order inferred from image proximity."
            ),
            fields=[
                "carrier",
                "support",
                "complete_state",
                "result_kind",
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
        "Apply the source-ordered four-stage square drawing procedure; the "
        "source also shows a rounded-form output variant."
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
pylos["uncertainties"] = [
    (
        "The source says the historical tablet pattern was “presumably made” "
        "by the depicted procedure; the diagrams support the procedure, not "
        "certainty about the artifact's actual production history."
    )
]
pylos["evidence"][0]["claim"] = (
    "The source presents a four-stage square procedure plus a rounded-form "
    "variant for the Pylos labyrinth while "
    "explicitly qualifying its attribution to the historical tablet as presumed."
)
attach_procedure_images(
    pylos,
    label_prefix="pylos-stage",
    entries=[
        ("U005173", "BACK-MATTER/NOTES/_page_888_Picture_5.jpeg"),
        ("U005174", "BACK-MATTER/NOTES/_page_888_Picture_6.jpeg"),
        ("U005175", "BACK-MATTER/NOTES/_page_888_Picture_7.jpeg"),
        ("U005176", "BACK-MATTER/NOTES/_page_888_Picture_8.jpeg"),
    ],
)
add_candidate_image(
    pylos,
    label="pylos-rounded-variant",
    unit="U005177",
    path="BACK-MATTER/NOTES/_page_888_Picture_9.jpeg",
    claim=(
        "Original-resolution inspection confirms a rounded-form completed "
        "labyrinth variant, not a fifth successor stage in the square sequence."
    ),
    fields=[
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
pylos["variants"].append(
    (
        "rounded completed form",
        "The final separate image supplies a rounded-form output variant of "
        "the labyrinth.",
        ["pylos-rounded-variant"],
    )
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
roman_rosette["uncertainties"] = [
    (
        "The source says the Roman mosaic was “presumably made” by the stated "
        "construction; the procedure is retained without converting that "
        "historical attribution into a fact."
    )
]
roman_rosette["evidence"][0]["claim"] = (
    "The source states the spoke, semicircle, and concentric-circle construction "
    "while qualifying its attribution to the Roman mosaic as presumed."
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
cosmati["uncertainties"] = [
    (
        "The source says the approximate nested structure was “presumably "
        "created” as in the diagrams; the construction is retained while its "
        "historical attribution remains conjectural."
    )
]
cosmati["evidence"][0]["claim"] = (
    "The source relates the approximate nested equilateral-triangle structure "
    "to the following diagrams while explicitly marking that creation account "
    "as presumed."
)
attach_procedure_images(
    cosmati,
    label_prefix="cosmati-stage",
    entries=[
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
        "object_kind": "A denotational finite-alphabet planar pattern space.",
        "carrier": "Square tile positions.",
        "support": "A two-dimensional square grid.",
        "topology": "Orthogonally adjacent square tile sites.",
        "structural_invariants": "Every site is occupied by one congruent square tile.",
        "alphabet_or_value_schema": (
            "Four square tiles distinguished by which triangular half is filled: "
            "◣, ◥, ◤, or ◢."
        ),
        "complete_state": "One choice of the four tile values at every grid site.",
        "input": "A requested finite square-grid domain.",
        "law_kind": "A model set/free-combination relation over a four-tile alphabet.",
        "rule_relation_constraint_function_or_probability_law": (
            "The denoted set contains the square-grid assignments formed by "
            "combining the four stated tile values at the sites."
        ),
        "result_kind": "The set of completed planar tile assignments on the domain.",
        "witness_semantics": (
            "A witness is a completed square-grid assignment with exactly one "
            "of the four stated tile values at every site."
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

random_ca_seed = source_candidate(
    key="random-ca-initial-condition",
    name="random cellular-automaton initial-condition ensemble",
    anchor="U005288",
    aliases=["random initial conditions"],
    facts={
        "object_kind": (
            "A stochastic/ensemble-valued cellular-automaton initial-condition class."
        ),
        "complete_state": "One sampled complete cellular-automaton configuration.",
        "input": (
            "A cellular-automaton family together with an unstated random "
            "initial-condition sampling specification."
        ),
        "seed": "A random initial configuration used to start a cellular automaton.",
        "law_kind": (
            "A probability/sampling law for initial configurations, with its "
            "actual measure left unstated in this passage."
        ),
        "rule_relation_constraint_function_or_probability_law": (
            "Sample an initial configuration at random, then use it as the "
            "cellular automaton's initial state."
        ),
        "result_kind": "A sampled cellular-automaton initial configuration.",
        "determinism_branching_or_measure": (
            "Stochastic or ensemble-valued; the probability measure is not stated."
        ),
        "parameters_and_variants": (
            "The cellular-automaton family, support/alphabet, and sampling "
            "distribution are parameters whose values are not given here."
        ),
        "excluded_observers_and_representations": (
            "The four behavior classes inferred from displayed runs are "
            "observations, not part of the seed generator."
        ),
        "evidence_limit": (
            "The historical passage explicitly says random initial conditions "
            "but does not state their support, alphabet, independence structure, "
            "probability measure, finite extent, or random source."
        ),
    },
    claim=(
        "The historical account explicitly distinguishes cellular automata "
        "started from random initial conditions in the systematic survey."
    ),
    missing=(
        "The historical passage explicitly says random initial conditions but "
        "does not state their support, alphabet, independence structure, "
        "probability measure, finite extent, or random source."
    ),
    strength="DIRECT_IDENTITY",
    parameters=[
        (
            "sampling specification",
            "The source establishes that initial conditions were random while "
            "leaving the measure and support unspecified.",
            ["random-ca-initial-condition-source"],
        )
    ],
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
    key="main-primes-page132",
    unit="U000293",
    literal="the distribution of prime numbers (see page 132)",
    topic="prime-number generation and distribution",
    vocabulary=["prime numbers", "generating primes", "page 132"],
)
add_route(
    key="main-pi-page136",
    unit="U000294",
    literal="digit sequence of a number like pi ... (see page 136)",
    topic="digit-sequence construction for pi",
    vocabulary=["digits of pi", "simple rules", "page 136"],
)
add_route(
    key="main-iterated-maps-page149",
    unit="U000297",
    literal="iterated maps ... discuss on page 149",
    topic="iterated-map native mechanics",
    vocabulary=["iterated maps", "complexity", "page 149"],
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
    key="symbolic-ca-formula-page618",
    unit="U005109",
    literal="such formulas rapidly become very complicated, as discussed on page 618",
    topic="symbolic closed formulas for cellular-automaton cell values",
    vocabulary=["formula", "cell value", "cellular automaton"],
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
    key="rule90-count-page902",
    unit="U005114",
    literal="DigitCount[t, 2, 1] is plotted on page 902",
    topic="Rule 90 black-cell count function",
    vocabulary=["rule 90", "DigitCount", "black cells"],
)
add_route(
    key="rule90-position-page117",
    unit="U005114",
    literal="the connection with the picture on page 117",
    topic="Rule 90 black-cell position construction",
    vocabulary=["rule 90", "positions", "page 117"],
)
add_route(
    key="pascal-polynomial-page1091",
    unit="U005116",
    literal="PolynomialMod[Expand[(1/x + x)^t], 2] (see page 1091)",
    topic="polynomial construction of the Rule 90/Pascal parity array",
    vocabulary=["PolynomialMod", "rule 90", "binomial coefficients"],
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
    key="k-color-count-dimension-page955",
    unit="U005127",
    literal="For prime k ... fractal dimension ... (see page 955).",
    topic="prime-k additive cellular-automaton counts and fractal dimensions",
    vocabulary=["prime k", "non-white cells", "fractal dimension", "page 955"],
)
add_route(
    key="rule90-dimension-page933",
    unit="U005119",
    literal="fractal dimension ... (see page 933)",
    topic="fractal-dimension definition applied to Rule 90",
    vocabulary=["rule 90", "fractal dimension", "page 933"],
)
add_route(
    key="rule90-sierpinski-page934",
    unit="U005119",
    literal="a Sierpinski pattern (see page 934)",
    topic="Sierpinski-pattern construction and Rule 90 correspondence",
    vocabulary=["Sierpinski pattern", "rule 90", "page 934"],
)
add_route(
    key="rule90-additive-page955",
    unit="U005119",
    literal="additive rules (see page 955)",
    topic="additive-rule nesting property and construction class",
    vocabulary=["additive rules", "nesting", "page 955"],
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
    key="rule30-boundary-page949",
    unit="U005142",
    literal="compare page 949",
    topic="Rule 30 regular/random-region boundary motion",
    vocabulary=["rule 30", "boundary", "average motion"],
)
add_route(
    key="rule30-randomness-tests-page1084",
    unit="U005141",
    literal="the eight listed on page 1084",
    topic="eight statistical tests applied to Rule 30 randomness",
    vocabulary=["tests of randomness", "statistical tests", "rule 30", "page 1084"],
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
    key="design-weaving-page929",
    unit="U005166",
    literal="See also page 929.",
    topic="rule-based design and weaving construction boundary",
    vocabulary=["design", "weaving patterns", "cellular automata"],
)
add_route(
    key="design-rule-selection-page929",
    unit="U005168",
    literal="(Compare page 929.)",
    topic="rule-selection and evaluation methods for generated designs",
    vocabulary=["rules", "design", "selection", "page 929"],
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
add_route(
    key="historical-additive-page870",
    unit="U005238",
    literal="binomial coefficient modulo primes ... (see page 870)",
    topic="additive cellular automata and binomial-coefficient parity",
    vocabulary=["additive cellular automata", "binomial coefficient", "rule 90"],
    scope="WITHIN_STAGE",
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
    ("random-initial-page112", "U005286", "See page 112.", "random-initial-condition versus intrinsic-randomness evidence", ["random initial conditions", "rule 30", "page 112"], "CROSS_RANGE"),
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


# ---------------------------------------------------------------------------
# Deterministic worker-local allocation and complete row/asset authoring.

SEED_KEYS = {
    "centered-single-seed",
    "cyclic-explicit-seed",
    "background-seed",
    "offset-block-seed",
    "dd-padded-seed",
    "explicit-cyclic-seed",
    "periodic-patch-seed",
    "positioned-patch-preset",
    "rule90-background-seed",
    "random-ca-initial-condition",
}
HISTORICAL_CANDIDATE_KEYS = {
    "pylos-labyrinth",
    "triangular-circle-array",
    "celtic-touching-circles",
    "roman-rosette",
    "cosmati-triangles",
    "triangle-grid-push",
    "nested-rope",
    "truchet-pattern-space",
    "game-of-life",
    "von-neumann-29color-ca",
    "ulam-recursive-2d-ca",
    "fredkin-2d-rule90",
    "code20",
    "linear-feedback-shift-register",
    "shift-commuting-block-map",
}
RELATION_IMAGE_UNITS = {
    "U000264",
    "U005200",
    "U005201",
    "U005202",
}
CONTROL_IMAGE_UNITS = {"U005240"}

UNKNOWN_FACT_LABELS = {
    "object_kind": "a more specific native object kind",
    "native_time": "whether the object has native time or iteration, and its time domain",
    "carrier": "what entities carry the native state or values",
    "support": "the native domain/support and its extent",
    "topology": "the native adjacency, incidence, or domain topology",
    "structural_invariants": "which structural facts must remain invariant",
    "alphabet_or_value_schema": "the complete native value/alphabet schema",
    "complete_state": "what information constitutes one complete native state or denotation",
    "visible_history": "whether a history is native and, if so, what it retains",
    "control_state": "whether separate native control state exists and what it contains",
    "seed": "a native seed or initial-state convention",
    "input": "the complete native input contract",
    "boundary": "the native boundary convention",
    "external_data": "whether native evaluation consumes external data",
    "frontier_or_activation": "which components are active or eligible at a step",
    "schedule": "the native evaluation/update schedule",
    "read_dependencies_or_neighborhood": "the complete native read-dependency relation",
    "law_kind": "the kind of native law",
    "rule_relation_constraint_function_or_probability_law": "the complete native law",
    "write_replacement_assembly_or_commit": "how native results are written, assembled, or committed",
    "result_kind": "the complete native result type",
    "successor_cardinality": "the number of native successors/results per valid input",
    "determinism_branching_or_measure": "whether results are deterministic, branching, or measure-valued",
    "termination_completion_failure": "native completion, termination, and failure semantics",
    "witness_semantics": "what counts as a native witness or certificate",
    "parameters_and_variants": "the full parameter and variant space",
    "excluded_observers_and_representations": "a complete boundary between native mechanics and observers/representations",
    "evidence_limit": "the complete source-evidence boundary",
}


def exact_unknown_reason(spec: CandidateSpec, field: str) -> str:
    return (
        f"The assigned Chapter 2 evidence for {spec['name']} does not state "
        f"{UNKNOWN_FACT_LABELS[field]}."
    )


def justify_not_applicable(
    spec: CandidateSpec,
    fields: list[str],
    reason: str,
) -> None:
    not_applicable = spec.setdefault("not_applicable", {})
    source_evidence = spec["evidence"][0]
    for field in fields:
        if field in spec["facts"]:
            continue
        not_applicable[field] = reason
        if field not in source_evidence["fields"]:
            source_evidence["fields"].append(field)


direct_object_reason = (
    "This object is evaluated directly as a function or relation over supplied "
    "coordinates; it has no native iterated transition for this field."
)
for key in {
    "ca-time-slice-query",
    "ca-space-slice-query",
    "rule90-row-black-count",
    "rule90-row-black-positions",
    "k-color-rule90-row-count",
    "binomial-k-exponent-borrow-count",
    "binomial-mod-k-prime",
    "pascal-mod2",
    "rule60-pattern",
    "binomial-mod2-array",
    "multinomial-mod2-array",
    "stirling1-mod2-array",
    "stirling2-mod2-array",
    "gcd-pattern",
    "jacobi-pattern",
    "bitand-function",
    "bitor-function",
    "bitxor-function",
    "munching-squares",
    "bitand-curve",
    "bitor-curve",
    "bitxor-curve",
}:
    justify_not_applicable(
        next(item for item in ALL_CANDIDATE_SPECS if item["key"] == key),
        [
            "native_time",
            "structural_invariants",
            "visible_history",
            "control_state",
            "seed",
            "boundary",
            "external_data",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "write_replacement_assembly_or_commit",
            "witness_semantics",
        ],
        direct_object_reason,
    )
justify_not_applicable(
    experiment,
    ["external_data"],
    (
        "Observed run histories are results inspected by the experiment, not "
        "external data consumed by the sampled programs or protocol."
    ),
)

seed_constructor_reason = (
    "This candidate constructs or samples an initial configuration; it has no "
    "native iterated transition for this field."
)
for key in {
    "centered-single-seed",
    "cyclic-explicit-seed",
    "background-seed",
    "offset-block-seed",
    "dd-padded-seed",
    "explicit-cyclic-seed",
    "periodic-patch-seed",
    "positioned-patch-preset",
    "rule90-background-seed",
    "random-ca-initial-condition",
}:
    justify_not_applicable(
        next(item for item in ALL_CANDIDATE_SPECS if item["key"] == key),
        [
            "native_time",
            "visible_history",
            "control_state",
            "external_data",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "termination_completion_failure",
            "witness_semantics",
        ],
        seed_constructor_reason,
    )
justify_not_applicable(
    centered_seed,
    ["boundary"],
    (
        "This constructor returns a finite row but does not itself evolve it; "
        "an evolution boundary is a downstream program choice."
    ),
)

justify_not_applicable(
    cyclic_boundary,
    [
        "native_time",
        "visible_history",
        "control_state",
        "seed",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
        "witness_semantics",
    ],
    (
        "This candidate is a direct boundary lookup relation, not an iterated "
        "transition or state-writing program."
    ),
)

justify_not_applicable(
    symbolic_ca_formula,
    [
        "native_time",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "write_replacement_assembly_or_commit",
        "witness_semantics",
    ],
    (
        "This candidate symbolically derives a formula from a supplied CA law; "
        "it does not define a second native transition system."
    ),
)

justify_not_applicable(
    truchet,
    [
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
        "successor_cardinality",
        "determinism_branching_or_measure",
        "termination_completion_failure",
    ],
    (
        "This candidate denotes the complete model set of tile assignments; "
        "it is not a stepwise tile-placement process or a sampler that chooses "
        "one assignment."
    ),
)
justify_not_applicable(
    center_column,
    [
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "witness_semantics",
    ],
    (
        "This candidate is a deterministic projection/query over an underlying "
        "Rule 30 history, not a second native transition system."
    ),
)


def anchor_order_maps(
    reading_input: list[dict[str, str]],
    asset_input: list[dict[str, str]],
) -> tuple[dict[str, int], dict[str, int], dict[str, dict[str, str]]]:
    unit_order: dict[str, int] = {}
    image_order: dict[str, int] = {}
    asset_by_path: dict[str, dict[str, str]] = {}
    ordinal = 1
    for path in EXPECTED_PATHS:
        for row in reading_input:
            if row["path"] == path:
                unit_order[row["source_unit_id"]] = ordinal
                ordinal += 1
        for row in asset_input:
            if row["assignment_path"] == path:
                image_order[row["physical_path"]] = ordinal
                asset_by_path[row["physical_path"]] = row
                ordinal += 1
    if len(unit_order) != len(reading_input):
        raise AuthoringError("reading assignment contains an unexpected path")
    if len(image_order) != len(asset_input):
        raise AuthoringError("asset assignment contains an unexpected path")
    return unit_order, image_order, asset_by_path


def allocate_semantic_records(
    reading_input: list[dict[str, str]],
    asset_input: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, list[str]],
]:
    unit_order, image_order, asset_by_path = anchor_order_maps(
        reading_input, asset_input
    )

    def anchor_details(anchor_id: str) -> tuple[str, int]:
        if anchor_id in unit_order:
            return "SOURCE_UNIT", unit_order[anchor_id]
        if anchor_id in image_order:
            return "IMAGE", image_order[anchor_id]
        raise AuthoringError(f"unknown discovery anchor {anchor_id}")

    candidate_specs = sorted(
        ALL_CANDIDATE_SPECS,
        key=lambda item: (
            anchor_details(item["anchor"])[1],
            item["_insertion"],
        ),
    )
    candidate_id_by_key = {
        spec["key"]: f"W{index:04d}"
        for index, spec in enumerate(candidate_specs, 1)
    }
    candidate_ordinal_by_key: dict[str, int] = {}
    candidate_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for spec in candidate_specs:
        kind, _ = anchor_details(spec["anchor"])
        identity = (kind, spec["anchor"])
        candidate_counts[identity] += 1
        candidate_ordinal_by_key[spec["key"]] = candidate_counts[identity]

    evidence_entries: list[tuple[CandidateSpec, EvidenceSpec, str, int]] = []
    for spec in ALL_CANDIDATE_SPECS:
        for evidence_spec in spec["evidence"]:
            evidence_anchor = (
                evidence_spec["image_path"]
                if evidence_spec["image_path"] is not None
                else evidence_spec["unit"]
            )
            kind, order = anchor_details(evidence_anchor)
            evidence_entries.append((spec, evidence_spec, kind, order))
    evidence_entries.sort(
        key=lambda item: (
            item[3],
            item[1]["_insertion"],
            item[0]["_insertion"],
        )
    )
    evidence_identity: dict[tuple[str, str], tuple[str, str, int]] = {}
    evidence_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for index, (spec, evidence_spec, kind, _) in enumerate(evidence_entries, 1):
        anchor_id = (
            evidence_spec["image_path"]
            if evidence_spec["image_path"] is not None
            else evidence_spec["unit"]
        )
        identity = (kind, anchor_id)
        evidence_counts[identity] += 1
        evidence_identity[(spec["key"], evidence_spec["label"])] = (
            f"WE{index:06d}",
            f"WG{index:06d}",
            evidence_counts[identity],
        )

    route_specs = sorted(
        ALL_ROUTE_SPECS,
        key=lambda item: (
            unit_order[item["unit"]],
            item["_insertion"],
        ),
    )
    route_id_by_key = {
        spec["key"]: f"WR{index:04d}"
        for index, spec in enumerate(route_specs, 1)
    }
    route_counts: defaultdict[str, int] = defaultdict(int)
    route_proposals: list[dict[str, str]] = []
    route_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    for spec in route_specs:
        route_counts[spec["unit"]] += 1
        route_id = route_id_by_key[spec["key"]]
        route_links_by_unit[spec["unit"]].append(route_id)
        route_proposals.append(
            {
                "route_id": route_id,
                "source_unit_id": spec["unit"],
                "source_asset_id": "",
                "discovery_epoch": "1",
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": spec["unit"],
                "discovery_ordinal": str(route_counts[spec["unit"]]),
                "literal_target": spec["literal"],
                "route_kind": spec["kind"],
                "expected_topic": spec["topic"],
                "owning_stage": "6",
                "closure_scope": spec["scope"],
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": "[]",
                "vocabulary_terms": compact(spec["vocabulary"]),
                "defect_boundary": "",
            }
        )

    candidate_proposals: list[dict[str, Any]] = []
    candidate_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    candidate_links_by_image: defaultdict[str, list[str]] = defaultdict(list)
    anchor_candidate_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    for spec in candidate_specs:
        candidate_id = candidate_id_by_key[spec["key"]]
        anchor_kind, _ = anchor_details(spec["anchor"])
        local_evidence: list[dict[str, Any]] = []
        label_to_id: dict[str, str] = {}
        for evidence_spec in spec["evidence"]:
            evidence_id, group_id, ordinal = evidence_identity[
                (spec["key"], evidence_spec["label"])
            ]
            label_to_id[evidence_spec["label"]] = evidence_id
            evidence_anchor = (
                evidence_spec["image_path"]
                if evidence_spec["image_path"] is not None
                else evidence_spec["unit"]
            )
            evidence_kind = (
                "IMAGE"
                if evidence_spec["image_path"] is not None
                else "SOURCE_UNIT"
            )
            local_evidence.append(
                {
                    "evidence_id": evidence_id,
                    "evidence_group_id": group_id,
                    "discovery_anchor": {
                        "epoch": 1,
                        "kind": evidence_kind,
                        "id": evidence_anchor,
                        "ordinal": ordinal,
                    },
                    "source_unit_id": evidence_spec["unit"],
                    "image_path": evidence_spec["image_path"],
                    "strength": evidence_spec["strength"],
                    "modality": evidence_spec["modality"],
                    "claim": evidence_spec["claim"],
                    "fingerprint_fields": evidence_spec["fields"],
                }
            )
        local_evidence.sort(
            key=lambda item: int(item["evidence_id"][2:])
        )
        source_unit_ids = sorted(
            {item["source_unit_id"] for item in local_evidence},
            key=lambda unit_id: unit_order[unit_id],
        )
        image_witnesses = sorted(
            {
                item["image_path"]
                for item in local_evidence
                if item["image_path"] is not None
            },
            key=lambda path: image_order[path],
        )
        for unit_id in source_unit_ids:
            candidate_links_by_unit[unit_id].append(candidate_id)
        for image_path in image_witnesses:
            candidate_links_by_image[image_path].append(candidate_id)
        if anchor_kind == "SOURCE_UNIT":
            anchor_candidate_links_by_unit[spec["anchor"]].append(candidate_id)
        else:
            anchor_candidate_links_by_unit[
                asset_by_path[spec["anchor"]]["source_unit_id"]
            ].append(candidate_id)

        fingerprint: dict[str, dict[str, Any]] = {}
        field_support: dict[str, str] = {}
        unknown_reasons: list[str] = []
        for field in FINGERPRINT_FIELDS:
            supporting_ids = [
                item["evidence_id"]
                for item in local_evidence
                if field in item["fingerprint_fields"]
            ]
            if field in spec["facts"]:
                if not supporting_ids:
                    raise AuthoringError(
                        f"{spec['key']} has no evidence for supported field {field}"
                    )
                field_support[field] = "SUPPORTED"
                fingerprint[field] = {
                    "status": "SUPPORTED",
                    "value": spec["facts"][field],
                    "evidence_ids": supporting_ids,
                    "reason": "",
                }
            elif field in spec.get("not_applicable", {}):
                if not supporting_ids:
                    raise AuthoringError(
                        f"{spec['key']} has no evidence for not-applicable field {field}"
                    )
                field_support[field] = "NOT_APPLICABLE"
                fingerprint[field] = {
                    "status": "NOT_APPLICABLE",
                    "value": None,
                    "evidence_ids": supporting_ids,
                    "reason": spec["not_applicable"][field],
                }
            else:
                if supporting_ids:
                    raise AuthoringError(
                        f"{spec['key']} evidence claims absent field {field}"
                    )
                reason = exact_unknown_reason(spec, field)
                unknown_reasons.append(reason)
                field_support[field] = "UNKNOWN_FROM_SOURCE"
                fingerprint[field] = {
                    "status": "UNKNOWN_FROM_SOURCE",
                    "value": None,
                    "evidence_ids": [],
                    "reason": reason,
                }

        def parameter_records(
            values: list[tuple[str, str, list[str]]],
        ) -> list[dict[str, Any]]:
            records: list[dict[str, Any]] = []
            for name, description, labels in values:
                try:
                    evidence_ids = [label_to_id[label] for label in labels]
                except KeyError as exc:
                    raise AuthoringError(
                        f"{spec['key']} parameter cites unknown evidence {exc}"
                    ) from exc
                records.append(
                    {
                        "name": name,
                        "source_description": description,
                        "evidence_ids": evidence_ids,
                    }
                )
            return records

        try:
            candidate_route_ids = [
                route_id_by_key[key] for key in spec["route_keys"]
            ]
        except KeyError as exc:
            raise AuthoringError(
                f"{spec['key']} cites unknown route key {exc}"
            ) from exc
        provenance_units = set(source_unit_ids)
        for route_key in spec["route_keys"]:
            route_source = next(
                item["unit"]
                for item in ALL_ROUTE_SPECS
                if item["key"] == route_key
            )
            if route_source not in provenance_units:
                raise AuthoringError(
                    f"{spec['key']} route {route_key} lacks candidate provenance"
                )

        structured_parameters = spec["parameters"]
        structured_variants = spec["variants"]
        if (
            "parameters_and_variants" in spec["facts"]
            and not structured_parameters
            and not structured_variants
        ):
            support_labels = [
                item["label"]
                for item in spec["evidence"]
                if "parameters_and_variants" in item["fields"]
            ]
            if not support_labels:
                raise AuthoringError(
                    f"{spec['key']} claims parameter support without evidence"
                )
            structured_parameters = [
                (
                    "source-delimited parameters and variants",
                    spec["facts"]["parameters_and_variants"],
                    support_labels,
                )
            ]

        values: dict[str, Any] = {
            "id": candidate_id,
            "record_status": "ACTIVE",
            "provisional_name": spec["name"],
            "aliases": spec["aliases"],
            "discovery_stage": 6,
            "discovery_anchor": {
                "epoch": 1,
                "kind": anchor_kind,
                "id": spec["anchor"],
                "ordinal": candidate_ordinal_by_key[spec["key"]],
            },
            "source_unit_ids": source_unit_ids,
            "source_evidence": local_evidence,
            "source_status": spec.get("source_status", ["CLEAR"]),
            "image_witnesses": image_witnesses,
            "evidence_strength": list(
                dict.fromkeys(item["strength"] for item in local_evidence)
            ),
            "field_support": field_support,
            "fingerprint": fingerprint,
            "parameters": parameter_records(structured_parameters),
            "variants": parameter_records(structured_variants),
            "missing_mechanics": list(
                dict.fromkeys([spec["missing"], *unknown_reasons])
            ),
            "uncertainties": spec.get("uncertainties", []),
            "related_candidate_ids": [],
            "cross_reference_ids": candidate_route_ids,
            "evidence_reassignments": [],
        }
        candidate_proposals.append(
            {field: values[field] for field in CANDIDATE_FIELDS}
        )

    return (
        candidate_proposals,
        route_proposals,
        dict(candidate_links_by_unit),
        dict(candidate_links_by_image),
        dict(anchor_candidate_links_by_unit),
    )


def unit_number(unit_id: str) -> int:
    return int(unit_id[1:])


def default_reading_judgment(
    row: dict[str, str],
) -> tuple[str, list[str], str]:
    number = unit_number(row["source_unit_id"])
    if row["block_kind"] == "image":
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["REPRESENTATION"],
            (
                "Reviewed with its surrounding source and at original image "
                "resolution; this unlinked image is an output, comparison, or "
                "historical representation rather than native mechanics."
            ),
        )
    if row["path"] == EXPECTED_PATHS[0]:
        if number >= 258:
            return (
                "HISTORICAL_ONLY",
                ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
                (
                    "Reviewed in full; this unit supplies historical, "
                    "methodological, or behavior context without a separately "
                    "delimited native construction."
                ),
            )
        if row["block_kind"] in {"caption", "code"}:
            return (
                "REPRESENTATION_OR_OBSERVER",
                ["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"],
                (
                    "Reviewed in context; the caption or display describes an "
                    "output/representation already governed by candidate evidence "
                    "elsewhere and does not add a separate construction."
                ),
            )
        return (
            "NO_CONSTRUCTION",
            ["BEHAVIOR_OR_OUTCOME", "CONTROL_OR_COMPARISON"],
            (
                "Reviewed in full; this main-text unit discusses observed "
                "behavior, explanatory framing, or methodology without a new "
                "identity-plus-mechanics construction."
            ),
        )
    if number <= 5111:
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["IMPLEMENTATION_DETAIL", "REPRESENTATION"],
            (
                "Reviewed in full; this Notes unit is implementation syntax, "
                "an algebraic/Boolean encoding, a display control, or an output "
                "representation rather than an additional native construction."
            ),
        )
    if number <= 5149:
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["OBSERVER_OR_ANALYZER", "BEHAVIOR_OR_OUTCOME", "REPRESENTATION"],
            (
                "Reviewed in full; this Notes unit records a property, test, "
                "plot, or observer result and is not a distinct native law."
            ),
        )
    if number <= 5166:
        return (
            "NO_CONSTRUCTION",
            ["CONTROL_OR_COMPARISON", "APPLICATION"],
            (
                "Reviewed in full; this reactions/design discussion supplies "
                "comparison or application context without reproducible native mechanics."
            ),
        )
    return (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
        (
            "Reviewed in full; this historical or cultural unit either lacks a "
            "delimited construction procedure or repeats a separately captured "
            "candidate without adding native mechanics."
        ),
    )


def candidate_secondary_roles(
    unit_id: str,
    candidate_ids: list[str],
    candidate_specs_by_id: dict[str, CandidateSpec],
    block_kind: str,
) -> list[str]:
    roles: list[str] = []
    keys = {candidate_specs_by_id[item]["key"] for item in candidate_ids}
    if keys & SEED_KEYS:
        roles.append("SEED_INPUT_OR_BOUNDARY")
    if keys & HISTORICAL_CANDIDATE_KEYS:
        roles.append("HISTORICAL_MENTION")
    if block_kind == "image":
        roles.append("REPRESENTATION")
    if unit_id in {"U005145", "U005146"}:
        roles.append("OBSERVER_OR_ANALYZER")
    if unit_id == "U005291":
        roles.append("APPLICATION")
    if unit_id == "U005129":
        roles.append("HISTORICAL_MENTION")
    if unit_id in {"U004988", "U005043", "U005148"}:
        roles.append("SOURCE_DEFECT")
    return list(dict.fromkeys(roles))


def build_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    if (
        manifest.get("worker_id") != EXPECTED_WORKER
        or manifest.get("content_set_sha256") != EXPECTED_CONTENT_SET
        or manifest.get("source_paths") != EXPECTED_PATHS
        or manifest.get("source_unit_count") != 489
        or manifest.get("asset_count") != 78
        or manifest.get("stage") != 6
        or manifest.get("discovery_epoch") != 1
    ):
        raise AuthoringError("bundle is not the exact Stage 6 epoch-1 assignment")

    output_path = bundle / "output" / "output.json"
    original_bytes = output_path.read_bytes()
    output = json.loads(original_bytes)
    reading_input = read_csv(bundle / "input" / "reading-input.csv")
    asset_input = read_csv(bundle / "input" / "asset-input.csv")
    scaffold = prepare_review_output.scaffold_output(
        prepare_review_output.expected_template(bundle, manifest),
        reading_input,
        asset_input,
    )
    if output != scaffold:
        raise AuthoringError(
            "worker output is not the exact nonsemantic scaffold; refusing "
            "to overwrite review work"
        )

    (
        candidate_proposals,
        route_proposals,
        candidate_links_by_unit,
        candidate_links_by_image,
        anchor_candidate_links_by_unit,
    ) = allocate_semantic_records(reading_input, asset_input)
    candidate_specs_sorted = sorted(
        ALL_CANDIDATE_SPECS,
        key=lambda spec: next(
            index
            for index, candidate in enumerate(candidate_proposals)
            if candidate["provisional_name"] == spec["name"]
            and candidate["discovery_anchor"]["id"] == spec["anchor"]
        ),
    )
    if len(candidate_specs_sorted) != len(candidate_proposals):
        raise AuthoringError("candidate proposal/spec allocation differs")
    candidate_specs_by_id = {
        proposal["id"]: spec
        for proposal, spec in zip(candidate_proposals, candidate_specs_sorted)
    }
    route_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    for route in route_proposals:
        route_links_by_unit[route["source_unit_id"]].append(route["route_id"])

    reading_updates: list[dict[str, str]] = []
    for original in reading_input:
        row = deepcopy(original)
        unit_id = row["source_unit_id"]
        candidate_ids = candidate_links_by_unit.get(unit_id, [])
        route_ids = route_links_by_unit.get(unit_id, [])
        if candidate_ids:
            is_anchor = bool(
                set(candidate_ids)
                & set(anchor_candidate_links_by_unit.get(unit_id, []))
            )
            disposition = "CANDIDATE" if is_anchor else "SUPPORTS_CANDIDATE"
            secondary = candidate_secondary_roles(
                unit_id,
                candidate_ids,
                candidate_specs_by_id,
                row["block_kind"],
            )
            names = [
                candidate_specs_by_id[item]["name"] for item in candidate_ids
            ]
            statement = (
                f"This unit {'discovers' if is_anchor else 'supports'} "
                f"{', '.join(candidate_ids)} ({'; '.join(names)}) with "
                "source-grounded identity, mechanics, representation limits, "
                "or explicit uncertainty."
            )
            if route_ids:
                statement += (
                    f" It also originates {', '.join(route_ids)} for mechanics "
                    "or relations not completed in this unit."
                )
        elif route_ids:
            disposition = "CROSS_REFERENCE"
            secondary = (
                ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"]
                if unit_number(unit_id) >= 5227
                else ["CONTROL_OR_COMPARISON"]
            )
            statement = (
                f"Reviewed in full; this unit originates "
                f"{', '.join(route_ids)} to construction-bearing targets while "
                "remaining route, context, property, or representation evidence here."
            )
        else:
            disposition, secondary, statement = default_reading_judgment(row)
        if unit_id in {"U004988", "U005043", "U005148"}:
            secondary = list(dict.fromkeys([*secondary, "SOURCE_DEFECT"]))
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": disposition,
                "source_status": (
                    "DEFECTIVE"
                    if unit_id in {"U004988", "U005043", "U005148"}
                    else "AMBIGUOUS"
                    if unit_id == "U005120"
                    else "CLEAR"
                ),
                "uncertainty": (
                    "The phrase “tries to updates” is grammatically defective; "
                    "the surrounding sentence still unambiguously states the "
                    "old-snapshot update requirement."
                    if unit_id == "U004988"
                    else (
                        "The sentence omits or corrupts the subject of the Rule "
                        "30 example call; U005044 supplies the exact call and output."
                        if unit_id == "U005043"
                        else (
                            "The striped inline seed symbol is identifiable, but "
                            "its individual binary cells and exact repeated value "
                            "sequence cannot be recovered unambiguously."
                            if unit_id == "U005120"
                            else (
                                "The phrase “I would amazed” is missing “be”; "
                                "the intended nonrepetition claim and page route "
                                "remain unambiguous."
                                if unit_id == "U005148"
                                else ""
                            )
                        )
                    )
                ),
                "secondary_roles": compact(secondary),
                "candidate_ids": compact(candidate_ids),
                "route_ids": compact(route_ids),
                "evidence_statement": statement,
                "review_stage": "6",
                "reviewer": EXPECTED_WORKER,
            }
        )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in asset_input:
        row = deepcopy(original)
        image_path = row["physical_path"]
        source_unit_id = row["source_unit_id"]
        candidate_ids = candidate_links_by_image.get(image_path, [])
        if candidate_ids:
            visual_role = "NATIVE_EVIDENCE"
            risk_flags = ["CONSTRUCTION_BEARING"]
            if (
                image_path
                == "BACK-MATTER/NOTES/_page_885_inline_black_gradient_white_block.jpeg"
            ):
                risk_flags.append("AMBIGUOUS")
            transcription_status = "CHECKED"
            statement = (
                "Original-resolution inspection confirms construction-bearing "
                f"visual evidence for {', '.join(candidate_ids)}; only visibly "
                "unambiguous geometry, symbols, or lookup cases are used."
            )
        elif image_path == "CHAPTERS/_page_38_Chapter_Opener.jpeg":
            visual_role = "DECORATIVE"
            risk_flags = []
            transcription_status = "NOT_REQUIRED"
            statement = (
                "Original-resolution inspection confirms a decorative Chapter 2 "
                "opener without a captioned rule, seed, or construction."
            )
        elif source_unit_id in RELATION_IMAGE_UNITS:
            visual_role = "RELATION"
            risk_flags = ["CONSTRUCTION_BEARING"]
            transcription_status = "NOT_REQUIRED"
            statement = (
                "Original-resolution inspection confirms a historical ornament "
                "or comparison image; surrounding text does not supply enough "
                "mechanics to use it as native candidate evidence."
            )
        elif source_unit_id in CONTROL_IMAGE_UNITS:
            visual_role = "CONTROL"
            risk_flags = ["TEXT_BEARING"]
            transcription_status = "CHECKED"
            statement = (
                "Original-resolution inspection confirms a historical publication-"
                "count/control figure, not a construction law."
            )
        else:
            visual_role = "OBSERVER"
            risk_flags = ["CONSTRUCTION_BEARING"]
            transcription_status = "NOT_REQUIRED"
            statement = (
                "Original-resolution inspection confirms an evolution, plot, "
                "rendered output, or comparison view; its native mechanics are "
                "supplied by prose/formula evidence or remain absent."
            )
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": visual_role,
                "source_status": (
                    "AMBIGUOUS"
                    if image_path
                    == "BACK-MATTER/NOTES/_page_885_inline_black_gradient_white_block.jpeg"
                    else "CLEAR"
                ),
                "risk_flags": compact(risk_flags),
                "original_resolution_status": "REVIEWED",
                "transcription_status": transcription_status,
                "candidate_ids": compact(candidate_ids),
                "route_ids": "[]",
                "evidence_statement": statement,
                "review_stage": "6",
                "reviewer": EXPECTED_WORKER,
                "uncertainty": (
                    "The striped background block is visible as a qualitative "
                    "symbol, but its individual binary cells and exact repeated "
                    "value sequence cannot be recovered unambiguously."
                    if image_path
                    == "BACK-MATTER/NOTES/_page_885_inline_black_gradient_white_block.jpeg"
                    else ""
                ),
            }
        )
        asset_updates.append(row)

    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": candidate_proposals,
            "asset_updates": asset_updates,
            "route_proposals": route_proposals,
            "uncertainties": [
                (
                    "The Rule 90 striped-background inline artwork is preserved "
                    "without inventing a numeric block transcription."
                ),
                (
                    "Historically named partial cellular automata retain exact "
                    "missing transition, seed, boundary, and witness mechanics "
                    "as source limits for later routed review."
                ),
            ],
        }
    )
    return original_bytes, proposed


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} BUNDLE", file=sys.stderr)
        return 2
    bundle = Path(sys.argv[1]).resolve()
    try:
        with prepare_review_output.output_lock(bundle):
            original_bytes, proposed = build_output(bundle)
            prepare_review_output.atomic_replace(
                bundle / "output" / "output.json",
                canonical_json_bytes(proposed),
                original_bytes,
            )
    except (OSError, csv.Error, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"Chapter 2 authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "recorded Stage 6 Chapter 2 review: "
        f"reading=489 assets=78 candidates={len(ALL_CANDIDATE_SPECS)} "
        f"routes={len(ALL_ROUTE_SPECS)} declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
