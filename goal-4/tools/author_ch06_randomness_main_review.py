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
from pathlib import Path
from typing import Any


WORKER_ID = "ch06-main"
STAGE = 10
EPOCH = 2
SOURCE_PATH = "CHAPTERS/06-Starting-from-Randomness.md"

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
            }
        )

    add(
        "random black-or-white cellular-automaton initial-condition generator",
        ["U001227", "U001416", "U001421"],
        ["U001227", "U001416", "U001421"],
        seed_values(
            "stochastic initial-condition generator",
            carrier="the cells of a cellular-automaton initial row",
            alphabet="black or white",
            law="choose the color of every cell at random; later examples vary the black-cell density",
            result="a complete black-or-white initial cell configuration",
            determinism="stochastic; the source does not state independence or exact probabilities in this range",
        ),
        aliases=["completely random initial conditions", "random initial conditions"],
        role="SEED",
        parameters=["black-cell density"],
        variants=["typical random initial condition", "low-density random initial condition"],
        uncertainties=[
            "The main text does not state an exact probability, independence condition, support extent, or random-bit source."
        ],
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
        "rule-4 isolated-black attractor and basin relation",
        ["U001485", "U001486", "U001488", "U001489", "U001490", "U001491"],
        ["U001485", "U001486", "U001488", "U001489", "U001491"],
        relation_values(
            "attractor-set and basin relation",
            carrier="binary cellular-automaton configurations",
            input_value="a rule-4 initial configuration",
            law=(
                "after one step the attractor consists of configurations in which every black cell has at least "
                "one white cell on each side; multiple initial configurations can map to the same attractor state"
            ),
            result="an allowed attractor configuration together with its basin membership",
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
        ["U001519", "U001532", "U001533", "U001534", "U001535", "U001536", "U001537", "U001538", "U001539", "U001540"],
        ["U001519", "U001533", "U001534", "U001536", "U001537", "U001538", "U001540"],
        relation_values(
            "enumeration and constraint query",
            carrier="finite cellular-automaton initial blocks and their evolutions",
            input_value="a cellular-automaton rule, an enumeration bound or repetition period, and candidate finite blocks",
            law=(
                "enumerate initial-condition numbers and test whether evolution dies out or yields a fixed or moving "
                "persistent structure; a separate systematic period-bounded method is only cross-referenced"
            ),
            result="persistent structures found within the stated enumeration or all structures for a stated small period",
        ),
        aliases=["persistent structure search"],
        role="OBSERVER",
        uncertainties=["The complete systematic period-bounded procedure is not stated here and is routed to page 268."],
    )
    add(
        "three-color nearest-neighbor cellular automaton code 357",
        ["U001527", "U001528", "U001543", "U001544", "U001545", "U001546"],
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
        ["U001529", "U001530", "U001549", "U001550", "U001551", "U001552", "U001553", "U001554", "U001555", "U001556"],
        ["U001529", "U001530", "U001550", "U001553", "U001556"],
        ca_values(
            "code 1329",
            colors="three cell colors",
            neighborhood="nearest neighbors",
        ),
        aliases=["code 1329 cellular automaton"],
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
    ("U001359", "later in this book", "OTHER", "information handling in systems in nature", "CROSS_RANGE", ["information handling"]),
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

    for index, candidate in enumerate(candidates, 1):
        candidate["id"] = f"W{index:04d}"
        candidate["units"] = sorted(set(candidate["units"]), key=ordinal.__getitem__)
        candidate["semantic_units"] = set(candidate["semantic_units"])
        check(candidate["units"][0] in candidate["semantic_units"], f"{candidate['id']} anchor lacks semantic evidence")
        check(all(unit in unit_by_id for unit in candidate["units"]), f"{candidate['id']} unknown unit")
        check(set(candidate["semantic_units"]) <= set(candidate["units"]), f"{candidate['id']} semantic unit outside units")
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
        if candidate["source_status"] == "CONFLICTING":
            strength = "DEFECT_LIMITED"
        elif semantic:
            strength = candidate["strength"]
        elif unit["block_kind"] == "image":
            strength = "CONTEXTUAL"
        else:
            strength = "CORROBORATING"
        if (
            unit["block_kind"] == "image"
            and strength in {"DIRECT_PARTIAL_MECHANICS", "DIRECT_COMPLETE_MECHANICS"}
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
        fields = list(candidate["values"]) if semantic else []
        for field in candidate["conflicting_fields"]:
            if field not in fields:
                fields.append(field)
        if "evidence_limit" not in fields:
            fields.append("evidence_limit")
        claim_prefix = "Direct source evidence" if semantic else "Corroborating source context"
        if unit["block_kind"] == "image":
            claim_prefix = "Original-resolution image evidence"
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
                "claim": f"{claim_prefix} for {candidate['name']}: {candidate['values']['rule_relation_constraint_function_or_probability_law']}",
                "fingerprint_fields": fields,
            }
        )

    candidate_records: list[dict[str, Any]] = []
    for candidate in candidates:
        evidence = sorted(evidence_by_candidate[candidate["id"]], key=lambda row: int(row["evidence_id"][2:]))
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
                reason = f"The {field} field is not applicable to this source-defined object."
                ids = []
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
                "source_status": [candidate["source_status"]],
                "image_witnesses": image_witnesses,
                "evidence_strength": list(dict.fromkeys(row["strength"] for row in evidence)),
                "field_support": {field: fingerprint[field]["status"] for field in FIELDS},
                "fingerprint": fingerprint,
                "parameters": [
                    {
                        "name": name,
                        "source_description": f"Source parameter for {candidate['name']}.",
                        "evidence_ids": all_evidence_ids,
                    }
                    for name in candidate["parameters"]
                ],
                "variants": [
                    {
                        "name": name,
                        "source_description": f"Source-delimited variant of {candidate['name']}.",
                        "evidence_ids": all_evidence_ids,
                    }
                    for name in candidate["variants"]
                ],
                "missing_mechanics": missing,
                "uncertainties": candidate["uncertainties"],
                "related_candidate_ids": [],
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
    check(len(output["candidate_proposals"]) == 47, "candidate output count")
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
    check(candidate_ids == [f"W{i:04d}" for i in range(1, 48)], "candidate ID sequence")
    route_ids = [row["route_id"] for row in output["route_proposals"]]
    check(route_ids == [f"WR{i:04d}" for i in range(1, 36)], "route ID sequence")
    check(all(row["status"] == "PENDING" for row in output["route_proposals"]), "worker routes must remain pending")
    evidence = sorted(
        (record for candidate in output["candidate_proposals"] for record in candidate["source_evidence"]),
        key=lambda row: int(row["evidence_id"][2:]),
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
