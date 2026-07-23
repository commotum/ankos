#!/usr/bin/env python3
"""Record the completed, source-grounded Stage 4 bookends review.

This is a reproducibility script for the explicit judgments in
``4-BOOKENDS.md``.  It is intentionally bound to the exact sealed epoch-1
bundle built from the current canonical corpus.  It supplies no decisions for
other stages and refuses to overwrite unrelated or partially different work.
"""

from __future__ import annotations

import csv
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import prepare_review_output
from audit_contract import CANDIDATE_FIELDS, FINGERPRINT_FIELDS, canonical_json_bytes


EXPECTED_CONTENT_SET = (
    "e53c60b50ac00aa9b1e2eb3bdf0c02c53ba89556a536557a39622993908ac8e7"
)
EXPECTED_WORKER = "bookends-reader-e1"
EXPECTED_PATHS = [
    "FRONT-MATTER/00-Publication-and-Contents.md",
    "FRONT-MATTER/01-Preface.md",
    "BACK-MATTER/NOTES/00-General-Notes.md",
    "BACK-MATTER/Colophon.md",
]
RULE_110_IMAGE = "BACK-MATTER/NOTES/_page_866_Picture_8.jpeg"
PREFACE_IMAGE = "FRONT-MATTER/_page_14_Picture_0.jpeg"


class AuthoringError(ValueError):
    """The exact Stage 4 assignment or worksheet is not safe to update."""


