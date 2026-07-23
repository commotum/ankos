#!/usr/bin/env python3
"""Author the sealed Stage 7 Chapter 3 Notes blind-review bundle."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

GOAL_TOOLS = Path("/home/jake/Developer/ankos/goal-4/tools")
sys.path.insert(0, str(GOAL_TOOLS))

import author_ch02_experiment_review as base  # noqa: E402
import prepare_review_output  # noqa: E402
from audit_contract import canonical_json_bytes  # noqa: E402


BUNDLE_HASH = "c1d14d069b2aef917d531d03ebe0f6ca9946f52a123cbb5754ecbd5fc6d5389b"
WORKER = "ch03-notes-reader-e1"
SOURCE_PATH = "BACK-MATTER/NOTES/03-The-World-of-Simple-Programs-Notes.md"

base.ALL_CANDIDATE_SPECS.clear()
base.ALL_ROUTE_SPECS.clear()
base.EXPECTED_PATHS = [SOURCE_PATH]


class AuthoringError(ValueError):
    pass


def compact(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def unknown_reason(spec: dict[str, Any], field: str) -> str:
    return (
        f"The assigned Chapter 3 Notes evidence for {spec['name']} does not "
        f"state {base.UNKNOWN_FACT_LABELS[field]}."
    )


base.exact_unknown_reason = unknown_reason


def transition(
    *,
    key: str,
    name: str,
    anchor: str,
    object_kind: str,
    carrier: str,
    state: str,
    law: str,
    result: str,
    input_text: str,
    neighborhood: str,
    parameters: str,
    aliases: list[str] | None = None,
    termination: str | None = None,
    missing: str | None = None,
) -> dict[str, Any]:
    limit = missing or (
        "The assigned passage fixes the stated transition but does not exhaust "
        "all boundary behavior, malformed-rule behavior, or equivalence classes."
    )
    facts = {
        "object_kind": object_kind,
        "native_time": "Discrete successive steps.",
        "carrier": carrier,
        "complete_state": state,
        "input": input_text,
        "frontier_or_activation": (
            "The components selected by the stated rule at the current step."
        ),
        "schedule": "One complete native step is evaluated from the current state.",
        "read_dependencies_or_neighborhood": neighborhood,
        "law_kind": "A deterministic replacement or transition rule.",
        "rule_relation_constraint_function_or_probability_law": law,
        "write_replacement_assembly_or_commit": (
            "The rule's returned replacements are assembled into the next state."
        ),
        "result_kind": result,
        "successor_cardinality": (
            "Exactly one successor for a valid state and a complete deterministic rule."
        ),
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": parameters,
        "excluded_observers_and_representations": (
            "Mathematica syntax, retained histories, plots, compression, and "
            "rendered layouts are implementations or observers unless stated "
            "as part of the native object."
        ),
        "evidence_limit": limit,
    }
    if termination is not None:
        facts["termination_completion_failure"] = termination
    return base.source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts=facts,
        claim=(
            f"The source directly specifies the state and native law of {name}."
        ),
        missing=limit,
        parameters=[
            (
                "source-delimited parameters and variants",
                parameters,
                [f"{key}-source"],
            )
        ],
    )


def preset(
    *,
    key: str,
    name: str,
    anchor: str,
    law: str,
    family: str,
    aliases: list[str] | None = None,
    extra: dict[str, str] | None = None,
    modality: str = "FORMULA",
    missing: str | None = None,
) -> dict[str, Any]:
    limit = missing or (
        "The source fixes this preset's identity and stated law but does not "
        "supply a complete boundary convention, seed contract, or termination law."
    )
    facts = {
        "object_kind": f"A materially delimited preset of {family}.",
        "law_kind": "A deterministic rule or finite lookup preset.",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": "The unique result selected by the stated preset law.",
        "successor_cardinality": "One result for every input covered by the rule.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": (
            "The named rule number, lookup table, algebraic operation, or program "
            "list distinguishes this preset."
        ),
        "excluded_observers_and_representations": (
            "Displayed evolutions and behavioral descriptions do not add native state."
        ),
        "evidence_limit": limit,
    }
    if extra:
        facts.update(extra)
    return base.source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts=facts,
        claim=f"The source directly delimits {name} and its rule.",
        missing=limit,
        modality=modality,
        parameters=[
            (
                "preset identity",
                facts["parameters_and_variants"],
                [f"{key}-source"],
            )
        ],
    )


DIRECT_NA = [
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
    "termination_completion_failure",
]


def direct_object(
    *,
    key: str,
    name: str,
    anchor: str,
    object_kind: str,
    input_text: str,
    law: str,
    result: str,
    parameters: str,
    aliases: list[str] | None = None,
    modality: str = "FORMULA",
    missing: str | None = None,
) -> dict[str, Any]:
    limit = missing or (
        "The source defines the stated function or relation but does not "
        "supply behavior outside its stated input domain."
    )
    facts = {
        "object_kind": object_kind,
        "carrier": input_text,
        "input": input_text,
        "law_kind": "A directly evaluated deterministic function or relation.",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "successor_cardinality": "Exactly one result for each valid input.",
        "determinism_branching_or_measure": "Deterministic.",
        "parameters_and_variants": parameters,
        "excluded_observers_and_representations": (
            "Plots and alternative closed forms are representations of the "
            "same denotation unless the source states a different object."
        ),
        "evidence_limit": limit,
    }
    spec = base.source_candidate(
        key=key,
        name=name,
        anchor=anchor,
        aliases=aliases or [],
        facts=facts,
        claim=f"The source directly defines {name}.",
        missing=limit,
        modality=modality,
        parameters=[
            (
                "source-delimited parameters",
                parameters,
                [f"{key}-source"],
            )
        ],
    )
    reason = (
        "This candidate is evaluated directly as a function, relation, "
        "constant, or sequence definition and is not a second iterated transition."
    )
    spec["not_applicable"] = {}
    for field in DIRECT_NA:
        if field not in spec["facts"]:
            spec["not_applicable"][field] = reason
            spec["evidence"][0]["fields"].append(field)
    return spec


def add_support(
    spec: dict[str, Any],
    *,
    label: str,
    unit: str,
    claim: str,
    fields: list[str],
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    modality: str = "PROSE",
    image_path: str | None = None,
) -> None:
    base.add_evidence(
        spec,
        label=label,
        unit=unit,
        claim=claim,
        fields=fields,
        strength=strength,
        modality=modality,
        image_path=image_path,
    )


# Cellular-automaton relations, presets, variants, and compositions.
equivalence = direct_object(
    key="eca-equivalence",
    name="elementary cellular-automaton color/reflection equivalence relation",
    anchor="U005322",
    object_kind="A finite equivalence relation on elementary rule numbers.",
    input_text="An elementary rule lookup list or rule number.",
    law=(
        "Generate color interchange by 1-Reverse[list], left/right reflection "
        "by the stated index permutation, and their composition."
    ),
    result="The four-rule equivalence block containing the input rule.",
    parameters="The elementary rule number and chosen symmetry operation.",
)
add_support(
    equivalence,
    label="eca-equivalence-table",
    unit="U005323",
    image_path="BACK-MATTER/NOTES/_page_898_Picture_8.jpeg",
    claim="The original-resolution table visibly enumerates the four-member blocks.",
    fields=["result_kind", "parameters_and_variants", "evidence_limit"],
    strength="CORROBORATING",
    modality="IMAGE",
)

boolean_map = direct_object(
    key="eca-boolean-map",
    name="elementary cellular-automaton Boolean-expression lookup",
    anchor="U005325",
    object_kind="A rule-number-to-Boolean-expression representation function.",
    input_text="An elementary rule number from 0 through 255.",
    law=(
        "Return the displayed minimal Boolean expression in left, center, and "
        "right variables p, q, r; Xor is denoted by the circled-plus symbol."
    ),
    result="A Boolean expression denoting the elementary local rule.",
    parameters="The rule number and equivalent-expression choice.",
    modality="PROSE",
)
add_support(
    boolean_map,
    label="eca-boolean-table",
    unit="U005326",
    claim="The complete code block supplies one Boolean expression for every rule.",
    fields=[
        "input",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="TABLE",
)

for key, number, law, alias in [
    ("rule51", 51, "Replace the center value by its complement.", "complement rule"),
    ("rule170", 170, "Copy the left-neighbor value as the next value.", "left shift"),
    ("rule204", 204, "Copy the center value unchanged.", "identity rule"),
    ("rule240", 240, "Copy the right-neighbor value as the next value.", "right shift"),
]:
    preset(
        key=key,
        name=f"Rule {number} elementary cellular-automaton preset",
        anchor="U005324",
        law=law,
        family="elementary cellular automata",
        aliases=[alias],
        modality="PROSE",
        extra={
            "read_dependencies_or_neighborhood": (
                "Only the single neighborhood cell named by the rule is read."
            )
        },
    )

rule_formulae = [
    ("rule22", 22, "Mod[p + q + r + p q r, 2]", "U005330"),
    ("rule60", 60, "Mod[p + q, 2]", "U005331"),
    ("rule105", 105, "Mod[1 + p + q + r, 2]", "U005332"),
    ("rule129", 129, "Mod[1 + p + q + r + p q + q r + p r, 2]", "U005333"),
    ("rule150", 150, "Mod[p + q + r, 2]", "U005334"),
    ("rule225", 225, "Mod[1 + p + q + r + q r, 2]", "U005335"),
    ("rule30", 30, "Mod[p + q + r + q r, 2]", "U005344"),
    ("rule45", 45, "Mod[1 + p + r + q r, 2]", "U005345"),
    ("rule73", 73, "Mod[1 + p + q + r + p r + p q r, 2]", "U005346"),
]
rule_specs: dict[int, dict[str, Any]] = {}
for key, number, law, support_unit in rule_formulae:
    spec = preset(
        key=key,
        name=f"Rule {number} elementary cellular-automaton preset",
        anchor="U005326",
        law=f"The Boolean-expression table fixes Rule {number}; its algebraic form is {law}.",
        family="elementary cellular automata",
        aliases=[f"cellular automaton rule {number}"],
        modality="TABLE",
        extra={
            "read_dependencies_or_neighborhood": (
                "The three Boolean arguments p, q, and r are the left, center, "
                "and right cells of the elementary neighborhood."
            )
        },
    )
    add_support(
        spec,
        label=f"{key}-algebraic",
        unit=support_unit,
        claim=f"The source gives the exact modulo-two algebraic law {law}.",
        fields=[
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        ],
        modality="FORMULA",
    )
    rule_specs[number] = spec

add_support(
    rule_specs[150],
    label="rule150-interpretation",
    unit="U005337",
    claim="Rule 150 adds all three neighborhood values modulo two.",
    fields=[
        "object_kind",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
    ],
)

rule150_row = direct_object(
    key="rule150-row-count",
    name="Rule 150 row black-cell count function",
    anchor="U005337",
    object_kind="A query returning the number of black cells on Rule 150 row t.",
    input_text="A nonnegative row index t.",
    law="Apply the displayed product over lengths of runs of 1 bits in t.",
    result="The black-cell count on row t.",
    parameters="The row index t and the single-seed Rule 150 evolution.",
)
add_support(
    rule150_row,
    label="rule150-row-count-code",
    unit="U005338",
    claim="The code gives the exact product over runs in IntegerDigits[t,2].",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "successor_cardinality",
    ],
    modality="CODE",
)

direct_object(
    key="rule150-cumulative-count",
    name="Rule 150 cumulative black-cell count at power-of-two depth",
    anchor="U005339",
    object_kind="A query for the total black cells through step 2^m.",
    input_text="A nonnegative integer m.",
    law="Return 2^m Fibonacci[m+2].",
    result="The cumulative number of black cells through the specified depth.",
    parameters="The exponent m and the single-seed Rule 150 evolution.",
)
direct_object(
    key="rule150-adjacent-column",
    name="Rule 150 adjacent-center column sequence function",
    anchor="U005340",
    object_kind="A query for the value next to the center on Rule 150 row t.",
    input_text="A nonnegative step t.",
    law="Return Mod[IntegerExponent[t,2],2].",
    result="The binary cell value adjacent to the center.",
    parameters="The step index t.",
)
direct_object(
    key="rule150-cell-value",
    name="Rule 150 Gegenbauer cell-value function",
    anchor="U005340",
    object_kind="A query for the Rule 150 cell at position n and row t.",
    input_text="A row index t and cell position n.",
    law="Return Mod[GegenbauerC[n,-t,-1/2],2].",
    result="The binary value of the selected cell.",
    parameters="The row t and position n.",
)

two_cell = transition(
    key="two-cell-ca",
    name="staggered two-cell-neighborhood cellular automaton class",
    anchor="U005352",
    object_kind="A cellular-automaton class with two predecessor cells per update.",
    carrier="Cells arranged on alternating staggered rows, drawn as hexagons or bricks.",
    state="The current row of k-valued cells.",
    law=(
        "Decode a k^2-digit base-k rule and index it by the two predecessor "
        "values using rule[[k^2-RotateLeft[a]-k a]]."
    ),
    result="A unique next row of cell values.",
    input_text="A k-valued row and a complete k^2-entry rule.",
    neighborhood="The two predecessor cells geometrically adjacent on the prior row.",
    parameters="The color count k, rule number/table, stagger orientation, and seed.",
)
two_cell["facts"]["alphabet_or_value_schema"] = (
    "A finite alphabet of k cell values; the displayed cases use k=2 and k=3."
)
for unit, path in [
    ("U005353", "BACK-MATTER/NOTES/_page_900_Picture_28.jpeg"),
    ("U005354", "BACK-MATTER/NOTES/_page_900_Picture_29.jpeg"),
    ("U005355", "BACK-MATTER/NOTES/_page_900_Picture_30.jpeg"),
]:
    add_support(
        two_cell,
        label=f"two-cell-{unit}",
        unit=unit,
        image_path=path,
        claim="The original-resolution image confirms the staggered two-parent geometry.",
        fields=["carrier", "read_dependencies_or_neighborhood", "result_kind"],
        strength="CORROBORATING",
        modality="IMAGE",
    )
add_support(
    two_cell,
    label="two-cell-counts",
    unit="U005356",
    claim="The source gives the rule count, base-k numbering, and k=2/k=3 cases.",
    fields=[
        "alphabet_or_value_schema",
        "parameters_and_variants",
        "evidence_limit",
    ],
)
add_support(
    two_cell,
    label="two-cell-step-code",
    unit="U005359",
    claim="The exact one-step code decodes both predecessor values.",
    fields=[
        "complete_state",
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)

rule7743 = preset(
    key="two-cell-7743",
    name="k=3 two-cell-neighborhood rule 7743 preset",
    anchor="U005356",
    law="Decode rule number 7743 as a 9-digit base-3 lookup under the two-cell rule schema.",
    family="staggered two-cell-neighborhood cellular automata",
)

k3_image = "BACK-MATTER/NOTES/_page_901_Picture_1.jpeg"
for number in [3826, 5451, 6385, 7743, 8364, 8701, 12294, 16963, 17989]:
    spec = rule7743 if number == 7743 else preset(
        key=f"two-cell-{number}",
        name=f"k=3 two-cell-neighborhood rule {number} preset",
        anchor="U005357",
        law=(
            f"Decode rule number {number} as a 9-digit base-3 lookup under "
            "the two-cell rule schema."
        ),
        family="staggered two-cell-neighborhood cellular automata",
        modality="IMAGE",
        missing=(
            "The image fixes the rule number and displayed evolution, while "
            "the exact seed and boundary convention are not stated here."
        ),
    )
    add_support(
        spec,
        label=f"two-cell-{number}-image",
        unit="U005357",
        image_path=k3_image,
        claim=f"Original-resolution inspection confirms the printed label rule {number}.",
        fields=["object_kind", "parameters_and_variants", "evidence_limit"],
        strength="DIRECT_IDENTITY",
        modality="IMAGE",
    )

general_ca = transition(
    key="general-ca",
    name="general k-color range-r cellular automaton class",
    anchor="U005360",
    object_kind="A one-dimensional k-color radius-r cellular-automaton family.",
    carrier="A one-dimensional list of k-valued cells.",
    state="The current complete list of cell values.",
    law=(
        "Decode a k^(2r+1)-digit base-k rule and apply the ListConvolve "
        "neighborhood index at every cell."
    ),
    result="A unique next cell list.",
    input_text="A rule number/list, k, r, and current cell list.",
    neighborhood="The 2r+1 cells centered at each target position.",
    parameters="Color count k, radius r, rule number/list, boundary, and seed.",
)
add_support(
    general_ca,
    label="general-ca-code",
    unit="U005362",
    claim="The CAStep code gives the exact weighted neighborhood index.",
    fields=[
        "complete_state",
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)

totalistic_ca = transition(
    key="totalistic-ca",
    name="k-color range-r totalistic cellular automaton class",
    anchor="U005364",
    object_kind="A cellular automaton whose rule depends only on the neighborhood sum.",
    carrier="A one-dimensional list of k-valued cells.",
    state="The current complete cell list.",
    law=(
        "Sum the 2r+1 cyclic shifts and index the totalistic rule list; "
        "ToTotalisticCARule decodes the stated code-number representation."
    ),
    result="A unique next cell list.",
    input_text="A totalistic code/list, k, r, and current cell list.",
    neighborhood="The sum of the radius-r neighborhood.",
    parameters="Color count k, radius r, totalistic code/list, boundary, and seed.",
)
for unit, label in [
    ("U005365", "nearest"),
    ("U005367", "range"),
    ("U005369", "decoder"),
]:
    add_support(
        totalistic_ca,
        label=f"totalistic-{label}",
        unit=unit,
        claim="The code fixes the stated totalistic evaluation or code decoding.",
        fields=[
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        ],
        modality="CODE",
    )

preset(
    key="code420",
    name="modulo-three additive cellular-automaton code 420 preset",
    anchor="U005371",
    law="The additive code 420 produces Pascal's triangle reduced modulo 3.",
    family="additive cellular automata",
    aliases=["code 420"],
    modality="PROSE",
)

transition(
    key="ca-composition",
    name="sequential composition of cellular-automaton rules",
    anchor="U005372",
    object_kind="A cellular-automaton composition applying two local rules per step.",
    carrier="A binary one-dimensional cell list.",
    state="The current binary row.",
    law="Apply one elementary CA rule to the row, then apply a second rule to that result.",
    result="A unique composite successor equivalent to a k=2, r=2 rule.",
    input_text="An ordered pair of elementary rules and a current row.",
    neighborhood="The effective radius-2 dependency induced by two radius-1 steps.",
    parameters="The ordered pair of component rules, seed, and boundary.",
)

algebraic_ca = transition(
    key="algebraic-ca",
    name="finite-algebraic-system cellular automaton class",
    anchor="U005373",
    object_kind="A cellular automaton whose values and local law come from a finite algebra.",
    carrier="A one-dimensional list of elements of a finite algebraic system.",
    state="The current element list.",
    law="Set a[t,i]=f[a[t-1,i-1],a[t-1,i]] for the supplied binary operation f.",
    result="A unique next list when f is a total binary operation.",
    input_text="A finite multiplication table or operation f, an initial list, and step count.",
    neighborhood="The left and current predecessor elements.",
    parameters="The finite element set, operation table, seed, and boundary.",
)
add_support(
    algebraic_ca,
    label="algebraic-evolve",
    unit="U005375",
    claim="NestList with RotateRight supplies the exact list evolution.",
    fields=[
        "schedule",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "result_kind",
    ],
    modality="CODE",
)

algebraic_presets: list[tuple[str, str, str, str, str | None]] = [
    ("times-sign", "Times cellular automaton on {1,-1}", "U005376", "Times on {1,-1}", "BACK-MATTER/NOTES/_page_901_Picture_21.jpeg"),
    ("times-complex", "Times cellular automaton on fourth roots of unity", "U005376", "Times on {1,i,-1,-i}", "BACK-MATTER/NOTES/_page_901_Picture_22.jpeg"),
    ("times-quaternion", "unit-quaternion multiplication cellular automaton", "U005376", "Quaternion multiplication on the stated unit values", "BACK-MATTER/NOTES/_page_901_Picture_23.jpeg"),
    ("table3-a", "first displayed three-element multiplication-table cellular automaton", "U005380", "{{1,1,3},{3,3,2},{2,2,1}}", "BACK-MATTER/NOTES/_page_901_Picture_25.jpeg"),
    ("table3-b", "second displayed three-element multiplication-table cellular automaton", "U005380", "{{3,1,3},{1,3,1},{3,1,2}}", "BACK-MATTER/NOTES/_page_901_Picture_26.jpeg"),
    ("s3-ca", "S3 multiplication-table cellular automaton preset", "U005385", "The displayed six-element S3 multiplication table", "BACK-MATTER/NOTES/_page_901_Picture_27.jpeg"),
]
for key, name, anchor, law, path in algebraic_presets:
    spec = preset(
        key=key,
        name=name,
        anchor=anchor,
        law=law,
        family="finite-algebraic-system cellular automata",
        modality="PROSE",
    )
    if path:
        unit = {
            "BACK-MATTER/NOTES/_page_901_Picture_21.jpeg": "U005377",
            "BACK-MATTER/NOTES/_page_901_Picture_22.jpeg": "U005378",
            "BACK-MATTER/NOTES/_page_901_Picture_23.jpeg": "U005379",
            "BACK-MATTER/NOTES/_page_901_Picture_25.jpeg": "U005381",
            "BACK-MATTER/NOTES/_page_901_Picture_26.jpeg": "U005382",
            "BACK-MATTER/NOTES/_page_901_Picture_27.jpeg": "U005383",
        }[path]
        add_support(
            spec,
            label=f"{key}-image",
            unit=unit,
            image_path=path,
            claim="Original-resolution inspection confirms the corresponding evolution.",
            fields=["result_kind", "excluded_observers_and_representations"],
            strength="CORROBORATING",
            modality="IMAGE",
        )
s3_spec = next(item for item in base.ALL_CANDIDATE_SPECS if item["key"] == "s3-ca")
s3_spec["facts"]["seed"] = (
    "A two-cell patch {5,6} surrounded by identity elements."
)
s3_spec["facts"]["input"] = (
    "The stated S3 multiplication table and the {5,6} patch in an identity background."
)
add_support(
    s3_spec,
    label="s3-table",
    unit="U005386",
    claim="The fenced table gives the exact six-element operation.",
    fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
    modality="TABLE",
)
add_support(
    s3_spec,
    label="s3-seed",
    unit="U005387",
    claim="The source states the {5,6} patch surrounded by identity elements.",
    fields=["seed", "input"],
)

# Mobile automata and generalized active sets.
mobile = transition(
    key="mobile-automaton",
    name="single-active-cell mobile automaton class",
    anchor="U005389",
    object_kind="A line of cells with one active position that reads and rewrites locally.",
    carrier="A finite cell list plus one active-cell position n.",
    state="The pair {list,n}.",
    law=(
        "Match the active cell and its left/right neighbors; return the active "
        "cell's new value and a displacement, then update {list,n} atomically."
    ),
    result="A new cell list and active position.",
    input_text="A complete rule table and an interior active-cell state.",
    neighborhood="The active cell and its immediate left and right neighbors.",
    parameters="The lookup table, color alphabet, displacement set, seed, and finite extent.",
    termination="The supplied MAStep is defined only while the active position is interior.",
)
mobile["facts"]["visible_history"] = (
    "MAEvolveList can retain the successive {list, active-position} states."
)
add_support(
    mobile,
    label="mobile-step",
    unit="U005392",
    claim="MAStep gives exact local lookup, rewrite, and active-position motion.",
    fields=[
        "complete_state",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)
add_support(
    mobile,
    label="mobile-evolve",
    unit="U005394",
    claim="MAEvolveList iterates MAStep while retaining the history.",
    fields=["visible_history", "result_kind", "parameters_and_variants"],
    modality="CODE",
)

preset(
    key="mobile-35-57",
    name="{35,57} mobile automaton preset",
    anchor="U005390",
    law="The displayed eight cases map each binary three-cell view to a new active value and displacement.",
    family="single-active-cell mobile automata",
    aliases=["page 71 mobile automaton"],
    modality="TABLE",
)
block_mobile = preset(
    key="mobile-block-rewrite",
    name="three-cell-block-rewriting mobile automaton preset",
    anchor="U005396",
    law=(
        "The displayed eight cases return a replacement three-cell block and "
        "a displacement; MAStep splices the block into the list."
    ),
    family="single-active-region mobile automata",
    aliases=["page 73 mobile automaton"],
    modality="PROSE",
)
block_mobile["facts"]["write_replacement_assembly_or_commit"] = (
    "Atomically splice the returned three-cell block at the active region, "
    "then move the active position by the returned displacement."
)
add_support(
    block_mobile,
    label="mobile-block-table",
    unit="U005397",
    claim="The code block supplies all eight block-replacement cases.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
    ],
    modality="TABLE",
)
add_support(
    block_mobile,
    label="mobile-block-step",
    unit="U005399",
    claim="The alternate MAStep gives exact three-cell atomic replacement and motion.",
    fields=["write_replacement_assembly_or_commit", "result_kind"],
    modality="CODE",
)

generalized_mobile = transition(
    key="generalized-mobile",
    name="generalized multiple-active-cell mobile automaton class",
    anchor="U005406",
    object_kind="A cell list with a finite set of simultaneously active positions.",
    carrier="A cell list and active-position list nlist.",
    state="The pair {list,nlist}.",
    law=(
        "Evaluate each active three-cell view, write returned values at the "
        "current active positions, and union all returned relative active positions."
    ),
    result="A new cell list and deduplicated active-position set.",
    input_text="A local rule table and {list,nlist}.",
    neighborhood="The three-cell interval centered at each active position.",
    parameters="The rule cases, alphabet, active-set seed, boundary, and conflict semantics.",
    missing=(
        "The code fixes the simultaneous calculation but does not state what "
        "happens when different active positions request conflicting writes."
    ),
)
add_support(
    generalized_mobile,
    label="generalized-mobile-code",
    unit="U005407",
    claim="GMAStep supplies the exact mapped lookups, Fold writes, and Union activation.",
    fields=[
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "result_kind",
        "evidence_limit",
    ],
    modality="CODE",
)

# Turing machines and the Busy Beaver relation.
turing = transition(
    key="turing-machine",
    name="single-tape Turing machine class",
    anchor="U005409",
    object_kind="A finite-control head operating on a one-dimensional tape.",
    carrier="A cell list/tape, head position, and finite head state.",
    state="The triple {s,list,n}.",
    law=(
        "Lookup {head state, scanned value}; return new state, written value, "
        "and head displacement."
    ),
    result="A new head state, tape state, and head position.",
    input_text="A complete transition table and initial tape/head state.",
    neighborhood="The head state and value of the single scanned tape cell.",
    parameters="State count s, color count k, rule table/number, initial tape, and boundary.",
)
turing["facts"]["visible_history"] = (
    "TMEvolveList retains successive {state, tape, head-position} triples."
)
turing["facts"]["seed"] = (
    "The stated blank-tape constructor uses a finite all-zero tape with the "
    "head at its center and the initial finite-control state."
)
for unit, label, fields in [
    ("U005413", "tm-step", ["complete_state", "schedule", "read_dependencies_or_neighborhood", "rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit"]),
    ("U005415", "tm-evolve", ["visible_history", "result_kind"]),
    ("U005419", "tm-blank", ["seed", "parameters_and_variants"]),
]:
    add_support(
        turing,
        label=label,
        unit=unit,
        claim="The code supplies the stated Turing-machine execution detail.",
        fields=fields,
        modality="CODE",
    )

tm78 = preset(
    key="tm-page78",
    name="page-78 three-state two-color Turing machine preset",
    anchor="U005410",
    law="The displayed six transition cases map state/scanned-color pairs to new state, write, and displacement.",
    family="single-tape Turing machines",
    modality="TABLE",
)
add_support(
    tm78,
    label="tm-page78-semantics",
    unit="U005411",
    claim="The prose decodes both sides of every transition triple.",
    fields=["law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind"],
)

tm_number = direct_object(
    key="tm-numbering",
    name="Turing-machine rule-number decoder",
    anchor="U005421",
    object_kind="A constructor mapping a number to a finite Turing transition table.",
    input_text="A rule number n, color count k, and state count s.",
    law="Apply the displayed base-(2sk) digit partition and quotient/mod decoding.",
    result="The ordered transition cases for the numbered Turing machine.",
    parameters="n, k, and s.",
)
add_support(
    tm_number,
    label="tm-numbering-code",
    unit="U005422",
    claim="The code gives the complete decoding formula.",
    fields=["rule_relation_constraint_function_or_probability_law", "result_kind"],
    modality="CODE",
)

preset(
    key="tm-counter1953",
    name="Turing machine 1953 binary-counter preset",
    anchor="U005424",
    law=(
        "Rule number 1953 under the stated numbering scheme evolves as a "
        "base-2 counter, writing reversed successive digit sequences."
    ),
    family="single-tape Turing machines",
    aliases=["page 79 Turing machine (f)"],
)

busy = direct_object(
    key="busy-beaver",
    name="Busy Beaver halting-time optimization problem",
    anchor="U005437",
    object_kind="A finite optimization relation over halting Turing machines.",
    input_text="A specified state count and the corresponding finite rule space.",
    law=(
        "Among machines that eventually enter halt state 0, maximize steps "
        "before halting; a stated variant maximizes final black-cell count."
    ),
    result="The maximum and one or more witness machines attaining or bounding it.",
    parameters="State count, tape alphabet, blank-tape convention, and objective variant.",
    missing=(
        "The five-state optimum is explicitly unknown; the image tables are "
        "preserved as witnesses without inventing an external transcription."
    ),
)
for unit, path, label in [
    ("U005438", "BACK-MATTER/NOTES/_page_904_busy_beaver_2_3_4_state_rules.jpeg", "busy-234"),
    ("U005440", "BACK-MATTER/NOTES/_page_904_busy_beaver_5_state_rule.jpeg", "busy-5"),
]:
    add_support(
        busy,
        label=label,
        unit=unit,
        image_path=path,
        claim="Original-resolution inspection confirms the printed witness rule table.",
        fields=["result_kind", "parameters_and_variants", "evidence_limit"],
        strength="CORROBORATING",
        modality="IMAGE",
    )

# Substitution systems, sequence objects, and digit transducers.
substitution = transition(
    key="neighbor-independent-substitution",
    name="neighbor-independent parallel substitution system class",
    anchor="U005446",
    object_kind="A parallel symbol-to-block substitution system.",
    carrier="A finite list or string over a finite alphabet.",
    state="The complete current word.",
    law="Replace every symbol by its rule block simultaneously and concatenate the blocks.",
    result="A unique next word and, under NestList, a retained evolution.",
    input_text="A symbol-to-block rule, initial word, and step count.",
    neighborhood="Each symbol is read independently.",
    parameters="Alphabet, replacement blocks, initial word, representation, and steps.",
)
substitution["facts"]["visible_history"] = (
    "The list and string implementations use NestList to retain successive words."
)
for unit, label in [("U005447", "list"), ("U005450", "string")]:
    add_support(
        substitution,
        label=f"substitution-{label}",
        unit=unit,
        claim="The implementation iterates simultaneous symbol replacement.",
        fields=["schedule", "rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit", "visible_history"],
        modality="CODE",
    )

dependent_sub = transition(
    key="neighbor-dependent-substitution",
    name="neighbor-dependent parallel substitution system class",
    anchor="U005451",
    object_kind="A parallel block-to-block substitution system.",
    carrier="A finite word over a finite alphabet.",
    state="The current complete word.",
    law="Partition into overlapping adjacent pairs, replace each pair, flatten the results.",
    result="A unique next word for a complete nonoverlapping output convention.",
    input_text="A pair-to-block rule, initial word, and step count.",
    neighborhood="Each adjacent two-symbol block.",
    parameters="Alphabet, pair rule, initial word, partition/boundary convention, and steps.",
)
dependent_sub["facts"]["visible_history"] = (
    "SS2EvolveList retains the successive words produced by the pair rule."
)
add_support(
    dependent_sub,
    label="neighbor-dependent-rule",
    unit="U005452",
    claim="The code block supplies the four binary pair replacements.",
    fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
    modality="TABLE",
)
add_support(
    dependent_sub,
    label="neighbor-dependent-step",
    unit="U005454",
    claim="SS2EvolveList fixes overlapping-pair partition, replacement, flattening, and iteration.",
    fields=["schedule", "read_dependencies_or_neighborhood", "write_replacement_assembly_or_commit", "visible_history"],
    modality="CODE",
)

direct_object(
    key="successive-digits-sequence",
    name="alternating successive-digits sequence",
    anchor="U005457",
    object_kind="A binary sequence indexed by positive positions.",
    input_text="A positive position n.",
    law="Return black for odd n and white for even n.",
    result="The uniquely determined binary sequence value.",
    parameters="Position n and optional prefix length 2^t.",
)
thue = direct_object(
    key="thue-morse",
    name="Thue-Morse binary sequence",
    anchor="U005458",
    object_kind="A recursively and digit-count-defined infinite binary sequence.",
    input_text="A positive position n or requested finite prefix.",
    law=(
        "s[n]=1-Mod[DigitCount[n-1,2,1],2], equivalently the stated parity "
        "recurrence or iterative complement-and-join constructor."
    ),
    result="The binary value s[n] or the requested prefix.",
    parameters="Position n or prefix exponent/length.",
)
add_support(
    thue,
    label="thue-polynomial",
    unit="U005459",
    claim="The product coefficient formula gives the first 2^m sequence values.",
    fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
    modality="FORMULA",
)

direct_object(
    key="fibonacci-substitution-sequence",
    name="Fibonacci-related substitution sequence",
    anchor="U005463",
    object_kind="A recursively concatenated binary sequence family.",
    input_text="A step t or positive position n.",
    law=(
        "a[t]=Join[a[t-1],a[t-2]] with a[1]={0}, a[2]={0,1}; the nth "
        "value is also given by the stated GoldenRatio floor difference."
    ),
    result="The finite word at step t or its nth binary value.",
    parameters="Step t, position n, and the stated initial words.",
)
cantor_seq = direct_object(
    key="cantor-digit-sequence",
    name="ternary Cantor-set membership sequence",
    anchor="U005464",
    object_kind="A binary sequence indicating absence of digit 1 in n-1 base 3.",
    input_text="A positive position n.",
    law="Return 1 iff IntegerDigits[n-1,3] contains no 1; otherwise return 0.",
    result="The binary Cantor-set membership indicator.",
    parameters="Position n or prefix step t.",
)
add_support(
    cantor_seq,
    label="cantor-binomial",
    unit="U005465",
    claim="The source supplies an equivalent binomial-modulo-three formula.",
    fields=["rule_relation_constraint_function_or_probability_law", "excluded_observers_and_representations"],
    modality="FORMULA",
)

direct_object(
    key="substitution-growth-analyzer",
    name="substitution-system color-count matrix analyzer",
    anchor="U005468",
    object_kind="A matrix method for exact and asymptotic symbol counts.",
    input_text="A neighbor-independent substitution rule, initial color-count vector, and step t.",
    law=(
        "Form m[i,j] from replacement-block counts; return init.MatrixPower[m,t], "
        "with largest eigenvalue/eigenvector giving asymptotic growth and proportions."
    ),
    result="Exact per-color counts and stated asymptotic growth data.",
    parameters="Rule alphabet, count matrix, initial counts, and step.",
)

fibonacci = direct_object(
    key="fibonacci-numbers",
    name="Fibonacci number sequence",
    anchor="U005469",
    object_kind="An integer sequence defined by a second-order recurrence.",
    input_text="A positive integer n.",
    law="f[n]=f[n-1]+f[n-2] with f[1]=f[2]=1.",
    result="The nth Fibonacci integer.",
    parameters="Index n and the stated initial values.",
)
add_support(
    fibonacci,
    label="fibonacci-recurrence",
    unit="U005470",
    claim="The fenced recurrence and initial conditions give the complete sequence.",
    fields=["rule_relation_constraint_function_or_probability_law", "result_kind"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)
add_support(
    fibonacci,
    label="fibonacci-fast",
    unit="U005482",
    claim="The binary-fold algorithm is an exact fast evaluator.",
    fields=["excluded_observers_and_representations", "parameters_and_variants"],
    modality="CODE",
)

golden = direct_object(
    key="golden-ratio",
    name="GoldenRatio algebraic constant",
    anchor="U005488",
    object_kind="A uniquely selected positive algebraic constant.",
    input_text="No varying native input; equivalent defining equations are supplied.",
    law="Select the positive solution of x=1+1/x, namely (1+Sqrt[5])/2.",
    result="The real constant GoldenRatio.",
    parameters="Equivalent equation, geometric, trigonometric, and fixed-point representations.",
)
add_support(
    golden,
    label="golden-equation",
    unit="U005489",
    claim="The source supplies the defining equations.",
    fields=["rule_relation_constraint_function_or_probability_law", "result_kind"],
    modality="FORMULA",
)

direct_object(
    key="lucas-numbers",
    name="Lucas number sequence",
    anchor="U005498",
    object_kind="An integer sequence with the Fibonacci recurrence and distinct seeds.",
    input_text="A positive integer n.",
    law="f[n]=f[n-1]+f[n-2] with f[1]=1 and f[2]=3.",
    result="The nth Lucas integer.",
    parameters="Index n and the stated initial values.",
)
direct_object(
    key="linear-recurrence-sequences",
    name="generalized linear-recurrence sequence class",
    anchor="U005501",
    object_kind="A class of sequences generated by fixed linear recurrence relations.",
    input_text="A recurrence, initial values, and index n.",
    law="Iterate the supplied linear recurrence from its supplied initial values.",
    result="The uniquely determined sequence value at n.",
    parameters="Recurrence order/coefficients, initial values, and n.",
)
direct_object(
    key="perrin-sequence",
    name="Perrin integer sequence",
    anchor="U005501",
    object_kind="A third-order integer recurrence sequence.",
    input_text="A nonnegative index n.",
    law="f[n]=f[n-2]+f[n-3], with f[0]=3, f[1]=0, f[2]=2.",
    result="The nth Perrin integer.",
    parameters="Index n and the three stated initial values.",
)

digit_fa = transition(
    key="digit-finite-automaton",
    name="finite automaton digit-sequence transducer",
    anchor="U005504",
    object_kind="A finite-state machine reading a base-k digit stream.",
    carrier="A finite state set and a sequence of base-k input digits.",
    state="The current finite state plus unread input suffix.",
    law="Use the current-state row and next digit to select the successor state.",
    result="A final state/output value or generated prefix.",
    input_text="A transition table and IntegerDigits[n-1,k].",
    neighborhood="The current state and next input digit.",
    parameters="State set, input base k, transition table, start state, and input integer.",
    termination="Evaluation completes after the finite digit sequence is consumed.",
)
add_support(
    digit_fa,
    label="digit-fa-code",
    unit="U005505",
    claim="The Fold and Nest formulas give exact nth-element and prefix evaluation.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "termination_completion_failure",
        "result_kind",
    ],
    modality="CODE",
)

direct_object(
    key="fibonacci-digit-representation",
    name="Fibonacci-weighted binary digit representation",
    anchor="U005506",
    object_kind="A numeral relation using Fibonacci positional weights.",
    input_text="A finite 0/1 digit sequence.",
    law="Map digits a[i] to Sum[a[i] Fibonacci[i+2]].",
    result="The represented nonnegative integer; uniqueness requires no adjacent 1 digits.",
    parameters="Digit sequence length and the no-adjacent-ones restriction.",
)

paper = direct_object(
    key="paperfolding-sequence",
    name="paperfolding crease sequence",
    anchor="U005515",
    object_kind="A binary sequence generated by repeated half-folding.",
    input_text="A nonnegative fold count t.",
    law="Iterate Join[#, {0}, Reverse[1-#]] starting from {0}.",
    result="The up/down crease sequence after t folds.",
    parameters="Fold count t and the stated orientation encoding.",
)
add_support(
    paper,
    label="paperfolding-path",
    unit="U005516",
    image_path="BACK-MATTER/NOTES/_page_907_Picture_11.jpeg",
    claim="Original-resolution inspection confirms the successive right-angle path rendering.",
    fields=["excluded_observers_and_representations", "evidence_limit"],
    strength="CORROBORATING",
    modality="IMAGE",
)

direct_object(
    key="period-doubling-sequence",
    name="period-doubling binary sequence",
    anchor="U005520",
    object_kind="A recursively doubled binary sequence.",
    input_text="A step t or positive index n.",
    law=(
        "Iterate MapAt[1-#&,Join[#,#],-1] from {0}; equivalently return "
        "Mod[IntegerExponent[n,2],2] for the nth term."
    ),
    result="The finite step-t word or nth binary value.",
    parameters="Step t or index n.",
)
direct_object(
    key="parity-sequence",
    name="modulo-two parity sequence",
    anchor="U005521",
    object_kind="A binary sequence defined directly by index parity.",
    input_text="A positive integer n.",
    law="Return Mod[n,2].",
    result="The nth binary value.",
    parameters="Index n.",
)
direct_object(
    key="doubled-period-sequence",
    name="doubled-symbol period-doubling sequence",
    anchor="U005522",
    object_kind="A sequence obtained by expanding every 1 of the period-doubling sequence.",
    input_text="A period-doubling sequence prefix.",
    law="Replace every 1 by {1,1}.",
    result="The expanded binary sequence.",
    parameters="Underlying prefix length.",
)
direct_object(
    key="sqrt2-sturmian-d",
    name="page-84(d) square-root-two Sturmian sequence",
    anchor="U005523",
    object_kind="A binary Sturmian sequence with a floor-difference formula.",
    input_text="A positive index n.",
    law=(
        "With f=Floor[(1-1/Sqrt[2])(# + 1/Sqrt[2])]&, return f[n+1]-f[n]."
    ),
    result="The nth binary value.",
    parameters="Index n.",
)
direct_object(
    key="sqrt2-sequence-f",
    name="page-84(f) square-root-two floor-difference sequence",
    anchor="U005525",
    object_kind="An integer sequence defined by consecutive floor differences.",
    input_text="A nonnegative index n.",
    law="Return Floor[Sqrt[2](n+1)]-Floor[Sqrt[2]n].",
    result="The nth sequence value.",
    parameters="Index n.",
)

# Sequential substitutions, tag systems, cyclic tags, and register machines.
sequential = transition(
    key="sequential-substitution",
    name="left-to-right sequential substitution system class",
    anchor="U005537",
    object_kind="A word-rewriting system applying one eligible replacement per step.",
    carrier="A flat symbolic word s[...] over a finite alphabet.",
    state="The complete current symbolic word.",
    law=(
        "Scan using Mathematica replacement order and apply the first matching "
        "subword rule once; repeat with NestList."
    ),
    result="A unique next word under the stated rule order.",
    input_text="An ordered rule list, initial word, and step count.",
    neighborhood="Any matching contiguous subword under Flat associativity.",
    parameters="Alphabet, ordered rules, initial word, matching order, and steps.",
    termination="Evolution stops natively when no replacement applies.",
)
sequential["facts"]["visible_history"] = (
    "SSSEvolveList retains the successive words produced by the ordered rules."
)
add_support(
    sequential,
    label="sequential-evolve",
    unit="U005544",
    claim="SSSEvolveList gives the exact single-replacement iteration.",
    fields=["schedule", "rule_relation_constraint_function_or_probability_law", "visible_history"],
    modality="CODE",
)
add_support(
    sequential,
    label="sequential-order",
    unit="U005547",
    claim="The source states failure-to-match stopping and rule-order dependence.",
    fields=["schedule", "termination_completion_failure", "parameters_and_variants"],
)

preset(
    key="sequential-sort",
    name="binary sequential-substitution sorting preset",
    anchor="U005546",
    law="Repeatedly replace s[1,0] by s[0,1] until no inversion remains.",
    family="sequential substitution systems",
    aliases=["binary swap sorting rule"],
)

tag = transition(
    key="tag-system",
    name="block-prefix tag system class",
    anchor="U005550",
    object_kind="A sequence system deleting a fixed prefix and appending a lookup block.",
    carrier="A finite word over k colors.",
    state="The complete current word.",
    law=(
        "If length is at least n, drop the first n elements and append the "
        "block selected by those n elements; otherwise return the empty word."
    ),
    result="A unique next word.",
    input_text="Deletion number n, prefix-to-block rule, and initial word.",
    neighborhood="The first n elements of the current word.",
    parameters="n, k, maximum appended length r, rule table, and initial word.",
    termination="Words shorter than n map to the empty terminal word.",
)
add_support(
    tag,
    label="tag-step",
    unit="U005553",
    claim="TSEvolveList gives exact deletion, lookup, append, and short-word behavior.",
    fields=[
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
    ],
    modality="CODE",
)

preset(
    key="tag-case-a",
    name="page-94(a) binary tag-system preset",
    anchor="U005551",
    law="Delete two elements and append the block selected by the displayed four-prefix table.",
    family="block-prefix tag systems",
    modality="TABLE",
)

post_class = transition(
    key="post-tag",
    name="Post first-symbol tag system class",
    anchor="U005558",
    object_kind="A tag-system restriction whose appended block depends only on the first symbol.",
    carrier="A finite word over a finite alphabet.",
    state="The complete current word.",
    law="Delete a fixed number of leading symbols and append the block selected by the first symbol.",
    result="A unique next word.",
    input_text="Deletion number, first-symbol lookup table, and initial word.",
    neighborhood="The first symbol chooses the append block; a fixed prefix is deleted.",
    parameters="Alphabet, deletion number, append table, and initial word.",
    termination="The source discusses eventual cycles and short-word stopping but not one universal completion law.",
)
preset(
    key="post-three-delete",
    name="Post binary three-symbol-deletion tag preset",
    anchor="U005558",
    law="{0,_,_}->{0,0}; {1,_,_}->{1,1,0,1}, deleting three symbols per step.",
    family="Post first-symbol tag systems",
    modality="TABLE",
)
preset(
    key="post-three-color",
    name="three-color two-symbol-deletion Post tag preset",
    anchor="U005558",
    law="{0,_}->{2,1}; {1,_}->{0}; {2,_}->{0,2,1,2}, deleting two symbols per step.",
    family="Post first-symbol tag systems",
    modality="TABLE",
)

cyclic = transition(
    key="cyclic-tag",
    name="binary cyclic tag system class",
    anchor="U005560",
    object_kind="A tag system that cycles through an ordered list of append blocks.",
    carrier="A finite binary word plus a cyclic rule-block list.",
    state="The pair {current rule rotation,current word}.",
    law=(
        "Remove the leftmost bit, rotate the rule list, and append the current "
        "block iff the removed bit is 1; an empty word remains empty."
    ),
    result="A new rule rotation and word.",
    input_text="An ordered cyclic block list and initial binary word.",
    neighborhood="The leftmost bit and current rule block.",
    parameters="Rule-block cycle, initial word, and step count.",
    termination="The empty word is absorbing.",
)
cyclic["facts"]["control_state"] = (
    "The current rotation of the ordered append-block list."
)
add_support(
    cyclic,
    label="cyclic-code",
    unit="U005561",
    claim="CTStep and CTEvolveList give the complete binary step and empty-word law.",
    fields=[
        "complete_state",
        "control_state",
        "schedule",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)

multivalue_cyclic = transition(
    key="multivalue-cyclic-tag",
    name="nonnegative-integer-valued cyclic tag system class",
    anchor="U005564",
    object_kind="A cyclic tag system whose leading element is a repetition count.",
    carrier="A finite list of nonnegative integers plus a cyclic block list.",
    state="The current rule rotation and integer-valued list.",
    law="Remove leading n, rotate, and append n copies of the current rule block.",
    result="A new rotation and list.",
    input_text="A cyclic block list and integer-valued initial list.",
    neighborhood="The leading integer and current rule block.",
    parameters="Rule cycle, integer value domain, initial list, and steps.",
    termination="The source inherits the empty-list stopping behavior.",
)
add_support(
    multivalue_cyclic,
    label="multivalue-step",
    unit="U005565",
    claim="The CTStep rule gives the exact n-copy append law.",
    fields=["rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit"],
    modality="CODE",
)

preset(
    key="cyclic-substitution-restriction",
    name="block-length-divisible cyclic-tag substitution restriction",
    anchor="U005571",
    law=(
        "Require every block length to be divisible by the block-count n; "
        "then addition times are predetermined and behavior corresponds to a "
        "neighbor-independent substitution system."
    ),
    family="cyclic tag systems",
    aliases=["substitution-equivalent cyclic tag systems"],
)

direct_object(
    key="kolakoski",
    name="Kolakoski self-run-length sequence",
    anchor="U005573",
    object_kind="A self-descriptive integer sequence over {1,2}.",
    input_text="A positive position or requested prefix length.",
    law="The sequence equals the list of lengths of its own consecutive equal-symbol runs.",
    result="The uniquely constrained {1,2} sequence prefix under the stated initial convention.",
    parameters="Prefix length and the initial 1,2,2,1,1,2 convention.",
)

register = transition(
    key="register-machine",
    name="increment/decrement-jump register machine class",
    anchor="U005575",
    object_kind="A finite program counter operating on nonnegative integer registers.",
    carrier="A finite instruction list and finite register vector.",
    state="The pair {program counter,register list}.",
    law=(
        "Increment advances and adds one; decrement-jump decrements a positive "
        "register and jumps, otherwise advances without decrement."
    ),
    result="A new program counter and register vector.",
    input_text="A program, initial program counter/register vector, and step count.",
    neighborhood="The current instruction and the register(s) it names.",
    parameters="Program length, register count, instruction list, initial values, and steps.",
    termination="RMStep leaves states beyond the program unchanged; a halt interpretation is separately stated.",
)
register["facts"]["control_state"] = "The current one-based program counter."
add_support(
    register,
    label="register-code",
    unit="U005579",
    claim="RMStep/RMExecute give exact increment, conditional decrement-jump, and iteration.",
    fields=[
        "complete_state",
        "control_state",
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "termination_completion_failure",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)

preset(
    key="register-page99",
    name="page-99 two-register machine preset",
    anchor="U005576",
    law="Execute {i[1],d[2,1],i[2],d[1,3],d[2,1]} under the stated register semantics.",
    family="increment/decrement-jump register machines",
    modality="CODE",
)
preset(
    key="register-halt-convention",
    name="beyond-program register-machine halt convention",
    anchor="U005581",
    law="Enter a distinguished halt state when the program counter addresses beyond the program.",
    family="register machines",
)
preset(
    key="register-max8",
    name="length-eight 1280-step register-machine preset",
    anchor="U005581",
    law="The displayed eight-instruction program runs 1280 steps before halting from {1,{0,0}}.",
    family="increment/decrement-jump register machines",
)
add_support(
    next(item for item in base.ALL_CANDIDATE_SPECS if item["key"] == "register-max8"),
    label="register-max8-program",
    unit="U005582",
    claim="The code block gives the exact eight-instruction witness program.",
    fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
    modality="CODE",
)

extended_register = transition(
    key="extended-register",
    name="extended-instruction register machine class",
    anchor="U005583",
    object_kind="A register machine extended with equality branch, addition, and indirect jump.",
    carrier="A finite program and register vector.",
    state="The program counter and register list.",
    law=(
        "eq compares two registers and conditionally jumps; add adds one "
        "register into another; jmp takes its next counter from a register."
    ),
    result="A unique next program counter and register state.",
    input_text="An extended program and initial register-machine state.",
    neighborhood="The current instruction and referenced registers.",
    parameters="Base and extended instruction repertoire, program, registers, and initial state.",
    termination="No additional completion law beyond program-counter behavior is stated.",
)
add_support(
    extended_register,
    label="extended-register-code",
    unit="U005584",
    claim="The three RMExecute definitions fix the extended instructions.",
    fields=["rule_relation_constraint_function_or_probability_law", "write_replacement_assembly_or_commit"],
    modality="CODE",
)

# Symbolic and operator systems.
symbolic = transition(
    key="symbolic-system",
    name="page-103 symbolic expression rewriting system",
    anchor="U005589",
    object_kind="A symbolic-expression rewrite system.",
    carrier="Untyped nested expressions built from the symbol e.",
    state="The complete current expression.",
    law="Apply e[x_][y_] -> x[x[y]] once per step under Mathematica replacement order.",
    result="A unique next expression under the stated scan order.",
    input_text="An initial expression and step count.",
    neighborhood="A matching expression subtree, potentially nonlocal in linear representations.",
    parameters="Rewrite rule, initial expression, replacement order, and steps.",
    termination="Evolution reaches a fixed point for the stated page-103 system.",
)

expression_enum = direct_object(
    key="symbolic-expression-enumerator",
    name="fixed-leaf-count symbolic expression enumerator",
    anchor="U005601",
    object_kind="A recursive generator of all binary application expressions of fixed leaf count.",
    input_text="A finite symbol set s and positive leaf count n.",
    law=(
        "c[s,1]=s; for n>1, combine every split n-m,m with Outer[#1[#2]&,...]."
    ),
    result="The complete list of expressions with LeafCount n.",
    parameters="Symbol set s and leaf count n.",
)
add_support(
    expression_enum,
    label="expression-enum-code",
    unit="U005603",
    claim="The recursive code gives the complete generator.",
    fields=["rule_relation_constraint_function_or_probability_law", "result_kind"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CODE",
)

transition(
    key="nested-r-symbolic",
    name="nested-r symbolic rewrite family",
    anchor="U005610",
    object_kind="A symbolic rewrite family parameterized by repetition count r.",
    carrier="Nested symbolic expressions.",
    state="The complete current expression.",
    law="Rewrite e[x_][y_] to Nest[x,y,r].",
    result="A next expression and eventually a fixed point for the stated family.",
    input_text="Parameter r, initial expression, and step count.",
    neighborhood="A matching e[x][y] subtree.",
    parameters="Positive repetition parameter r, initial expression, and scan order.",
    termination="The source states eventual fixed points, with potentially tower-like halting time.",
)

operator = transition(
    key="operator-system",
    name="one-way operator-pattern rewriting system class",
    anchor="U005620",
    object_kind="A symbolic operator system applying a pattern axiom one way once per step.",
    carrier="Operator expressions or their parenthesis encodings.",
    state="The complete current operator expression.",
    law="Apply the supplied Mathematica-pattern rewrite once per step using ReplaceAll order.",
    result="A unique next expression under the stated ordering.",
    input_text="A pattern rule, initial expression, and step count.",
    neighborhood="Any subtree matching the left-hand operator pattern.",
    parameters="Pattern rule, operator alphabet, initial expression, order, and steps.",
    termination="No general completion law is stated.",
)

for key, anchor, name, law, image_unit, image_path in [
    ("operator-dup", "U005621", "balanced-duplication operator-system preset", "x_ -> x ∘ x", "U005622", "BACK-MATTER/NOTES/_page_913_Picture_8.jpeg"),
    ("operator-swap", "U005623", "swap-and-copy operator-system preset", "x_ ∘ y_ -> (y ∘ x) ∘ y", "U005624", "BACK-MATTER/NOTES/_page_913_Picture_9.jpeg"),
    ("operator-double", "U005625", "double-square operator-system preset", "x_ ∘ y_ -> (y ∘ y) ∘ (x ∘ x)", "U005626", "BACK-MATTER/NOTES/_page_913_Picture_10.jpeg"),
    ("operator-right", "U005627", "right-duplicating operator-system preset", "x_ ∘ y_ -> y ∘ (x ∘ x)", "U005628", "BACK-MATTER/NOTES/_page_913_Picture_11.jpeg"),
]:
    spec = preset(
        key=key,
        name=name,
        anchor=anchor,
        law=law,
        family="one-way operator-pattern rewriting systems",
        modality="FORMULA",
    )
    add_support(
        spec,
        label=f"{key}-image",
        unit=image_unit,
        image_path=image_path,
        claim="Original-resolution inspection confirms the displayed parenthesis pattern.",
        fields=["result_kind", "excluded_observers_and_representations"],
        strength="CORROBORATING",
        modality="IMAGE",
    )


# Cross-reference obligations, in source order.
def route(
    key: str,
    unit: str,
    literal: str,
    topic: str,
    vocabulary: list[str],
    scope: str = "CROSS_RANGE",
) -> None:
    base.add_route(
        key=key,
        unit=unit,
        literal=literal,
        topic=topic,
        vocabulary=vocabulary,
        scope=scope,
    )


for args in [
    ("gray-code", "U005328", "page 901", "Gray-code rule ordering", ["Gray code", "rule ordering"]),
    ("algebraic-ca", "U005329", "page 869", "Boolean/algebraic cellular-rule representations", ["algebraic forms", "cellular automata"]),
    ("rule150-nested", "U005340", "page 892", "period-doubling nested sequence", ["rule 150", "nested sequence"]),
    ("gegenbauer", "U005340", "page 612", "Gegenbauer cell-value relation", ["GegenbauerC", "cell value"]),
    ("rule225-seeds", "U005341", "page 951", "Rule 225 complex initial conditions", ["rule 225", "initial conditions"]),
    ("rule22-seeds", "U005342", "page 263", "Rule 22 complex initial conditions", ["rule 22", "initial conditions"]),
    ("higher-dimensional-ca", "U005363", "page 927", "higher-dimensional cellular automata", ["higher-dimensional", "cellular automata"]),
    ("builtin-ca", "U005370", "page 867", "built-in CellularAutomaton semantics", ["CellularAutomaton", "built-in"]),
    ("code420-pascal", "U005371", "page 870", "Pascal modulo-k additive construction", ["code 420", "Pascal", "modulo 3"]),
    ("ca-composition", "U005372", "page 956", "cellular-automaton composition mechanics", ["composition", "cellular automata"]),
    ("algebraic-systems", "U005373", "page 1094", "finite algebraic-system operations", ["algebraic systems", "multiplication table"]),
    ("semigroup", "U005384", "page 805", "semigroup associativity mechanics", ["semigroup", "associative"]),
    ("groups", "U005385", "page 945", "finite group construction", ["group", "inverses"]),
    ("abelian", "U005385", "page 955", "Abelian group/additive nesting relation", ["Abelian", "nested"]),
    ("mobile-compression", "U005400", "page 488", "mobile-automaton compressed evolution", ["mobile automata", "compression"]),
    ("mobile-pages73", "U005404", "pages 73, 74 and 75", "mobile-automaton rule tables for motion plots", ["active cell", "mobile automata"], "WITHIN_STAGE"),
    ("tm-alt", "U005418", "page 1143", "alternative Turing-machine implementation", ["Turing machine", "implementation"]),
    ("tm-equivalence", "U005420", "page 1120", "Turing-machine rule equivalence", ["Turing machine", "equivalence"]),
    ("tm-complex", "U005425", "page 709", "complex small Turing-machine presets", ["Turing machine", "complex behavior"]),
    ("tm-foundations", "U005435", "page 1128", "Turing-machine calculation model", ["Turing", "calculation"]),
    ("tm-universality", "U005435", "page 1110", "Turing-machine capabilities", ["Turing machines", "capabilities"]),
    ("tm-constructions", "U005436", "page 1119", "small universal Turing-machine constructions", ["Minsky", "Turing machine"]),
    ("busy-six", "U005441", "page 1144", "large-state Busy Beaver bounds", ["Busy Beaver", "halting"]),
    ("thue-polynomial", "U005458", "page 1081", "Thue-Morse polynomial relation", ["Thue-Morse", "polynomial"]),
    ("thue-series", "U005460", "page 1092", "Thue-Morse generating series", ["Thue-Morse", "series"]),
    ("fibonacci-slope", "U005463", "page 904", "quadratic-irrational projection sequences", ["Fibonacci-related", "GoldenRatio"]),
    ("fibonacci-period", "U005485", "page 975", "Fibonacci modulo-k periods", ["Fibonacci", "modulo"]),
    ("golden-angle", "U005497", "page 1006", "GoldenRatio angular point generator", ["GoldenRatio", "circle"]),
    ("recurrences", "U005501", "page 128", "general recurrence-relation systems", ["recurrence relations", "sequences"], "CROSS_RANGE"),
    ("digit-patterns", "U005502", "page 117", "digit-sequence nested construction", ["digit sequences", "nested"]),
    ("zeckendorf", "U005506", "page 1070", "unique Fibonacci digit representations", ["Fibonacci", "digit representation"]),
    ("sub-square-root", "U005507", "page 904", "substitution sequences as irrational-slope projections", ["substitution systems", "square roots"]),
    ("sub-spectra", "U005508", "page 1080", "spectra of substitution systems", ["substitution", "spectra"]),
    ("path-2d", "U005511", "page 190", "two-dimensional geometrical substitution systems", ["path", "2D substitution"], "CROSS_RANGE"),
    ("paperfolding", "U005515", "page 189", "paperfolding/geometrical substitution construction", ["paperfolding", "path"], "CROSS_RANGE"),
    ("l-systems", "U005530", "page 1005", "L-system plant-generation mechanics", ["L systems", "branching plants"]),
    ("geometric-sub", "U005534", "page 189", "two-dimensional geometrical substitution systems", ["geometrical substitution", "paths"], "CROSS_RANGE"),
    ("multiway-order", "U005547", "page 497", "multiway all-replacements semantics", ["multiway systems", "replacements"]),
    ("confluence", "U005547", "page 1036", "confluence/Church-Rosser property", ["confluence", "replacement order"]),
    ("multiway", "U005548", "page 938", "multiway string-rewriting systems", ["multiway systems", "string rewriting"]),
    ("tag-syntax", "U005558", "page 1149", "Post syntactic reduction systems", ["Post", "tag systems"]),
    ("tag-first", "U005558", "page 670", "first-symbol tag-system restriction", ["tag system", "first element"], "CROSS_RANGE"),
    ("tag-computation", "U005558", "pages 1113 and 1141", "tag-system computational mechanics", ["tag systems", "computation"]),
    ("register-halt", "U005581", "page 1137", "register-machine halting semantics", ["register machine", "halt"]),
    ("random-programs", "U005587", "page 1182", "random program generation", ["random programs", "register machine"]),
    ("polish", "U005593", "page 1173", "Polish symbolic-expression representation", ["Polish notation", "symbolic expressions"]),
    ("balanced", "U005604", "page 989", "balanced bracket sequence construction", ["balanced brackets", "expressions"]),
    ("church", "U005605", "page 1122", "Church numeral interpretation", ["Church numeral", "symbolic system"]),
    ("symbolic-halting", "U005610", "page 1145", "symbolic-system halting-time growth", ["symbolic systems", "halting"]),
    ("arithmetic-axioms", "U005610", "page 1163", "arithmetic axiom-system independence", ["axiom system", "halting"]),
    ("church-rosser", "U005617", "page 1036", "Church-Rosser fixed-point independence", ["Church-Rosser", "fixed point"]),
    ("combinators", "U005618", "page 1121", "combinator rewrite mechanics", ["combinators", "Schönfinkel"]),
    ("operator-axioms", "U005620", "page 1172", "operator-system axioms", ["operator systems", "axioms"]),
    ("network-substitution", "U005629", "page 508", "network substitution systems", ["network substitution", "symbolic systems"]),
    ("network-paths", "U005629", "page 277", "infinite path-tree unfolding of networks", ["network", "infinite tree"]),
    ("lorenz", "U005635", "page 971", "Lorenz differential-equation dynamics", ["Lorenz", "chaos"]),
    ("iterated-maps", "U005635", "page 921", "iterated-map universal behavior", ["iterated maps", "Feigenbaum"]),
]:
    route(*args)


HISTORICAL_UNITS = {
    "U005321",
    "U005328",
    "U005435",
    "U005436",
    "U005483",
    "U005529",
    "U005530",
    "U005531",
    "U005532",
    "U005533",
    "U005534",
    "U005535",
    "U005548",
    "U005558",
    "U005573",
    "U005586",
    "U005618",
    "U005619",
    "U005635",
}

DEFECT_ASSETS = {
    "BACK-MATTER/NOTES/_page_902_Figure_24.jpeg": (
        "The unreferenced physical asset is an orphaned text strip duplicating "
        "the opening of U005406 rather than a figure.",
        ["TEXT_BEARING", "CAPTION_INCOMPLETE"],
    ),
    "BACK-MATTER/NOTES/_page_906_golden_ratio_rectangle.jpeg": (
        "The 22×22 raster is too degraded to carry the intended similarity "
        "geometry independently; the adjacent prose and alt text remain clear.",
        ["CONSTRUCTION_BEARING", "AMBIGUOUS", "CAPTION_INCOMPLETE"],
    ),
}

ORIGINAL_REVIEWED = {
    "BACK-MATTER/NOTES/_page_898_Picture_8.jpeg",
    "BACK-MATTER/NOTES/_page_900_Picture_28.jpeg",
    "BACK-MATTER/NOTES/_page_900_Picture_29.jpeg",
    "BACK-MATTER/NOTES/_page_900_Picture_30.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_1.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_21.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_22.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_23.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_25.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_26.jpeg",
    "BACK-MATTER/NOTES/_page_901_Picture_27.jpeg",
    "BACK-MATTER/NOTES/_page_902_Figure_23.jpeg",
    "BACK-MATTER/NOTES/_page_902_Figure_24.jpeg",
    "BACK-MATTER/NOTES/_page_904_busy_beaver_2_3_4_state_rules.jpeg",
    "BACK-MATTER/NOTES/_page_904_busy_beaver_5_state_rule.jpeg",
    "BACK-MATTER/NOTES/_page_906_golden_ratio_rectangle.jpeg",
    "BACK-MATTER/NOTES/_page_907_Picture_11.jpeg",
    "BACK-MATTER/NOTES/_page_907_Picture_7.jpeg",
    "BACK-MATTER/NOTES/_page_907_Picture_9.jpeg",
    "BACK-MATTER/NOTES/_page_907_rule_b_path_evolution.jpeg",
    "BACK-MATTER/NOTES/_page_910_cyclic_tag_trough.jpeg",
    "BACK-MATTER/NOTES/_page_911_symbolic_representation_table.jpeg",
    "BACK-MATTER/NOTES/_page_912_Figure_19.jpeg",
    "BACK-MATTER/NOTES/_page_912_Figure_21.jpeg",
    "BACK-MATTER/NOTES/_page_913_Picture_8.jpeg",
    "BACK-MATTER/NOTES/_page_913_Picture_9.jpeg",
    "BACK-MATTER/NOTES/_page_913_Picture_10.jpeg",
    "BACK-MATTER/NOTES/_page_913_Picture_11.jpeg",
}


def build(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    manifest = json.loads((bundle / "allowed-manifest.json").read_text())
    if (
        manifest.get("worker_id") != WORKER
        or manifest.get("content_set_sha256") != BUNDLE_HASH
        or manifest.get("source_paths") != [SOURCE_PATH]
        or manifest.get("source_unit_count") != 318
        or manifest.get("asset_count") != 46
        or manifest.get("stage") != 7
        or manifest.get("discovery_epoch") != 1
    ):
        raise AuthoringError("bundle identity differs from the sealed Stage 7 Notes assignment")

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
        raise AuthoringError("output is not the pristine nonsemantic worksheet")

    (
        candidate_proposals,
        route_proposals,
        candidate_links_by_unit,
        candidate_links_by_image,
        anchor_candidate_links_by_unit,
    ) = base.allocate_semantic_records(reading_input, asset_input)
    for candidate in candidate_proposals:
        candidate["discovery_stage"] = 7
        for text in candidate["missing_mechanics"]:
            if "assigned Chapter 2 evidence" in text:
                raise AuthoringError("stale Chapter 2 candidate boundary")
    for proposal in route_proposals:
        proposal["owning_stage"] = "7"

    sorted_specs = sorted(
        base.ALL_CANDIDATE_SPECS,
        key=lambda spec: next(
            i for i, candidate in enumerate(candidate_proposals)
            if candidate["provisional_name"] == spec["name"]
            and candidate["discovery_anchor"]["id"] == spec["anchor"]
        ),
    )
    specs_by_id = dict(zip((c["id"] for c in candidate_proposals), sorted_specs))
    route_links: defaultdict[str, list[str]] = defaultdict(list)
    for proposal in route_proposals:
        route_links[proposal["source_unit_id"]].append(proposal["route_id"])

    reading_updates: list[dict[str, str]] = []
    for original in reading_input:
        row = deepcopy(original)
        unit = row["source_unit_id"]
        candidates = candidate_links_by_unit.get(unit, [])
        routes = route_links.get(unit, [])
        if candidates:
            is_anchor = bool(
                set(candidates) & set(anchor_candidate_links_by_unit.get(unit, []))
            )
            disposition = "CANDIDATE" if is_anchor else "SUPPORTS_CANDIDATE"
            roles: list[str] = []
            if row["block_kind"] in {"fenced_code", "image"}:
                roles.append("REPRESENTATION")
            if unit in HISTORICAL_UNITS:
                roles.append("HISTORICAL_MENTION")
            statement = (
                f"This unit {'discovers' if is_anchor else 'supports'} "
                f"{', '.join(candidates)} with source-grounded identity, native "
                "mechanics, a formal denotation, or an explicit evidence limit."
            )
            if routes:
                statement += f" It also opens {', '.join(routes)}."
        elif routes:
            disposition = "CROSS_REFERENCE"
            roles = ["CONTROL_OR_COMPARISON"]
            if unit in HISTORICAL_UNITS:
                roles.append("HISTORICAL_MENTION")
            statement = (
                f"Reviewed in full; this unit principally opens {', '.join(routes)} "
                "to construction-bearing targets not completed here."
            )
        elif row["block_kind"] == "heading":
            disposition = "NO_CONSTRUCTION"
            roles = ["CONTROL_OR_COMPARISON"]
            statement = "Reviewed in sequence; this heading only organizes the assigned Notes."
        elif row["block_kind"] == "image":
            disposition = "REPRESENTATION_OR_OBSERVER"
            roles = ["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"]
            statement = (
                "Screened in source context; this image is an output, plot, or "
                "representation whose native mechanics are absent or governed elsewhere."
            )
        elif unit in HISTORICAL_UNITS:
            disposition = "HISTORICAL_ONLY"
            roles = ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"]
            statement = (
                "Reviewed in full; this unit supplies attribution or chronology "
                "without a new local identity-plus-mechanics construction."
            )
        elif row["block_kind"] == "fenced_code":
            disposition = "REPRESENTATION_OR_OBSERVER"
            roles = ["REPRESENTATION", "IMPLEMENTATION_DETAIL"]
            statement = (
                "Reviewed in context; this unlinked code is an equivalent "
                "implementation or analyzer rather than a distinct native object."
            )
        elif unit >= "U005631":
            disposition = "NO_CONSTRUCTION"
            roles = ["CONTROL_OR_COMPARISON", "BEHAVIOR_OR_OUTCOME"]
            statement = (
                "Reviewed in full; this methodological discussion contains no "
                "new delimited native construction."
            )
        else:
            disposition = "REPRESENTATION_OR_OBSERVER"
            roles = ["BEHAVIOR_OR_OUTCOME", "CONTROL_OR_COMPARISON"]
            statement = (
                "Reviewed in full; this unit states behavior, counts, analysis, "
                "or representation without a separately delimited native law."
            )
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": disposition,
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": compact(list(dict.fromkeys(roles))),
                "candidate_ids": compact(candidates),
                "route_ids": compact(routes),
                "evidence_statement": statement,
                "review_stage": "7",
                "reviewer": WORKER,
            }
        )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in asset_input:
        row = deepcopy(original)
        path = row["physical_path"]
        candidates = candidate_links_by_image.get(path, [])
        if path in DEFECT_ASSETS:
            uncertainty, flags = DEFECT_ASSETS[path]
            role = "SOURCE_DEFECT"
            status = "DEFECTIVE"
            statement = uncertainty
            transcription = "CHECKED"
        elif candidates:
            role = "NATIVE_EVIDENCE"
            status = "CLEAR"
            flags = ["CONSTRUCTION_BEARING"]
            if path in {
                "BACK-MATTER/NOTES/_page_898_Picture_8.jpeg",
                "BACK-MATTER/NOTES/_page_901_Picture_1.jpeg",
                "BACK-MATTER/NOTES/_page_904_busy_beaver_2_3_4_state_rules.jpeg",
                "BACK-MATTER/NOTES/_page_904_busy_beaver_5_state_rule.jpeg",
            }:
                flags.append("TEXT_BEARING")
            uncertainty = ""
            statement = (
                "Original-resolution contextual inspection confirms the "
                f"construction-bearing evidence linked to {', '.join(candidates)}; "
                "only visibly supported labels, geometry, or outputs are used."
            )
            transcription = "CHECKED"
        elif path == "BACK-MATTER/NOTES/_page_911_symbolic_representation_table.jpeg":
            role = "RELATION"
            status = "CLEAR"
            flags = ["TEXT_BEARING", "CONSTRUCTION_BEARING"]
            uncertainty = ""
            statement = (
                "Original-resolution inspection confirms the functional, Polish, "
                "operator, and tree representation table; it is representational."
            )
            transcription = "CHECKED"
        elif path == "BACK-MATTER/NOTES/_page_910_cyclic_tag_trough.jpeg":
            role = "RELATION"
            status = "CLEAR"
            flags = ["CONSTRUCTION_BEARING"]
            uncertainty = ""
            statement = (
                "Original-resolution inspection confirms the mechanical trough "
                "rendering; prose, not pixels, supplies its operational semantics."
            )
            transcription = "NOT_REQUIRED"
        else:
            role = "OBSERVER"
            status = "CLEAR"
            flags = ["CONSTRUCTION_BEARING"]
            uncertainty = ""
            statement = (
                "Thumbnail/context screening confirms an evolution, plot, path, "
                "or comparison output rather than an independently encoded law."
            )
            transcription = "NOT_REQUIRED"
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": role,
                "source_status": status,
                "risk_flags": compact(flags),
                "original_resolution_status": (
                    "REVIEWED" if path in ORIGINAL_REVIEWED else "NOT_REQUIRED"
                ),
                "transcription_status": transcription,
                "candidate_ids": compact(candidates),
                "route_ids": "[]",
                "evidence_statement": statement,
                "review_stage": "7",
                "reviewer": WORKER,
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append(row)

    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "asset_updates": asset_updates,
            "candidate_proposals": candidate_proposals,
            "route_proposals": route_proposals,
            "uncertainties": [
                "A000407 is an unreferenced orphaned text strip, not a usable figure.",
                "A000422 is only 22×22 pixels; its geometry is supported by adjacent prose, not by independent image measurement.",
                "Busy Beaver witness tables are retained without importing an external transcription.",
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
            original, proposed = build(bundle)
            prepare_review_output.atomic_replace(
                bundle / "output" / "output.json",
                canonical_json_bytes(proposed),
                original,
            )
    except (OSError, csv.Error, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"Chapter 3 Notes authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "recorded Stage 7 Chapter 3 Notes review: "
        f"reading=318 assets=46 candidates={len(base.ALL_CANDIDATE_SPECS)} "
        f"routes={len(base.ALL_ROUTE_SPECS)} declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
