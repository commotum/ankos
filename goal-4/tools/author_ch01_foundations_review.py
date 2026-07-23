#!/usr/bin/env python3
"""Record the completed, source-grounded Stage 5 Chapter 1 review.

The script is deliberately bound to the exact sealed epoch-1 Chapter 1
bundle.  It records the author's unit-by-unit judgments after sequential
reading and original-resolution image inspection; it supplies no defaults to
any other stage and refuses to overwrite non-scaffold worker output.
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
    "5936f6eda19d95daa95512d478151cd7b325c9d6f84b56b9f5382562689ea350"
)
EXPECTED_WORKER = "ch01-foundations-reader-e1"
EXPECTED_PATHS = [
    "CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science.md",
    "BACK-MATTER/NOTES/01-The-Foundations-for-a-New-Kind-of-Science-Notes.md",
]
CHAPTER_IMAGE = "CHAPTERS/_page_16_Picture_0.jpeg"
PHYSICS_COVER = "CHAPTERS/_page_32_Picture_8.jpeg"
PRINT_OUT = "CHAPTERS/_page_34_Figure_9.jpeg"


class AuthoringError(ValueError):
    """The exact Stage 5 assignment or worksheet is not safe to update."""


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
    source_unit_id: str,
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
    uncertainties: list[str] | None = None,
) -> dict[str, Any]:
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
        "discovery_stage": 5,
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
        "field_support": {
            field: "SUPPORTED" if field in supported else "UNKNOWN_FROM_SOURCE"
            for field in FINGERPRINT_FIELDS
        },
        "fingerprint": fingerprint,
        "parameters": parameters,
        "variants": variants,
        "missing_mechanics": [missing],
        "uncertainties": uncertainties or [],
        "related_candidate_ids": [],
        "cross_reference_ids": route_ids,
        "evidence_reassignments": [],
    }
    return {field: values[field] for field in CANDIDATE_FIELDS}


def elementary_experiment_candidate() -> dict[str, Any]:
    e1 = evidence(
        "WE000001",
        "WG000001",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U000149",
        source_unit_id="U000149",
        image_path=None,
        strength="DIRECT_IDENTITY",
        modality="PROSE",
        claim=(
            "The personal history delimits the 1981 experiment as a systematic "
            "run over all programs of one particular simple type."
        ),
        fields=["object_kind", "parameters_and_variants", "evidence_limit"],
    )
    e2 = evidence(
        "WE000002",
        "WG000002",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U000150",
        source_unit_id="U000150",
        image_path=None,
        strength="CONTEXTUAL",
        modality="PROSE",
        claim=(
            "The surrounding prose identifies the printed patterns as typical "
            "output of that experiment and records emergent complexity as an "
            "observed result, not an extra native law."
        ),
        fields=[
            "visible_history",
            "result_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    e3 = evidence(
        "WE000003",
        "WG000003",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U000153",
        source_unit_id="U000153",
        image_path=None,
        strength="DIRECT_IDENTITY",
        modality="PROSE",
        claim=(
            "The later co-reference identifies systems similar to those in "
            "the experiment as cellular automata."
        ),
        fields=["object_kind", "law_kind", "evidence_limit"],
    )
    e4 = evidence(
        "WE000004",
        "WG000004",
        anchor_kind="IMAGE",
        anchor_id=PRINT_OUT,
        source_unit_id="U000151",
        image_path=PRINT_OUT,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="IMAGE",
        claim=(
            "Original-resolution inspection shows multiple rule-labelled "
            "binary row evolutions with successive rows retained as histories; "
            "no lookup tables or boundary convention are inferred from pixels."
        ),
        fields=[
            "native_time",
            "carrier",
            "support",
            "alphabet_or_value_schema",
            "visible_history",
            "law_kind",
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    e7 = evidence(
        "WE000007",
        "WG000007",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U004953",
        source_unit_id="U004953",
        image_path=None,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="CAPTION",
        claim=(
            "The Notes identify the printouts as a series of elementary "
            "cellular automata started from random initial conditions and "
            "route fuller mechanics to page 232."
        ),
        fields=[
            "object_kind",
            "seed",
            "law_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    supported = {
        "object_kind": (
            "A systematically sampled series of elementary cellular automata.",
            ["WE000001", "WE000003", "WE000007"],
        ),
        "native_time": (
            "Discrete successive rows are shown in the printed evolutions.",
            ["WE000004"],
        ),
        "carrier": (
            "Black or white cells arranged in rows.",
            ["WE000004"],
        ),
        "support": (
            "One-dimensional cell rows displayed as two-dimensional "
            "space-time histories.",
            ["WE000004"],
        ),
        "alphabet_or_value_schema": (
            "Two visually distinct cell values, printed as dots and blanks.",
            ["WE000004"],
        ),
        "visible_history": (
            "The printout retains each successive row below its predecessor.",
            ["WE000002", "WE000004"],
        ),
        "seed": (
            "Random initial conditions.",
            ["WE000007"],
        ),
        "law_kind": (
            "Rule-labelled elementary cellular-automaton laws.",
            ["WE000003", "WE000004", "WE000007"],
        ),
        "result_kind": (
            "One printed evolution history for each sampled rule.",
            ["WE000002", "WE000004"],
        ),
        "parameters_and_variants": (
            "The varied rule in the series and the random initial condition.",
            ["WE000001", "WE000004", "WE000007"],
        ),
        "excluded_observers_and_representations": (
            "The C/VAX implementation, printout layout, retained history, and "
            "visual complexity are representation, implementation, or "
            "observed behavior rather than additional native mechanics.",
            ["WE000002", "WE000004", "WE000007"],
        ),
        "evidence_limit": (
            "Chapter 1 does not give the neighborhood, rule encoding, update "
            "schedule, boundary, or exact members of the displayed series.",
            ["WE000001", "WE000002", "WE000003", "WE000004", "WE000007"],
        ),
    }
    missing = (
        "The exact rule set and lookup encoding, neighborhood, complete state, "
        "frontier, synchronous/other schedule, boundary convention, commit "
        "semantics, and completion semantics are not stated in Chapter 1."
    )
    return candidate(
        candidate_id="W0001",
        name="1981 elementary-cellular-automaton experiment series",
        aliases=["1981 computer printouts", "elementary cellular automata"],
        anchor_id="U000149",
        source_unit_ids=[
            "U000149",
            "U000150",
            "U000151",
            "U000153",
            "U004953",
        ],
        source_evidence=[e1, e2, e3, e4, e7],
        image_witnesses=[PRINT_OUT],
        supported=supported,
        parameters=[
            {
                "name": "rule",
                "source_description": (
                    "The experiment systematically varies the elementary "
                    "cellular-automaton rule."
                ),
                "evidence_ids": ["WE000001", "WE000004", "WE000007"],
            }
        ],
        variants=[
            {
                "name": "random initial condition",
                "source_description": (
                    "The displayed elementary cellular automata are started "
                    "from random initial conditions."
                ),
                "evidence_ids": ["WE000007"],
            }
        ],
        missing=missing,
        route_ids=["WR0007"],
    )


def disk_simulation_candidate() -> dict[str, Any]:
    e5 = evidence(
        "WE000005",
        "WG000005",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U004951",
        source_unit_id="U004951",
        image_path=None,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="PROSE",
        claim=(
            "The Notes specify 40 idealized molecular disks bouncing in a "
            "box, randomized initial positions and velocities from a "
            "middle-square generator, a roughly ten-collision-time run, and "
            "a 64-bit roundoff limit."
        ),
        fields=[
            "object_kind",
            "native_time",
            "carrier",
            "support",
            "topology",
            "alphabet_or_value_schema",
            "complete_state",
            "seed",
            "boundary",
            "external_data",
            "law_kind",
            "result_kind",
            "termination_completion_failure",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    supported = {
        "object_kind": (
            "A finite hard-disk-like statistical-physics simulation preset.",
            ["WE000005"],
        ),
        "native_time": (
            "Motion is followed for about ten collision times.",
            ["WE000005"],
        ),
        "carrier": (
            "Forty disks representing idealized molecules.",
            ["WE000005"],
        ),
        "support": (
            "A bounded two-dimensional box.",
            ["WE000005"],
        ),
        "topology": (
            "Continuous geometric positions inside a box with disk contacts.",
            ["WE000005"],
        ),
        "alphabet_or_value_schema": (
            "Each disk has numerical position and velocity data.",
            ["WE000005"],
        ),
        "complete_state": (
            "The positions and velocities of all 40 disks.",
            ["WE000005"],
        ),
        "seed": (
            "Positions and velocities supplied by a middle-square random "
            "number generator.",
            ["WE000005"],
        ),
        "boundary": (
            "The disks are confined to and bounce around in a box; exact wall "
            "collision equations are omitted.",
            ["WE000005"],
        ),
        "external_data": (
            "A random digit sequence determines the initial numerical state.",
            ["WE000005"],
        ),
        "law_kind": (
            "Molecular disks move and undergo collisions/bounces.",
            ["WE000005"],
        ),
        "result_kind": (
            "A finite motion history exhibiting increasing randomization.",
            ["WE000005"],
        ),
        "termination_completion_failure": (
            "The reported run ends after about ten collision times when "
            "64-bit roundoff error has become too large.",
            ["WE000005"],
        ),
        "parameters_and_variants": (
            "Forty disks, 64-bit numerical values, randomized initial state, "
            "and an approximately ten-collision-time observation window.",
            ["WE000005"],
        ),
        "excluded_observers_and_representations": (
            "The oscilloscope/cover pictures and the observed randomization "
            "do not add native state or laws.",
            ["WE000005"],
        ),
        "evidence_limit": (
            "The exact free-motion, disk-collision, and wall-collision "
            "equations and numerical event schedule are not supplied.",
            ["WE000005"],
        ),
    }
    missing = (
        "The exact collision response, disk geometry, wall law, event "
        "schedule, numerical integrator/event handling, determinism under "
        "ties, and witness semantics are not stated."
    )
    return candidate(
        candidate_id="W0002",
        name="1964 forty-disk statistical-physics simulation preset",
        aliases=["statistical physics cover simulation", "40 bouncing disks"],
        anchor_id="U004951",
        source_unit_ids=["U004951"],
        source_evidence=[e5],
        image_witnesses=[],
        supported=supported,
        parameters=[
            {
                "name": "disk count",
                "source_description": "The simulation uses 40 disks.",
                "evidence_ids": ["WE000005"],
            },
            {
                "name": "numeric precision",
                "source_description": "Positions and velocities use 64-bit numbers.",
                "evidence_ids": ["WE000005"],
            },
        ],
        variants=[
            {
                "name": "middle-square randomized seed",
                "source_description": (
                    "Initial positions and velocities come from a middle-square "
                    "random number generator."
                ),
                "evidence_ids": ["WE000005"],
            }
        ],
        missing=missing,
        route_ids=["WR0004", "WR0005"],
    )


def particle_ca_candidate() -> dict[str, Any]:
    e6 = evidence(
        "WE000006",
        "WG000006",
        anchor_kind="SOURCE_UNIT",
        anchor_id="U004952",
        source_unit_id="U004952",
        image_path=None,
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="PROSE",
        claim=(
            "The Notes identify the 1973 experiment as a two-dimensional "
            "cellular automaton with discrete particles colliding on a square "
            "grid, constrained by physics-like conservation laws, and route "
            "further details to page 999."
        ),
        fields=[
            "object_kind",
            "carrier",
            "support",
            "topology",
            "structural_invariants",
            "complete_state",
            "law_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        ],
    )
    supported = {
        "object_kind": (
            "A two-dimensional particle cellular automaton.",
            ["WE000006"],
        ),
        "carrier": (
            "Discrete particles represented on cellular sites.",
            ["WE000006"],
        ),
        "support": (
            "A two-dimensional square grid.",
            ["WE000006"],
        ),
        "topology": (
            "Square-grid cellular adjacency; the precise neighborhood is not "
            "given.",
            ["WE000006"],
        ),
        "structural_invariants": (
            "Physics-like conservation laws constrain the construction.",
            ["WE000006"],
        ),
        "complete_state": (
            "A grid configuration of discrete particles, with any direction "
            "or collision-state fields left unspecified.",
            ["WE000006"],
        ),
        "law_kind": (
            "Particles collide according to an unspecified cellular-automaton "
            "law.",
            ["WE000006"],
        ),
        "parameters_and_variants": (
            "Square-grid geometry and the imposition of physics-like "
            "conservation laws are coverage-bearing choices.",
            ["WE000006"],
        ),
        "excluded_observers_and_representations": (
            "The Elliott 903 hardware, assembly program size, and teleprinter "
            "output are implementation or representation details.",
            ["WE000006"],
        ),
        "evidence_limit": (
            "No particle alphabet, collision table, propagation schedule, "
            "boundary, or exact conservation law is supplied.",
            ["WE000006"],
        ),
    }
    missing = (
        "The particle value schema, exact collision/propagation lookup, "
        "neighborhood, frontier, schedule, boundary, commit semantics, "
        "conserved quantities, and completion semantics are not stated."
    )
    return candidate(
        candidate_id="W0003",
        name="1973 two-dimensional particle cellular automaton",
        aliases=["1973 computer experiment", "square-grid particle automaton"],
        anchor_id="U004952",
        source_unit_ids=["U004952"],
        source_evidence=[e6],
        image_witnesses=[],
        supported=supported,
        parameters=[
            {
                "name": "grid geometry",
                "source_description": "The reported experiment uses a square grid.",
                "evidence_ids": ["WE000006"],
            }
        ],
        variants=[
            {
                "name": "physics-like conservation restriction",
                "source_description": (
                    "The experiment was designed to respect physics-like "
                    "conservation laws."
                ),
                "evidence_ids": ["WE000006"],
            }
        ],
        missing=missing,
        route_ids=["WR0006"],
    )


def route(
    route_id: str,
    source_unit_id: str,
    ordinal: int,
    literal_target: str,
    expected_topic: str,
    vocabulary: list[str],
    route_kind: str = "PAGE",
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
        "route_kind": route_kind,
        "expected_topic": expected_topic,
        "owning_stage": "5",
        "closure_scope": "CROSS_RANGE",
        "status": "PENDING",
        "target_unit_ids": "[]",
        "target_asset_ids": "[]",
        "attempts": "[]",
        "vocabulary_terms": compact(vocabulary),
        "defect_boundary": "",
    }


ROW_OVERRIDES: dict[str, tuple[str, list[str], str]] = {}


def add_rows(
    ids: list[str],
    disposition: str,
    secondary: list[str],
    statement: str,
) -> None:
    for unit_id in ids:
        ROW_OVERRIDES[unit_id] = (disposition, secondary, statement)


add_rows(
    [f"U000{i:03d}" for i in range(100, 116)],
    "APPLICATION_OR_EMULATION",
    ["APPLICATION", "CONTROL_OR_COMPARISON"],
    (
        "This relations-to-other-areas unit discusses applications, scope, or "
        "comparison with another discipline without specifying a new native law."
    ),
)
add_rows(
    [f"U000{i:03d}" for i in range(117, 135)],
    "HISTORICAL_ONLY",
    ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
    (
        "This survey-of-past-initiatives unit names a field or model family "
        "historically and comparatively but does not delimit reproducible "
        "candidate mechanics."
    ),
)
add_rows(
    [
        "U000136",
        "U000139",
        "U000140",
        "U000141",
        "U000142",
        "U000143",
        "U000144",
        "U000145",
        "U000146",
        "U000147",
        "U000148",
    ],
    "HISTORICAL_ONLY",
    ["HISTORICAL_MENTION", "IMPLEMENTATION_DETAIL"],
    (
        "This autobiographical unit supplies provenance, motivation, or "
        "research-method context; any named system here lacks candidate-level "
        "mechanics in this unit."
    ),
)
add_rows(
    ["U000137", "U000138"],
    "REPRESENTATION_OR_OBSERVER",
    ["REPRESENTATION", "CONTROL_OR_COMPARISON"],
    (
        "The textbook-cover image or caption represents the historical "
        "randomization example; its mechanics are not established here."
    ),
)
ROW_OVERRIDES.update(
    {
        "U000149": (
            "CANDIDATE",
            ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
            (
                "This unit discovers W0001 by delimiting the 1981 systematic "
                "experiment over every program of one particular simple type."
            ),
        ),
        "U000150": (
            "SUPPORTS_CANDIDATE",
            ["BEHAVIOR_OR_OUTCOME", "REPRESENTATION"],
            (
                "The prose supports W0001 by identifying the adjacent "
                "printout as typical output and records complexity only as an "
                "observed result."
            ),
        ),
        "U000151": (
            "SUPPORTS_CANDIDATE",
            ["REPRESENTATION"],
            (
                "The image-bearing unit supports W0001 through the screened "
                "original printout; exact rule tables are not inferred."
            ),
        ),
        "U000152": (
            "REPRESENTATION_OR_OBSERVER",
            ["REPRESENTATION", "HISTORICAL_MENTION"],
            (
                "The caption identifies the image as a reproduction of a "
                "historical printout but supplies no additional native "
                "mechanics."
            ),
        ),
        "U000153": (
            "SUPPORTS_CANDIDATE",
            ["HISTORICAL_MENTION"],
            (
                "The historical prose supplies W0001's cellular-automaton "
                "co-reference without adding a transition table."
            ),
        ),
        "U004928": (
            "CROSS_REFERENCE",
            ["REPRESENTATION", "PROPERTY_OR_RESTRICTION"],
            (
                "The unit contrasts equations that state static facts with "
                "action rules and WR0001 routes the promised extension at "
                "page 793."
            ),
        ),
        "U004932": (
            "CROSS_REFERENCE",
            ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
            (
                "Traditional logic is presented as a narrow formal rule "
                "system; WR0002 routes the source's page-806 comparison."
            ),
        ),
        "U004946": (
            "CROSS_REFERENCE",
            ["CONTROL_OR_COMPARISON"],
            (
                "The unit names Turing machines and register machines only "
                "as Chapter 3 examples; WR0003 routes their mechanics to that "
                "assigned range."
            ),
        ),
        "U004951": (
            "CANDIDATE",
            [
                "SEED_INPUT_OR_BOUNDARY",
                "BEHAVIOR_OR_OUTCOME",
                "REPRESENTATION",
            ],
            (
                "This unit discovers W0002, specifying forty bouncing disks, "
                "a box, randomized positions and velocities, a collision-time "
                "run limit, and WR0004/WR0005."
            ),
        ),
        "U004952": (
            "CANDIDATE",
            ["PROPERTY_OR_RESTRICTION", "HISTORICAL_MENTION"],
            (
                "This unit discovers W0003 as a two-dimensional particle "
                "cellular automaton on a square grid with physics-like "
                "conservation constraints; WR0006 routes page 999."
            ),
        ),
        "U004953": (
            "SUPPORTS_CANDIDATE",
            [
                "SEED_INPUT_OR_BOUNDARY",
                "REPRESENTATION",
                "HISTORICAL_MENTION",
            ],
            (
                "The note supports W0001 by identifying elementary cellular "
                "automata with random initial conditions; WR0007 routes page "
                "232 for fuller mechanics."
            ),
        ),
    }
)
add_rows(
    [
        "U004926",
        "U004927",
        "U004929",
        "U004930",
        "U004933",
        "U004934",
        "U004935",
        "U004936",
        "U004937",
        "U004938",
        "U004939",
        "U004940",
    ],
    "HISTORICAL_ONLY",
    ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
    (
        "The Notes unit is historical or conceptual context; names of "
        "external fields and model families are not accompanied by a "
        "delimited native law."
    ),
)
add_rows(
    [f"U004{i:03d}" for i in range(942, 950)],
    "REPRESENTATION_OR_OBSERVER",
    ["REPRESENTATION", "CONTROL_OR_COMPARISON"],
    (
        "This relations-to-other-areas note is navigational coverage guidance "
        "rather than a construction specification."
    ),
)
add_rows(
    [f"U004{i:03d}" for i in range(954, 962)],
    "HISTORICAL_ONLY",
    ["HISTORICAL_MENTION", "IMPLEMENTATION_DETAIL"],
    (
        "This timeline or detailed-history unit records chronology and "
        "implementation provenance without construction mechanics."
    ),
)


def default_statement(path: str) -> str:
    if path == EXPECTED_PATHS[0]:
        return (
            "Reviewed in full; this Chapter 1 unit is conceptual framing, a "
            "heading, or general methodology without both a delimited identity "
            "and native semantic anchor."
        )
    return (
        "Reviewed in full; this Chapter 1 Notes unit is a heading, navigation, "
        "or contextual statement without a candidate-level law."
    )


def build_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    manifest = json.loads(
        (bundle / "allowed-manifest.json").read_text(encoding="utf-8")
    )
    if (
        manifest.get("worker_id") != EXPECTED_WORKER
        or manifest.get("content_set_sha256") != EXPECTED_CONTENT_SET
        or manifest.get("source_paths") != EXPECTED_PATHS
        or manifest.get("source_unit_count") != 142
        or manifest.get("asset_count") != 3
        or manifest.get("stage") != 5
        or manifest.get("discovery_epoch") != 1
    ):
        raise AuthoringError("bundle is not the exact Stage 5 epoch-1 assignment")

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
        "U000149": ["W0001"],
        "U000150": ["W0001"],
        "U000151": ["W0001"],
        "U000153": ["W0001"],
        "U004951": ["W0002"],
        "U004952": ["W0003"],
        "U004953": ["W0001"],
    }
    route_links = {
        "U004928": ["WR0001"],
        "U004932": ["WR0002"],
        "U004946": ["WR0003"],
        "U004951": ["WR0004", "WR0005"],
        "U004952": ["WR0006"],
        "U004953": ["WR0007"],
    }
    reading_updates: list[dict[str, str]] = []
    for original in reading_input:
        row = deepcopy(original)
        unit_id = row["source_unit_id"]
        disposition, secondary, statement = ROW_OVERRIDES.get(
            unit_id,
            ("NO_CONSTRUCTION", [], default_statement(row["path"])),
        )
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": disposition,
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": compact(secondary),
                "candidate_ids": compact(candidate_links.get(unit_id, [])),
                "route_ids": compact(route_links.get(unit_id, [])),
                "evidence_statement": statement,
                "review_stage": "5",
                "reviewer": EXPECTED_WORKER,
            }
        )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in asset_input:
        row = deepcopy(original)
        common = {
            "inspection_status": "SCREENED",
            "review_epoch": "1",
            "source_status": "CLEAR",
            "original_resolution_status": "REVIEWED",
            "review_stage": "5",
            "reviewer": EXPECTED_WORKER,
            "uncertainty": "",
            "route_ids": "[]",
        }
        if row["physical_path"] == CHAPTER_IMAGE:
            row.update(
                {
                    **common,
                    "visual_role": "DECORATIVE",
                    "risk_flags": "[]",
                    "transcription_status": "NOT_REQUIRED",
                    "candidate_ids": "[]",
                    "evidence_statement": (
                        "Original-resolution inspection shows a decorative "
                        "Chapter 1 numeral over a faint cellular texture; no "
                        "rule, seed, or mechanics are asserted."
                    ),
                }
            )
        elif row["physical_path"] == PHYSICS_COVER:
            row.update(
                {
                    **common,
                    "visual_role": "CONTROL",
                    "risk_flags": compact(["CONSTRUCTION_BEARING", "TEXT_BEARING"]),
                    "transcription_status": "CHECKED",
                    "candidate_ids": "[]",
                    "evidence_statement": (
                        "Original-resolution inspection confirms a textbook "
                        "cover with successive disk configurations and the "
                        "title 'statistical physics'; it is a historical "
                        "comparison image, while U004951 separately supplies "
                        "the partial mechanics."
                    ),
                }
            )
        elif row["physical_path"] == PRINT_OUT:
            row.update(
                {
                    **common,
                    "visual_role": "NATIVE_EVIDENCE",
                    "risk_flags": compact(["CONSTRUCTION_BEARING", "TEXT_BEARING"]),
                    "transcription_status": "CHECKED",
                    "candidate_ids": compact(["W0001"]),
                    "evidence_statement": (
                        "Original-resolution inspection shows multiple "
                        "rule-labelled binary cellular histories and supports "
                        "W0001; exact lookup tables and boundaries are not "
                        "inferred from the pixels."
                    ),
                }
            )
        else:
            raise AuthoringError(f"unexpected Stage 5 asset: {row['physical_path']}")
        asset_updates.append(row)

    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": [
                elementary_experiment_candidate(),
                disk_simulation_candidate(),
                particle_ca_candidate(),
            ],
            "asset_updates": asset_updates,
            "route_proposals": [
                route(
                    "WR0001",
                    "U004928",
                    1,
                    "see page 793",
                    "static equations/formal facts versus action rules",
                    ["equations", "statically state facts", "rules define actions"],
                ),
                route(
                    "WR0002",
                    "U004932",
                    1,
                    "as we will see on page 806",
                    "traditional logic rules compared with general simple-program rules",
                    ["traditional logic", "logical rules", "page 806"],
                ),
                route(
                    "WR0003",
                    "U004946",
                    1,
                    "Chapter 3 uses standard computer science models",
                    "Turing-machine and register-machine native mechanics",
                    ["Turing machines", "register machines"],
                    route_kind="SECTION",
                ),
                route(
                    "WR0004",
                    "U004951",
                    1,
                    "middle-square random number generator (see page 975)",
                    "middle-square initial-state generator mechanics",
                    ["middle-square", "random number generator"],
                ),
                route(
                    "WR0005",
                    "U004951",
                    2,
                    "See page 441",
                    "random-input versus intrinsic-randomness comparison",
                    ["random initial conditions", "randomization", "statistical physics"],
                ),
                route(
                    "WR0006",
                    "U004952",
                    1,
                    "See page 999",
                    "1973 two-dimensional particle cellular-automaton mechanics",
                    ["2D cellular automaton", "discrete particles", "square grid"],
                ),
                route(
                    "WR0007",
                    "U004953",
                    1,
                    "see page 232",
                    "elementary cellular automata with random initial conditions",
                    ["elementary cellular automata", "random initial conditions"],
                ),
            ],
            "uncertainties": [],
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
        print(f"Chapter 1 authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "recorded Stage 5 Chapter 1 review: "
        "reading=142 assets=3 candidates=3 routes=7 declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