def compact(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def evidence(
    evidence_id: str,
    group_id: str,
    *,
    anchor_kind: str,
    anchor_id: str,
    source_unit_id: str | None,
    image_path: str | None,
    strength: str,
    modality: str,
    claim: str,
    fields: list[str],
) -> dict[str, Any]:
    return {
        "evidence_id": evidence_id,
        "evidence_group_id": group_id,
        "discovery_anchor": {
            "epoch": 1,
            "kind": anchor_kind,
            "id": anchor_id,
            "ordinal": 1,
        },
        "source_unit_id": source_unit_id,
        "image_path": image_path,
        "strength": strength,
        "modality": modality,
        "claim": claim,
        "fingerprint_fields": fields,
    }


def candidate(
    *,
    candidate_id: str,
    name: str,
    aliases: list[str],
    anchor_id: str,
    source_unit_ids: list[str],
    source_evidence: list[dict[str, Any]],
    image_witnesses: list[str],
    supported: dict[str, tuple[str, list[str]]],
    parameters: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    missing: str,
    route_ids: list[str],
) -> dict[str, Any]:
    field_support = {
        field: (
            "SUPPORTED" if field in supported else "UNKNOWN_FROM_SOURCE"
        )
        for field in FINGERPRINT_FIELDS
    }
    fingerprint = {
        field: (
            {
                "status": "SUPPORTED",
                "value": supported[field][0],
                "evidence_ids": supported[field][1],
                "reason": "",
            }
            if field in supported
            else {
                "status": "UNKNOWN_FROM_SOURCE",
                "value": None,
                "evidence_ids": [],
                "reason": missing,
            }
        )
        for field in FINGERPRINT_FIELDS
    }
    values: dict[str, Any] = {
        "id": candidate_id,
        "record_status": "ACTIVE",
        "provisional_name": name,
        "aliases": aliases,
        "discovery_stage": 4,
        "discovery_anchor": {
            "epoch": 1,
            "kind": "SOURCE_UNIT",
            "id": anchor_id,
            "ordinal": 1,
        },
        "source_unit_ids": source_unit_ids,
        "source_evidence": source_evidence,
        "source_status": ["CLEAR"],
        "image_witnesses": image_witnesses,
        "evidence_strength": list(
            dict.fromkeys(item["strength"] for item in source_evidence)
        ),
        "field_support": field_support,
        "fingerprint": fingerprint,
        "parameters": parameters,
        "variants": variants,
        "missing_mechanics": [missing],
        "uncertainties": [],
        "related_candidate_ids": [],
        "cross_reference_ids": route_ids,
        "evidence_reassignments": [],
    }
    return {field: values[field] for field in CANDIDATE_FIELDS}


def rule_30_candidate() -> dict[str, Any]:
    e1_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "topology",
        "alphabet_or_value_schema",
        "complete_state",
        "seed",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    e4_fields = [
        "native_time",
        "support",
        "seed",
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    e1 = evidence(
        "WE000001",
        "WG000001",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U004864",
        source_unit_id="U004864",
        image_path=None,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="PROSE",
        claim=(
            "The stadium description names Rule 30, gives black/white cell "
            "values, a single-black-cell seed, synchronous successive rows, "
            "and a left/self/right predecessor neighborhood; it routes the "
            "missing lookup rule to page 27."
        ),
        fields=e1_fields,
    )
    e4 = evidence(
        "WE000004",
        "WG000004",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U004873",
        source_unit_id="U004873",
        image_path=None,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="PROSE",
        claim=(
            "The endpaper note identifies Rule 30 from one black cell and "
            "describes two finite display windows totaling about 1000 steps."
        ),
        fields=e4_fields,
    )
    supported = {
        "object_kind": (
            "Named one-dimensional binary cellular-automaton preset.",
            ["WE000001"],
        ),
        "native_time": (
            "Discrete generations represented by successive rows.",
            ["WE000001", "WE000004"],
        ),
        "carrier": (
            "A row of cell positions represented by people holding cards.",
            ["WE000001"],
        ),
        "support": (
            "A one-dimensional row whose successive generations form a "
            "two-dimensional history display.",
            ["WE000001", "WE000004"],
        ),
        "topology": (
            "Linear left/self/right adjacency is used for predecessor reads.",
            ["WE000001"],
        ),
        "alphabet_or_value_schema": (
            "Two values represented by black and white cards/cells.",
            ["WE000001"],
        ),
        "complete_state": (
            "The current row of black/white cell values.",
            ["WE000001"],
        ),
        "seed": (
            "One black cell with all other displayed cells white.",
            ["WE000001", "WE000004"],
        ),
        "frontier_or_activation": (
            "Every position in the next successive row determines a value.",
            ["WE000001"],
        ),
        "schedule": (
            "Generation-synchronous row-by-row evaluation.",
            ["WE000001"],
        ),
        "read_dependencies_or_neighborhood": (
            "The predecessor directly above and its immediate left and right "
            "neighbors.",
            ["WE000001"],
        ),
        "law_kind": (
            "A named deterministic local cellular-automaton rule.",
            ["WE000001"],
        ),
        "result_kind": (
            "A unique successive-row evolution, displayed as a space-time "
            "pattern.",
            ["WE000001", "WE000004"],
        ),
        "successor_cardinality": (
            "Each next-row cell is determined once the referenced rule is "
            "supplied.",
            ["WE000001"],
        ),
        "determinism_branching_or_measure": (
            "Deterministic; no branching or probability is described.",
            ["WE000001"],
        ),
        "parameters_and_variants": (
            "Rule number 30, a single-black-cell seed, and finite stadium or "
            "endpaper display windows.",
            ["WE000001", "WE000004"],
        ),
        "excluded_observers_and_representations": (
            "People/cards, the stadium photograph, endpaper cropping, and "
            "retained prior rows are representations rather than extra native "
            "state or mechanics.",
            ["WE000001", "WE000004"],
        ),
        "evidence_limit": (
            "These bookends omit the Rule 30 lookup table and boundary "
            "convention; page 27/page 29 routes must supply them.",
            ["WE000001", "WE000004"],
        ),
    }
    missing = (
        "The exact Rule 30 lookup table, boundary/infinite-support convention, "
        "write/commit atomicity, external-input semantics, native completion, "
        "failure, and witness semantics are not stated in the Stage 4 sources."
    )
    return candidate(
        candidate_id="W0001",
        name="Rule 30 cellular automaton preset",
        aliases=["rule 30"],
        anchor_id="U004864",
        source_unit_ids=["U004864", "U004873"],
        source_evidence=[e1, e4],
        image_witnesses=[],
        supported=supported,
        parameters=[
            {
                "name": "rule number",
                "source_description": (
                    "The construction is explicitly named Rule 30; the rule "
                    "table is routed to page 27."
                ),
                "evidence_ids": ["WE000001"],
            },
            {
                "name": "display window",
                "source_description": (
                    "The endpapers show the first and next roughly 500 steps."
                ),
                "evidence_ids": ["WE000004"],
            },
        ],
        variants=[
            {
                "name": "single-black-cell initial condition",
                "source_description": (
                    "One black cell is used with all other cells white."
                ),
                "evidence_ids": ["WE000001", "WE000004"],
            }
        ],
        missing=missing,
        route_ids=["WR0001", "WR0004"],
    )


def rule_110_candidate() -> dict[str, Any]:
    e2_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "seed",
        "law_kind",
        "result_kind",
        "determinism_branching_or_measure",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    e3_fields = [
        "support",
        "visible_history",
        "result_kind",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    e2 = evidence(
        "WE000002",
        "WG000002",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U004871",
        source_unit_id="U004871",
        image_path=None,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="CAPTION",
        claim=(
            "The cover note names Rule 110, gives the two repeated binary "
            "domains forming its initial condition, reports 3000 displayed "
            "steps, and distinguishes growth and persistent-structure "
            "measurements from the rule itself."
        ),
        fields=e2_fields,
    )
    e3 = evidence(
        "WE000003",
        "WG000003",
        anchor_kind="IMAGE",
        anchor_id=RULE_110_IMAGE,
        source_unit_id="U004872",
        image_path=RULE_110_IMAGE,
        strength="CORROBORATING",
        modality="IMAGE",
        claim=(
            "Original-resolution inspection shows the stated long "
            "black/white cellular-automaton history and persistent structures; "
            "no transition table is transcribed from pixels."
        ),
        fields=e3_fields,
    )
    supported = {
        "object_kind": (
            "Named one-dimensional binary cellular-automaton preset.",
            ["WE000002"],
        ),
        "native_time": (
            "Discrete evolution steps.",
            ["WE000002"],
        ),
        "carrier": (
            "Cell positions carrying black/white values.",
            ["WE000002"],
        ),
        "support": (
            "A one-dimensional cellular row whose evolution is displayed as "
            "a long space-time diagram.",
            ["WE000002", "WE000003"],
        ),
        "alphabet_or_value_schema": (
            "Two values represented by empty and filled square symbols.",
            ["WE000002"],
        ),
        "visible_history": (
            "The illustration retains 3000 generations as a space-time "
            "history; this does not establish that the rule reads history.",
            ["WE000003"],
        ),
        "seed": (
            "An interface between repeats of □□□■■■■■ and repeats of "
            "■■■■■□□□.",
            ["WE000002"],
        ),
        "law_kind": (
            "A named deterministic local cellular-automaton rule.",
            ["WE000002"],
        ),
        "result_kind": (
            "A unique long evolution pattern with measured growth and "
            "persistent structures.",
            ["WE000002", "WE000003"],
        ),
        "determinism_branching_or_measure": (
            "The source presents one deterministic evolution; no branching "
            "or probability is described.",
            ["WE000002"],
        ),
        "parameters_and_variants": (
            "Rule number 110, the two-domain repeated initial condition, "
            "3000 displayed steps, and the cropped cover window.",
            ["WE000002"],
        ),
        "excluded_observers_and_representations": (
            "Cover cropping, growth rates, edge-period measurements, and "
            "persistent-structure counts describe or observe the evolution "
            "rather than alter its native rule.",
            ["WE000002", "WE000003"],
        ),
        "evidence_limit": (
            "The transition lookup and boundary convention are absent; page "
            "32 and page 292 routes must supply rule and structure details.",
            ["WE000002", "WE000003"],
        ),
    }
    missing = (
        "The exact Rule 110 lookup table, boundary/support convention, complete "
        "native state, activation/neighborhood details, write/commit atomicity, "
        "completion, failure, and witness semantics are not stated in the "
        "Stage 4 sources."
    )
    return candidate(
        candidate_id="W0002",
        name="Rule 110 cellular automaton preset",
        aliases=["rule 110"],
        anchor_id="U004871",
        source_unit_ids=["U004871", "U004872"],
        source_evidence=[e2, e3],
        image_witnesses=[RULE_110_IMAGE],
        supported=supported,
        parameters=[
            {
                "name": "rule number",
                "source_description": (
                    "The construction is explicitly named Rule 110; the "
                    "transition table is routed to page 32."
                ),
                "evidence_ids": ["WE000002"],
            },
            {
                "name": "initial condition",
                "source_description": (
                    "Two repeated binary blocks meet to form the displayed "
                    "initial condition."
                ),
                "evidence_ids": ["WE000002"],
            },
            {
                "name": "display window",
                "source_description": (
                    "The note distinguishes a 3000-step illustration from the "
                    "roughly 440-step cropped cover image."
                ),
                "evidence_ids": ["WE000002", "WE000003"],
            },
        ],
        variants=[],
        missing=missing,
        route_ids=["WR0002", "WR0003"],
    )


def route(
    route_id: str,
    source_unit_id: str,
    ordinal: int,
    literal_target: str,
    expected_topic: str,
    vocabulary: list[str],
) -> dict[str, str]:
    return {
        "route_id": route_id,
        "source_unit_id": source_unit_id,
        "source_asset_id": "",
        "discovery_epoch": "1",
        "discovery_kind": "SOURCE_UNIT",
        "discovery_id": source_unit_id,
        "discovery_ordinal": str(ordinal),
        "literal_target": literal_target,
        "route_kind": "PAGE",
        "expected_topic": expected_topic,
        "owning_stage": "4",
        "closure_scope": "CROSS_RANGE",
        "status": "PENDING",
        "target_unit_ids": "[]",
        "target_asset_ids": "[]",
        "attempts": "[]",
        "vocabulary_terms": compact(vocabulary),
        "defect_boundary": "",
    }


ROW_OVERRIDES: dict[str, tuple[str, list[str], str, str]] = {
    "U000024": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The copyright discussion treats illustrations, rule choices, and "
        "initial conditions as presentation/licensing subjects, not as a "
        "construction specification.",
    ),
    "U000025": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit describes licensing and execution of source-code "
        "representations; it specifies no Book construction.",
    ),
    "U000033": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "CONTROL_OR_COMPARISON"],
        "CLEAR",
        "The contents table is navigation over later assigned ranges and "
        "contains no mechanics.",
    ),
    "U000035": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION"],
        "CLEAR",
        "The Preface recalls an unspecified computer experiment without an "
        "identity or semantic law.",
    ),
    "U000041": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION"],
        "CLEAR",
        "The unit contrasts technical formalism with ordinary-language and "
        "picture exposition; it is about representation.",
    ),
    "U000044": (
        "APPLICATION_OR_EMULATION",
        ["OBSERVER_OR_ANALYZER", "CONTROL_OR_COMPARISON"],
        "CLEAR",
        "The unit says the Book's experiments can be reproduced, but names no "
        "specific system or mechanics.",
    ),
    "U000049": (
        "APPLICATION_OR_EMULATION",
        ["APPLICATION"],
        "CLEAR",
        "The unit forecasts conceptual and practical applications without "
        "specifying a model or formal mechanism.",
    ),
    "U000054": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "HISTORICAL_MENTION"],
        "CLEAR",
        "The unit identifies Mathematica as the author's research tool and "
        "gives no construction semantics.",
    ),
    "U000059": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The acknowledgments mention technical work and constructions only as "
        "credits, without anchored mechanics.",
    ),
    "U000061": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION"],
        "CLEAR",
        "Additive cellular automata, two-dimensional cellular automata, and "
        "cellular-automaton fluids occur only as historical collaboration "
        "topics; names alone do not satisfy candidate capture.",
    ),
    "U000068": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit reports aggregate computing effort and tooling, not a "
        "formal construction.",
    ),
    "U000069": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "SOURCE_DEFECT"],
        "AMBIGUOUS",
        "The final Preface image is an uncaptioned, pale "
        "cellular-automaton-like design; its rule, seed, and intended "
        "evidentiary role are not established.",
    ),
    "U004864": (
        "CANDIDATE",
        ["SEED_INPUT_OR_BOUNDARY", "EMULATION", "REPRESENTATION"],
        "CLEAR",
        "This unit discovers W0001 and partially specifies Rule 30 through a "
        "stadium/card emulation, single-black seed, synchronous rows, and a "
        "three-cell predecessor neighborhood; WR0001 routes the missing rule.",
    ),
    "U004866": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "EXTERNAL_ONLY"],
        "CLEAR",
        "The unit explains provenance conventions and an external website; it "
        "does not specify a construction.",
    ),
    "U004867": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "EXTERNAL_ONLY"],
        "CLEAR",
        "The unit describes citation practice and external reference search, "
        "not formal mechanics.",
    ),
    "U004868": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION"],
        "CLEAR",
        "The unit explains the purpose and limitations of historical notes "
        "without specifying a construction.",
    ),
    "U004870": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION"],
        "CLEAR",
        "The autobiographical note is historical context only.",
    ),
    "U004871": (
        "CANDIDATE",
        ["SEED_INPUT_OR_BOUNDARY", "BEHAVIOR_OR_OUTCOME", "REPRESENTATION"],
        "CLEAR",
        "This unit discovers W0002, names Rule 110, gives its two-domain "
        "repeated seed and display parameters, and routes the rule and "
        "persistent-structure definitions through WR0002 and WR0003.",
    ),
    "U004872": (
        "SUPPORTS_CANDIDATE",
        ["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"],
        "CLEAR",
        "The original-resolution image is native visual evidence for W0002's "
        "long Rule 110 evolution; no rule table is inferred from pixels.",
    ),
    "U004873": (
        "SUPPORTS_CANDIDATE",
        ["SEED_INPUT_OR_BOUNDARY", "REPRESENTATION"],
        "CLEAR",
        "The endpaper note supports W0001 with a single-black-cell seed and "
        "finite display windows; WR0004 routes the missing page-29 context.",
    ),
    "U004874": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "OBSERVER_OR_ANALYZER"],
        "CLEAR",
        "The unit concerns color-induced visual artifacts and therefore an "
        "observer/representation issue, not a new generator.",
    ),
    "U004875": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit describes how diagrams and photographs were produced.",
    ),
    "U004876": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit explains adaptable picture layout and display sizing, not "
        "native construction mechanics.",
    ),
    "U004878": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "REPRESENTATION"],
        "CLEAR",
        "The MIF/Mathematica/FrameMaker/PDF pipeline is Book-production "
        "tooling and not a scientific construction under audit.",
    ),
    "U004879": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit concerns physical printing fidelity for dense cell images.",
    ),
    "U004880": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "OBSERVER_OR_ANALYZER", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The index is described as a navigation/analysis representation built "
        "with automated tooling, not as a native construction.",
    ),
    "U004881": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "HISTORICAL_MENTION"],
        "CLEAR",
        "The unit documents personal-name normalization in the index.",
    ),
    "U004882": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit explicitly frames Mathematica as executable notation for "
        "objects, rules, procedures, and algorithms; notation is not promoted "
        "to a separate Book construction.",
    ),
    "U004883": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "EXTERNAL_ONLY", "HISTORICAL_MENTION"],
        "CLEAR",
        "Mathematica is introduced as an external computing language and "
        "environment, not a construction studied by the Book.",
    ),
    "U004884": (
        "NO_CONSTRUCTION",
        ["EXTERNAL_ONLY"],
        "CLEAR",
        "The unit gives external product availability information.",
    ),
    "U004885": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "EXTERNAL_ONLY"],
        "CLEAR",
        "The unit names external books about Mathematica.",
    ),
    "U004886": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "EXTERNAL_ONLY"],
        "CLEAR",
        "Symbolic programming is described as a property of the external "
        "Mathematica language, without a Book construction law.",
    ),
    "U004887": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "EXTERNAL_ONLY"],
        "CLEAR",
        "The unit records software-version compatibility for note programs.",
    ),
    "U004888": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit introduces incidental notation examples used to read later "
        "notes.",
    ),
    "U004889": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The heading labels an incidental notation/tool example.",
    ),
    "U004890": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "Nest and Fold examples demonstrate external language notation; they "
        "are not Book construction candidates.",
    ),
    "U004891": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The heading labels incidental functional-operation syntax.",
    ),
    "U004892": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The examples give denotations of external language primitives only "
        "to establish notation.",
    ),
    "U004893": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The heading labels incidental list-manipulation syntax.",
    ),
    "U004894": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The list operations are incidental executable-notation examples and "
        "not systems studied by the Book.",
    ),
    "U004895": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The heading labels incidental transformation-rule syntax.",
    ),
    "U004896": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The replacement examples establish notation for later programs; they "
        "do not introduce a separately studied rewrite system.",
    ),
    "U004897": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The heading labels incidental numerical-function syntax.",
    ),
    "U004898": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The numerical primitives are notation/tool examples rather than "
        "coverage-bearing Book constructions.",
    ),
    "U004899": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit introduces a StandardForm/InputForm notation table.",
    ),
    "U004900": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The table maps typeset symbols to keyboard notation.",
    ),
    "U004901": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL", "EXTERNAL_ONLY"],
        "CLEAR",
        "The unit discusses reading, executing, testing, and rewriting note "
        "programs as implementation artifacts.",
    ),
    "U004902": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit records hardware, languages, and execution history for the "
        "author's experiments.",
    ),
    "U004907": (
        "APPLICATION_OR_EMULATION",
        ["APPLICATION", "SEED_INPUT_OR_BOUNDARY", "CONTROL_OR_COMPARISON"],
        "CLEAR",
        "A randomly selected cellular-automaton rule is only a hypothetical "
        "educational experiment; no particular rule or law is anchored.",
    ),
    "U004909": (
        "REPRESENTATION_OR_OBSERVER",
        ["CONTROL_OR_COMPARISON"],
        "CLEAR",
        "The unit gives reading/navigation guidance across chapters.",
    ),
    "U004912": (
        "APPLICATION_OR_EMULATION",
        ["APPLICATION", "OBSERVER_OR_ANALYZER"],
        "CLEAR",
        "The unit recommends computer experiments as a learning method but "
        "does not specify a particular formal system.",
    ),
    "U004913": (
        "APPLICATION_OR_EMULATION",
        ["APPLICATION", "OBSERVER_OR_ANALYZER", "CONTROL_OR_COMPARISON"],
        "CLEAR",
        "The unit describes experimental extension, observation, and "
        "comparison methodology without an anchored construction.",
    ),
    "U004914": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "EXTERNAL_ONLY"],
        "CLEAR",
        "The unit recommends learning Mathematica as external tooling.",
    ),
    "U004917": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION"],
        "CLEAR",
        "Cellular automata occur as a general research domain, without a "
        "specific rule or semantic law.",
    ),
    "U004918": (
        "NO_CONSTRUCTION",
        ["EXTERNAL_ONLY", "APPLICATION"],
        "CLEAR",
        "The unit describes a future external question list and research "
        "activities.",
    ),
    "U004919": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit discusses research skills and Mathematica programming, not "
        "a formal construction.",
    ),
    "U004923": (
        "APPLICATION_OR_EMULATION",
        ["APPLICATION"],
        "CLEAR",
        "The unit discusses the difficulty of building application models "
        "without specifying one; page 364 is not needed to identify a "
        "construction here.",
    ),
    "U014293": (
        "NO_CONSTRUCTION",
        ["IMPLEMENTATION_DETAIL", "REPRESENTATION"],
        "CLEAR",
        "The colophon describes the Book's production and graphics pipeline.",
    ),
    "U014294": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION"],
        "CLEAR",
        "The unit lists fonts used to represent the Book.",
    ),
    "U014295": (
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "IMPLEMENTATION_DETAIL"],
        "CLEAR",
        "The unit specifies printing and binding parameters, not a scientific "
        "construction.",
    ),
    "U014309": (
        "HISTORICAL_ONLY",
        ["HISTORICAL_MENTION", "REPRESENTATION"],
        "CLEAR",
        "The unit records image provenance and photograph credits.",
    ),
}


