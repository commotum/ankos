#!/usr/bin/env python3
"""Author the sealed Stage 8 Chapter 4 main-text blind review reproducibly.

This helper is bound to the exact epoch-1 bundle for
``CHAPTERS/04-Systems-Based-on-Numbers.md``.  It records the judgments made
after the 306 units were read in canonical order and all 63 assigned assets
were screened.  It refuses to modify anything except a pristine nonsemantic
worksheet for that exact assignment.
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
    "0b5a50b9f6214e4b3600bf8ba55f2064739bf3f835113a135b0c09b7f877ab4d"
)
EXPECTED_WORKER = "ch04-main-reader-e1"
EXPECTED_PATHS = ["CHAPTERS/04-Systems-Based-on-Numbers.md"]
STAGE = 8


class AuthoringError(ValueError):
    """The assignment or worksheet is not safe for this exact authoring pass."""


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
    strength: str = "DIRECT_PARTIAL_MECHANICS",
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
    evidence(
        spec,
        f"{key}-source",
        anchor,
        claim,
        list(facts) + list((not_applicable or {}).keys()),
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
    fields: list[str] | None = None,
    strength: str = "CORROBORATING",
    modality: str = "PROSE",
    image_path: str | None = None,
) -> None:
    evidence(
        spec,
        label,
        unit,
        claim,
        fields or [],
        strength=strength,
        modality=("IMAGE" if image_path else modality),
        image_path=image_path,
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
    if any(item["key"] == key for item in ALL_ROUTES):
        raise AuthoringError(f"duplicate route key {key}")
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


EVOLUTION_NA = {
    "control_state": "No independently stored head, instruction pointer, or control register is part of this law.",
    "external_data": "After the rule and initial state are supplied, no external data stream is read.",
}

DECLARATIVE_NA = {
    "visible_history": "This fixed denotation or query has no native trajectory.",
    "control_state": "This fixed denotation or query has no control register.",
    "seed": "This fixed denotation or query has no initial state.",
    "boundary": "No evolution boundary is part of this fixed denotation or query.",
    "external_data": "No external data stream is consumed.",
    "frontier_or_activation": "No components fire in a fixed denotation or query.",
    "schedule": "There is no update schedule.",
    "read_dependencies_or_neighborhood": "There is no local update neighborhood.",
    "write_replacement_assembly_or_commit": "No state update is committed.",
}

SEED_NA = {
    "visible_history": "An initial-state object has no native trajectory.",
    "control_state": "An initial-state object has no control register.",
    "input": "The object is supplied as input rather than consuming another input.",
    "boundary": "Any evolution boundary belongs to the associated law, not this seed object.",
    "external_data": "No external data stream is consumed.",
    "frontier_or_activation": "A seed has no update frontier.",
    "schedule": "A seed has no update schedule.",
    "read_dependencies_or_neighborhood": "A seed performs no local reads.",
    "law_kind": "A seed is data, not an update law.",
    "rule_relation_constraint_function_or_probability_law": "A seed is data, not an update law.",
    "write_replacement_assembly_or_commit": "A seed performs no writes.",
    "termination_completion_failure": "Providing the complete seed completes this object.",
}


def iterative_facts(
    *,
    kind: str,
    carrier: str,
    support: str,
    topology: str,
    invariants: str,
    alphabet: str,
    state: str,
    seed: str,
    input_value: str,
    frontier: str,
    schedule: str,
    read: str,
    law_kind: str,
    law: str,
    write: str,
    result: str,
    successor: str = "Exactly one successor follows from each complete state.",
    determinism: str = "Deterministic for a fixed rule and complete state.",
    termination: str = "The law is iterated for the requested number of steps unless its stated domain condition fails.",
    witness: str = "Every adjacent pair in a valid trajectory satisfies the stated update law.",
    variants: str,
    excluded: str,
    limit: str,
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
        "visible_history": "The ordered sequence of complete numeric states.",
        "seed": seed,
        "input": input_value,
        "frontier_or_activation": frontier,
        "schedule": schedule,
        "read_dependencies_or_neighborhood": read,
        "law_kind": law_kind,
        "rule_relation_constraint_function_or_probability_law": law,
        "write_replacement_assembly_or_commit": write,
        "result_kind": result,
        "successor_cardinality": successor,
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": termination,
        "witness_semantics": witness,
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": excluded,
        "evidence_limit": limit,
    }


def number_map_facts(
    name: str,
    domain: str,
    law: str,
    seed: str,
    variants: str,
) -> dict[str, str]:
    return iterative_facts(
        kind=name,
        carrier="One numeric register n.",
        support="A single scalar position.",
        topology="No spatial adjacency; the next value depends on the current scalar.",
        invariants=f"The state remains in {domain} under the stated scope.",
        alphabet=domain,
        state="The current value of n.",
        seed=seed,
        input_value="The current scalar n.",
        frontier="The one scalar register is active at each step.",
        schedule="Apply the map once per step.",
        read="Read the complete current value of n and any stated arithmetic predicate.",
        law_kind="A deterministic arithmetic map.",
        law=law,
        write="Replace n atomically by the map result.",
        result="A successor number and, under iteration, a numeric sequence.",
        variants=variants,
        excluded="Digit plots, size plots, parity traces, and behavior labels are observers of the numeric trajectory.",
        limit="Finite-precision implementation details are not stated; the mathematical values are treated exactly.",
    )


def recurrence_facts(name: str, law: str, seed: str, read: str) -> dict[str, str]:
    return iterative_facts(
        kind=name,
        carrier="An indexed sequence f[1], f[2], ... of numbers.",
        support="Positive integer indices.",
        topology="Index order supplies access to already generated sequence elements.",
        invariants="Previously generated elements are retained while one new element is appended.",
        alphabet="Integers in the displayed examples.",
        state="The generated prefix f[1] through f[n-1].",
        seed=seed,
        input_value="The current index n and the already generated prefix.",
        frontier="The next not-yet-generated index n.",
        schedule="Generate terms in increasing index order.",
        read=read,
        law_kind="A deterministic recurrence.",
        law=law,
        write="Append the computed value as f[n] without changing earlier terms.",
        result="A new sequence prefix and, by continuation, an infinite or failed recursive sequence.",
        termination="Generation continues while every referenced index is a defined positive earlier index; otherwise the rule fails.",
        variants="The recurrence formula and initial terms are the parameters.",
        excluded="Plots of growth and detrended fluctuations are observers, not recurrence state.",
        limit="The source explicitly notes that many formulas fail by requesting f[0] or negative indices.",
    )


def declarative_facts(
    *,
    kind: str,
    carrier: str,
    support: str,
    alphabet: str,
    state: str,
    input_value: str,
    law_kind: str,
    law: str,
    result: str,
    successor: str,
    determinism: str,
    termination: str,
    witness: str,
    variants: str,
    excluded: str,
    limit: str,
) -> dict[str, str]:
    return {
        "object_kind": kind,
        "native_time": "No native time; this is a fixed function, relation, representation, or query.",
        "carrier": carrier,
        "support": support,
        "topology": "No spatial topology beyond the stated ordered/indexed support.",
        "structural_invariants": "The stated domain, codomain, and relation remain fixed during evaluation.",
        "alphabet_or_value_schema": alphabet,
        "complete_state": state,
        "input": input_value,
        "law_kind": law_kind,
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "successor_cardinality": successor,
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": termination,
        "witness_semantics": witness,
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": excluded,
        "evidence_limit": limit,
    }


def seed_facts(kind: str, carrier: str, support: str, value: str, variants: str) -> dict[str, str]:
    return {
        "object_kind": kind,
        "native_time": "No native time; this object denotes initial data.",
        "carrier": carrier,
        "support": support,
        "topology": "The topology is inherited from the associated evolution law.",
        "structural_invariants": "The complete initial value is fixed as stated.",
        "alphabet_or_value_schema": value,
        "complete_state": value,
        "seed": value,
        "result_kind": "A complete initial state for an associated evolution law.",
        "successor_cardinality": "Exactly one initial state for the stated preset.",
        "determinism_branching_or_measure": "Deterministic, not sampled.",
        "witness_semantics": "The supplied initial state equals the stated value or configuration.",
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": "Its printed digits or drawn row are representations of the seed.",
        "evidence_limit": "Coordinates or finite-display conventions not stated by the source remain outside this seed object.",
    }
