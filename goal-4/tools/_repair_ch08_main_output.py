#!/usr/bin/env python3
"""One-shot semantic repair for the sealed ch08-main Stage 12 review."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def evidence(
    evidence_id: str,
    source_unit_id: str,
    strength: str,
    modality: str,
    claim: str,
    image_path: str | None = None,
) -> dict[str, Any]:
    return {
        "evidence_id": evidence_id,
        "evidence_group_id": "G_" + evidence_id,
        "discovery_anchor": {
            "epoch": 2,
            "kind": "SOURCE_UNIT",
            "id": source_unit_id,
            "ordinal": 1,
        },
        "source_unit_id": source_unit_id,
        "image_path": image_path,
        "strength": strength,
        "modality": modality,
        "claim": claim,
        "fingerprint_fields": [],
    }


def fp(
    status: str,
    value: str | None,
    evidence_ids: list[str],
    reason: str = "",
) -> dict[str, Any]:
    return {
        "status": status,
        "value": value,
        "evidence_ids": evidence_ids,
        "reason": reason,
    }


def supported(value: str, *evidence_ids: str) -> dict[str, Any]:
    return fp("SUPPORTED", value, list(evidence_ids))


def unknown(reason: str) -> dict[str, Any]:
    return fp("UNKNOWN_FROM_SOURCE", None, [], reason)


def not_applicable(name: str, field: str, *evidence_ids: str) -> dict[str, Any]:
    return fp(
        "NOT_APPLICABLE",
        None,
        list(evidence_ids),
        f"This field is not part of the source-defined semantics of {name}.",
    )


def unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def make_candidate(
    candidate_id: str,
    name: str,
    anchor: str,
    source_evidence: list[dict[str, Any]],
    fingerprint: dict[str, dict[str, Any]],
    *,
    related_candidate_ids: list[str] | None = None,
) -> dict[str, Any]:
    missing = unique(
        [
            item["reason"]
            for item in fingerprint.values()
            if item["status"] == "UNKNOWN_FROM_SOURCE"
        ]
    )
    return {
        "id": candidate_id,
        "record_status": "ACTIVE",
        "provisional_name": name,
        "aliases": [],
        "discovery_stage": 12,
        "discovery_anchor": {
            "epoch": 2,
            "kind": "SOURCE_UNIT",
            "id": anchor,
            "ordinal": 1,
        },
        "source_unit_ids": unique([item["source_unit_id"] for item in source_evidence]),
        "source_evidence": source_evidence,
        "source_status": ["CLEAR"],
        "image_witnesses": unique(
            [
                item["image_path"]
                for item in source_evidence
                if item["image_path"] is not None
            ]
        ),
        "evidence_strength": unique([item["strength"] for item in source_evidence]),
        "field_support": {
            field: item["status"] for field, item in fingerprint.items()
        },
        "fingerprint": fingerprint,
        "parameters": [],
        "variants": [],
        "missing_mechanics": missing,
        "uncertainties": list(missing),
        "related_candidate_ids": related_candidate_ids or [],
        "cross_reference_ids": [],
        "evidence_reassignments": [],
    }


def replace_tokens(value: Any, mapping: dict[str, str]) -> Any:
    token_re = re.compile(
        "|".join(re.escape(token) for token in sorted(mapping, key=len, reverse=True))
    )

    def visit(item: Any) -> Any:
        if isinstance(item, str):
            return token_re.sub(lambda match: mapping[match.group(0)], item)
        if isinstance(item, list):
            return [visit(child) for child in item]
        if isinstance(item, dict):
            return {key: visit(child) for key, child in item.items()}
        return item

    return visit(value)


def source_ordinal(source_unit_id: str) -> int:
    require(source_unit_id.startswith("U"), f"bad source unit: {source_unit_id}")
    return int(source_unit_id[1:])


def natural_selection_candidate(
    field_order: list[str],
) -> dict[str, Any]:
    name = "Natural-selection random search over organism programs"
    rows = [
        evidence(
            "NAT141",
            "U002141",
            "DIRECT_PARTIAL_MECHANICS",
            "PROSE",
            "Programs whose organism lineages produce more offspring become more numerous; small random mutations in offspring make successive generations a random search for programs with greater fitness.",
        ),
        evidence(
            "NAT143",
            "U002143",
            "CONTEXTUAL",
            "PROSE",
            "Fitness maximization is compared with constraint satisfaction: iterative random search may converge for simple constraints but can require astronomically many steps for complicated ones.",
        ),
        evidence(
            "NAT144",
            "U002144",
            "DIRECT_PARTIAL_MECHANICS",
            "PROSE",
            "Sexual reproduction can mix similar programs and organ differentiation can update program parts separately, but the source does not turn these search accelerators into an exact schedule.",
        ),
        evidence(
            "NAT145",
            "U002145",
            "CONTEXTUAL",
            "PROSE",
            "The source cautions that evolution commonly finds solutions that are merely easy and nonfatal rather than globally optimal.",
        ),
        evidence(
            "NAT154",
            "U002154",
            "CORROBORATING",
            "PROSE",
            "Random mutations cause a sequence of organism programs to be tried, many of which can yield complex behavior.",
        ),
        evidence(
            "NAT155",
            "U002155",
            "DIRECT_PARTIAL_MECHANICS",
            "PROSE",
            "Natural selection makes programs associated with more successful organisms dominate, while success may depend only on coarse behavioral features.",
        ),
        evidence(
            "NAT157",
            "U002157",
            "CORROBORATING",
            "PROSE",
            "The first randomly encountered program that is successful enough to survive may persist, but no exact survival or pruning threshold is supplied.",
        ),
        evidence(
            "NAT158",
            "U002158",
            "CONTEXTUAL",
            "PROSE",
            "The source attributes much biological complexity to the prevalence of complex behavior among randomly chosen programs rather than to exact optimization.",
        ),
        evidence(
            "NAT195",
            "U002195",
            "CORROBORATING",
            "PROSE",
            "Natural selection is explicitly characterized as an iterative random search, contrasted with explicit human effort in engineering.",
        ),
    ]
    values = {
        "object_kind": supported(
            "Population-level stochastic search over inherited organism programs.",
            "NAT141",
            "NAT195",
        ),
        "native_time": supported(
            "Discrete biological generations.", "NAT141", "NAT195"
        ),
        "carrier": supported(
            "A population of organism lineages carrying heritable programs.", "NAT141"
        ),
        "support": unknown(
            f"The bundled source does not determine the support for {name}."
        ),
        "topology": unknown(
            "The bundled source does not determine a population, mating, or lineage-interaction topology for the natural-selection search."
        ),
        "structural_invariants": unknown(
            "The bundled source does not state invariants for population size, lineage structure, or program length during the natural-selection search."
        ),
        "alphabet_or_value_schema": unknown(
            "The bundled source does not specify the representation or mutation alphabet of organism programs."
        ),
        "complete_state": supported(
            "The current organism population together with its inherited programs and relative reproductive or survival outcomes.",
            "NAT141",
            "NAT155",
        ),
        "visible_history": not_applicable(name, "visible_history", "NAT141"),
        "control_state": not_applicable(name, "control_state", "NAT141"),
        "seed": unknown(
            "The bundled source does not specify an initial population or initial organism programs."
        ),
        "input": supported(
            "Fitness constraints and organism features that affect reproductive or survival success.",
            "NAT143",
            "NAT155",
        ),
        "boundary": unknown(
            "The bundled source does not specify population bounds, carrying capacity, or replacement size."
        ),
        "external_data": supported(
            "Relative offspring production and survival provide the qualitative fitness signal.",
            "NAT141",
            "NAT155",
        ),
        "frontier_or_activation": supported(
            "Lineages are amplified when they produce more offspring or are successful enough to survive.",
            "NAT141",
            "NAT155",
            "NAT157",
        ),
        "schedule": unknown(
            "The bundled source states iteration over generations but does not determine the within-generation ordering of fitness evaluation, reproduction, mutation, pruning, and replacement."
        ),
        "read_dependencies_or_neighborhood": unknown(
            "The bundled source does not specify which organisms, lineages, environmental variables, or competitors are read when fitness is assigned."
        ),
        "law_kind": supported(
            "Stochastic program mutation coupled to fitness-weighted reproduction and natural selection.",
            "NAT141",
            "NAT154",
            "NAT155",
            "NAT195",
        ),
        "rule_relation_constraint_function_or_probability_law": unknown(
            "The bundled source does not determine the quantitative fitness-to-offspring map, population-pruning rule, recombination rule, or mutation probability law."
        ),
        "write_replacement_assembly_or_commit": supported(
            "More successful lineages contribute more inherited, randomly mutated offspring programs to later generations.",
            "NAT141",
            "NAT154",
            "NAT155",
        ),
        "result_kind": supported(
            "A sequence of program populations in which sufficiently successful programs can dominate, without a guarantee of finding an optimum.",
            "NAT143",
            "NAT145",
            "NAT155",
            "NAT157",
            "NAT158",
        ),
        "successor_cardinality": supported(
            "Multiple descendant populations are possible because offspring programs mutate randomly.",
            "NAT141",
            "NAT154",
        ),
        "determinism_branching_or_measure": supported(
            "Stochastic branching through random program mutation.", "NAT141", "NAT154"
        ),
        "termination_completion_failure": unknown(
            "The bundled source says a program may be successful enough to survive but gives no pruning threshold, stopping rule, or completion criterion."
        ),
        "witness_semantics": not_applicable(name, "witness_semantics", "NAT195"),
        "parameters_and_variants": supported(
            "Sexual reproduction mixes similar programs, while organ differentiation permits separate updates of program parts.",
            "NAT144",
        ),
        "excluded_observers_and_representations": supported(
            "Explicit human engineering effort is a comparison, not a native step of the natural-selection process.",
            "NAT195",
        ),
        "evidence_limit": supported(
            "The source gives a qualitative search mechanism and explicitly questions optimality, but leaves the fitness, mutation, pruning, recombination, population, and update schedule quantitative laws unstated.",
            "NAT141",
            "NAT143",
            "NAT145",
            "NAT155",
            "NAT157",
            "NAT195",
        ),
    }
    require(list(values) == field_order, "natural-selection fingerprint order mismatch")
    return make_candidate(
        "NATURAL_SELECTION",
        name,
        "U002141",
        rows,
        values,
    )


def homeobox_candidate(field_order: list[str]) -> dict[str, Any]:
    name = "Homeobox concentration-threshold regional differentiation mechanism"
    rows = [
        evidence(
            "HOX323",
            "U002323",
            "CONTEXTUAL",
            "PROSE",
            "The source poses selection of genetic-program sections during development and contrasts cell-by-cell selection in very simple animals with the regional mechanism that follows.",
        ),
        evidence(
            "HOX324",
            "U002324",
            "DIRECT_PARTIAL_MECHANICS",
            "PROSE",
            "Developing regions, rather than generally individual cells, use different genetic-program sections and can split into smaller regions at a characteristic scale.",
        ),
        evidence(
            "HOX325",
            "U002325",
            "DIRECT_PARTIAL_MECHANICS",
            "PROSE",
            "Cells produce chemicals whose concentrations decline over distance; homeobox genes switch at particular concentration levels and control which genetic-program section is used.",
        ),
        evidence(
            "HOX326",
            "U002326",
            "CORROBORATING",
            "PROSE",
            "A fixed spatial length scale makes early development hierarchical because only a handful of program regions fit in a small embryo.",
        ),
        evidence(
            "HOX327",
            "U002327",
            "CORROBORATING",
            "PROSE",
            "As a region grows it can differentiate into smaller program regions, recursively yielding structures such as feet, tissue classes, and individual bones.",
        ),
    ]
    values = {
        "object_kind": supported(
            "Spatial developmental-control mechanism coupling chemical concentration thresholds to homeobox-gene activation and genetic-program selection.",
            "HOX323",
            "HOX325",
        ),
        "native_time": supported(
            "Successive stages of embryo growth and regional differentiation.",
            "HOX326",
            "HOX327",
        ),
        "carrier": supported(
            "Cells and spatial tissue regions carrying concentration fields, homeobox-gene states, and an underlying genetic program.",
            "HOX324",
            "HOX325",
        ),
        "support": unknown(
            f"The bundled source does not determine the support for {name}."
        ),
        "topology": supported(
            "Spatially extended embryonic tissue organized into regions over distances of a few tenths of a millimeter.",
            "HOX324",
            "HOX325",
        ),
        "structural_invariants": supported(
            "A fixed differentiation length scale induces a hierarchical region structure as the embryo grows.",
            "HOX324",
            "HOX326",
            "HOX327",
        ),
        "alphabet_or_value_schema": supported(
            "Chemical concentrations, active/inactive homeobox genes, and selected sections of the genetic program.",
            "HOX325",
        ),
        "complete_state": unknown(
            "The bundled source does not enumerate the chemical species, concentration fields, gene states, region geometry, and program-section state needed for a complete configuration."
        ),
        "visible_history": not_applicable(name, "visible_history", "HOX323"),
        "control_state": supported(
            "Homeobox-gene activation states and the genetic-program section selected for each region.",
            "HOX325",
        ),
        "seed": unknown(
            "The bundled source does not specify initial chemical sources, concentration profiles, gene states, or embryo geometry."
        ),
        "input": supported(
            "The underlying genetic program whose sections can be selected in cells or regions.",
            "HOX323",
            "HOX325",
        ),
        "boundary": unknown(
            "The bundled source does not give chemical boundary conditions or tissue-domain boundary behavior."
        ),
        "external_data": not_applicable(name, "external_data", "HOX325"),
        "frontier_or_activation": supported(
            "Crossing particular chemical-concentration levels activates or inactivates homeobox genes, and sufficiently grown regions differentiate further.",
            "HOX325",
            "HOX327",
        ),
        "schedule": unknown(
            "The bundled source does not determine the timing or update order for chemical production, diffusion, threshold evaluation, gene switching, growth, and region subdivision."
        ),
        "read_dependencies_or_neighborhood": unknown(
            "The bundled source says concentrations decrease with distance but gives no diffusion neighborhood, coupling graph, kernel, or differential operator."
        ),
        "law_kind": supported(
            "Spatial chemical-gradient threshold control of developmental program selection.",
            "HOX325",
        ),
        "rule_relation_constraint_function_or_probability_law": unknown(
            "The bundled source does not supply diffusion equations or coefficients, threshold values, chemical-to-gene logic, or the gene-to-program-section map."
        ),
        "write_replacement_assembly_or_commit": supported(
            "Activated homeobox genes control which underlying genetic-program section a region uses.",
            "HOX325",
        ),
        "result_kind": supported(
            "Hierarchical differentiation into progressively smaller regions that use different program sections and yield distinct tissues or structures.",
            "HOX324",
            "HOX326",
            "HOX327",
        ),
        "successor_cardinality": unknown(
            "The bundled source says regions split into a handful of smaller regions but does not specify an exact arity or successor construction."
        ),
        "determinism_branching_or_measure": unknown(
            "The bundled source does not state whether threshold ties, fluctuations, or region choices are deterministic or stochastic."
        ),
        "termination_completion_failure": unknown(
            "The bundled source does not define a terminal developmental state or failure condition for the mechanism."
        ),
        "witness_semantics": not_applicable(name, "witness_semantics", "HOX323"),
        "parameters_and_variants": supported(
            "Very simple animals may select programs cell by cell; larger animals use regions at a characteristic scale and recursively differentiate as regions grow.",
            "HOX323",
            "HOX324",
            "HOX325",
            "HOX327",
        ),
        "excluded_observers_and_representations": supported(
            "Individual cell identity is not generally the program-selection unit; the source identifies developing regions as the typical unit.",
            "HOX324",
        ),
        "evidence_limit": supported(
            "The qualitative chemical-gradient, concentration-threshold, homeobox-switch, and program-selection chain is explicit, but its diffusion, threshold, gene logic, and program-mapping mechanics are not.",
            "HOX325",
        ),
    }
    require(list(values) == field_order, "homeobox fingerprint order mismatch")
    return make_candidate(
        "HOMEOBOX",
        name,
        "U002323",
        rows,
        values,
    )


def repair(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    candidates = data["candidate_proposals"]
    require(len(candidates) == 22, "expected rejected 22-candidate output")
    by_id = {candidate["id"]: candidate for candidate in candidates}
    field_order = list(candidates[0]["fingerprint"])

    # U002054 directly supplies the alternating tree/faceted outcome.
    snowflake = by_id["W0002"]
    snow_evidence = evidence(
        "SNOW054",
        "U002054",
        "CORROBORATING",
        "PROSE",
        "The model predicts alternation between tree-like and faceted snowflake shapes as branches grow and then collide.",
    )
    snowflake["source_evidence"].insert(1, snow_evidence)
    result_ids = snowflake["fingerprint"]["result_kind"]["evidence_ids"]
    result_ids.insert(1, "SNOW054")

    # The old W0007 is a mutation-only display, explicitly without selection.
    mutation = by_id["W0007"]
    mutation["related_candidate_ids"] = []
    mutation_caption = next(
        item
        for item in mutation["source_evidence"]
        if item["source_unit_id"] == "U002176"
    )
    mutation_caption["claim"] = (
        "The caption defines a three-color, 27-neighborhood single-random-mutation "
        "sequence and explicitly says that this idealization has no explicit natural selection."
    )
    mutation["fingerprint"]["excluded_observers_and_representations"]["value"] = (
        "The displayed spacetime patterns evaluate each program but are not mutation "
        "state; the sequence explicitly omits fitness-based reproduction and natural selection."
    )
    mutation["fingerprint"]["evidence_limit"]["value"] = (
        "The mutation operation is qualitative, with no explicit distribution over entries "
        "or replacement colors, and the caption explicitly excludes natural selection."
    )

    # Correct the one-unit drift around the rectangular-subdivision discussion.
    rectangle = by_id["W0017"]
    rectangle["discovery_anchor"]["id"] = "U002328"
    old_to_temp = {
        "WE000066": "RECT328",
        "WE000067": "RECT329",
        "WE000068": "RECT330",
    }
    rectangle = replace_tokens(rectangle, old_to_temp)
    rectangle["source_evidence"] = [
        evidence(
            "RECT328",
            "U002328",
            "DIRECT_PARTIAL_MECHANICS",
            "PROSE",
            "Equal regional growth yields a regular structure, while different substitution rules for each cell type generally produce nesting.",
        ),
        evidence(
            "RECT329",
            "U002329",
            "DIRECT_PARTIAL_MECHANICS",
            "CAPTION",
            "The schematic repeatedly subdivides in two directions, always producing three simple rectangles that grow at the same rate.",
        ),
        evidence(
            "RECT330",
            "U002330",
            "CORROBORATING",
            "IMAGE",
            "Original-resolution inspection confirms three labeled stages of alternating three-rectangle refinement.",
            "CHAPTERS/_page_435_Picture_5.jpeg",
        ),
        evidence(
            "RECT331",
            "U002331",
            "CONTEXTUAL",
            "PROSE",
            "Real regions may split concentrically or in more complex layouts, grow at unequal rates, fold, or deform, with geometry affecting later subdivisions.",
        ),
    ]
    rfp = rectangle["fingerprint"]
    rfp["carrier"]["evidence_ids"] = ["RECT328", "RECT329"]
    rfp["topology"]["evidence_ids"] = ["RECT328", "RECT329"]
    rfp["structural_invariants"]["evidence_ids"] = ["RECT328", "RECT329"]
    rfp["alphabet_or_value_schema"]["evidence_ids"] = ["RECT328", "RECT330"]
    rfp["complete_state"]["evidence_ids"] = ["RECT328"]
    rfp["visible_history"]["evidence_ids"] = ["RECT330"]
    rfp["seed"]["evidence_ids"] = ["RECT329", "RECT330"]
    rfp["schedule"]["evidence_ids"] = ["RECT328", "RECT329"]
    rfp["read_dependencies_or_neighborhood"]["evidence_ids"] = ["RECT328"]
    rfp["law_kind"]["evidence_ids"] = ["RECT328", "RECT329"]
    rfp["rule_relation_constraint_function_or_probability_law"][
        "evidence_ids"
    ] = ["RECT328", "RECT329"]
    rfp["write_replacement_assembly_or_commit"]["evidence_ids"] = [
        "RECT328",
        "RECT329",
    ]
    rfp["result_kind"]["evidence_ids"] = ["RECT328", "RECT330", "RECT331"]
    rfp["determinism_branching_or_measure"]["evidence_ids"] = [
        "RECT328",
        "RECT329",
    ]
    rfp["parameters_and_variants"]["value"] = (
        "The schematic uses two directions and equal growth; the source also allows "
        "concentric or more complicated layouts, unequal growth, folding, and deformation."
    )
    rfp["parameters_and_variants"]["evidence_ids"] = [
        "RECT328",
        "RECT329",
        "RECT330",
        "RECT331",
    ]
    rfp["evidence_limit"]["value"] = (
        "The schematic fixes three equal-growing rectangles in two directions, while "
        "real geometry and growth may be more complex and no exact type-to-substitution table is enumerated."
    )
    rfp["evidence_limit"]["evidence_ids"] = ["RECT329", "RECT331"]
    by_id["W0017"] = rectangle

    # U002394 defines the observer; U002395 instead states propagation/randomness.
    market = by_id["W0022"]
    market_observer = evidence(
        "MARKET394",
        "U002394",
        "DIRECT_PARTIAL_MECHANICS",
        "PROSE",
        "The market-price analog is the running difference between total black and white cells on successive cellular-automaton steps.",
    )
    market["source_evidence"].insert(len(market["source_evidence"]) - 1, market_observer)
    market_395 = next(
        item
        for item in market["source_evidence"]
        if item["source_unit_id"] == "U002395"
    )
    market_395["claim"] = (
        "When the local rule eventually propagates information from any entity to all "
        "others, the running cell-count totals inevitably exhibit significant randomness."
    )
    mfp = market["fingerprint"]
    mfp["result_kind"]["evidence_ids"].extend(["MARKET394", "WE000086"])
    mfp["excluded_observers_and_representations"]["evidence_ids"] = [
        item
        for item in mfp["excluded_observers_and_representations"]["evidence_ids"]
        if item != "WE000086"
    ]
    mfp["excluded_observers_and_representations"]["evidence_ids"].append("MARKET394")
    mfp["evidence_limit"]["value"] = (
        "The exact local table and displayed seed are graphical; propagation to all "
        "entities supports random-looking totals, but the model defines no real transaction "
        "price or order-matching mechanism."
    )
    mfp["evidence_limit"]["evidence_ids"].append("WE000086")

    candidates = [
        by_id[candidate["id"]] for candidate in data["candidate_proposals"]
    ]
    candidates.extend(
        [
            natural_selection_candidate(field_order),
            homeobox_candidate(field_order),
        ]
    )
    candidates.sort(
        key=lambda candidate: (
            source_ordinal(candidate["discovery_anchor"]["id"]),
            candidate["discovery_anchor"]["ordinal"],
        )
    )
    candidate_id_map = {
        candidate["id"]: f"W{ordinal:04d}"
        for ordinal, candidate in enumerate(candidates, start=1)
    }
    data["candidate_proposals"] = candidates
    data = replace_tokens(data, candidate_id_map)

    # Reallocate global evidence/group IDs by frozen source traversal.
    all_evidence: list[dict[str, Any]] = [
        item
        for candidate in data["candidate_proposals"]
        for item in candidate["source_evidence"]
    ]
    all_evidence.sort(
        key=lambda item: (
            source_ordinal(item["discovery_anchor"]["id"]),
            item["discovery_anchor"]["ordinal"],
            item["evidence_id"],
        )
    )
    anchors = [
        (
            item["discovery_anchor"]["kind"],
            item["discovery_anchor"]["id"],
            item["discovery_anchor"]["ordinal"],
        )
        for item in all_evidence
    ]
    require(len(anchors) == len(set(anchors)), "duplicate evidence discovery anchor")
    evidence_id_map = {
        item["evidence_id"]: f"WE{ordinal:06d}"
        for ordinal, item in enumerate(all_evidence, start=1)
    }
    group_id_map = {
        item["evidence_group_id"]: f"WG{ordinal:06d}"
        for ordinal, item in enumerate(all_evidence, start=1)
    }
    data = replace_tokens(data, group_id_map)
    data = replace_tokens(data, evidence_id_map)

    # Derive all redundant candidate projections and exact fingerprint inverses.
    for candidate in data["candidate_proposals"]:
        source_evidence = candidate["source_evidence"]
        source_sorted = sorted(
            source_evidence, key=lambda item: source_ordinal(item["source_unit_id"])
        )
        candidate["source_unit_ids"] = unique(
            [item["source_unit_id"] for item in source_sorted]
        )
        candidate["image_witnesses"] = unique(
            [
                item["image_path"]
                for item in source_sorted
                if item["image_path"] is not None
            ]
        )
        candidate["evidence_strength"] = unique(
            [item["strength"] for item in source_evidence]
        )
        candidate["field_support"] = {
            field: item["status"]
            for field, item in candidate["fingerprint"].items()
        }
        missing = unique(
            [
                item["reason"]
                for item in candidate["fingerprint"].values()
                if item["status"] == "UNKNOWN_FROM_SOURCE"
            ]
        )
        candidate["missing_mechanics"] = missing
        candidate["uncertainties"] = list(missing)
        for item in source_evidence:
            item["fingerprint_fields"] = [
                field
                for field, fingerprint_item in candidate["fingerprint"].items()
                if item["evidence_id"] in fingerprint_item["evidence_ids"]
            ]
            require(
                item["fingerprint_fields"],
                f"unreferenced evidence {item['evidence_id']}",
            )

    # Rebuild exact reading-to-candidate joins after renumbering.
    unit_to_candidates: dict[str, list[str]] = {}
    anchor_by_candidate: dict[str, str] = {}
    for candidate in data["candidate_proposals"]:
        anchor_by_candidate[candidate["id"]] = candidate["discovery_anchor"]["id"]
        for source_unit_id in candidate["source_unit_ids"]:
            unit_to_candidates.setdefault(source_unit_id, []).append(candidate["id"])
    for candidate_ids in unit_to_candidates.values():
        candidate_ids.sort()

    natural_id = next(
        candidate["id"]
        for candidate in data["candidate_proposals"]
        if candidate["provisional_name"]
        == "Natural-selection random search over organism programs"
    )
    mutation_id = next(
        candidate["id"]
        for candidate in data["candidate_proposals"]
        if candidate["provisional_name"]
        == "Random-mutation sequence of three-color cellular-automaton programs"
    )
    homeobox_id = next(
        candidate["id"]
        for candidate in data["candidate_proposals"]
        if candidate["provisional_name"]
        == "Homeobox concentration-threshold regional differentiation mechanism"
    )
    rectangle_id = next(
        candidate["id"]
        for candidate in data["candidate_proposals"]
        if candidate["provisional_name"]
        == "Recursive rectangular embryo-subdivision model"
    )
    market_id = next(
        candidate["id"]
        for candidate in data["candidate_proposals"]
        if candidate["provisional_name"]
        == "One-dimensional market cellular automaton with price observer"
    )
    snowflake_id = next(
        candidate["id"]
        for candidate in data["candidate_proposals"]
        if candidate["provisional_name"]
        == "Exactly-one-neighbor hexagonal snowflake cellular automaton"
    )

    statements = {
        "U002054": (
            "This unit supports "
            + snowflake_id
            + " by directly predicting alternating tree-like and faceted outcomes as branches grow and collide."
        ),
        "U002141": (
            "This unit first defines "
            + natural_id
            + ": fitness-weighted reproduction plus random mutation produces a generational program search."
        ),
        "U002143": (
            "This unit bounds "
            + natural_id
            + " by explaining when iterative random search converges or becomes astronomically slow."
        ),
        "U002144": (
            "This unit supplies sexual recombination and separately updated program parts as qualitative variants of "
            + natural_id
            + "."
        ),
        "U002145": (
            "This unit supports "
            + natural_id
            + " by distinguishing easy, nonfatal solutions from global fitness optima."
        ),
        "U002154": (
            "This unit supports the random-mutation program sequence within "
            + natural_id
            + "."
        ),
        "U002155": (
            "This unit directly supplies natural-selection dominance and coarse fitness criteria for "
            + natural_id
            + "."
        ),
        "U002157": (
            "This unit states the first-successful-enough survival behavior for "
            + natural_id
            + " while leaving its pruning threshold unstated."
        ),
        "U002158": (
            "This unit supplies the complex-program outcome interpretation for "
            + natural_id
            + "."
        ),
        "U002176": (
            "This caption supports "
            + mutation_id
            + " and explicitly distinguishes its mutation-only sequence from "
            + natural_id
            + " by stating that no natural selection is included."
        ),
        "U002195": (
            "This unit directly characterizes natural selection in "
            + natural_id
            + " as an iterative random search rather than explicit engineering effort."
        ),
        "U002323": (
            "This unit first frames "
            + homeobox_id
            + " as the mechanism selecting genetic-program sections during development."
        ),
        "U002324": (
            "This unit supplies region-scale program selection and subdivision evidence for "
            + homeobox_id
            + "."
        ),
        "U002325": (
            "This unit supplies the core chemical-gradient, concentration-threshold, homeobox-switch, and program-control chain for "
            + homeobox_id
            + "."
        ),
        "U002326": (
            "This unit supports the fixed spatial scale and hierarchical-development result of "
            + homeobox_id
            + "."
        ),
        "U002327": (
            "This unit supports recursive region differentiation as an outcome of "
            + homeobox_id
            + "."
        ),
        "U002328": (
            "This unit first supplies type-dependent substitution, equal growth, and nested structure for "
            + rectangle_id
            + "."
        ),
        "U002329": (
            "This caption supports "
            + rectangle_id
            + " with two subdivision directions and three equal-growing rectangles."
        ),
        "U002330": (
            "Original-resolution image inspection corroborates the staged rectangular refinements of "
            + rectangle_id
            + "."
        ),
        "U002331": (
            "This unit bounds "
            + rectangle_id
            + " with complex layouts, unequal growth, folding, deformation, and geometry-dependent later subdivision."
        ),
        "U002394": (
            "This unit directly defines the black-minus-white running-total price observer for "
            + market_id
            + "."
        ),
        "U002395": (
            "This unit supports "
            + market_id
            + " by linking all-entity information propagation to significant randomness in running totals."
        ),
    }
    for row in data["reading_updates"]:
        source_unit_id = row["source_unit_id"]
        candidate_ids = unit_to_candidates.get(source_unit_id, [])
        row["candidate_ids"] = json.dumps(candidate_ids)
        if candidate_ids:
            row["review_disposition"] = (
                "CANDIDATE"
                if any(
                    anchor_by_candidate[candidate_id] == source_unit_id
                    for candidate_id in candidate_ids
                )
                else "SUPPORTS_CANDIDATE"
            )
            if source_unit_id in statements:
                row["evidence_statement"] = statements[source_unit_id]

    # Rebuild exact asset-to-candidate joins.
    path_to_candidates: dict[str, list[str]] = {}
    for candidate in data["candidate_proposals"]:
        for image_path in candidate["image_witnesses"]:
            path_to_candidates.setdefault(image_path, []).append(candidate["id"])
    for candidate_ids in path_to_candidates.values():
        candidate_ids.sort()
    for row in data["asset_updates"]:
        candidate_ids = path_to_candidates.get(row["physical_path"], [])
        row["candidate_ids"] = json.dumps(candidate_ids)

    data["uncertainties"].extend(
        [
            "The natural-selection program-search source gives a qualitative fitness-weighted reproduction and mutation process but not an exact mutation law, pruning threshold, population rule, or within-generation schedule.",
            "The homeobox source gives a qualitative diffusion-to-threshold-to-program-control chain but not exact diffusion equations, threshold values, gene logic, or program-section mapping.",
        ]
    )

    rendered = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(rendered)
    import hashlib

    return hashlib.sha256(rendered).hexdigest()


def main() -> int:
    require(len(sys.argv) == 2, "usage: _repair_ch08_main_output.py OUTPUT_JSON")
    path = Path(sys.argv[1])
    digest = repair(path)
    print(
        f"{path} sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