def default_statement(path: str) -> str:
    if path == EXPECTED_PATHS[0]:
        return (
            "Reviewed in full; this publication/contents unit is "
            "bibliographic, legal, or navigational and supplies no anchored "
            "construction mechanics."
        )
    if path == EXPECTED_PATHS[1]:
        return (
            "Reviewed in full; this Preface unit is framing, biography, "
            "acknowledgment, or general methodology without an identity plus "
            "semantic law."
        )
    if path == EXPECTED_PATHS[2]:
        return (
            "Reviewed in full; this General Notes unit is exposition, "
            "history, tooling, education, or application context without a "
            "candidate-level semantic anchor."
        )
    return (
        "Reviewed in full; this Colophon unit is production metadata or "
        "credits without construction mechanics."
    )


def build_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    if (
        manifest.get("worker_id") != EXPECTED_WORKER
        or manifest.get("content_set_sha256") != EXPECTED_CONTENT_SET
        or manifest.get("source_paths") != EXPECTED_PATHS
        or manifest.get("source_unit_count") != 157
        or manifest.get("asset_count") != 2
        or manifest.get("stage") != 4
        or manifest.get("discovery_epoch") != 1
    ):
        raise AuthoringError("bundle is not the exact Stage 4 epoch-1 assignment")

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

    candidate_links = {
        "U004864": ["W0001"],
        "U004871": ["W0002"],
        "U004872": ["W0002"],
        "U004873": ["W0001"],
    }
    route_links = {
        "U004864": ["WR0001"],
        "U004871": ["WR0002", "WR0003"],
        "U004873": ["WR0004"],
    }
    reading_updates: list[dict[str, str]] = []
    for original in reading_input:
        row = deepcopy(original)
        unit_id = row["source_unit_id"]
        disposition, secondary, status, statement = ROW_OVERRIDES.get(
            unit_id,
            (
                "NO_CONSTRUCTION",
                [],
                "CLEAR",
                default_statement(row["path"]),
            ),
        )
        uncertainty = (
            "The uncaptioned image resembles a cellular-automaton evolution, "
            "but the source does not identify its rule, seed, or intended "
            "semantic role."
            if unit_id == "U000069"
            else ""
        )
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": disposition,
                "source_status": status,
                "uncertainty": uncertainty,
                "secondary_roles": compact(secondary),
                "candidate_ids": compact(candidate_links.get(unit_id, [])),
                "route_ids": compact(route_links.get(unit_id, [])),
                "evidence_statement": statement,
                "review_stage": "4",
                "reviewer": EXPECTED_WORKER,
            }
        )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in asset_input:
        row = deepcopy(original)
        if row["physical_path"] == RULE_110_IMAGE:
            row.update(
                {
                    "inspection_status": "SCREENED",
                    "review_epoch": "1",
                    "visual_role": "NATIVE_EVIDENCE",
                    "source_status": "CLEAR",
                    "risk_flags": compact(["CONSTRUCTION_BEARING"]),
                    "original_resolution_status": "REVIEWED",
                    "transcription_status": "NOT_REQUIRED",
                    "candidate_ids": compact(["W0002"]),
                    "route_ids": "[]",
                    "evidence_statement": (
                        "Inspected at original resolution: the image shows the "
                        "long binary evolution described by U004871 and "
                        "corroborates W0002; no exact rule is inferred from "
                        "pixels."
                    ),
                    "review_stage": "4",
                    "reviewer": EXPECTED_WORKER,
                    "uncertainty": "",
                }
            )
        elif row["physical_path"] == PREFACE_IMAGE:
            row.update(
                {
                    "inspection_status": "SCREENED",
                    "review_epoch": "1",
                    "visual_role": "DECORATIVE",
                    "source_status": "AMBIGUOUS",
                    "risk_flags": compact(
                        [
                            "CONSTRUCTION_BEARING",
                            "AMBIGUOUS",
                            "CAPTION_INCOMPLETE",
                        ]
                    ),
                    "original_resolution_status": "REVIEWED",
                    "transcription_status": "NOT_APPLICABLE",
                    "candidate_ids": "[]",
                    "route_ids": "[]",
                    "evidence_statement": (
                        "Inspected at original resolution: a pale, "
                        "cellular-automaton-like decorative pattern is visible, "
                        "but no caption establishes a rule, seed, or mechanics."
                    ),
                    "review_stage": "4",
                    "reviewer": EXPECTED_WORKER,
                    "uncertainty": (
                        "The image is construction-like but uncaptioned; exact "
                        "identity and intended role are not recoverable from "
                        "the Stage 4 source."
                    ),
                }
            )
        else:
            raise AuthoringError(f"unexpected Stage 4 asset: {row['physical_path']}")
        asset_updates.append(row)

    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": [
                rule_30_candidate(),
                rule_110_candidate(),
            ],
            "asset_updates": asset_updates,
            "route_proposals": [
                route(
                    "WR0001",
                    "U004864",
                    1,
                    "the simple rule on page 27",
                    "Rule 30 transition lookup and boundary convention",
                    ["rule 30", "cellular automaton"],
                ),
                route(
                    "WR0002",
                    "U004871",
                    1,
                    "the rule 110 cellular automaton discussed on page 32",
                    "Rule 110 transition lookup and native update mechanics",
                    ["rule 110", "cellular automaton"],
                ),
                route(
                    "WR0003",
                    "U004871",
                    2,
                    "11 of the 15 kinds from page 292",
                    "persistent-structure definitions and their relation to "
                    "Rule 110 behavior",
                    ["persistent structures", "rule 110"],
                ),
                route(
                    "WR0004",
                    "U004873",
                    1,
                    "the rule 30 cellular automaton of page 29",
                    "Rule 30 single-cell evolution and displayed boundary "
                    "context",
                    ["rule 30", "single black cell"],
                ),
            ],
            "uncertainties": [
                (
                    "A001607/U000069 is an uncaptioned "
                    "cellular-automaton-like Preface image. It remains an "
                    "explicit ambiguous representation and is not used as "
                    "candidate mechanics evidence."
                )
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
    except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"bookends authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "recorded Stage 4 bookends review: "
        "reading=157 assets=2 candidates=2 routes=4 declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
