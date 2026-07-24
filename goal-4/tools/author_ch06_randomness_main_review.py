#!/usr/bin/env python3
"""Author and verify the sealed Stage 10 Chapter 6 main-text blind review.

This helper is intentionally data driven.  It consumes only the sealed worker
bundle named on the command line and never consults canonical audit ledgers.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


WORKER_ID = "ch06-main"
STAGE = 10
EPOCH = 2
SOURCE_PATH = "CHAPTERS/06-Starting-from-Randomness.md"
EXPECTED_CANDIDATE_COUNT = 60

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


def jdump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def ca_values(
    code: str,
    *,
    dimension: str = "one-dimensional",
    colors: str = "black and white",
    neighborhood: str | None = None,
    law: str | None = None,
) -> dict[str, str]:
    values = {
        "object_kind": f"{dimension} cellular-automaton preset",
        "native_time": "discrete successive steps",
        "carrier": f"{dimension} array of cells",
        "alphabet_or_value_schema": colors,
        "complete_state": "the color of every cell at one step",
        "seed": "an initial cell configuration",
        "frontier_or_activation": "all cells are updated on each displayed step",
        "schedule": "synchronous cellular-automaton steps",
        "law_kind": "deterministic local transition law",
        "rule_relation_constraint_function_or_probability_law": law
        or f"preset {code} under the source's cellular-automaton code scheme",
        "write_replacement_assembly_or_commit": "the next configuration replaces the current cell colors",
        "result_kind": "one successor cell configuration",
        "successor_cardinality": "one successor for each complete state",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "iteration may continue without an intrinsic stopping condition",
        "parameters_and_variants": code,
        "evidence_limit": "Only the mechanics stated or visibly transcribed in the Chapter 6 main-text bundle are asserted.",
    }
    if neighborhood is not None:
        values["read_dependencies_or_neighborhood"] = neighborhood
    return values


def relation_values(
    object_kind: str,
    *,
    carrier: str,
    input_value: str,
    law: str,
    result: str,
    determinism: str = "deterministic relation",
) -> dict[str, str]:
    return {
        "object_kind": object_kind,
        "native_time": "no independent native evolution; the relation is evaluated over its input",
        "carrier": carrier,
        "complete_state": "the complete input needed to evaluate the relation",
        "input": input_value,
        "law_kind": "relation, constraint, classifier, query, or observer law",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": "evaluation completes when the relation or query result is determined",
        "witness_semantics": "a witness is an input/output pair satisfying the stated relation",
        "evidence_limit": "Only the mechanics stated or visibly transcribed in the Chapter 6 main-text bundle are asserted.",
    }


def seed_values(
    object_kind: str,
    *,
    carrier: str,
    alphabet: str,
    law: str,
    result: str,
    determinism: str,
) -> dict[str, str]:
    return {
        "object_kind": object_kind,
        "native_time": "no iterative native time; one initial configuration is generated or delimited",
        "carrier": carrier,
        "alphabet_or_value_schema": alphabet,
        "complete_state": result,
        "input": "the stated generator parameters or constraint",
        "law_kind": "initial-state generator, probability law, or configuration constraint",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "successor_cardinality": "multiple admissible or sampled initial configurations",
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": "generation completes with an initial configuration",
        "parameters_and_variants": "the source-described density, block, alphabet, or constraint parameters",
        "evidence_limit": "Only the mechanics stated or visibly transcribed in the Chapter 6 main-text bundle are asserted.",
    }


def candidate_definitions() -> list[dict[str, Any]]:
    defs: list[dict[str, Any]] = []

    def add(
        name: str,
        units: list[str],
        semantic_units: list[str],
        values: dict[str, str],
        *,
        aliases: list[str] | None = None,
        strength: str = "DIRECT_PARTIAL_MECHANICS",
        role: str = "NATIVE",
        variants: list[str] | None = None,
        parameters: list[str] | None = None,
        uncertainties: list[str] | None = None,
        source_status: str = "CLEAR",
        conflicting_fields: list[str] | None = None,
        na_fields: list[str] | None = None,
        mechanics_units: list[str] | None = None,
        field_units: dict[str, list[str]] | None = None,
        evidence_overrides: dict[str, dict[str, Any]] | None = None,
        route_units: list[str] | None = None,
        related_names: list[str] | None = None,
        related_evidence_units: dict[str, list[str]] | None = None,
        variant_units: dict[str, list[str]] | None = None,
        anchor_priority: int = 0,
    ) -> None:
        defs.append(
            {
                "name": name,
                "units": units,
                "semantic_units": semantic_units,
                "values": values,
                "aliases": aliases or [],
                "strength": strength,
                "role": role,
                "variants": variants or [],
                "parameters": parameters or [],
                "uncertainties": uncertainties or [],
                "source_status": source_status,
                "conflicting_fields": conflicting_fields or [],
                "na_fields": na_fields or [],
                "mechanics_units": mechanics_units or [semantic_units[0]],
                "field_units": field_units or {},
                "evidence_overrides": evidence_overrides or {},
                "route_units": route_units or [],
                "related_names": related_names or [],
                "related_evidence_units": related_evidence_units or {},
                "variant_units": variant_units or {},
                "anchor_priority": anchor_priority,
            }
        )

    add(
        "random cellular-automaton initial-field generator family",
        ["U001227", "U001316", "U001324", "U001331", "U001333", "U001416", "U001421"],
        ["U001227", "U001316", "U001324", "U001331", "U001333", "U001416", "U001421"],
        seed_values(
            "carrier- and alphabet-parameterized stochastic initial-field generator family",
            carrier=(
                "the target cellular automaton's field: a one-dimensional binary row, a one-dimensional "
                "real-valued row, or a two-dimensional binary grid in the displayed variants"
            ),
            alphabet=(
                "the target field's value domain: black/white for binary examples or gray levels in [0,1] "
                "for continuous examples"
            ),
            law=(
                "choose every field value at random in the target carrier and value domain; binary examples "
                "also vary black-cell density"
            ),
            result="one complete initial field for the selected target carrier and value domain",
            determinism="stochastic; exact measures and independence are not stated in this range",
        ),
        aliases=["completely random initial conditions", "random initial conditions"],
        role="SEED",
        parameters=["target carrier", "target value domain", "black-cell density for binary fields"],
        variants=[
            "one-dimensional black-or-white random row",
            "one-dimensional random real-valued field in [0,1]",
            "two-dimensional black-or-white random field",
            "low-density one-dimensional binary field",
        ],
        uncertainties=[
            "The main text does not state exact probability measures, independence conditions, support extents, or random-bit sources for these variants."
        ],
        mechanics_units=["U001227"],
        field_units={
            "carrier": ["U001227", "U001316", "U001324", "U001331", "U001333"],
            "alphabet_or_value_schema": ["U001227", "U001316", "U001331"],
            "complete_state": ["U001227", "U001316", "U001324", "U001331", "U001333"],
            "rule_relation_constraint_function_or_probability_law": [
                "U001227",
                "U001316",
                "U001324",
                "U001331",
                "U001333",
                "U001416",
                "U001421",
            ],
            "result_kind": ["U001227", "U001316", "U001324", "U001331", "U001333"],
            "parameters_and_variants": [
                "U001227",
                "U001316",
                "U001324",
                "U001331",
                "U001333",
                "U001416",
                "U001421",
            ],
        },
        variant_units={
            "one-dimensional black-or-white random row": ["U001227"],
            "one-dimensional random real-valued field in [0,1]": ["U001316"],
            "two-dimensional black-or-white random field": ["U001324", "U001331", "U001333"],
            "low-density one-dimensional binary field": ["U001421"],
        },
    )
    add(
        "elementary cellular automaton rule 254",
        ["U001229", "U001231", "U001232", "U001233"],
        ["U001229", "U001231", "U001232", "U001233"],
        ca_values(
            "rule 254",
            neighborhood="the left and right neighbors of the updated cell",
            law="a cell becomes black whenever either neighbor is black",
        ),
        aliases=["rule 254"],
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "uniform-attractor elementary cellular-automaton preset panel",
        ["U001235", "U001236"],
        ["U001235", "U001236"],
        ca_values("rules 0, 32, 160, and 250"),
        variants=["rule 0", "rule 32", "rule 160", "rule 250"],
        uncertainties=["The local transition tables are visible, but the prose does not transcribe each table entry."],
    )
    add(
        "fixed-or-periodic-structure elementary cellular-automaton preset panel",
        ["U001239", "U001240", "U001485", "U001486"],
        ["U001239", "U001240", "U001486"],
        ca_values("rules 4, 108, 218, and 232"),
        variants=["rule 4", "rule 108", "rule 218", "rule 232"],
        uncertainties=["Only rule 4 receives a later attractor constraint; the other preset tables are not transcribed in prose."],
    )
    add(
        "elementary cellular automaton rule 126",
        ["U001242", "U001243", "U001244", "U001437", "U001438", "U001439"],
        ["U001242", "U001243", "U001244", "U001439"],
        ca_values("rule 126"),
        aliases=["rule 126"],
    )
    add(
        "elementary cellular automaton rule 22",
        ["U001245", "U001406", "U001407", "U001409", "U001410", "U001420", "U001421"],
        ["U001245", "U001407", "U001410", "U001421"],
        ca_values("rule 22"),
        aliases=["rule 22"],
    )
    add(
        "elementary cellular automaton rule 30",
        [
            "U001246",
            "U001400",
            "U001401",
            "U001402",
            "U001425",
            "U001426",
            "U001427",
            "U001428",
            "U001429",
            "U001430",
            "U001431",
            "U001440",
            "U001441",
        ],
        ["U001246", "U001402", "U001426", "U001431", "U001441"],
        ca_values("rule 30"),
        aliases=["rule 30"],
    )
    add(
        "elementary cellular automaton rule 150",
        ["U001247", "U001460", "U001461", "U001462", "U001463", "U001464"],
        ["U001247", "U001463", "U001464"],
        ca_values("rule 150"),
        aliases=["rule 150"],
    )
    add(
        "elementary cellular automaton rule 182",
        ["U001248"],
        ["U001248"],
        ca_values("rule 182"),
        aliases=["rule 182"],
    )
    add(
        "elementary cellular automaton rule 90",
        [
            "U001250",
            "U001413",
            "U001414",
            "U001420",
            "U001421",
            "U001446",
            "U001447",
            "U001448",
            "U001455",
            "U001456",
            "U001457",
            "U001458",
        ],
        ["U001250", "U001414", "U001448", "U001458"],
        ca_values("rule 90"),
        aliases=["rule 90"],
    )
    add(
        "elementary cellular automaton rule 105",
        ["U001250"],
        ["U001250"],
        ca_values("rule 105"),
        aliases=["rule 105"],
    )
    add(
        "elementary cellular automaton rule 110",
        [
            "U001254",
            "U001255",
            "U001256",
            "U001257",
            "U001557",
            "U001558",
            "U001560",
            "U001561",
            "U001562",
            "U001567",
            "U001568",
            "U001569",
            "U001570",
            "U001571",
            "U001572",
            "U001573",
            "U001574",
            "U001575",
            "U001576",
        ],
        ["U001254", "U001256", "U001558", "U001560", "U001568", "U001570", "U001572", "U001574", "U001576"],
        ca_values(
            "rule 110",
            neighborhood="nearest neighbors in one dimension",
        ),
        aliases=["rule 110"],
    )
    add(
        "four-class cellular-automaton behavior classification",
        [
            "U001264",
            "U001265",
            "U001266",
            "U001267",
            "U001268",
            "U001269",
            "U001270",
            "U001271",
            "U001278",
            "U001279",
            "U001280",
            "U001293",
            "U001298",
        ],
        ["U001264", "U001269", "U001270", "U001271", "U001278", "U001279", "U001280", "U001298"],
        relation_values(
            "qualitative behavioral classification relation",
            carrier="cellular-automaton evolution histories from random initial conditions",
            input_value="an evolution pattern and a chosen reasonable definition of the classes",
            law=(
                "assign class 1 to almost-uniform final behavior, class 2 to fixed or periodically repeating "
                "simple structures, class 3 to apparently random behavior with small structures, and class 4 "
                "to moving localized structures and complicated interactions; borderline assignments may differ"
            ),
            result="one of four class labels, or multiple plausible labels for a documented borderline rule",
            determinism="definition-dependent on rare borderline cases",
        ),
        aliases=["four classes of behavior", "classes 1, 2, 3, and 4"],
        role="OBSERVER",
        uncertainties=["The source explicitly says different reasonable definitions disagree on rare borderline systems."],
    )
    add(
        "symmetric quiescent-white binary nearest-neighbor cellular-automaton family",
        ["U001272", "U001273"],
        ["U001272", "U001273"],
        ca_values(
            "symmetric binary nearest-neighbor rules leaving all-white unchanged",
            neighborhood="nearest neighbors used symmetrically",
        ),
        role="FAMILY",
        parameters=["rule table"],
    )
    add(
        "binary next-nearest-neighbor totalistic cellular-automaton family",
        ["U001274", "U001275"],
        ["U001274", "U001275"],
        ca_values(
            "binary totalistic rules with nearest and next-nearest neighbors",
            neighborhood="nearest and next-nearest neighbors, read totalistically",
        ),
        role="FAMILY",
        parameters=["totalistic rule code"],
    )
    add(
        "three-color nearest-neighbor totalistic cellular-automaton family",
        ["U001276", "U001277"],
        ["U001276", "U001277"],
        ca_values(
            "three-color nearest-neighbor totalistic rules",
            colors="three cell colors",
            neighborhood="nearest neighbors, read totalistically",
        ),
        role="FAMILY",
        parameters=["totalistic rule code"],
    )
    add(
        "three-color class-4 totalistic cellular-automaton preset panel",
        ["U001285", "U001286", "U001287", "U001288", "U001289", "U001290", "U001291", "U001292"],
        ["U001285", "U001286", "U001287", "U001288", "U001289", "U001290", "U001291", "U001292"],
        ca_values(
            "codes 1815, 2007, 1659, and 2043",
            colors="three cell colors",
            neighborhood="nearest neighbors, read totalistically",
        ),
        variants=["code 1815", "code 2007", "code 1659 (transcribed from the owned image)", "code 2043"],
    )
    add(
        "four-color nearest-neighbor totalistic cellular-automaton sequence",
        ["U001305", "U001306"],
        ["U001305", "U001306"],
        ca_values(
            "a displayed sequence of four-color totalistic codes",
            colors="four cell colors",
            neighborhood="nearest neighbors, read totalistically",
        ),
        role="FAMILY",
        parameters=["totalistic rule code"],
    )
    add(
        "fractional-average continuous cellular automaton",
        ["U001311", "U001315", "U001316", "U001317", "U001318", "U001319", "U001320"],
        ["U001311", "U001315", "U001316", "U001318", "U001320"],
        {
            **ca_values(
                "fractional-average continuous cellular automaton",
                colors="a real gray level from 0 through 1",
                neighborhood="the cell and its two nearest neighbors",
                law="average the three gray levels, add a specified constant, and retain only the fractional part",
            ),
            "parameters_and_variants": "additive constant in [0,1], including displayed values 0.398 and 0.4",
        },
        aliases=["continuous cellular automaton"],
        strength="DIRECT_COMPLETE_MECHANICS",
        parameters=["additive constant"],
    )
    add(
        "neighbor-weighted fractional-average continuous cellular automaton",
        ["U001321", "U001322", "U001323"],
        ["U001321", "U001322", "U001323"],
        {
            **ca_values(
                "neighbor-weighted fractional-average continuous cellular automaton",
                colors="a real gray level from 0 through 1",
                neighborhood="the cell and its two nearest neighbors",
                law=(
                    "multiply each neighboring gray level by 1.13 before averaging, use the stated 0.5 parameter, "
                    "add the constant, and retain the fractional part"
                ),
            ),
            "parameters_and_variants": "displayed parameter pair {0.5, 1.13}",
        },
        parameters=["additive constant", "neighbor multiplier"],
        uncertainties=["The prose does not state whether the central cell is also weighted before the average."],
    )
    add(
        "Game of Life cellular automaton",
        ["U001329", "U001336", "U001337", "U001338", "U001339", "U001340", "U001341"],
        ["U001329", "U001336", "U001338", "U001339", "U001340", "U001341"],
        {
            **ca_values(
                "outer-totalistic 9-neighbor code 224 (Game of Life)",
                dimension="two-dimensional",
                neighborhood="the eight orthogonal and diagonal neighbors",
                law=(
                    "with two black neighbors retain the cell's prior color; with three black neighbors become "
                    "black; with any other neighbor count become white"
                ),
            ),
            "topology": "two-dimensional square grid with orthogonal and diagonal adjacency",
        },
        aliases=["Game of Life", "outer totalistic 9-neighbor code 224"],
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "binary two-dimensional von-Neumann-totalistic cellular-automaton family",
        ["U001330", "U001331", "U001332", "U001333"],
        ["U001330", "U001331", "U001332", "U001333"],
        {
            **ca_values(
                "64 binary totalistic codes",
                dimension="two-dimensional",
                neighborhood="the cell and its four immediate orthogonal neighbors; their total ranges from 0 to 5",
                law="successive base-2 code digits give the output for neighborhood totals from 5 down to 0",
            ),
            "topology": "two-dimensional square grid with four immediate orthogonal neighbors",
        },
        role="FAMILY",
        parameters=["six-bit totalistic rule code"],
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "single-cell initial-perturbation difference observer",
        [
            "U001344",
            "U001345",
            "U001346",
            "U001348",
            "U001349",
            "U001350",
            "U001351",
            "U001352",
            "U001359",
            "U001360",
            "U001361",
            "U001362",
        ],
        ["U001344", "U001345", "U001346", "U001348", "U001352", "U001359", "U001362"],
        relation_values(
            "comparative evolution observer",
            carrier="two cellular-automaton space-time histories",
            input_value="two runs whose initial conditions differ in the color of one selected cell",
            law="mark every cell whose color differs between the corresponding runs",
            result="a space-time difference set rendered by black dots",
        ),
        aliases=["sensitivity to initial conditions experiment"],
        role="OBSERVER",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "finite cyclic translation of a single dot",
        ["U001367", "U001368", "U001369", "U001370", "U001371", "U001372", "U001373", "U001374", "U001375", "U001376"],
        ["U001367", "U001369", "U001372", "U001374", "U001376"],
        {
            "object_kind": "finite deterministic dynamical system",
            "native_time": "discrete successive steps",
            "carrier": "one dot on a finite ordered set of positions",
            "support": "n positions",
            "topology": "a cycle formed by wrapping the right end to the left end",
            "alphabet_or_value_schema": "exactly one occupied position",
            "complete_state": "the dot's current position",
            "input": "system size n and fixed step displacement k",
            "boundary": "cyclic wraparound",
            "frontier_or_activation": "the single dot",
            "schedule": "one move per step",
            "law_kind": "deterministic modular translation",
            "rule_relation_constraint_function_or_probability_law": "advance k positions to the right modulo n",
            "write_replacement_assembly_or_commit": "replace the current position by the translated position",
            "result_kind": "one successor dot position",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "termination_completion_failure": "iteration continues periodically",
            "parameters_and_variants": "n and k; examples use n = 6, 10, and 11",
            "evidence_limit": "Only the mechanics stated or visibly transcribed in the Chapter 6 main-text bundle are asserted.",
        },
        aliases=["single-dot wraparound system"],
        parameters=["number of positions n", "displacement k"],
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "finite cyclic doubling map",
        ["U001377", "U001378", "U001379", "U001380", "U001381"],
        ["U001377", "U001378", "U001379", "U001380", "U001381"],
        {
            "object_kind": "finite deterministic dynamical system",
            "native_time": "discrete successive steps",
            "carrier": "one dot on positions modulo n",
            "support": "n positions",
            "topology": "cyclic modular positions",
            "alphabet_or_value_schema": "one integer position",
            "complete_state": "the dot's current integer position",
            "input": "system size n",
            "boundary": "modular wraparound",
            "frontier_or_activation": "the single dot",
            "schedule": "one doubling per step",
            "law_kind": "deterministic modular map",
            "rule_relation_constraint_function_or_probability_law": "after t steps the position is Mod[2^t,n]",
            "write_replacement_assembly_or_commit": "replace the position by twice its value modulo n",
            "result_kind": "one successor dot position",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "termination_completion_failure": "iteration continues periodically",
            "parameters_and_variants": "system size n",
            "evidence_limit": "Only the mechanics stated or visibly transcribed in the Chapter 6 main-text bundle are asserted.",
        },
        parameters=["system size n"],
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "finite cyclic binary cellular automaton",
        ["U001383", "U001390", "U001391"],
        ["U001383", "U001390", "U001391"],
        {
            **ca_values(
                "finite cyclic cellular-automaton variants",
                neighborhood="the rule's ordinary neighborhood with the rightmost and leftmost cells treated as neighbors",
            ),
            "support": "a finite number n of cells",
            "topology": "a one-dimensional cycle",
            "boundary": "the right neighbor of the rightmost cell is the leftmost cell and vice versa",
            "parameters_and_variants": "cell count n and cellular-automaton rule",
        },
        aliases=["limited-size cellular automaton", "periodic-boundary cellular automaton"],
        role="FAMILY",
        parameters=["cell count n", "cellular-automaton rule"],
    )
    add(
        "elementary cellular automaton rule 45 on a finite cycle",
        ["U001388", "U001392", "U001393"],
        ["U001388", "U001392", "U001393"],
        {
            **ca_values("rule 45"),
            "support": "a finite cyclic row of n cells",
            "boundary": "cyclic",
            "parameters_and_variants": "rule 45 and finite size n",
        },
        aliases=["rule 45"],
    )
    add(
        "periodic-block cellular-automaton initial-condition generator",
        ["U001432", "U001433", "U001434", "U001440", "U001441"],
        ["U001432", "U001433", "U001434", "U001441"],
        seed_values(
            "deterministic periodic initial-condition generator",
            carrier="an unbounded one-dimensional row partitioned into identical blocks",
            alphabet="the cellular automaton's cell alphabet",
            law="repeat one fixed finite block forever in both directions",
            result="a spatially periodic initial configuration",
            determinism="deterministic given the block",
        ),
        aliases=["fixed block repeated forever"],
        role="SEED",
        parameters=["finite block"],
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "rule-126 random two-block initial-condition ensemble",
        ["U001436", "U001437", "U001438", "U001439"],
        ["U001436", "U001439"],
        seed_values(
            "stochastic block-sequence initial-condition generator",
            carrier="a one-dimensional concatenation of four-cell blocks",
            alphabet="the two blocks BBWW and BBBW",
            law="form a random sequence from blocks BBWW and BBBW",
            result="a rule-126 initial configuration composed of the two allowed blocks",
            determinism="stochastic; block probabilities and independence are not stated",
        ),
        role="SEED",
        variants=["BBWW block", "BBBW block"],
        uncertainties=["The source does not state block probabilities, independence, or the spatial extent of the sequence."],
    )
    add(
        "rule-126 to rule-90 pair-block emulation",
        ["U001444", "U001445", "U001446", "U001447", "U001448", "U001449"],
        ["U001444", "U001445", "U001446", "U001447", "U001448", "U001449"],
        relation_values(
            "block encoding and temporal-subsampling emulation",
            carrier="rule-126 configurations tiled by uniform two-cell blocks",
            input_value="a rule-90 cell configuration encoded as BB or WW pairs",
            law="evolve rule 126 and inspect alternate steps; each pair then behaves as one rule-90 cell",
            result="the corresponding rule-90 evolution decoded from the block configuration",
        ),
        aliases=["rule 126 emulates rule 90"],
        role="EMULATION",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "rule-90 pair-block self-emulation",
        ["U001452", "U001453", "U001454", "U001455", "U001456", "U001457", "U001458"],
        ["U001452", "U001453", "U001454", "U001455", "U001456", "U001457", "U001458"],
        relation_values(
            "cellular-automaton block self-emulation",
            carrier="rule-90 configurations grouped into adjacent two-cell blocks",
            input_value="an appropriately block-encoded rule-90 configuration",
            law="the configuration of two-cell blocks evolves according to rule 90 just as individual cells do",
            result="a decoded rule-90 evolution at block scale",
        ),
        aliases=["rule 90 emulates itself"],
        role="EMULATION",
    )
    add(
        "rule-150 block self-emulation",
        ["U001459", "U001460", "U001461", "U001462", "U001463", "U001464"],
        ["U001459", "U001460", "U001461", "U001462", "U001463", "U001464"],
        relation_values(
            "cellular-automaton block self-emulation",
            carrier="rule-150 configurations partitioned into the displayed blocks",
            input_value="an appropriately block-encoded rule-150 configuration",
            law="the displayed blocks behave like individual cells under rule 150",
            result="a decoded rule-150 evolution at block scale",
        ),
        aliases=["rule 150 emulates itself"],
        role="EMULATION",
        uncertainties=["The prose does not transcribe the full block code; it is supplied by the owned images."],
    )
    add(
        "elementary cellular automaton rule 184",
        ["U001465", "U001466", "U001467", "U001468", "U001469", "U001472", "U001473", "U001474", "U001476", "U001477"],
        ["U001465", "U001466", "U001467", "U001468", "U001469", "U001474", "U001477"],
        ca_values("rule 184"),
        aliases=["rule 184"],
    )
    add(
        "rule-184 three-cell-block self-emulation",
        ["U001465", "U001466", "U001467", "U001468", "U001469", "U001475"],
        ["U001465", "U001466", "U001467", "U001468", "U001469", "U001475"],
        relation_values(
            "cellular-automaton block self-emulation",
            carrier="rule-184 configurations partitioned into three-cell blocks",
            input_value="a configuration encoded with the displayed three-cell blocks",
            law="each allowed three-cell block acts like one cell under rule 184",
            result="a decoded rule-184 evolution at block scale",
        ),
        aliases=["rule 184 emulates itself"],
        role="EMULATION",
        uncertainties=["The prose states the block width, while the precise block code is image-borne."],
    )
    add(
        "nested substitution initial condition for rule 184",
        ["U001470", "U001471", "U001472", "U001473", "U001474"],
        ["U001470", "U001471", "U001472", "U001473", "U001474"],
        seed_values(
            "deterministic substitution-generated initial condition",
            carrier="a one-dimensional symbolic sequence",
            alphabet="black and white cells",
            law="B -> BWB and W -> WWB, iterated from one black element",
            result="the nested black-or-white sequence used as the rule-184 initial condition",
            determinism="deterministic",
        ),
        role="SEED",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "next-nearest cellular automaton rule 4067213884",
        ["U001479", "U001480"],
        ["U001479", "U001480"],
        ca_values(
            "rule 4067213884",
            neighborhood="nearest and next-nearest neighbors",
        ),
        aliases=["rule 4067213884"],
    )
    add(
        "rule-255 all-black attractor",
        ["U001484", "U001485", "U001486", "U001487"],
        ["U001484", "U001485", "U001486", "U001487"],
        relation_values(
            "attractor relation",
            carrier="binary cellular-automaton configurations",
            input_value="any rule-255 initial configuration",
            law="after one step only the all-black configuration can occur",
            result="the singleton all-black attractor",
        ),
        role="CONSTRAINT",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "rule-4 isolated-black attractor-set constraint",
        ["U001486", "U001488"],
        ["U001486", "U001488"],
        relation_values(
            "attractor-set membership constraint",
            carrier="binary cellular-automaton configurations",
            input_value="a proposed rule-4 attractor configuration",
            law=(
                "accept exactly configurations in which every black cell has at least one white cell on each side"
            ),
            result="membership in the rule-4 attractor set",
        ),
        role="CONSTRAINT",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "rule-4 many-to-one basin-of-attraction relation",
        ["U001489", "U001490", "U001491"],
        ["U001489", "U001491"],
        relation_values(
            "many-to-one basin/preimage relation",
            carrier="pairs of rule-4 initial and final configurations",
            input_value="a rule-4 final attractor configuration",
            law=(
                "collect the distinct initial configurations that evolve to the selected final attractor state"
            ),
            result="the basin or preimage set of initial configurations for that final state",
            determinism="the forward rule is deterministic, while the inverse basin relation can have many members",
        ),
        role="CONSTRAINT",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "allowed-sequence path-network observer",
        [
            "U001492",
            "U001493",
            "U001494",
            "U001495",
            "U001496",
            "U001497",
            "U001498",
            "U001499",
            "U001500",
            "U001501",
            "U001502",
            "U001503",
            "U001504",
            "U001505",
            "U001506",
        ],
        ["U001492", "U001493", "U001494", "U001495", "U001496", "U001498", "U001500", "U001503", "U001504", "U001506"],
        relation_values(
            "finite-network representation of an allowed sequence language",
            carrier="directed labeled networks and binary cell sequences",
            input_value="the set of cell sequences allowed at one evolution step",
            law="construct a network so each allowed black-or-white sequence corresponds to a possible path",
            result="a path network representing exactly the allowed sequences",
        ),
        aliases=["network of possible sequences"],
        role="OBSERVER",
        uncertainties=["The main text gives examples but not the general network-construction algorithm."],
    )
    add(
        "full binary configuration language",
        ["U001494", "U001498"],
        ["U001494", "U001498"],
        seed_values(
            "declarative configuration set",
            carrier="one-dimensional binary sequences",
            alphabet="black and white",
            law="allow any number of black and white cells in any order",
            result="the set of all binary sequences",
            determinism="declarative set with many members; it is not itself a sampling measure",
        ),
        aliases=["all possible black-and-white sequences"],
        role="CONSTRAINT",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    add(
        "elementary cellular automaton rule 128",
        ["U001499", "U001500", "U001501", "U001502", "U001503"],
        ["U001499", "U001500", "U001503"],
        ca_values(
            "rule 128",
            law="regions of black shrink by one cell on each side at each step",
        ),
        aliases=["rule 128"],
    )
    add(
        "surjective binary cellular-automaton mapping family",
        ["U001508", "U001509", "U001510", "U001511", "U001512"],
        ["U001508", "U001511", "U001512"],
        relation_values(
            "surjective cellular-automaton mapping class",
            carrier="binary configurations under one-dimensional cellular-automaton evolution",
            input_value="the full set of possible binary configurations",
            law="every possible binary sequence remains attainable at every subsequent step",
            result="a surjective or onto global map on binary configurations",
        ),
        aliases=["onto cellular automata", "surjective cellular automata"],
        role="CONSTRAINT",
    )
    add(
        "conflicted adjacent-black constrained initial-condition language",
        ["U001513", "U001514", "U001515"],
        ["U001513", "U001514", "U001515"],
        seed_values(
            "source-conflicted declarative initial-condition set",
            carrier="one-dimensional binary sequences",
            alphabet="black and white",
            law=(
                "CONFLICT: prose says no pair of black cells is allowed together, while the following caption says "
                "black cells are only allowed to appear in pairs"
            ),
            result="an initial-condition language whose intended constraint cannot be decided from the bundled source",
            determinism="declarative set, but its membership condition conflicts",
        ),
        role="CONSTRAINT",
        source_status="CONFLICTING",
        strength="DEFECT_LIMITED",
        conflicting_fields=["rule_relation_constraint_function_or_probability_law", "result_kind"],
        uncertainties=[
            "U001513 forbids adjacent black cells, while U001515 requires black cells to appear in pairs; the owned image does not resolve the contradiction."
        ],
    )
    add(
        "two-color next-nearest-neighbor cellular automaton code 20",
        ["U001519", "U001525", "U001526", "U001532", "U001533", "U001535", "U001536", "U001539", "U001540"],
        ["U001519", "U001526", "U001533", "U001536", "U001540"],
        ca_values(
            "code 20",
            neighborhood="nearest and next-nearest neighbors",
        ),
        aliases=["code 20 cellular automaton"],
    )
    add(
        "persistent-structure exhaustive search query",
        ["U001519", "U001532", "U001533", "U001534", "U001535", "U001536"],
        ["U001519", "U001533", "U001534", "U001536"],
        relation_values(
            "bounded brute-force enumeration query",
            carrier="finite cellular-automaton initial blocks and their evolutions",
            input_value="a cellular-automaton rule and an integer bound on consecutively encoded finite initial blocks",
            law=(
                "enumerate initial-condition integers in order, decode each as a finite initial block, evolve it, "
                "and record whether it dies out or yields a fixed or moving persistent structure"
            ),
            result="persistent structures witnessed within the finite enumerated prefix; completeness beyond that prefix is not claimed",
        ),
        aliases=["persistent structure search"],
        role="OBSERVER",
        uncertainties=["The source does not state a universal stopping or equivalence-deduplication criterion for this brute-force search."],
        mechanics_units=["U001519"],
    )
    add(
        "three-color nearest-neighbor cellular automaton code 357",
        ["U001527", "U001528", "U001542", "U001543", "U001544", "U001545", "U001546"],
        ["U001527", "U001528", "U001544", "U001546"],
        ca_values(
            "code 357",
            colors="three cell colors",
            neighborhood="nearest neighbors",
        ),
        aliases=["code 357 cellular automaton"],
    )
    add(
        "three-color nearest-neighbor cellular automaton code 1329",
        ["U001529", "U001530", "U001548", "U001549", "U001550", "U001551", "U001552", "U001553", "U001554", "U001555", "U001556"],
        ["U001529", "U001530", "U001550", "U001553", "U001556"],
        ca_values(
            "code 1329",
            colors="three cell colors",
            neighborhood="nearest neighbors",
        ),
        aliases=["code 1329 cellular automaton"],
    )

    add(
        "neighbor-difference gray-field display transformation",
        ["U001323"],
        ["U001323"],
        {
            **relation_values(
                "deterministic observer transformation",
                carrier="a one-dimensional real-valued cellular-automaton field",
                input_value="the actual gray level of each cell and the gray level of its selected neighbor",
                law="replace the displayed gray level by the difference between each cell's gray level and its neighbor's",
                result="a derived gray-field display with uniform stripes removed",
            ),
            "read_dependencies_or_neighborhood": "each displayed cell reads its own actual value and one neighboring actual value",
            "excluded_observers_and_representations": (
                "the differenced gray levels are a display transformation and are not the continuous cellular automaton's native state"
            ),
        },
        aliases=["neighbor-difference display", "stripe-removing gray display"],
        role="OBSERVER",
        strength="DIRECT_COMPLETE_MECHANICS",
        mechanics_units=["U001323"],
    )
    add(
        "one-dimensional slice-through-time and temporal-fog observer",
        ["U001325", "U001326", "U001327", "U001334", "U001335", "U001341"],
        ["U001325", "U001335", "U001341"],
        {
            **relation_values(
                "deterministic space-time slice and history-rendering observer",
                carrier="a two-dimensional cellular-automaton history",
                input_value="a two-dimensional evolution, a chosen one-dimensional slice, and successive observation steps",
                law=(
                    "extract the chosen one-dimensional slice through successive steps; optionally retain cells black "
                    "on preceding steps in progressively lighter gray to form a temporal fog"
                ),
                result="a one-dimensional-through-time display, optionally augmented by receding gray history",
            ),
            "read_dependencies_or_neighborhood": "the selected spatial slice and its earlier time layers",
            "parameters_and_variants": "slice position, history depth, fog shading, and displayed codes 4, 12, 24, 30, 38, 52 or Game of Life",
            "excluded_observers_and_representations": (
                "the slice and fog are observer outputs; they do not alter or define the two-dimensional native transition law"
            ),
        },
        aliases=["one-dimensional slice observer", "temporal fog display"],
        role="OBSERVER",
        variants=[
            "code 4 slice",
            "code 12 slice",
            "code 24 slice",
            "code 30 slice",
            "code 38 slice",
            "code 52 slice",
            "Game of Life slice with temporal fog",
        ],
        mechanics_units=["U001325", "U001335", "U001341"],
        variant_units={
            "code 4 slice": ["U001334", "U001335"],
            "code 12 slice": ["U001334", "U001335"],
            "code 24 slice": ["U001334", "U001335"],
            "code 30 slice": ["U001334", "U001335"],
            "code 38 slice": ["U001334", "U001335"],
            "code 52 slice": ["U001334", "U001335"],
            "Game of Life slice with temporal fog": ["U001341"],
        },
    )
    add(
        "finite-system repetition-period and maximum-period observer",
        [
            "U001385",
            "U001386",
            "U001387",
            "U001388",
            "U001389",
            "U001390",
            "U001391",
            "U001392",
            "U001393",
        ],
        ["U001385", "U001387", "U001388", "U001389", "U001391", "U001393"],
        {
            **relation_values(
                "finite-orbit repetition-period query and curve observer",
                carrier="finite deterministic systems, including cyclic binary cellular automata",
                input_value="a transition rule, finite size n, and initial state",
                law=(
                    "iterate the finite deterministic system until a state recurs, measure its eventual repetition "
                    "period, and compare it with the number of possible states"
                ),
                result="one eventual repetition period or a period-versus-size curve",
            ),
            "support": "n binary cells give 2^n complete states",
            "structural_invariants": (
                "every finite deterministic orbit eventually repeats; its period is at most the number of states, "
                "hence at most 2^n for n binary cells"
            ),
            "parameters_and_variants": (
                "system size n, initial state, and rules 90, 30, 45, and 110; the displayed peaks are "
                "2^((n-1)/2)-1 for rule 90, about 2^(0.63n) for rule 30, close to 2^n for rule 45, "
                "and roughly n^3 for rule 110"
            ),
            "excluded_observers_and_representations": (
                "the evolution panels and period curves measure finite instances; they do not define the plotted rules' native transition laws"
            ),
        },
        aliases=["finite repetition-period query", "period-versus-size observer"],
        role="OBSERVER",
        variants=["rule 90 period curve", "rule 30 period curve", "rule 45 period curve", "rule 110 period curve"],
        mechanics_units=["U001385", "U001387", "U001393"],
        variant_units={
            "rule 90 period curve": ["U001392", "U001393"],
            "rule 30 period curve": ["U001392", "U001393"],
            "rule 45 period curve": ["U001388", "U001392", "U001393"],
            "rule 110 period curve": ["U001392", "U001393"],
        },
    )
    add(
        "additive cellular-automaton superposition relation",
        ["U001411", "U001412", "U001413", "U001414", "U001463", "U001464"],
        ["U001412", "U001414", "U001463", "U001464"],
        {
            **relation_values(
                "algebraic superposition and self-emulation relation",
                carrier="binary cellular-automaton initial configurations and their complete evolution patterns",
                input_value="an additive rule and one or more component initial configurations or evolution patterns",
                law=(
                    "the evolution from a superposed initial configuration is the corresponding superposition of "
                    "component evolutions; every additive rule self-emulates and yields nested patterns"
                ),
                result="a superposed evolution equivalent to evolving the combined initial condition",
            ),
            "structural_invariants": (
                "additivity is preserved through evolution and implies block self-emulation; rules 90 and 150 are "
                "the only fundamentally different two-color nearest-neighbor examples stated here"
            ),
            "parameters_and_variants": "rule 90 and rule 150",
        },
        aliases=["cellular-automaton additivity", "pattern superposition"],
        role="CONSTRAINT",
        variants=["rule 90 additivity", "rule 150 additivity"],
        mechanics_units=["U001414", "U001464"],
        related_names=[
            "elementary cellular automaton rule 90",
            "elementary cellular automaton rule 150",
            "rule-90 pair-block self-emulation",
            "rule-150 block self-emulation",
        ],
        variant_units={
            "rule 90 additivity": ["U001412", "U001413", "U001414", "U001463", "U001464"],
            "rule 150 additivity": ["U001463", "U001464"],
        },
    )
    add(
        "elementary cellular automaton rule 255",
        ["U001484", "U001485", "U001486"],
        ["U001484", "U001486"],
        ca_values("rule 255"),
        aliases=["rule 255"],
        strength="DIRECT_PARTIAL_MECHANICS",
        mechanics_units=["U001486"],
        anchor_priority=-1,
        uncertainties=["The local rule table is image-borne or delegated to the rule-number scheme; this range directly identifies the preset and its outcome."],
    )
    add(
        "elementary cellular automaton rule 4",
        ["U001485", "U001486"],
        ["U001485", "U001486"],
        ca_values("rule 4"),
        aliases=["rule 4"],
        strength="DIRECT_COMPLETE_MECHANICS",
        mechanics_units=[],
        uncertainties=[],
    )
    add(
        "localized finite-seed integer codec family",
        ["U001533", "U001536", "U001544"],
        ["U001533", "U001536", "U001544"],
        {
            "object_kind": "deterministic integer-to-localized-seed codec family",
            "native_time": "one decoding operation",
            "carrier": "a finite localized block of cells used as a cellular-automaton initial condition",
            "alphabet_or_value_schema": "radix-matched cell values: two colors for base 2 or three colors for base 3",
            "complete_state": "the finite cell block encoded by the integer's digit sequence",
            "input": "a nonnegative integer and the selected radix/color correspondence",
            "law_kind": "deterministic positional-radix decoding function",
            "rule_relation_constraint_function_or_probability_law": (
                "write the integer in base 2 or base 3 and map its digit sequence to the corresponding two-color "
                "or three-color finite initial block"
            ),
            "result_kind": "one localized finite seed",
            "successor_cardinality": "one seed for each integer and selected codec",
            "determinism_branching_or_measure": "deterministic",
            "termination_completion_failure": "decoding completes after the finite digit sequence is emitted",
            "parameters_and_variants": "base 2 for binary code 20 examples; base 3 for three-color code 357 examples",
            "excluded_observers_and_representations": (
                "the integer labels encode initial conditions and are not cellular-automaton rule numbers or evolution laws"
            ),
            "evidence_limit": "Digit orientation, leading-zero convention, and the surrounding blank-background convention are not fully stated.",
        },
        aliases=["initial-condition integer codec"],
        role="SEED",
        variants=["base-2 binary finite-seed codec", "base-3 three-color finite-seed codec"],
        uncertainties=["Digit orientation, leading-zero convention, and the surrounding blank-background convention are not fully stated."],
        mechanics_units=["U001533", "U001544"],
        variant_units={
            "base-2 binary finite-seed codec": ["U001533", "U001536"],
            "base-3 three-color finite-seed codec": ["U001544"],
        },
    )
    add(
        "systematic fixed-period persistent-structure constraint solver",
        ["U001537", "U001538", "U001539", "U001540"],
        ["U001537", "U001538", "U001540"],
        {
            **relation_values(
                "complete fixed-period constraint-solving procedure",
                carrier="finite fixed or moving cellular-automaton structures",
                input_value="a cellular-automaton rule and requested repetition period",
                law=(
                    "apply a systematic constraint method to find all fixed or moving persistent structures having "
                    "the requested period"
                ),
                result="the complete set of persistent structures for that bounded period",
            ),
            "parameters_and_variants": "displayed code-20 results for repetition periods through 15",
            "evidence_limit": (
                "The range states the completeness contract and results but does not give the constraint encoding or solving algorithm; WR0024 routes it to page 268."
            ),
        },
        aliases=["complete fixed-period structure search"],
        role="OBSERVER",
        uncertainties=[
            "The range states the completeness contract and results but does not give the constraint encoding or solving algorithm; WR0024 routes it to page 268."
        ],
        mechanics_units=["U001537", "U001540"],
    )

    # The four class-4 code panels share a survey introduction but define four
    # independently selectable native presets.  Keep their discovery anchor
    # shared and preserve display order with per-anchor ordinals.
    panel = next(
        row
        for row in defs
        if row["name"] == "three-color class-4 totalistic cellular-automaton preset panel"
    )
    panel_specs = [
        ("1815", ["U001285", "U001286", "U001287"], ["U001285", "U001287"]),
        ("2007", ["U001285", "U001288", "U001289"], ["U001285", "U001289"]),
        ("1659", ["U001285", "U001290"], ["U001285", "U001290"]),
        ("2043", ["U001285", "U001291", "U001292"], ["U001285", "U001292"]),
    ]
    panel_clones: list[dict[str, Any]] = []
    for code, units, semantic_units in panel_specs:
        clone = deepcopy(panel)
        clone["name"] = f"three-color nearest-neighbor totalistic cellular automaton code {code}"
        clone["aliases"] = [f"code {code}"]
        clone["units"] = units
        clone["semantic_units"] = semantic_units
        clone["mechanics_units"] = ["U001285"]
        clone["values"] = {
            "object_kind": "class-4 three-color nearest-neighbor totalistic cellular-automaton preset",
            "native_time": "successive cellular-automaton steps",
            "carrier": "one-dimensional array of cells",
            "alphabet_or_value_schema": "three possible colors for each cell",
            "seed": "a random initial condition",
            "read_dependencies_or_neighborhood": "nearest neighbors, read totalistically",
            "law_kind": "totalistic nearest-neighbor cellular-automaton rule",
            "rule_relation_constraint_function_or_probability_law": (
                f"preset code {code} under the source's three-color nearest-neighbor totalistic code scheme"
            ),
            "result_kind": "a finite 1500-step evolution from a random initial condition",
            "parameters_and_variants": f"code {code}; displayed run length 1500 steps",
        }
        clone["variants"] = [f"code {code}"]
        clone["variant_units"] = {f"code {code}": units}
        clone["field_units"] = {
            "rule_relation_constraint_function_or_probability_law": [semantic_units[-1]],
            "parameters_and_variants": units,
        }
        clone["evidence_overrides"] = {}
        panel_clones.append(clone)
    panel_index = defs.index(panel)
    defs[panel_index : panel_index + 1] = panel_clones

    # Keep spatial slice projection/depth fog separate from the prior-time
    # gray-trail representation used in the Game of Life panels.
    combined_slice = next(
        row
        for row in defs
        if row["name"] == "one-dimensional slice-through-time and temporal-fog observer"
    )
    combined_slice["name"] = "one-dimensional slice-through-time and spatial-depth-fog observer"
    combined_slice["units"] = ["U001325", "U001326", "U001327", "U001334", "U001335"]
    combined_slice["semantic_units"] = ["U001325", "U001335"]
    combined_slice["mechanics_units"] = ["U001325"]
    combined_slice["values"]["rule_relation_constraint_function_or_probability_law"] = (
        "extract one spatial line through successive two-dimensional states and optionally show cells spatially "
        "farther behind the slice in progressively lighter gray"
    )
    combined_slice["values"]["visible_history"] = "spatial depth behind the selected slice"
    combined_slice["values"]["parameters_and_variants"] = (
        "slice position, spatial-depth fog shading, and displayed codes 4, 12, 24, 30, 38, and 52"
    )
    combined_slice["variants"] = [
        "code 4 slice",
        "code 12 slice",
        "code 24 slice",
        "code 30 slice",
        "code 38 slice",
        "code 52 slice",
        "spatial-depth fog",
    ]
    combined_slice["variant_units"] = {
        variant: ["U001334", "U001335"] for variant in combined_slice["variants"]
    }
    add(
        "prior-time gray-trail rendering observer",
        ["U001341"],
        ["U001341"],
        {
            **relation_values(
                "deterministic temporal-history rendering observer",
                carrier="a two-dimensional cellular-automaton history",
                input_value="the current state and cells that were black on preceding steps",
                law="render cells black on preceding steps in progressively lighter shades of gray",
                result="a layered gray trail behind current black cells",
            ),
            "visible_history": "preceding time layers",
            "read_dependencies_or_neighborhood": "the current cell and its prior-time black history",
            "parameters_and_variants": "Game of Life prior-time trail display",
            "excluded_observers_and_representations": (
                "the gray trail is an observer rendering and is not the Game of Life native state or transition law"
            ),
        },
        aliases=["temporal fog", "prior-step gray trail"],
        role="OBSERVER",
        strength="DIRECT_COMPLETE_MECHANICS",
        mechanics_units=["U001341"],
    )

    by_name = {candidate["name"]: candidate for candidate in defs}

    def candidate(name: str) -> dict[str, Any]:
        return by_name[name]

    def evidence(
        name: str,
        unit_id: str,
        *,
        fields: list[str],
        claim: str,
        strength: str = "DIRECT_PARTIAL_MECHANICS",
        allow_direct_image: bool = False,
    ) -> None:
        # evidence_limit is assigned once later to the strongest identity/law
        # anchor for the whole candidate, never piecemeal by unit overrides.
        fields = [field for field in fields if field != "evidence_limit"]
        candidate(name)["evidence_overrides"][unit_id] = {
            "fields": fields,
            "claim": claim,
            "strength": strength,
            "allow_direct_image": allow_direct_image,
        }

    def configure_family(
        name: str,
        *,
        object_kind: str,
        law: str,
        parameters: str,
        variants: list[str],
        image_unit: str,
        caption_unit: str,
    ) -> None:
        row = candidate(name)
        prior_values = row["values"]
        row["values"] = {
            "object_kind": object_kind,
            "carrier": prior_values["carrier"],
            "alphabet_or_value_schema": prior_values["alphabet_or_value_schema"],
            "read_dependencies_or_neighborhood": prior_values[
                "read_dependencies_or_neighborhood"
            ],
            "law_kind": "parameterized cellular-automaton rule family",
            "rule_relation_constraint_function_or_probability_law": law,
            "result_kind": "the behavior of a selected family member",
            "parameters_and_variants": parameters,
        }
        row["mechanics_units"] = [caption_unit]
        row["variants"] = variants
        row["variant_units"] = {variant: [image_unit, caption_unit] for variant in variants}
        evidence(
            name,
            image_unit,
            fields=["parameters_and_variants"],
            claim=f"Original-resolution survey image preserves the complete labeled inventory for {name}: {parameters}.",
            strength="DIRECT_PARTIAL_MECHANICS",
            allow_direct_image=True,
        )

    # Exact image-borne survey inventories and family semantics.
    configure_family(
        "symmetric quiescent-white binary nearest-neighbor cellular-automaton family",
        object_kind="parameterized one-dimensional binary nearest-neighbor cellular-automaton family",
        law=(
            "choose one of the 32 symmetric nearest-neighbor binary rule tables that leave the all-white state unchanged"
        ),
        parameters=(
            "rule code in {0,4,18,22,32,36,50,54,72,76,90,94,104,108,122,126,"
            "128,132,146,150,160,164,178,182,200,204,218,222,232,236,250,254}"
        ),
        variants=[
            f"rule {code}"
            for code in (
                0,
                4,
                18,
                22,
                32,
                36,
                50,
                54,
                72,
                76,
                90,
                94,
                104,
                108,
                122,
                126,
                128,
                132,
                146,
                150,
                160,
                164,
                178,
                182,
                200,
                204,
                218,
                222,
                232,
                236,
                250,
                254,
            )
        ],
        image_unit="U001272",
        caption_unit="U001273",
    )
    configure_family(
        "binary next-nearest-neighbor totalistic cellular-automaton family",
        object_kind="parameterized binary next-nearest-neighbor totalistic cellular-automaton family",
        law="choose a binary totalistic nearest-and-next-nearest-neighbor code from the displayed even-code survey",
        parameters="even totalistic code from 0 through 62",
        variants=[f"code {code}" for code in range(0, 63, 2)],
        image_unit="U001274",
        caption_unit="U001275",
    )
    configure_family(
        "three-color nearest-neighbor totalistic cellular-automaton family",
        object_kind="parameterized three-color nearest-neighbor totalistic cellular-automaton family",
        law="choose a three-color nearest-neighbor totalistic rule from the displayed code sequence",
        parameters="totalistic code from 1002 through 1095 in increments of 3",
        variants=[f"code {code}" for code in range(1002, 1096, 3)],
        image_unit="U001276",
        caption_unit="U001277",
    )
    configure_family(
        "four-color nearest-neighbor totalistic cellular-automaton sequence",
        object_kind="parameterized four-color nearest-neighbor totalistic cellular-automaton survey",
        law="choose a four-color nearest-neighbor totalistic rule from the displayed transition survey",
        parameters="totalistic code from 1000816 through 1000940 in increments of 4",
        variants=[f"code {code}" for code in range(1000816, 1000941, 4)],
        image_unit="U001305",
        caption_unit="U001306",
    )

    # General random-field variants: every unit supports only the carrier/domain it actually states.
    random_name = "random cellular-automaton initial-field generator family"
    candidate(random_name)["values"]["topology"] = "one-dimensional row or two-dimensional square grid selected by the target system"
    candidate(random_name)["field_units"]["topology"] = ["U001227", "U001324", "U001331"]
    evidence(
        random_name,
        "U001227",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "topology",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "termination_completion_failure",
            "parameters_and_variants",
            "evidence_limit",
        ],
        claim="U001227 defines the one-dimensional binary variant by choosing every cell black or white at random.",
    )
    evidence(
        random_name,
        "U001316",
        fields=[
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "parameters_and_variants",
        ],
        claim="U001316 states a random continuous initial field whose cells take gray levels in [0,1].",
    )
    evidence(
        random_name,
        "U001324",
        fields=["carrier", "topology", "complete_state", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
        claim="U001324 identifies a two-dimensional cellular-automaton random-initial-field variant without specifying its measure.",
        strength="DIRECT_IDENTITY",
    )
    evidence(
        random_name,
        "U001331",
        fields=[
            "carrier",
            "topology",
            "alphabet_or_value_schema",
            "complete_state",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "parameters_and_variants",
        ],
        claim="U001331 states that the displayed two-dimensional binary totalistic systems start from random initial fields.",
    )
    evidence(
        random_name,
        "U001333",
        fields=["carrier", "complete_state", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
        claim="U001333 corroborates the two-dimensional random-field variant in a 500-step rule survey.",
        strength="CORROBORATING",
    )
    evidence(
        random_name,
        "U001416",
        fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
        claim="U001416 states that rule 90 needs infinitely many randomly placed black cells to obtain a random pattern.",
    )
    evidence(
        random_name,
        "U001421",
        fields=["parameters_and_variants"],
        claim="U001421 supplies the low-black-density binary random-field variant.",
        strength="CORROBORATING",
    )

    # Code-specific panel evidence: one row supports one displayed code, never the whole panel.
    code_units = {
        "1815": ("U001286", "U001287"),
        "2007": ("U001288", "U001289"),
        "1659": ("U001290", "U001290"),
        "2043": ("U001291", "U001292"),
    }
    for code, (image_unit, identity_unit) in code_units.items():
        preset_name = f"three-color nearest-neighbor totalistic cellular automaton code {code}"
        evidence(
            preset_name,
            image_unit,
            fields=["parameters_and_variants"]
            + (
                ["rule_relation_constraint_function_or_probability_law"]
                if image_unit == identity_unit
                else []
            ),
            claim=(
                f"{image_unit} is the original-resolution finite evolution"
                f"{' and visible identity label' if image_unit == identity_unit else ''} for code {code}; "
                "it supports no other preset."
            ),
            strength="DIRECT_IDENTITY" if image_unit == identity_unit else "CONTEXTUAL",
            allow_direct_image=image_unit == identity_unit,
        )
        if identity_unit != image_unit:
            evidence(
                preset_name,
                identity_unit,
                fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
                claim=f"{identity_unit} supplies only the code-{code} identity for its preceding evolution panel.",
                strength="DIRECT_IDENTITY",
            )

    # Borderline classifier panels retain their exact image-borne code identities.
    classifier_name = "four-class cellular-automaton behavior classification"
    classifier = candidate(classifier_name)
    classifier["units"].extend(["U001294", "U001295", "U001296", "U001297"])
    classifier["variants"] = [
        "code 219: class 2 or 4",
        "code 438: class 3 or 4",
        "code 1380: class 2 or 3",
        "code 1632: class 1, 2, or 3",
    ]
    classifier["variant_units"] = {
        "code 219: class 2 or 4": ["U001294", "U001298"],
        "code 438: class 3 or 4": ["U001295", "U001298"],
        "code 1380: class 2 or 3": ["U001296", "U001298"],
        "code 1632: class 1, 2, or 3": ["U001297", "U001298"],
    }
    for unit_id, code in zip(
        ["U001294", "U001295", "U001296", "U001297"],
        ["219", "438", "1380", "1632"],
    ):
        evidence(
            classifier_name,
            unit_id,
            fields=["rule_relation_constraint_function_or_probability_law"],
            claim=f"Original-resolution borderline-case panel identifies totalistic code {code}; the class ambiguity is transcribed by U001298.",
            strength="CONTEXTUAL",
        )

    # Continuous native laws explicitly exclude the neighbor-difference display.
    continuous_name = "fractional-average continuous cellular automaton"
    continuous = candidate(continuous_name)
    continuous["units"].append("U001323")
    continuous["mechanics_units"] = []
    continuous["values"] = {
        "object_kind": "one-dimensional continuous cellular-automaton family",
        "native_time": "successive discrete steps",
        "carrier": "a row of cells",
        "alphabet_or_value_schema": "a gray level in [0,1] for each cell",
        "seed": "a random initial condition",
        "frontier_or_activation": "each cell at each step",
        "read_dependencies_or_neighborhood": "the cell and its two adjacent neighbors",
        "law_kind": "deterministic local fractional-average transition law",
        "rule_relation_constraint_function_or_probability_law": (
            "average the cell and its two neighbors, add the selected constant, and retain the fractional part"
        ),
        "write_replacement_assembly_or_commit": "use the resulting fractional part as the cell's next gray level",
        "result_kind": "a successive gray-level field evolution",
        "determinism_branching_or_measure": "deterministic for a fixed constant and initial field",
        "parameters_and_variants": "additive constant in [0,1], including displayed values 0.398 and 0.4",
        "excluded_observers_and_representations": (
            "the neighbor-difference gray rendering in U001323 is derived display data, not the automaton's native gray-level state"
        ),
    }
    continuous["field_units"]["excluded_observers_and_representations"] = ["U001323"]
    evidence(
        continuous_name,
        "U001316",
        fields=[
            field
            for field in continuous["values"]
            if field != "excluded_observers_and_representations"
        ],
        claim=(
            "U001316 defines the continuous-cellular-automaton update over gray levels in [0,1], "
            "including the random initial field, three-cell average, additive constant, and fractional-part write."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        continuous_name,
        "U001323",
        fields=["excluded_observers_and_representations"],
        claim="U001323 explicitly distinguishes actual continuous-CA gray levels from the neighbor-difference values used for display.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    weighted_name = "neighbor-weighted fractional-average continuous cellular automaton"
    weighted = candidate(weighted_name)
    weighted["mechanics_units"] = []
    weighted["values"] = {
        "object_kind": "neighbor-weighted continuous cellular-automaton preset",
        "native_time": "successive discrete steps",
        "carrier": "a row of continuous-valued cells",
        "alphabet_or_value_schema": "a gray level in [0,1] for each cell",
        "read_dependencies_or_neighborhood": "the cell and its two adjacent neighbors",
        "law_kind": "deterministic local weighted fractional-average transition law",
        "rule_relation_constraint_function_or_probability_law": (
            "multiply the two neighboring gray levels by 1.13 while leaving the central cell unweighted, "
            "average the three values, add 0.5, and retain the fractional part"
        ),
        "write_replacement_assembly_or_commit": "use the resulting fractional part as the cell's next gray level",
        "result_kind": "a successive continuous gray-level evolution",
        "determinism_branching_or_measure": "deterministic for the stated parameters and an initial field",
        "parameters_and_variants": "displayed parameter pair {0.5, 1.13}",
        "excluded_observers_and_representations": (
            "the neighbor-difference gray rendering is a post-evolution display and is not part of this native update law"
        ),
    }
    weighted["uncertainties"] = []
    evidence(
        weighted_name,
        "U001321",
        fields=[],
        claim="A000956 is the displayed class-4 evolution witness; its differenced rendering does not independently establish the native weighted update.",
        strength="CONTEXTUAL",
    )
    evidence(
        weighted_name,
        "U001322",
        fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
        claim="U001322 supplies only the displayed parameter pair {0.5, 1.13}.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        weighted_name,
        "U001323",
        fields=[
            field
            for field in weighted["values"]
            if field != "parameters_and_variants"
        ],
        claim=(
            "U001323 defines the weighted-neighbor exception to the preceding continuous rule and explicitly "
            "separates the neighbor-difference display from the native gray levels."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    # New display observers use distinct spatial-depth and prior-time fog variants.
    difference_name = "neighbor-difference gray-field display transformation"
    difference = candidate(difference_name)
    difference["units"] = ["U001317", "U001319", "U001321", "U001323"]
    difference["semantic_units"] = ["U001317", "U001319", "U001321", "U001323"]
    difference["anchor_priority"] = 1
    difference["mechanics_units"] = []
    difference["values"] = {
        "object_kind": "derived gray-field display transformation",
        "native_time": "applied to each displayed continuous-cellular-automaton step",
        "carrier": "a continuous gray-level cell field",
        "input": "the actual gray levels of a cell and a neighboring cell",
        "read_dependencies_or_neighborhood": "a cell and one unspecified neighbor",
        "law_kind": "neighbor-difference display transformation",
        "rule_relation_constraint_function_or_probability_law": (
            "display a difference between each cell's native gray level and a neighbor's gray level"
        ),
        "result_kind": "a derived gray-level image with uniform stripes removed",
        "determinism_branching_or_measure": (
            "deterministic once the unspecified neighbor, sign/absolute-value convention, and gray remapping are fixed"
        ),
        "excluded_observers_and_representations": (
            "the displayed differences are not the continuous cellular automaton's native gray-level state"
        ),
    }
    difference["uncertainties"] = [
        "The source does not state which neighbor is selected, whether the difference is signed or absolute, or how it is remapped to display gray."
    ]
    difference["parameters"] = [
        "neighbor selection",
        "difference convention",
        "gray remapping",
    ]
    for unit_id, asset_id in [
        ("U001317", "A000954"),
        ("U001319", "A000955"),
    ]:
        evidence(
            difference_name,
            unit_id,
            fields=[],
            claim=(
                f"{asset_id} is one of the three original-resolution page-259 evolutions whose "
                "display gray levels U001323 defines as neighbor differences; it supplies observer "
                "output rather than additional transformation mechanics."
            ),
            strength="CONTEXTUAL",
        )
    evidence(
        difference_name,
        "U001321",
        fields=[],
        claim=(
            "A000956 is the original-resolution neighbor-difference rendering output linked to this "
            "observer; U001323 supplies the transformation prose."
        ),
        strength="CONTEXTUAL",
    )
    evidence(
        difference_name,
        "U001323",
        fields=list(difference["values"]),
        claim=(
            "U001323 defines the displayed values as differences between each native cell gray level and "
            "a neighbor, while leaving direction, sign convention, and gray remapping unspecified."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    slice_name = "one-dimensional slice-through-time and spatial-depth-fog observer"
    slice_candidate = candidate(slice_name)
    slice_candidate["aliases"] = [
        "one-dimensional slice observer",
        "slice-history projection",
        "spatial-depth fog display",
    ]
    slice_candidate["parameters"] = ["slice location", "spatial-depth fog enabled"]
    slice_candidate["mechanics_units"] = []
    slice_candidate["values"] = {
        "object_kind": "one-dimensional slice-through-time observer with an optional spatial-depth display",
        "native_time": "the source cellular automaton's successive steps",
        "carrier": "a two-dimensional cellular-automaton space-time history",
        "input": "a two-dimensional evolution and a selected one-dimensional slice",
        "visible_history": "the selected slice across a whole sequence of steps",
        "read_dependencies_or_neighborhood": (
            "cells on the selected slice; the depth-fog variant also reads cells spatially behind the slice"
        ),
        "law_kind": "deterministic projection and spatial-depth display transformation",
        "rule_relation_constraint_function_or_probability_law": (
            "extract the selected one-dimensional slice at every step; optionally render cells farther "
            "behind the slice progressively lighter"
        ),
        "result_kind": "a one-dimensional slice history, optionally with spatial-depth fog",
        "determinism_branching_or_measure": "deterministic once the slice and display convention are selected",
        "witness_semantics": "the projected history exposes behavioral classes without changing the native evolution",
        "parameters_and_variants": "slice location and optional spatial-depth fog",
        "excluded_observers_and_representations": (
            "the slice and depth fog are observer projections, not native two-dimensional states"
        ),
    }
    evidence(
        slice_name,
        "U001325",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "input",
            "visible_history",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "witness_semantics",
            "parameters_and_variants",
            "excluded_observers_and_representations",
        ],
        claim=(
            "U001325 defines the one-dimensional slice-through-time projection over a whole sequence "
            "of two-dimensional cellular-automaton steps."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        slice_name,
        "U001326",
        fields=["result_kind", "parameters_and_variants"],
        claim="U001326 states that one-dimensional slice histories expose the same four behavioral classes.",
        strength="CORROBORATING",
    )
    evidence(
        slice_name,
        "U001327",
        fields=["parameters_and_variants"],
        claim="U001327 identifies the class-4 repetitive-background slice comparison and routes its examples.",
        strength="CONTEXTUAL",
    )
    evidence(
        slice_name,
        "U001334",
        fields=["result_kind", "parameters_and_variants"],
        claim="A000959 is the original-resolution slice-history survey labeled with codes 4, 12, 24, 30, 38, and 52.",
        strength="CONTEXTUAL",
    )
    evidence(
        slice_name,
        "U001335",
        fields=[
            "carrier",
            "input",
            "visible_history",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
        ],
        claim="U001335 defines the spatial-depth fog variant: cells farther behind the slice are shown progressively lighter.",
    )
    trail_name = "prior-time gray-trail rendering observer"
    trail = candidate(trail_name)
    trail["units"].extend(["U001336", "U001338", "U001339", "U001340"])
    trail["semantic_units"].extend(["U001336", "U001338", "U001339", "U001340"])
    trail["mechanics_units"] = []
    trail["values"] = {
        "object_kind": "prior-time gray-trail rendering observer",
        "native_time": "the source cellular automaton's preceding steps",
        "carrier": "a two-dimensional cellular-automaton history",
        "input": "current black cells and cells that were black on preceding steps",
        "visible_history": "preceding black-cell time layers",
        "read_dependencies_or_neighborhood": "the current cell and its prior black-state history",
        "law_kind": "deterministic temporal-history rendering transformation",
        "rule_relation_constraint_function_or_probability_law": (
            "show cells black on preceding steps in progressively lighter shades of gray"
        ),
        "result_kind": "a layered gray trail behind current black cells",
        "determinism_branching_or_measure": "deterministic for the selected history depth and shade convention",
        "witness_semantics": "the trail displays past occupancy without changing the Game of Life evolution",
        "parameters_and_variants": "Game of Life prior-time trail display",
        "excluded_observers_and_representations": (
            "the gray trail is a rendering and not the Game of Life native state or transition law"
        ),
    }
    trail["uncertainties"] = [
        "The source does not state the retained history depth or the exact mapping from temporal age to gray shade."
    ]
    trail["parameters"] = ["retained history depth", "age-to-gray mapping"]
    for unit_id in ["U001336", "U001338", "U001339", "U001340"]:
        evidence(
            trail_name,
            unit_id,
            fields=["visible_history", "result_kind", "witness_semantics"],
            claim=f"{unit_id} is an original-resolution prior-time gray-trail output linked to the rendering observer.",
            strength="CONTEXTUAL",
        )
    evidence(
        trail_name,
        "U001341",
        fields=list(trail["values"]),
        claim="U001341 defines the distinct prior-time trail variant for Game of Life by fading cells black on preceding steps.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    # Life and two-dimensional-family records distinguish native laws from
    # slice/fog observer outputs.
    life_name = "Game of Life cellular automaton"
    life = candidate(life_name)
    life["mechanics_units"] = []
    life["values"] = {
        "object_kind": "class-4 two-dimensional cellular-automaton preset",
        "native_time": "successive steps",
        "carrier": "a two-dimensional field of cells",
        "topology": "eight-neighbor square-grid adjacency including diagonals",
        "alphabet_or_value_schema": "black and white cell colors",
        "complete_state": "the current black-or-white color of every cell",
        "read_dependencies_or_neighborhood": "the eight neighbors of a cell, including diagonals",
        "law_kind": "outer-totalistic local cellular-automaton transition law",
        "rule_relation_constraint_function_or_probability_law": (
            "with two black neighbors retain the cell's prior color; with three become black; "
            "with any other count become white"
        ),
        "write_replacement_assembly_or_commit": "set each next cell color from its current color and black-neighbor count",
        "result_kind": "the next two-dimensional black-or-white configuration",
        "determinism_branching_or_measure": "deterministic",
        "parameters_and_variants": "Game of Life; outer-totalistic 9-neighbor code 224",
        "witness_semantics": (
            "finite step panels witness localized structures; gray trails and slices are derived observer renderings"
        ),
        "excluded_observers_and_representations": (
            "one-dimensional slices and progressively lighter prior-step trails are observer outputs, not the native Life state"
        ),
    }
    evidence(
        life_name,
        "U001329",
        fields=["object_kind", "parameters_and_variants"],
        claim="U001329 identifies Game of Life and its localized-structure behavior but does not state the transition table.",
        strength="DIRECT_IDENTITY",
    )
    for unit_id in ["U001336", "U001338", "U001339", "U001340"]:
        evidence(
            life_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a finite Game-of-Life behavior/trail witness and does not independently establish the native rule.",
            strength="CONTEXTUAL",
        )
    evidence(
        life_name,
        "U001337",
        fields=[],
        claim="U001337 is editorial source accounting for a legacy raster caption and adds no Life mechanics.",
        strength="CONTEXTUAL",
    )
    evidence(
        life_name,
        "U001341",
        fields=list(life["values"]),
        claim=(
            "U001341 identifies Game of Life, gives its complete neighbor-count update and code 224, "
            "and explicitly identifies the lighter prior-step trail as a display."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    family_2d_name = "binary two-dimensional von-Neumann-totalistic cellular-automaton family"
    family_2d = candidate(family_2d_name)
    family_2d["units"].extend(["U001334", "U001335"])
    family_2d["mechanics_units"] = []
    family_2d["values"] = {
        "object_kind": "parameterized binary two-dimensional von-Neumann-totalistic cellular-automaton family",
        "native_time": "successive evolution steps",
        "carrier": "a two-dimensional field of cells",
        "topology": "a square grid with four immediate orthogonal neighbors",
        "alphabet_or_value_schema": "binary cell colors",
        "seed": "a random initial condition in the displayed examples",
        "read_dependencies_or_neighborhood": "the cell and its four immediate orthogonal neighbors",
        "law_kind": "six-bit totalistic cellular-automaton code family",
        "rule_relation_constraint_function_or_probability_law": (
            "successive base-2 code digits give the output for neighborhood totals from 5 down to 0"
        ),
        "result_kind": "a two-dimensional cellular-automaton evolution",
        "structural_invariants": (
            "six output bits cover neighborhood totals 5 through 0, giving 64 family members; "
            "the displayed even-code subset leaves the all-white state unchanged"
        ),
        "parameters_and_variants": (
            "six-bit totalistic code; labeled examples 4,12,24,30,38,52 and the even-code survey 2,4,6,...,60"
        ),
        "excluded_observers_and_representations": (
            "the one-dimensional slice and spatial-depth fog panels are observer projections, not native two-dimensional states"
        ),
    }
    family_2d["variants"] = [f"code {code}" for code in range(2, 61, 2)]
    family_2d["variant_units"] = {
        f"code {code}": (
            ["U001330", "U001332", "U001333"]
            if code in {4, 12, 24, 30, 38, 52}
            else ["U001332", "U001333"]
        )
        for code in range(2, 61, 2)
    }
    family_2d["field_units"].update(
        {
            "structural_invariants": ["U001331", "U001333"],
            "parameters_and_variants": ["U001330", "U001331", "U001332", "U001333"],
            "excluded_observers_and_representations": ["U001334", "U001335"],
        }
    )
    evidence(
        family_2d_name,
        "U001330",
        fields=["parameters_and_variants"],
        claim="A000957 preserves the labeled native-family examples 4, 12, 24, 30, 38, and 52; it does not define the code convention.",
        strength="CONTEXTUAL",
    )
    evidence(
        family_2d_name,
        "U001331",
        fields=[
            field
            for field in family_2d["values"]
            if field != "excluded_observers_and_representations"
        ],
        claim=(
            "U001331 defines the two-dimensional totalistic code family, its five-cell orthogonal "
            "neighborhood, binary code ordering, random-start examples, and resulting evolutions."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        family_2d_name,
        "U001332",
        fields=["parameters_and_variants"],
        claim="A000958 preserves the labeled even-code survey 2,4,6,...,60 as finite 500-step outcomes.",
        strength="CONTEXTUAL",
    )
    evidence(
        family_2d_name,
        "U001333",
        fields=["structural_invariants", "parameters_and_variants"],
        claim="U001333 states that the broader survey includes most of the 64 rules that leave the all-white state unchanged.",
        strength="CORROBORATING",
    )
    evidence(
        family_2d_name,
        "U001334",
        fields=["excluded_observers_and_representations"],
        claim="A000959 is a slice-history observer output linked to this family, not a native two-dimensional state.",
        strength="CONTEXTUAL",
    )
    evidence(
        family_2d_name,
        "U001335",
        fields=["excluded_observers_and_representations"],
        claim="U001335 explicitly describes the one-dimensional slice and spatial-depth fog transformation.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    perturb_name = "single-cell initial-perturbation difference observer"
    perturb = candidate(perturb_name)
    perturb["mechanics_units"] = ["U001346"]
    perturb["parameters"] = [
        "cellular-automaton rule",
        "base initial condition",
        "changed cell",
    ]
    evidence(
        perturb_name,
        "U001344",
        fields=["input"],
        claim="U001344 supplies the paired-run input condition: change the initial color of one cell.",
    )
    evidence(
        perturb_name,
        "U001345",
        fields=[],
        claim="A000965 is a finite four-class comparison witness; the difference-mask rule is stated in U001346.",
        strength="CONTEXTUAL",
    )
    evidence(
        perturb_name,
        "U001348",
        fields=["result_kind", "witness_semantics"],
        claim="U001348 records the class-dependent fate of a one-cell perturbation, not the comparison algorithm.",
        strength="CORROBORATING",
    )
    for unit_id in ["U001349", "U001350", "U001351"]:
        evidence(
            perturb_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a class-3 or class-4 perturbation-spread witness.",
            strength="CONTEXTUAL",
        )
    evidence(
        perturb_name,
        "U001352",
        fields=["input", "witness_semantics"],
        claim="U001352 identifies three class-3 one-cell-change comparisons.",
        strength="CORROBORATING",
    )
    evidence(
        perturb_name,
        "U001359",
        fields=["result_kind", "witness_semantics"],
        claim="U001359 states that rule-110 perturbations spread through localized structures.",
        strength="CORROBORATING",
    )
    for unit_id in ["U001360", "U001361"]:
        evidence(
            perturb_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a finite rule-110 perturbation witness.",
            strength="CONTEXTUAL",
        )
    evidence(
        perturb_name,
        "U001362",
        fields=["input"],
        claim="U001362 labels the comparison as one changed initial cell and adds no observer mechanics.",
        strength="CORROBORATING",
    )

    # Finite-system invariants and the dedicated repetition-period observer.
    translation_name = "finite cyclic translation of a single dot"
    translation = candidate(translation_name)
    translation["mechanics_units"] = []
    translation["values"].pop("input", None)
    translation["values"]["structural_invariants"] = (
        "the period is at most n and is maximal, equal to n, when displacement k is coprime to n"
    )
    translation["field_units"]["structural_invariants"] = ["U001375", "U001376"]
    evidence(
        translation_name,
        "U001367",
        fields=[
            field
            for field in translation["values"]
            if field not in {"termination_completion_failure", "structural_invariants"}
        ],
        claim=(
            "U001367 defines the single-dot cyclic translation: six positions in the first examples, "
            "a fixed rightward displacement each step, and wraparound at the right edge."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        translation_name,
        "U001369",
        fields=["termination_completion_failure", "parameters_and_variants"],
        claim="U001369 states that the six-position translation is always repetitive and varies the displacement.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        translation_name,
        "U001375",
        fields=["structural_invariants"],
        claim="U001375 states that finite-system period may reach its state-count maximum but depends on size and rule.",
    )
    evidence(
        translation_name,
        "U001376",
        fields=["structural_invariants"],
        claim="U001376 gives the maximal-period condition gcd(k,n)=1 for cyclic translation.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    doubling_name = "finite cyclic doubling map"
    doubling = candidate(doubling_name)
    doubling["mechanics_units"] = []
    doubling["values"].pop("input", None)
    doubling["values"]["rule_relation_constraint_function_or_probability_law"] = (
        "replace position x by 2x modulo the system size n"
    )
    doubling["values"]["structural_invariants"] = (
        "the period is at most n; for odd n the displayed period is MultiplicativeOrder[2,n]"
    )
    doubling["field_units"]["structural_invariants"] = ["U001380", "U001381"]
    evidence(
        doubling_name,
        "U001377",
        fields=[
            field
            for field in doubling["values"]
            if field not in {"termination_completion_failure", "structural_invariants"}
        ],
        claim=(
            "U001377 defines the cyclic doubling map by doubling the dot's numeric position each step "
            "and wrapping at the right edge."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    for unit_id in ["U001378", "U001379"]:
        evidence(
            doubling_name,
            unit_id,
            fields=[],
            claim=f"{unit_id} is a finite orbit or period-plot witness for the doubling map.",
            strength="CONTEXTUAL",
        )
    evidence(
        doubling_name,
        "U001380",
        fields=["rule_relation_constraint_function_or_probability_law", "structural_invariants", "parameters_and_variants"],
        claim="U001380 gives x_t=Mod[2^t,n] and period MultiplicativeOrder[2,n] for odd n.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        doubling_name,
        "U001381",
        fields=["termination_completion_failure", "structural_invariants"],
        claim="U001381 states the at-most-n bound and size-factor dependence.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    finite_ca_name = "finite cyclic binary cellular automaton"
    finite_ca = candidate(finite_ca_name)
    finite_ca["units"].extend(["U001385", "U001387", "U001389", "U001393"])
    finite_ca["mechanics_units"] = []
    finite_ca["values"] = {
        "object_kind": "parameterized finite cyclic binary cellular-automaton family",
        "native_time": "successive cellular-automaton steps",
        "carrier": "a finite row of n cells arranged as a cycle",
        "support": "n cells",
        "topology": "a one-dimensional cycle",
        "alphabet_or_value_schema": "black and white",
        "complete_state": "one black-or-white arrangement of all n cells",
        "boundary": "the leftmost and rightmost cells are mutual neighbors",
        "read_dependencies_or_neighborhood": "the selected rule's ordinary neighborhood with cyclic wraparound",
        "law_kind": "a selected cellular-automaton rule applied on the finite cyclic carrier",
        "rule_relation_constraint_function_or_probability_law": (
            "apply the selected cellular-automaton rule with the stated cyclic boundary; member transition tables "
            "are not defined by this family passage"
        ),
        "result_kind": "a finite orbit that eventually repeats",
        "determinism_branching_or_measure": "deterministic for a selected rule and initial state",
        "termination_completion_failure": "iteration is ultimately repetitive",
        "parameters_and_variants": "cell count n and selected cellular-automaton rule",
        "structural_invariants": (
            "the finite deterministic orbit eventually repeats and has period at most 2^n for n binary cells"
        ),
        "excluded_observers_and_representations": (
            "finite evolution panels and period-versus-size curves are measurements of instantiated rules, not native transition definitions"
        ),
    }
    finite_ca["field_units"].update(
        {
            "structural_invariants": ["U001385", "U001387", "U001389", "U001391"],
            "excluded_observers_and_representations": ["U001393"],
        }
    )
    evidence(
        finite_ca_name,
        "U001390",
        fields=["parameters_and_variants"],
        claim="A000975 preserves finite-cycle examples labeled rule 90 and rule 30.",
        strength="CONTEXTUAL",
    )
    evidence(
        finite_ca_name,
        "U001383",
        fields=[
            "object_kind",
            "carrier",
            "support",
            "topology",
            "boundary",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        ],
        claim=(
            "U001383 defines the finite cyclic carrier and its left/right wraparound neighborhood; "
            "it does not supply any selected member's transition table."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        finite_ca_name,
        "U001387",
        fields=["alphabet_or_value_schema", "complete_state", "structural_invariants"],
        claim="U001387 identifies every black-or-white arrangement of n cells as a state and counts 2^n such states.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        finite_ca_name,
        "U001391",
        fields=[
            "native_time",
            "boundary",
            "result_kind",
            "determinism_branching_or_measure",
            "termination_completion_failure",
            "structural_invariants",
        ],
        claim="U001391 states the cyclic boundary and eventual repetition of each finite cellular-automaton orbit.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id, claim in {
        "U001385": "U001385 bounds any finite-system period by its number of possible states.",
        "U001389": "U001389 applies the 2^n bound to any pattern occupying n cells.",
        "U001393": "U001393 is a period-curve description and is explicitly excluded from native-law evidence.",
    }.items():
        fields = (
            ["excluded_observers_and_representations"]
            if unit_id == "U001393"
            else ["structural_invariants"]
        )
        evidence(
            finite_ca_name,
            unit_id,
            fields=fields,
            claim=claim,
            strength=(
                "DIRECT_PARTIAL_MECHANICS"
                if unit_id in {"U001385", "U001389", "U001393"}
                else "CORROBORATING"
            ),
        )
    rule45_name = "elementary cellular automaton rule 45 on a finite cycle"
    rule45 = candidate(rule45_name)
    rule45["units"] = ["U001388", "U001393"]
    rule45["semantic_units"] = ["U001388"]
    rule45["mechanics_units"] = ["U001388"]
    rule45["values"]["excluded_observers_and_representations"] = (
        "the rule-45 period curve is an observer result and does not define the rule-45 transition table"
    )
    rule45["field_units"]["excluded_observers_and_representations"] = ["U001393"]
    evidence(
        rule45_name,
        "U001393",
        fields=["excluded_observers_and_representations"],
        claim="U001393 reports rule-45 period scaling as an observer result; A000976 is not native rule-45 evidence.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    period_name = "finite-system repetition-period and maximum-period observer"
    period = candidate(period_name)
    period["units"] = ["U001366", "U001384", *period["units"]]
    period["semantic_units"] = ["U001366", "U001384", *period["semantic_units"]]
    period["mechanics_units"] = []
    period["parameters"] = [
        "finite system or cellular-automaton rule",
        "system size or state count",
        "initial state",
    ]
    period["uncertainties"] = [
        "The source gives bounds, measured curves, and rule-specific formulas but does not define a general period-computation algorithm."
    ]
    period_specs = {
        "U001366": (
            [
                "object_kind",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "termination_completion_failure",
                "structural_invariants",
            ],
            "U001366 states the general finite deterministic-system recurrence result: a discrete limited-size system following definite rules must eventually repeat.",
        ),
        "U001384": (
            [
                "carrier",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "termination_completion_failure",
            ],
            "U001384 applies the finite-system recurrence result to cyclic cellular automata and states that their behavior is ultimately repetitive.",
        ),
        "U001385": (
            ["object_kind", "native_time", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "termination_completion_failure", "evidence_limit"],
            "U001385 states that a finite definite-rule system must recur and bounds its period by its state count.",
        ),
        "U001386": (
            ["carrier", "support", "input", "parameters_and_variants"],
            "U001386 identifies state count with system size for the single-dot finite example.",
        ),
        "U001387": (
            ["carrier", "support", "complete_state", "rule_relation_constraint_function_or_probability_law", "structural_invariants", "parameters_and_variants"],
            "U001387 gives 2^n possible configurations for n binary cellular-automaton cells.",
        ),
        "U001388": (
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001388 identifies rule- and size-dependent repetition measurements and rule 45's near-maximum behavior.",
        ),
        "U001389": (
            ["support", "rule_relation_constraint_function_or_probability_law", "structural_invariants", "result_kind", "termination_completion_failure"],
            "U001389 applies the 2^n period bound to a pattern confined to n cells.",
        ),
        "U001390": (
            ["witness_semantics", "parameters_and_variants"],
            "A000975 is an original-resolution finite-orbit witness labeled rules 90 and 30.",
        ),
        "U001391": (
            ["carrier", "input", "result_kind", "termination_completion_failure", "parameters_and_variants"],
            "U001391 states that finite cyclic cellular automata eventually repeat and their periods can grow with size.",
        ),
        "U001392": (
            ["input", "result_kind", "witness_semantics", "parameters_and_variants", "excluded_observers_and_representations"],
            "A000976 is the original-resolution period-versus-size observer for rules 90, 30, 45, and 110.",
        ),
        "U001393": (
            [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "structural_invariants",
                "result_kind",
                "determinism_branching_or_measure",
                "witness_semantics",
                "parameters_and_variants",
                "excluded_observers_and_representations",
            ],
            "U001393 supplies the single-black seed and the rule-specific period formulas or scalings for rules 90, 30, 45, and 110.",
        ),
    }
    for unit_id, (fields, claim) in period_specs.items():
        evidence(
            period_name,
            unit_id,
            fields=fields,
            claim=claim,
            strength="CONTEXTUAL" if unit_id == "U001390" else "DIRECT_PARTIAL_MECHANICS",
        )

    # Additivity is a separate source relation; route-bearing comparison units
    # are also retained as contextual provenance on the relevant native rules.
    additivity_name = "additive cellular-automaton superposition relation"
    additivity = candidate(additivity_name)
    additivity["semantic_units"].append("U001411")
    additivity["mechanics_units"] = []
    additivity["parameters"] = [
        "additive cellular-automaton rule",
        "component initial configurations",
    ]
    additivity["uncertainties"] = [
        "The source states superposition consequences but does not define the algebraic superposition operator in this range."
    ]
    additivity_specs = {
        "U001411": (
            [],
            "U001411 motivates the special simple-initial-condition case and supplies no additivity mechanics.",
            "CONTEXTUAL",
        ),
        "U001412": (
            ["carrier", "input", "law_kind", "rule_relation_constraint_function_or_probability_law", "result_kind", "witness_semantics"],
            "U001412 states that the displayed rule-90 patterns are superpositions of its single-black-cell nested pattern.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001413": (
            ["witness_semantics"],
            "A000981 is a finite rule-90 superposition witness and does not define the superposition operation.",
            "CONTEXTUAL",
        ),
        "U001414": (
            [
                "object_kind",
                "native_time",
                "carrier",
                "complete_state",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "determinism_branching_or_measure",
                "termination_completion_failure",
                "witness_semantics",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U001414 names rule 90's additivity and states that arbitrary-initial-condition patterns are superpositions of the basic nested pattern.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001463": (
            ["rule_relation_constraint_function_or_probability_law", "structural_invariants", "parameters_and_variants"],
            "U001463 identifies rules 90 and 150 as the only fundamentally different elementary additive rules.",
            "CORROBORATING",
        ),
        "U001464": (
            ["law_kind", "rule_relation_constraint_function_or_probability_law", "structural_invariants", "result_kind", "parameters_and_variants"],
            "U001464 states that any additive rule self-emulates and yields nested patterns.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
    }
    for unit_id, (fields, claim, strength) in additivity_specs.items():
        evidence(additivity_name, unit_id, fields=fields, claim=claim, strength=strength)

    for native_name in [
        "elementary cellular automaton rule 90",
        "elementary cellular automaton rule 22",
    ]:
        native = candidate(native_name)
        if native_name.endswith("rule 90"):
            native["units"].extend(["U001450", "U001463", "U001464"])
        else:
            native["units"].append("U001450")
        evidence(
            native_name,
            "U001450",
            fields=[],
            claim="U001450 routes the special rule-22 initial-condition emulation of rule 90; it is not native-law evidence.",
            strength="CORROBORATING",
        )
    for unit_id in ["U001463", "U001464"]:
        evidence(
            "elementary cellular automaton rule 90",
            unit_id,
            fields=["parameters_and_variants"],
            claim=f"{unit_id} identifies rule 90 as an additive rule; the additivity mechanics belong to the separate relation record.",
            strength="CORROBORATING",
        )

    # Periodic seeds are deterministic and include the source-delimited rule-110
    # 14-cell/7-step background variant.
    periodic_name = "periodic-block cellular-automaton initial-condition generator"
    periodic = candidate(periodic_name)
    periodic["units"].extend(["U001435", "U001558", "U001561", "U001570"])
    periodic["semantic_units"].append("U001435")
    periodic["parameters"] = ["finite period block", "spatial period"]
    periodic["values"].update(
        {
            "object_kind": "deterministic periodic-block initial-condition generator",
            "native_time": "one spatial repetition operation for a supplied finite block",
            "complete_state": "the unique bi-infinite periodic configuration generated by the supplied block",
            "result_kind": "one periodic initial configuration",
            "successor_cardinality": "one output configuration per supplied block",
            "determinism_branching_or_measure": "deterministic",
            "termination_completion_failure": "construction is complete once the finite period block is specified",
            "structural_invariants": (
                "an n-cell repeated block evolves like an n-cell cyclic system and therefore repeats within at most "
                "2^n steps; for rule 30, only repeated-block initial conditions can yield repetitive behavior"
            ),
            "parameters_and_variants": (
                "finite period block and width n; rule-30 fixed-period examples; rule-110 14-cell background with temporal period 7"
            ),
        }
    )
    periodic["mechanics_units"] = ["U001432", "U001433"]
    periodic["field_units"].update(
        {
            "structural_invariants": ["U001432", "U001433", "U001434"],
            "parameters_and_variants": ["U001432", "U001433", "U001434", "U001441", "U001558", "U001561", "U001570"],
        }
    )
    periodic["variants"].append("rule-110 14-cell periodic background with temporal period 7")
    periodic["variant_units"]["rule-110 14-cell periodic background with temporal period 7"] = [
        "U001558",
        "U001561",
        "U001570",
    ]
    periodic["related_names"] = ["elementary cellular automaton rule 110"]
    evidence(
        periodic_name,
        "U001434",
        fields=["structural_invariants", "parameters_and_variants"],
        claim="U001434 records attainable short periods and a missing exact period-2 block for rule 30.",
        strength="CORROBORATING",
    )
    evidence(
        periodic_name,
        "U001435",
        fields=[
            "object_kind",
            "rule_relation_constraint_function_or_probability_law",
            "structural_invariants",
            "parameters_and_variants",
        ],
        claim=(
            "U001435 states the rule-30 exclusivity result: no initial condition other than a single "
            "fixed block repeated forever can yield repetitive behavior."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        periodic_name,
        "U001441",
        fields=["parameters_and_variants"],
        claim="U001441 catalogs rule-30 repeated-block seeds through period 10 and the 275-cell period-11 block.",
        strength="CORROBORATING",
    )
    evidence(
        periodic_name,
        "U001558",
        fields=["result_kind", "parameters_and_variants"],
        claim="U001558 identifies rule 110's background as a 14-cell block repeating every 7 steps.",
        strength="CORROBORATING",
    )
    evidence(
        periodic_name,
        "U001561",
        fields=["result_kind", "parameters_and_variants"],
        claim="U001561 states that rule-110 structures are disruptions in the 14-cell/7-step periodic background.",
        strength="CORROBORATING",
    )
    evidence(
        periodic_name,
        "U001570",
        fields=["input", "result_kind", "parameters_and_variants"],
        claim="U001570 supplies a length-41 block inserted between periodic rule-110 background blocks as a seed variant.",
        strength="CORROBORATING",
    )

    two_block_name = "rule-126 random two-block initial-condition ensemble"
    two_block = candidate(two_block_name)
    two_block["values"]["alphabet_or_value_schema"] = "black and white cells"
    two_block["values"]["structural_invariants"] = "the configuration is tiled by permitted four-cell blocks BBWW and BBBW"
    two_block["values"]["parameters_and_variants"] = (
        "permitted blocks BBWW and BBBW; block probabilities, independence, and extent are not stated"
    )
    two_block["field_units"]["structural_invariants"] = ["U001439"]
    two_block["field_units"]["alphabet_or_value_schema"] = ["U001439"]
    two_block["mechanics_units"] = ["U001439"]
    two_block["parameters"] = ["permitted four-cell blocks", "block probability law"]

    # Block emulations expose their scale, codec, and temporal resampling as
    # structural invariants rather than hiding these mechanics in prose.
    block_repairs = {
        "rule-126 to rule-90 pair-block emulation": (
            "two-cell BB/WW blocks decode to one rule-90 cell and are sampled on alternate steps",
            ["U001444", "U001445", "U001448", "U001449"],
            [],
        ),
        "rule-90 pair-block self-emulation": (
            "two-cell spatial blocks, shown as 2-by-2 space-time tiles, decode to one rule-90 macrocell at two-step scale",
            ["U001453", "U001455", "U001456", "U001457", "U001458"],
            [
                "The exact two-cell black/white block codec is image-borne; the prose states only that an appropriate two-cell form is used."
            ],
        ),
        "rule-150 block self-emulation": (
            "two-cell spatial blocks, shown as 2-by-2 space-time tiles, decode to one rule-150 macrocell at two-step scale",
            ["U001459", "U001460", "U001461", "U001462", "U001463", "U001464"],
            [
                "The prose does not transcribe the full block codec; its two-cell/two-step realization is supplied by the owned images."
            ],
        ),
        "rule-184 three-cell-block self-emulation": (
            "three-cell spatial blocks, shown as 3-by-3 space-time tiles, decode to one rule-184 macrocell at three-step scale",
            ["U001465", "U001466", "U001467", "U001468", "U001469", "U001475"],
            [
                "The prose states the three-cell width, while the precise 3-by-3 block codec is image-borne."
            ],
        ),
    }
    for name, (invariant, units, uncertainties) in block_repairs.items():
        row = candidate(name)
        row["values"]["structural_invariants"] = invariant
        row["field_units"]["structural_invariants"] = units
        row["uncertainties"] = uncertainties
        for unit_id in units:
            if unit_id in row["units"] and unit_id not in row["mechanics_units"]:
                row["evidence_overrides"].setdefault(
                    unit_id,
                    {
                        "fields": ["structural_invariants"],
                        "claim": f"{unit_id} supports the stated block scale, decoding, or resampling invariant for {name}.",
                        "strength": "DIRECT_PARTIAL_MECHANICS",
                    },
                )

    # The emulation passages define block relations, not free-standing
    # time-evolving programs with generic completion semantics.
    emulation_specs = {
        "rule-126 to rule-90 pair-block emulation": {
            "values": {
                "object_kind": "block encoding and temporal-subsampling emulation relation",
                "carrier": "rule-126 configurations tiled by uniform two-cell blocks and decoded rule-90 cells",
                "input": "a rule-126 initial condition composed only of BB or WW pairs",
                "law_kind": "cellular-automaton block-emulation relation",
                "rule_relation_constraint_function_or_probability_law": (
                    "evolve rule 126 and inspect alternate steps; each uniform pair then behaves as one rule-90 cell"
                ),
                "result_kind": "the corresponding decoded rule-90 evolution",
                "parameters_and_variants": "source rule 126, target rule 90, two-cell blocks, alternate-step sampling",
            },
            "anchor": "U001444",
            "anchor_fields": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
                "structural_invariants",
            ],
            "detail": "U001445",
        },
        "rule-90 pair-block self-emulation": {
            "values": {
                "object_kind": "rule-90 block self-emulation relation",
                "carrier": "rule-90 configurations grouped into adjacent two-cell blocks",
                "input": "a rule-90 configuration encoded using an appropriate two-cell block form",
                "law_kind": "cellular-automaton block self-emulation relation",
                "rule_relation_constraint_function_or_probability_law": (
                    "the two-cell block configuration evolves according to rule 90 as individual rule-90 cells do"
                ),
                "result_kind": "a decoded rule-90 evolution at block scale",
                "parameters_and_variants": "rule 90 and an image-borne two-cell/two-step block codec",
            },
            "anchor": "U001452",
            "anchor_fields": [
                "object_kind",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
            ],
            "detail": "U001453",
        },
        "rule-150 block self-emulation": {
            "values": {
                "object_kind": "rule-150 block self-emulation relation",
                "carrier": "rule-150 configurations partitioned into the displayed blocks",
                "input": "a rule-150 configuration encoded using the displayed block form",
                "law_kind": "cellular-automaton block self-emulation relation",
                "rule_relation_constraint_function_or_probability_law": (
                    "the displayed blocks behave like individual cells under rule 150"
                ),
                "result_kind": "a decoded rule-150 evolution at block scale",
                "parameters_and_variants": "rule 150 and an image-borne two-cell/two-step block codec",
            },
            "anchor": "U001459",
            "anchor_fields": [
                "object_kind",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
            ],
            "detail": "U001463",
        },
        "rule-184 three-cell-block self-emulation": {
            "values": {
                "object_kind": "rule-184 three-cell-block self-emulation relation",
                "carrier": "rule-184 configurations partitioned into three-cell blocks",
                "input": "a rule-184 configuration encoded using the displayed three-cell blocks",
                "law_kind": "cellular-automaton block self-emulation relation",
                "rule_relation_constraint_function_or_probability_law": (
                    "each allowed three-cell block acts like one cell under rule 184"
                ),
                "result_kind": "a decoded rule-184 evolution at block scale",
                "parameters_and_variants": "rule 184 and an image-borne three-cell/three-step block codec",
            },
            "anchor": "U001465",
            "anchor_fields": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
                "structural_invariants",
            ],
            "detail": None,
        },
    }
    for name, spec in emulation_specs.items():
        row = candidate(name)
        invariant = row["values"]["structural_invariants"]
        row["values"] = {
            **spec["values"],
            "structural_invariants": invariant,
        }
        row["mechanics_units"] = []
        row["parameters"] = {
            "rule-126 to rule-90 pair-block emulation": [
                "source rule",
                "target rule",
                "spatial block width",
                "temporal sampling interval",
            ],
            "rule-90 pair-block self-emulation": [
                "cellular-automaton rule",
                "spatial block codec",
                "temporal sampling interval",
            ],
            "rule-150 block self-emulation": [
                "cellular-automaton rule",
                "spatial block codec",
                "temporal sampling interval",
            ],
            "rule-184 three-cell-block self-emulation": [
                "cellular-automaton rule",
                "spatial block codec",
                "temporal sampling interval",
            ],
        }[name]
        evidence(
            name,
            spec["anchor"],
            fields=spec["anchor_fields"],
            claim=(
                f"{spec['anchor']} establishes the source/target block-emulation identity and the "
                "listed prose-level relation; image-borne codec details remain bounded by the record uncertainty."
            ),
            strength="DIRECT_PARTIAL_MECHANICS",
        )
        if spec["detail"] is not None:
            evidence(
                name,
                spec["detail"],
                fields=[
                    "carrier",
                    "input",
                    "law_kind",
                    "rule_relation_constraint_function_or_probability_law",
                    "result_kind",
                    "structural_invariants",
                    "parameters_and_variants",
                ],
                claim=f"{spec['detail']} supplies the prose-level block scale, decoding, or resampling relation for {name}.",
                strength="DIRECT_PARTIAL_MECHANICS",
            )

    # Nested rule-184 seed is a deterministic iterative substitution generator.
    nested_name = "nested substitution initial condition for rule 184"
    nested = candidate(nested_name)
    nested["units"] = ["U001470", "U001471", "U001472", "U001474"]
    nested["semantic_units"] = ["U001470", "U001474"]
    nested["mechanics_units"] = []
    nested["values"] = {
        "object_kind": "deterministic iterative substitution initial-condition generator",
        "carrier": "a one-dimensional symbolic cell sequence",
        "alphabet_or_value_schema": "black and white cells",
        "seed": "one black element",
        "input": "the two stated substitution productions",
        "law_kind": "deterministic substitution-system law",
        "rule_relation_constraint_function_or_probability_law": "B -> BWB and W -> WWB, starting from one B",
        "result_kind": "a nested black-or-white initial condition for rule 184",
        "determinism_branching_or_measure": "deterministic",
        "structural_invariants": "the seed is generated from one black element using the two fixed productions",
    }
    nested["uncertainties"] = [
        "The source supplies the productions and seed but does not state a preferred finite depth for the displayed initial condition."
    ]
    nested["parameters"] = ["substitution depth"]
    evidence(
        nested_name,
        "U001470",
        fields=["object_kind", "law_kind"],
        claim="U001470 identifies the initial condition as an iterated substitution-system construction.",
    )
    evidence(
        nested_name,
        "U001471",
        fields=[],
        claim="U001471 describes rule-184 behavior from the nested seed and adds no substitution mechanics.",
        strength="CORROBORATING",
    )
    evidence(
        nested_name,
        "U001472",
        fields=[],
        claim="A001001 is the evolved nested-pattern witness; it does not encode the substitution productions.",
        strength="CONTEXTUAL",
    )
    evidence(
        nested_name,
        "U001474",
        fields=list(nested["values"]),
        claim=(
            "U001474 gives both black/white productions and the one-black-element seed for the nested "
            "rule-184 initial condition; it does not choose a finite substitution depth."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    # U001473/A001002 is native rule-184 transition evidence, not substitution
    # seed evidence.
    rule184_name = "elementary cellular automaton rule 184"
    rule184 = candidate(rule184_name)
    rule184["mechanics_units"] = []
    rule184["values"] = {
        "object_kind": "one-dimensional binary nearest-neighbor cellular-automaton preset",
        "carrier": "a one-dimensional row of cells",
        "alphabet_or_value_schema": "black and white",
        "read_dependencies_or_neighborhood": "the left neighbor, cell itself, and right neighbor",
        "law_kind": "deterministic local transition table",
        "rule_relation_constraint_function_or_probability_law": "elementary cellular-automaton rule 184",
        "write_replacement_assembly_or_commit": "write the table-selected next color for each cell",
        "result_kind": "one next binary configuration",
        "successor_cardinality": "one table-selected output for each neighborhood",
        "determinism_branching_or_measure": "deterministic",
        "parameters_and_variants": "rule 184",
    }
    evidence(
        rule184_name,
        "U001465",
        fields=["object_kind", "carrier", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
        claim=(
            "U001465 identifies rule 184 as a cellular automaton over cell blocks; the self-emulation "
            "relation is recorded separately and does not supply its native transition table."
        ),
        strength="DIRECT_IDENTITY",
    )
    evidence(
        rule184_name,
        "U001473",
        fields=[
            "alphabet_or_value_schema",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
        ],
        claim="A001002 is the original-resolution rule-184 transition-table strip and directly supports the scoped native local law.",
        strength="DIRECT_COMPLETE_MECHANICS",
        allow_direct_image=True,
    )

    # The rule-255 native preset and its all-black attractor are distinct.
    rule255_name = "elementary cellular automaton rule 255"
    rule255 = candidate(rule255_name)
    rule255["mechanics_units"] = []
    rule255["values"] = {
        "object_kind": "one-dimensional binary nearest-neighbor cellular-automaton preset",
        "native_time": "discrete successive steps",
        "carrier": "a one-dimensional row of binary cells",
        "alphabet_or_value_schema": "black and white",
        "complete_state": "the color of every cell at one step",
        "read_dependencies_or_neighborhood": "the left neighbor, cell itself, and right neighbor",
        "law_kind": "deterministic local transition law",
        "rule_relation_constraint_function_or_probability_law": "all eight binary nearest-neighbor input triples map to black",
        "write_replacement_assembly_or_commit": "replace every cell by black on the next synchronous step",
        "result_kind": "the all-black successor configuration",
        "successor_cardinality": "one successor for each complete state",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "after one step the native state is all black and remains there",
        "witness_semantics": "the displayed transition table and one-step evolution witness the native preset",
        "parameters_and_variants": "rule 255",
        "evidence_limit": "The transition table is image-borne and was transcribed at original resolution.",
    }
    rule255["uncertainties"] = []
    evidence(
        rule255_name,
        "U001484",
        fields=["native_time", "result_kind", "termination_completion_failure", "witness_semantics"],
        claim="U001484 states that the first class-1 example permits only all-black sequences after one step.",
    )
    evidence(
        rule255_name,
        "U001485",
        fields=[
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "witness_semantics",
            "evidence_limit",
        ],
        claim="A001005's top transition table maps every binary nearest-neighbor triple to black; original-resolution review confirms all eight entries.",
        strength="DIRECT_COMPLETE_MECHANICS",
        allow_direct_image=True,
    )
    evidence(
        rule255_name,
        "U001486",
        fields=["object_kind", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
        claim="U001486 identifies the first displayed native preset as rule 255.",
        strength="DIRECT_IDENTITY",
    )
    attractor255_name = "rule-255 all-black attractor"
    candidate(attractor255_name)["mechanics_units"] = ["U001487"]
    evidence(
        attractor255_name,
        "U001484",
        fields=["rule_relation_constraint_function_or_probability_law", "result_kind", "termination_completion_failure"],
        claim="U001484 states the one-step restriction to all-black sequences.",
    )
    evidence(
        attractor255_name,
        "U001485",
        fields=["witness_semantics"],
        claim="A001005 is the finite native/attractor witness shared with rule 255; the attractor relation itself is stated in prose.",
        strength="CONTEXTUAL",
    )
    evidence(
        attractor255_name,
        "U001486",
        fields=["object_kind", "input", "rule_relation_constraint_function_or_probability_law", "result_kind", "termination_completion_failure"],
        claim="U001486 associates rule 255 with the one-step all-black allowed-sequence result.",
    )

    # The lower A001005 transition table defines native rule 4. Keep its
    # attractor-set restriction and inverse basin relation as distinct objects.
    rule4_name = "elementary cellular automaton rule 4"
    rule4 = candidate(rule4_name)
    rule4["mechanics_units"] = []
    rule4["values"] = {
        "object_kind": "one-dimensional binary nearest-neighbor cellular-automaton preset",
        "native_time": "discrete successive steps",
        "carrier": "a one-dimensional row of binary cells",
        "alphabet_or_value_schema": "black and white",
        "complete_state": "the color of every cell at one step",
        "read_dependencies_or_neighborhood": "the left neighbor, cell itself, and right neighbor",
        "law_kind": "deterministic local transition table",
        "rule_relation_constraint_function_or_probability_law": (
            "write black only for the white-black-white neighborhood; write white for the other seven binary triples"
        ),
        "write_replacement_assembly_or_commit": "write the table-selected next color for each cell",
        "result_kind": "one next binary configuration",
        "successor_cardinality": "one table-selected output for each neighborhood",
        "determinism_branching_or_measure": "deterministic",
        "witness_semantics": "the lower original-resolution table in A001005 transcribes the complete native rule",
        "parameters_and_variants": "rule 4",
    }
    rule4["related_names"] = [
        "rule-4 isolated-black attractor-set constraint",
        "rule-4 many-to-one basin-of-attraction relation",
    ]
    evidence(
        rule4_name,
        "U001485",
        fields=[
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "witness_semantics",
        ],
        claim=(
            "A001005's lower original-resolution transition table maps only white-black-white to black "
            "and maps the other seven binary nearest-neighbor triples to white."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
        allow_direct_image=True,
    )
    evidence(
        rule4_name,
        "U001486",
        fields=[
            "object_kind",
            "native_time",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "parameters_and_variants",
        ],
        claim="U001486 identifies the second displayed preset as rule 4 and states its one-step attractor outcome.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    attractor4_name = "rule-4 isolated-black attractor-set constraint"
    attractor4 = candidate(attractor4_name)
    attractor4["units"] = ["U001485", *attractor4["units"]]
    attractor4["semantic_units"] = ["U001485", *attractor4["semantic_units"]]
    attractor4["anchor_priority"] = 1
    attractor4["mechanics_units"] = []
    attractor4["values"] = {
        "object_kind": "rule-4 attractor-set membership constraint",
        "carrier": "one-dimensional binary configurations",
        "input": "a proposed final rule-4 configuration",
        "law_kind": "declarative configuration-membership constraint",
        "rule_relation_constraint_function_or_probability_law": (
            "accept exactly configurations in which every black cell has at least one white cell on each side"
        ),
        "result_kind": "membership in the rule-4 one-step attractor set",
        "determinism_branching_or_measure": "deterministic membership relation",
        "termination_completion_failure": "membership is decided by checking the stated adjacency restriction",
        "witness_semantics": "an accepted configuration has no adjacent black cells",
        "parameters_and_variants": "rule 4 one-step attractor",
    }
    attractor4["related_names"] = [rule4_name, "rule-4 many-to-one basin-of-attraction relation"]
    evidence(
        attractor4_name,
        "U001485",
        fields=[],
        claim=(
            "A001005 is the finite rule-4 table/evolution witness; the attractor-set constraint "
            "itself is supported directly by U001486 and U001488."
        ),
        strength="CONTEXTUAL",
    )
    evidence(
        attractor4_name,
        "U001486",
        fields=[
            "object_kind",
            "carrier",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "parameters_and_variants",
        ],
        claim="U001486 identifies rule 4's one-step attractor as configurations with every black cell surrounded by white cells.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        attractor4_name,
        "U001488",
        fields=list(attractor4["values"]),
        claim=(
            "U001488 directly defines the complete rule-4 attractor set as all configurations whose black "
            "cells have at least one white cell on both sides."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    basin4_name = "rule-4 many-to-one basin-of-attraction relation"
    basin4 = candidate(basin4_name)
    basin4["mechanics_units"] = []
    basin4["values"] = {
        "object_kind": "rule-4 inverse basin/preimage relation",
        "carrier": "pairs of initial and final binary configurations",
        "input": "a selected final rule-4 attractor configuration",
        "law_kind": "inverse-image relation under deterministic rule-4 evolution",
        "rule_relation_constraint_function_or_probability_law": (
            "collect all initial configurations that evolve to the selected final attractor state"
        ),
        "result_kind": "the basin or preimage set for that final configuration",
        "successor_cardinality": "many initial configurations may share one final state",
        "determinism_branching_or_measure": (
            "the forward rule is deterministic; the inverse basin relation can have many members"
        ),
        "termination_completion_failure": "a proposed initial/final pair is checked by rule-4 evolution",
        "witness_semantics": "the source exhibits four distinct initial conditions with the same final state",
        "parameters_and_variants": "rule 4 and the selected final attractor configuration",
    }
    basin4["related_names"] = [rule4_name, attractor4_name]
    evidence(
        basin4_name,
        "U001489",
        fields=[
            "object_kind",
            "carrier",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "successor_cardinality",
            "determinism_branching_or_measure",
        ],
        claim="U001489 directly states that many different initial configurations can lead to one selected attractor configuration.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        basin4_name,
        "U001490",
        fields=["witness_semantics"],
        claim="A001006 is the finite four-input/one-output basin witness; the basin relation is stated in prose.",
        strength="CONTEXTUAL",
    )
    evidence(
        basin4_name,
        "U001491",
        fields=list(basin4["values"]),
        claim=(
            "U001491 identifies four distinct rule-4 initial conditions that share one final state and names "
            "those initial conditions as elements of its basin of attraction."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    panel4_name = "fixed-or-periodic-structure elementary cellular-automaton preset panel"
    evidence(
        panel4_name,
        "U001485",
        fields=[],
        claim="A001005 concerns later rule-255/rule-4 attractors and supplies no mechanics for panel rules 108, 218, or 232.",
        strength="CONTEXTUAL",
    )
    evidence(
        panel4_name,
        "U001486",
        fields=[],
        claim="U001486 identifies only the rule-4 member's isolated-black attractor behavior; it does not support the whole four-rule panel.",
        strength="CORROBORATING",
    )

    # The unrestricted initial language is a declarative set, not a seed
    # sampler or a time-evolving program.  U001483 states the language before
    # the later network representation is introduced.
    full_binary_name = "full binary configuration language"
    full_binary = candidate(full_binary_name)
    full_binary["units"] = ["U001483", "U001494", "U001498"]
    full_binary["semantic_units"] = ["U001483", "U001494", "U001498"]
    full_binary["mechanics_units"] = []
    full_binary["values"] = {
        "object_kind": "declarative full binary configuration language",
        "carrier": "one-dimensional binary cell sequences",
        "alphabet_or_value_schema": "black and white",
        "complete_state": "one complete black-or-white sequence",
        "law_kind": "declarative sequence-membership constraint",
        "rule_relation_constraint_function_or_probability_law": (
            "allow any number of black and white cells in any order"
        ),
        "result_kind": "the set of all binary cell sequences",
        "determinism_branching_or_measure": (
            "a many-member declarative set; no sampling measure is implied"
        ),
    }
    evidence(
        full_binary_name,
        "U001483",
        fields=list(full_binary["values"]),
        claim=(
            "U001483 directly states that random initial conditions can contain absolutely any "
            "sequence of black and white cells; it defines the unrestricted language, not a probability measure."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        full_binary_name,
        "U001494",
        fields=[
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
        ],
        claim="U001494 restates the step-1 language as all black-and-white sequences before showing its path network.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        full_binary_name,
        "U001498",
        fields=["result_kind"],
        claim="U001498 corroborates that the first network represents all possible binary sequences.",
        strength="CORROBORATING",
    )

    conflict_name = "conflicted adjacent-black constrained initial-condition language"
    conflict = candidate(conflict_name)
    conflict["mechanics_units"] = []
    conflict["values"] = {
        "object_kind": "source-conflicted declarative binary configuration language",
        "carrier": "one-dimensional binary cell sequences",
        "alphabet_or_value_schema": "black and white",
        "complete_state": "one proposed black-or-white initial sequence",
        "law_kind": "declarative sequence-membership constraint",
        "rule_relation_constraint_function_or_probability_law": (
            "CONFLICT: U001513 forbids adjacent black cells, while U001515 says black cells may appear only in pairs"
        ),
        "result_kind": (
            "CONFLICT: the admissible initial-condition language cannot be resolved from this source range"
        ),
        "determinism_branching_or_measure": (
            "declarative membership would be deterministic once the contradictory condition is resolved"
        ),
    }
    evidence(
        conflict_name,
        "U001513",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
        ],
        claim=(
            "U001513 defines a binary initial-condition language forbidding adjacent black cells; "
            "its condition conflicts with U001515."
        ),
        strength="DEFECT_LIMITED",
    )
    evidence(
        conflict_name,
        "U001514",
        fields=[],
        claim="A001011 is the owned network witness but does not resolve the contradictory live captions.",
        strength="CONTEXTUAL",
    )
    evidence(
        conflict_name,
        "U001515",
        fields=[
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
        ],
        claim=(
            "U001515 says black cells are allowed only in pairs, directly contradicting U001513's "
            "adjacent-black prohibition."
        ),
        strength="DEFECT_LIMITED",
    )

    # The allowed-sequence network is an observer with worked path-language
    # examples; later growth panels support outputs only.
    network_name = "allowed-sequence path-network observer"
    network = candidate(network_name)
    network["mechanics_units"] = []
    network["values"] = {
        "object_kind": "finite path-network representation of an allowed binary-sequence language",
        "carrier": "directed path networks and black-or-white cell sequences",
        "input": "a set of allowed black-or-white cell sequences",
        "law_kind": "representation relation; the general construction algorithm is not stated",
        "rule_relation_constraint_function_or_probability_law": (
            "represent each allowed cell sequence by a possible path through the network"
        ),
        "result_kind": "a path network representing the allowed sequence set",
        "witness_semantics": "a permitted path witnesses an allowed cell sequence",
        "structural_invariants": "each permitted cell sequence corresponds to a path through the network",
        "parameters_and_variants": (
            "full binary language, all-black language, isolated-black language, rule-128 shrinking blocks, "
            "and class-3/4 forbidden-block surveys"
        ),
        "excluded_observers_and_representations": (
            "the networks encode reachable sequence languages and are not native cellular-automaton configurations"
        ),
    }
    network["field_units"].update(
        {
            "structural_invariants": ["U001493", "U001494", "U001496", "U001498"],
            "parameters_and_variants": ["U001494", "U001495", "U001496", "U001498", "U001500", "U001503", "U001504", "U001506"],
        }
    )
    network["parameters"] = ["allowed sequence language", "evolution step"]
    network["variants"] = [
        "full binary language network",
        "all-black language network",
        "isolated-black language network",
        "rule-128 shrinking-block network sequence",
        "rule-126 forbidden-block and network-growth survey",
    ]
    network["variant_units"] = {
        "full binary language network": ["U001494"],
        "all-black language network": ["U001495", "U001498"],
        "isolated-black language network": ["U001496", "U001498"],
        "rule-128 shrinking-block network sequence": ["U001500", "U001503"],
        "rule-126 forbidden-block and network-growth survey": ["U001504", "U001506"],
    }
    network_specs = {
        "U001492": (
            ["object_kind", "carrier", "result_kind"],
            "U001492 identifies a compact network representation for allowed one-dimensional binary sequences.",
            "DIRECT_IDENTITY",
        ),
        "U001494": (
            ["input", "rule_relation_constraint_function_or_probability_law", "result_kind", "witness_semantics", "structural_invariants", "parameters_and_variants"],
            "U001494 gives the worked two-loop path language for all black/white sequences.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001495": (
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001495 gives the one-loop all-black path language for rule 255.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001496": (
            ["input", "rule_relation_constraint_function_or_probability_law", "result_kind", "witness_semantics", "structural_invariants", "parameters_and_variants"],
            "U001496 explains the two-node rule-4 path language and its isolated-black constraint.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001498": (
            ["result_kind", "witness_semantics", "structural_invariants", "parameters_and_variants"],
            "U001498 states that paths encode all allowed sequences for rules 255 and 4.",
            "CORROBORATING",
        ),
        "U001500": (
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001500 gives the rule-128 allowed-block condition after t steps, not the generic network algorithm.",
            "CORROBORATING",
        ),
        "U001503": (
            ["result_kind", "witness_semantics", "parameters_and_variants"],
            "U001503 reports at-most-about-t^2 node growth for class-1/2 network outputs.",
            "CORROBORATING",
        ),
        "U001504": (
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001504 supplies rule-126 forbidden-block results and rapid network growth, not the generic construction law.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001506": (
            ["result_kind", "witness_semantics", "parameters_and_variants"],
            "U001506 reports at-least-exponential node growth for class-3/4 network outputs.",
            "CORROBORATING",
        ),
    }
    evidence(
        network_name,
        "U001493",
        fields=[
            "object_kind",
            "carrier",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "witness_semantics",
            "structural_invariants",
            "excluded_observers_and_representations",
        ],
        claim=(
            "U001493 states the representation relation—each allowed binary sequence corresponds to a "
            "network path—but does not give the general network-construction algorithm."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id, (fields, claim, strength) in network_specs.items():
        evidence(network_name, unit_id, fields=fields, claim=claim, strength=strength)
    for unit_id in ["U001497", "U001499", "U001501", "U001502", "U001505"]:
        evidence(
            network_name,
            unit_id,
            fields=[],
            claim=f"{unit_id} is a finite network/result witness and supplies no generic network-construction mechanics.",
            strength="CONTEXTUAL",
        )

    surjective_name = "surjective binary cellular-automaton mapping family"
    surjective = candidate(surjective_name)
    surjective["variants"] = ["rule 204", "rule 240", "rule 30", "rule 90"]
    surjective["variant_units"] = {variant: ["U001511", "U001512"] for variant in surjective["variants"]}
    surjective["values"]["parameters_and_variants"] = "surjective examples rules 204, 240, 30, and 90"
    surjective["field_units"]["parameters_and_variants"] = ["U001511", "U001512"]
    evidence(
        surjective_name,
        "U001511",
        fields=["parameters_and_variants"],
        claim="A001010 preserves the original-resolution surjective-example inventory: rules 204, 240, 30, and 90.",
        strength="CONTEXTUAL",
    )

    # Native class-4 codes explicitly exclude their enumeration/result panels.
    native_search_records = {
        "two-color next-nearest-neighbor cellular automaton code 20": {
            "mechanics": "U001526",
            "excluded_units": ["U001532", "U001533", "U001535", "U001536", "U001539", "U001540"],
            "excluded": "integer-coded enumeration panels and persistent-structure catalogs are observer/search results, not code-20 transition-law evidence",
        },
        "three-color nearest-neighbor cellular automaton code 357": {
            "mechanics": "U001528",
            "excluded_units": ["U001542", "U001543", "U001544", "U001545", "U001546"],
            "excluded": "base-3 enumeration and persistent-structure panels are observer/search results, not code-357 transition-law evidence",
        },
        "three-color nearest-neighbor cellular automaton code 1329": {
            "mechanics": "U001530",
            "excluded_units": ["U001548", "U001549", "U001550", "U001551", "U001552", "U001553", "U001554", "U001555", "U001556"],
            "excluded": "persistent-structure and unbounded-growth panels are observer/search results, not code-1329 transition-law evidence",
        },
    }
    for name, spec in native_search_records.items():
        row = candidate(name)
        row["mechanics_units"] = [spec["mechanics"]]
        row["values"]["excluded_observers_and_representations"] = spec["excluded"]
        row["field_units"]["excluded_observers_and_representations"] = spec["excluded_units"]
        for unit_id in spec["excluded_units"]:
            if unit_id in row["units"]:
                evidence(
                    name,
                    unit_id,
                    fields=["excluded_observers_and_representations"],
                    claim=f"{unit_id} is a search/result witness explicitly excluded from {name}'s native-law mechanics.",
                    strength=(
                        "CONTEXTUAL"
                        if unit_id
                        in {
                            "U001532",
                            "U001535",
                            "U001543",
                            "U001549",
                            "U001552",
                            "U001555",
                        }
                        else "DIRECT_PARTIAL_MECHANICS"
                    ),
                )

    brute_name = "persistent-structure exhaustive search query"
    brute = candidate(brute_name)
    brute["mechanics_units"] = []
    brute_specs = {
        "U001519": (
            [
                "object_kind",
                "native_time",
                "carrier",
                "complete_state",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "determinism_branching_or_measure",
                "termination_completion_failure",
                "witness_semantics",
                "evidence_limit",
            ],
            "U001519 defines the brute-force method: try possible initial conditions in turn, evolve each, and test for a new persistent structure.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001532": (
            ["witness_semantics"],
            "A001015 is a finite first-200-initial-condition result panel, not the enumeration algorithm.",
            "CONTEXTUAL",
        ),
        "U001533": (
            ["input", "rule_relation_constraint_function_or_probability_law", "result_kind", "witness_semantics"],
            "U001533 states the finite region bound, base-2 numbering, and per-input persistence outcomes.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001534": (
            ["input", "rule_relation_constraint_function_or_probability_law", "result_kind", "termination_completion_failure", "witness_semantics"],
            "U001534 reports a finite prefix of 25 billion tested inputs and explicitly does not claim completeness.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001535": (
            ["witness_semantics"],
            "A001016 is the finite persistent-structure result catalog from the brute-force prefix.",
            "CONTEXTUAL",
        ),
        "U001536": (
            ["input", "result_kind", "witness_semantics"],
            "U001536 labels the first-25-billion result catalog and its base-2 seed numbers.",
            "CORROBORATING",
        ),
    }
    for unit_id, (fields, claim, strength) in brute_specs.items():
        evidence(brute_name, unit_id, fields=fields, claim=claim, strength=strength)

    codec_name = "localized finite-seed integer codec family"
    codec = candidate(codec_name)
    codec["mechanics_units"] = []
    codec["values"]["support"] = "a finite localized digit block; U001533 explicitly bounds one binary survey to regions smaller than nine cells"
    codec["values"]["external_data"] = "the assigned nonnegative integer whose positional digits encode the seed"
    codec_specs = {
        "U001533": (
            [
                "object_kind",
                "native_time",
                "carrier",
                "support",
                "alphabet_or_value_schema",
                "complete_state",
                "input",
                "external_data",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "termination_completion_failure",
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            ],
            "U001533 defines the base-2 integer-digit encoding of binary initial blocks smaller than nine cells.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001536": (
            ["input", "external_data", "rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
            "U001536 corroborates that listed base-2 digit sequences correspond to the binary initial conditions.",
            "CORROBORATING",
        ),
        "U001544": (
            [
                "alphabet_or_value_schema",
                "input",
                "external_data",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
            "U001544 defines the three-color base-3 integer-digit variant used for code-357 initial conditions.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
    }
    for unit_id, (fields, claim, strength) in codec_specs.items():
        evidence(codec_name, unit_id, fields=fields, claim=claim, strength=strength)

    solver_name = "systematic fixed-period persistent-structure constraint solver"
    solver = candidate(solver_name)
    solver["mechanics_units"] = []
    solver_specs = {
        "U001537": (
            [
                "object_kind",
                "native_time",
                "carrier",
                "complete_state",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "determinism_branching_or_measure",
                "termination_completion_failure",
                "witness_semantics",
                "evidence_limit",
            ],
            "U001537 states the completeness contract: a systematic procedure finds absolutely all structures for a given small period.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
        "U001538": (
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001538 reports period-through-15 results and minimum-width facts, not the missing constraint algorithm.",
            "CORROBORATING",
        ),
        "U001539": (
            ["result_kind", "witness_semantics", "parameters_and_variants"],
            "A001017 is the original-resolution labeled catalog of systematic period-bounded results.",
            "CONTEXTUAL",
        ),
        "U001540": (
            [
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "termination_completion_failure",
                "witness_semantics",
                "parameters_and_variants",
            ],
            "U001540 states that all code-20 structures through period 15 were found by a constraint method routed to page 268.",
            "DIRECT_PARTIAL_MECHANICS",
        ),
    }
    for unit_id, (fields, claim, strength) in solver_specs.items():
        evidence(solver_name, unit_id, fields=fields, claim=claim, strength=strength)

    # Rule 110: periodic backgrounds, catalogs, growth, and collisions remain
    # seed/observer witnesses rather than native transition-law evidence.
    rule110_name = "elementary cellular automaton rule 110"
    rule110 = candidate(rule110_name)
    rule110["units"].extend(["U001563", "U001564"])
    rule110["mechanics_units"] = ["U001560"]
    rule110["values"]["excluded_observers_and_representations"] = (
        "the 14-cell periodic background is a seed/environment; persistent-structure catalogs, growth panels, "
        "and collision diagrams are observer/experiment outputs rather than rule-110 transition-law evidence"
    )
    rule110["field_units"]["excluded_observers_and_representations"] = [
        "U001558",
        "U001561",
        "U001562",
        "U001563",
        "U001564",
        "U001568",
        "U001570",
        "U001572",
        "U001574",
        "U001576",
    ]
    rule110["related_names"] = ["periodic-block cellular-automaton initial-condition generator"]
    rule110_specs = {
        "U001558": (
            ["excluded_observers_and_representations"],
            "U001558 gives the random seed context and the 14-cell/7-step periodic background; it supplies no native transition entries.",
        ),
        "U001561": (
            ["excluded_observers_and_representations"],
            "U001561 states that rule-110 structures are disruptions in a regular 14-cell/7-step background.",
        ),
        "U001562": (
            ["excluded_observers_and_representations"],
            "U001562 introduces a bounded seed search and persistent-structure catalog as observer evidence.",
        ),
        "U001563": (
            ["excluded_observers_and_representations"],
            "U001563 routes a width-41 unbounded-growth search result and is not native-law evidence.",
        ),
        "U001564": (
            ["excluded_observers_and_representations"],
            "U001564 routes rule-110 collision experiments and is not native-law evidence.",
        ),
        "U001568": (
            ["excluded_observers_and_representations"],
            "U001568 labels a persistent-structure catalog and extension variants.",
        ),
        "U001570": (
            ["excluded_observers_and_representations"],
            "U001570 records the length-41 seed and measured 77-step growth cycle, displacement, and separations.",
        ),
        "U001572": (
            ["excluded_observers_and_representations"],
            "U001572 records spacing variants in collisions between catalog structures o and j.",
        ),
        "U001574": (
            ["excluded_observers_and_representations"],
            "U001574 records a collision between catalog structures e and o.",
        ),
        "U001576": (
            ["excluded_observers_and_representations"],
            "U001576 records a greater-than-4000-step collision outcome producing eight structures.",
        ),
    }
    for unit_id, (fields, claim) in rule110_specs.items():
        evidence(
            rule110_name,
            unit_id,
            fields=fields,
            claim=claim,
            strength="DIRECT_PARTIAL_MECHANICS",
        )
    for unit_id in ["U001557", "U001567", "U001569", "U001571", "U001573", "U001575"]:
        evidence(
            rule110_name,
            unit_id,
            fields=[],
            claim=f"{unit_id} is a rule-110 background, catalog, growth, or collision image and is not native-law evidence.",
            strength="CONTEXTUAL",
        )

    # Code-only presets remain candidate identities, but absent transition
    # tables are left unknown instead of being reconstructed from generic CA
    # boilerplate.
    def narrow_code_identity(
        name: str,
        *,
        code: str,
        mechanics_unit: str,
        extra_values: dict[str, str] | None = None,
        extra_fields: list[str] | None = None,
        claim: str | None = None,
        image_mechanics: bool = False,
    ) -> None:
        row = candidate(name)
        row["mechanics_units"] = []
        row["values"] = {
            "object_kind": "source-identified cellular-automaton preset",
            "rule_relation_constraint_function_or_probability_law": code,
            "parameters_and_variants": code,
        }
        if extra_values:
            row["values"].update(extra_values)
        fields = [
            "object_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        ] + (extra_fields or [])
        evidence(
            name,
            mechanics_unit,
            fields=fields,
            claim=claim
            or f"{mechanics_unit} identifies {code} and provides a finite behavior witness; no unstated transition entries are inferred.",
            strength=(
                "DIRECT_PARTIAL_MECHANICS"
                if extra_fields
                else "DIRECT_IDENTITY"
            ),
            allow_direct_image=image_mechanics,
        )

    narrow_code_identity(
        "elementary cellular automaton rule 126",
        code="rule 126",
        mechanics_unit="U001244",
        claim="U001244 identifies the displayed cellular automaton as rule 126 and describes its nonsettling behavior.",
    )
    narrow_code_identity(
        "elementary cellular automaton rule 22",
        code="rule 22",
        mechanics_unit="U001245",
        image_mechanics=True,
    )
    narrow_code_identity(
        "elementary cellular automaton rule 30",
        code="rule 30",
        mechanics_unit="U001246",
        image_mechanics=True,
    )
    narrow_code_identity(
        "elementary cellular automaton rule 150",
        code="rule 150",
        mechanics_unit="U001247",
        image_mechanics=True,
    )
    narrow_code_identity(
        "elementary cellular automaton rule 182",
        code="rule 182",
        mechanics_unit="U001248",
        image_mechanics=True,
    )
    narrow_code_identity(
        "elementary cellular automaton rule 90",
        code="rule 90",
        mechanics_unit="U001250",
        image_mechanics=True,
    )
    narrow_code_identity(
        "elementary cellular automaton rule 105",
        code="rule 105",
        mechanics_unit="U001250",
        image_mechanics=True,
    )
    narrow_code_identity(
        "next-nearest cellular automaton rule 4067213884",
        code="rule 4067213884",
        mechanics_unit="U001480",
        extra_values={
            "alphabet_or_value_schema": "black and white cells",
            "read_dependencies_or_neighborhood": "nearest and next-nearest neighbors",
        },
        extra_fields=["alphabet_or_value_schema", "read_dependencies_or_neighborhood"],
        claim="U001480 identifies rule 4067213884, its black/white evolution witness, and its nearest-plus-next-nearest dependency range.",
    )
    narrow_code_identity(
        "elementary cellular automaton rule 45 on a finite cycle",
        code="rule 45 on a finite cyclic row",
        mechanics_unit="U001388",
        extra_values={
            "support": "n cells",
            "boundary": "cyclic",
            "excluded_observers_and_representations": (
                "the rule-45 period curve is an observer result and does not define the transition table"
            ),
        },
        extra_fields=["support", "boundary"],
        claim="U001388 identifies rule 45 as the elementary finite-cycle example whose periods remain near 2^n.",
    )
    rule45 = candidate("elementary cellular automaton rule 45 on a finite cycle")
    rule45["field_units"]["excluded_observers_and_representations"] = ["U001393"]
    evidence(
        "elementary cellular automaton rule 45 on a finite cycle",
        "U001393",
        fields=["excluded_observers_and_representations"],
        claim="U001393 reports an observer period curve and is not rule-45 transition-table evidence.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    # Native identities with directly stated carrier/alphabet/neighborhood.
    narrow_code_identity(
        "two-color next-nearest-neighbor cellular automaton code 20",
        code="code 20",
        mechanics_unit="U001526",
        extra_values={
            "alphabet_or_value_schema": "two cell colors",
            "read_dependencies_or_neighborhood": "nearest and next-nearest neighbors",
            "excluded_observers_and_representations": native_search_records[
                "two-color next-nearest-neighbor cellular automaton code 20"
            ]["excluded"],
        },
        extra_fields=["alphabet_or_value_schema", "read_dependencies_or_neighborhood"],
        claim="U001526 identifies code 20 as a two-color nearest-and-next-nearest-neighbor cellular automaton.",
    )
    narrow_code_identity(
        "three-color nearest-neighbor cellular automaton code 357",
        code="code 357",
        mechanics_unit="U001528",
        extra_values={
            "alphabet_or_value_schema": "three cell colors",
            "read_dependencies_or_neighborhood": "nearest neighbors",
            "excluded_observers_and_representations": native_search_records[
                "three-color nearest-neighbor cellular automaton code 357"
            ]["excluded"],
        },
        extra_fields=["alphabet_or_value_schema", "read_dependencies_or_neighborhood"],
        claim="U001528 identifies code 357 as a three-color nearest-neighbor cellular automaton.",
    )
    narrow_code_identity(
        "three-color nearest-neighbor cellular automaton code 1329",
        code="code 1329",
        mechanics_unit="U001530",
        extra_values={
            "alphabet_or_value_schema": "three cell colors",
            "read_dependencies_or_neighborhood": "nearest neighbors",
            "excluded_observers_and_representations": native_search_records[
                "three-color nearest-neighbor cellular automaton code 1329"
            ]["excluded"],
        },
        extra_fields=["alphabet_or_value_schema", "read_dependencies_or_neighborhood"],
        claim="U001530 identifies code 1329 as a three-color nearest-neighbor cellular automaton.",
    )
    for name, spec in native_search_records.items():
        row = candidate(name)
        row["field_units"]["excluded_observers_and_representations"] = spec["excluded_units"]

    # Rule 110 has directly stated two-color/nearest-neighbor scope, but its
    # code table remains outside the reviewed range.
    rule110["values"] = {
        "object_kind": "one-dimensional cellular-automaton preset",
        "carrier": "one-dimensional array of cells",
        "alphabet_or_value_schema": "two colors of cells",
        "read_dependencies_or_neighborhood": "nearest neighbors in one dimension",
        "law_kind": "simple nearest-neighbor cellular-automaton rule",
        "rule_relation_constraint_function_or_probability_law": (
            "rule 110; the complete transition table is outside this reviewed range"
        ),
        "parameters_and_variants": "rule 110",
        "excluded_observers_and_representations": (
            "the 14-cell periodic background is a seed/environment; persistent-structure catalogs, growth panels, "
            "and collision diagrams are observer/experiment outputs rather than rule-110 transition-law evidence"
        ),
    }
    rule110["mechanics_units"] = []
    rule110["parameters"] = ["rule code"]
    rule110["variants"] = [
        "random-initial-condition evolution",
        "14-cell/7-step periodic-background evolution",
        "bounded persistent-structure catalog",
        "width-41 unbounded-growth experiment",
        "persistent-structure collision experiments",
    ]
    rule110["variant_units"] = {
        "random-initial-condition evolution": ["U001254", "U001256", "U001558"],
        "14-cell/7-step periodic-background evolution": ["U001558", "U001561"],
        "bounded persistent-structure catalog": ["U001562", "U001568"],
        "width-41 unbounded-growth experiment": ["U001563", "U001570"],
        "persistent-structure collision experiments": [
            "U001564",
            "U001572",
            "U001574",
            "U001576",
        ],
    }
    rule110["related_names"] = [
        "periodic-block cellular-automaton initial-condition generator",
        "single-cell initial-perturbation difference observer",
    ]
    evidence(
        rule110_name,
        "U001560",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        ],
        claim=(
            "U001560 identifies rule 110 as a simple cellular-automaton rule involving nearest neighbors "
            "and two cell colors; it does not transcribe the transition table or generic update mechanics."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    # Rule 128 is identified here through a global shrinkage property; the
    # native local transition table is not transcribed in this range.
    rule128_name = "elementary cellular automaton rule 128"
    rule128 = candidate(rule128_name)
    rule128["mechanics_units"] = []
    rule128["values"] = {
        "object_kind": "source-identified elementary cellular-automaton preset",
        "native_time": "successive evolution steps",
        "carrier": "one-dimensional black-or-white cell sequences",
        "alphabet_or_value_schema": "black and white",
        "law_kind": "code-identified cellular-automaton rule with an untranscribed local table",
        "rule_relation_constraint_function_or_probability_law": (
            "rule 128; regions of black shrink by one cell on each side at each step"
        ),
        "result_kind": "progressive evolution toward a class-1 or class-2 final state",
        "structural_invariants": (
            "a black region surviving after t steps has at least t white cells on either side"
        ),
        "parameters_and_variants": "rule 128",
        "excluded_observers_and_representations": (
            "the path networks are derived allowed-sequence observers, not native cellular-automaton states"
        ),
    }
    rule128["uncertainties"] = [
        "The range identifies rule 128 and its black-region shrinkage property but does not transcribe the local transition table."
    ]
    evidence(
        rule128_name,
        "U001499",
        fields=["native_time", "result_kind"],
        claim=(
            "U001499 supplies the successive-step class-1/class-2 outcome context but does not identify "
            "rule 128 or its transition table."
        ),
        strength="CORROBORATING",
    )
    evidence(
        rule128_name,
        "U001500",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "alphabet_or_value_schema",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "structural_invariants",
            "parameters_and_variants",
        ],
        claim=(
            "U001500 identifies rule 128 and states its one-cell-per-side black-region shrinkage and "
            "the resulting t-cell white-separation condition; it does not give the local table."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        rule128_name,
        "U001501",
        fields=["excluded_observers_and_representations"],
        claim="U001501 identifies the successive networks as derived summaries of allowed sequences.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        rule128_name,
        "U001502",
        fields=[],
        claim="A001008 is a finite allowed-sequence-network witness, not rule-128 native-law evidence.",
        strength="CONTEXTUAL",
    )
    evidence(
        rule128_name,
        "U001503",
        fields=["excluded_observers_and_representations"],
        claim="U001503 describes the network observer outputs and their growth, not a native transition table.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    # Evolution/parameter images for continuous rules are witnesses only.
    for unit_id in ["U001315", "U001317", "U001319"]:
        evidence(
            continuous_name,
            unit_id,
            fields=[],
            claim=f"{unit_id} is a finite continuous-CA evolution witness, not an independent statement of the update law.",
            strength="CONTEXTUAL",
        )
    evidence(
        continuous_name,
        "U001318",
        fields=["parameters_and_variants"],
        claim="U001318 supplies only the displayed additive constant 0.398.",
        strength="DIRECT_IDENTITY",
    )
    evidence(
        continuous_name,
        "U001320",
        fields=["parameters_and_variants"],
        claim="U001320 supplies only the displayed additive constant 0.4.",
        strength="DIRECT_IDENTITY",
    )

    # Survey panels are represented by their captioned inventory/outcome, not
    # as one complete transition table.
    rule254_name = "elementary cellular automaton rule 254"
    rule254 = candidate(rule254_name)
    rule254["values"] = {
        "object_kind": "one-dimensional binary cellular-automaton preset",
        "native_time": "successive evolution steps",
        "carrier": "a row of cells",
        "alphabet_or_value_schema": "black and white",
        "seed": "a typical random initial condition",
        "read_dependencies_or_neighborhood": "the two adjacent neighbors",
        "law_kind": "local cellular-automaton transition rule",
        "rule_relation_constraint_function_or_probability_law": (
            "a cell becomes black if either adjacent neighbor is black"
        ),
        "write_replacement_assembly_or_commit": "set the cell's next color from the two neighboring colors",
        "result_kind": "the next row and its successive evolution",
        "determinism_branching_or_measure": "deterministic once the initial condition is fixed",
        "parameters_and_variants": "rule 254",
    }
    rule254["mechanics_units"] = []
    evidence(
        rule254_name,
        "U001229",
        fields=list(rule254["values"]),
        claim=(
            "U001229 defines the rule-254 example from a random initial condition: at each step a cell "
            "becomes black when either adjacent neighbor is black."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    panel_specs = {
        "uniform-attractor elementary cellular-automaton preset panel": {
            "codes": "rules 0, 32, 160, and 250",
            "result": "evolution from random initial conditions to completely uniform states",
            "unit": "U001236",
        },
        panel4_name: {
            "codes": "rules 4, 108, 218, and 232",
            "result": (
                "evolution from random initial conditions to rule-specific fixed or periodic simple structures"
            ),
            "unit": "U001240",
        },
    }
    for name, spec in panel_specs.items():
        row = candidate(name)
        row["values"] = {
            "object_kind": "source-delimited four-preset elementary cellular-automaton panel",
            "carrier": "one-dimensional binary cellular-automaton configurations",
            "alphabet_or_value_schema": "black and white",
            "seed": "random initial conditions",
            "law_kind": "four code-identified cellular-automaton presets",
            "rule_relation_constraint_function_or_probability_law": spec["codes"],
            "result_kind": spec["result"],
            "witness_semantics": "the displayed evolutions witness the panel's stated outcome class",
            "parameters_and_variants": spec["codes"],
        }
        row["mechanics_units"] = []
        evidence(
            name,
            spec["unit"],
            fields=list(row["values"]),
            claim=(
                f"{spec['unit']} delimits {spec['codes']} and states their shared outcome from random "
                "initial conditions; it does not transcribe any member's transition table."
            ),
            strength="DIRECT_PARTIAL_MECHANICS",
        )

    # Expose the source-level knobs separately from prose summaries of fixed
    # presets.  These names describe only choices actually delimited by this
    # range; unresolved conventions remain in uncertainties.
    parameter_specs = {
        "uniform-attractor elementary cellular-automaton preset panel": [
            "selected panel rule code"
        ],
        "fixed-or-periodic-structure elementary cellular-automaton preset panel": [
            "selected panel rule code"
        ],
        "four-class cellular-automaton behavior classification": [
            "observed long-run behavior"
        ],
        "rule-4 many-to-one basin-of-attraction relation": [
            "selected final attractor configuration"
        ],
        "surjective binary cellular-automaton mapping family": [
            "selected cellular-automaton rule"
        ],
        "persistent-structure exhaustive search query": [
            "cellular-automaton rule",
            "initial-region bound or enumeration prefix",
        ],
        "localized finite-seed integer codec family": [
            "radix",
            "cell alphabet",
            "nonnegative integer",
        ],
        "systematic fixed-period persistent-structure constraint solver": [
            "cellular-automaton rule",
            "requested repetition period",
        ],
    }
    for name, parameters in parameter_specs.items():
        candidate(name)["parameters"] = parameters

    # Exact-hash audit repair.  Reset the affected records after all earlier
    # incremental repairs so stale generic-template fields and evidence joins
    # cannot survive into the final proposal.
    def reset_record(
        name: str,
        *,
        values: dict[str, str],
        semantic_units: list[str],
        parameters: list[str] | None = None,
        variants: list[str] | None = None,
        variant_units: dict[str, list[str]] | None = None,
        related_names: list[str] | None = None,
        related_evidence_units: dict[str, list[str]] | None = None,
        na_fields: list[str] | None = None,
        uncertainties: list[str] | None = None,
        role: str | None = None,
    ) -> dict[str, Any]:
        row = candidate(name)
        row["values"] = values
        row["semantic_units"] = semantic_units
        row["mechanics_units"] = []
        row["field_units"] = {}
        row["evidence_overrides"] = {}
        row["parameters"] = parameters or []
        row["variants"] = variants or []
        row["variant_units"] = variant_units or {}
        row["related_names"] = related_names or []
        row["related_evidence_units"] = related_evidence_units or {}
        row["na_fields"] = na_fields or []
        row["uncertainties"] = uncertainties or []
        if role is not None:
            row["role"] = role
        return row

    def binary_native_values(
        code: str,
        table: str,
        *,
        neighborhood: str = "the left neighbor, cell itself, and right neighbor",
    ) -> dict[str, str]:
        return {
            "object_kind": "one-dimensional binary nearest-neighbor cellular-automaton preset",
            "native_time": "successive discrete cellular-automaton steps",
            "carrier": "a one-dimensional row of cells",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one black-or-white value for every cell in the row",
            "frontier_or_activation": "every cell on each step",
            "schedule": "synchronous cellular-automaton update",
            "read_dependencies_or_neighborhood": neighborhood,
            "law_kind": "deterministic local transition table",
            "rule_relation_constraint_function_or_probability_law": table,
            "write_replacement_assembly_or_commit": (
                "write the table-selected next color at each cell and commit all cell writes simultaneously"
            ),
            "result_kind": "one next binary configuration",
            "successor_cardinality": "exactly one successor configuration",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": code,
        }

    native_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "alphabet_or_value_schema",
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
        "parameters_and_variants",
    ]

    rule254_name = "elementary cellular automaton rule 254"
    rule254 = reset_record(
        rule254_name,
        values=binary_native_values(
            "rule 254",
            (
                "for neighborhoods BBB, BBW, BWB, BWW, WBB, WBW, WWB, WWW respectively, "
                "the outputs are B, B, B, B, B, B, B, W"
            ),
            neighborhood=(
                "the left neighbor, cell itself, and right neighbor; the exact table is black "
                "unless all three cells are white"
            ),
        ),
        semantic_units=["U001229", "U001231", "U001233"],
        related_names=["random cellular-automaton initial-field generator family"],
        related_evidence_units={
            "random cellular-automaton initial-field generator family": [
                "U001229",
                "U001233",
            ]
        },
        na_fields=["seed"],
    )
    rule254["values"]["witness_semantics"] = (
        "the random-initial-condition evolution is a behavior witness, not an intrinsic seed of rule 254"
    )
    evidence(
        rule254_name,
        "U001229",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "witness_semantics",
        ],
        claim=(
            "U001229 states the stepwise rule-254 example and the sufficient neighbor condition for "
            "black output; A000924 supplies the complete three-cell table."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        rule254_name,
        "U001231",
        fields=[
            field
            for field in native_fields
            if field != "parameters_and_variants"
        ],
        claim=(
            "A000924 was checked at original resolution: in BBB, BBW, BWB, BWW, WBB, WBW, "
            "WWB, WWW order, rule 254 outputs B,B,B,B,B,B,B,W."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
        allow_direct_image=True,
    )
    evidence(
        rule254_name,
        "U001232",
        fields=["witness_semantics"],
        claim="A000925 is the random-start evolution witness and does not define rule 254's seed.",
        strength="CONTEXTUAL",
    )
    evidence(
        rule254_name,
        "U001233",
        fields=["object_kind", "parameters_and_variants", "witness_semantics"],
        claim="U001233 identifies the displayed preset as rule 254 and labels the random-start outcome.",
        strength="DIRECT_IDENTITY",
    )

    panel_table_specs = {
        "uniform-attractor elementary cellular-automaton preset panel": {
            "unit_image": "U001235",
            "unit_caption": "U001236",
            "codes": ["rule 0", "rule 32", "rule 160", "rule 250"],
            "law": (
                "selected code to table mapping in BBB, BBW, BWB, BWW, WBB, WBW, WWB, WWW order: "
                "rule 0 -> W,W,W,W,W,W,W,W; "
                "rule 32 -> W,W,B,W,W,W,W,W; "
                "rule 160 -> B,W,B,W,W,W,W,W; "
                "rule 250 -> B,B,B,B,B,W,B,W"
            ),
            "witness": "the displayed random-start runs evolve to uniform states",
        },
        "fixed-or-periodic-structure elementary cellular-automaton preset panel": {
            "unit_image": "U001239",
            "unit_caption": "U001240",
            "codes": ["rule 4", "rule 108", "rule 218", "rule 232"],
            "law": (
                "selected code to table mapping in BBB, BBW, BWB, BWW, WBB, WBW, WWB, WWW order: "
                "rule 4 -> W,W,W,W,W,B,W,W; "
                "rule 108 -> W,B,B,W,B,B,W,W; "
                "rule 218 -> B,B,W,B,B,W,B,W; "
                "rule 232 -> B,B,B,W,B,W,W,W"
            ),
            "witness": (
                "the displayed random-start runs evolve to fixed or periodically repeating simple structures"
            ),
        },
    }
    for name, spec in panel_table_specs.items():
        values = {
            "object_kind": "finite family of four elementary binary cellular-automaton presets",
            "native_time": "successive discrete cellular-automaton steps",
            "carrier": "a one-dimensional row of cells",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one black-or-white value for every cell in the row",
            "frontier_or_activation": "every cell on each step",
            "schedule": "synchronous cellular-automaton update",
            "read_dependencies_or_neighborhood": "the left neighbor, cell itself, and right neighbor",
            "law_kind": "code-selected deterministic local transition table",
            "rule_relation_constraint_function_or_probability_law": spec["law"],
            "write_replacement_assembly_or_commit": (
                "write the selected table's next color at each cell and commit all writes simultaneously"
            ),
            "result_kind": "one next binary configuration under the selected preset",
            "successor_cardinality": "exactly one successor configuration for a selected code",
            "determinism_branching_or_measure": "deterministic after the rule code is selected",
            "witness_semantics": spec["witness"],
            "parameters_and_variants": ", ".join(spec["codes"]),
        }
        row = reset_record(
            name,
            values=values,
            semantic_units=[spec["unit_image"], spec["unit_caption"]],
            parameters=["selected rule code"],
            variants=spec["codes"],
            variant_units={
                code: [spec["unit_image"], spec["unit_caption"]]
                for code in spec["codes"]
            },
            related_names=["random cellular-automaton initial-field generator family"],
            related_evidence_units={
                "random cellular-automaton initial-field generator family": [
                    spec["unit_caption"]
                ]
            },
            na_fields=["seed"],
            role="FAMILY",
        )
        evidence(
            name,
            spec["unit_image"],
            fields=[
                "object_kind",
                "native_time",
                "carrier",
                "alphabet_or_value_schema",
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
                "witness_semantics",
                "parameters_and_variants",
            ],
            claim=(
                f"{spec['unit_image']} was checked at original resolution and transcribed as the four "
                "ordered BBB-through-WWW transition tables; the same panel supplies finite outcome witnesses."
            ),
            strength="DIRECT_COMPLETE_MECHANICS",
            allow_direct_image=True,
        )
        evidence(
            name,
            spec["unit_caption"],
            fields=[
                "object_kind",
                "parameters_and_variants",
                "witness_semantics",
            ],
            claim=(
                f"{spec['unit_caption']} fixes the top-to-bottom rule-code ordering and describes the "
                "random-start outcomes without making random initialization part of the native family."
            ),
            strength="DIRECT_PARTIAL_MECHANICS",
        )

    rule126_name = "elementary cellular automaton rule 126"
    rule126 = reset_record(
        rule126_name,
        values=binary_native_values(
            "rule 126",
            (
                "for neighborhoods BBB, BBW, BWB, BWW, WBB, WBW, WWB, WWW respectively, "
                "the outputs are W, B, B, B, B, B, B, W"
            ),
        ),
        semantic_units=["U001242", "U001243", "U001244"],
        related_names=[
            "random cellular-automaton initial-field generator family",
            "rule-126 random two-block initial-condition ensemble",
            "rule-126 to rule-90 pair-block emulation",
        ],
        related_evidence_units={
            "random cellular-automaton initial-field generator family": ["U001244"],
            "rule-126 random two-block initial-condition ensemble": ["U001439"],
            "rule-126 to rule-90 pair-block emulation": ["U001439"],
        },
        na_fields=["seed"],
    )
    rule126["values"]["witness_semantics"] = (
        "the random-start evolution and special-seed experiments witness behavior but do not define the native seed"
    )
    evidence(
        rule126_name,
        "U001242",
        fields=["witness_semantics"],
        claim="A000928 is a random-start evolution witness, not native transition-table evidence.",
        strength="CONTEXTUAL",
    )
    evidence(
        rule126_name,
        "U001243",
        fields=[
            field
            for field in native_fields
            if field != "parameters_and_variants"
        ],
        claim=(
            "A000929 was checked at original resolution: in BBB, BBW, BWB, BWW, WBB, WBW, "
            "WWB, WWW order, rule 126 outputs W,B,B,B,B,B,B,W."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
        allow_direct_image=True,
    )
    evidence(
        rule126_name,
        "U001244",
        fields=["object_kind", "parameters_and_variants", "witness_semantics"],
        claim="U001244 identifies the displayed preset as rule 126 and describes its random-start behavior.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in ("U001437", "U001438", "U001439"):
        evidence(
            rule126_name,
            unit_id,
            fields=["witness_semantics"] if unit_id == "U001439" else [],
            claim=(
                f"{unit_id} belongs to the separately modeled special two-block seed experiment and "
                "does not supply rule-126 transition entries."
            ),
            strength="CORROBORATING" if unit_id == "U001439" else "CONTEXTUAL",
        )

    rule30_name = "elementary cellular automaton rule 30"
    rule30_row = candidate(rule30_name)
    if "U001435" not in rule30_row["units"]:
        rule30_row["units"].append("U001435")
    rule30 = reset_record(
        rule30_name,
        values={
            **binary_native_values(
                "rule 30",
                (
                    "for neighborhoods BBB, BBW, BWB, BWW, WBB, WBW, WWB, WWW respectively, "
                    "the outputs are W, W, W, B, B, B, B, W"
                ),
            ),
            "structural_invariants": (
                "for rule 30, repetitive behavior can arise only from an initial condition formed by "
                "one fixed finite block repeated forever"
            ),
            "witness_semantics": (
                "random-start, simple-start, and special periodic-start runs are behavior witnesses"
            ),
        },
        semantic_units=["U001246", "U001430", "U001431", "U001435"],
        related_names=[
            "random cellular-automaton initial-field generator family",
            "periodic-block cellular-automaton initial-condition generator",
        ],
        related_evidence_units={
            "random cellular-automaton initial-field generator family": ["U001246"],
            "periodic-block cellular-automaton initial-condition generator": [
                "U001431",
                "U001435",
            ],
        },
        na_fields=["seed"],
    )
    evidence(
        rule30_name,
        "U001246",
        fields=["object_kind", "parameters_and_variants", "witness_semantics"],
        claim="A000933 identifies rule 30 and is a random-start behavior witness, not its native seed.",
        strength="DIRECT_IDENTITY",
        allow_direct_image=True,
    )
    evidence(
        rule30_name,
        "U001430",
        fields=[
            field
            for field in native_fields
            if field != "parameters_and_variants"
        ],
        claim=(
            "A000986 was checked at original resolution: in BBB, BBW, BWB, BWW, WBB, WBW, "
            "WWB, WWW order, rule 30 outputs W,W,W,B,B,B,B,W."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
        allow_direct_image=True,
    )
    evidence(
        rule30_name,
        "U001431",
        fields=["object_kind", "parameters_and_variants", "witness_semantics"],
        claim="U001431 identifies the table strip as rule 30 and the adjacent panels as special periodic-start witnesses.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        rule30_name,
        "U001435",
        fields=["structural_invariants", "witness_semantics"],
        claim=(
            "U001435 directly states that no rule-30 initial condition other than a single fixed block "
            "repeated forever can yield repetitive behavior."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    classifier_name = "four-class cellular-automaton behavior classification"
    classifier = reset_record(
        classifier_name,
        values={
            "object_kind": "qualitative four-class cellular-automaton behavior classifier",
            "carrier": "cellular-automaton space-time evolution histories",
            "visible_history": "the overall long-run appearance and correlated detailed properties of an evolution",
            "input": "an observed cellular-automaton evolution and a chosen reasonable class definition",
            "law_kind": "qualitative behavior classification",
            "rule_relation_constraint_function_or_probability_law": (
                "class 1: almost all initial conditions reach the same uniform final state; "
                "class 2: final behavior consists of simple fixed or short-period structures; "
                "class 3: behavior appears random while retaining small-scale structures; "
                "class 4: localized structures mix order and randomness by moving and interacting; "
                "rare borderline systems may receive different labels under different reasonable definitions"
            ),
            "result_kind": "one class label from 1 through 4, or the stated set of plausible labels for a borderline rule",
            "determinism_branching_or_measure": (
                "normally stable across reasonable definitions, but explicitly definition-dependent for rare borderline cases"
            ),
            "witness_semantics": (
                "ordinary panels exemplify the four classes; the four labeled borderline panels witness the stated alternative assignments"
            ),
            "parameters_and_variants": (
                "chosen reasonable class definition or correlated property; borderline codes 219, 438, 1380, and 1632"
            ),
        },
        semantic_units=[
            "U001264",
            "U001269",
            "U001270",
            "U001271",
            "U001278",
            "U001279",
            "U001280",
            "U001293",
            "U001294",
            "U001295",
            "U001296",
            "U001297",
            "U001298",
        ],
        parameters=["chosen reasonable class definition or correlated property"],
        variants=[
            "class 1",
            "class 2",
            "class 3",
            "class 4",
            "code 219: class 2 or 4",
            "code 438: class 3 or 4",
            "code 1380: class 2 or 3",
            "code 1632: class 1, 2, or 3",
        ],
        variant_units={
            "class 1": ["U001271"],
            "class 2": ["U001278"],
            "class 3": ["U001279"],
            "class 4": ["U001280"],
            "code 219: class 2 or 4": ["U001294", "U001298"],
            "code 438: class 3 or 4": ["U001295", "U001298"],
            "code 1380: class 2 or 3": ["U001296", "U001298"],
            "code 1632: class 1, 2, or 3": ["U001297", "U001298"],
        },
        na_fields=[
            "native_time",
            "complete_state",
            "termination_completion_failure",
        ],
        uncertainties=[
            "The source deliberately leaves the precise class definition selectable and records rare definition-dependent borderline cases."
        ],
    )
    evidence(
        classifier_name,
        "U001264",
        fields=["object_kind", "carrier", "result_kind"],
        claim="U001264 establishes only the four-class scope and the assignment of evolution patterns to four labels.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in ("U001265", "U001266", "U001267", "U001268"):
        evidence(
            classifier_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is one of the four ordinary class-example panels.",
            strength="CONTEXTUAL",
        )
    evidence(
        classifier_name,
        "U001269",
        fields=["witness_semantics"],
        claim="U001269 identifies the four preceding panels as examples of the four basic classes.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        classifier_name,
        "U001270",
        fields=["parameters_and_variants"],
        claim="U001270 fixes the class labels 1 through 4 and orders them by increasing complexity.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id, class_label, definition in [
        (
            "U001271",
            "class 1",
            "almost all initial conditions lead to the same uniform final state",
        ),
        (
            "U001278",
            "class 2",
            "many final states consist of simple structures that remain fixed or repeat every few steps",
        ),
        (
            "U001279",
            "class 3",
            "behavior seems random while triangles and other small-scale structures remain visible",
        ),
        (
            "U001280",
            "class 4",
            "localized structures mix order and randomness by moving and interacting",
        ),
    ]:
        evidence(
            classifier_name,
            unit_id,
            fields=[
                "visible_history",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
            claim=f"{unit_id} directly defines {class_label}: {definition}.",
            strength="DIRECT_COMPLETE_MECHANICS",
        )
    evidence(
        classifier_name,
        "U001293",
        fields=[
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "determinism_branching_or_measure",
            "parameters_and_variants",
        ],
        claim=(
            "U001293 states that detailed properties can furnish more precise definitions and that "
            "reasonable definitions normally agree."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id, code in [
        ("U001294", "219"),
        ("U001295", "438"),
        ("U001296", "1380"),
        ("U001297", "1632"),
    ]:
        evidence(
            classifier_name,
            unit_id,
            fields=["witness_semantics", "parameters_and_variants"],
            claim=f"{unit_id} is the original-resolution borderline panel labeled totalistic code {code}.",
            strength="CONTEXTUAL",
        )
    evidence(
        classifier_name,
        "U001298",
        fields=[
            "input",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim=(
            "U001298 gives the exact alternatives: code 219 class 2/4, 438 class 3/4, "
            "1380 class 2/3, and 1632 class 1/2/3 under different definitions."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    class4_code_specs = {
        "three-color nearest-neighbor totalistic cellular automaton code 1815": (
            "1815",
            ["U001285", "U001286", "U001287"],
            "U001286",
            "U001287",
        ),
        "three-color nearest-neighbor totalistic cellular automaton code 2007": (
            "2007",
            ["U001285", "U001288", "U001289"],
            "U001288",
            "U001289",
        ),
        "three-color nearest-neighbor totalistic cellular automaton code 1659": (
            "1659",
            ["U001285", "U001290"],
            "U001290",
            "U001290",
        ),
        "three-color nearest-neighbor totalistic cellular automaton code 2043": (
            "2043",
            ["U001285", "U001291", "U001292"],
            "U001291",
            "U001292",
        ),
    }
    for name, (code, units, image_unit, identity_unit) in class4_code_specs.items():
        row = candidate(name)
        row["units"] = units
        values = {
            "object_kind": "three-color nearest-neighbor totalistic cellular-automaton preset",
            "native_time": "successive cellular-automaton steps",
            "carrier": "a one-dimensional row of cells",
            "alphabet_or_value_schema": "three cell colors",
            "complete_state": "one three-color value for every cell in the row",
            "frontier_or_activation": "every cell on each step",
            "schedule": "synchronous cellular-automaton update",
            "read_dependencies_or_neighborhood": "the cell and its nearest neighbors, read totalistically",
            "law_kind": "deterministic code-identified totalistic transition table",
            "rule_relation_constraint_function_or_probability_law": (
                f"code {code} under the source's three-color nearest-neighbor totalistic code scheme; "
                "the full table is not transcribed in this range"
            ),
            "write_replacement_assembly_or_commit": (
                "write the code-selected next color at every cell and commit synchronously"
            ),
            "result_kind": "one next three-color configuration",
            "successor_cardinality": "exactly one successor configuration",
            "determinism_branching_or_measure": "deterministic",
            "witness_semantics": (
                "the displayed 1500-step random-start run witnesses class-4 behavior and is not a native seed or parameter"
            ),
            "parameters_and_variants": f"fixed preset code {code}",
        }
        reset_record(
            name,
            values=values,
            semantic_units=["U001285", identity_unit],
            related_names=["random cellular-automaton initial-field generator family"],
            related_evidence_units={
                "random cellular-automaton initial-field generator family": [
                    "U001285",
                    image_unit,
                ]
            },
            na_fields=["seed"],
        )
        evidence(
            name,
            "U001285",
            fields=[
                "object_kind",
                "native_time",
                "carrier",
                "alphabet_or_value_schema",
                "complete_state",
                "frontier_or_activation",
                "schedule",
                "read_dependencies_or_neighborhood",
                "law_kind",
                "write_replacement_assembly_or_commit",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "witness_semantics",
            ],
            claim=(
                "U001285 defines the shared native scope—three colors, nearest-neighbor totalistic "
                "cellular automata—and separately describes the 1500-step random-start witnesses."
            ),
            strength="DIRECT_PARTIAL_MECHANICS",
        )
        if identity_unit == image_unit:
            evidence(
                name,
                image_unit,
                fields=[
                    "rule_relation_constraint_function_or_probability_law",
                    "parameters_and_variants",
                    "witness_semantics",
                ],
                claim=(
                    f"{image_unit} was checked at original resolution: it identifies code {code} and "
                    "supplies its finite random-start evolution witness, not a transition-table transcription."
                ),
                strength="DIRECT_IDENTITY",
                allow_direct_image=True,
            )
        else:
            evidence(
                name,
                image_unit,
                fields=["witness_semantics"],
                claim=f"{image_unit} is the finite 1500-step random-start witness for code {code}.",
                strength="CONTEXTUAL",
            )
            evidence(
                name,
                identity_unit,
                fields=[
                    "rule_relation_constraint_function_or_probability_law",
                    "parameters_and_variants",
                ],
                claim=f"{identity_unit} identifies the fixed native preset as code {code}.",
                strength="DIRECT_IDENTITY",
            )

    rule110_name = "elementary cellular automaton rule 110"
    rule110 = candidate(rule110_name)
    rule110["units"] = [
        "U001254",
        "U001255",
        "U001256",
        "U001257",
        "U001359",
        "U001360",
        "U001361",
        "U001362",
        "U001557",
        "U001558",
        "U001560",
        "U001561",
        "U001564",
        "U001571",
        "U001572",
        "U001573",
        "U001574",
        "U001575",
        "U001576",
    ]
    reset_record(
        rule110_name,
        values={
            "object_kind": "one-dimensional cellular-automaton preset",
            "carrier": "a one-dimensional array of cells",
            "alphabet_or_value_schema": "two cell colors",
            "read_dependencies_or_neighborhood": "nearest neighbors in one dimension",
            "law_kind": "simple nearest-neighbor cellular-automaton rule",
            "rule_relation_constraint_function_or_probability_law": (
                "rule 110; the complete transition table is outside this reviewed range"
            ),
            "witness_semantics": (
                "random-start evolutions, one-cell perturbation comparisons, and collision experiments "
                "witness rule-110 behavior without supplying transition entries"
            ),
            "parameters_and_variants": "fixed rule code 110",
        },
        semantic_units=[
            "U001254",
            "U001256",
            "U001359",
            "U001362",
            "U001558",
            "U001560",
            "U001561",
            "U001564",
            "U001572",
            "U001574",
            "U001576",
        ],
        parameters=["rule code"],
        related_names=[
            "single-cell initial-perturbation difference observer",
            "periodic-block cellular-automaton initial-condition generator",
        ],
        related_evidence_units={
            "single-cell initial-perturbation difference observer": [
                "U001359",
                "U001360",
                "U001361",
                "U001362",
            ],
            "periodic-block cellular-automaton initial-condition generator": [
                "U001557",
                "U001558",
                "U001561",
            ],
        },
        na_fields=["seed"],
        uncertainties=[
            "The reviewed range identifies rule 110's two-color nearest-neighbor scope but does not transcribe its transition table."
        ],
    )
    for unit_id in ("U001255", "U001257", "U001360", "U001361", "U001557"):
        evidence(
            rule110_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a finite rule-110 behavior witness and supplies no transition entries.",
            strength="CONTEXTUAL",
        )
    evidence(
        rule110_name,
        "U001254",
        fields=["witness_semantics"],
        claim="U001254 introduces the random-start localized-structure behavior later identified as rule 110.",
        strength="CORROBORATING",
    )
    evidence(
        rule110_name,
        "U001256",
        fields=[
            "object_kind",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001256 identifies the random-start class-4 evolution as rule 110.",
        strength="DIRECT_IDENTITY",
    )
    for unit_id in ("U001359", "U001362"):
        evidence(
            rule110_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} links rule 110 to the separately modeled one-cell perturbation comparison.",
            strength="CORROBORATING",
        )
    evidence(
        rule110_name,
        "U001558",
        fields=["witness_semantics", "parameters_and_variants"],
        claim=(
            "U001558 identifies rule 110's random-start witness and 14-cell/7-step background; "
            "the background itself belongs to the periodic-seed record."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        rule110_name,
        "U001560",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        ],
        claim=(
            "U001560 identifies rule 110 as a simple one-dimensional nearest-neighbor rule with two "
            "cell colors; no transition entries are inferred."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        rule110_name,
        "U001561",
        fields=["witness_semantics"],
        claim="U001561 links rule-110 structures to disruptions in the separately modeled periodic background.",
        strength="CORROBORATING",
    )
    evidence(
        rule110_name,
        "U001564",
        fields=["witness_semantics"],
        claim="U001564 introduces rule-110 collision experiments as behavior witnesses.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in ("U001571", "U001573", "U001575"):
        evidence(
            rule110_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is an original-resolution rule-110 collision witness.",
            strength="CONTEXTUAL",
        )
    for unit_id in ("U001572", "U001574", "U001576"):
        evidence(
            rule110_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} directly describes a source-delimited rule-110 collision outcome.",
            strength="DIRECT_PARTIAL_MECHANICS",
        )

    random_name = "random cellular-automaton initial-field generator family"
    random_field = reset_record(
        random_name,
        values={
            "object_kind": "carrier- and value-domain-parameterized stochastic initial-field generator",
            "carrier": (
                "the selected cellular automaton's field: a one-dimensional row or two-dimensional grid "
                "in the stated examples"
            ),
            "alphabet_or_value_schema": (
                "the selected cell-value domain: black/white or a continuous gray level in [0,1]"
            ),
            "complete_state": "one complete initial field on the selected carrier",
            "input": (
                "target carrier, target value domain, and binary black-cell density when the source states one"
            ),
            "law_kind": "stochastic initial-field generation law",
            "rule_relation_constraint_function_or_probability_law": (
                "choose field values at random in the selected value domain; binary examples may specify "
                "a black-cell density, while the exact probability measure and independence assumptions remain unstated"
            ),
            "result_kind": "one random initial field for the selected cellular automaton",
            "determinism_branching_or_measure": (
                "stochastic; the source does not fully specify the sampling measure or independence convention"
            ),
            "parameters_and_variants": (
                "target carrier, target value domain, and stated black-cell density"
            ),
        },
        semantic_units=[
            "U001227",
            "U001316",
            "U001324",
            "U001331",
            "U001333",
            "U001416",
            "U001421",
        ],
        parameters=[
            "target carrier",
            "target value domain",
            "stated black-cell density",
        ],
        variants=[
            "one-dimensional random black-or-white field",
            "one-dimensional random continuous gray field",
            "two-dimensional random black-or-white field",
            "low-density random binary field",
        ],
        variant_units={
            "one-dimensional random black-or-white field": ["U001227"],
            "one-dimensional random continuous gray field": ["U001316"],
            "two-dimensional random black-or-white field": [
                "U001324",
                "U001331",
                "U001333",
            ],
            "low-density random binary field": ["U001421"],
        },
        na_fields=[
            "native_time",
            "seed",
            "termination_completion_failure",
        ],
        uncertainties=[
            "Exact probability measures, independence assumptions, spatial extent, and random-bit sources are not stated."
        ],
        role="SEED",
    )
    evidence(
        random_name,
        "U001227",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "parameters_and_variants",
        ],
        claim="U001227 defines the binary random field by choosing every cell black or white at random.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id, claim in [
        (
            "U001316",
            "U001316 supplies the one-dimensional continuous gray-field random-start variant.",
        ),
        (
            "U001324",
            "U001324 directly identifies two-dimensional cellular-automaton random initial fields.",
        ),
        (
            "U001331",
            "U001331 supplies the two-dimensional binary random-field variant.",
        ),
        (
            "U001333",
            "U001333 corroborates the broader two-dimensional random-start survey.",
        ),
        (
            "U001416",
            "U001416 states the infinite random placement required for rule-90 random behavior.",
        ),
        (
            "U001421",
            "U001421 supplies the low-black-density random-field parameter variant.",
        ),
    ]:
        evidence(
            random_name,
            unit_id,
            fields=[
                "carrier",
                "alphabet_or_value_schema",
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
            ],
            claim=claim,
            strength="DIRECT_PARTIAL_MECHANICS",
        )

    continuous_name = "fractional-average continuous cellular automaton"
    continuous = reset_record(
        continuous_name,
        values={
            "object_kind": "one-dimensional continuous cellular automaton",
            "native_time": "successive discrete steps",
            "carrier": "a one-dimensional row of cells",
            "alphabet_or_value_schema": "one gray level in [0,1] per cell",
            "complete_state": "the complete gray-level field at one step",
            "frontier_or_activation": "every cell on each step",
            "schedule": "synchronous cellular-automaton update",
            "read_dependencies_or_neighborhood": "the cell and its two adjacent neighbors",
            "law_kind": "deterministic local fractional-average transition law",
            "rule_relation_constraint_function_or_probability_law": (
                "average the three gray levels, add the selected constant, and keep only the fractional part"
            ),
            "write_replacement_assembly_or_commit": (
                "write the resulting fractional part as each cell's next gray level and commit synchronously"
            ),
            "result_kind": "one next complete gray-level field",
            "successor_cardinality": "exactly one successor field",
            "determinism_branching_or_measure": "deterministic for a selected additive constant",
            "witness_semantics": (
                "the random-start evolutions witness behavior; random initialization is supplied by the separate stochastic generator"
            ),
            "parameters_and_variants": "additive constant in [0,1], including displayed values 0.398 and 0.4",
            "excluded_observers_and_representations": (
                "the page-259 neighbor-difference gray values are observer output, not native cell state"
            ),
        },
        semantic_units=["U001311", "U001316", "U001318", "U001320", "U001323"],
        parameters=["additive constant"],
        related_names=[
            "random cellular-automaton initial-field generator family",
            "neighbor-difference gray-field display transformation",
        ],
        related_evidence_units={
            "random cellular-automaton initial-field generator family": [
                "U001315",
                "U001316",
                "U001317",
                "U001319",
            ],
            "neighbor-difference gray-field display transformation": [
                "U001317",
                "U001319",
                "U001323",
            ],
        },
        na_fields=["seed"],
    )
    evidence(
        continuous_name,
        "U001311",
        fields=["object_kind", "parameters_and_variants"],
        claim="U001311 identifies the continuous-cellular-automaton family and its smoothly varying parameter in [0,1].",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        continuous_name,
        "U001315",
        fields=["witness_semantics"],
        claim="A000953 is a finite random-start evolution witness, not native-law or intrinsic-seed evidence.",
        strength="CONTEXTUAL",
    )
    evidence(
        continuous_name,
        "U001316",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "alphabet_or_value_schema",
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
            "witness_semantics",
        ],
        claim=(
            "U001316 completely states the gray-field update and separately identifies the displayed "
            "run as starting from a random field."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    for unit_id in ("U001317", "U001319"):
        evidence(
            continuous_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a finite parameterized evolution witness rendered by the separate difference observer.",
            strength="CONTEXTUAL",
        )
    evidence(
        continuous_name,
        "U001318",
        fields=["parameters_and_variants"],
        claim="U001318 directly labels the displayed additive constant as 0.398.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        continuous_name,
        "U001320",
        fields=["parameters_and_variants"],
        claim="U001320 directly labels the displayed additive constant as 0.4.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        continuous_name,
        "U001323",
        fields=["excluded_observers_and_representations"],
        claim="U001323 explicitly says all three page-259 pictures display neighbor differences rather than native gray levels.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    difference_name = "neighbor-difference gray-field display transformation"
    difference = candidate(difference_name)
    difference["parameters"] = []
    difference["values"].pop("parameters_and_variants", None)

    life_name = "Game of Life cellular automaton"
    life = reset_record(
        life_name,
        values={
            "object_kind": "two-dimensional binary outer-totalistic cellular automaton",
            "native_time": "successive discrete steps",
            "carrier": "a two-dimensional square grid",
            "topology": "orthogonal and diagonal square-grid adjacency",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one black-or-white value for every grid cell",
            "frontier_or_activation": "every cell on each step",
            "schedule": "synchronous cellular-automaton update",
            "read_dependencies_or_neighborhood": "the eight orthogonal and diagonal neighbors",
            "law_kind": "deterministic outer-totalistic transition table",
            "rule_relation_constraint_function_or_probability_law": (
                "with two black neighbors retain the cell's previous color; with three become black; "
                "with any other count become white"
            ),
            "write_replacement_assembly_or_commit": (
                "write the rule-selected next color at every grid cell and commit synchronously"
            ),
            "result_kind": "one next complete binary grid",
            "successor_cardinality": "exactly one successor grid",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "fixed outer-totalistic 9-neighbor code 224",
            "excluded_observers_and_representations": (
                "one-dimensional slices and prior-time gray trails are observer renderings, not native states"
            ),
        },
        semantic_units=["U001329", "U001341"],
        related_names=[
            "one-dimensional slice-through-time and spatial-depth-fog observer",
            "prior-time gray-trail rendering observer",
        ],
        related_evidence_units={
            "one-dimensional slice-through-time and spatial-depth-fog observer": ["U001329"],
            "prior-time gray-trail rendering observer": [
                "U001336",
                "U001338",
                "U001339",
                "U001340",
                "U001341",
            ],
        },
        na_fields=["seed"],
    )
    evidence(
        life_name,
        "U001329",
        fields=[
            field
            for field in life["values"]
            if field != "excluded_observers_and_representations"
        ],
        claim=(
            "U001329 gives the complete Game of Life update over eight neighbors, identifies code 224, "
            "and thereby determines one successor grid."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    for unit_id in ("U001336", "U001338", "U001339", "U001340"):
        evidence(
            life_name,
            unit_id,
            fields=[],
            claim=f"{unit_id} is observer-rendered Game of Life output and supplies no native transition mechanics.",
            strength="CONTEXTUAL",
        )
    evidence(
        life_name,
        "U001341",
        fields=["excluded_observers_and_representations"],
        claim="U001341 explicitly defines the prior-time gray-trail rendering as a display of preceding black cells.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    family_2d_name = "binary two-dimensional von-Neumann-totalistic cellular-automaton family"
    family_2d = reset_record(
        family_2d_name,
        values={
            "object_kind": "parameterized two-dimensional binary totalistic cellular-automaton family",
            "native_time": "successive discrete steps",
            "carrier": "a two-dimensional square grid",
            "topology": "four-neighbor orthogonal square-grid adjacency",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one black-or-white value for every grid cell",
            "frontier_or_activation": "every cell on each step",
            "schedule": "synchronous cellular-automaton update",
            "read_dependencies_or_neighborhood": "the cell and its four immediate orthogonal neighbors",
            "law_kind": "code-selected deterministic totalistic transition table",
            "rule_relation_constraint_function_or_probability_law": (
                "successive base-2 digits in the selected six-bit code give the next color for totals 5 down to 0"
            ),
            "write_replacement_assembly_or_commit": (
                "write the code-selected next color at every grid cell and commit synchronously"
            ),
            "result_kind": "one next complete binary grid under the selected code",
            "successor_cardinality": "exactly one successor grid for a selected code",
            "determinism_branching_or_measure": "deterministic after code selection",
            "witness_semantics": (
                "the random-start grids are experimental runs supplied by the separate stochastic field generator"
            ),
            "structural_invariants": "the surveyed family includes most of the 64 rules that leave all-white unchanged",
            "parameters_and_variants": "selected six-bit totalistic code; displayed even codes 2 through 60",
            "excluded_observers_and_representations": (
                "one-dimensional slice and spatial-depth-fog panels are observer outputs"
            ),
        },
        semantic_units=["U001330", "U001331", "U001332", "U001333", "U001335"],
        parameters=["six-bit totalistic rule code"],
        variants=[f"code {code}" for code in range(2, 61, 2)],
        variant_units={
            f"code {code}": ["U001332", "U001333"]
            for code in range(2, 61, 2)
        },
        related_names=[
            "random cellular-automaton initial-field generator family",
            "one-dimensional slice-through-time and spatial-depth-fog observer",
        ],
        related_evidence_units={
            "random cellular-automaton initial-field generator family": [
                "U001331",
                "U001332",
                "U001333",
            ],
            "one-dimensional slice-through-time and spatial-depth-fog observer": [
                "U001334",
                "U001335",
            ],
        },
        na_fields=["seed"],
        role="FAMILY",
    )
    evidence(
        family_2d_name,
        "U001330",
        fields=["witness_semantics", "parameters_and_variants"],
        claim="A000957 is a labeled finite-step random-start family witness, not an intrinsic seed.",
        strength="CONTEXTUAL",
    )
    evidence(
        family_2d_name,
        "U001331",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "topology",
            "alphabet_or_value_schema",
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
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim=(
            "U001331 completely defines the binary five-cell totalistic code scheme and separately "
            "describes random-start experimental runs."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        family_2d_name,
        "U001332",
        fields=["witness_semantics", "parameters_and_variants"],
        claim="A000958 is the original-resolution labeled even-code random-start survey.",
        strength="CONTEXTUAL",
    )
    evidence(
        family_2d_name,
        "U001333",
        fields=["structural_invariants", "parameters_and_variants", "witness_semantics"],
        claim="U001333 identifies the surveyed even-code inventory and the all-white-preserving family restriction.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        family_2d_name,
        "U001334",
        fields=[],
        claim="A000959 is a separate slice/depth-fog observer output.",
        strength="CONTEXTUAL",
    )
    evidence(
        family_2d_name,
        "U001335",
        fields=["excluded_observers_and_representations"],
        claim="U001335 explicitly defines the one-dimensional slice and spatial-depth-fog rendering.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    perturb_name = "single-cell initial-perturbation difference observer"
    perturb = reset_record(
        perturb_name,
        values={
            "object_kind": "paired-run one-cell-perturbation difference observer",
            "carrier": "two aligned cellular-automaton space-time histories",
            "visible_history": "corresponding cells over the aligned evolution histories",
            "input": (
                "two runs under the same cellular-automaton rule and base initial condition, differing only "
                "in the initial color of one selected cell"
            ),
            "read_dependencies_or_neighborhood": (
                "the pair of corresponding cell values at each aligned space-time coordinate"
            ),
            "law_kind": "deterministic aligned comparative difference",
            "rule_relation_constraint_function_or_probability_law": (
                "place a black dot exactly where the corresponding cells in the two runs have different colors"
            ),
            "result_kind": "an aligned black-dot space-time difference history",
            "determinism_branching_or_measure": "deterministic for the supplied pair of histories",
            "witness_semantics": (
                "black dots denote all changed cells; class-specific panels witness dying, localized, uniform-spreading, or sporadic-spreading differences"
            ),
            "parameters_and_variants": (
                "cellular-automaton rule, base initial condition, and selected changed cell"
            ),
        },
        semantic_units=[
            "U001344",
            "U001346",
            "U001348",
            "U001352",
            "U001359",
            "U001362",
        ],
        parameters=[
            "cellular-automaton rule",
            "base initial condition",
            "selected changed cell",
        ],
        related_names=["elementary cellular automaton rule 110"],
        related_evidence_units={
            "elementary cellular automaton rule 110": [
                "U001359",
                "U001360",
                "U001361",
                "U001362",
            ]
        },
        na_fields=["native_time"],
        uncertainties=[
            "The source does not state a completion or stopping criterion for an unbounded comparison."
        ],
    )
    evidence(
        perturb_name,
        "U001344",
        fields=["input", "parameters_and_variants"],
        claim="U001344 defines the paired input by changing the initial color of exactly one cell.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in ("U001345", "U001349", "U001350", "U001351", "U001360", "U001361"):
        evidence(
            perturb_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a finite aligned perturbation-difference witness.",
            strength="CONTEXTUAL",
        )
    evidence(
        perturb_name,
        "U001346",
        fields=[
            "object_kind",
            "carrier",
            "visible_history",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "witness_semantics",
        ],
        claim="U001346 defines the aligned comparison and states that black dots mark every cell that changes.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        perturb_name,
        "U001348",
        fields=["result_kind", "witness_semantics"],
        claim="U001348 directly states the class-specific fates of a one-cell perturbation.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        perturb_name,
        "U001352",
        fields=["parameters_and_variants", "witness_semantics"],
        claim="U001352 identifies the three class-3 rule instances in the one-cell-change comparison.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        perturb_name,
        "U001359",
        fields=["parameters_and_variants", "result_kind", "witness_semantics"],
        claim="U001359 identifies rule 110 and states that differences spread when carried by localized structures.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        perturb_name,
        "U001362",
        fields=["input", "parameters_and_variants"],
        claim="U001362 labels the rule-110 experiment as one changed initial cell.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    period_name = "finite-system repetition-period and maximum-period observer"
    period = reset_record(
        period_name,
        values={
            "object_kind": "finite-orbit recurrence-period observer",
            "native_time": "successive applications of the selected deterministic rule until recurrence",
            "carrier": "a finite deterministic state system, including a finite cyclic cellular automaton",
            "support": "the selected finite state count or cellular-automaton size n",
            "complete_state": "one complete state of the selected finite system",
            "input": "a deterministic transition rule, finite size or state set, and initial state",
            "law_kind": "finite-orbit recurrence measurement",
            "rule_relation_constraint_function_or_probability_law": (
                "iterate from the initial state until a state previously seen on that orbit recurs, "
                "then measure the eventual repetition period; repeat across sizes when a curve is requested"
            ),
            "result_kind": (
                "a repeated-state witness and eventual period, or a period-versus-size curve; the source "
                "reports rule-90 maxima 2^((n-1)/2)-1, rule-30 peaks about 2^(0.63n), "
                "rule-45 peaks near 2^n, and rule-110 peaks roughly n^3"
            ),
            "determinism_branching_or_measure": "deterministic for a fixed rule, size, and initial state",
            "termination_completion_failure": (
                "guaranteed to encounter a repeated state because the deterministic state space is finite"
            ),
            "witness_semantics": (
                "a repeated pair of states witnesses the measured orbit period; plotted points witness the period-versus-size results"
            ),
            "structural_invariants": (
                "the eventual period is at most the number of states; n binary cells have 2^n states and hence period at most 2^n"
            ),
            "parameters_and_variants": "transition rule, finite size or state count, and initial state",
        },
        semantic_units=[
            "U001366",
            "U001384",
            "U001385",
            "U001386",
            "U001387",
            "U001388",
            "U001389",
            "U001391",
            "U001393",
        ],
        parameters=[
            "transition rule",
            "finite size or state count",
            "initial state",
        ],
        variants=[
            "rule 90 period curve",
            "rule 30 period curve",
            "rule 45 period curve",
            "rule 110 period curve",
        ],
        variant_units={
            "rule 90 period curve": ["U001390", "U001392", "U001393"],
            "rule 30 period curve": ["U001390", "U001392", "U001393"],
            "rule 45 period curve": ["U001388", "U001392", "U001393"],
            "rule 110 period curve": ["U001392", "U001393"],
        },
        uncertainties=[
            "The source states the finite-state recurrence procedure and its guarantees but does not present implementation-level storage or cycle-detection details."
        ],
    )
    for unit_id, fields, claim in [
        (
            "U001366",
            [
                "object_kind",
                "carrier",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "termination_completion_failure",
                "structural_invariants",
            ],
            "U001366 states the general finite discrete definite-rule recurrence guarantee.",
        ),
        (
            "U001384",
            [
                "carrier",
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "termination_completion_failure",
            ],
            "U001384 applies ultimate recurrence to finite cyclic cellular automata.",
        ),
        (
            "U001385",
            [
                "support",
                "rule_relation_constraint_function_or_probability_law",
                "termination_completion_failure",
                "structural_invariants",
            ],
            "U001385 bounds the period by the total number of possible states.",
        ),
        (
            "U001386",
            ["support", "parameters_and_variants"],
            "U001386 identifies the finite state count with system size for the single-dot examples.",
        ),
        (
            "U001387",
            [
                "carrier",
                "support",
                "complete_state",
                "structural_invariants",
                "parameters_and_variants",
            ],
            "U001387 states that n binary cells have 2^n complete states.",
        ),
        (
            "U001388",
            ["input", "result_kind", "parameters_and_variants", "witness_semantics"],
            "U001388 directly describes rule- and size-dependent periods and rule 45's near-maximum results.",
        ),
        (
            "U001389",
            [
                "support",
                "rule_relation_constraint_function_or_probability_law",
                "termination_completion_failure",
                "structural_invariants",
            ],
            "U001389 applies the 2^n bound to a pattern confined to n cells.",
        ),
        (
            "U001391",
            [
                "native_time",
                "carrier",
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "termination_completion_failure",
                "parameters_and_variants",
            ],
            "U001391 states eventual repetition for finite cyclic cellular automata and size-dependent periods.",
        ),
        (
            "U001393",
            [
                "input",
                "result_kind",
                "determinism_branching_or_measure",
                "witness_semantics",
                "structural_invariants",
                "parameters_and_variants",
            ],
            "U001393 supplies the single-black initial state and the four rule-specific peak formulas or scalings.",
        ),
    ]:
        evidence(
            period_name,
            unit_id,
            fields=fields,
            claim=claim,
            strength="DIRECT_PARTIAL_MECHANICS",
        )
    for unit_id in ("U001390", "U001392"):
        evidence(
            period_name,
            unit_id,
            fields=["result_kind", "witness_semantics", "parameters_and_variants"],
            claim=f"{unit_id} is an original-resolution finite-orbit or period-curve witness.",
            strength="CONTEXTUAL",
        )

    additivity_name = "additive cellular-automaton superposition relation"
    additivity = reset_record(
        additivity_name,
        values={
            "object_kind": "pointwise cellular-automaton superposition relation",
            "carrier": "aligned binary cellular-automaton configurations and evolution histories",
            "complete_state": "the full aligned component configurations or histories",
            "input": "two or more component initial configurations or their aligned evolutions",
            "law_kind": "additive evolution relation",
            "rule_relation_constraint_function_or_probability_law": (
                "form the source's pointwise aligned superposition of the component configurations; "
                "for an additive rule, evolving the combined initial condition yields the same aligned "
                "superposition of the component evolutions"
            ),
            "result_kind": "the combined initial configuration and its superposed evolution",
            "determinism_branching_or_measure": "one combined relation result for fixed components and an additive rule",
            "witness_semantics": (
                "the component patterns together with the displayed combined pattern witness the superposition identity"
            ),
            "structural_invariants": (
                "additivity is preserved through evolution; rules 90 and 150 are the two fundamentally different elementary additive rules stated here"
            ),
            "parameters_and_variants": "selected additive rule and component configurations",
        },
        semantic_units=["U001411", "U001412", "U001414", "U001463", "U001464"],
        parameters=[
            "selected additive cellular-automaton rule",
            "component configurations",
        ],
        variants=["rule 90 additivity", "rule 150 additivity"],
        variant_units={
            "rule 90 additivity": ["U001412", "U001413", "U001414", "U001463"],
            "rule 150 additivity": ["U001463", "U001464"],
        },
        related_names=[
            "elementary cellular automaton rule 90",
            "elementary cellular automaton rule 150",
        ],
        related_evidence_units={
            "elementary cellular automaton rule 90": [
                "U001412",
                "U001413",
                "U001414",
                "U001463",
            ],
            "elementary cellular automaton rule 150": ["U001463", "U001464"],
        },
        na_fields=["native_time", "termination_completion_failure"],
        uncertainties=[
            "This range names and demonstrates superposition but does not transcribe a separate symbolic formula for the pointwise operator."
        ],
    )
    evidence(
        additivity_name,
        "U001411",
        fields=[],
        claim="U001411 introduces the special initial-condition discussion but supplies no additivity mechanics.",
        strength="CONTEXTUAL",
    )
    evidence(
        additivity_name,
        "U001412",
        fields=[
            "carrier",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001412 states that the displayed rule-90 patterns are superpositions of the basic component pattern.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        additivity_name,
        "U001413",
        fields=["witness_semantics"],
        claim="A000981 is the component-plus-combined rule-90 superposition witness.",
        strength="CONTEXTUAL",
    )
    evidence(
        additivity_name,
        "U001414",
        fields=[
            "object_kind",
            "carrier",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001414 names rule 90's additivity and states the component/combined evolution identity.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        additivity_name,
        "U001463",
        fields=["structural_invariants", "parameters_and_variants"],
        claim="U001463 identifies rules 90 and 150 as the two elementary additive-rule forms.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        additivity_name,
        "U001464",
        fields=[
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "structural_invariants",
            "parameters_and_variants",
        ],
        claim="U001464 states that any additive rule self-emulates and produces nested patterns.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    periodic_name = "periodic-block cellular-automaton initial-condition generator"
    periodic = candidate(periodic_name)
    periodic["units"] = [
        "U001432",
        "U001433",
        "U001434",
        "U001435",
        "U001440",
        "U001441",
        "U001557",
        "U001558",
        "U001561",
    ]
    reset_record(
        periodic_name,
        values={
            "object_kind": "deterministic periodic-tiling initial-condition generator",
            "carrier": "a bi-infinite one-dimensional row tiled by copies of one finite block",
            "alphabet_or_value_schema": "the target cellular automaton's cell alphabet",
            "complete_state": "the complete spatially periodic initial configuration",
            "input": "one finite cell block",
            "law_kind": "deterministic spatial repetition",
            "rule_relation_constraint_function_or_probability_law": (
                "repeat the supplied finite block forever in both spatial directions"
            ),
            "result_kind": "one spatially periodic initial configuration",
            "determinism_branching_or_measure": "deterministic for the supplied block",
            "structural_invariants": "the generated configuration consists everywhere of identical repeated blocks",
            "witness_semantics": (
                "rule-30 period examples and rule 110's 14-cell/7-step background are downstream evolution witnesses, not generator parameters"
            ),
            "parameters_and_variants": "the finite block to be repeated",
        },
        semantic_units=[
            "U001432",
            "U001433",
            "U001434",
            "U001435",
            "U001441",
            "U001558",
            "U001561",
        ],
        parameters=["finite block"],
        variants=["rule-110 14-cell periodic background"],
        variant_units={
            "rule-110 14-cell periodic background": [
                "U001557",
                "U001558",
                "U001561",
            ]
        },
        related_names=[
            "elementary cellular automaton rule 30",
            "elementary cellular automaton rule 110",
        ],
        related_evidence_units={
            "elementary cellular automaton rule 30": ["U001435"],
            "elementary cellular automaton rule 110": [
                "U001557",
                "U001558",
                "U001561",
            ],
        },
        na_fields=["native_time", "seed", "termination_completion_failure"],
        role="SEED",
    )
    evidence(
        periodic_name,
        "U001432",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "structural_invariants",
            "parameters_and_variants",
        ],
        claim="U001432 defines the fixed-block-repeated-forever construction.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        periodic_name,
        "U001433",
        fields=[
            "carrier",
            "rule_relation_constraint_function_or_probability_law",
            "structural_invariants",
        ],
        claim="U001433 explains why identical repeated blocks behave like a finite cyclic system.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in ("U001434", "U001435", "U001441"):
        evidence(
            periodic_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is a downstream rule-30 periodic-start result or restriction.",
            strength="DIRECT_PARTIAL_MECHANICS",
        )
    evidence(
        periodic_name,
        "U001440",
        fields=["witness_semantics"],
        claim="A000989 is a downstream rule-30 periodic-start catalog witness.",
        strength="CONTEXTUAL",
    )
    evidence(
        periodic_name,
        "U001557",
        fields=["witness_semantics"],
        claim="A001022 is the rule-110 random evolution showing its periodic background.",
        strength="CONTEXTUAL",
    )
    for unit_id in ("U001558", "U001561"):
        evidence(
            periodic_name,
            unit_id,
            fields=["witness_semantics", "parameters_and_variants"],
            claim=f"{unit_id} identifies rule 110's repeated 14-cell spatial background and 7-step evolution period.",
            strength="DIRECT_PARTIAL_MECHANICS",
        )

    two_block_name = "rule-126 random two-block initial-condition ensemble"
    two_block = reset_record(
        two_block_name,
        values={
            "object_kind": "stochastic two-block-sequence initial-condition generator",
            "carrier": "a one-dimensional concatenation of four-cell blocks",
            "alphabet_or_value_schema": "black and white cells",
            "complete_state": "one complete block-concatenated initial configuration",
            "input": "the permitted block set {BBWW, BBBW} and an unstated random block-selection process",
            "law_kind": "stochastic block-sequence generation law",
            "rule_relation_constraint_function_or_probability_law": (
                "form a random sequence whose successive four-cell blocks are BBWW or BBBW"
            ),
            "result_kind": "one rule-126 initial configuration tiled by the permitted blocks",
            "determinism_branching_or_measure": (
                "stochastic; block probabilities, independence, and spatial extent are not stated"
            ),
            "structural_invariants": "every generated four-cell block is BBWW or BBBW",
            "parameters_and_variants": "permitted four-cell block set {BBWW, BBBW}",
        },
        semantic_units=["U001436", "U001439"],
        parameters=["permitted four-cell block set"],
        related_names=["elementary cellular automaton rule 126"],
        related_evidence_units={
            "elementary cellular automaton rule 126": [
                "U001436",
                "U001437",
                "U001438",
                "U001439",
            ]
        },
        na_fields=["native_time", "seed", "termination_completion_failure"],
        uncertainties=[
            "The source does not state the probability of either block, independence between selections, or spatial extent."
        ],
        role="SEED",
    )
    evidence(
        two_block_name,
        "U001436",
        fields=[
            "object_kind",
            "carrier",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "parameters_and_variants",
        ],
        claim="U001436 introduces the rule-126 initial condition involving a random sequence of two different blocks.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in ("U001437", "U001438"):
        evidence(
            two_block_name,
            unit_id,
            fields=["witness_semantics"] if "witness_semantics" in two_block["values"] else [],
            claim=f"{unit_id} is a finite native-rule outcome witness for the special two-block seed.",
            strength="CONTEXTUAL",
        )
    evidence(
        two_block_name,
        "U001439",
        fields=[
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "structural_invariants",
            "parameters_and_variants",
        ],
        claim="U001439 transcribes the permitted blocks BBWW and BBBW and states that their sequence is random.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    nested_name = "nested substitution initial condition for rule 184"
    nested = candidate(nested_name)
    nested["parameters"] = []
    nested["values"].pop("parameters_and_variants", None)

    full_binary_name = "full binary configuration language"
    full_binary = reset_record(
        full_binary_name,
        values={
            "object_kind": "declarative full binary configuration language",
            "carrier": "one-dimensional binary cell sequences",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one proposed complete black-or-white sequence",
            "input": "a proposed binary cell sequence",
            "law_kind": "declarative sequence-membership relation",
            "rule_relation_constraint_function_or_probability_law": (
                "accept every binary sequence; there are no forbidden finite strings"
            ),
            "result_kind": "membership in the full binary configuration language",
            "determinism_branching_or_measure": (
                "deterministic membership relation; no sampling measure is implied"
            ),
            "structural_invariants": "the language has no forbidden black-or-white strings",
            "excluded_observers_and_representations": (
                "the two-loop path network represents this language but is not the language itself"
            ),
        },
        semantic_units=["U001483", "U001494", "U001498"],
        related_names=["allowed-sequence path-network observer"],
        related_evidence_units={
            "allowed-sequence path-network observer": ["U001494", "U001498"]
        },
        na_fields=[
            "native_time",
            "parameters_and_variants",
            "termination_completion_failure",
        ],
        role="CONSTRAINT",
    )
    evidence(
        full_binary_name,
        "U001483",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "structural_invariants",
        ],
        claim="U001483 states that absolutely any black-or-white sequence is admitted.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        full_binary_name,
        "U001494",
        fields=[
            "carrier",
            "alphabet_or_value_schema",
            "input",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "structural_invariants",
            "excluded_observers_and_representations",
        ],
        claim="U001494 restates the unrestricted step-1 language and gives its separate two-loop path-network representation.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        full_binary_name,
        "U001498",
        fields=["excluded_observers_and_representations"],
        claim="U001498 confirms that network paths represent all sequences in the unrestricted language.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    attractor255_name = "rule-255 all-black attractor"
    attractor255 = reset_record(
        attractor255_name,
        values={
            "object_kind": "one-step rule-255 attractor relation",
            "native_time": "one rule-255 cellular-automaton step",
            "carrier": "one-dimensional binary configurations",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one complete binary configuration",
            "input": "any complete binary initial configuration",
            "law_kind": "deterministic one-step attractor relation",
            "rule_relation_constraint_function_or_probability_law": (
                "apply rule 255 once; every cell becomes black"
            ),
            "result_kind": "the unique all-black configuration",
            "determinism_branching_or_measure": "deterministic",
            "termination_completion_failure": "the attractor result is reached after exactly one step",
            "witness_semantics": (
                "the rule table and one-step evolution witness that every input maps to all black"
            ),
        },
        semantic_units=["U001484", "U001486"],
        related_names=["elementary cellular automaton rule 255"],
        related_evidence_units={
            "elementary cellular automaton rule 255": [
                "U001484",
                "U001485",
                "U001486",
            ]
        },
        na_fields=["parameters_and_variants"],
        role="CONSTRAINT",
    )
    evidence(
        attractor255_name,
        "U001484",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "termination_completion_failure",
        ],
        claim="U001484 states that after one step the only possible sequences are all black.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        attractor255_name,
        "U001485",
        fields=["witness_semantics"],
        claim="A001005 is the original-resolution rule-table and one-step attractor witness.",
        strength="CONTEXTUAL",
    )
    evidence(
        attractor255_name,
        "U001486",
        fields=[
            "object_kind",
            "native_time",
            "alphabet_or_value_schema",
            "input",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "termination_completion_failure",
            "witness_semantics",
        ],
        claim="U001486 identifies rule 255 and its one-step all-black allowed-sequence result.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        attractor255_name,
        "U001487",
        fields=[],
        claim="U001487 transitions to the contrasting rule-4 attractor and adds no rule-255 mechanics.",
        strength="CONTEXTUAL",
    )

    attractor4_name = "rule-4 isolated-black attractor-set constraint"
    attractor4 = reset_record(
        attractor4_name,
        values={
            "object_kind": "rule-4 attractor-set membership constraint",
            "carrier": "one-dimensional binary configurations",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one proposed complete binary configuration",
            "input": "a proposed rule-4 attractor configuration",
            "law_kind": "declarative configuration-membership constraint",
            "rule_relation_constraint_function_or_probability_law": (
                "accept exactly configurations with no adjacent black cells"
            ),
            "result_kind": "membership in the rule-4 one-step attractor set",
            "determinism_branching_or_measure": "deterministic membership relation",
            "structural_invariants": (
                "every black cell has at least one white cell on each side; equivalently, no two black cells are adjacent"
            ),
            "excluded_observers_and_representations": (
                "the two-node path network represents this language but is not the constraint itself"
            ),
        },
        semantic_units=["U001485", "U001486", "U001488"],
        related_names=[
            "elementary cellular automaton rule 4",
            "allowed-sequence path-network observer",
            "rule-4 many-to-one basin-of-attraction relation",
        ],
        related_evidence_units={
            "elementary cellular automaton rule 4": [
                "U001485",
                "U001486",
            ],
            "allowed-sequence path-network observer": ["U001486"],
            "rule-4 many-to-one basin-of-attraction relation": ["U001488"],
        },
        na_fields=["native_time", "parameters_and_variants"],
        role="CONSTRAINT",
    )
    evidence(
        attractor4_name,
        "U001485",
        fields=[],
        claim="A001005 is a finite rule-4 table/evolution witness; the constraint is stated in prose.",
        strength="CONTEXTUAL",
    )
    evidence(
        attractor4_name,
        "U001486",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "structural_invariants",
            "excluded_observers_and_representations",
        ],
        claim="U001486 defines the rule-4 attractor language and identifies its separate path-network representation.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        attractor4_name,
        "U001488",
        fields=[
            "input",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "structural_invariants",
        ],
        claim="U001488 directly states the complete no-adjacent-black attractor-set constraint.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    basin4_name = "rule-4 many-to-one basin-of-attraction relation"
    basin4 = reset_record(
        basin4_name,
        values={
            "object_kind": "one-step rule-4 basin-membership relation",
            "native_time": "one rule-4 cellular-automaton step",
            "carrier": "ordered pairs of initial and final one-dimensional binary configurations",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one complete proposed initial/final configuration pair",
            "input": "a proposed initial configuration and proposed final attractor configuration",
            "law_kind": "deterministic one-step basin-membership test",
            "rule_relation_constraint_function_or_probability_law": (
                "accept the pair exactly when one rule-4 step maps the proposed initial configuration to the proposed final configuration"
            ),
            "result_kind": "membership of the proposed pair in the one-step basin relation",
            "determinism_branching_or_measure": (
                "deterministic membership test; many accepted initial configurations may share one final configuration"
            ),
            "termination_completion_failure": "the membership test completes after one rule-4 step",
            "witness_semantics": (
                "the source exhibits four accepted initial/final pairs sharing the same final configuration"
            ),
        },
        semantic_units=["U001489", "U001491"],
        related_names=[
            "elementary cellular automaton rule 4",
            "rule-4 isolated-black attractor-set constraint",
        ],
        related_evidence_units={
            "elementary cellular automaton rule 4": [
                "U001489",
                "U001490",
                "U001491",
            ],
            "rule-4 isolated-black attractor-set constraint": ["U001489"],
        },
        na_fields=["parameters_and_variants"],
        role="CONSTRAINT",
    )
    evidence(
        basin4_name,
        "U001489",
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "termination_completion_failure",
            "witness_semantics",
        ],
        claim="U001489 states that many distinct initial configurations can map to one selected final attractor configuration.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        basin4_name,
        "U001490",
        fields=["witness_semantics"],
        claim="A001006 is the original-resolution four-pair/one-final-state basin witness.",
        strength="CONTEXTUAL",
    )
    evidence(
        basin4_name,
        "U001491",
        fields=[
            "input",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "termination_completion_failure",
            "witness_semantics",
        ],
        claim="U001491 labels four distinct initial/final pairs as members of the same rule-4 basin.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    surjective_name = "surjective binary cellular-automaton mapping family"
    surjective = reset_record(
        surjective_name,
        values={
            "object_kind": "surjectivity property of a selected cellular-automaton global map",
            "carrier": "global maps on one-dimensional black-or-white configurations",
            "alphabet_or_value_schema": "black and white",
            "input": "a selected cellular-automaton global map on the full binary configuration domain",
            "law_kind": "declarative global-map property",
            "rule_relation_constraint_function_or_probability_law": (
                "classify the selected map as surjective when every possible binary sequence can still occur at every subsequent step"
            ),
            "result_kind": "membership of the selected global map in the surjective or onto class",
            "determinism_branching_or_measure": "deterministic property of the selected map",
            "parameters_and_variants": "selected rule; examples 204, 240, 30, and 90",
        },
        semantic_units=["U001508", "U001511", "U001512"],
        parameters=["selected cellular-automaton rule"],
        variants=["rule 204", "rule 240", "rule 30", "rule 90"],
        variant_units={
            variant: ["U001511", "U001512"]
            for variant in ("rule 204", "rule 240", "rule 30", "rule 90")
        },
        na_fields=[
            "complete_state",
            "native_time",
            "termination_completion_failure",
            "witness_semantics",
        ],
        role="CONSTRAINT",
    )
    evidence(
        surjective_name,
        "U001508",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
        ],
        claim="U001508 defines surjective cellular automata by preservation of all possible binary sequences at every step.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    for unit_id in ("U001509", "U001510"):
        evidence(
            surjective_name,
            unit_id,
            fields=[],
            claim=f"{unit_id} is contextual discussion of the surjective examples.",
            strength="CONTEXTUAL",
        )
    evidence(
        surjective_name,
        "U001511",
        fields=["parameters_and_variants"],
        claim="A001010 is the original-resolution inventory labeled rules 204, 240, 30, and 90.",
        strength="CONTEXTUAL",
    )
    evidence(
        surjective_name,
        "U001512",
        fields=["parameters_and_variants"],
        claim="U001512 identifies the displayed rules as surjective or onto mappings.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )

    network_name = "allowed-sequence path-network observer"
    network = candidate(network_name)
    for unit_id in ("U001513", "U001514", "U001515"):
        if unit_id not in network["units"]:
            network["units"].append(unit_id)
        if unit_id not in network["semantic_units"]:
            network["semantic_units"].append(unit_id)
    conflict_variant = "source-conflicted adjacent-black language network"
    if conflict_variant not in network["variants"]:
        network["variants"].append(conflict_variant)
    network["variant_units"][conflict_variant] = ["U001513", "U001514", "U001515"]
    network["related_names"] = list(
        dict.fromkeys(
            [
                *network["related_names"],
                full_binary_name,
                attractor4_name,
                "conflicted adjacent-black constrained initial-condition language",
            ]
        )
    )
    network["related_evidence_units"].update(
        {
            full_binary_name: ["U001494", "U001498"],
            attractor4_name: ["U001496", "U001498"],
            "conflicted adjacent-black constrained initial-condition language": [
                "U001513",
                "U001514",
                "U001515",
            ],
        }
    )
    network["uncertainties"] = list(
        dict.fromkeys(
            [
                *network["uncertainties"],
                "The U001513–U001515 network instance is source-conflicted: the prose forbids adjacent black cells while its caption permits black cells only in pairs.",
            ]
        )
    )
    network["source_statuses"] = ["CLEAR", "CONFLICTING"]
    for unit_id, claim in [
        (
            "U001513",
            "U001513 supplies one side of the conflicted adjacent-black input-language specification.",
        ),
        (
            "U001514",
            "A001011 is the network instance whose surrounding live text is contradictory.",
        ),
        (
            "U001515",
            "U001515 supplies the contradictory caption-side paired-black specification.",
        ),
    ]:
        evidence(
            network_name,
            unit_id,
            fields=["parameters_and_variants", "witness_semantics"],
            claim=claim,
            strength="DEFECT_LIMITED",
        )

    conflict_name = "conflicted adjacent-black constrained initial-condition language"
    conflict = reset_record(
        conflict_name,
        values={
            "object_kind": "source-conflicted declarative binary configuration language",
            "carrier": "one-dimensional binary cell sequences",
            "alphabet_or_value_schema": "black and white",
            "complete_state": "one proposed complete binary initial sequence",
            "input": "a proposed binary initial sequence",
            "law_kind": "declarative sequence-membership constraint",
            "rule_relation_constraint_function_or_probability_law": (
                "CONFLICT: U001513 forbids adjacent black cells, while U001515 says black cells are allowed only in pairs"
            ),
            "result_kind": "CONFLICT: membership in the intended language cannot be resolved",
            "determinism_branching_or_measure": (
                "membership would be deterministic after the contradictory language definition is resolved"
            ),
            "structural_invariants": (
                "CONFLICT: no-adjacent-black and paired-black invariants are mutually incompatible"
            ),
            "witness_semantics": (
                "CONFLICT: the network image cannot decide which of the contradictory live descriptions it witnesses"
            ),
        },
        semantic_units=["U001513", "U001514", "U001515"],
        related_names=[network_name],
        related_evidence_units={
            network_name: ["U001513", "U001514", "U001515"]
        },
        na_fields=[
            "native_time",
            "parameters_and_variants",
            "termination_completion_failure",
        ],
        uncertainties=[
            "U001513 forbids adjacent black cells, while U001515 requires black cells to occur in pairs; A001011 cannot resolve the contradiction."
        ],
        role="CONSTRAINT",
    )
    conflict["source_status"] = "CONFLICTING"
    conflict["conflicting_fields"] = [
        "rule_relation_constraint_function_or_probability_law",
        "structural_invariants",
        "result_kind",
        "witness_semantics",
    ]
    evidence(
        conflict_name,
        "U001513",
        fields=[
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "structural_invariants",
            "result_kind",
            "determinism_branching_or_measure",
            "witness_semantics",
        ],
        claim="U001513 defines the no-adjacent-black side of the conflict.",
        strength="DEFECT_LIMITED",
    )
    evidence(
        conflict_name,
        "U001514",
        fields=[
            "rule_relation_constraint_function_or_probability_law",
            "structural_invariants",
            "result_kind",
            "witness_semantics",
        ],
        claim="A001011 is the owned network witness but cannot resolve the contradictory descriptions.",
        strength="DEFECT_LIMITED",
    )
    evidence(
        conflict_name,
        "U001515",
        fields=[
            "rule_relation_constraint_function_or_probability_law",
            "structural_invariants",
            "result_kind",
            "witness_semantics",
        ],
        claim="U001515 defines the paired-black side of the conflict.",
        strength="DEFECT_LIMITED",
    )

    brute_name = "persistent-structure exhaustive search query"
    brute = candidate(brute_name)
    brute["units"] = [
        "U001519",
        "U001532",
        "U001533",
        "U001534",
        "U001535",
        "U001536",
        "U001542",
        "U001543",
        "U001544",
        "U001545",
        "U001546",
        "U001548",
        "U001549",
        "U001550",
        "U001551",
        "U001552",
        "U001553",
        "U001554",
        "U001555",
        "U001556",
        "U001562",
        "U001563",
        "U001567",
        "U001568",
        "U001569",
        "U001570",
    ]
    reset_record(
        brute_name,
        values={
            "object_kind": "bounded ordered persistent-structure enumeration query",
            "carrier": (
                "localized cellular-automaton seeds in the selected codec or periodic-background environment, "
                "together with their trial evolutions"
            ),
            "input": (
                "a cellular-automaton rule, seed codec or environment, and a finite numeric-prefix or block-width bound"
            ),
            "law_kind": "bounded ordered seed enumeration and trial-evolution query",
            "rule_relation_constraint_function_or_probability_law": (
                "enumerate seeds in the source's stated numeric or width order, decode or embed each seed, "
                "evolve it under the selected rule, and classify the witnessed outcome as dying, fixed, "
                "moving, persistent, or unbounded"
            ),
            "result_kind": (
                "a finite bounded-search catalog of dying, fixed, moving, persistent, or unbounded outcomes; "
                "no completeness beyond the selected bound is implied"
            ),
            "determinism_branching_or_measure": (
                "deterministic for the selected rule, codec or environment, bound, and trial-classification convention"
            ),
            "termination_completion_failure": (
                "the ordered enumeration terminates after the requested finite prefix or width-bounded candidate set is exhausted"
            ),
            "witness_semantics": (
                "each catalog entry couples a seed identifier or block with its evolution and reported outcome class"
            ),
            "parameters_and_variants": (
                "selected cellular-automaton rule and finite numeric-prefix or block-width bound"
            ),
        },
        semantic_units=[
            "U001519",
            "U001533",
            "U001534",
            "U001536",
            "U001542",
            "U001544",
            "U001545",
            "U001546",
            "U001548",
            "U001550",
            "U001551",
            "U001553",
            "U001554",
            "U001556",
            "U001562",
            "U001563",
            "U001568",
            "U001570",
        ],
        parameters=[
            "cellular-automaton rule",
            "finite numeric-prefix or block-width bound",
        ],
        variants=[
            "code-20 first-200 binary-seed survey",
            "code-20 first-25-billion binary-seed survey",
            "code-357 first-2-billion base-3-seed survey",
            "code-1329 persistent-structure survey",
            "code-1329 unbounded-growth survey",
            "rule-110 blocks-smaller-than-40 background-embedded survey",
            "rule-110 width-41 unbounded-growth survey",
        ],
        variant_units={
            "code-20 first-200 binary-seed survey": ["U001532", "U001533"],
            "code-20 first-25-billion binary-seed survey": [
                "U001534",
                "U001535",
                "U001536",
            ],
            "code-357 first-2-billion base-3-seed survey": [
                "U001542",
                "U001543",
                "U001544",
                "U001545",
                "U001546",
            ],
            "code-1329 persistent-structure survey": [
                "U001548",
                "U001549",
                "U001550",
            ],
            "code-1329 unbounded-growth survey": [
                "U001551",
                "U001552",
                "U001553",
                "U001554",
                "U001555",
                "U001556",
            ],
            "rule-110 blocks-smaller-than-40 background-embedded survey": [
                "U001562",
                "U001567",
                "U001568",
            ],
            "rule-110 width-41 unbounded-growth survey": [
                "U001563",
                "U001569",
                "U001570",
            ],
        },
        related_names=[
            "two-color next-nearest-neighbor cellular automaton code 20",
            "three-color nearest-neighbor cellular automaton code 357",
            "three-color nearest-neighbor cellular automaton code 1329",
            "elementary cellular automaton rule 110",
            "localized finite-seed integer codec family",
            "periodic-block cellular-automaton initial-condition generator",
        ],
        related_evidence_units={
            "two-color next-nearest-neighbor cellular automaton code 20": [
                "U001519",
                "U001532",
                "U001533",
                "U001534",
                "U001535",
                "U001536",
            ],
            "three-color nearest-neighbor cellular automaton code 357": [
                "U001542",
                "U001543",
                "U001544",
                "U001545",
                "U001546",
            ],
            "three-color nearest-neighbor cellular automaton code 1329": [
                "U001548",
                "U001549",
                "U001550",
                "U001551",
                "U001552",
                "U001553",
                "U001554",
                "U001555",
                "U001556",
            ],
            "elementary cellular automaton rule 110": [
                "U001562",
                "U001563",
                "U001567",
                "U001568",
                "U001569",
                "U001570",
            ],
            "localized finite-seed integer codec family": [
                "U001533",
                "U001536",
                "U001544",
            ],
            "periodic-block cellular-automaton initial-condition generator": [
                "U001562",
                "U001563",
                "U001567",
                "U001568",
                "U001569",
                "U001570",
            ],
        },
        uncertainties=[
            "The source reports finite searches and outcomes but does not state a universal per-trial stopping or equivalence-deduplication algorithm."
        ],
    )
    evidence(
        brute_name,
        "U001519",
        fields=[
            "object_kind",
            "carrier",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "termination_completion_failure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim=(
            "U001519 defines the ordered method: try possible initial conditions in turn, evolve each, "
            "and look for new persistent structures."
        ),
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    for unit_id in (
        "U001532",
        "U001535",
        "U001543",
        "U001549",
        "U001552",
        "U001555",
        "U001567",
        "U001569",
    ):
        evidence(
            brute_name,
            unit_id,
            fields=["witness_semantics"],
            claim=f"{unit_id} is an original-resolution bounded-search catalog or outcome witness.",
            strength="CONTEXTUAL",
        )
    for unit_id, fields, claim in [
        (
            "U001533",
            [
                "carrier",
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "witness_semantics",
                "parameters_and_variants",
            ],
            "U001533 fixes the code-20 region-smaller-than-nine bound, base-2 seed order, and dying/persistent outcomes.",
        ),
        (
            "U001534",
            [
                "input",
                "result_kind",
                "termination_completion_failure",
                "witness_semantics",
                "parameters_and_variants",
            ],
            "U001534 reports the finite first-25-billion prefix and explicitly leaves larger structures possible.",
        ),
        (
            "U001536",
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001536 labels the code-20 catalog by its base-2 seed numbers.",
        ),
        (
            "U001542",
            [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "termination_completion_failure",
                "parameters_and_variants",
            ],
            "U001542 states that the code-357 catalog comes from explicitly testing the first two billion seeds.",
        ),
        (
            "U001544",
            [
                "carrier",
                "input",
                "result_kind",
                "witness_semantics",
                "parameters_and_variants",
            ],
            "U001544 supplies base-3 seed decoding and reports no code-357 persistent structures with period below five.",
        ),
        (
            "U001545",
            ["result_kind", "witness_semantics"],
            "U001545 describes the first code-357 persistent outcomes found in the bounded prefix.",
        ),
        (
            "U001546",
            ["result_kind", "witness_semantics"],
            "U001546 records the moving code-357 structure at seed 4,803,890.",
        ),
        (
            "U001548",
            ["input", "result_kind", "witness_semantics", "parameters_and_variants"],
            "U001548 introduces the first code-1329 persistent structures and their ordered seed identifiers.",
        ),
        (
            "U001550",
            ["result_kind", "witness_semantics"],
            "U001550 labels the code-1329 persistent-structure catalog.",
        ),
        (
            "U001551",
            ["result_kind", "witness_semantics", "parameters_and_variants"],
            "U001551 identifies the seed-54,889 unbounded-growth outcome.",
        ),
        (
            "U001553",
            ["result_kind", "witness_semantics"],
            "U001553 gives the 10-cell seed, 256-step repeating edge, and unbounded trail of persistent structures.",
        ),
        (
            "U001554",
            ["result_kind", "witness_semantics"],
            "U001554 introduces the simpler unbounded-growth outcome at seed 97,439.",
        ),
        (
            "U001556",
            ["result_kind", "witness_semantics"],
            "U001556 labels the simple and complex code-1329 unbounded-growth witnesses.",
        ),
        (
            "U001562",
            [
                "carrier",
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "termination_completion_failure",
                "parameters_and_variants",
            ],
            "U001562 bounds the rule-110 catalog to blocks less than 40 cells wide in its periodic environment.",
        ),
        (
            "U001563",
            ["input", "result_kind", "parameters_and_variants"],
            "U001563 states that width-41 blocks yield the rule-110 unbounded-growth case.",
        ),
        (
            "U001568",
            ["result_kind", "witness_semantics"],
            "U001568 labels the bounded rule-110 persistent-structure catalog and extension forms.",
        ),
        (
            "U001570",
            [
                "carrier",
                "input",
                "result_kind",
                "witness_semantics",
                "parameters_and_variants",
            ],
            "U001570 supplies the width-41 block embedded between periodic background blocks and its 77-step growth cycle.",
        ),
    ]:
        evidence(
            brute_name,
            unit_id,
            fields=fields,
            claim=claim,
            strength="DIRECT_PARTIAL_MECHANICS",
        )

    solver_name = "systematic fixed-period persistent-structure constraint solver"
    solver = candidate(solver_name)
    if "U001544" not in solver["units"]:
        solver["units"].append("U001544")
    reset_record(
        solver_name,
        values={
            "object_kind": "complete fixed-period persistent-structure constraint solver",
            "carrier": "fixed or moving cellular-automaton structures",
            "input": "a cellular-automaton rule and requested repetition period",
            "law_kind": "systematic fixed-period constraint solution",
            "rule_relation_constraint_function_or_probability_law": (
                "solve the period constraints so as to find absolutely all fixed or moving persistent structures "
                "with the requested small period"
            ),
            "result_kind": (
                "the complete solution set for the requested period, including an explicit no-solution result when the set is empty"
            ),
            "determinism_branching_or_measure": "complete deterministic constraint query for the requested rule and period",
            "termination_completion_failure": (
                "the source states completion for each requested small period handled by the systematic procedure"
            ),
            "witness_semantics": (
                "a complete structure catalog witnesses a nonempty solution set; an asserted absent period witnesses no solution"
            ),
            "parameters_and_variants": "cellular-automaton rule and requested repetition period",
        },
        semantic_units=["U001537", "U001538", "U001540", "U001544"],
        parameters=[
            "cellular-automaton rule",
            "requested repetition period",
        ],
        variants=[
            "code-20 complete results through period 15",
            "code-357 no persistent structure below period 5",
        ],
        variant_units={
            "code-20 complete results through period 15": [
                "U001537",
                "U001538",
                "U001539",
                "U001540",
            ],
            "code-357 no persistent structure below period 5": ["U001544"],
        },
        related_names=[
            "two-color next-nearest-neighbor cellular automaton code 20",
            "three-color nearest-neighbor cellular automaton code 357",
        ],
        related_evidence_units={
            "two-color next-nearest-neighbor cellular automaton code 20": [
                "U001537",
                "U001538",
                "U001539",
                "U001540",
            ],
            "three-color nearest-neighbor cellular automaton code 357": ["U001544"],
        },
        na_fields=["native_time"],
        uncertainties=[
            "The source states the solver's completeness contract but routes implementation details of the constraint encoding to page 268."
        ],
    )
    evidence(
        solver_name,
        "U001537",
        fields=[
            "object_kind",
            "carrier",
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "determinism_branching_or_measure",
            "termination_completion_failure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001537 states that the systematic procedure finds absolutely all structures for a requested small period.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        solver_name,
        "U001538",
        fields=[
            "input",
            "result_kind",
            "termination_completion_failure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001538 reports complete code-20 results through period 15 and period-specific no/large-solution facts.",
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        solver_name,
        "U001539",
        fields=["result_kind", "witness_semantics", "parameters_and_variants"],
        claim="A001017 is the original-resolution complete period-bounded code-20 solution catalog.",
        strength="CONTEXTUAL",
    )
    evidence(
        solver_name,
        "U001540",
        fields=[
            "input",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "termination_completion_failure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001540 states that all code-20 structures through period 15 were found by the constraint method.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )
    evidence(
        solver_name,
        "U001544",
        fields=[
            "input",
            "result_kind",
            "termination_completion_failure",
            "witness_semantics",
            "parameters_and_variants",
        ],
        claim="U001544 supplies the universal no-solution result for code-357 repetition periods below five.",
        strength="DIRECT_COMPLETE_MECHANICS",
    )

    # Remove inherited per-unit evidence-limit declarations. build_output()
    # assigns the record boundary once to the strongest identity/law anchor.
    for row in defs:
        row["values"].pop("evidence_limit", None)
        row["field_units"].pop("evidence_limit", None)
        for override in row["evidence_overrides"].values():
            override["fields"] = [
                field for field in override.get("fields", []) if field != "evidence_limit"
            ]

    defs.sort(
        key=lambda candidate: (
            int(candidate["units"][0][1:]),
            candidate["anchor_priority"],
        )
    )
    return defs


ROUTE_DEFS = [
    ("U001233", "page 24", "PAGE", "earlier presentation of rule 254", "CROSS_RANGE", ["rule 254"]),
    ("U001233", "page 53", "PAGE", "elementary cellular-automaton rule-number scheme", "CROSS_RANGE", ["rule numbering"]),
    ("U001254", "page 32", "PAGE", "earlier rule-110 discussion", "CROSS_RANGE", ["rule 110"]),
    ("U001302", "page 232", "PAGE", "rule columns restricting possible behavior classes", "WITHIN_STAGE", ["class 1", "class 2"]),
    ("U001311", "page 155", "PAGE", "continuous cellular-automaton construction", "CROSS_RANGE", ["continuous cellular automaton"]),
    ("U001316", "page 155", "PAGE", "continuous cellular-automaton construction", "CROSS_RANGE", ["continuous cellular automaton"]),
    ("U001326", "page 248", "PAGE", "one-dimensional slices of two-dimensional evolution", "WITHIN_STAGE", ["slice"]),
    ("U001327", "page 248", "PAGE", "class-4 two-dimensional slice examples", "WITHIN_STAGE", ["class 4"]),
    ("U001327", "page 229", "PAGE", "rule-110 repetitive background comparison", "WITHIN_STAGE", ["rule 110"]),
    ("U001329", "page 249", "PAGE", "Game of Life and its one-dimensional slice", "WITHIN_STAGE", ["Game of Life"]),
    ("U001358", "later in this book", "OTHER", "information handling in systems in nature", "CROSS_RANGE", ["information handling"]),
    ("U001366", "the next chapter", "SECTION", "limited-size repetition in nature", "CROSS_RANGE", ["repetition"]),
    ("U001399", "page 27", "PAGE", "rule-30 simple-initial-condition construction", "CROSS_RANGE", ["rule 30"]),
    ("U001423", "the next few chapters", "SECTION", "natural-system stability from intrinsic randomness", "CROSS_RANGE", ["stability"]),
    ("U001431", "page 210", "PAGE", "constraint satisfaction for periodic behavior", "CROSS_RANGE", ["constraints"]),
    ("U001433", "page 255", "PAGE", "limited-size cellular-automaton systems", "WITHIN_STAGE", ["limited size"]),
    ("U001450", "page 263", "PAGE", "rule-22 initial conditions yielding rule-90 behavior", "WITHIN_STAGE", ["rule 22", "rule 90"]),
    ("U001463", "page 264", "PAGE", "additivity and superposition", "WITHIN_STAGE", ["additive rule"]),
    ("U001464", "page 264", "PAGE", "additivity and superposition", "WITHIN_STAGE", ["additive rule"]),
    ("U001470", "page 82", "PAGE", "substitution-system construction", "CROSS_RANGE", ["substitution system"]),
    ("U001474", "page 83", "PAGE", "substitution-system construction", "CROSS_RANGE", ["substitution system"]),
    ("U001478", "page 338", "PAGE", "equal-density rule-184 nested patterns", "CROSS_RANGE", ["rule 184"]),
    ("U001522", "page 252", "PAGE", "moving structures and information communication", "WITHIN_STAGE", ["moving structure"]),
    ("U001540", "page 268", "PAGE", "systematic constraint method for all fixed-period structures", "WITHIN_STAGE", ["constraints", "persistent structures"]),
    ("U001542", "page 282", "PAGE", "code-357 cellular automaton", "WITHIN_STAGE", ["code 357"]),
    ("U001544", "page 282", "PAGE", "code-357 cellular automaton", "WITHIN_STAGE", ["code 357"]),
    ("U001548", "page 282", "PAGE", "code-1329 cellular automaton", "WITHIN_STAGE", ["code 1329"]),
    ("U001550", "page 282", "PAGE", "code-1329 cellular automaton", "WITHIN_STAGE", ["code 1329"]),
    ("U001559", "Chapter 11", "SECTION", "computation and universality", "CROSS_RANGE", ["universality"]),
    ("U001560", "page 32", "PAGE", "earlier rule-110 discussion", "CROSS_RANGE", ["rule 110"]),
    ("U001563", "page 293", "PAGE", "rule-110 unbounded-growth example", "WITHIN_STAGE", ["rule 110"]),
    ("U001564", "pages 294–296", "PAGE", "rule-110 structure collisions", "WITHIN_STAGE", ["rule 110", "collision"]),
    ("U001572", "page 292", "PAGE", "rule-110 persistent-structure labels", "WITHIN_STAGE", ["rule 110"]),
    ("U001574", "page 292", "PAGE", "rule-110 persistent-structure labels", "WITHIN_STAGE", ["rule 110"]),
    ("U001576", "page 292", "PAGE", "rule-110 persistent-structure labels", "WITHIN_STAGE", ["rule 110"]),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_bundle(bundle: Path) -> dict[str, Any]:
    manifest_bytes = (bundle / "allowed-manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    units = [json.loads(line) for line in (bundle / "input/source-units.jsonl").read_text(encoding="utf-8").splitlines()]
    reading = read_csv(bundle / "input/reading-input.csv")
    assets = read_csv(bundle / "input/asset-input.csv")
    source_bytes = (bundle / "input/sources" / SOURCE_PATH).read_bytes()
    schemas = {
        path.name: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((bundle / "input/schemas").glob("*.json"))
    }
    return {
        "manifest": manifest,
        "manifest_sha": sha256_bytes(manifest_bytes),
        "units": units,
        "reading": reading,
        "assets": assets,
        "source_bytes": source_bytes,
        "schemas": schemas,
    }


def validate_bundle(bundle: Path, data: dict[str, Any]) -> None:
    manifest = data["manifest"]
    check(manifest["worker_id"] == WORKER_ID, "wrong bundle worker")
    check(manifest["stage"] == STAGE, "wrong bundle stage")
    check(manifest["discovery_epoch"] == EPOCH, "wrong discovery epoch")
    check(manifest["source_paths"] == [SOURCE_PATH], "unexpected source paths")
    check(len(data["units"]) == manifest["source_unit_count"] == 354, "source-unit count mismatch")
    check(len(data["reading"]) == 354, "reading projection count mismatch")
    check(len(data["assets"]) == manifest["asset_count"] == 105, "asset count mismatch")
    allowed = {row["path"]: row for row in manifest["allowed_inputs"]}
    for rel, row in allowed.items():
        raw = (bundle / rel).read_bytes()
        check(len(raw) == row["bytes"], f"byte mismatch for {rel}")
        check(sha256_bytes(raw) == row["sha256"], f"hash mismatch for {rel}")
    check(sha256_bytes(data["source_bytes"]) == allowed[f"input/sources/{SOURCE_PATH}"]["sha256"], "source hash mismatch")
    for unit, row in zip(data["units"], data["reading"]):
        check(unit["id"] == row["source_unit_id"], "reading/source order mismatch")
        raw = data["source_bytes"][unit["byte_start"] : unit["byte_end"]]
        check(sha256_bytes(raw) == unit["sha256"] == row["unit_sha256"], f"unit hash mismatch: {unit['id']}")
    check([row["asset_id"] for row in data["assets"]] == sorted(row["asset_id"] for row in data["assets"]), "asset order")


def build_output(bundle: Path) -> dict[str, Any]:
    data = load_bundle(bundle)
    validate_bundle(bundle, data)
    manifest = data["manifest"]
    unit_by_id = {unit["id"]: unit for unit in data["units"]}
    ordinal = {unit["id"]: index for index, unit in enumerate(data["units"], 1)}
    asset_by_unit = {row["source_unit_id"]: row for row in data["assets"]}
    candidates = candidate_definitions()

    common_na = {"control_state", "external_data"}
    role_na = {
        "NATIVE": {
            "input",
            "visible_history",
            "witness_semantics",
            "excluded_observers_and_representations",
        },
        "FAMILY": {
            "input",
            "visible_history",
            "witness_semantics",
            "excluded_observers_and_representations",
        },
        "OBSERVER": {
            "boundary",
            "frontier_or_activation",
            "schedule",
            "seed",
            "successor_cardinality",
            "write_replacement_assembly_or_commit",
        },
        "CONSTRAINT": {
            "boundary",
            "frontier_or_activation",
            "read_dependencies_or_neighborhood",
            "schedule",
            "seed",
            "successor_cardinality",
            "visible_history",
            "write_replacement_assembly_or_commit",
        },
        "EMULATION": {
            "boundary",
            "complete_state",
            "frontier_or_activation",
            "native_time",
            "read_dependencies_or_neighborhood",
            "schedule",
            "seed",
            "successor_cardinality",
            "termination_completion_failure",
            "visible_history",
            "witness_semantics",
            "write_replacement_assembly_or_commit",
        },
        "SEED": {
            "control_state",
            "external_data",
            "visible_history",
            "witness_semantics",
        },
    }
    noniterative_seed_na = {
        "frontier_or_activation",
        "read_dependencies_or_neighborhood",
        "schedule",
        "write_replacement_assembly_or_commit",
    }
    for candidate in candidates:
        profile_na = common_na | role_na[candidate["role"]]
        if (
            candidate["role"] == "SEED"
            and candidate["name"] != "nested substitution initial condition for rule 184"
        ):
            profile_na |= noniterative_seed_na
        candidate["na_fields"] = [
            field
            for field in FIELDS
            if field in (set(candidate["na_fields"]) | profile_na)
            and field not in candidate["values"]
            and field not in candidate["conflicting_fields"]
            and field != "evidence_limit"
        ]

    for index, candidate in enumerate(candidates, 1):
        candidate["id"] = f"W{index:04d}"
        candidate["units"] = sorted(set(candidate["units"]), key=ordinal.__getitem__)
        candidate["semantic_units"] = set(candidate["semantic_units"])
        candidate["mechanics_units"] = set(candidate["mechanics_units"])
        candidate["route_units"] = set(candidate["route_units"])
        check(candidate["units"][0] in candidate["semantic_units"], f"{candidate['id']} anchor lacks semantic evidence")
        check(all(unit in unit_by_id for unit in candidate["units"]), f"{candidate['id']} unknown unit")
        check(set(candidate["semantic_units"]) <= set(candidate["units"]), f"{candidate['id']} semantic unit outside units")
        check(candidate["mechanics_units"] <= set(candidate["units"]), f"{candidate['id']} mechanics unit outside units")
        check(candidate["route_units"] <= set(candidate["units"]), f"{candidate['id']} route unit outside units")
        check(
            all(set(units_for_field) <= set(candidate["units"]) for units_for_field in candidate["field_units"].values()),
            f"{candidate['id']} field evidence unit outside units",
        )
        check(
            set(candidate["evidence_overrides"]) <= set(candidate["units"]),
            f"{candidate['id']} evidence override outside units",
        )
        check(
            all(
                set(unit_ids) <= set(candidate["units"])
                for unit_ids in candidate["related_evidence_units"].values()
            ),
            f"{candidate['id']} related-candidate evidence unit outside units",
        )
    check(
        [ordinal[c["units"][0]] for c in candidates] == sorted(ordinal[c["units"][0]] for c in candidates),
        "candidate definitions are not in canonical discovery order",
    )
    candidate_anchor_counts: dict[str, int] = {}
    for candidate in candidates:
        anchor_id = candidate["units"][0]
        candidate_anchor_counts[anchor_id] = candidate_anchor_counts.get(anchor_id, 0) + 1
        candidate["anchor_ordinal"] = candidate_anchor_counts[anchor_id]

    routes: list[dict[str, str]] = []
    route_ids_by_unit: dict[str, list[str]] = {}
    route_anchor_counts: dict[str, int] = {}
    for index, (unit_id, literal, kind, topic, scope, vocabulary) in enumerate(ROUTE_DEFS, 1):
        route_id = f"WR{index:04d}"
        route_anchor_counts[unit_id] = route_anchor_counts.get(unit_id, 0) + 1
        route_ids_by_unit.setdefault(unit_id, []).append(route_id)
        routes.append(
            {
                "route_id": route_id,
                "source_unit_id": unit_id,
                "source_asset_id": "",
                "discovery_epoch": str(EPOCH),
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": unit_id,
                "discovery_ordinal": str(route_anchor_counts[unit_id]),
                "literal_target": literal,
                "route_kind": kind,
                "expected_topic": topic,
                "owning_stage": str(STAGE),
                "closure_scope": scope,
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": "[]",
                "vocabulary_terms": jdump(vocabulary),
                "defect_boundary": "",
            }
        )

    candidate_ids_by_unit: dict[str, list[str]] = {}
    roles_by_unit: dict[str, list[str]] = {}
    for candidate in candidates:
        role_map = {
            "SEED": "SEED_INPUT_OR_BOUNDARY",
            "OBSERVER": "OBSERVER_OR_ANALYZER",
            "EMULATION": "EMULATION",
            "CONSTRAINT": "PROPERTY_OR_RESTRICTION",
            "FAMILY": "PROPERTY_OR_RESTRICTION",
            "NATIVE": "BEHAVIOR_OR_OUTCOME",
        }
        role = role_map[candidate["role"]]
        for unit_id in candidate["units"]:
            candidate_ids_by_unit.setdefault(unit_id, []).append(candidate["id"])
            if role not in roles_by_unit.setdefault(unit_id, []):
                roles_by_unit[unit_id].append(role)
    candidate_by_id = {candidate["id"]: candidate for candidate in candidates}

    # Allocate evidence globally by canonical source occurrence, then candidate ID.
    evidence_allocations: list[tuple[int, str, dict[str, Any], str]] = []
    for candidate in candidates:
        for unit_id in candidate["units"]:
            evidence_allocations.append((ordinal[unit_id], candidate["id"], candidate, unit_id))
    evidence_allocations.sort(key=lambda item: (item[0], item[1]))
    evidence_by_candidate: dict[str, list[dict[str, Any]]] = {candidate["id"]: [] for candidate in candidates}
    evidence_anchor_counts: dict[str, int] = {}
    for evidence_number, (_, _, candidate, unit_id) in enumerate(evidence_allocations, 1):
        unit = unit_by_id[unit_id]
        asset = asset_by_unit.get(unit_id)
        semantic = unit_id in candidate["semantic_units"]
        evidence_anchor_counts[unit_id] = evidence_anchor_counts.get(unit_id, 0) + 1
        override = candidate["evidence_overrides"].get(unit_id, {})
        fields = list(candidate["values"]) if unit_id in candidate["mechanics_units"] else []
        for field, field_unit_ids in candidate["field_units"].items():
            if field not in candidate["values"]:
                continue
            if field in fields and unit_id not in field_unit_ids:
                fields.remove(field)
            if unit_id in field_unit_ids and field not in fields:
                fields.append(field)
        for field in candidate["conflicting_fields"]:
            if unit_id in candidate["semantic_units"] and field not in fields:
                fields.append(field)
        if "fields" in override:
            fields = list(override["fields"])
        check(set(fields) <= set(FIELDS), f"{candidate['id']} evidence uses unknown field")
        check(
            set(fields) <= (set(candidate["values"]) | set(candidate["conflicting_fields"])),
            f"{candidate['id']} evidence supports an undeclared field",
        )
        if candidate["source_status"] == "CONFLICTING":
            strength = "DEFECT_LIMITED"
        elif "strength" in override:
            strength = override["strength"]
        elif unit_id in candidate["mechanics_units"]:
            strength = candidate["strength"]
        elif fields:
            strength = "DIRECT_PARTIAL_MECHANICS"
        elif unit["block_kind"] == "image":
            strength = "CONTEXTUAL"
        else:
            strength = "CORROBORATING"
        if (
            unit["block_kind"] == "image"
            and strength in {"DIRECT_PARTIAL_MECHANICS", "DIRECT_COMPLETE_MECHANICS"}
            and not override.get("allow_direct_image", False)
            and any(
                candidate_by_id[candidate_id]["role"] in {"OBSERVER", "EMULATION", "CONSTRAINT"}
                for candidate_id in candidate_ids_by_unit[unit_id]
            )
        ):
            strength = "CONTEXTUAL"
        if unit["block_kind"] == "image":
            modality = "IMAGE"
        else:
            previous = data["units"][ordinal[unit_id] - 2] if ordinal[unit_id] > 1 else None
            if previous and previous["block_kind"] == "image":
                modality = "CAPTION"
            else:
                raw = data["source_bytes"][unit["byte_start"] : unit["byte_end"]]
                modality = "FORMULA" if b"$" in raw else "PROSE"
        if "claim" in override:
            claim = override["claim"]
        elif unit_id in candidate["mechanics_units"]:
            claim = (
                f"{unit_id} supplies the source-scoped mechanics attributed to {candidate['name']}; "
                "no mechanics outside its listed fingerprint fields are inferred."
            )
        elif fields:
            claim = (
                f"{unit_id} directly supports the listed identity, parameter, structural, or witness fields for "
                f"{candidate['name']}; no unlisted mechanics are inferred."
            )
        elif unit["block_kind"] == "image":
            claim = (
                f"Original-resolution image {asset['physical_path'] if asset else unit_id} is a finite or labeled "
                f"witness for {candidate['name']}; it is not used to infer unlisted mechanics."
            )
        else:
            claim = (
                f"{unit_id} supplies contextual behavior or provenance for {candidate['name']}; "
                "no fingerprint field is attributed to this row."
            )
        evidence_by_candidate[candidate["id"]].append(
            {
                "evidence_id": f"WE{evidence_number:06d}",
                "evidence_group_id": f"WG{evidence_number:06d}",
                "discovery_anchor": {
                    "epoch": EPOCH,
                    "kind": "SOURCE_UNIT",
                    "id": unit_id,
                    "ordinal": evidence_anchor_counts[unit_id],
                },
                "source_unit_id": unit_id,
                "image_path": asset["physical_path"] if asset else None,
                "strength": strength,
                "modality": modality,
                "claim": claim,
                "fingerprint_fields": fields,
            }
        )

    candidate_records: list[dict[str, Any]] = []
    candidate_id_by_name = {candidate["name"]: candidate["id"] for candidate in candidates}
    strength_rank = {
        "DIRECT_COMPLETE_MECHANICS": 6,
        "DIRECT_PARTIAL_MECHANICS": 5,
        "DIRECT_IDENTITY": 4,
        "DEFECT_LIMITED": 3,
        "CORROBORATING": 2,
        "CONTEXTUAL": 1,
        "LEAD_ONLY": 0,
    }
    for candidate in candidates:
        evidence = sorted(evidence_by_candidate[candidate["id"]], key=lambda row: int(row["evidence_id"][2:]))
        profile_anchor = max(
            evidence,
            key=lambda row: (
                strength_rank[row["strength"]],
                bool(
                    {
                        "object_kind",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                    }
                    & set(row["fingerprint_fields"])
                ),
                len(row["fingerprint_fields"]),
                -int(row["evidence_id"][2:]),
            ),
        )
        candidate["values"]["evidence_limit"] = (
            "Review-record boundary: only mechanics stated or directly transcribed in the sealed Chapter 6 "
            "main-text bundle are supported; absent profile mechanics remain unknown, and profile-irrelevant "
            "fields are explicitly not applicable."
        )
        profile_fields = [
            field
            for field in FIELDS
            if field == "evidence_limit" or field in candidate["na_fields"]
        ]
        for field in profile_fields:
            if field not in profile_anchor["fingerprint_fields"]:
                profile_anchor["fingerprint_fields"].append(field)
        profile_anchor["claim"] += (
            " This strongest identity/law anchor also fixes the review-record evidence boundary and "
            "justifies the candidate profile's explicit not-applicable fields."
        )
        evidence_by_unit = {row["source_unit_id"]: row["evidence_id"] for row in evidence}
        evidence_for_field = {
            field: [row["evidence_id"] for row in evidence if field in row["fingerprint_fields"]]
            for field in FIELDS
        }
        fingerprint: dict[str, Any] = {}
        missing: list[str] = []
        for field in FIELDS:
            if field in candidate["conflicting_fields"]:
                status = "CONFLICTING_SOURCE"
                value = None
                reason = candidate["uncertainties"][0]
                ids = evidence_for_field[field]
            elif field in candidate["values"]:
                status = "SUPPORTED"
                value = candidate["values"][field]
                reason = ""
                ids = evidence_for_field[field]
                check(ids, f"{candidate['id']} supported field lacks evidence: {field}")
            elif field in candidate["na_fields"]:
                status = "NOT_APPLICABLE"
                value = None
                reason = (
                    f"The {candidate['role'].lower()} profile for {candidate['name']} has no independent "
                    f"{field.replace('_', ' ')} mechanic beyond its supported identity, input, or law semantics."
                )
                ids = evidence_for_field[field]
                check(len(ids) == 1, f"{candidate['id']} not-applicable field requires one profile anchor: {field}")
            else:
                status = "UNKNOWN_FROM_SOURCE"
                value = None
                reason = f"The source does not determine {field}."
                ids = []
                missing.append(reason)
            fingerprint[field] = {"status": status, "value": value, "evidence_ids": ids, "reason": reason}
        route_ids = []
        for unit_id in candidate["units"]:
            for route_id in route_ids_by_unit.get(unit_id, []):
                if route_id not in route_ids:
                    route_ids.append(route_id)
        all_evidence_ids = [row["evidence_id"] for row in evidence]
        supporting_evidence_ids = [
            row["evidence_id"] for row in evidence if row["fingerprint_fields"]
        ]
        check(supporting_evidence_ids, f"{candidate['id']} has no field-supporting evidence")
        image_witnesses = [
            asset_by_unit[unit_id]["physical_path"]
            for unit_id in candidate["units"]
            if unit_id in asset_by_unit
        ]
        candidate_records.append(
            {
                "id": candidate["id"],
                "record_status": "ACTIVE",
                "provisional_name": candidate["name"],
                "aliases": candidate["aliases"],
                "discovery_stage": STAGE,
                "discovery_anchor": {
                    "epoch": EPOCH,
                    "kind": "SOURCE_UNIT",
                    "id": candidate["units"][0],
                    "ordinal": candidate["anchor_ordinal"],
                },
                "source_unit_ids": candidate["units"],
                "source_evidence": evidence,
                "source_status": candidate.get(
                    "source_statuses",
                    [candidate["source_status"]],
                ),
                "image_witnesses": image_witnesses,
                "evidence_strength": list(dict.fromkeys(row["strength"] for row in evidence)),
                "field_support": {field: fingerprint[field]["status"] for field in FIELDS},
                "fingerprint": fingerprint,
                "parameters": [
                    {
                        "name": name,
                        "source_description": f"Source parameter for {candidate['name']}.",
                        "evidence_ids": supporting_evidence_ids,
                    }
                    for name in candidate["parameters"]
                ],
                "variants": [
                    {
                        "name": name,
                        "source_description": f"Source-delimited variant of {candidate['name']}.",
                        "evidence_ids": [
                            evidence_by_unit[unit_id]
                            for unit_id in candidate["variant_units"].get(name, [])
                        ]
                        or supporting_evidence_ids,
                    }
                    for name in candidate["variants"]
                ],
                "missing_mechanics": missing,
                "uncertainties": candidate["uncertainties"],
                "related_candidate_ids": [
                    {
                        "candidate_id": candidate_id_by_name[name],
                        "relation": "SOURCE_COMPARE",
                        "proof_kind": "PROVISIONAL_COMPARISON",
                        "evidence_ids": [
                            evidence_by_unit[unit_id]
                            for unit_id in candidate["related_evidence_units"].get(name, [])
                        ]
                        or supporting_evidence_ids,
                        "before_rationale": "",
                        "after_rationale": "",
                        "uncertainty": (
                            "The source states this semantic connection, but the blind review does not assert "
                            "identity or equivalence beyond the cited mechanics."
                        ),
                    }
                    for name in candidate["related_names"]
                ],
                "cross_reference_ids": route_ids,
                "evidence_reassignments": [],
            }
        )

    conflict_units = {"U001513", "U001514", "U001515"}
    historical_fragments = ("first developed", "originally discovered", "some seventeen years")
    reading_updates: list[dict[str, str]] = []
    for input_row, unit in zip(data["reading"], data["units"]):
        unit_id = input_row["source_unit_id"]
        row = dict(input_row)
        ids = candidate_ids_by_unit.get(unit_id, [])
        route_ids = route_ids_by_unit.get(unit_id, [])
        roles = list(roles_by_unit.get(unit_id, []))
        raw_text = data["source_bytes"][unit["byte_start"] : unit["byte_end"]].decode("utf-8")
        if unit_id in conflict_units:
            disposition = "SOURCE_DEFECT_OR_AMBIGUITY"
            source_status = "CONFLICTING"
            uncertainty = (
                "Adjacent-black constraint conflict: U001513 forbids a black pair while U001515 says black cells "
                "are only allowed in pairs; the image cannot decide the intended language."
            )
            if "SOURCE_DEFECT" not in roles:
                roles.append("SOURCE_DEFECT")
            statement = uncertainty
        elif ids:
            anchors = [c["units"][0] for c in candidates if c["id"] in ids]
            disposition = "CANDIDATE" if unit_id in anchors else "SUPPORTS_CANDIDATE"
            source_status = "CLEAR"
            uncertainty = ""
            statement = f"Source-limited evidence for {jdump(ids)}; finite rendered examples remain witnesses rather than stochastic laws."
        elif route_ids:
            disposition = "CROSS_REFERENCE"
            source_status = "CLEAR"
            uncertainty = ""
            roles.append("EXTERNAL_ONLY")
            statement = f"Construction-relevant target recorded as {jdump(route_ids)} without blind-worker resolution."
        elif unit_id == "U001337":
            disposition = "NO_CONSTRUCTION"
            source_status = "CLEAR"
            uncertainty = ""
            roles.append("IMPLEMENTATION_DETAIL")
            statement = "Editorial source-accounting comment points to a legacy raster of the following live caption."
        elif unit["block_kind"] == "image":
            disposition = "REPRESENTATION_OR_OBSERVER"
            source_status = "CLEAR"
            uncertainty = ""
            roles.extend(["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"])
            statement = "Original-resolution image is a finite realization, control, or summary; it does not by itself define an ensemble or new native law."
        elif any(fragment in raw_text for fragment in historical_fragments):
            disposition = "HISTORICAL_ONLY"
            source_status = "CLEAR"
            uncertainty = ""
            roles.append("HISTORICAL_MENTION")
            statement = "Historical provenance is recorded without an independent native construction."
        else:
            disposition = "NO_CONSTRUCTION"
            source_status = "CLEAR"
            uncertainty = ""
            if unit["block_kind"] != "heading":
                roles.append("BEHAVIOR_OR_OUTCOME")
            statement = "Complete in-context reading yields behavior, motivation, or property discussion but no independent source-defined construction."
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": str(EPOCH),
                "review_disposition": disposition,
                "source_status": source_status,
                "uncertainty": uncertainty,
                "secondary_roles": jdump(list(dict.fromkeys(roles))),
                "candidate_ids": jdump(ids),
                "route_ids": jdump(route_ids),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": WORKER_ID,
            }
        )
        reading_updates.append(row)

    observer_candidate_ids = {
        candidate["id"]
        for candidate in candidates
        if candidate["role"] in {"OBSERVER"}
    }
    relation_candidate_ids = {
        candidate["id"]
        for candidate in candidates
        if candidate["role"] in {"EMULATION", "CONSTRAINT"}
    }
    asset_review_overrides: dict[str, dict[str, str]] = {
        "A000924": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": (
                "Original-resolution rule-254 transition table checked in BBB,BBW,BWB,BWW,WBB,WBW,WWB,WWW "
                "order: B,B,B,B,B,B,B,W."
            ),
        },
        "A000926": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": (
                "Original-resolution ordered transition tables checked for rules 0,32,160,250; the "
                "random-start evolutions remain behavior witnesses."
            ),
        },
        "A000927": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": (
                "Original-resolution ordered transition tables checked for rules 4,108,218,232; the "
                "random-start evolutions remain behavior witnesses."
            ),
        },
        "A000929": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": (
                "Original-resolution rule-126 transition table checked in BBB,BBW,BWB,BWW,WBB,WBW,WWB,WWW "
                "order: W,B,B,B,B,B,B,W."
            ),
        },
        "A000941": {
            "evidence_statement": (
                "Original-resolution labeled survey inventory: rules "
                "0,4,18,22,32,36,50,54,72,76,90,94,104,108,122,126,"
                "128,132,146,150,160,164,178,182,200,204,218,222,232,236,250,254."
            )
        },
        "A000942": {
            "evidence_statement": "Original-resolution labeled inventory: every even totalistic code from 0 through 62 inclusive."
        },
        "A000943": {
            "evidence_statement": "Original-resolution labeled inventory: three-color totalistic codes 1002 through 1095 in increments of 3."
        },
        "A000948": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution borderline-classifier panel labeled code 219; source caption permits class 2 or class 4.",
        },
        "A000949": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution borderline-classifier panel labeled code 438; source caption permits class 3 or class 4.",
        },
        "A000950": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution borderline-classifier panel labeled code 1380; source caption permits class 2 or class 3.",
        },
        "A000951": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution borderline-classifier panel labeled code 1632; source caption permits class 1, 2, or 3.",
        },
        "A000952": {
            "evidence_statement": "Original-resolution labeled inventory: four-color totalistic codes 1000816 through 1000940 in increments of 4."
        },
        "A000954": {
            "visual_role": "OBSERVER",
            "evidence_statement": (
                "Original-resolution continuous-cellular-automaton evolution rendered through the "
                "neighbor-difference gray display stated for all three page-259 pictures; it remains "
                "linked to its native law but is observer output."
            ),
        },
        "A000955": {
            "visual_role": "OBSERVER",
            "evidence_statement": (
                "Original-resolution continuous-cellular-automaton evolution rendered through the "
                "neighbor-difference gray display stated for all three page-259 pictures; it remains "
                "linked to its native law but is observer output."
            ),
        },
        "A000956": {
            "visual_role": "OBSERVER",
            "evidence_statement": (
                "Original-resolution weighted continuous-cellular-automaton evolution rendered through the "
                "neighbor-difference gray display; it is a finite observer witness, not native-state or "
                "transition-law evidence."
            ),
        },
        "A000957": {
            "evidence_statement": "Original-resolution native-family step survey labeled codes 4,12,24,30,38,52 at steps 1,2,5,100,500."
        },
        "A000958": {
            "evidence_statement": "Original-resolution broader two-dimensional survey labeled every even code from 2 through 60 inclusive."
        },
        "A000959": {
            "visual_role": "OBSERVER",
            "evidence_statement": (
                "Original-resolution one-dimensional slice/spatial-depth-fog observer output labeled "
                "codes 4,12,24,30,38,52."
            ),
        },
        "A000975": {
            "visual_role": "CONTROL",
            "evidence_statement": "Original-resolution finite cyclic evolution/control inventory labeled rule 90 and rule 30.",
        },
        "A000976": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution period-versus-size observer curves labeled rules 90,30,45,110 with a 2^n reference bound.",
        },
        "A000986": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": (
                "Original-resolution rule-30 transition table checked in BBB,BBW,BWB,BWW,WBB,WBW,WWB,WWW "
                "order: W,W,W,B,B,B,B,W."
            ),
        },
        "A001002": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": "Original-resolution rule-184 transition-table strip checked as native local-law evidence, not substitution-seed evidence.",
        },
        "A001005": {
            "visual_role": "NATIVE_EVIDENCE",
            "evidence_statement": (
                "Original-resolution rule-table/attractor panel: top rule 255 table maps all eight binary "
                "nearest-neighbor triples to black; lower rule 4 table and attractor are separately labeled."
            ),
        },
        "A001010": {
            "visual_role": "RELATION",
            "evidence_statement": "Original-resolution surjective/onto mapping example inventory labeled rules 204,240,30,90.",
        },
        "A001018": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution code-357 brute-force persistent-structure result catalog; not native-law evidence.",
        },
        "A001019": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution code-1329 persistent-structure search-result catalog; not native-law evidence.",
        },
        "A001020": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution code-1329 unbounded-growth bounded-search result; not native-law evidence.",
        },
        "A001021": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution code-1329 simple/complex unbounded-growth search results; not native-law evidence.",
        },
        "A001022": {
            "visual_role": "CONTROL",
            "evidence_statement": "Original-resolution rule-110 random-background witness showing the periodic environment; not native-law evidence.",
        },
        "A001023": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution rule-110 persistent-structure catalog with labels and extensions; not native-law evidence.",
        },
        "A001024": {
            "visual_role": "OBSERVER",
            "evidence_statement": "Original-resolution rule-110 width-41 unbounded-growth bounded-search result; not native-law evidence.",
        },
        "A001025": {
            "visual_role": "RELATION",
            "evidence_statement": "Original-resolution rule-110 collision/spacing relation for structures o and j; not native-law evidence.",
        },
        "A001026": {
            "visual_role": "RELATION",
            "evidence_statement": "Original-resolution rule-110 collision relation for structures e and o; not native-law evidence.",
        },
        "A001027": {
            "visual_role": "RELATION",
            "evidence_statement": "Original-resolution greater-than-4000-step rule-110 collision relation producing eight structures; not native-law evidence.",
        },
    }
    asset_updates: list[dict[str, str]] = []
    for input_row in data["assets"]:
        row = dict(input_row)
        unit_id = row["source_unit_id"]
        ids = candidate_ids_by_unit.get(unit_id, [])
        route_ids = route_ids_by_unit.get(unit_id, [])
        if unit_id == "U001514":
            visual_role = "SOURCE_DEFECT"
            source_status = "CONFLICTING"
            risk = ["CONSTRUCTION_BEARING", "TEXT_BEARING", "AMBIGUOUS", "CAPTION_INCOMPLETE"]
            uncertainty = (
                "The image does not resolve whether the adjacent prose's no-pair constraint or the following "
                "caption's pairs-only constraint is intended."
            )
            evidence_statement = uncertainty
        elif row["physical_path"].endswith("_page_238_Chapter_Opener.jpeg"):
            visual_role = "DECORATIVE"
            source_status = "CLEAR"
            risk = []
            uncertainty = ""
            evidence_statement = "Chapter opener screened at original pixels; decorative chapter identification only."
        elif unit_id == "U001337":
            visual_role = "RELATION"
            source_status = "CLEAR"
            risk = ["TEXT_BEARING", "CAPTION_INCOMPLETE"]
            uncertainty = ""
            evidence_statement = (
                "Legacy raster caption checked at original pixels against the live U001341 transcription; it adds "
                "no mechanics beyond that caption."
            )
        elif any(candidate_id in observer_candidate_ids for candidate_id in ids):
            visual_role = "OBSERVER"
            source_status = "CLEAR"
            risk = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            uncertainty = ""
            evidence_statement = "Original-pixel observer or query diagram checked, including its labels and finite-result status."
        elif any(candidate_id in relation_candidate_ids for candidate_id in ids):
            visual_role = "RELATION"
            source_status = "CLEAR"
            risk = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            uncertainty = ""
            evidence_statement = "Original-pixel relation, constraint, block map, or attractor witness checked against adjacent prose."
        elif ids:
            visual_role = "NATIVE_EVIDENCE"
            source_status = "CLEAR"
            risk = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            uncertainty = ""
            evidence_statement = (
                "Original-pixel rule table, labeled preset, initial state, or evolution witness checked; it is not "
                "promoted beyond the mechanics stated by the bundle."
            )
        else:
            visual_role = "CONTROL"
            source_status = "CLEAR"
            risk = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            uncertainty = ""
            evidence_statement = (
                "Original-pixel finite realization or comparison panel checked; it is treated as a control or "
                "behavioral witness, not as a probability law or ensemble definition."
            )
        if row["asset_id"] in asset_review_overrides:
            override = asset_review_overrides[row["asset_id"]]
            visual_role = override.get("visual_role", visual_role)
            evidence_statement = override.get("evidence_statement", evidence_statement)
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": str(EPOCH),
                "visual_role": visual_role,
                "source_status": source_status,
                "risk_flags": jdump(risk),
                "original_resolution_status": "REVIEWED",
                "transcription_status": "NOT_REQUIRED" if not risk else "CHECKED",
                "candidate_ids": jdump(ids),
                "route_ids": jdump(route_ids),
                "evidence_statement": evidence_statement,
                "review_stage": str(STAGE),
                "reviewer": WORKER_ID,
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append(row)

    output = {
        "worker_id": WORKER_ID,
        "bundle_sha256": manifest["content_set_sha256"],
        "prompt_sha256": manifest["prompt_sha256"],
        "schema_sha256": manifest["schema_sha256"],
        "allowed_manifest_sha256": data["manifest_sha"],
        "prohibited_input_nonuse": True,
        "reading_updates": reading_updates,
        "candidate_proposals": candidate_records,
        "asset_updates": asset_updates,
        "route_proposals": routes,
        "uncertainties": [
            "The Chapter 6 main text does not state exact probabilities or independence for its random initial-condition generators.",
            "U001513 and U001515 give contradictory adjacent-black constraints; the owned image does not resolve them.",
            "Several cellular-automaton presets are code-identified or image-transcribed while their complete code scheme is cross-referenced.",
            "The neighbor-difference display omits neighbor direction, difference convention, and gray remapping; the prior-time trail omits retained depth and its age-to-shade map.",
            "Several self-emulation block codecs are image-borne, and their prose supplies only the stated block widths or qualitative correspondence.",
            "The source states rule-90 superposition consequences but does not define the algebraic superposition operator in this range.",
            "The finite-period discussion gives bounds and measurements but no general computation algorithm; brute-force persistent-structure searches omit a universal stopping or equivalence-deduplication rule.",
            "The localized integer seed codec leaves digit orientation, leading zeros, and surrounding blank-background conventions unresolved.",
            "The general allowed-sequence network construction and systematic fixed-period structure procedure are not fully stated in this range.",
        ],
    }
    verify_output(bundle, output)
    return output


def verify_output(bundle: Path, output: dict[str, Any]) -> None:
    data = load_bundle(bundle)
    validate_bundle(bundle, data)
    check(output["worker_id"] == WORKER_ID, "output worker mismatch")
    check(output["bundle_sha256"] == data["manifest"]["content_set_sha256"], "bundle declaration mismatch")
    check(output["prompt_sha256"] == data["manifest"]["prompt_sha256"], "prompt declaration mismatch")
    check(output["schema_sha256"] == data["manifest"]["schema_sha256"], "schema declaration mismatch")
    check(output["allowed_manifest_sha256"] == data["manifest_sha"], "manifest declaration mismatch")
    check(output["prohibited_input_nonuse"] is True, "prohibited-input declaration must be true")
    check(len(output["reading_updates"]) == 354, "reading output count")
    check(len(output["asset_updates"]) == 105, "asset output count")
    check(len(output["candidate_proposals"]) == EXPECTED_CANDIDATE_COUNT, "candidate output count")
    check(len(output["route_proposals"]) == 35, "route output count")
    check(
        [row["source_unit_id"] for row in output["reading_updates"]]
        == [row["source_unit_id"] for row in data["reading"]],
        "reading allocation/order mismatch",
    )
    check(
        [row["asset_id"] for row in output["asset_updates"]] == [row["asset_id"] for row in data["assets"]],
        "asset allocation/order mismatch",
    )
    for before, after in zip(data["reading"], output["reading_updates"]):
        immutable = [
            "source_unit_id",
            "document_order",
            "path",
            "block_kind",
            "byte_start",
            "byte_end",
            "line_start",
            "line_end",
            "global_line_start",
            "global_line_end",
            "unit_sha256",
        ]
        check(all(before[key] == after[key] for key in immutable), f"reading immutable mismatch: {after['source_unit_id']}")
        check(after["review_status"] == "REVIEWED" and after["review_epoch"] == "2", "reading status mismatch")
        check(after["source_status"] == "CLEAR" or after["uncertainty"], "reading uncertainty contract")
    for before, after in zip(data["assets"], output["asset_updates"]):
        immutable = [
            "asset_id",
            "link_id",
            "physical_path",
            "sha256",
            "bytes",
            "source_path",
            "source_unit_id",
            "assignment_path",
            "assignment_stage",
            "assignment_basis",
            "reference_status",
        ]
        check(all(before[key] == after[key] for key in immutable), f"asset immutable mismatch: {after['asset_id']}")
        check(after["inspection_status"] == "SCREENED" and after["review_epoch"] == "2", "asset status mismatch")
        check(after["original_resolution_status"] == "REVIEWED", "all 105 images must be original-pixel reviewed")
        check(after["source_status"] == "CLEAR" or after["uncertainty"], "asset uncertainty contract")
    candidate_ids = [row["id"] for row in output["candidate_proposals"]]
    check(
        candidate_ids == [f"W{i:04d}" for i in range(1, EXPECTED_CANDIDATE_COUNT + 1)],
        "candidate ID sequence",
    )
    candidate_by_id = {row["id"]: row for row in output["candidate_proposals"]}
    rule110_unit = next(
        row
        for row in candidate_by_id["W0012"]["source_evidence"]
        if row["source_unit_id"] == "U001560"
    )
    rule110_na_fields = {
        field
        for field, item in candidate_by_id["W0012"]["fingerprint"].items()
        if item["status"] == "NOT_APPLICABLE"
    }
    check(
        set(rule110_unit["fingerprint_fields"])
        - rule110_na_fields
        - {"evidence_limit"}
        == {
            "object_kind",
            "carrier",
            "alphabet_or_value_schema",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "parameters_and_variants",
        },
        "rule-110 identity prose must not acquire generic CA mechanics",
    )
    check(
        rule110_unit["strength"] == "DIRECT_PARTIAL_MECHANICS",
        "rule-110 identity/mechanics prose must be scoped as direct partial mechanics",
    )
    for candidate_id in ("W0017", "W0018", "W0019", "W0020"):
        panel_na_fields = {
            field
            for field, item in candidate_by_id[candidate_id]["fingerprint"].items()
            if item["status"] == "NOT_APPLICABLE"
        }
        panel_intro = next(
            row
            for row in candidate_by_id[candidate_id]["source_evidence"]
            if row["source_unit_id"] == "U001285"
        )
        check(
            {
                "complete_state",
                "frontier_or_activation",
                "schedule",
                "write_replacement_assembly_or_commit",
                "successor_cardinality",
                "determinism_branching_or_measure",
            }
            <= set(panel_intro["fingerprint_fields"]),
            f"{candidate_id} class-4 native successor mechanics missing",
        )
        check(
            not {"seed", "termination_completion_failure"}
            & (set(panel_intro["fingerprint_fields"]) - panel_na_fields),
            f"{candidate_id} class-4 random run contaminates native profile",
        )
    asset_by_id = {row["asset_id"]: row for row in output["asset_updates"]}
    for asset_id in ("A000954", "A000955", "A000956"):
        check(
            asset_by_id[asset_id]["visual_role"] == "OBSERVER",
            f"{asset_id} neighbor-difference rendering role",
        )
    exact_native_tables = {
        "W0002": "B, B, B, B, B, B, B, W",
        "W0003": "rule 250 -> B,B,B,B,B,W,B,W",
        "W0004": "rule 232 -> B,B,B,W,B,W,W,W",
        "W0005": "W, B, B, B, B, B, B, W",
        "W0007": "W, W, W, B, B, B, B, W",
    }
    for candidate_id, expected_table_fragment in exact_native_tables.items():
        check(
            expected_table_fragment
            in candidate_by_id[candidate_id]["fingerprint"][
                "rule_relation_constraint_function_or_probability_law"
            ]["value"],
            f"{candidate_id} exact ordered native table missing",
        )
    rule110 = candidate_by_id["W0012"]
    rule110_evidence_by_id = {
        row["evidence_id"]: row["source_unit_id"]
        for row in rule110["source_evidence"]
    }
    check(not rule110["variants"], "rule 110 experiments must not be native variants")
    check(
        {
            rule110_evidence_by_id[evidence_id]
            for evidence_id in rule110["fingerprint"]["parameters_and_variants"][
                "evidence_ids"
            ]
        }
        == {"U001256", "U001558", "U001560"},
        "rule-110 code parameter evidence scope",
    )
    for candidate_id in ("W0017", "W0018", "W0019", "W0020"):
        check(
            not candidate_by_id[candidate_id]["variants"],
            f"{candidate_id} singleton code must not be a variant",
        )
        check(
            candidate_by_id[candidate_id]["fingerprint"]["seed"]["status"]
            == "NOT_APPLICABLE",
            f"{candidate_id} random run must not become native seed",
        )
    check(
        not candidate_by_id["W0023"]["parameters"],
        "neighbor-difference unresolved conventions must not be top-level parameters",
    )
    search_units = set(candidate_by_id["W0056"]["source_unit_ids"])
    check(
        {
            "U001542",
            "U001543",
            "U001544",
            "U001545",
            "U001546",
            "U001548",
            "U001549",
            "U001550",
            "U001551",
            "U001552",
            "U001553",
            "U001554",
            "U001555",
            "U001556",
            "U001562",
            "U001563",
            "U001567",
            "U001568",
            "U001569",
            "U001570",
        }
        <= search_units,
        "expanded bounded-search instance coverage",
    )
    for asset_id in ("A001018", "A001019", "A001020", "A001021", "A001023", "A001024"):
        check(
            asset_by_id[asset_id]["visual_role"] == "OBSERVER"
            and "W0056" in json.loads(asset_by_id[asset_id]["candidate_ids"]),
            f"{asset_id} bounded-search reverse join",
        )
    route_ids = [row["route_id"] for row in output["route_proposals"]]
    check(route_ids == [f"WR{i:04d}" for i in range(1, 36)], "route ID sequence")
    check(
        next(
            row
            for row in output["route_proposals"]
            if row["literal_target"] == "later in this book"
        )["source_unit_id"]
        == "U001358",
        "later-in-book route source",
    )
    check(all(row["status"] == "PENDING" for row in output["route_proposals"]), "worker routes must remain pending")
    evidence = sorted(
        (record for candidate in output["candidate_proposals"] for record in candidate["source_evidence"]),
        key=lambda row: int(row["evidence_id"][2:]),
    )
    check(
        sum("evidence_limit" in row["fingerprint_fields"] for row in evidence)
        == EXPECTED_CANDIDATE_COUNT,
        "record-level evidence_limit must use exactly one profile anchor per candidate",
    )
    check(
        all(
            candidate["fingerprint"]["evidence_limit"]["status"] == "SUPPORTED"
            and len(candidate["fingerprint"]["evidence_limit"]["evidence_ids"]) == 1
            for candidate in output["candidate_proposals"]
        ),
        "record-level evidence_limit must be supported by one strongest identity/law anchor",
    )
    check(
        all(
            any(value["status"] == "NOT_APPLICABLE" for value in candidate["fingerprint"].values())
            for candidate in output["candidate_proposals"]
        ),
        "every candidate profile must adjudicate at least one not-applicable field",
    )
    check(
        [row["evidence_id"] for row in evidence] == [f"WE{i:06d}" for i in range(1, len(evidence) + 1)],
        "evidence ID sequence",
    )
    check(
        [row["evidence_group_id"] for row in evidence] == [f"WG{i:06d}" for i in range(1, len(evidence) + 1)],
        "evidence-group ID sequence",
    )
    unit_order = {row["source_unit_id"]: index for index, row in enumerate(data["reading"], 1)}
    candidate_anchor_ordinals: dict[str, list[int]] = {}
    candidate_anchor_keys: list[tuple[int, int]] = []
    for candidate in output["candidate_proposals"]:
        anchor = candidate["discovery_anchor"]
        candidate_anchor_ordinals.setdefault(anchor["id"], []).append(anchor["ordinal"])
        candidate_anchor_keys.append((unit_order[anchor["id"]], anchor["ordinal"]))
    check(candidate_anchor_keys == sorted(candidate_anchor_keys), "candidate anchor order")
    check(
        all(values == list(range(1, len(values) + 1)) for values in candidate_anchor_ordinals.values()),
        "candidate anchor ordinal sequence",
    )
    evidence_anchor_ordinals: dict[str, list[int]] = {}
    evidence_anchor_keys: list[tuple[int, int]] = []
    for row in evidence:
        anchor = row["discovery_anchor"]
        evidence_anchor_ordinals.setdefault(anchor["id"], []).append(anchor["ordinal"])
        evidence_anchor_keys.append((unit_order[anchor["id"]], anchor["ordinal"]))
    check(evidence_anchor_keys == sorted(evidence_anchor_keys), "evidence anchor order")
    check(
        all(sorted(values) == list(range(1, len(values) + 1)) for values in evidence_anchor_ordinals.values()),
        "evidence anchor ordinal sequence",
    )
    route_anchor_ordinals: dict[str, list[int]] = {}
    route_anchor_keys: list[tuple[int, int]] = []
    for route in output["route_proposals"]:
        anchor_id = route["discovery_id"]
        anchor_ordinal = int(route["discovery_ordinal"])
        route_anchor_ordinals.setdefault(anchor_id, []).append(anchor_ordinal)
        route_anchor_keys.append((unit_order[anchor_id], anchor_ordinal))
        check(route["target_unit_ids"] == "[]" and route["target_asset_ids"] == "[]", "pending route targets")
        check(route["attempts"] == "[]" and route["defect_boundary"] == "", "pending route closure state")
    check(route_anchor_keys == sorted(route_anchor_keys), "route anchor order")
    check(
        all(values == list(range(1, len(values) + 1)) for values in route_anchor_ordinals.values()),
        "route anchor ordinal sequence",
    )
    allowed_candidate_ids = set(candidate_ids)
    allowed_route_ids = set(route_ids)
    for row in output["reading_updates"]:
        check(set(json.loads(row["candidate_ids"])) <= allowed_candidate_ids, "unknown reading candidate link")
        check(set(json.loads(row["route_ids"])) <= allowed_route_ids, "unknown reading route link")
    for row in output["asset_updates"]:
        check(set(json.loads(row["candidate_ids"])) <= allowed_candidate_ids, "unknown asset candidate link")
        check(set(json.loads(row["route_ids"])) <= allowed_route_ids, "unknown asset route link")
    for candidate in output["candidate_proposals"]:
        check(set(candidate["fingerprint"]) == set(FIELDS), f"{candidate['id']} fingerprint key set")
        check(set(candidate["field_support"]) == set(FIELDS), f"{candidate['id']} field-support key set")
        for field, record in candidate["fingerprint"].items():
            check(record["status"] == candidate["field_support"][field], f"{candidate['id']} field mirror")
            if record["status"] == "UNKNOWN_FROM_SOURCE":
                check(record["reason"] in candidate["missing_mechanics"], f"{candidate['id']} missing-mechanics mirror")
        check(set(candidate["cross_reference_ids"]) <= allowed_route_ids, f"{candidate['id']} unknown route")


def canonical_bytes(output: dict[str, Any]) -> bytes:
    return (json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path("/tmp/goal4-stage10-main"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output_path = args.output or args.bundle / "output/output.json"
    if args.verify:
        output = json.loads(output_path.read_text(encoding="utf-8"))
        verify_output(args.bundle, output)
        print(
            f"PASS worker={WORKER_ID} units={len(output['reading_updates'])} "
            f"assets={len(output['asset_updates'])} candidates={len(output['candidate_proposals'])} "
            f"evidence={sum(len(c['source_evidence']) for c in output['candidate_proposals'])} "
            f"routes={len(output['route_proposals'])} sha256={sha256_bytes(canonical_bytes(output))}"
        )
        return 0
    output = build_output(args.bundle)
    raw = canonical_bytes(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(raw)
    print(
        f"WROTE {output_path} units={len(output['reading_updates'])} assets={len(output['asset_updates'])} "
        f"candidates={len(output['candidate_proposals'])} "
        f"evidence={sum(len(c['source_evidence']) for c in output['candidate_proposals'])} "
        f"routes={len(output['route_proposals'])} sha256={sha256_bytes(raw)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
