#!/usr/bin/env python3
"""Author the sealed Stage 7 Chapter 3 main-text blind review reproducibly.

The helper is deliberately bound to the exact epoch-1 sealed bundle.  It
records judgments made after U000306--U000640 were read sequentially and all
87 assigned assets were screened and inspected at source-preserving
resolution.  It will only replace the pristine nonsemantic worksheet.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

TOOLS = Path("/home/jake/Developer/ankos/goal-4/tools")
sys.path.insert(0, str(TOOLS))

import prepare_review_output  # noqa: E402
from audit_contract import (  # noqa: E402
    CANDIDATE_FIELDS,
    FINGERPRINT_FIELDS,
    canonical_json_bytes,
)


EXPECTED_CONTENT_SET = (
    "e554fe52881b9a2dc3ca6062df10b3458f5556035d257a81301e7c3eb48d2aae"
)
EXPECTED_WORKER = "ch03-main-reader-e1"
EXPECTED_PATHS = ["CHAPTERS/03-The-World-of-Simple-Programs.md"]
STAGE = 7


class AuthoringError(ValueError):
    """The exact assignment or pristine output is not safe to update."""


def compact(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


CandidateSpec = dict[str, Any]
EvidenceSpec = dict[str, Any]
RouteSpec = dict[str, Any]
ALL_CANDIDATES: list[CandidateSpec] = []
ALL_ROUTES: list[RouteSpec] = []
_evidence_insertion = 0


def candidate(
    key: str,
    name: str,
    anchor: str,
    facts: dict[str, str],
    *,
    aliases: list[str] | None = None,
    not_applicable: dict[str, str] | None = None,
    missing: str,
    source_status: list[str] | None = None,
    uncertainties: list[str] | None = None,
    parameters: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    if any(item["key"] == key for item in ALL_CANDIDATES):
        raise AuthoringError(f"duplicate candidate key {key}")
    spec: CandidateSpec = {
        "key": key,
        "name": name,
        "anchor": anchor,
        "facts": facts,
        "aliases": aliases or [],
        "not_applicable": not_applicable or {},
        "missing": missing,
        "source_status": source_status or ["CLEAR"],
        "uncertainties": uncertainties or [],
        "parameters": parameters or [],
        "variants": variants or [],
        "route_keys": route_keys or [],
        "evidence": [],
        "_insertion": len(ALL_CANDIDATES),
    }
    ALL_CANDIDATES.append(spec)
    return spec


def evidence(
    spec: CandidateSpec,
    label: str,
    unit: str,
    claim: str,
    fields: list[str],
    *,
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    modality: str = "PROSE",
    image_path: str | None = None,
) -> None:
    global _evidence_insertion
    if any(item["label"] == label for item in spec["evidence"]):
        raise AuthoringError(f"duplicate evidence label {label}")
    spec["evidence"].append(
        {
            "label": label,
            "unit": unit,
            "claim": claim,
            "fields": fields,
            "strength": strength,
            "modality": modality,
            "image_path": image_path,
            "_insertion": _evidence_insertion,
        }
    )
    _evidence_insertion += 1


def source_candidate(
    key: str,
    name: str,
    anchor: str,
    facts: dict[str, str],
    *,
    aliases: list[str] | None = None,
    not_applicable: dict[str, str] | None = None,
    missing: str,
    claim: str,
    strength: str = "DIRECT_COMPLETE_MECHANICS",
    modality: str = "PROSE",
    image_path: str | None = None,
    source_status: list[str] | None = None,
    uncertainties: list[str] | None = None,
    parameters: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    spec = candidate(
        key,
        name,
        anchor,
        facts,
        aliases=aliases,
        not_applicable=not_applicable,
        missing=missing,
        source_status=source_status,
        uncertainties=uncertainties,
        parameters=parameters,
        variants=variants,
        route_keys=route_keys,
    )
    fields = list(facts) + list((not_applicable or {}).keys())
    evidence(
        spec,
        f"{key}-source",
        anchor,
        claim,
        fields,
        strength=strength,
        modality=("IMAGE" if image_path else modality),
        image_path=image_path,
    )
    return spec


def context_evidence(
    spec: CandidateSpec,
    label: str,
    unit: str,
    claim: str,
    *,
    image_path: str | None = None,
    strength: str = "CONTEXTUAL",
    modality: str = "PROSE",
) -> None:
    evidence(
        spec,
        label,
        unit,
        claim,
        [],
        strength=strength,
        modality=("IMAGE" if image_path else modality),
        image_path=image_path,
    )


NA_NO_CONTROL = {
    "control_state": (
        "This construction has no independently stored head, instruction "
        "pointer, or other control register."
    ),
    "external_data": (
        "The assigned construction is closed after its rule and initial state "
        "are supplied; no external data stream is part of the native law."
    ),
}


def trajectory_facts(
    *,
    kind: str,
    carrier: str,
    support: str,
    topology: str,
    invariants: str,
    alphabet: str,
    state: str,
    seed: str,
    frontier: str,
    schedule: str,
    read: str,
    law_kind: str,
    law: str,
    write: str,
    result: str,
    variants: str,
    excluded: str,
) -> dict[str, str]:
    return {
        "object_kind": kind,
        "native_time": "Discrete successive steps.",
        "carrier": carrier,
        "support": support,
        "topology": topology,
        "structural_invariants": invariants,
        "alphabet_or_value_schema": alphabet,
        "complete_state": state,
        "visible_history": (
            "A run is witnessed by the ordered sequence of complete states; "
            "the chapter normally stacks or juxtaposes these states as a picture."
        ),
        "seed": seed,
        "frontier_or_activation": frontier,
        "schedule": schedule,
        "read_dependencies_or_neighborhood": read,
        "law_kind": law_kind,
        "rule_relation_constraint_function_or_probability_law": law,
        "write_replacement_assembly_or_commit": write,
        "result_kind": result,
        "successor_cardinality": (
            "Exactly one successor state follows from each state for a fixed rule."
        ),
        "determinism_branching_or_measure": (
            "Deterministic for a fixed rule and complete state; no branching "
            "or probability is part of the native update."
        ),
        "termination_completion_failure": (
            "The source treats the law as iteratable for successive steps; "
            "termination occurs only where the construction explicitly loses "
            "all applicable structure."
        ),
        "witness_semantics": (
            "A valid trajectory is a state sequence in which every adjacent "
            "pair satisfies the stated update law."
        ),
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": excluded,
        "evidence_limit": (
            "The chapter fixes the stated rule class and examples but does not "
            "always state finite-display boundary or implementation conventions."
        ),
    }


ECA_BASE = trajectory_facts(
    kind="A one-dimensional elementary binary cellular automaton.",
    carrier="Cell positions carrying one of two colors.",
    support="A one-dimensional line of cells.",
    topology="Every cell has an immediate left and right neighbor.",
    invariants="The line support, binary alphabet, and three-cell read shape persist.",
    alphabet="Two colors, represented as white/0 and black/1.",
    state="The current black/white value at every cell position.",
    seed="The displayed survey starts from one black cell on a white background.",
    frontier="Every cell position is updated at every generation.",
    schedule="All cells are updated in parallel from the preceding complete row.",
    read="The old values of left neighbor, self, and right neighbor.",
    law_kind="A deterministic eight-case local lookup table.",
    law=(
        "For each of the eight binary left/self/right cases, choose one binary "
        "output; the eight outputs form the base-2 digits of rule numbers 0--255."
    ),
    write="Commit every chosen output simultaneously as the next row.",
    result="A new complete binary row and, under iteration, a cellular-automaton trajectory.",
    variants=(
        "There are 256 numbered rules, 88 inequivalent after the stated "
        "left-right and black-white symmetries, with initial condition varied separately."
    ),
    excluded=(
        "Stacked grids, cropping, behavior classes, fractal dimensions, and "
        "visual labels are observations or representations, not extra update state."
    ),
)


eca_family = source_candidate(
    "eca-family",
    "elementary binary nearest-neighbor cellular automaton family",
    "U000320",
    ECA_BASE,
    aliases=["256 elementary cellular automaton rules"],
    not_applicable=NA_NO_CONTROL,
    missing="The chapter does not explicitly fix the off-picture boundary convention.",
    claim=(
        "The passage and adjacent rule diagram delimit binary line cellular "
        "automata whose parallel next-cell value is selected from the eight "
        "left/self/right color cases."
    ),
)
context_evidence(
    eca_family,
    "eca-family-codec",
    "U000325",
    "The rule-number paragraph fixes the 0--255 base-2 lookup-table encoding.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    eca_family,
    "eca-family-survey",
    "U000333",
    "The survey caption fixes the single-black-cell runs and 88 symmetry classes.",
)
for _label, _unit, _path in [
    ("eca-catalog-page69", "U000329", "CHAPTERS/_page_69_Rules_100_139.jpeg"),
    ("eca-catalog-page70", "U000331", "CHAPTERS/_page_70_Picture_2.jpeg"),
    ("eca-catalog-page71", "U000332", "CHAPTERS/_page_71_Picture_2.jpeg"),
]:
    context_evidence(
        eca_family,
        _label,
        _unit,
        "Original-resolution inspection confirms that this is one part of the complete 256-rule catalog.",
        image_path=_path,
        strength="CORROBORATING",
    )


codec_facts = {
    "object_kind": "A deterministic codec between an elementary-rule table and an integer.",
    "native_time": "No native time; this is a fixed encoding/decoding function.",
    "carrier": "Eight ordered binary output choices.",
    "support": "The eight possible binary left/self/right neighborhood cases.",
    "alphabet_or_value_schema": "Eight base-2 digits and an integer in 0--255.",
    "complete_state": "An ordered eight-output lookup table or its integer code.",
    "input": "One ordered eight-case binary rule table, or one code in 0--255.",
    "law_kind": "A base-2 positional encoding and its inverse.",
    "rule_relation_constraint_function_or_probability_law": (
        "Read the eight chosen outputs in the pictured case order as base-2 "
        "digits to obtain the rule number; decode the number to recover them."
    ),
    "result_kind": "The corresponding integer code or lookup table.",
    "successor_cardinality": "Exactly one code per table and one table per code.",
    "determinism_branching_or_measure": "Deterministic and bijective on the stated domain.",
    "witness_semantics": "Re-encoding the decoded eight digits yields the same integer.",
    "parameters_and_variants": "The case ordering is the ordering shown in the rule diagram.",
    "excluded_observers_and_representations": "Printed cell icons display the case order.",
    "evidence_limit": "The visual case order must be preserved; it is not safe to infer another convention.",
}
codec_na = {
    field: "A fixed codec has no iterative state transition for this field."
    for field in [
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
    ]
}
eca_codec = source_candidate(
    "eca-codec",
    "elementary cellular-automaton base-2 rule-number codec",
    "U000323",
    codec_facts,
    aliases=["rules 0 to 255 numbering scheme"],
    not_applicable=codec_na,
    missing="No mechanics are missing within the pictured case-order convention.",
    claim="The passage introduces the 0--255 numbering; the following caption defines it as an eight-digit base-2 encoding.",
)
context_evidence(
    eca_codec,
    "eca-codec-caption",
    "U000325",
    "The caption explicitly defines the bidirectional rule-table/code correspondence.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    eca_codec,
    "eca-codec-image",
    "U000324",
    "Original-resolution inspection confirms the ordered eight-case visual table.",
    image_path="CHAPTERS/_page_68_Figure_7.jpeg",
    strength="CORROBORATING",
)

eca_quotient_facts = {
    "object_kind": "A deterministic equivalence quotient on elementary cellular-automaton rules.",
    "native_time": "No native time; this is a fixed equivalence-class query.",
    "carrier": "The 256 elementary binary nearest-neighbor rule tables.",
    "support": "Ordered eight-case elementary rule tables and their 0--255 codes.",
    "alphabet_or_value_schema": "Binary rule outputs, acted on by left/right reflection and black/white exchange.",
    "complete_state": "One complete elementary rule table or its code.",
    "input": "One elementary rule.",
    "law_kind": "A finite symmetry-generated equivalence relation.",
    "rule_relation_constraint_function_or_probability_law": (
        "Treat rules as equivalent when one is obtained from another by "
        "interchanging left and right or by interchanging black and white, "
        "including compositions of those operations."
    ),
    "result_kind": "The rule's equivalence class, one of 88 fundamentally inequivalent classes.",
    "successor_cardinality": "Exactly one equivalence class contains each elementary rule.",
    "determinism_branching_or_measure": "Deterministic and non-probabilistic.",
    "witness_semantics": "Two rules witness equivalence when a stated interchange maps one complete table to the other.",
    "parameters_and_variants": "The source permits left/right and black/white interchange.",
    "excluded_observers_and_representations": "Catalog layout and observed behavior do not alter equivalence.",
    "evidence_limit": "The source does not select a canonical representative for each class.",
}
eca_quotient = source_candidate(
    "eca-symmetry-quotient",
    "elementary cellular-automaton reflection/color equivalence quotient",
    "U000333",
    eca_quotient_facts,
    aliases=["88 fundamentally inequivalent elementary rules"],
    not_applicable=codec_na,
    missing="No canonical representative-selection convention is stated.",
    claim=(
        "The caption explicitly defines equivalence under left/right or "
        "black/white interchange and states that the 256 rules form 88 classes."
    ),
)
context_evidence(
    eca_quotient,
    "eca-symmetry-rule110",
    "U000348",
    "The rule-110 discussion corroborates the quotient by identifying four equivalent cases under the same interchanges.",
    strength="CORROBORATING",
)


def seed_facts(name: str, carrier: str, value: str, scope: str) -> dict[str, str]:
    return {
        "object_kind": f"An initial-state class: {name}.",
        "native_time": "No native time; this object denotes admissible initial states.",
        "carrier": carrier,
        "support": scope,
        "alphabet_or_value_schema": value,
        "complete_state": "The fully specified initial configuration.",
        "seed": name,
        "result_kind": "An initial complete state for the associated evolution law.",
        "successor_cardinality": "Exactly one initial configuration for a fixed placement convention.",
        "determinism_branching_or_measure": "Deterministic, not sampled.",
        "witness_semantics": "The initial state visibly has exactly the stated non-background content.",
        "parameters_and_variants": "Placement and the associated system family are external parameters.",
        "excluded_observers_and_representations": "Its drawn row is a representation of the seed.",
        "evidence_limit": "The source does not state a separate finite boundary convention.",
    }


seed_na = {
    field: "An initial-state object has no independent update law for this field."
    for field in [
        "visible_history",
        "control_state",
        "input",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
    ]
}
single_black = source_candidate(
    "eca-single-black-seed",
    "single-black-cell cellular-automaton seed",
    "U000330",
    seed_facts(
        "one black cell on an otherwise white line",
        "Binary cell positions",
        "One black/1 position and white/0 elsewhere",
        "A one-dimensional cell line",
    ),
    not_applicable=seed_na,
    missing="The exact origin coordinate and finite-display boundary are not stated.",
    claim="The caption states that every rule survey run starts from a single black cell.",
)


def eca_preset(
    rule: int,
    anchor: str,
    behavior: str,
    *,
    image_path: str | None = None,
) -> CandidateSpec:
    facts = deepcopy(ECA_BASE)
    facts["object_kind"] = f"Elementary cellular automaton rule {rule}."
    facts["rule_relation_constraint_function_or_probability_law"] = (
        f"Decode integer {rule} in the chapter's ordered eight-case base-2 "
        "scheme and use the resulting bit for every left/self/right neighborhood."
    )
    facts["result_kind"] = behavior
    facts["parameters_and_variants"] = (
        f"Rule number is fixed at {rule}; the displayed run uses the chapter's "
        "single-black-cell initial condition."
    )
    key = f"eca-rule-{rule}"
    spec = source_candidate(
        key,
        f"elementary cellular automaton rule {rule} preset",
        anchor,
        facts,
        aliases=[f"rule {rule}"],
        not_applicable=NA_NO_CONTROL,
        missing="The off-picture boundary convention is not explicitly stated.",
        claim=(
            f"The source unambiguously delimits rule {rule}; read with the "
            "chapter's immediately established 0--255 codec, its eight-case "
            f"local law is fixed. The cited behavior is {behavior.lower()}."
        ),
        image_path=image_path,
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    return spec


rule_image = "CHAPTERS/_page_68_Picture_3.jpeg"
eca_rules: dict[int, CandidateSpec] = {}
for _rule, _desc in [
    (250, "A displayed elementary-rule evolution."),
    (90, "A displayed nested elementary-rule evolution."),
    (30, "A displayed evolution with apparently random features."),
    (110, "A displayed evolution mixing regular and irregular localized structures."),
]:
    eca_rules[_rule] = eca_preset(_rule, "U000321", _desc, image_path=rule_image)
for _rule, _desc in [
    (0, "All cells become white after one step."),
    (128, "All cells become white after one step."),
    (255, "All cells become black after one step."),
    (7, "The cells alternate between black and white on successive steps."),
    (127, "The cells alternate between black and white on successive steps."),
]:
    eca_rules[_rule] = eca_preset(_rule, "U000328", _desc)
for _rule, _desc in [
    (4, "A small stationary persistent pattern."),
    (123, "A small stationary persistent pattern."),
    (2, "A small persistent pattern that moves."),
    (103, "A moving pattern with average speed one half cell per step."),
]:
    eca_rules[_rule] = eca_preset(_rule, "U000334", _desc)
eca_rules[3] = eca_preset(
    3, "U000335", "A moving pattern with average speed one half cell per step."
)
for _rule in [50, 109]:
    eca_rules[_rule] = eca_preset(
        _rule, "U000336", "An indefinitely growing purely repetitive pattern."
    )
for _rule, _desc in [
    (22, "A nested pattern."),
    (60, "A nested pattern."),
    (225, "A nested pattern whose width grows on average as the square root of time."),
]:
    eca_rules[_rule] = eca_preset(_rule, "U000337", _desc)
eca_rules[150] = eca_preset(
    150,
    "U000338",
    "A nested pattern with the captioned fractal dimension.",
    image_path="CHAPTERS/_page_73_Figure_1.jpeg",
)
for _rule in [105, 129]:
    eca_rules[_rule] = eca_preset(
        _rule,
        "U000338",
        "A displayed nested elementary-rule evolution.",
        image_path="CHAPTERS/_page_73_Figure_1.jpeg",
    )
for _rule in [22, 60, 225]:
    context_evidence(
        eca_rules[_rule],
        f"eca-rule-{_rule}-nested-figure",
        "U000338",
        f"The curated nested-rule figure visibly identifies and displays rule {_rule}.",
        image_path="CHAPTERS/_page_73_Figure_1.jpeg",
        strength="CORROBORATING",
    )
eca_rules[45] = eca_preset(
    45,
    "U000344",
    "A displayed evolution with many apparently random features.",
    image_path="CHAPTERS/_page_74_Picture_3.jpeg",
)
context_evidence(
    eca_rules[45],
    "eca-rule-45-name",
    "U000345",
    "The following label names the preceding evolution as rule 45.",
    strength="DIRECT_IDENTITY",
)
eca_rules[73] = eca_preset(
    73,
    "U000346",
    "A displayed evolution with many apparently random features.",
    image_path="CHAPTERS/_page_74_Picture_5.jpeg",
)
context_evidence(
    eca_rules[73],
    "eca-rule-73-name",
    "U000347",
    "The following label names the preceding evolution as rule 73.",
    strength="DIRECT_IDENTITY",
)
context_evidence(
    eca_rules[30],
    "eca-rule-30-defective-label",
    "U000343",
    "The assigned 42-by-14 crop contains only a damaged 'rule 30' label; it is retained as defect-limited corroboration, not used to reconstruct mechanics.",
    image_path="CHAPTERS/_page_74_Picture_2.jpeg",
    strength="DEFECT_LIMITED",
)
eca_rules[30]["source_status"] = ["CLEAR", "DEFECTIVE"]
eca_rules[30]["uncertainties"].append(
    "The page-74 rule-30 label asset is severely cropped, but the earlier complete rule table independently fixes the preset."
)


TOTALISTIC_BASE = trajectory_facts(
    kind="A three-color totalistic nearest-neighbor cellular automaton.",
    carrier="Cell positions carrying white, gray, or black.",
    support="A one-dimensional line of cells.",
    topology="Every cell has immediate left and right neighbors.",
    invariants="The line, three-color schema, and totalistic three-cell read remain fixed.",
    alphabet="0=white, 1=gray, 2=black.",
    state="The current 0/1/2 value at every cell position.",
    seed="Displayed examples use one gray cell on a white background.",
    frontier="Every cell position is updated each generation.",
    schedule="Parallel update from the complete preceding row.",
    read="The average (equivalently sum) of left, self, and right old color values.",
    law_kind="A deterministic seven-case totalistic lookup table.",
    law=(
        "Select the next color from the seven possible neighborhood averages "
        "0, 1/3, ..., 2; the seven ternary outputs encode a code in 0--2186."
    ),
    write="Commit every selected color simultaneously as the next row.",
    result="A complete three-color next row and its iterated trajectory.",
    variants="There are 2187 three-color totalistic rules, identified by ternary code number.",
    excluded="Grids, code labels, behavior classes, and compressed long runs are representations or observations.",
)

totalistic_family = source_candidate(
    "totalistic-3-family",
    "three-color totalistic cellular automaton family",
    "U000350",
    TOTALISTIC_BASE,
    aliases=["2187 three-color totalistic rules"],
    not_applicable=NA_NO_CONTROL,
    missing="The source does not explicitly state the off-picture boundary convention.",
    claim="The passage introduces the three-color restriction and delimits the totalistic subfamily.",
)
context_evidence(
    totalistic_family,
    "totalistic-3-law",
    "U000353",
    "The caption fixes colors 0/1/2, seven averages, and the ternary rule-code convention.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

totalistic_code_image = "CHAPTERS/_page_75_Figure_6.jpeg"

totalistic_codec_facts = {
    "object_kind": "A deterministic codec between a three-color totalistic rule table and an integer.",
    "native_time": "No native time; this is a fixed encoding/decoding function.",
    "carrier": "Seven ordered three-color outputs.",
    "support": "The seven possible averages 0, 1/3, 2/3, 1, 4/3, 5/3, and 2.",
    "alphabet_or_value_schema": "Seven ternary digits and an integer in 0--2186.",
    "complete_state": "An ordered seven-output totalistic table or its integer code.",
    "input": "One ordered seven-case ternary table, or one code in 0--2186.",
    "law_kind": "A base-3 positional encoding and its inverse.",
    "rule_relation_constraint_function_or_probability_law": (
        "Read the outputs in the pictured average-case order as base-3 digits "
        "to obtain the code; decode the code to recover the seven outputs."
    ),
    "result_kind": "The corresponding totalistic code or seven-output table.",
    "successor_cardinality": "Exactly one code per table and one table per code.",
    "determinism_branching_or_measure": "Deterministic and bijective on the stated domain.",
    "witness_semantics": "Re-encoding the decoded seven ternary outputs yields the same integer.",
    "parameters_and_variants": "The average-case order is the one shown in the worked rule.",
    "excluded_observers_and_representations": "Printed color boxes display, but do not change, the case order.",
    "evidence_limit": "The visual case order must be preserved; another convention is not inferred.",
}
totalistic_codec = source_candidate(
    "totalistic-3-codec",
    "three-color totalistic cellular-automaton base-3 rule codec",
    "U000351",
    totalistic_codec_facts,
    aliases=["three-color totalistic code number"],
    not_applicable=codec_na,
    missing="No mechanics are missing within the pictured seven-average convention.",
    claim="The passage defines 2187 three-color totalistic rules and introduces their code numbers.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    totalistic_codec,
    "totalistic-codec-diagram",
    "U000352",
    "The worked original-resolution rule orders all seven average cases and their ternary outputs.",
    image_path=totalistic_code_image,
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    totalistic_codec,
    "totalistic-codec-caption",
    "U000353",
    "The caption explicitly defines the average-case order and base-3 positional encoding.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

white_preserving_totalistic = source_candidate(
    "totalistic-white-background-restriction",
    "white-background-preserving three-color totalistic-rule restriction",
    "U000355",
    {
        **TOTALISTIC_BASE,
        "object_kind": "The restriction to three-color totalistic rules that preserve an all-white background.",
        "structural_invariants": "The all-white configuration is a fixed background under every admitted rule.",
        "rule_relation_constraint_function_or_probability_law": (
            "Use a three-color totalistic table whose output for the all-white, average-0 neighborhood is white."
        ),
        "parameters_and_variants": "Exclude every three-color totalistic rule that changes the white background.",
        "result_kind": "A white-background-preserving next row and trajectory.",
    },
    not_applicable=NA_NO_CONTROL,
    missing="The figure is a representative code-numbered survey, not a textual enumeration of every admitted code.",
    claim="The original-resolution grid delimits the selected totalistic-rule survey.",
    image_path="CHAPTERS/_page_76_Figure_2.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    white_preserving_totalistic,
    "totalistic-white-preserving-caption",
    "U000356",
    "The caption explicitly states that rules which change the white background are excluded.",
    strength="DIRECT_COMPLETE_MECHANICS",
)


def totalistic_preset(
    code: int | None,
    anchor: str,
    behavior: str,
    *,
    image_path: str | None = None,
    ambiguous_name: str | None = None,
    source_strength: str | None = None,
    claim_override: str | None = None,
) -> CandidateSpec:
    label = ambiguous_name or f"code {code}"
    key = (
        "totalistic-unnamed-page81"
        if code is None
        else f"totalistic-code-{code}"
    )
    facts = deepcopy(TOTALISTIC_BASE)
    facts["object_kind"] = (
        f"Three-color totalistic cellular automaton {label} preset."
    )
    facts["rule_relation_constraint_function_or_probability_law"] = (
        (
            f"Decode ternary integer {code} in the chapter's seven-average "
            "case order and use those outputs as the totalistic lookup."
        )
        if code is not None
        else (
            "Use the three-color totalistic update represented by the middle "
            "page-81 evolution; the assigned source omits its code label."
        )
    )
    facts["result_kind"] = behavior
    facts["parameters_and_variants"] = (
        f"Rule identity is {label}; displayed runs use the single-gray-cell seed."
    )
    ambiguous = code is None
    spec = source_candidate(
        key,
        f"three-color totalistic cellular automaton {label} preset",
        anchor,
        facts,
        aliases=([label] if code is not None else ["middle page-81 totalistic example"]),
        not_applicable=NA_NO_CONTROL,
        missing=(
            "The rule code is absent from the assigned crop, so the exact seven outputs cannot be recovered."
            if ambiguous
            else "The off-picture boundary convention is not explicitly stated."
        ),
        claim=claim_override
        or (
            f"The source delimits {label} within the already-defined ternary "
            "totalistic code convention and records the stated behavior."
        ),
        image_path=image_path,
        strength=source_strength
        or ("DIRECT_PARTIAL_MECHANICS" if ambiguous else "DIRECT_COMPLETE_MECHANICS"),
        source_status=(["AMBIGUOUS"] if ambiguous else None),
        uncertainties=(
            ["The middle page-81 evolution is unambiguously delimited, but its code number is absent from the assigned image and surrounding units."]
            if ambiguous
            else None
        ),
    )
    return spec


def totalistic_survey(
    key: str,
    name: str,
    anchor: str,
    image_path: str,
    codes: list[int],
    result: str,
) -> CandidateSpec:
    facts = deepcopy(TOTALISTIC_BASE)
    facts.update(
        {
            "object_kind": f"A bounded survey of {len(codes)} code-identified three-color totalistic presets.",
            "result_kind": result,
            "parameters_and_variants": (
                "The survey members are exactly the visibly delimited codes "
                + ", ".join(str(code) for code in codes)
                + "."
            ),
        }
    )
    evidence_label = f"{key}-source"
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=NA_NO_CONTROL,
        missing="The visual code labels plus the established codec fix each rule; no finite-display boundary convention is stated.",
        claim="Original-resolution inspection confirms the complete bounded code-labeled preset survey.",
        image_path=image_path,
        variants=[
            (
                f"code {code}",
                f"The survey member identified by totalistic code {code}.",
                [evidence_label],
            )
            for code in codes
        ],
    )


tot_codes: dict[int, CandidateSpec] = {}
tot_codes[777] = totalistic_preset(
    777, "U000352", "The complete example evolution.", image_path=totalistic_code_image
)
totalistic_finite_survey = totalistic_survey(
    "totalistic-finite-periodic-survey",
    "finite/repetitive three-color totalistic preset survey",
    "U000359",
    "CHAPTERS/_page_77_Figure_6.jpeg",
    [600, 843, 870, 1086, 1167, 1329, 1572, 1815, 1842],
    "Nine displayed trajectories that attain finite size and then repeat.",
)
single_gray = source_candidate(
    "totalistic-single-gray-seed",
    "single-gray-cell totalistic cellular-automaton seed",
    "U000360",
    seed_facts(
        "one gray cell on an otherwise white line",
        "Three-color cell positions",
        "One gray/1 position and white/0 elsewhere",
        "A one-dimensional cell line",
    ),
    not_applicable=seed_na,
    missing="The exact origin coordinate and finite-display boundary are not stated.",
    claim="The caption explicitly fixes the initial condition used on the following totalistic examples.",
)
tot_codes[1329] = totalistic_preset(
    1329,
    "U000359",
    "A finite pattern with the reported maximum period of 78 steps.",
    image_path="CHAPTERS/_page_77_Figure_6.jpeg",
)
context_evidence(
    tot_codes[1329],
    "totalistic-code-1329-caption",
    "U000360",
    "The caption materially identifies code 1329 as the maximum-period-78 case.",
    strength="DIRECT_IDENTITY",
)
totalistic_forever_survey = totalistic_survey(
    "totalistic-forever-repetitive-survey",
    "forever-growing repetitive three-color totalistic preset survey",
    "U000361",
    "CHAPTERS/_page_78_Figure_2.jpeg",
    [219, 957, 966, 1884],
    "Four displayed forever-growing trajectories with fundamentally repetitive structure.",
)
tot_codes[420] = totalistic_preset(
    420,
    "U000363",
    "A nested pattern with a structure not seen in the elementary examples.",
    image_path="CHAPTERS/_page_78_Figure_4.jpeg",
)
context_evidence(
    tot_codes[420],
    "totalistic-code-420-caption",
    "U000364",
    "The following prose materially identifies code 420 as the uncommon nested structure.",
    strength="DIRECT_IDENTITY",
)
for _code in [237, 948, 1749]:
    tot_codes[_code] = totalistic_preset(
        _code,
        "U000363",
        "A named nested-pattern example.",
        image_path="CHAPTERS/_page_78_Figure_4.jpeg",
    )
    context_evidence(
        tot_codes[_code],
        f"totalistic-code-{_code}-caption",
        "U000367",
        f"The comparison prose explicitly identifies code {_code} as a nested example.",
        strength="DIRECT_IDENTITY",
    )
for _code in [177, 912, 2040]:
    tot_codes[_code] = totalistic_preset(
        _code,
        "U000365",
        "A displayed evolution with seemingly random features.",
        image_path="CHAPTERS/_page_79_Picture_2.jpeg",
    )
tot_codes[1041] = totalistic_preset(
    1041,
    "U000373",
    "A displayed complex evolution mixing regularity and irregularity.",
    image_path="CHAPTERS/_page_81_Picture_1.jpeg",
)
tot_codes[1635] = totalistic_preset(
    1635,
    "U000374",
    "A displayed complex evolution mixing regularity and irregularity.",
    image_path="CHAPTERS/_page_81_Picture_2.jpeg",
    source_strength="DEFECT_LIMITED",
    claim_override=(
        "The trajectory is intact, but its bottom-edge code label is clipped; "
        "the later continuation and explicit label establish code 1635."
    ),
)
tot_codes[1635]["source_status"] = ["CLEAR", "DEFECTIVE"]
tot_codes[1635]["uncertainties"].append(
    "The page-81 trajectory is intact but its code-1635 label is clipped; the later continuation and explicit label resolve the identity."
)
tot_codes[2049] = totalistic_preset(
    2049,
    "U000375",
    "A displayed complex evolution followed for 3000 steps.",
    image_path="CHAPTERS/_page_81_Picture_3.jpeg",
)
context_evidence(
    tot_codes[2049],
    "totalistic-code-2049-long-name",
    "U000380",
    "The later caption explicitly names the continued run as code 2049.",
    strength="DIRECT_IDENTITY",
)
context_evidence(
    tot_codes[2049],
    "totalistic-code-2049-long-image",
    "U000379",
    "Original-resolution inspection confirms the long continued trajectory.",
    image_path="CHAPTERS/_page_83_Picture_1.jpeg",
)
context_evidence(
    tot_codes[1635],
    "totalistic-code-1635-long-image",
    "U000377",
    "Original-resolution inspection confirms the 3000-step continuation of the middle page-81 trajectory.",
    image_path="CHAPTERS/_page_82_Picture_1.jpeg",
    strength="CORROBORATING",
)
context_evidence(
    tot_codes[1635],
    "totalistic-code-1635-name",
    "U000378",
    "The following source label identifies the long evolution as code 1635.",
    strength="DIRECT_IDENTITY",
)
tot_codes[1599] = totalistic_preset(
    1599,
    "U000383",
    "An edge-of-extinction run that resolves after 8282 steps.",
    image_path="CHAPTERS/_page_84_Picture_2.jpeg",
)
totalistic_growth_survey = totalistic_survey(
    "totalistic-growth-extinction-survey",
    "growth/extinction three-color totalistic preset survey",
    "U000383",
    "CHAPTERS/_page_84_Picture_2.jpeg",
    [357, 600, 1599, 2058],
    "Four displayed trajectories initially poised between growth and extinction.",
)
context_evidence(
    tot_codes[1599],
    "totalistic-code-1599-prose",
    "U000384",
    "The prose singles out code 1599 as the unresolved long-running case.",
    strength="DIRECT_IDENTITY",
)
context_evidence(
    tot_codes[1599],
    "totalistic-code-1599-long",
    "U000386",
    "Original-resolution inspection confirms the 9000-step evolution.",
    image_path="CHAPTERS/_page_85_Picture_2.jpeg",
)
context_evidence(
    tot_codes[1599],
    "totalistic-code-1599-caption",
    "U000387",
    "The caption fixes the single-gray seed, 9000-step display, and resolution after 8282 steps.",
)


def observer_facts(name: str, input_text: str, law: str, result: str) -> dict[str, str]:
    return {
        "object_kind": f"A deterministic observer/trajectory transform: {name}.",
        "native_time": "No independent native time; it filters or maps an input history.",
        "carrier": "An ordered trajectory of source-system states or events.",
        "support": "The time-indexed states of the input trajectory.",
        "alphabet_or_value_schema": "The input system's state/event schema.",
        "complete_state": "The complete input history prefix needed to decide retained events.",
        "input": input_text,
        "law_kind": "A deterministic selection or representation function.",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "successor_cardinality": "Exactly one transformed history for each input history.",
        "determinism_branching_or_measure": "Deterministic; it adds no branching or probability.",
        "termination_completion_failure": "Output ends when the supplied input history ends.",
        "witness_semantics": "Every retained item satisfies the observer's stated predicate.",
        "parameters_and_variants": "The source system and trajectory length are parameters.",
        "excluded_observers_and_representations": "This record is itself an observer, not a source-system transition law.",
        "evidence_limit": "It does not reconstruct states omitted by the filtering operation.",
    }


observer_na = {
    field: "A deterministic observer has no independent evolving state for this field."
    for field in [
        "topology",
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
    ]
}

totalistic_fate = source_candidate(
    "totalistic-fate-resolution-query",
    "totalistic growth/extinction fate and first-resolution query",
    "U000382",
    observer_facts(
        "totalistic growth/extinction fate and first-resolution",
        "A three-color totalistic cellular-automaton trajectory.",
        (
            "Determine whether the evolving pattern resolves to extinction or "
            "a simple repetitive form, and report the first step at which that "
            "resolution occurs; leave the result unresolved over the observed "
            "prefix when no such step has yet occurred."
        ),
        "A fate classification and, when witnessed, its first resolution step.",
    ),
    not_applicable=observer_na,
    missing="The prose does not formalize a machine-checkable predicate for when a fate first becomes visually clear.",
    claim="The passage explicitly asks when the displayed growth/extinction cases resolve and contrasts resolved and still-unresolved prefixes.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    totalistic_fate,
    "totalistic-fate-panel",
    "U000383",
    "The original-resolution panel supplies the four code-identified query inputs, including code 1599.",
    image_path="CHAPTERS/_page_84_Picture_2.jpeg",
    strength="CORROBORATING",
)
context_evidence(
    totalistic_fate,
    "totalistic-fate-panel-caption",
    "U000384",
    "The caption states the under-100-step resolution bound for all displayed cases except code 1599.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    totalistic_fate,
    "totalistic-fate-code1599",
    "U000387",
    "The caption reports code 1599 resolving after 8282 steps into 31 repetitive structures.",
    strength="DIRECT_PARTIAL_MECHANICS",
)


def add_route(
    key: str,
    unit: str,
    literal: str,
    topic: str,
    vocabulary: list[str],
    *,
    scope: str = "CROSS_RANGE",
    kind: str = "PAGE",
) -> None:
    ALL_ROUTES.append(
        {
            "key": key,
            "unit": unit,
            "literal": literal,
            "topic": topic,
            "vocabulary": vocabulary,
            "scope": scope,
            "kind": kind,
            "_insertion": len(ALL_ROUTES),
        }
    )


def bounded_trajectory_survey(
    key: str,
    name: str,
    anchor: str,
    base_facts: dict[str, str],
    image_path: str,
    members: list[tuple[str, str]],
    result: str,
    *,
    not_applicable: dict[str, str],
    missing: str,
    claim: str,
) -> CandidateSpec:
    facts = deepcopy(base_facts)
    facts.update(
        {
            "object_kind": f"A bounded survey of {len(members)} explicitly pictured presets.",
            "result_kind": result,
            "parameters_and_variants": (
                "The survey contains exactly "
                + ", ".join(member for member, _description in members)
                + "."
            ),
        }
    )
    evidence_label = f"{key}-source"
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=not_applicable,
        missing=missing,
        claim=claim,
        image_path=image_path,
        variants=[
            (member, description, [evidence_label])
            for member, description in members
        ],
    )


# Remaining construction families are declared below in canonical source order.

MOBILE_BASE = trajectory_facts(
    kind="A standard mobile automaton.",
    carrier="A binary cell line plus one distinguished active-cell position.",
    support="A one-dimensional line of cells.",
    topology="The active cell has immediate left and right neighbors.",
    invariants="Exactly one cell is active; the binary line support persists.",
    alphabet="Two cell colors plus an active-position marker.",
    state="All cell colors and the active-cell position.",
    seed="A binary line and one initial active-cell position.",
    frontier="Only the single active cell fires at a step.",
    schedule="One active-cell update and one left/right move per step.",
    read="The old colors of left neighbor, active cell, and right neighbor.",
    law_kind="A deterministic eight-case active-cell lookup.",
    law="For each three-color case, choose the active cell's new color and move direction left or right.",
    write="Update the source active cell's color and move the active marker one cell.",
    result="A new binary line and active-cell position.",
    variants="There are 65,536 standard rules; extended rules may also write neighbors.",
    excluded="Dots, stacked histories, and compressed record-extremum views are representations or observers.",
)
mobile = source_candidate(
    "mobile-family",
    "standard single-active-cell mobile automaton family",
    "U000390",
    MOBILE_BASE,
    aliases=["mobile automata"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source does not state the finite-display boundary convention.",
    claim="The section introduces mobile automata; the following passages fix one active cell, a three-cell read, source-color write, and left/right move.",
)
context_evidence(
    mobile,
    "mobile-family-mechanics",
    "U000392",
    "The passage states the active-cell read, write, and movement mechanics.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

mobile_case_f = source_candidate(
    "mobile-case-f",
    "standard mobile automaton survey case (f) preset",
    "U000393",
    {**MOBILE_BASE, "parameters_and_variants": "The complete eight-case rule pictured on page 86 and co-referred to as survey case (f)."},
    aliases=["page-86 mobile automaton example", "survey case (f)"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source does not assign a numeric rule code or finite boundary convention.",
    claim="The evolution is unambiguously paired with the adjacent complete eight-case rule and later identified as case (f).",
    image_path="CHAPTERS/_page_86_Picture_7.jpeg",
)
context_evidence(
    mobile_case_f,
    "mobile-case-f-rule",
    "U000394",
    "Original-resolution inspection confirms all eight rule cases.",
    image_path="CHAPTERS/_page_86_Picture_8.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    mobile_case_f,
    "mobile-case-f-coreference",
    "U000395",
    "The caption explicitly identifies this example with case (f) on the next page.",
    strength="DIRECT_IDENTITY",
)
context_evidence(
    mobile_case_f,
    "mobile-case-f-survey",
    "U000397",
    "The survey figure independently shows case (f), its evolution, and its rule.",
    image_path="CHAPTERS/_page_87_Figure_2.jpeg",
    strength="CORROBORATING",
)

mobile_survey = bounded_trajectory_survey(
    "mobile-eight-case-survey",
    "eight-case ordinary mobile-automaton preset survey",
    "U000397",
    MOBILE_BASE,
    "CHAPTERS/_page_87_Figure_2.jpeg",
    [
        ("case (a)", "A localized purely repetitive active-cell trajectory."),
        ("case (b)", "A localized purely repetitive active-cell trajectory."),
        ("case (c)", "A purely repetitive trajectory shifting systematically to the right."),
        ("case (d)", "A purely repetitive trajectory shifting systematically to the right."),
        ("case (e)", "A right-shifting repetitive trajectory that leaves stripes."),
        ("case (f)", "A right-shifting repetitive trajectory that leaves stripes."),
        ("case (g)", "A nonperiodic back-and-forth sweep with record-extreme growth."),
        ("case (h)", "A nonperiodic back-and-forth sweep with record-extreme growth."),
    ],
    "Eight complete rule/evolution panels spanning localized, drifting, striped, and record-sweeping behavior.",
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The cases have letter identities but no numeric rule codes or finite-display boundary convention.",
    claim="The original-resolution figure visibly delimits eight complete ordinary mobile-automaton rules and trajectories.",
)
context_evidence(
    mobile,
    "mobile-family-eight-case-survey",
    "U000397",
    "The eight-case original-resolution survey corroborates the finite standard rule-table shape.",
    image_path="CHAPTERS/_page_87_Figure_2.jpeg",
    strength="CORROBORATING",
)

record_extrema = source_candidate(
    "record-extremum-compression",
    "record-extremum head-position compression observer",
    "U000401",
    observer_facts(
        "record-extremum head-position compression",
        "A mobile-automaton or Turing-machine trajectory with a distinguished active/head position.",
        "Retain exactly those steps at which the distinguished position is farther left or farther right than at every earlier step.",
        "The subsequence of record-extremum states.",
    ),
    aliases=["compressed mobile automaton evolution", "compressed Turing machine evolution"],
    not_applicable=observer_na,
    missing="The observer does not define how to render intervals between retained events.",
    claim="The original-resolution image delimits the compressed histories of mobile cases (g) and (h).",
    image_path="CHAPTERS/_page_87_Picture_7.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    record_extrema,
    "record-extremum-mobile-definition",
    "U000402",
    "The caption explicitly defines compression by new left/right position records.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

EXT_MOBILE_BASE = deepcopy(MOBILE_BASE)
EXT_MOBILE_BASE.update(
    {
        "object_kind": "An extended neighbor-writing mobile automaton.",
        "structural_invariants": "Exactly one active cell persists while the binary line is locally rewritten.",
        "frontier_or_activation": "The active cell fires; its own cell and immediate neighbors form the writable region.",
        "law_kind": "A deterministic eight-case local rewrite-and-move lookup.",
        "rule_relation_constraint_function_or_probability_law": (
            "For each old left/self/right color case, choose new colors for all "
            "three cells and a left/right destination for the active marker."
        ),
        "write_replacement_assembly_or_commit": (
            "Atomically replace the active cell and both immediate-neighbor colors, then move the active marker."
        ),
        "parameters_and_variants": "The enlarged rule space contains 4,294,967,296 possible rules.",
    }
)
ext_mobile = source_candidate(
    "extended-mobile-family",
    "neighbor-writing mobile automaton family",
    "U000404",
    EXT_MOBILE_BASE,
    aliases=["extended mobile automata"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The finite-display boundary convention is not stated.",
    claim="The passage extends standard mobile rules so the active cell and both immediate neighbors can be updated.",
)


def mobile_extended_preset(
    key: str,
    name: str,
    anchor: str,
    image_path: str,
    behavior: str,
) -> CandidateSpec:
    facts = deepcopy(EXT_MOBILE_BASE)
    facts["object_kind"] = name
    facts["result_kind"] = behavior
    facts["parameters_and_variants"] = "The complete pictured eight-case extended rule fixes this preset."
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
        missing="No numeric rule code or finite boundary convention is stated.",
        claim="The original-resolution rule/evolution figure unambiguously delimits this extended mobile-automaton preset.",
        image_path=image_path,
    )


mobile_nested = mobile_extended_preset(
    "extended-mobile-nested",
    "nested-pattern extended mobile automaton preset",
    "U000406",
    "CHAPTERS/_page_88_Picture_5.jpeg",
    "A regular nested trajectory and its record-extremum compressed form.",
)
context_evidence(
    mobile_nested,
    "extended-mobile-nested-rule",
    "U000408",
    "The original-resolution rule asset supplies the complete lookup.",
    image_path="CHAPTERS/_page_88_Picture_8.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    mobile_nested,
    "extended-mobile-nested-compressed",
    "U000407",
    "The original-resolution compressed history supports the same nested preset.",
    image_path="CHAPTERS/_page_88_Picture_6.jpeg",
    strength="CORROBORATING",
)
mobile_random_color = mobile_extended_preset(
    "extended-mobile-random-color",
    "apparently-random-color extended mobile automaton preset",
    "U000410",
    "CHAPTERS/_page_89_Picture_3.jpeg",
    "A regular active-cell motion whose compressed color pattern appears random.",
)
context_evidence(
    mobile_random_color,
    "extended-mobile-random-color-rule",
    "U000411",
    "The original-resolution rule diagram fixes the lookup.",
    image_path="CHAPTERS/_page_89_Picture_3.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
for _label, _unit, _path in [
    ("extended-mobile-random-color-history", "U000412", "CHAPTERS/_page_89_Picture_5.jpeg"),
    ("extended-mobile-random-color-compressed", "U000413", "CHAPTERS/_page_89_Picture_6.jpeg"),
]:
    context_evidence(
        mobile_random_color,
        _label,
        _unit,
        "The original-resolution history is a co-referential view of the same extended mobile preset.",
        image_path=_path,
        strength="CORROBORATING",
    )
mobile_random_motion = mobile_extended_preset(
    "extended-mobile-random-motion",
    "apparently-random-active-motion extended mobile automaton preset",
    "U000415",
    "CHAPTERS/_page_90_Figure_2.jpeg",
    "An active-cell trajectory whose position appears random.",
)
context_evidence(
    mobile_random_motion,
    "extended-mobile-random-motion-rule",
    "U000418",
    "The original-resolution rule diagram fixes the lookup.",
    image_path="CHAPTERS/_page_90_Figure_4.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    mobile_random_motion,
    "extended-mobile-random-motion-history",
    "U000417",
    "The original-resolution ordinary history supports the same random-motion preset.",
    image_path="CHAPTERS/_page_90_Figure_3.jpeg",
    strength="CORROBORATING",
)

GENERAL_MOBILE_BASE = deepcopy(EXT_MOBILE_BASE)
GENERAL_MOBILE_BASE.update(
    {
        "object_kind": "A generalized multiple-active-cell mobile automaton.",
        "structural_invariants": "A binary line persists; the number of active cells may change.",
        "complete_state": "All cell colors and the set of active positions.",
        "frontier_or_activation": "Every currently active cell fires at the step.",
        "schedule": "Apply the rule to all currently active cells for the same step.",
        "rule_relation_constraint_function_or_probability_law": (
            "An active cell may move left/right, split into two active cells, or disappear, while applying the pictured local color rewrite."
        ),
        "write_replacement_assembly_or_commit": (
            "Commit the local color changes and the union of moved, split, or surviving active markers for the next state."
        ),
        "parameters_and_variants": "Rules vary in movement, splitting, disappearance, and color writes.",
    }
)
general_mobile = source_candidate(
    "generalized-mobile-family",
    "generalized multiple-active-cell mobile automaton family",
    "U000421",
    GENERAL_MOBILE_BASE,
    aliases=["generalized mobile automata"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source does not state conflict resolution when writable local regions overlap.",
    claim="The passage delimits multiple active cells and rules that move, split, or delete active cells.",
)
context_evidence(
    general_mobile,
    "generalized-mobile-worked-rule",
    "U000424",
    "The original-resolution worked rule corroborates generalized move/split mechanics.",
    image_path="CHAPTERS/_page_91_Figure_6.jpeg",
    strength="CORROBORATING",
)
general_split = source_candidate(
    "generalized-mobile-split-preset",
    "generalized mobile automaton splitting preset",
    "U000423",
    {**GENERAL_MOBILE_BASE, "object_kind": "The pictured generalized mobile-automaton splitting preset.", "result_kind": "A trajectory in which new active cells are created every few steps."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source does not state overlapping-write conflict semantics.",
    claim="The paired rule and evolution unambiguously delimit a generalized rule that sometimes splits one active cell into two.",
    image_path="CHAPTERS/_page_91_Figure_6.jpeg",
)
context_evidence(
    general_split,
    "generalized-mobile-split-evolution",
    "U000425",
    "Original-resolution inspection confirms the multiple-active-cell evolution.",
    image_path="CHAPTERS/_page_91_Figure_8.jpeg",
)
general_mobile_survey = bounded_trajectory_survey(
    "generalized-mobile-eight-case-survey",
    "eight-case generalized mobile-automaton preset survey",
    "U000429",
    GENERAL_MOBILE_BASE,
    "CHAPTERS/_page_92_Figure_1.jpeg",
    [
        (f"case ({letter})", description)
        for letter, description in [
            ("a", "A rule for which only finitely many cells become active."),
            ("b", "A rule with indefinitely proliferating active cells."),
            ("c", "A rule with indefinitely proliferating active cells."),
            ("d", "A rule with near-cellular-automaton activity."),
            ("e", "A rule with a complicated active-cell arrangement."),
            ("f", "A rule with a complicated active-cell arrangement."),
            ("g", "A rule with a complicated active-cell arrangement."),
            ("h", "A rule with a complicated active-cell arrangement."),
        ]
    ],
    "Eight complete generalized-mobile rule/evolution panels with differing active-cell proliferation.",
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source does not state conflict resolution for overlapping writable regions.",
    claim="The original-resolution figure visibly delimits all eight generalized-mobile rule tables and trajectories.",
)
context_evidence(
    general_mobile,
    "generalized-mobile-eight-case-survey",
    "U000429",
    "The original-resolution eight-case survey corroborates the generalized family mechanics.",
    image_path="CHAPTERS/_page_92_Figure_1.jpeg",
    strength="CORROBORATING",
)


TM_BASE = trajectory_facts(
    kind="A deterministic Turing machine.",
    carrier="A binary tape plus one head position and one head state.",
    support="A one-dimensional tape of cells.",
    topology="The head occupies one tape position and can move left or right.",
    invariants="Exactly one head persists; the tape support and color alphabet persist.",
    alphabet="Two tape colors; the head has a finite state set.",
    state="All tape colors, head position, and current head state.",
    seed="A tape configuration plus an initial head position and state.",
    frontier="Only the cell under the head is read and rewritten.",
    schedule="One read/write/state-transition/move action per step.",
    read="Current head state and color at the head position; neighboring colors are not read.",
    law_kind="A deterministic finite transition table.",
    law="Map each (head state, tape color) pair to a new color, new head state, and left/right move.",
    write="Write the selected color, change head state, and move one tape cell.",
    result="A new tape, head position, and head state.",
    variants="The chapter varies the finite number of head states while keeping two tape colors.",
    excluded="Arrow glyphs, stacked tape histories, and record-extremum compression are representations/observers.",
)
turing = source_candidate(
    "turing-family",
    "finite-state binary-tape Turing machine family",
    "U000432",
    TM_BASE,
    aliases=["Turing machines"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source does not explicitly state a halting state or finite boundary convention.",
    claim="The section and following mechanics passages delimit a tape, one multi-state head, and a transition depending only on head state and scanned color.",
)
context_evidence(
    turing,
    "turing-family-read",
    "U000434",
    "The passage explicitly excludes neighboring colors from the rule's read dependencies.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
turing_example = source_candidate(
    "turing-example",
    "page-93 Turing machine example preset",
    "U000435",
    {**TM_BASE, "object_kind": "The complete page-93 Turing-machine preset.", "parameters_and_variants": "The six pictured transition cases fix the preset."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="No numeric machine code, halting state, or finite boundary convention is stated.",
    claim="The paired original-resolution evolution and six-case rule delimit a complete Turing-machine preset.",
    image_path="CHAPTERS/_page_93_Picture_5.jpeg",
)
context_evidence(
    turing_example,
    "turing-example-rule",
    "U000436",
    "The original-resolution rule image supplies all pictured transition cases.",
    image_path="CHAPTERS/_page_93_Picture_6.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)


def tm_restriction(
    states: int,
    anchor: str,
    count: str,
    result: str,
    *,
    blank_tape_survey: bool,
) -> CandidateSpec:
    facts = deepcopy(TM_BASE)
    facts["object_kind"] = f"A {states}-head-state, two-tape-color Turing-machine restriction."
    facts["control_state"] = f"Exactly {states} possible head states."
    facts["parameters_and_variants"] = f"Head states={states}, tape colors=2; {count}."
    facts["result_kind"] = result
    if blank_tape_survey:
        facts["seed"] = "The reported survey starts from an all-white tape with the head in its first state."
    return source_candidate(
        f"turing-{states}-state",
        f"{states}-state two-color Turing machine family",
        anchor,
        facts,
        aliases=[f"{states}-state Turing machines"],
        not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
        missing=(
            "The source does not specify a halting state or finite boundary convention."
            if blank_tape_survey
            else "The source does not explicitly state a blank-tape survey condition, halting state, or finite boundary convention."
        ),
        claim=(
            f"The passage materially delimits the {states}-state/two-color rule space"
            + (" and its blank-tape behavior survey." if blank_tape_survey else ".")
        ),
    )


tm2 = tm_restriction(
    2,
    "U000439",
    "4096 possible rules",
    "Only repetitive or nested displayed behavior.",
    blank_tape_survey=False,
)
tm3 = tm_restriction(
    3,
    "U000443",
    "about three million possible rules",
    "Ultimately repetitive or nested behavior from an all-white tape in the reported survey.",
    blank_tape_survey=True,
)
tm4 = tm_restriction(
    4,
    "U000444",
    "a finite large rule space",
    "Some blank-tape presets yield apparently random behavior.",
    blank_tape_survey=True,
)
tm2_survey = bounded_trajectory_survey(
    "turing-two-state-six-case-survey",
    "six-case two-state/two-color Turing-machine preset survey",
    "U000440",
    {**TM_BASE, "control_state": "Exactly two possible head states."},
    "CHAPTERS/_page_94_Figure_1.jpeg",
    [
        (f"case ({letter})", "A complete two-state/two-color transition table and displayed trajectory.")
        for letter in "abcdef"
    ],
    "Six complete two-state/two-color transition-table and trajectory panels.",
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The cases have letter identities but no numeric machine codes, halting states, or explicit finite boundary convention.",
    claim="The original-resolution figure visibly delimits all six complete two-state/two-color Turing rules.",
)
context_evidence(
    tm2,
    "turing-two-state-survey",
    "U000440",
    "The original-resolution six-case rule survey corroborates the two-state restriction.",
    image_path="CHAPTERS/_page_94_Figure_1.jpeg",
    strength="CORROBORATING",
)
tm_mixed_survey = bounded_trajectory_survey(
    "turing-three-four-state-eight-case-survey",
    "eight-case three/four-state Turing-machine preset survey",
    "U000447",
    TM_BASE,
    "CHAPTERS/_page_95_Figure_2.jpeg",
    [
        ("case (a)", "A complete three-state/two-color blank-tape preset."),
        ("case (b)", "A complete three-state/two-color blank-tape preset."),
        ("case (c)", "A complete four-state/two-color blank-tape preset."),
        ("case (d)", "A complete four-state/two-color blank-tape preset."),
        ("case (e)", "A complete four-state/two-color blank-tape preset."),
        ("case (f)", "A complete four-state/two-color blank-tape preset."),
        ("case (g)", "A complete four-state/two-color blank-tape preset."),
        ("case (h)", "A complete four-state/two-color blank-tape preset."),
    ],
    "Eight complete transition-table panels run from a blank tape and first head state.",
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The cases have letter identities but no numeric machine codes, halting states, or finite boundary convention.",
    claim="The original-resolution figure visibly delimits all eight three/four-state transition tables and their trajectories.",
)
for _spec, _label in [
    (tm3, "turing-three-state-survey"),
    (tm4, "turing-four-state-survey"),
]:
    context_evidence(
        _spec,
        _label,
        "U000447",
        "The original-resolution eight-case survey corroborates this state-count restriction.",
        image_path="CHAPTERS/_page_95_Figure_2.jpeg",
        strength="CORROBORATING",
    )
blank_tm_seed = source_candidate(
    "turing-blank-seed",
    "blank-tape first-head-state Turing-machine seed",
    "U000447",
    {
        **seed_facts(
            "all tape cells white with the head in its first state",
            "Binary tape cells plus a head marker/state",
            "White at every tape cell; first head state",
            "A one-dimensional tape",
        ),
        "control_state": "The initial head is in the first state (up-arrow representation).",
    },
    not_applicable={k: v for k, v in seed_na.items() if k != "control_state"},
    missing="The exact initial tape coordinate is not stated.",
    claim="The original-resolution survey visibly delimits the common blank-tape/first-state start.",
    image_path="CHAPTERS/_page_95_Figure_2.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    blank_tm_seed,
    "turing-blank-seed-caption",
    "U000448",
    "The caption explicitly fixes the blank tape and first head state for the survey.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    record_extrema,
    "record-extremum-turing",
    "U000448",
    "The Turing-machine caption applies the same new-left/right-record filter to head positions.",
    strength="CORROBORATING",
)
tm_random = source_candidate(
    "turing-four-state-random-preset",
    "apparently-random four-state Turing machine preset",
    "U000449",
    {**TM_BASE, "object_kind": "The pictured four-state, two-color Turing-machine preset.", "control_state": "Four possible head states.", "seed": "A blank all-white tape with the head in its first state.", "result_kind": "An apparently random trajectory shown for 20,000 compressed steps.", "parameters_and_variants": "The complete eight-case transition table fixes this preset."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="No numeric machine code, halting state, or finite boundary convention is stated.",
    claim="The evolution, compressed view, and adjacent complete rule unambiguously delimit this four-state preset.",
    image_path="CHAPTERS/_page_96_Picture_2.jpeg",
)
context_evidence(
    tm_random,
    "turing-four-state-random-rule",
    "U000451",
    "The original-resolution rule image supplies the complete transition table.",
    image_path="CHAPTERS/_page_96_Picture_4.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    tm_random,
    "turing-four-state-random-compressed",
    "U000450",
    "The original-resolution compressed/continued trajectory is co-referential evidence for the same preset.",
    image_path="CHAPTERS/_page_96_Picture_3.jpeg",
    strength="CORROBORATING",
)


SUB_BASE = trajectory_facts(
    kind="A parallel neighbor-independent string substitution system.",
    carrier="A finite sequence of colored elements.",
    support="Ordered positions in a variable-length sequence.",
    topology="Sequence order; the basic rule reads one element independently.",
    invariants="Element order remains sequential while length may change.",
    alphabet="A finite element/color alphabet, initially illustrated with two colors.",
    state="The complete finite element sequence.",
    seed="A finite initial element sequence.",
    frontier="Every current element is replaced at every step.",
    schedule="All element replacements are evaluated in parallel.",
    read="Only the current element's color in the neighbor-independent family.",
    law_kind="A deterministic finite substitution table.",
    law="Map each element color to a fixed replacement block.",
    write="Concatenate replacement blocks in the old left-to-right element order.",
    result="A new finite sequence, possibly of different length.",
    variants="Replacement blocks, alphabet size, and initial sequence vary.",
    excluded="Subdivision boxes and branch trees are alternative representations of the same substitution trajectory.",
)
sub = source_candidate(
    "substitution-parallel-family",
    "parallel neighbor-independent substitution system family",
    "U000455",
    SUB_BASE,
    aliases=["neighbor-independent substitution systems"],
    not_applicable=NA_NO_CONTROL,
    missing="The source does not define behavior for an element color omitted from a rule table.",
    claim="The passage defines simultaneous replacement of every sequence element by a fixed block selected only by its color.",
)


def sub_preset(
    key: str,
    name: str,
    anchor: str,
    image_path: str,
    result: str,
) -> CandidateSpec:
    facts = deepcopy(SUB_BASE)
    facts["object_kind"] = name
    facts["result_kind"] = result
    facts["parameters_and_variants"] = "The two pictured replacement cases fix the preset."
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=NA_NO_CONTROL,
        missing="The source supplies the visual rule but not a separate textual symbol transcription.",
        claim="The original-resolution rule/evolution figure unambiguously delimits this substitution preset.",
        image_path=image_path,
    )


sub_thue = sub_preset(
    "substitution-thue-morse",
    "Thue-Morse/doubling substitution preset",
    "U000457",
    "CHAPTERS/_page_97_Picture_6.jpeg",
    "The element count doubles at every step and the subdivision view is identified as Thue-Morse case (b).",
)
context_evidence(
    sub_thue,
    "substitution-thue-morse-name",
    "U000463",
    "The later caption identifies subdivision rule (b) as the Thue-Morse sequence.",
    strength="DIRECT_IDENTITY",
)
sub_fib = sub_preset(
    "substitution-fibonacci",
    "Fibonacci-growth substitution preset",
    "U000458",
    "CHAPTERS/_page_97_Picture_7.jpeg",
    "Element counts follow a Fibonacci sequence and grow asymptotically by the golden ratio.",
)
context_evidence(
    sub_fib,
    "substitution-fibonacci-name",
    "U000463",
    "The later caption identifies subdivision rule (c) as Fibonacci-related.",
    strength="DIRECT_IDENTITY",
)
sub_cantor = sub_preset(
    "substitution-cantor",
    "Cantor-set substitution preset",
    "U000462",
    "CHAPTERS/_page_98_Figure_2.jpeg",
    "Subdivision case (d) yields a version of the Cantor set.",
)


def representation_candidate(
    key: str,
    name: str,
    anchor: str,
    input_text: str,
    law: str,
    result: str,
    *,
    image_path: str,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    facts = observer_facts(name, input_text, law, result)
    facts["object_kind"] = f"A deterministic representation transform: {name}."
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=observer_na,
        missing="The representation does not alter or recover the underlying native substitution law.",
        claim="The passage explicitly defines this alternative rendering of substitution evolution.",
        image_path=image_path,
        route_keys=route_keys,
    )


subdivision_rep = representation_candidate(
    "substitution-subdivision-representation",
    "substitution-system subdivision-box representation",
    "U000460",
    "A neighbor-independent substitution trajectory.",
    "Begin with one full-width box and draw each replacement as smaller sub-boxes within its predecessor.",
    "A nested fixed-width subdivision picture.",
    image_path="CHAPTERS/_page_98_Figure_2.jpeg",
)
tree_rep = representation_candidate(
    "substitution-tree-representation",
    "substitution-system branch-tree representation",
    "U000466",
    "A neighbor-independent substitution trajectory.",
    "Represent the initial element as a trunk and every replacement block as smaller child branches colored by element type.",
    "A rooted colored branch tree encoding the replacement genealogy.",
    image_path="CHAPTERS/_page_99_Picture_4.jpeg",
    route_keys=["trees-page400"],
)

NEIGHBOR_SUB_BASE = deepcopy(SUB_BASE)
NEIGHBOR_SUB_BASE.update(
    {
        "object_kind": "A right-neighbor-dependent substitution system.",
        "read_dependencies_or_neighborhood": "The current element and the element immediately to its right.",
        "rule_relation_constraint_function_or_probability_law": "Map each pictured (self,right-neighbor) color pair to a replacement block.",
        "write_replacement_assembly_or_commit": "Concatenate the chosen blocks; drop the rightmost element because no right-neighbor rule applies to it.",
        "parameters_and_variants": "Replacement blocks may be empty, enabling deletion as well as creation.",
    }
)
neighbor_sub = source_candidate(
    "substitution-right-neighbor-family",
    "right-neighbor-dependent substitution system family",
    "U000472",
    NEIGHBOR_SUB_BASE,
    aliases=["neighbor-dependent substitution systems"],
    not_applicable=NA_NO_CONTROL,
    missing="The source's right-edge drop is fixed, but no alternative boundary policy is specified.",
    claim="The passage defines replacement from self plus immediate-right color; the caption fixes dropping the rightmost element.",
)
for _idx, _name in [(1, "nested"), (2, "non-nested")]:
    _facts = deepcopy(NEIGHBOR_SUB_BASE)
    _facts["object_kind"] = f"The pictured right-neighbor substitution example {_idx}."
    _facts["result_kind"] = f"A {_name} displayed sequence trajectory."
    source_candidate(
        f"substitution-right-neighbor-example-{_idx}",
        f"right-neighbor substitution example {_idx} preset",
        "U000473",
        _facts,
        not_applicable=NA_NO_CONTROL,
        missing="The visual rule is clear but has no independent textual symbol transcription.",
        claim=f"The original-resolution page-100 figure delimits example {_idx} with a rule table and evolution.",
        image_path="CHAPTERS/_page_100_Picture_3.jpeg",
    )

DELETION_SUB_BASE = deepcopy(NEIGHBOR_SUB_BASE)
DELETION_SUB_BASE.update(
    {
        "object_kind": "A creation-and-deletion substitution system.",
        "rule_relation_constraint_function_or_probability_law": "A neighbor-dependent replacement table may map some cases to an empty block.",
        "write_replacement_assembly_or_commit": "Concatenate nonempty blocks and omit elements whose selected replacement is empty.",
        "result_kind": "A variable-length sequence that may grow, shrink, stabilize, or become empty.",
    }
)
deletion_sub = source_candidate(
    "substitution-deletion-family",
    "creation-and-deletion substitution system family",
    "U000477",
    DELETION_SUB_BASE,
    not_applicable=NA_NO_CONTROL,
    missing="The source does not give a general classification of extinction/termination.",
    claim="The passage materially extends substitution rules to permit empty replacements and hence disappearing elements.",
)
balanced_sub = source_candidate(
    "substitution-balanced-growth-preset",
    "balanced creation/deletion substitution preset",
    "U000479",
    {**DELETION_SUB_BASE, "object_kind": "The pictured balanced creation/deletion substitution preset.", "result_kind": "A repetitive trajectory whose length grows by a fixed amount per step.", "parameters_and_variants": "The pictured rule table fixes the preset; fixed-width and rescaled-width views are observers."},
    not_applicable=NA_NO_CONTROL,
    missing="No independent textual symbol transcription of the visual rule is supplied.",
    claim="The paired original-resolution views and rule unambiguously delimit a slowly growing creation/deletion preset.",
    image_path="CHAPTERS/_page_101_Picture_4.jpeg",
)
context_evidence(
    balanced_sub,
    "substitution-balanced-rule",
    "U000480",
    "The original-resolution asset shows the preset's rule table.",
    image_path="CHAPTERS/_page_101_Picture_5.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
multicolor_sub = source_candidate(
    "substitution-multicolor-slow-growth",
    "three/four-color slow-growth substitution family",
    "U000484",
    {**DELETION_SUB_BASE, "object_kind": "A three- or four-color creation/deletion substitution family.", "alphabet_or_value_schema": "Three or four element colors.", "result_kind": "Slow-growth trajectories including repetitive, nested, grid-like, and apparently random examples.", "parameters_and_variants": "Alphabet size is three or four; the survey contains six explicit rules (a)--(f)."},
    not_applicable=NA_NO_CONTROL,
    missing="The prose does not transcribe the six visual rule tables into symbols.",
    claim="The passage and facing rule/evolution survey delimit the multicolor slow-growth extension.",
)
context_evidence(
    multicolor_sub,
    "substitution-multicolor-rules",
    "U000486",
    "Original-resolution inspection confirms six separate visual rule tables.",
    image_path="CHAPTERS/_page_102_Figure_4.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)


SEQ_BASE = trajectory_facts(
    kind="A sequential ordered string-substitution system.",
    carrier="A finite string over a finite alphabet.",
    support="Ordered character positions in a variable-length string.",
    topology="Left-to-right string order.",
    invariants="The state remains a finite string while length may change.",
    alphabet="A finite symbol alphabet, illustrated with A and B.",
    state="The complete current string.",
    seed="A finite initial string.",
    frontier="The first leftmost occurrence accepted by the ordered replacement scan.",
    schedule="At each step scan left-to-right; with multiple rules, try them in order on successive full scans and stop at the first applicable rule.",
    read="Candidate substrings matching the left side of a replacement.",
    law_kind="A deterministic ordered first-match replacement list.",
    law="Find the first leftmost match for the first applicable replacement and replace that one occurrence.",
    write="Splice the replacement right-hand string into the matched interval.",
    result="One new finite string.",
    variants="Alphabet, ordered replacement list, and initial string vary.",
    excluded="Black dots, square encodings, stacked histories, and record-length compression are representations/observers.",
)
sequential = source_candidate(
    "sequential-substitution-family",
    "sequential ordered first-match substitution family",
    "U000494",
    SEQ_BASE,
    aliases=["sequential substitution systems", "text-editor search-and-replace model"],
    not_applicable=NA_NO_CONTROL,
    missing="Failure behavior when no replacement applies is not explicitly stated.",
    claim="The passage defines a left-to-right first-occurrence replacement; following context defines ordered multiple-rule scans.",
)


def seq_preset(key: str, name: str, anchor: str, law: str, seed: str, image: str) -> CandidateSpec:
    facts = deepcopy(SEQ_BASE)
    facts["object_kind"] = name
    facts["rule_relation_constraint_function_or_probability_law"] = law
    facts["seed"] = seed
    facts["parameters_and_variants"] = "The stated ordered replacement list and seed fix the preset."
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=NA_NO_CONTROL,
        missing="The source does not state an explicit no-match terminal marker.",
        claim="The passage and original-resolution figure state the ordered replacements, initial string, and first-match schedule.",
        image_path=image,
    )


seq_ba = seq_preset(
    "sequential-ba-aba",
    "BA-to-ABA sequential substitution preset",
    "U000495",
    "Replace the first leftmost BA by ABA.",
    "BABA",
    "CHAPTERS/_page_104_Picture_3.jpeg",
)
seq_two = seq_preset(
    "sequential-two-rule",
    "ordered two-replacement sequential substitution preset",
    "U000499",
    "Try ABA→AAB first; if unavailable on the scan, try A→ABA.",
    "The initial string shown in the page-105 evolution.",
    "CHAPTERS/_page_105_Figure_4.jpeg",
)
seq_three = source_candidate(
    "sequential-three-rule-survey",
    "three-replacement sequential substitution survey family",
    "U000505",
    {**SEQ_BASE, "object_kind": "The eight explicitly pictured three-replacement sequential-substitution presets.", "seed": "BAB for every survey case.", "parameters_and_variants": "Eight ordered three-replacement lists (a)--(h), all run from BAB."},
    not_applicable=NA_NO_CONTROL,
    missing="The visual rule glyphs are not independently transcribed into prose.",
    claim="The survey and caption delimit eight ordered three-rule presets with common seed BAB.",
)
context_evidence(
    seq_three,
    "sequential-three-rule-tables",
    "U000509",
    "Original-resolution inspection confirms the eight ordered replacement tables.",
    image_path="CHAPTERS/_page_106_Figure_4.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)
seq_random = source_candidate(
    "sequential-three-rule-g",
    "apparently-random sequential substitution case (g) preset",
    "U000511",
    {**SEQ_BASE, "object_kind": "Sequential-substitution survey case (g).", "seed": "BAB.", "result_kind": "An apparently random variable-length string trajectory.", "parameters_and_variants": "The rule is explicitly co-referred to case (g) of the preceding eight-rule survey."},
    not_applicable=NA_NO_CONTROL,
    missing="The rule must be read from the preceding visual table; no prose symbol transcription is supplied.",
    claim="The multi-panel run is explicitly identified as preceding survey case (g).",
    image_path="CHAPTERS/_page_107_Picture_2.jpeg",
)
context_evidence(
    seq_random,
    "sequential-three-rule-g-rule",
    "U000514",
    "The small original-resolution rule panel corroborates the selected case.",
    image_path="CHAPTERS/_page_107_Picture_5.jpeg",
    strength="CORROBORATING",
)
record_length = source_candidate(
    "record-length-compression",
    "record-string-length compression observer",
    "U000515",
    observer_facts(
        "record-string-length compression",
        "A variable-length sequential-substitution trajectory.",
        "Retain exactly those steps at which the current string is longer than every earlier string.",
        "The subsequence of record-long strings.",
    ),
    not_applicable=observer_na,
    missing="The observer does not reconstruct omitted strings.",
    claim="The caption explicitly defines the million-step compressed picture by new length records.",
)


TAG_BASE = trajectory_facts(
    kind="A tag system.",
    carrier="A finite sequence of colored elements.",
    support="Ordered positions in a variable-length sequence.",
    topology="A distinguished beginning and end of the sequence.",
    invariants="The state remains an ordered finite sequence until it can become empty.",
    alphabet="A finite color alphabet, illustrated as black/white.",
    state="The complete current sequence.",
    seed="A finite initial sequence.",
    frontier="A fixed-size prefix is consumed each step.",
    schedule="One prefix deletion followed by one suffix append per step.",
    read="The fixed number of elements removed from the beginning.",
    law_kind="A deterministic prefix-conditioned append table.",
    law="Delete d leading elements and append the block selected by their colors.",
    write="Remove the prefix and concatenate the selected block at the end.",
    result="A new finite sequence, which may be empty.",
    variants="Deletion number d, append blocks, color alphabet, and seed vary.",
    excluded="Stacked sequence pictures and length plots are representations/observers.",
)
tag = source_candidate(
    "tag-family",
    "fixed-prefix-deletion tag system family",
    "U000517",
    TAG_BASE,
    aliases=["tag systems"],
    not_applicable=NA_NO_CONTROL,
    missing="The source does not explicitly state behavior when fewer than d elements remain.",
    claim="The passage defines fixed prefix deletion and an append block chosen from the removed colors.",
)
tag1 = source_candidate(
    "tag-delete-one",
    "one-deletion tag system restriction",
    "U000519",
    {**TAG_BASE, "object_kind": "A tag system with deletion number one.", "read_dependencies_or_neighborhood": "The one element removed from the beginning.", "parameters_and_variants": "Deletion number d=1; four pictured append-table examples.", "result_kind": "A slowed trajectory operationally corresponding after full cycles to neighbor-independent substitution."},
    not_applicable=NA_NO_CONTROL,
    missing="The exact phase mapping to each page-83 substitution example is routed rather than resolved by this worker.",
    claim="The passage materially restricts deletion to one and the captions state the cycle-by-cycle substitution correspondence.",
    route_keys=["tag1-page83-a", "tag1-page83-b"],
)
tag2 = source_candidate(
    "tag-delete-two",
    "two-deletion tag system restriction",
    "U000526",
    {**TAG_BASE, "object_kind": "A tag system with deletion number two.", "read_dependencies_or_neighborhood": "The two elements removed from the beginning.", "seed": "A pair of black elements in the six displayed examples.", "parameters_and_variants": "Deletion number d=2; six pictured append-table examples.", "result_kind": "Variable-length trajectories including one that eventually becomes empty."},
    not_applicable=NA_NO_CONTROL,
    missing="Behavior when a nonempty sequence has fewer than two elements is not explicitly stated.",
    claim="The passage and following figure delimit deletion number two, six rules, and the common black-pair seed.",
)
context_evidence(
    tag2,
    "tag-delete-two-figure",
    "U000527",
    "Original-resolution inspection confirms the rule diagrams, trajectories, and length plots.",
    image_path="CHAPTERS/_page_109_Figure_2.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)


CYCLIC_BASE = trajectory_facts(
    kind="A cyclic tag system.",
    carrier="A finite binary sequence plus a cyclic append-block phase.",
    support="An ordered variable-length sequence and a finite cyclic rule list.",
    topology="A distinguished sequence beginning/end and cyclic rule index.",
    invariants="Exactly one rule phase advances per step; the data sequence may change length.",
    alphabet="Black/white data elements and a finite list of append blocks.",
    state="The current data sequence and current position in the cyclic block list.",
    seed="A finite initial sequence and initial rule phase.",
    frontier="The first data element is consumed.",
    schedule="Delete one element, conditionally append the current block, then advance the cyclic phase.",
    read="The removed first element and current cyclic block.",
    law_kind="A deterministic cyclic conditional-append law.",
    law="If the removed element is black append the current block; if white append nothing; advance to the next block cyclically.",
    write="Remove the first element, append conditionally, and advance rule phase.",
    result="A new sequence and cyclic phase.",
    variants="The cyclic block list and initial sequence vary.",
    excluded="Stacked histories and growth-fluctuation plots are representations/observers.",
)
cyclic = source_candidate(
    "cyclic-tag-family",
    "cyclic conditional-append tag system family",
    "U000530",
    CYCLIC_BASE,
    aliases=["cyclic tag systems"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="Behavior after the data sequence becomes empty is not explicitly stated.",
    claim="The section defines a predetermined cyclic append-block schedule; following passages fix deletion, black conditioning, and phase advance.",
)
cyclic_example = source_candidate(
    "cyclic-tag-two-block-example",
    "two-block alternating cyclic tag preset",
    "U000531",
    {**CYCLIC_BASE, "object_kind": "The pictured two-block alternating cyclic tag preset.", "parameters_and_variants": "Exactly two pictured blocks alternate; the pictured seed fixes the run."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The source supplies a visual rather than textual block transcription.",
    claim="The paired evolution, two-case rule, and summary block list delimit this preset.",
    image_path="CHAPTERS/_page_110_Picture_4.jpeg",
)
context_evidence(
    cyclic_example,
    "cyclic-tag-two-block-rule",
    "U000533",
    "Original-resolution inspection confirms the two alternating cases.",
    image_path="CHAPTERS/_page_110_Picture_5.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
cyclic_seed = source_candidate(
    "cyclic-tag-single-black-seed",
    "single-black-element cyclic-tag seed",
    "U000539",
    seed_facts(
        "one black element",
        "A finite binary sequence plus cyclic phase",
        "A length-one black sequence",
        "An ordered sequence",
    ),
    not_applicable=seed_na,
    missing="The initial cyclic phase is supplied by each pictured rule but not restated in prose.",
    claim="The caption explicitly fixes a single black initial element for all five examples.",
    route_keys=["cyclic-page83"],
)
for _case in ["d", "e"]:
    source_candidate(
        f"cyclic-tag-case-{_case}",
        f"cyclic tag survey case ({_case}) preset",
        "U000538",
        {**CYCLIC_BASE, "object_kind": f"The pictured cyclic-tag case ({_case}) preset.", "seed": "A single black element.", "result_kind": "A sequence whose average growth has apparently random fluctuations.", "parameters_and_variants": f"The visual block list labeled ({_case}) fixes the preset."},
        not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
        missing="The block list is visual and has no independent symbol transcription.",
        claim=f"The original-resolution survey unambiguously delimits cyclic-tag case ({_case}) and its rule blocks.",
        image_path="CHAPTERS/_page_111_Figure_1.jpeg",
    )


REGISTER_BASE = trajectory_facts(
    kind="A two-register increment/decrement-jump machine.",
    carrier="Two unbounded nonnegative integer registers plus a finite instruction pointer.",
    support="A fixed finite ordered program and two registers.",
    topology="Sequential instruction order with explicit jump targets.",
    invariants="Register values remain nonnegative; the program is fixed.",
    alphabet="Nonnegative integers and two instruction kinds.",
    state="Both register values and the current instruction index.",
    seed="Initial register values and the first instruction.",
    frontier="The current instruction fires.",
    schedule="Execute exactly one current instruction per step.",
    read="The current instruction and, for decrement-jump, the addressed register's zero/nonzero status.",
    law_kind="A deterministic instruction interpreter.",
    law="Increment adds one and advances; decrement-jump on positive subtracts one and jumps, while on zero leaves the register unchanged and advances.",
    write="Update the addressed register and set the next instruction pointer.",
    result="New register values and instruction pointer.",
    variants="Program length, instruction sequence, jump targets, and register count/instruction set may vary.",
    excluded="Block bars, dots, logarithmic views, zero-event compression, and derived arithmetic subsequences are observers/representations.",
)
register = source_candidate(
    "register-machine-family",
    "two-register increment/decrement-jump machine family",
    "U000543",
    REGISTER_BASE,
    aliases=["register machines"],
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The behavior after falling off a program without an explicit jump is not separately formalized.",
    claim="The passage and following instruction definitions delimit two nonnegative registers, increment, and conditional decrement-jump execution.",
)
register_seed = source_candidate(
    "register-zero-seed",
    "zero-register first-instruction register-machine seed",
    "U000552",
    {
        **seed_facts(
            "both registers zero and instruction pointer at the first program instruction",
            "Two nonnegative registers plus instruction pointer",
            "Register values (0,0) and first instruction",
            "A fixed finite program",
        ),
        "control_state": "The instruction pointer starts at the first instruction.",
    },
    not_applicable={k: v for k, v in seed_na.items() if k != "control_state"},
    missing="The seed is tied to each pictured program; no standalone program is selected.",
    claim="The passages explicitly state first-instruction execution and both registers initially zero.",
)
register_short = source_candidate(
    "register-four-or-fewer-restriction",
    "register-machine programs of length at most four restriction",
    "U000554",
    {**REGISTER_BASE, "object_kind": "The finite restriction to two-register programs of four or fewer instructions.", "parameters_and_variants": "Program length ≤4, comprising 10,552 possible machines.", "result_kind": "The reported exhaustive survey yields only repetitive behavior."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The precise program enumeration convention is not stated in prose.",
    claim="The passage delimits and reports exhaustive coverage of the ≤4-instruction program space.",
)
register5 = source_candidate(
    "register-five-instruction-preset",
    "five-instruction nested register-machine preset",
    "U000555",
    {**REGISTER_BASE, "object_kind": "The pictured five-instruction register-machine preset.", "result_kind": "A regular nested register trajectory.", "parameters_and_variants": "A complete five-instruction visual program, one of two register-swapped cases among 248,832."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The visual program is not independently transcribed into text.",
    claim="The passage and original-resolution program/evolution figure delimit the five-instruction preset.",
    image_path="CHAPTERS/_page_114_Picture_5.jpeg",
)
register8 = source_candidate(
    "register-eight-instruction-preset",
    "eight-instruction complex register-machine preset",
    "U000558",
    {**REGISTER_BASE, "object_kind": "The pictured eight-instruction register-machine preset.", "result_kind": "A trajectory with apparently random zero-event subsequences.", "parameters_and_variants": "A complete eight-instruction visual program, one of 126 complex cases among 11,019,960,576."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The visual program is not independently transcribed into prose.",
    claim="The passage and original-resolution four-panel figure delimit the eight-instruction preset.",
)
context_evidence(
    register8,
    "register-eight-instruction-figure",
    "U000559",
    "Original-resolution inspection confirms the program, evolution, zero-event view, trace, and digit subsequence.",
    image_path="CHAPTERS/_page_115_Figure_1.jpeg",
    strength="DIRECT_COMPLETE_MECHANICS",
)
zero_observer = source_candidate(
    "register-zero-event-compression",
    "register zero-event compression observer",
    "U000560",
    observer_facts(
        "register zero-event compression",
        "A two-register-machine trajectory.",
        "Retain only steps at which either register has just decreased to zero; optional subviews select which register hit zero and show the other value/instruction.",
        "A zero-event state/instruction subsequence and derived register-value sequence.",
    ),
    not_applicable=observer_na,
    missing="Logarithmic and binary renderings are separate display choices.",
    claim="The caption explicitly defines all retained zero events and the two derived subviews.",
    route_keys=["register-page122"],
)

map_facts = {
    "object_kind": "A deterministic piecewise arithmetic function iterated on positive integers.",
    "native_time": "Discrete function iteration.",
    "carrier": "Positive integers.",
    "support": "One integer value at each iteration.",
    "alphabet_or_value_schema": "Positive integer n.",
    "complete_state": "The current integer n.",
    "seed": "n=1.",
    "frontier_or_activation": "The single current integer is evaluated.",
    "schedule": "Apply the piecewise function once per iteration.",
    "read_dependencies_or_neighborhood": "The value n and its parity.",
    "law_kind": "A deterministic piecewise arithmetic function.",
    "rule_relation_constraint_function_or_probability_law": "n↦3n/2 when n is even; n↦(3n+1)/2 when n is odd.",
    "write_replacement_assembly_or_commit": "Replace n by the selected arithmetic result.",
    "result_kind": "The next positive integer and its iterated sequence.",
    "successor_cardinality": "Exactly one successor per positive integer.",
    "determinism_branching_or_measure": "Deterministic.",
    "termination_completion_failure": "No terminal case is specified.",
    "witness_semantics": "Each adjacent pair obeys the parity-selected formula.",
    "parameters_and_variants": "Initial condition n=1 in the stated sequence.",
    "excluded_observers_and_representations": "Binary digit display and its register-machine derivation are not extra state.",
    "evidence_limit": "The page-122 route may provide derivation/context but the function itself is explicit here.",
}
arith_map = source_candidate(
    "register-derived-piecewise-map",
    "register-derived 3n/2 versus (3n+1)/2 map",
    "U000560",
    map_facts,
    aliases=["successive second-register zero-event value map"],
    not_applicable={"control_state": NA_NO_CONTROL["control_state"], "boundary": "An integer function has no spatial boundary.", "external_data": NA_NO_CONTROL["external_data"], "input": "The initial value is represented by the seed field."},
    missing="The in-scope passage does not derive why the register-machine subsequence obeys this map.",
    claim="The caption states the complete parity-conditioned function and initial value n=1.",
    route_keys=["register-page122"],
)
register3 = source_candidate(
    "register-three-register-variant",
    "three-register register-machine variant",
    "U000565",
    {**REGISTER_BASE, "object_kind": "A three-register variant of the register-machine family.", "carrier": "Three unbounded nonnegative integer registers plus instruction pointer.", "complete_state": "Three register values and current instruction.", "parameters_and_variants": "Three registers; random-looking behavior occurs with a seven-instruction program."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="The seven-instruction example program is not supplied in this passage.",
    claim="The passage materially delimits the three-register extension and its reduced seven-instruction threshold example.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
register_extended = source_candidate(
    "register-extended-instruction-variant",
    "multi-register arithmetic/comparison instruction-set variant",
    "U000566",
    {**REGISTER_BASE, "object_kind": "A register-machine variant with instructions that jointly reference two registers.", "read_dependencies_or_neighborhood": "One or two addressed registers depending on instruction.", "rule_relation_constraint_function_or_probability_law": "In addition to increment/decrement-jump, instructions may add, subtract, or compare register contents.", "parameters_and_variants": "Instruction set and number of addressed registers vary."},
    not_applicable={"external_data": NA_NO_CONTROL["external_data"]},
    missing="Exact operand, branch, overflow, and comparison-result semantics are not supplied.",
    claim="The passage explicitly delimits a broader instruction family but only partially specifies its operations.",
    strength="DIRECT_PARTIAL_MECHANICS",
)


SYMBOLIC_BASE = trajectory_facts(
    kind="A symbolic expression rewrite system.",
    carrier="Nested application expressions built from symbol e.",
    support="The rooted ordered syntax tree / bracket structure of the expression.",
    topology="Nested application structure with left-to-right textual order.",
    invariants="Every state remains a well-formed symbolic expression.",
    alphabet="Symbol e, brackets/application, and pattern variables.",
    state="The complete current symbolic expression.",
    seed="A finite initial expression.",
    frontier="All non-overlapping left-to-right matches selected during one scan.",
    schedule="Scan once left-to-right per step and apply wherever possible without overlap.",
    read="Subexpressions matching the left-hand pattern and its bound pattern variables.",
    law_kind="A deterministic symbolic pattern-rewrite rule.",
    law="Match the left pattern, bind its expression variables, and instantiate the right expression.",
    write="Replace every selected non-overlapping match in the scan by its instantiated right side.",
    result="A new well-formed symbolic expression.",
    variants="Rewrite rule and initial expression vary.",
    excluded="Bracket-square encodings, truncation, expression-size plots, and Mathematica syntax are representations/implementation context.",
)
symbolic = source_candidate(
    "symbolic-family",
    "left-to-right non-overlapping symbolic rewrite family",
    "U000571",
    SYMBOLIC_BASE,
    aliases=["symbolic systems", "combinator-like expression systems"],
    not_applicable=NA_NO_CONTROL,
    missing="Tie behavior for structurally simultaneous nested matches beyond the stated scan/non-overlap policy is not elaborated.",
    claim="The passage and following scan rule delimit expressions, pattern variables, and repeated non-overlapping left-to-right rewriting.",
)
symbolic_main = source_candidate(
    "symbolic-main-preset",
    "e[x][y] to x[x[y]] symbolic rewrite preset",
    "U000571",
    {**SYMBOLIC_BASE, "object_kind": "The symbolic rewrite preset e[x_][y_]→x[x[y]].", "seed": "e[e[e][e]][e][e] in the displayed main run.", "rule_relation_constraint_function_or_probability_law": "e[x_][y_]→x[x[y]], with x_ and y_ matching arbitrary expressions.", "result_kind": "A deterministic expression trajectory that eventually reaches a fixed expression for the discussed inputs.", "parameters_and_variants": "Rule fixed as stated; initial expression varies."},
    aliases=["expression /. rule example"],
    not_applicable=NA_NO_CONTROL,
    missing="The source states stabilization empirically but does not define a separate proof certificate.",
    claim="The passage explicitly states the rule, variable denotation, and sample initial expression.",
)
context_evidence(
    symbolic_main,
    "symbolic-main-evolution",
    "U000573",
    "Original-resolution inspection confirms the matched boxed regions and successive expressions.",
    image_path="CHAPTERS/_page_117_Figure_5.jpeg",
    strength="CORROBORATING",
)
bracket_rep = representation_candidate(
    "symbolic-bracket-square-representation",
    "symbolic opening/closing-bracket square encoding",
    "U000575",
    "A symbolic expression or expression trajectory.",
    "Encode each opening bracket by a dark square and each closing bracket by a light square, preserving bracket order.",
    "A binary square sequence/picture of expression bracket structure.",
    image_path="CHAPTERS/_page_118_Picture_3.jpeg",
)
symbolic_survey = source_candidate(
    "symbolic-six-rule-survey",
    "six-rule symbolic-system survey",
    "U000582",
    {**SYMBOLIC_BASE, "object_kind": "Six explicitly pictured symbolic rewrite presets.", "seed": "e[e[e][e]][e][e] for every survey rule.", "parameters_and_variants": "Six separate visual rewrite rules with a common seed.", "result_kind": "Repetitive, nested, nonstabilizing, and apparently random expression trajectories with size-change plots."},
    not_applicable=NA_NO_CONTROL,
    missing="Some fine rule glyphs are too small to transcribe safely without a dedicated symbolic check; the six presets remain separately visible within the figure.",
    claim="The passage and original-resolution figure delimit six rule/trajectory cases with a common initial expression.",
)
context_evidence(
    symbolic_survey,
    "symbolic-six-rule-figure",
    "U000583",
    "Original-resolution inspection confirms six distinct rule panels and their size-difference plots.",
    image_path="CHAPTERS/_page_119_Figure_3.jpeg",
    strength="DIRECT_PARTIAL_MECHANICS",
)


K_TOTALISTIC = deepcopy(TOTALISTIC_BASE)
K_TOTALISTIC.update(
    {
        "object_kind": "A k-color radius-one totalistic cellular-automaton family.",
        "alphabet_or_value_schema": "k ordered colors represented by integer values 0 through k-1.",
        "read_dependencies_or_neighborhood": "The sum/average of left, self, and right old color values.",
        "rule_relation_constraint_function_or_probability_law": "Choose one of k outputs for each of 3(k-1)+1 possible neighborhood sums.",
        "parameters_and_variants": "k varies; the chapter compares k=2,3,4,5 and states 16, 2187, and 1,220,703,125 rule counts for k=2,3,5.",
    }
)
k_totalistic = source_candidate(
    "k-color-totalistic-family",
    "k-color totalistic cellular automaton family",
    "U000602",
    K_TOTALISTIC,
    aliases=["totalistic rules with varying numbers of colors"],
    not_applicable=NA_NO_CONTROL,
    missing="The source routes the base totalistic definition to page 60 and does not state every general-k code convention here.",
    claim="The caption materially parameterizes totalistic cellular automata by color count and number of sum cases.",
    route_keys=["totalistic-page60"],
)

eca_symmetric = source_candidate(
    "eca-symmetric-blank-preserving",
    "left-right-symmetric blank-preserving elementary-rule restriction",
    "U000630",
    {**ECA_BASE, "object_kind": "The restriction of elementary rules to left-right symmetry and a blank-background fixed point.", "parameters_and_variants": "Exactly 32 elementary rules satisfy both stated restrictions."},
    not_applicable=NA_NO_CONTROL,
    missing="The 32 rule numbers are not enumerated in this passage.",
    claim="The historical-method passage explicitly delimits the conjunction of left-right symmetry and blank-background preservation as a 32-rule set.",
)
random_seed = source_candidate(
    "eca-random-initial-condition",
    "random cellular-automaton initial-condition ensemble",
    "U000631",
    {
        "object_kind": "A random initial-condition ensemble for cellular-automaton experiments.",
        "native_time": "No native time; the object is a probability-valued seed generator.",
        "carrier": "Binary cell configurations.",
        "support": "A one-dimensional cell line.",
        "alphabet_or_value_schema": "Black/white cell values.",
        "complete_state": "A sampled complete initial row.",
        "seed": "A random binary initial condition.",
        "law_kind": "A probability law over initial configurations.",
        "rule_relation_constraint_function_or_probability_law": "Sample the initial cell colors randomly; the exact distribution is not stated.",
        "result_kind": "A random initial cellular-automaton state.",
        "successor_cardinality": "Many possible seeds with an unspecified measure.",
        "determinism_branching_or_measure": "Measure-valued/random.",
        "parameters_and_variants": "Distribution, finite extent, and random seed are unstated parameters.",
        "excluded_observers_and_representations": "Subsequent automaton evolution is not part of the seed generator.",
        "evidence_limit": "The Bernoulli parameter, independence, support extent, and boundary are not stated.",
    },
    aliases=["random initial conditions"],
    not_applicable={
        "visible_history": "A seed ensemble does not itself have an evolution history.",
        "control_state": NA_NO_CONTROL["control_state"],
        "input": "The ensemble produces inputs rather than consuming one.",
        "boundary": "The source does not define a finite boundary; this is recorded as an evidence limit.",
        "external_data": NA_NO_CONTROL["external_data"],
        "frontier_or_activation": "A seed ensemble has no update frontier.",
        "schedule": "A seed ensemble has no iterative schedule.",
        "read_dependencies_or_neighborhood": "No local update is performed.",
        "write_replacement_assembly_or_commit": "Sampling output is represented by result_kind.",
        "termination_completion_failure": "One sample completes the generator call.",
        "witness_semantics": "No certificate beyond membership in the binary configuration space is defined.",
        "structural_invariants": "No trajectory invariants apply to a one-shot seed ensemble.",
        "topology": "The source does not state dependence structure between sampled positions.",
    },
    missing="The probability distribution and finite/infinite support convention are not stated.",
    claim="The passage explicitly contrasts experiments from random initial conditions with simple seeds, but leaves the sampling law unspecified.",
    strength="DIRECT_PARTIAL_MECHANICS",
)

experiment_facts = {
    "object_kind": "A reproducible computer-experiment search and inspection protocol.",
    "native_time": "Experiments run each selected program for successive steps.",
    "carrier": "A chosen rule/program space and the trajectories generated from its members.",
    "support": "An enumerated or randomly sampled collection of precisely specified programs.",
    "complete_state": "The exact rule, initial condition, and run prefix for each experiment.",
    "input": "A simple program class, rule selection, exact initial conditions, and run length.",
    "frontier_or_activation": "Each selected program is independently run and inspected.",
    "schedule": "Prefer broad/mindless enumeration or sampling, execute, display raw behavior, inspect, then revise assumptions and repeat.",
    "read_dependencies_or_neighborhood": "The protocol reads exact trajectories and their direct visual presentations.",
    "law_kind": "An experimental enumeration/execution/inspection procedure.",
    "rule_relation_constraint_function_or_probability_law": "Specify exact rules and seeds, run many simple cases, inspect actual behavior rather than a narrow summary, and iteratively remove search assumptions.",
    "result_kind": "A reproducible collection of trajectories and discovered behavior classes/examples.",
    "successor_cardinality": "Many experimental cases; each fixed deterministic program has one run.",
    "determinism_branching_or_measure": "Deterministic per exact program/seed, with enumeration or random sampling at the experiment-selection level.",
    "termination_completion_failure": "An experiment round ends at its selected case/run bounds and may be revised for a new round.",
    "witness_semantics": "A claimed example is witnessed by its exact rule, initial condition, and directly inspectable run.",
    "parameters_and_variants": "Program family, search order/distribution, seed, run length, display, and criteria vary.",
    "excluded_observers_and_representations": "Automated criteria and pictures aid discovery but do not replace the native laws of tested systems.",
    "evidence_limit": "The methodology is procedural guidance, not a single fixed exhaustive algorithm for every program space.",
}
experiment = source_candidate(
    "computer-experiment-protocol",
    "simple direct computer-experiment discovery protocol",
    "U000607",
    experiment_facts,
    aliases=["methodology based on doing computer experiments"],
    not_applicable={
        "topology": "The experiment protocol has no single spatial topology.",
        "structural_invariants": "Invariants belong to each tested program, not the protocol.",
        "alphabet_or_value_schema": "The schema varies with the tested program family.",
        "visible_history": "Histories are outputs consumed by the protocol, represented in result_kind.",
        "control_state": "No mandatory controller state beyond experiment-round choices is defined.",
        "seed": "Initial conditions are protocol inputs rather than a fixed protocol seed.",
        "boundary": "Boundaries belong to the tested program.",
        "external_data": "No external stream is intrinsic to the protocol.",
        "write_replacement_assembly_or_commit": "The protocol observes program runs; it has no shared state commit.",
    },
    missing="No single stopping or saturation criterion for all searches is specified.",
    claim="The methodology section defines precise repeatable program experiments and later specifies broad search, direct behavior inspection, visual analysis, and iterative assumption removal.",
)
context_evidence(
    experiment,
    "computer-experiment-precision",
    "U000610",
    "Rules and initial conditions can be specified perfectly precisely and rerun identically.",
    strength="CORROBORATING",
)
context_evidence(
    experiment,
    "computer-experiment-broad-search",
    "U000625",
    "The passage prescribes a broad mindless search over a narrowly crafted one.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    experiment,
    "computer-experiment-direct-view",
    "U000626",
    "The passage prescribes inspection of actual behavior rather than lossy summaries.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
visual_observer = source_candidate(
    "visual-raster-inspection-observer",
    "direct visual trajectory-inspection observer",
    "U000626",
    observer_facts(
        "direct visual trajectory inspection",
        "Raw program trajectories or large arrays of states.",
        "Render raw state data as pictures with minimal summarization and inspect the picture directly for unexpected structure.",
        "A visual representation supporting rapid human recognition of behavior.",
    ),
    not_applicable=observer_na,
    missing="The source intentionally does not reduce human visual recognition to a fixed automated classifier.",
    claim="The passage distinguishes actual behavior from summaries; the following passage defines picture rendering as the practical analysis interface.",
)
context_evidence(
    visual_observer,
    "visual-raster-inspection-picture",
    "U000627",
    "The passage states that pictures make huge raw datasets rapidly analyzable by eye.",
    strength="DIRECT_COMPLETE_MECHANICS",
)


# Literal construction-bearing routes.  Workers propose them but do not resolve.
add_route(
    "rule90-page26",
    "U000339",
    "rule 90 from page 26",
    "rule 90 construction and comparison",
    ["rule 90", "page 26", "nested pattern"],
)
add_route(
    "rule110-page32",
    "U000376",
    "rule 110 on page 32",
    "rule 110 localized-structure construction",
    ["rule 110", "page 32", "identifiable structures"],
)
add_route(
    "trees-page400",
    "U000471",
    "On page 400 I will use similar systems to discuss the growth of actual trees and leaves.",
    "substitution systems applied to tree and leaf growth",
    ["page 400", "actual trees", "leaves", "substitution"],
)
add_route(
    "tag1-page83-a",
    "U000524",
    "the first three ordinary neighbor-independent substitution systems shown on page 83",
    "tag/substitution cycle correspondence",
    ["page 83", "tag system", "neighbor-independent substitution"],
    scope="WITHIN_STAGE",
)
add_route(
    "tag1-page83-b",
    "U000525",
    "neighbor-independent substitution system of the kind we discussed on page 83",
    "one-deletion tag-system equivalence profile",
    ["page 83", "one element removed", "substitution system"],
    scope="WITHIN_STAGE",
)
add_route(
    "cyclic-page83",
    "U000539",
    "the third neighbor-independent substitution system shown on page 83",
    "cyclic-tag case (c) nested-form correspondence",
    ["page 83", "cyclic tag", "third substitution system"],
    scope="WITHIN_STAGE",
)
add_route(
    "register-page122",
    "U000560",
    "As discussed on page 122",
    "arithmetic derivation of the register-machine zero-event value map",
    ["page 122", "register machine", "3n/2", "(3n+1)/2"],
)
add_route(
    "totalistic-page60",
    "U000602",
    "totalistic type described on page 60",
    "base definition of totalistic cellular automata",
    ["page 60", "totalistic", "number of colors"],
    scope="WITHIN_STAGE",
)
add_route(
    "rule30-page27",
    "U000631",
    "rule 30 from page 27",
    "rule 30 simple-seed evolution",
    ["rule 30", "page 27", "non-symmetric rule"],
)
add_route(
    "mobile-page74",
    "U000637",
    "the example shown on page 74",
    "extended mobile automaton found after correcting compression criteria",
    ["page 74", "mobile automaton", "compression", "search criteria"],
    scope="WITHIN_STAGE",
)
add_route(
    "mobile-page75",
    "U000638",
    "the example shown on page 75",
    "extended mobile automaton found after removing search assumptions",
    ["page 75", "mobile automaton", "search assumptions"],
    scope="WITHIN_STAGE",
)

# Attach later route-source evidence to candidates so every route is provenance-bound.
for _spec, _label, _unit in [
    (eca_rules[90], "eca-rule-90-route-context", "U000339"),
    (eca_rules[110], "eca-rule-110-route-context", "U000376"),
    (tag1, "tag-delete-one-route-a", "U000524"),
    (tag1, "tag-delete-one-route-b", "U000525"),
    (cyclic_seed, "cyclic-tag-route-context", "U000539"),
    (zero_observer, "register-zero-route-context", "U000560"),
    (arith_map, "register-map-route-context", "U000560"),
    (k_totalistic, "k-totalistic-route-context", "U000602"),
    (eca_rules[30], "eca-rule-30-route-context", "U000631"),
    (mobile_random_color, "extended-mobile-page74-route-context", "U000637"),
    (mobile_random_motion, "extended-mobile-page75-route-context", "U000638"),
]:
    context_evidence(
        _spec,
        _label,
        _unit,
        "This unit supplies the literal route attached to the candidate.",
        strength="LEAD_ONLY",
        modality="CROSS_REFERENCE",
    )


UNKNOWN_LABELS = {
    field: field.replace("_", " ") for field in FINGERPRINT_FIELDS
}


def unknown_reason(spec: CandidateSpec, field: str) -> str:
    return (
        f"The assigned Chapter 3 main-text evidence for {spec['name']} does "
        f"not state {UNKNOWN_LABELS[field]} beyond the recorded facts and routes."
    )


def allocate(
    reading_input: list[dict[str, str]],
    asset_input: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, list[str]],
]:
    unit_order = {
        row["source_unit_id"]: index
        for index, row in enumerate(reading_input, 1)
    }
    image_order = {
        row["physical_path"]: len(reading_input) + index
        for index, row in enumerate(asset_input, 1)
    }
    asset_by_path = {row["physical_path"]: row for row in asset_input}

    def anchor_details(anchor: str) -> tuple[str, int]:
        if anchor in unit_order:
            return "SOURCE_UNIT", unit_order[anchor]
        if anchor in image_order:
            return "IMAGE", image_order[anchor]
        raise AuthoringError(f"unknown anchor {anchor}")

    specs = sorted(
        ALL_CANDIDATES,
        key=lambda item: (anchor_details(item["anchor"])[1], item["_insertion"]),
    )
    id_by_key = {
        item["key"]: f"W{index:04d}" for index, item in enumerate(specs, 1)
    }
    candidate_ordinals: dict[str, int] = {}
    candidate_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for item in specs:
        kind, _ = anchor_details(item["anchor"])
        identity = (kind, item["anchor"])
        candidate_counts[identity] += 1
        candidate_ordinals[item["key"]] = candidate_counts[identity]

    evidence_entries: list[tuple[CandidateSpec, EvidenceSpec, str, int]] = []
    for item in ALL_CANDIDATES:
        for ev in item["evidence"]:
            anchor = ev["image_path"] or ev["unit"]
            kind, order = anchor_details(anchor)
            evidence_entries.append((item, ev, kind, order))
    evidence_entries.sort(key=lambda x: (x[3], x[1]["_insertion"], x[0]["_insertion"]))
    ev_identity: dict[tuple[str, str], tuple[str, str, int]] = {}
    ev_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for index, (item, ev, kind, _order) in enumerate(evidence_entries, 1):
        anchor = ev["image_path"] or ev["unit"]
        identity = (kind, anchor)
        ev_counts[identity] += 1
        ev_identity[(item["key"], ev["label"])] = (
            f"WE{index:06d}",
            f"WG{index:06d}",
            ev_counts[identity],
        )

    route_specs = sorted(
        ALL_ROUTES,
        key=lambda item: (unit_order[item["unit"]], item["_insertion"]),
    )
    route_id_by_key = {
        item["key"]: f"WR{index:04d}"
        for index, item in enumerate(route_specs, 1)
    }
    route_counts: defaultdict[str, int] = defaultdict(int)
    route_proposals: list[dict[str, str]] = []
    for item in route_specs:
        route_counts[item["unit"]] += 1
        route_proposals.append(
            {
                "route_id": route_id_by_key[item["key"]],
                "source_unit_id": item["unit"],
                "source_asset_id": "",
                "discovery_epoch": "1",
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": item["unit"],
                "discovery_ordinal": str(route_counts[item["unit"]]),
                "literal_target": item["literal"],
                "route_kind": item["kind"],
                "expected_topic": item["topic"],
                "owning_stage": str(STAGE),
                "closure_scope": item["scope"],
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": "[]",
                "vocabulary_terms": compact(item["vocabulary"]),
                "defect_boundary": "",
            }
        )

    candidate_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    candidate_links_by_image: defaultdict[str, list[str]] = defaultdict(list)
    anchor_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    proposals: list[dict[str, Any]] = []

    for item in specs:
        cid = id_by_key[item["key"]]
        anchor_kind, anchor_order = anchor_details(item["anchor"])
        local: list[dict[str, Any]] = []
        label_to_id: dict[str, str] = {}
        for ev in item["evidence"]:
            eid, gid, ordinal = ev_identity[(item["key"], ev["label"])]
            label_to_id[ev["label"]] = eid
            ev_anchor = ev["image_path"] or ev["unit"]
            ev_kind, ev_order = anchor_details(ev_anchor)
            if ev_order < anchor_order:
                raise AuthoringError(
                    f"evidence {ev['label']} predates candidate {item['key']}"
                )
            local.append(
                {
                    "evidence_id": eid,
                    "evidence_group_id": gid,
                    "discovery_anchor": {
                        "epoch": 1,
                        "kind": ev_kind,
                        "id": ev_anchor,
                        "ordinal": ordinal,
                    },
                    "source_unit_id": ev["unit"],
                    "image_path": ev["image_path"],
                    "strength": ev["strength"],
                    "modality": ev["modality"],
                    "claim": ev["claim"],
                    "fingerprint_fields": ev["fields"],
                }
            )
        local.sort(key=lambda x: int(x["evidence_id"][2:]))
        units = sorted(
            {ev["source_unit_id"] for ev in local},
            key=lambda x: unit_order[x],
        )
        images = sorted(
            {ev["image_path"] for ev in local if ev["image_path"] is not None},
            key=lambda x: image_order[x],
        )
        for uid in units:
            candidate_links_by_unit[uid].append(cid)
        for path in images:
            candidate_links_by_image[path].append(cid)
        anchor_unit = (
            item["anchor"]
            if anchor_kind == "SOURCE_UNIT"
            else asset_by_path[item["anchor"]]["source_unit_id"]
        )
        anchor_links_by_unit[anchor_unit].append(cid)

        field_support: dict[str, str] = {}
        fingerprint: dict[str, dict[str, Any]] = {}
        unknowns: list[str] = []
        for field in FINGERPRINT_FIELDS:
            supporting = [
                ev["evidence_id"] for ev in local if field in ev["fingerprint_fields"]
            ]
            if field in item["facts"]:
                if not supporting:
                    raise AuthoringError(f"{item['key']} lacks evidence for {field}")
                field_support[field] = "SUPPORTED"
                fingerprint[field] = {
                    "status": "SUPPORTED",
                    "value": item["facts"][field],
                    "evidence_ids": supporting,
                    "reason": "",
                }
            elif field in item["not_applicable"]:
                if not supporting:
                    raise AuthoringError(f"{item['key']} lacks N/A evidence for {field}")
                field_support[field] = "NOT_APPLICABLE"
                fingerprint[field] = {
                    "status": "NOT_APPLICABLE",
                    "value": None,
                    "evidence_ids": supporting,
                    "reason": item["not_applicable"][field],
                }
            else:
                if supporting:
                    raise AuthoringError(f"{item['key']} claims absent field {field}")
                reason = unknown_reason(item, field)
                unknowns.append(reason)
                field_support[field] = "UNKNOWN_FROM_SOURCE"
                fingerprint[field] = {
                    "status": "UNKNOWN_FROM_SOURCE",
                    "value": None,
                    "evidence_ids": [],
                    "reason": reason,
                }

        def records(values: list[tuple[str, str, list[str]]]) -> list[dict[str, Any]]:
            return [
                {
                    "name": name,
                    "source_description": description,
                    "evidence_ids": [label_to_id[label] for label in labels],
                }
                for name, description, labels in values
            ]

        route_ids = [route_id_by_key[key] for key in item["route_keys"]]
        values: dict[str, Any] = {
            "id": cid,
            "record_status": "ACTIVE",
            "provisional_name": item["name"],
            "aliases": item["aliases"],
            "discovery_stage": STAGE,
            "discovery_anchor": {
                "epoch": 1,
                "kind": anchor_kind,
                "id": item["anchor"],
                "ordinal": candidate_ordinals[item["key"]],
            },
            "source_unit_ids": units,
            "source_evidence": local,
            "source_status": item["source_status"],
            "image_witnesses": images,
            "evidence_strength": list(dict.fromkeys(ev["strength"] for ev in local)),
            "field_support": field_support,
            "fingerprint": fingerprint,
            "parameters": records(item["parameters"]),
            "variants": records(item["variants"]),
            "missing_mechanics": list(dict.fromkeys([item["missing"], *unknowns])),
            "uncertainties": item["uncertainties"],
            "related_candidate_ids": [],
            "cross_reference_ids": route_ids,
            "evidence_reassignments": [],
        }
        proposals.append({field: values[field] for field in CANDIDATE_FIELDS})

    return (
        proposals,
        route_proposals,
        dict(candidate_links_by_unit),
        dict(candidate_links_by_image),
        dict(anchor_links_by_unit),
    )


DEFECT_UNITS = {
    "U000343": (
        "The assigned image is a severely cropped 42×14 fragment containing "
        "only part of the 'rule 30' label; no evolution or rule mechanics can "
        "be recovered from it."
    )
}
AMBIGUOUS_UNITS = {
    "U000374": (
        "The middle page-81 totalistic evolution is present, but the assigned "
        "asset and adjacent source omit its code label."
    ),
    "U000375": (
        "The crop contains a top-edge spill label 'code 1635' and a clear "
        "bottom label 'code 2049'; later explicit labels resolve the continued "
        "runs, but this asset boundary is ambiguous in isolation."
    ),
}


def default_reading(row: dict[str, str]) -> tuple[str, list[str], str]:
    uid = row["source_unit_id"]
    number = int(uid[1:])
    kind = row["block_kind"]
    if kind == "image":
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"],
            "Reviewed in context and at original resolution; this unlinked image is an evolution/output representation rather than an additional native law.",
        )
    if kind == "caption":
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"],
            "Reviewed in full; the caption describes an output or comparison without independently introducing a construction.",
        )
    if 585 <= number <= 603:
        return (
            "NO_CONSTRUCTION",
            ["BEHAVIOR_OR_OUTCOME", "CONTROL_OR_COMPARISON"],
            "Reviewed in full; this conclusions unit compares behavior classes or rule complexity without a new identity-plus-mechanics object.",
        )
    if 604 <= number <= 640:
        return (
            "HISTORICAL_ONLY" if number in {631, 632, 633, 634, 635, 636, 637, 638, 640} else "NO_CONSTRUCTION",
            ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
            "Reviewed in full; this methodology/history unit supplies motivation, chronology, or design guidance without an independently captured construction.",
        )
    if number in {491, 494, 507, 567, 568, 569, 571, 574}:
        return (
            "APPLICATION_OR_EMULATION",
            ["APPLICATION", "EMULATION"],
            "Reviewed in full; this unit relates an identified construction to text editors, practical languages, or Mathematica without adding another native law.",
        )
    return (
        "NO_CONSTRUCTION",
        ["BEHAVIOR_OR_OUTCOME", "CONTROL_OR_COMPARISON"],
        "Reviewed in full; this unit supplies behavioral, explanatory, quantitative, or comparative context without a separately delimited construction.",
    )


def candidate_roles(
    candidate_ids: list[str],
    specs_by_id: dict[str, CandidateSpec],
    block_kind: str,
) -> list[str]:
    roles: list[str] = []
    names = " ".join(specs_by_id[cid]["name"].lower() for cid in candidate_ids)
    if "seed" in names or "initial-condition" in names:
        roles.append("SEED_INPUT_OR_BOUNDARY")
    if "observer" in names or "compression" in names or "inspection" in names:
        roles.append("OBSERVER_OR_ANALYZER")
    if "representation" in names or "encoding" in names:
        roles.append("REPRESENTATION")
    if "restriction" in names or "variant" in names:
        roles.append("PROPERTY_OR_RESTRICTION")
    if block_kind == "image":
        roles.append("REPRESENTATION")
    return list(dict.fromkeys(roles))


RULE_IMAGES = {
    "CHAPTERS/_page_68_Figure_7.jpeg",
    "CHAPTERS/_page_68_Picture_3.jpeg",
    "CHAPTERS/_page_75_Figure_6.jpeg",
    "CHAPTERS/_page_86_Picture_8.jpeg",
    "CHAPTERS/_page_87_Figure_2.jpeg",
    "CHAPTERS/_page_88_Picture_8.jpeg",
    "CHAPTERS/_page_89_Picture_3.jpeg",
    "CHAPTERS/_page_90_Figure_4.jpeg",
    "CHAPTERS/_page_91_Figure_6.jpeg",
    "CHAPTERS/_page_92_Figure_1.jpeg",
    "CHAPTERS/_page_93_Picture_6.jpeg",
    "CHAPTERS/_page_94_Figure_1.jpeg",
    "CHAPTERS/_page_95_Figure_2.jpeg",
    "CHAPTERS/_page_96_Picture_4.jpeg",
    "CHAPTERS/_page_97_Picture_6.jpeg",
    "CHAPTERS/_page_97_Picture_7.jpeg",
    "CHAPTERS/_page_98_Figure_2.jpeg",
    "CHAPTERS/_page_100_Picture_3.jpeg",
    "CHAPTERS/_page_101_Picture_5.jpeg",
    "CHAPTERS/_page_102_Figure_4.jpeg",
    "CHAPTERS/_page_104_Picture_3.jpeg",
    "CHAPTERS/_page_105_Picture_2.jpeg",
    "CHAPTERS/_page_105_Figure_4.jpeg",
    "CHAPTERS/_page_106_Figure_4.jpeg",
    "CHAPTERS/_page_107_Picture_5.jpeg",
    "CHAPTERS/_page_108_Figure_5.jpeg",
    "CHAPTERS/_page_108_Figure_6.jpeg",
    "CHAPTERS/_page_108_Figure_7.jpeg",
    "CHAPTERS/_page_108_Figure_8.jpeg",
    "CHAPTERS/_page_109_Figure_2.jpeg",
    "CHAPTERS/_page_110_Picture_5.jpeg",
    "CHAPTERS/_page_110_Picture_7.jpeg",
    "CHAPTERS/_page_111_Figure_1.jpeg",
    "CHAPTERS/_page_113_Figure_1.jpeg",
    "CHAPTERS/_page_114_Picture_5.jpeg",
    "CHAPTERS/_page_115_Figure_1.jpeg",
    "CHAPTERS/_page_117_Figure_5.jpeg",
    "CHAPTERS/_page_119_Figure_3.jpeg",
    "CHAPTERS/_page_122_Figure_2.jpeg",
}
TEXT_IMAGES = RULE_IMAGES | {
    "CHAPTERS/_page_74_Picture_2.jpeg",
    "CHAPTERS/_page_81_Picture_1.jpeg",
    "CHAPTERS/_page_81_Picture_3.jpeg",
}


def build_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    manifest = json.loads((bundle / "allowed-manifest.json").read_text())
    if (
        manifest.get("worker_id") != EXPECTED_WORKER
        or manifest.get("content_set_sha256") != EXPECTED_CONTENT_SET
        or manifest.get("source_paths") != EXPECTED_PATHS
        or manifest.get("source_unit_count") != 335
        or manifest.get("asset_count") != 87
        or manifest.get("stage") != STAGE
        or manifest.get("discovery_epoch") != 1
    ):
        raise AuthoringError("bundle is not the exact Stage 7 epoch-1 assignment")

    output_path = bundle / "output" / "output.json"
    original_bytes = output_path.read_bytes()
    output = json.loads(original_bytes)
    readings = read_csv(bundle / "input" / "reading-input.csv")
    assets = read_csv(bundle / "input" / "asset-input.csv")
    scaffold = prepare_review_output.scaffold_output(
        prepare_review_output.expected_template(bundle, manifest),
        readings,
        assets,
    )
    if output != scaffold:
        raise AuthoringError("output is not the pristine nonsemantic scaffold")

    (
        candidates,
        routes,
        candidate_links_by_unit,
        candidate_links_by_image,
        anchor_links_by_unit,
    ) = allocate(readings, assets)
    specs_sorted = sorted(
        ALL_CANDIDATES,
        key=lambda spec: next(
            i
            for i, proposal in enumerate(candidates)
            if proposal["provisional_name"] == spec["name"]
            and proposal["discovery_anchor"]["id"] == spec["anchor"]
        ),
    )
    specs_by_id = {
        proposal["id"]: spec
        for proposal, spec in zip(candidates, specs_sorted)
    }
    route_links: defaultdict[str, list[str]] = defaultdict(list)
    for route in routes:
        route_links[route["source_unit_id"]].append(route["route_id"])

    reading_updates: list[dict[str, str]] = []
    for original in readings:
        row = deepcopy(original)
        uid = row["source_unit_id"]
        cids = candidate_links_by_unit.get(uid, [])
        rids = route_links.get(uid, [])
        if uid in DEFECT_UNITS:
            disposition = "SOURCE_DEFECT_OR_AMBIGUITY"
            secondary = ["SOURCE_DEFECT"]
            statement = (
                f"Reviewed in full and at original resolution; {DEFECT_UNITS[uid]} "
                f"Linked candidate context: {', '.join(cids) if cids else 'none'}."
            )
        elif cids:
            is_anchor = bool(set(cids) & set(anchor_links_by_unit.get(uid, [])))
            disposition = "CANDIDATE" if is_anchor else "SUPPORTS_CANDIDATE"
            secondary = candidate_roles(cids, specs_by_id, row["block_kind"])
            statement = (
                f"This unit {'discovers' if is_anchor else 'supports'} "
                f"{', '.join(cids)} with source-grounded identity, mechanics, "
                "restriction, seed, observer, or representation evidence."
            )
            if rids:
                statement += f" It also originates {', '.join(rids)}."
        elif rids:
            disposition = "CROSS_REFERENCE"
            secondary = ["CONTROL_OR_COMPARISON"]
            statement = (
                f"Reviewed in full; this unit originates {', '.join(rids)} "
                "to construction-bearing targets and does not independently "
                "supply another native law here."
            )
        else:
            disposition, secondary, statement = default_reading(row)
        status = (
            "DEFECTIVE"
            if uid in DEFECT_UNITS
            else "AMBIGUOUS"
            if uid in AMBIGUOUS_UNITS
            else "CLEAR"
        )
        uncertainty = DEFECT_UNITS.get(uid, AMBIGUOUS_UNITS.get(uid, ""))
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": disposition,
                "source_status": status,
                "uncertainty": uncertainty,
                "secondary_roles": compact(secondary),
                "candidate_ids": compact(cids),
                "route_ids": compact(rids),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": EXPECTED_WORKER,
            }
        )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in assets:
        row = deepcopy(original)
        path = row["physical_path"]
        uid = row["source_unit_id"]
        cids = candidate_links_by_image.get(path, [])
        if path == "CHAPTERS/_page_66_Picture_0.jpeg":
            role = "DECORATIVE"
            risks: list[str] = []
            transcription = "NOT_REQUIRED"
            statement = "Original-resolution inspection confirms a decorative chapter opener with no rule, seed, or construction."
        elif uid in DEFECT_UNITS:
            role = "SOURCE_DEFECT"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING", "AMBIGUOUS", "CAPTION_INCOMPLETE"]
            transcription = "CHECKED"
            statement = "Original-resolution inspection confirms the severe rule-30 label crop; no mechanics were inferred from the fragment."
        elif path in RULE_IMAGES:
            role = "NATIVE_EVIDENCE"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            transcription = "CHECKED"
            statement = (
                "Original-resolution inspection confirms a construction-bearing "
                "rule, code, program, or finite rule survey"
                + (f" linked to {', '.join(cids)}." if cids else ".")
            )
        else:
            role = "OBSERVER"
            risks = ["CONSTRUCTION_BEARING"]
            if path in TEXT_IMAGES:
                risks.append("TEXT_BEARING")
            transcription = "CHECKED" if path in TEXT_IMAGES else "NOT_REQUIRED"
            statement = (
                "Original-resolution inspection confirms an evolution, long-run "
                "history, compressed view, plot, or alternative representation"
                + (f" supporting {', '.join(cids)}." if cids else ".")
            )
        if uid in AMBIGUOUS_UNITS:
            risks = list(dict.fromkeys([*risks, "AMBIGUOUS", "CAPTION_INCOMPLETE"]))
        status = (
            "DEFECTIVE"
            if uid in DEFECT_UNITS
            else "AMBIGUOUS"
            if uid in AMBIGUOUS_UNITS
            else "CLEAR"
        )
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": role,
                "source_status": status,
                "risk_flags": compact(risks),
                "original_resolution_status": "REVIEWED",
                "transcription_status": transcription,
                "candidate_ids": compact(cids),
                "route_ids": compact(route_links.get(uid, [])),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": EXPECTED_WORKER,
                "uncertainty": DEFECT_UNITS.get(uid, AMBIGUOUS_UNITS.get(uid, "")),
            }
        )
        asset_updates.append(row)

    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": candidates,
            "asset_updates": asset_updates,
            "route_proposals": routes,
            "uncertainties": [
                "The 42×14 page-74 rule-30 label crop is defective; complete earlier rule evidence prevents mechanics loss.",
                "The middle page-81 three-color totalistic evolution is retained as an unnamed candidate because its code label is absent.",
                "The adjacent page-81 code-1635/code-2049 crop boundary is ambiguous in isolation; later explicit labels resolve the two continued runs.",
                "Finite survey figures are retained as survey candidates where individual visual rules are explicit but not separately transcribed; no unseen rule text is invented.",
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
        print(f"Chapter 3 main authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "recorded Stage 7 Chapter 3 main review: "
        f"reading=335 assets=87 candidates={len(ALL_CANDIDATES)} "
        f"routes={len(ALL_ROUTES)} declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
