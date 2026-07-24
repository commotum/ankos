#!/usr/bin/env python3
"""Deterministically author the blind Stage 9 CH05 main-text review bundle.

This helper intentionally contains the complete semantic inventory.  It never
falls back to a default disposition, visual role, candidate, or route.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


WORKER_ID = "ch05-dimensions-main-reader-e2"
STAGE = "9"
EPOCH = "2"
REVIEWER = WORKER_ID
SOURCE_PATH = "CHAPTERS/05-Two-Dimensions-and-Beyond.md"
EXPECTED_BUNDLE_SHA = "c24385f9a8116f9b5fe0e7b02781ad3ee7a8b5bda5bea2ea8f5290aa239a327e"
EXPECTED_PROMPT_SHA = "b07f7cb1657c5b43b395424d78f6bf4404b0631312aef6b85dd9782651c33781"
EXPECTED_SCHEMA_SHA = "0dc082f9e1e434ca8c6c1839320044a89a18772c6179d831940fc35dd5955a17"
EXPECTED_MANIFEST_SHA = "8039afe30feab7af0c86ab21e7bb809ed00b5e7f0064ca8b7ce3ddfb87d7f585"

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

STATUSES = {
    "SUPPORTED",
    "NOT_APPLICABLE",
    "UNKNOWN_FROM_SOURCE",
    "CONFLICTING_SOURCE",
}

# Prose units that state a complete executable law or complete native
# constraint for every candidate to which they are attached. Fenced code is
# treated the same way when evidence records are built.
DIRECT_COMPLETE_SOURCE_UNITS = {
    "U000966",
    "U000968",
    "U000982",
    "U000989",
    "U001099",
    "U001104",
    "U001162",
    "U001166",
    "U001173",
}

# These units identify, summarize, or visualize already-delimited systems; they
# do not independently state the native transition or constraint mechanics.
SOURCE_EVIDENCE_OVERRIDES = {
    "U000997": (
        "CONTEXTUAL",
        {
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001031": (
        "CONTEXTUAL",
        {
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001053": (
        "DIRECT_PARTIAL_MECHANICS",
        {
            "topology",
            "structural_invariants",
            "read_dependencies_or_neighborhood",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001071": (
        "DIRECT_PARTIAL_MECHANICS",
        {
            "object_kind",
            "carrier",
            "structural_invariants",
            "alphabet_or_value_schema",
            "complete_state",
            "parameters_and_variants",
            "evidence_limit",
        },
    ),
    "U001090": (
        "DIRECT_PARTIAL_MECHANICS",
        {
            "object_kind",
            "carrier",
            "structural_invariants",
            "alphabet_or_value_schema",
            "complete_state",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001094": (
        "DIRECT_PARTIAL_MECHANICS",
        {
            "object_kind",
            "native_time",
            "frontier_or_activation",
            "read_dependencies_or_neighborhood",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "result_kind",
            "parameters_and_variants",
            "evidence_limit",
        },
    ),
    "U001121": (
        "CONTEXTUAL",
        {
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001134": (
        "CORROBORATING",
        {
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001139": (
        "CORROBORATING",
        {
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001150": (
        "DIRECT_IDENTITY",
        {
            "object_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
    "U001158": (
        "CONTEXTUAL",
        {
            "result_kind",
            "parameters_and_variants",
            "excluded_observers_and_representations",
            "evidence_limit",
        },
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_json_array(value: str) -> list[str]:
    result = json.loads(value)
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    return result


def load_bundle(bundle: Path) -> dict[str, Any]:
    manifest_path = bundle / "allowed-manifest.json"
    assert sha256(manifest_path) == EXPECTED_MANIFEST_SHA
    manifest = json.loads(manifest_path.read_text())
    assert manifest["worker_id"] == WORKER_ID
    assert manifest["stage"] == 9
    assert manifest["discovery_epoch"] == 2
    assert manifest["content_set_sha256"] == EXPECTED_BUNDLE_SHA
    assert manifest["prompt_sha256"] == EXPECTED_PROMPT_SHA
    assert manifest["schema_sha256"] == EXPECTED_SCHEMA_SHA
    assert manifest["source_paths"] == [SOURCE_PATH]
    assert manifest["source_unit_count"] == 276
    assert manifest["asset_count"] == 80
    for item in manifest["allowed_inputs"]:
        path = bundle / item["path"]
        assert path.is_file(), path
        assert path.stat().st_size == item["bytes"], path
        assert sha256(path) == item["sha256"], path

    with (bundle / "input/reading-input.csv").open(newline="") as handle:
        readings = list(csv.DictReader(handle))
    with (bundle / "input/asset-input.csv").open(newline="") as handle:
        assets = list(csv.DictReader(handle))
    units = [
        json.loads(line)
        for line in (bundle / "input/source-units.jsonl").read_text().splitlines()
    ]
    source = (
        bundle / "input/sources/CHAPTERS/05-Two-Dimensions-and-Beyond.md"
    ).read_bytes()
    assert [row["source_unit_id"] for row in readings] == [u["id"] for u in units]
    assert readings[0]["source_unit_id"] == "U000947"
    assert readings[-1]["source_unit_id"] == "U001222"
    assert assets[0]["asset_id"] == "A000843"
    assert assets[-1]["asset_id"] == "A000922"
    assert all(row["review_status"] == "PENDING" for row in readings)
    assert all(row["inspection_status"] == "PENDING" for row in assets)
    assert all(as_json_array(row["candidate_ids"]) == [] for row in readings)
    assert all(as_json_array(row["route_ids"]) == [] for row in readings)
    assert all(as_json_array(row["candidate_ids"]) == [] for row in assets)
    assert all(as_json_array(row["route_ids"]) == [] for row in assets)
    asset_by_path = {a["physical_path"]: a for a in assets}
    assert len(asset_by_path) == len(assets)
    return {
        "manifest": manifest,
        "readings": readings,
        "assets": assets,
        "units": units,
        "source": source,
        "unit_by_id": {u["id"]: u for u in units},
        "asset_by_id": {a["asset_id"]: a for a in assets},
        "asset_by_path": asset_by_path,
    }


def unit_text(state: dict[str, Any], unit_id: str) -> str:
    unit = state["unit_by_id"][unit_id]
    text = state["source"][unit["byte_start"] : unit["byte_end"]].decode("utf-8")
    return " ".join(text.replace("```text", "").replace("```", "").split())


def excerpt(state: dict[str, Any], unit_id: str, limit: int = 210) -> str:
    text = unit_text(state, unit_id)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def profile_blueprint(
    kind: str,
    name: str,
    overrides: dict[str, tuple[str, str | None]] | None = None,
) -> dict[str, dict[str, Any]]:
    """Return a complete typed fingerprint blueprint for one explicit kind."""

    supported: dict[str, str] = {}
    na: set[str] = set()
    unknown: set[str] = set()

    if kind in {"CA2", "CA3"}:
        dimension = "two-dimensional" if kind == "CA2" else "three-dimensional"
        supported = {
            "object_kind": "cellular automaton",
            "native_time": "discrete successive steps",
            "carrier": f"{dimension} regular cell array",
            "support": "the finite active pattern explicitly shown at each finite stage",
            "topology": f"{dimension} grid/lattice topology",
            "structural_invariants": "carrier adjacency is fixed while cell values update",
            "alphabet_or_value_schema": "black/white cell values",
            "complete_state": "all cell values at one step",
            "frontier_or_activation": "all cells are eligible for synchronous update",
            "schedule": "synchronous parallel update",
            "read_dependencies_or_neighborhood": "explicit neighbor set around each cell",
            "law_kind": "deterministic local transition rule",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "replace each cell value with its rule result",
            "result_kind": "one successor cell array",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "dimension, neighborhood, rule code/predicate, and seed as stated",
            "excluded_observers_and_representations": "rendered growth shapes, slices, stacked histories, and measured radii are observations",
            "evidence_limit": "only mechanics explicitly stated or checked in the assigned source are asserted",
        }
        na = {"visible_history", "control_state", "input", "external_data"}
        na.update({"termination_completion_failure", "witness_semantics"})
        unknown = {"seed", "boundary"}
    elif kind == "TM2":
        supported = {
            "object_kind": "two-dimensional Turing machine",
            "native_time": "discrete successive head transitions",
            "carrier": "two-dimensional grid of writable cells plus one head",
            "support": "finite visited region on an otherwise uniform grid",
            "topology": "four-direction square grid",
            "structural_invariants": "one head occupies one cell and the grid adjacency remains fixed",
            "alphabet_or_value_schema": "black/white cell values and a finite head-state alphabet",
            "complete_state": "grid values, head position, and head state",
            "control_state": "head state",
            "seed": "all cells initially white with one initial head state and position",
            "frontier_or_activation": "the single head location",
            "schedule": "one head transition per step",
            "read_dependencies_or_neighborhood": "current head state and current cell color",
            "law_kind": "deterministic read/write/state/move transition",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "write the current cell, update head state, and move in one of four directions",
            "result_kind": "one successor machine state",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "number of head states and checked transition strip",
            "excluded_observers_and_representations": "the plotted visited region and head path are observers",
            "evidence_limit": "graphic transition cases are not assigned semantics beyond their checked symbols",
        }
        na = {
            "visible_history",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
    elif kind == "SUB_GENERAL":
        supported = {
            "object_kind": "two-dimensional substitution system",
            "native_time": "discrete replacement steps",
            "carrier": "a two-dimensional collection of replaceable square elements",
            "support": "a finite pattern of elements",
            "structural_invariants": "the same replacement template is reused for every matching element",
            "complete_state": "the current collection, placement, and types of elements",
            "frontier_or_activation": "all elements eligible under the replacement rule",
            "schedule": "parallel replacement at every step",
            "read_dependencies_or_neighborhood": "the individual element for the noninteracting family introduced here",
            "law_kind": "deterministic structural replacement rule",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "replace every matched element by its specified subpattern",
            "result_kind": "one successor pattern",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "element types, replacement templates, and placement geometry",
            "excluded_observers_and_representations": "nested appearance and rendered stages are outcomes",
            "evidence_limit": "the generic introduction does not choose fixed-grid versus free geometry, a seed, or a complete alphabet",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
        unknown = {"topology", "alphabet_or_value_schema", "seed"}
    elif kind == "SUB_GEOM_GENERAL":
        supported = {
            "object_kind": "geometrical replacement/fractal system",
            "native_time": "discrete repeated geometrical replacement steps",
            "carrier": "geometrical black-square elements placed in the plane",
            "support": "a finite collection of geometrical square elements",
            "topology": "free geometrical placement in the plane rather than a fixed grid",
            "structural_invariants": "the same geometrical replacement rule is reused for every element",
            "alphabet_or_value_schema": "black square elements",
            "complete_state": "the current squares together with their geometrical placement and scale",
            "frontier_or_activation": "all current elements eligible under the repeated replacement rule",
            "schedule": "parallel replacement at each step",
            "read_dependencies_or_neighborhood": "the replaced element alone; the source explicitly excludes dependence on other elements",
            "law_kind": "deterministic noninteracting geometrical replacement rule",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "replace each black square by two or more smaller black squares in the stated geometry",
            "result_kind": "one successor geometrical pattern",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "number, relative scale, and placement of the smaller black squares",
            "excluded_observers_and_representations": "nested appearance and rendered stages are outcomes; neighbor interaction is explicitly absent",
            "evidence_limit": "only the stated black-square, noninteracting geometrical replacement mechanics are asserted; no family seed is established",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
        unknown = {"seed"}
    elif kind == "SUB_GRID_NEIGHBOR":
        supported = {
            "object_kind": "two-dimensional neighbor-dependent substitution system",
            "native_time": "discrete replacement steps",
            "carrier": "black/white cells on a fixed two-dimensional grid",
            "support": "the finite wrapped grid used by the rule",
            "topology": "square grid wrapping in both dimensions",
            "structural_invariants": "grid adjacency and extent remain fixed while cell values are replaced",
            "alphabet_or_value_schema": "black/white cell values shown by the checked rule panels",
            "complete_state": "all cell values on the wrapped grid at one step",
            "boundary": "the grid wraps in both dimensions",
            "frontier_or_activation": "all grid cells are eligible for parallel replacement",
            "schedule": "parallel replacement at every step",
            "read_dependencies_or_neighborhood": "the cell and the neighboring grid cells selected by the rule",
            "law_kind": "deterministic neighbor-dependent grid replacement rule",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "replace each grid-cell value according to its old local neighborhood",
            "result_kind": "one successor wrapped-grid pattern",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "local neighborhood, replacement table, and wrapped-grid extent",
            "excluded_observers_and_representations": "rendered stages and sequential scan orders are not native mechanics",
            "evidence_limit": "only the wrapped-grid neighbor-dependent mechanics shown by the checked source and rule panels are asserted; no generic seed is established",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
        unknown = {"seed"}
    elif kind in {"SUB_GRID", "SUB_GEOM"}:
        carrier = (
            "two-dimensional grid of colored square elements"
            if kind == "SUB_GRID"
            else "oriented geometrical square elements in the plane"
        )
        topology = (
            "fixed square grid, with wrapping where explicitly stated"
            if kind == "SUB_GRID"
            else "geometrical placement and orientation rather than a fixed grid"
        )
        read_dependencies = (
            "the individual grid element alone"
            if kind == "SUB_GRID"
            else "the individual geometrical element alone; neighboring-element interaction is absent"
        )
        supported = {
            "object_kind": "two-dimensional substitution system",
            "native_time": "discrete replacement steps",
            "carrier": carrier,
            "support": "finite collection/pattern of square elements",
            "topology": topology,
            "structural_invariants": "replacement templates are reused at every occurrence",
            "alphabet_or_value_schema": "black/white or oriented square types shown by the rule",
            "complete_state": "the current collection and types/orientations of elements",
            "seed": "a single black square unless another seed is stated",
            "frontier_or_activation": "all elements eligible under the parallel replacement rule",
            "schedule": "parallel replacement at every step",
            "read_dependencies_or_neighborhood": read_dependencies,
            "law_kind": "deterministic structural replacement rule",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "replace each matched element by the displayed smaller-element template",
            "result_kind": "one successor pattern",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "replacement geometry, orientation, colors, and neighborhood dependence as shown",
            "excluded_observers_and_representations": "nested appearance and rendered stages are outcomes",
            "evidence_limit": "unshown metric coordinates and collision policies are not inferred",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
    elif kind == "GRAPH":
        supported = {
            "object_kind": "directed graph/network object",
            "native_time": "none; immutable graph identity",
            "carrier": "nodes and directed outgoing connections",
            "support": "finite graph or explicitly delimited infinite graph family",
            "topology": "connection incidence, independent of drawing coordinates",
            "structural_invariants": "graph identity ignores node labels/layout as stated",
            "alphabet_or_value_schema": "identical nodes with two distinguished outgoing connections where stated",
            "complete_state": "the complete connection relation",
            "law_kind": "declarative graph specification",
            "rule_relation_constraint_function_or_probability_law": name,
            "result_kind": "graph or graph-isomorphism class",
            "witness_semantics": "the checked drawing witnesses incidence but its coordinates are non-semantic",
            "parameters_and_variants": "dimension, branching, node count, or nesting as stated",
            "excluded_observers_and_representations": "node positions and line-above/line-below page layouts are representations",
            "evidence_limit": "only incidence distinctions visible in the source and caption are asserted",
        }
        na = {
            "visible_history",
            "control_state",
            "seed",
            "input",
            "boundary",
            "external_data",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "termination_completion_failure",
        }
    elif kind == "NETWORK_GENERAL":
        supported = {
            "object_kind": "network evolution system",
            "native_time": "discrete successive network states",
            "carrier": "nodes and connections between nodes",
            "topology": "connection incidence independent of drawing layout",
            "structural_invariants": "node coordinates and drawn wire geometry are non-semantic",
            "alphabet_or_value_schema": "nodes and connection identities; connection arity is not fixed by the general family",
            "complete_state": "the nodes and complete connection relation at one step",
            "law_kind": "network connection-update rule",
            "rule_relation_constraint_function_or_probability_law": "a supplied rule specifying how connections change from one step to the next",
            "write_replacement_assembly_or_commit": "update the network connection relation as specified by the rule",
            "result_kind": "a successor network",
            "parameters_and_variants": "connection arity and connection-update rule",
            "excluded_observers_and_representations": "node positions and wire layout in a drawing are representations",
            "evidence_limit": "the introductory family does not yet fix arity, seed, local dependency, schedule, or determinism",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
        unknown = {
            "support",
            "seed",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "successor_cardinality",
            "determinism_branching_or_measure",
        }
    elif kind == "NETWORK_BINARY_GENERAL":
        supported = {
            "object_kind": "binary-outdegree network-system restriction",
            "native_time": "discrete successive network states",
            "carrier": "nodes with exactly two outgoing connection slots",
            "structural_invariants": "every node has exactly two outgoing connections, each targeting another node or itself",
            "alphabet_or_value_schema": "identical nodes and two outgoing connection slots",
            "complete_state": "all nodes and both outgoing targets for every node",
            "frontier_or_activation": "the outgoing connections of each node are eligible for local rerouting",
            "read_dependencies_or_neighborhood": "the local connection structure around the node, as selected by a supplied rule",
            "law_kind": "local network connection-rerouting rule",
            "rule_relation_constraint_function_or_probability_law": "a supplied local rerouting rule restricted to networks with two outgoing connections per node",
            "write_replacement_assembly_or_commit": "reroute outgoing connections according to the supplied local rule",
            "result_kind": "a successor binary-outdegree network",
            "parameters_and_variants": "the two-outgoing restriction and the supplied local rerouting rule",
            "excluded_observers_and_representations": "node layout and nested drawings are representations, not mechanics",
            "evidence_limit": "only the two-outgoing restriction and generic local rerouting described here are asserted; support, topology, seed, schedule, successor count, and determinism remain unknown",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
        unknown = {
            "support",
            "topology",
            "seed",
            "schedule",
            "successor_cardinality",
            "determinism_branching_or_measure",
        }
    elif kind == "NETWORK":
        supported = {
            "object_kind": "network evolution system",
            "native_time": "discrete successive network states",
            "carrier": "nodes with two distinguished outgoing connections",
            "support": "finite reachable network component",
            "topology": "connection incidence independent of drawing layout",
            "structural_invariants": "each retained node has two outgoing connection slots",
            "alphabet_or_value_schema": "identical nodes; connection slots labelled above/1 and below/2",
            "complete_state": "all retained nodes and both outgoing targets per node",
            "seed": "single-node network where stated",
            "frontier_or_activation": "every retained node is evaluated",
            "schedule": "parallel per-node rerouting/replacement each step",
            "read_dependencies_or_neighborhood": "connection paths or local distinct-node counts stated by the rule",
            "law_kind": "deterministic graph rewrite/rerouting rule",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "reroute connections and optionally insert nodes; retain the component containing the first node",
            "result_kind": "one successor network",
            "successor_cardinality": "one",
            "determinism_branching_or_measure": "deterministic",
            "parameters_and_variants": "path expressions, conditional cases, insertion pattern, or distance-two counts",
            "excluded_observers_and_representations": "linear page layout, gray ancestry lines, and node-count plots are representations/observers",
            "evidence_limit": "rules shown only graphically remain expressed at the checked-symbol level",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
    elif kind == "MULTIWAY":
        supported = {
            "object_kind": "multiway string-replacement system",
            "native_time": "discrete breadth-wise replacement steps",
            "carrier": "collection of finite element sequences",
            "support": "all distinct sequences generated at the current step",
            "topology": "one-dimensional sequence adjacency within each state and a branching state graph across steps",
            "structural_invariants": "identical successor sequences are deduplicated while all distinct results are retained",
            "alphabet_or_value_schema": "one- or two-color sequence elements shown by the rule",
            "complete_state": "the full set of distinct sequences at a step",
            "seed": "the explicitly shown initial sequence",
            "frontier_or_activation": "all applicable replacement occurrences in all current states",
            "schedule": "all possible single replacements are generated for each step",
            "read_dependencies_or_neighborhood": "matched sequence block",
            "law_kind": "nondeterministic replacement relation with exhaustive branching",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "replace one matched block; union and deduplicate all resulting sequences",
            "result_kind": "set of distinct successor sequences",
            "successor_cardinality": "zero, one, or multiple distinct successors per state",
            "determinism_branching_or_measure": "exhaustive branching without a probability measure",
            "parameters_and_variants": "replacement set and initial sequence",
            "excluded_observers_and_representations": "tree layout, state counts, differences, and single-occurrence graph layout are observers/representations",
            "evidence_limit": "graphic replacement glyphs are retained without inventing unstated symbol names",
        }
        na = {
            "visible_history",
            "control_state",
            "input",
            "boundary",
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
    elif kind == "TRANSITION_RELATION":
        supported = {
            "object_kind": "derived state-transition relation/representation",
            "native_time": "none; an immutable relation derived from the multiway evolution",
            "carrier": "distinct finite sequences as nodes and one-step generation links as directed edges",
            "support": "the sequences and transition links reached from the stated seed under the stated replacement system",
            "topology": "directed sequence-to-sequence transition network",
            "structural_invariants": "each distinct sequence is represented once, with repeated generation shown by links to the same node",
            "alphabet_or_value_schema": "the sequence elements of the represented multiway system",
            "complete_state": "the derived directed relation between represented sequences",
            "law_kind": "derived one-step reachability relation",
            "rule_relation_constraint_function_or_probability_law": "an edge connects a sequence to every distinct sequence produced by one allowed native replacement",
            "result_kind": "an immutable directed transition network/relation",
            "witness_semantics": "each node witnesses one reached sequence and each edge witnesses one native one-step generation relation",
            "parameters_and_variants": "the represented replacement set, seed, and accumulated reachability extent",
            "excluded_observers_and_representations": "breadth-wise layer placement, duplicate drawings of the same sequence, and page geometry are presentation choices; the relation is not the native successor set",
            "evidence_limit": "the source establishes the relation for the displayed multiway system without asserting completion of an infinite transitive closure",
        }
        na = {
            "visible_history",
            "control_state",
            "seed",
            "input",
            "boundary",
            "external_data",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "determinism_branching_or_measure",
            "termination_completion_failure",
        }
    elif kind == "CONSTRAINT_GENERAL":
        supported = {
            "object_kind": "constraint-defined model set",
            "native_time": "none; the source contrasts constraints with explicit evolution rules",
            "structural_invariants": "every accepted object satisfies the stated constraints",
            "law_kind": "declarative constraint relation",
            "rule_relation_constraint_function_or_probability_law": "a supplied set of constraints to satisfy",
            "result_kind": "the set of objects that satisfy the constraints",
            "determinism_branching_or_measure": "declarative solution set rather than a probability law",
            "witness_semantics": "an object satisfying the stated constraints is an accepted model",
            "parameters_and_variants": "the object domain and constraints",
            "excluded_observers_and_representations": "a procedure for finding a model is separate from the constraint itself",
            "evidence_limit": "the introductory passage does not yet restrict the carrier, value schema, locality, or solution-set cardinality",
        }
        na = {
            "visible_history",
            "control_state",
            "seed",
            "input",
            "external_data",
            "frontier_or_activation",
            "schedule",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "termination_completion_failure",
        }
        unknown = {
            "carrier",
            "support",
            "topology",
            "alphabet_or_value_schema",
            "complete_state",
            "boundary",
            "read_dependencies_or_neighborhood",
        }
    elif kind in {
        "CONSTRAINT_1D",
        "CONSTRAINT_NEIGHBOR2D",
        "CONSTRAINT_TEMPLATE_CROSS",
        "CONSTRAINT_TEMPLATE_REQUIRED",
        "CONSTRAINT_TEMPLATE_3X3",
        "CONSTRAINT_TEMPLATE_3X3_REQUIRED",
    }:
        constraint_profiles = {
            "CONSTRAINT_1D": {
                "carrier": "one-dimensional line of cells",
                "support": "a complete infinite line coloring",
                "topology": "two nearest neighbors on a line",
                "boundary": "unbounded one-dimensional line",
                "read": "the center cell and its two nearest neighbors as stated",
                "law": "one-dimensional local neighbor constraint",
                "parameters": "the permitted relation between a cell and its two neighbors",
                "witness": "a complete infinite line coloring that satisfies the relation at every cell",
            },
            "CONSTRAINT_NEIGHBOR2D": {
                "carrier": "two-dimensional square grid of cells",
                "support": "a complete infinite grid coloring",
                "topology": "four orthogonal nearest neighbors",
                "boundary": "unbounded grid; wrapping in a displayed finite tile is a representation of periodicity",
                "read": "the center cell and its four orthogonal neighbors",
                "law": "two-dimensional black/white neighbor-count constraint",
                "parameters": "the required black/white neighbor counts for black and white center cells",
                "witness": "a complete infinite grid coloring that satisfies both count conditions at every cell",
            },
            "CONSTRAINT_TEMPLATE_CROSS": {
                "carrier": "two-dimensional square grid of cells",
                "support": "a complete infinite grid coloring",
                "topology": "overlapping center-plus-four-orthogonal-neighbor templates",
                "boundary": "unbounded two-dimensional grid",
                "read": "the center cell and its four orthogonal neighbors",
                "law": "overlapping allowed-cross-template constraint",
                "parameters": "the allowed set of five-cell cross templates",
                "witness": "a complete infinite grid coloring whose cross neighborhood at every cell is allowed",
            },
            "CONSTRAINT_TEMPLATE_REQUIRED": {
                "carrier": "two-dimensional square grid of cells",
                "support": "a complete infinite grid coloring",
                "topology": "overlapping center-plus-four-orthogonal-neighbor templates",
                "boundary": "unbounded two-dimensional grid",
                "read": "the center cell and its four orthogonal neighbors",
                "law": "allowed-cross-template constraint plus one required template occurrence",
                "parameters": "the allowed cross-template set and the designated template that must occur",
                "witness": "a complete infinite grid coloring that uses only allowed cross templates and contains the required one",
            },
            "CONSTRAINT_TEMPLATE_3X3": {
                "carrier": "two-dimensional square grid of cells",
                "support": "a complete infinite grid coloring",
                "topology": "overlapping complete 3 × 3 blocks including diagonals",
                "boundary": "unbounded two-dimensional grid",
                "read": "the complete 3 × 3 neighborhood centered at each cell",
                "law": "overlapping allowed-3 × 3-template constraint",
                "parameters": "the allowed 3 × 3 template set",
                "witness": "a complete infinite grid coloring whose every 3 × 3 block is allowed",
            },
            "CONSTRAINT_TEMPLATE_3X3_REQUIRED": {
                "carrier": "two-dimensional square grid of cells",
                "support": "a complete infinite grid coloring",
                "topology": "overlapping complete 3 × 3 blocks including diagonals",
                "boundary": "unbounded two-dimensional grid",
                "read": "the complete 3 × 3 neighborhood centered at each cell",
                "law": "overlapping allowed-3 × 3-template constraint plus one required template occurrence",
                "parameters": "the allowed 3 × 3 template set and the designated template that must occur",
                "witness": "a complete infinite grid coloring whose every 3 × 3 block is allowed and that contains the required template",
            },
        }
        constraint_profile = constraint_profiles[kind]
        supported = {
            "object_kind": "constraint-defined model set",
            "native_time": "none; declarative satisfaction relation",
            "carrier": constraint_profile["carrier"],
            "support": constraint_profile["support"],
            "topology": constraint_profile["topology"],
            "structural_invariants": "the same local constraint applies at every cell",
            "alphabet_or_value_schema": "black/white cell values",
            "complete_state": "a complete cell assignment",
            "boundary": constraint_profile["boundary"],
            "frontier_or_activation": "every cell must satisfy the relation",
            "read_dependencies_or_neighborhood": constraint_profile["read"],
            "law_kind": constraint_profile["law"],
            "rule_relation_constraint_function_or_probability_law": name,
            "result_kind": "the set of complete satisfying assignments",
            "determinism_branching_or_measure": "declarative solution set without probability measure",
            "witness_semantics": constraint_profile["witness"],
            "parameters_and_variants": constraint_profile["parameters"],
            "excluded_observers_and_representations": "search order, gray unknown cells, tessellation rendering, and CA correspondence are not the native constraint",
            "evidence_limit": "only the stated or independently checked local relation is asserted; numeric codes are not treated as decoded laws",
        }
        na = {
            "visible_history",
            "control_state",
            "seed",
            "input",
            "external_data",
            "schedule",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "termination_completion_failure",
        }
    elif kind == "WITNESS":
        supported = {
            "object_kind": "finite universal witness set for a constraint family",
            "native_time": "none; immutable finite collection",
            "carrier": "two-dimensional periodic black/white cell patterns",
            "support": "171 explicitly enumerated periodic patterns",
            "topology": "two-dimensional square grid",
            "structural_invariants": "rotations, reflections, and global black/white interchange are quotient symmetries",
            "alphabet_or_value_schema": "black/white cells",
            "complete_state": "one complete periodic pattern together with its period",
            "law_kind": "declarative coverage relation",
            "rule_relation_constraint_function_or_probability_law": name,
            "result_kind": "finite set of satisfying-pattern witnesses",
            "termination_completion_failure": "if none of the 171 witnesses satisfies a constraint in scope, no pattern satisfies it",
            "witness_semantics": "each member is a positive satisfying witness for the minimal labelled constraint and possibly others",
            "parameters_and_variants": "minimal constraint labels and quotient symmetries",
            "excluded_observers_and_representations": "page ordering and rendered tile size are presentation choices",
            "evidence_limit": "the assigned source asserts completeness for the stated template-constraint family only",
        }
        na = {
            "visible_history",
            "control_state",
            "seed",
            "input",
            "boundary",
            "external_data",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "determinism_branching_or_measure",
        }
    elif kind == "SOLVER_ENUMERATION":
        supported = {
            "object_kind": "exhaustive complete-pattern constraint solver",
            "native_time": "successive complete-pattern trials",
            "carrier": "complete finite cell assignments over a fixed region",
            "support": "the fixed finite region being tested",
            "topology": "the constraint carrier's local grid",
            "structural_invariants": "every trial assigns every cell in the same finite region",
            "alphabet_or_value_schema": "black/white cell values",
            "complete_state": "the current complete candidate pattern and enumeration position",
            "input": "a local constraint specification and finite region",
            "frontier_or_activation": "the next complete candidate pattern in the enumeration",
            "schedule": "enumerate every complete pattern and test each against the constraint",
            "read_dependencies_or_neighborhood": "all local constraint checks across the complete candidate",
            "law_kind": "exhaustive enumerate-and-test search",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "advance to another complete candidate; retain candidates that satisfy the constraint",
            "result_kind": "one or more satisfying complete patterns, or exhaustion with none",
            "successor_cardinality": "one next trial for a chosen enumeration order",
            "determinism_branching_or_measure": "exhaustive coverage; enumeration order is unspecified",
            "termination_completion_failure": "finite exhaustion establishes that no assignment over the tested region satisfies the constraint",
            "witness_semantics": "a satisfying complete pattern is a positive witness; exhaustive failure is a finite negative result",
            "parameters_and_variants": "finite region size and enumeration order",
            "excluded_observers_and_representations": "the astronomical search cost is a performance property, not a native transition",
            "evidence_limit": "the source gives no enumeration order, pruning rule, region-growth step, or backtracking mechanic",
        }
        na = {
            "visible_history",
            "control_state",
            "boundary",
            "external_data",
        }
        unknown = {"seed"}
    elif kind == "SOLVER":
        supported = {
            "object_kind": "constraint-satisfaction search procedure",
            "native_time": "iterative search stages",
            "carrier": "partial finite cell assignments",
            "support": "a growing finite region",
            "topology": "the constraint carrier's local grid",
            "structural_invariants": "assigned cells obey all currently decidable constraints",
            "alphabet_or_value_schema": "black, white, and unresolved cell states",
            "complete_state": "partial assignment plus search/backtracking state",
            "seed": "a small deduced region or enumerated initial candidate",
            "input": "a local constraint specification",
            "frontier_or_activation": "the next unresolved cell/pattern choice",
            "schedule": "iterative choice, propagation, and optional backtracking",
            "read_dependencies_or_neighborhood": "currently constrained neighboring cells/templates",
            "law_kind": "deterministic enumeration/search strategy with branching choices",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "extend a partial assignment; reject and backtrack when a constraint fails",
            "result_kind": "satisfying witness, finite refutation, or unresolved search",
            "successor_cardinality": "multiple trial branches may be generated",
            "determinism_branching_or_measure": "branching search without probability measure",
            "termination_completion_failure": "completion yields a witness or finite impossibility proof; search may become impractical",
            "witness_semantics": "a complete assignment is a positive witness and an unsatisfiable finite region is a negative witness",
            "parameters_and_variants": "enumeration order, region growth, propagation, and backtracking",
            "excluded_observers_and_representations": "gray cell rendering and stage snapshots are visualization",
            "evidence_limit": "the source gives a strategy, not a fully specified implementation or tie-breaking policy",
        }
        na = {"visible_history", "control_state", "boundary", "external_data"}
    else:
        raise AssertionError(kind)

    if overrides:
        for field, (status, value) in overrides.items():
            supported.pop(field, None)
            na.discard(field)
            unknown.discard(field)
            assert status in STATUSES
            if status == "SUPPORTED":
                assert value is not None
                supported[field] = value
            elif status == "NOT_APPLICABLE":
                assert value is None
                na.add(field)
            else:
                assert value is None
                unknown.add(field)

    assert not (set(supported) & na)
    assert not (set(supported) & unknown)
    assert not (na & unknown)
    unassigned = set(FIELDS) - set(supported) - na - unknown
    # A typed profile deliberately treats fields not meaningful to the object as
    # N/A; this is profile construction, not a candidate-level semantic fallback.
    na.update(unassigned)

    blueprint: dict[str, dict[str, Any]] = {}
    for field in FIELDS:
        if field in supported:
            blueprint[field] = {
                "status": "SUPPORTED",
                "value": supported[field],
                "reason": "The assigned canonical source directly supports this field.",
            }
        elif field in unknown:
            blueprint[field] = {
                "status": "UNKNOWN_FROM_SOURCE",
                "value": None,
                "reason": f"The assigned source does not establish {field} for this candidate.",
            }
        else:
            blueprint[field] = {
                "status": "NOT_APPLICABLE",
                "value": None,
                "reason": f"{field} is not a native field for this candidate as delimited.",
            }
    return blueprint


def build_candidate_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []

    def add(
        name: str,
        kind: str,
        anchor_kind: str,
        anchor_id: str,
        ordinal: int,
        units: list[str],
        assets: list[str] | None = None,
        *,
        aliases: list[str] | None = None,
        parameters: dict[str, str] | None = None,
        variants: dict[str, str] | None = None,
        overrides: dict[str, tuple[str, str | None]] | None = None,
        parent_index: int | None = None,
        route_keys: list[str] | None = None,
    ) -> int:
        specs.append(
            {
                "name": name,
                "kind": kind,
                "anchor_kind": anchor_kind,
                "anchor_id": anchor_id,
                "ordinal": ordinal,
                "units": units,
                "assets": assets or [],
                "aliases": aliases or [],
                "parameters": parameters or {},
                "variants": variants or {},
                "overrides": overrides or {},
                "parent_index": parent_index,
                "route_keys": route_keys or [],
            }
        )
        return len(specs)

    ca2 = add(
        "two-dimensional totalistic cellular-automaton family",
        "CA2",
        "SOURCE_UNIT",
        "U000960",
        1,
        ["U000960", "U000962"],
        ["A000845"],
        parameters={"neighborhood": "four orthogonal neighbors plus the center cell"},
    )
    add(
        "two-dimensional CA code 1022 (any black orthogonal neighbor)",
        "CA2",
        "SOURCE_UNIT",
        "U000963",
        1,
        ["U000963", "U000965"],
        ["A000846"],
        aliases=["code 1022"],
        parameters={"seed": "single black cell", "rule code": "1022"},
        parent_index=ca2,
        route_keys=["page-173-code-1022"],
    )
    add(
        "two-dimensional CA code 942 (exactly one or four black neighbors)",
        "CA2",
        "SOURCE_UNIT",
        "U000966",
        1,
        ["U000966", "U000968"],
        ["A000847"],
        aliases=["code 942"],
        parameters={"seed": "single black cell", "rule code": "942"},
        parent_index=ca2,
        route_keys=["page-173-code-942"],
    )
    for ordinal, code in enumerate(range(450, 499), 1):
        add(
            f"two-dimensional totalistic CA code {code}",
            "CA2",
            "IMAGE",
            "A000849",
            ordinal,
            ["U000974"],
            ["A000849"],
            aliases=[f"code {code}"],
            parameters={
                "rule code": str(code),
                "seed": "single black square",
                "display horizon": "22 steps",
            },
            parent_index=ca2,
            route_keys=["page-60-code-comparison"],
        )
    exact3 = add(
        "eight-neighbor retaining CA with exactly three black neighbors",
        "CA2",
        "SOURCE_UNIT",
        "U000982",
        1,
        ["U000982", "U000983", "U000984", "U000993", "U000997", "U001002"],
        ["A000855", "A000856", "A000857", "A000858", "A000859", "A000860"],
        aliases=["code 174826"],
        parameters={
            "neighborhood": "eight neighbors including diagonals",
            "rule code": "174826",
            "seed sweep": "rows of black cells of various lengths",
        },
        parent_index=ca2,
        route_keys=["pages-179-181-exact3", "page-179-seeds", "page-181-row11"],
    )
    add(
        "eight-neighbor rough-surface CA code 175850",
        "CA2",
        "SOURCE_UNIT",
        "U000989",
        1,
        ["U000989"],
        ["A000852", "A000853"],
        aliases=["code 175850"],
        parameters={
            "neighborhood": "eight neighbors including diagonals",
            "seed": "row of seven black cells",
            "rule code": "175850",
        },
        parent_index=ca2,
    )
    add(
        "eight-neighbor approximate-circle CA code 746",
        "CA2",
        "SOURCE_UNIT",
        "U000991",
        1,
        ["U000991"],
        ["A000854"],
        aliases=["code 746"],
        parameters={
            "neighborhood": "eight neighbors including diagonals",
            "seed": "row of seven black cells",
            "rule code": "746",
        },
        parent_index=ca2,
        route_keys=["page-178-circle"],
    )
    ca3 = add(
        "three-dimensional cellular-automaton family",
        "CA3",
        "SOURCE_UNIT",
        "U000994",
        1,
        ["U000994"],
        [],
    )
    add(
        "six-face-neighbor 3D CA: any black neighbor",
        "CA3",
        "SOURCE_UNIT",
        "U001005",
        1,
        ["U001005"],
        ["A000861", "A000862"],
        parameters={"neighborhood": "six face-sharing neighbors", "seed": "single black cell"},
        parent_index=ca3,
        route_keys=["page-171-3d-analogy"],
    )
    add(
        "six-face-neighbor 3D CA: exactly one black neighbor",
        "CA3",
        "SOURCE_UNIT",
        "U001005",
        2,
        ["U001005"],
        ["A000861", "A000862"],
        parameters={"neighborhood": "six face-sharing neighbors", "seed": "single black cell"},
        parent_index=ca3,
        route_keys=["page-171-3d-analogy"],
    )
    add(
        "26-neighbor 3D CA: exactly one black neighbor",
        "CA3",
        "SOURCE_UNIT",
        "U001008",
        1,
        ["U001008"],
        ["A000863", "A000864"],
        parameters={"neighborhood": "all 26 face/edge/corner neighbors", "seed": "single black cell"},
        parent_index=ca3,
    )
    add(
        "26-neighbor 3D CA: exactly two black neighbors",
        "CA3",
        "SOURCE_UNIT",
        "U001008",
        2,
        ["U001008"],
        ["A000863", "A000864"],
        parameters={"neighborhood": "all 26 face/edge/corner neighbors", "seed": "line of three black cells"},
        parent_index=ca3,
    )

    tm2_family = add(
        "two-dimensional Turing-machine family",
        "TM2",
        "SOURCE_UNIT",
        "U001010",
        1,
        ["U001010"],
        ["A000865"],
        parameters={"movement carrier": "two-dimensional grid"},
        overrides={"seed": ("UNKNOWN_FROM_SOURCE", None)},
    )
    add(
        "illustrated three-state two-dimensional Turing machine",
        "TM2",
        "IMAGE",
        "A000865",
        1,
        ["U001010", "U001012"],
        ["A000865"],
        parameters={"head states": "three", "movement directions": "four"},
        parent_index=tm2_family,
    )
    tm_output_assets = ["A000866", "A000867", "A000868", "A000869", "A000871"]
    for ordinal, (label, output_asset) in enumerate(
        zip("abcde", tm_output_assets, strict=True), 1
    ):
        units = ["U001016", "U001026"]
        assets = ["A000870", output_asset]
        if label == "e":
            units.append("U001031")
            assets.extend(["A000872", "A000873"])
        add(
            f"four-state two-dimensional Turing-machine rule ({label})",
            "TM2",
            "IMAGE",
            "A000870",
            ordinal,
            units,
            assets,
            aliases=[f"rule ({label})"],
            parameters={"head states": "four", "rule panel": label},
            parent_index=tm2_family,
            route_keys=["page-186-turing-rule"] if label == "e" else [],
        )

    sub2 = add(
        "two-dimensional parallel substitution-system family",
        "SUB_GENERAL",
        "SOURCE_UNIT",
        "U001034",
        1,
        ["U001034", "U001039"],
        [],
        route_keys=["page-82-substitution"],
    )
    add(
        "four-square two-dimensional subdivision preset",
        "SUB_GRID",
        "SOURCE_UNIT",
        "U001037",
        1,
        ["U001037"],
        ["A000874", "A000875"],
        parameters={"replacement": "each square is replaced by four smaller squares"},
        parent_index=sub2,
    )
    for ordinal, label in enumerate("abcdefghi", 1):
        add(
            f"two-dimensional substitution preset ({label}) on page 188 figure",
            "SUB_GRID",
            "IMAGE",
            "A000876",
            ordinal,
            ["U001041"],
            ["A000876"],
            aliases=[f"substitution preset ({label})"],
            parameters={"panel": label, "horizon": "five steps", "seed": "single black square"},
            parent_index=sub2,
            route_keys=["page-83-substitution"],
        )
    geom_family = add(
        "geometrical replacement and fractal-system family",
        "SUB_GEOM_GENERAL",
        "SOURCE_UNIT",
        "U001042",
        1,
        ["U001042", "U001050", "U001051", "U001053"],
        [],
        parameters={
            "replacement domain": "geometrical black-square elements without a fixed grid",
            "interaction": "none; replacement does not depend on other elements",
        },
    )
    add(
        "orientation-sensitive two-square geometrical replacement preset",
        "SUB_GEOM",
        "SOURCE_UNIT",
        "U001045",
        1,
        ["U001042", "U001045", "U001053"],
        ["A000877", "A000878"],
        parameters={"replacement count": "two smaller black squares", "orientation": "carried by each square"},
        parent_index=geom_family,
    )
    add(
        "overlap-producing geometrical replacement preset",
        "SUB_GEOM",
        "SOURCE_UNIT",
        "U001049",
        1,
        ["U001046", "U001049"],
        ["A000879", "A000880"],
        parameters={"replacement count": "two smaller black squares", "overlap": "arises in later stages"},
        parent_index=geom_family,
    )
    for ordinal, label in enumerate("abcd", 1):
        add(
            f"geometrical fractal replacement preset ({label})",
            "SUB_GEOM",
            "IMAGE",
            "A000881",
            ordinal,
            ["U001050", "U001051", "U001055"],
            ["A000881"],
            aliases=[f"fractal preset ({label})"],
            parameters={"panel": label, "horizon": "12 steps"},
            parent_index=geom_family,
        )
    neighbor_sub = add(
        "two-dimensional neighbor-dependent substitution-system family",
        "SUB_GRID_NEIGHBOR",
        "SOURCE_UNIT",
        "U001056",
        1,
        ["U001052", "U001056", "U001059"],
        ["A000882"],
        parameters={"boundary": "grid wraps in both dimensions", "dependency": "neighboring cells"},
        parent_index=sub2,
        route_keys=["page-85-interacting-substitution", "chapter-3-substitution-schedules"],
    )
    add(
        "illustrated neighbor-dependent substitution demonstration",
        "SUB_GRID_NEIGHBOR",
        "IMAGE",
        "A000882",
        1,
        ["U001059"],
        ["A000882"],
        parameters={"boundary": "wraps in both dimensions", "figure region": "top demonstration"},
        parent_index=neighbor_sub,
    )
    for ordinal, label in enumerate("abcdefgh", 2):
        add(
            f"neighbor-dependent substitution preset ({label})",
            "SUB_GRID_NEIGHBOR",
            "IMAGE",
            "A000882",
            ordinal,
            ["U001059", "U001060"],
            ["A000882"],
            aliases=[f"neighbor-dependent preset ({label})"],
            parameters={
                "panel": label,
                "horizon": "eight steps",
                "boundary": "grid wraps in both dimensions",
            },
            parent_index=neighbor_sub,
        )

    network_family = add(
        "network-system family",
        "NETWORK_GENERAL",
        "SOURCE_UNIT",
        "U001067",
        1,
        [
            "U001066",
            "U001067",
            "U001069",
            "U001070",
        ],
        [],
    )
    network = add(
        "binary-outdegree network-system restriction",
        "NETWORK_BINARY_GENERAL",
        "SOURCE_UNIT",
        "U001071",
        1,
        [
            "U001071",
            "U001090",
            "U001094",
        ],
        [],
        parameters={"outgoing connections per node": "two"},
        overrides={"seed": ("UNKNOWN_FROM_SOURCE", None)},
        parent_index=network_family,
    )
    add(
        "unlabelled reachable binary-outdegree graphs on one to three nodes",
        "GRAPH",
        "SOURCE_UNIT",
        "U001072",
        1,
        ["U001072", "U001074"],
        ["A000883"],
        parameters={"node counts": "one, two, or three", "equivalence": "node labels ignored; unreachable-node cases excluded"},
        overrides={
            "result_kind": (
                "SUPPORTED",
                "the finite set of reachable graph-isomorphism classes on one, two, or three nodes",
            )
        },
    )
    graph_indices: list[int] = []
    for ordinal, dimension in enumerate(("one", "two", "three"), 1):
        graph_indices.append(
            add(
                f"binary-outdegree network with effective {dimension}-dimensional array structure",
                "GRAPH",
                "IMAGE",
                "A000884",
                ordinal,
                [
                    ["U001079", "U001080"],
                    ["U001078", "U001079", "U001081"],
                    ["U001079", "U001082"],
                ][ordinal - 1],
                ["A000884"],
                parameters={"effective dimension": dimension},
            )
        )
    tree_ac = add(
        "binary-outdegree infinite-tree graph shown as panels (a) and (c)",
        "GRAPH",
        "IMAGE",
        "A000885",
        1,
        ["U001083", "U001085"],
        ["A000885"],
        aliases=["tree panels (a) and (c)"],
        parameters={"identity": "panels (a) and (c) have identical connection patterns"},
    )
    add(
        "binary-outdegree infinite-tree graph shown as panel (b)",
        "GRAPH",
        "IMAGE",
        "A000885",
        2,
        ["U001083", "U001085"],
        ["A000885"],
        aliases=["tree panel (b)"],
        parameters={"identity": "connection pattern distinct from the shared (a)/(c) graph"},
    )
    add(
        "nested binary-outdegree network graph",
        "GRAPH",
        "SOURCE_UNIT",
        "U001088",
        1,
        ["U001086", "U001088"],
        ["A000886"],
        parameters={"effective structure": "nested geometrical connection pattern"},
    )
    rerouting_cases = {
        "a": {
            "above replacement": "follow below then above: path {2,1}",
            "below replacement": "retain below: path {2}",
        },
        "b": {
            "above replacement": "follow above twice: path {1,1}",
            "below replacement": "retain below: path {2}",
        },
        "c": {
            "above replacement": "loop to the source node: empty path {}",
            "below replacement": "retain below: path {2}",
        },
        "d": {
            "above replacement": "loop to the source node: empty path {}",
            "below replacement": "follow the old above connection: path {1}",
        },
    }
    for ordinal, label in enumerate("abcd", 1):
        units = ["U001095", "U001096", "U001097", "U001099"]
        case = rerouting_cases[label]
        add(
            f"binary-outdegree network rerouting rule ({label})",
            "NETWORK",
            "SOURCE_UNIT",
            "U001099",
            ordinal,
            units,
            ["A000888"],
            aliases=[f"network rule ({label})"],
            parameters={"rule panel": label, **case},
            overrides={
                "write_replacement_assembly_or_commit": (
                    "SUPPORTED",
                    f"reroute existing connections only: above -> {case['above replacement']}; below -> {case['below replacement']}; do not insert nodes",
                ),
                "parameters_and_variants": (
                    "SUPPORTED",
                    f"connection-rerouting case ({label}) over the two distinguished outgoing links",
                ),
            },
            parent_index=network,
        )
    insertion_cases = {
        "a": "the new node copies the original node's above and below targets",
        "b": "the new node swaps the original node's above and below targets",
    }
    for ordinal, (label, asset_id) in enumerate(
        (("a", "A000889"), ("b", "A000890")), 1
    ):
        new_node_targets = insertion_cases[label]
        add(
            f"node-inserting network rule ({label})",
            "NETWORK",
            "SOURCE_UNIT",
            "U001104",
            ordinal,
            ["U001100", "U001101", "U001104"],
            [asset_id],
            aliases=[f"node-addition rule ({label})"],
            parameters={
                "rule panel": label,
                "seed": "single-node network",
                "new-node outgoing targets": new_node_targets,
            },
            overrides={
                "write_replacement_assembly_or_commit": (
                    "SUPPORTED",
                    f"insert one new node in each above connection; {new_node_targets}",
                ),
                "parameters_and_variants": (
                    "SUPPORTED",
                    f"node-insertion case ({label})",
                ),
            },
            parent_index=network,
        )
    conditional = add(
        "one-hop same-target/different-target conditional network-rule family",
        "NETWORK",
        "SOURCE_UNIT",
        "U001107",
        1,
        ["U001106", "U001107", "U001110"],
        ["A000891"],
        parameters={"case predicate": "whether the two outgoing connections reach the same node"},
        parent_index=network,
    )
    for ordinal, label in enumerate("abc", 1):
        add(
            f"one-hop conditional network preset ({label})",
            "NETWORK",
            "IMAGE",
            "A000891",
            ordinal,
            ["U001110"],
            ["A000891"],
            aliases=[f"conditional network rule ({label})"],
            parameters={"rule panel": label},
            parent_index=conditional,
        )
    distance2 = add(
        "distance-two distinct-node-count network-rule family",
        "NETWORK",
        "SOURCE_UNIT",
        "U001111",
        1,
        ["U001111", "U001115"],
        ["A000892"],
        parameters={"dependency radius": "up to two successive connections"},
        parent_index=network,
    )
    for ordinal, label in enumerate("abc", 1):
        add(
            f"distance-two network preset ({label})",
            "NETWORK",
            "IMAGE",
            "A000892",
            ordinal,
            ["U001115"],
            ["A000892"],
            aliases=[f"distance-two network rule ({label})"],
            parameters={"rule panel": label},
            parent_index=distance2,
        )
    add(
        "distance-two network preset (d)",
        "NETWORK",
        "SOURCE_UNIT",
        "U001118",
        1,
        ["U001117", "U001118", "U001121"],
        ["A000893"],
        aliases=["distance-two network rule (d)"],
        parameters={"rule panel": "d", "rule table": unit_literal("U001118")},
        parent_index=distance2,
    )
    add(
        "distance-two network preset (e)",
        "NETWORK",
        "SOURCE_UNIT",
        "U001120",
        1,
        ["U001119", "U001120", "U001121"],
        ["A000893"],
        aliases=["distance-two network rule (e)"],
        parameters={"rule panel": "e", "rule table": unit_literal("U001120")},
        parent_index=distance2,
    )

    multiway = add(
        "multiway string-replacement-system family",
        "MULTIWAY",
        "SOURCE_UNIT",
        "U001124",
        1,
        ["U001124", "U001129"],
        [],
        route_keys=["page-88-sequential-substitution"],
    )
    add(
        "one-element-or-two-elements multiway preset",
        "MULTIWAY",
        "SOURCE_UNIT",
        "U001127",
        1,
        ["U001127", "U001128"],
        ["A000894"],
        parameters={"replacement alternatives": "one element remains one or becomes a pair", "seed": "one element"},
        parent_index=multiway,
    )
    simple_assets = ["A000899", "A000900", "A000897", "A000898", "A000895"]
    for ordinal, asset_id in enumerate(simple_assets, 1):
        caption = "U001134" if ordinal <= 3 else "U001139"
        add(
            f"page-205 multiway preset {ordinal}",
            "MULTIWAY",
            "IMAGE",
            asset_id,
            1,
            [caption],
            [asset_id],
            parameters={"page-205 figure order": str(ordinal)},
            parent_index=multiway,
        )
    add(
        "three-replacement multiway preset with period-1071 differences",
        "MULTIWAY",
        "SOURCE_UNIT",
        "U001143",
        1,
        ["U001140", "U001143"],
        ["A000901", "A000902"],
        parameters={"replacement alternatives": "three", "observed difference period": "1071 shifted by one"},
        parent_index=multiway,
    )
    add(
        "rapid-growth multiway preset generating white-initial states",
        "MULTIWAY",
        "SOURCE_UNIT",
        "U001147",
        1,
        ["U001145", "U001147"],
        ["A000903"],
        parameters={"eventual state set": "all states beginning with a white cell"},
        overrides={
            "seed": ("UNKNOWN_FROM_SOURCE", None),
            "rule_relation_constraint_function_or_probability_law": (
                "UNKNOWN_FROM_SOURCE",
                None,
            ),
        },
        parent_index=multiway,
        route_keys=["page-205-rapid-multiway"],
    )
    for ordinal, label in enumerate("abcdefghijklm", 1):
        route_keys = []
        if label in {"d", "f"}:
            route_keys.append("page-205-multiway-df")
        if label == "k":
            route_keys.append("previous-page-multiway-k")
        add(
            f"multiway survey preset ({label})",
            "MULTIWAY",
            "IMAGE",
            "A000904",
            ordinal,
            ["U001148", "U001150"],
            ["A000904"],
            aliases=[f"multiway rule ({label})"],
            parameters={"survey panel": label},
            parent_index=multiway,
            route_keys=route_keys,
        )
    add(
        "three-replacement multiway rule used in the page-224 evolution",
        "MULTIWAY",
        "IMAGE",
        "A000905",
        1,
        ["U001151", "U001152", "U001155", "U001156", "U001158"],
        ["A000905", "A000906", "A000907"],
        parameters={
            "replacement set": "three checked graphical replacements",
            "seed": "the checked two-element initial sequence",
        },
        parent_index=multiway,
    )
    add(
        "derived sequence-transition network for the page-224 multiway evolution",
        "TRANSITION_RELATION",
        "SOURCE_UNIT",
        "U001156",
        1,
        ["U001151", "U001152", "U001155", "U001156", "U001158"],
        ["A000906", "A000907"],
        aliases=[
            "network of what sequence leads to what other",
            "multiway state-transition relation",
        ],
        parameters={
            "represented system": "the checked three-replacement multiway rule",
            "represented seed": "the checked two-element initial sequence",
            "node identity": "each distinct sequence is shown once",
            "edge identity": "one-step native generation of one sequence from another",
        },
    )

    constraint_family = add(
        "constraint-specified system family",
        "CONSTRAINT_GENERAL",
        "SOURCE_UNIT",
        "U001161",
        1,
        ["U001161"],
        [],
    )
    add(
        "one-dimensional exact-one-black-and-one-white-neighbor constraint",
        "CONSTRAINT_1D",
        "SOURCE_UNIT",
        "U001162",
        1,
        ["U001162", "U001164"],
        ["A000908"],
        parameters={"constraint": "every cell has exactly one black and one white neighbor"},
        overrides={
            "result_kind": (
                "SUPPORTED",
                "the unique satisfying periodic line pattern stated by the source",
            ),
            "witness_semantics": (
                "SUPPORTED",
                "the displayed complete periodic coloring is the source's unique-model witness",
            ),
        },
        parent_index=constraint_family,
    )
    add(
        "one-dimensional at-least-one-unlike-neighbor constraint",
        "CONSTRAINT_1D",
        "SOURCE_UNIT",
        "U001166",
        1,
        ["U001166", "U001168"],
        ["A000909"],
        parameters={"constraint": "every cell has at least one neighbor of the opposite color"},
        overrides={
            "result_kind": (
                "SUPPORTED",
                "many satisfying line colorings, exactly those with no run longer than two equal-colored cells",
            ),
            "witness_semantics": (
                "SUPPORTED",
                "each displayed complete coloring witnesses one member of the many-model set",
            ),
        },
        parent_index=constraint_family,
    )
    fixed_specific = add(
        "two-dimensional neighbor-count constraint: black has one black, white has two white",
        "CONSTRAINT_NEIGHBOR2D",
        "SOURCE_UNIT",
        "U001173",
        1,
        ["U001173", "U001175"],
        ["A000910", "A000911"],
        parameters={
            "black-center condition": "one black and three white orthogonal neighbors",
            "white-center condition": "two white and two black orthogonal neighbors",
        },
        overrides={
            "result_kind": (
                "SUPPORTED",
                "one satisfying periodic grid pattern up to rotations and reflections",
            ),
            "witness_semantics": (
                "SUPPORTED",
                "the displayed periodic grid and its rotations/reflections are the complete source-stated model class",
            ),
        },
        parent_index=constraint_family,
    )
    fixed_family = add(
        "two-dimensional fixed black/white-neighbor-count constraint family",
        "CONSTRAINT_NEIGHBOR2D",
        "SOURCE_UNIT",
        "U001178",
        1,
        ["U001178", "U001181"],
        ["A000911"],
        parameters={"neighborhood": "four orthogonal neighbors"},
        parent_index=constraint_family,
    )
    for row_black_neighbors in range(5):
        for visual_column in range(5):
            # The checked panel runs from 4 white neighbors at the left to 0
            # at the right; black-neighbor counts run 0→4 top-to-bottom.
            col_white_neighbors = 4 - visual_column
            # The row/column matching the previously introduced prose preset is
            # linked as evidence there instead of duplicated.
            if row_black_neighbors == 1 and col_white_neighbors == 2:
                continue
            ordinal = row_black_neighbors * 5 + visual_column + 1
            is_unsatisfiable = ordinal in {4, 10}
            add(
                "two-dimensional neighbor-count preset "
                f"(black-center black={row_black_neighbors}, "
                f"white-center white={col_white_neighbors})",
                "CONSTRAINT_NEIGHBOR2D",
                "IMAGE",
                "A000911",
                ordinal,
                ["U001181"],
                ["A000911"],
                parameters={
                    "black-center condition": (
                        f"{row_black_neighbors} black and "
                        f"{4 - row_black_neighbors} white orthogonal neighbors"
                    ),
                    "white-center condition": (
                        f"{col_white_neighbors} white and "
                        f"{4 - col_white_neighbors} black orthogonal neighbors"
                    ),
                    "survey panel": str(ordinal),
                    "model outcome": (
                        "unsatisfiable"
                        if is_unsatisfiable
                        else "at least one displayed satisfying pattern"
                    ),
                },
                overrides={
                    "result_kind": (
                        "SUPPORTED",
                        (
                            "the empty set of complete satisfying grid assignments"
                            if is_unsatisfiable
                            else "a nonempty set of complete satisfying grid assignments"
                        ),
                    ),
                    "witness_semantics": (
                        "SUPPORTED",
                        (
                            "the blank panel, interpreted by the caption, records that no pattern satisfies the constraint"
                            if is_unsatisfiable
                            else "the displayed complete periodic pattern witnesses satisfiability"
                        ),
                    ),
                },
                parent_index=fixed_family,
            )
    template_family = add(
        "overlapping local-template constraint family",
        "CONSTRAINT_TEMPLATE_CROSS",
        "SOURCE_UNIT",
        "U001182",
        1,
        ["U001182", "U001184", "U001185"],
        ["A000912"],
        parameters={"local footprint": "center cell and four orthogonal neighbors"},
        parent_index=constraint_family,
    )
    for ordinal, (code, block) in enumerate(
        (("1384774", "5 × 10"), ("328778790", "24 × 24")), 1
    ):
        add(
            f"local-template constraint {code}",
            "CONSTRAINT_TEMPLATE_CROSS",
            "SOURCE_UNIT",
            "U001184",
            ordinal,
            ["U001184"],
            ["A000912"],
            aliases=[f"constraint {code}"],
            parameters={"constraint code": code, "displayed tessellation block": block},
            overrides={
                "result_kind": (
                    "SUPPORTED",
                    "a nonempty set of complete satisfying grid assignments",
                ),
                "witness_semantics": (
                    "SUPPORTED",
                    f"the displayed {block} periodic tessellation is a positive complete-model witness",
                ),
            },
            parent_index=template_family,
        )
    add(
        "complete 171-pattern witness basis for local-template constraints",
        "WITNESS",
        "SOURCE_UNIT",
        "U001188",
        1,
        ["U001185", "U001188"],
        ["A000913", "A000914"],
        aliases=["171-pattern witness basis"],
        parameters={
            "collection size": "171",
            "coverage": "one member satisfies every satisfiable constraint in the stated family",
        },
    )
    required_family = add(
        "local-template constraint with a required template occurrence",
        "CONSTRAINT_TEMPLATE_REQUIRED",
        "SOURCE_UNIT",
        "U001190",
        1,
        ["U001190", "U001191", "U001193"],
        ["A000915"],
        parameters={"global condition": "one designated allowed template must occur at least once"},
        parent_index=template_family,
    )
    required_codes = [
        "151828",
        "86294",
        "4670324",
        "1428252506",
        "1143305038",
        "106389882",
        "1125528937",
        "339833662",
        "375604536",
        "1378162297",
    ]
    code_to_index: dict[str, int] = {}
    for ordinal, code in enumerate(required_codes, 1):
        code_to_index[code] = add(
            f"required-template constraint {code}",
            "CONSTRAINT_TEMPLATE_REQUIRED",
            "IMAGE",
            "A000915",
            ordinal,
            ["U001193"],
            ["A000915"],
            aliases=[f"constraint {code}"],
            parameters={"constraint code": code, "survey panel": str(ordinal)},
            overrides={
                "rule_relation_constraint_function_or_probability_law": (
                    "UNKNOWN_FROM_SOURCE",
                    None,
                ),
                "result_kind": (
                    "SUPPORTED",
                    "a nonempty set of satisfying assignments; the displayed pattern is one witness",
                ),
                "parameters_and_variants": (
                    "SUPPORTED",
                    "numeric constraint code and required-center occurrence; the allowed-template set is not decoded in the assigned source",
                ),
                "witness_semantics": (
                    "SUPPORTED",
                    "the displayed pattern witnesses satisfiability but does not decode the complete allowed-template law",
                ),
            },
            parent_index=required_family,
        )
    enumeration_solver = add(
        "exhaustive complete-pattern enumeration constraint solver",
        "SOLVER_ENUMERATION",
        "SOURCE_UNIT",
        "U001197",
        1,
        ["U001194", "U001195", "U001196", "U001197"],
        [],
        parameters={"strategy": "enumerate every possible pattern and test the constraint"},
    )
    backtracking_solver = add(
        "iterative region-growth backtracking constraint solver",
        "SOLVER",
        "SOURCE_UNIT",
        "U001198",
        1,
        [
            "U001198",
            "U001199",
            "U001200",
            "U001201",
            "U001202",
            "U001205",
        ],
        ["A000916"],
        parameters={"strategy": "extend a small region in all possible ways and backtrack on violation"},
    )
    # Constraint 4670324 is already independently delimited in the ten-panel
    # survey; the later solver figure supports it rather than duplicating it.
    specs[code_to_index["4670324"] - 1]["units"].append("U001205")
    specs[code_to_index["4670324"] - 1]["assets"].append("A000916")
    for ordinal, code in enumerate(("373384574", "387520105"), 2):
        has_infinite_model = code == "373384574"
        add(
            f"solver-witnessed constraint {code}",
            "CONSTRAINT_TEMPLATE_REQUIRED",
            "SOURCE_UNIT",
            "U001205",
            ordinal,
            ["U001205"],
            ["A000916"],
            aliases=[f"constraint {code}"],
            parameters={
                "constraint code": code,
                "solver figure panel": chr(96 + ordinal),
                "model outcome": (
                    "a repetitive infinite pattern exists"
                    if has_infinite_model
                    else "no infinite satisfying pattern exists"
                ),
            },
            overrides={
                "rule_relation_constraint_function_or_probability_law": (
                    "UNKNOWN_FROM_SOURCE",
                    None,
                ),
                "result_kind": (
                    "SUPPORTED",
                    (
                        "a nonempty set of infinite satisfying assignments"
                        if has_infinite_model
                        else "an empty set of infinite satisfying assignments, despite large finite satisfiable regions"
                    ),
                ),
                "parameters_and_variants": (
                    "SUPPORTED",
                    "numeric constraint code and solver outcome; the allowed-template set is not decoded in the assigned source",
                ),
                "witness_semantics": (
                    "SUPPORTED",
                    (
                        "the displayed repetitive pattern is a positive infinite-model witness"
                        if has_infinite_model
                        else "the displayed finite partial pattern is not a global witness; the prose states that no infinite model exists"
                    ),
                ),
            },
            parent_index=required_family,
        )
    add(
        "required-template constraint 18762389",
        "CONSTRAINT_TEMPLATE_REQUIRED",
        "SOURCE_UNIT",
        "U001210",
        1,
        ["U001206", "U001210"],
        ["A000917", "A000918"],
        aliases=["constraint 18762389"],
        parameters={
            "constraint code": "18762389",
            "allowed templates": "12 checked cross-neighborhood templates",
            "required occurrence": "a template containing a stacked black pair",
        },
        overrides={
            "result_kind": (
                "SUPPORTED",
                "one satisfying nonperiodic grid pattern up to translations",
            ),
            "witness_semantics": (
                "SUPPORTED",
                "the displayed infinite pattern is the unique source-stated model class up to translation",
            ),
        },
        parent_index=required_family,
        route_keys=["pages-214-215-constraint-order"],
    )
    template3 = add(
        "3x3 allowed-template constraint family",
        "CONSTRAINT_TEMPLATE_3X3",
        "SOURCE_UNIT",
        "U001213",
        1,
        ["U001213"],
        [],
        parameters={"local footprint": "complete 3 × 3 block including diagonals"},
        parent_index=constraint_family,
        route_keys=["page-216-constraint-family"],
    )
    add(
        "33-template rule-60-correspondence constraint",
        "CONSTRAINT_TEMPLATE_3X3_REQUIRED",
        "SOURCE_UNIT",
        "U001216",
        1,
        ["U001216"],
        ["A000919", "A000920"],
        parameters={
            "allowed templates": "33 of 512 checked 3 × 3 templates",
            "required occurrence": "the first displayed template",
            "correspondence": "rule 60 elementary one-dimensional cellular automaton",
        },
        overrides={
            "result_kind": (
                "SUPPORTED",
                "a nonempty set of complete grid assignments containing the forced nested pattern",
            ),
            "witness_semantics": (
                "SUPPORTED",
                "the displayed rule-60-correspondence pattern is a positive complete-model witness",
            ),
        },
        parent_index=template3,
        route_keys=["rule-60-correspondence"],
    )
    add(
        "56-template rule-30-correspondence constraint",
        "CONSTRAINT_TEMPLATE_3X3_REQUIRED",
        "SOURCE_UNIT",
        "U001217",
        1,
        ["U001217", "U001220"],
        ["A000921", "A000922"],
        parameters={
            "allowed templates": "56 checked 3 × 3 templates",
            "required occurrence": "the first displayed template",
            "correspondence": "shifted rule 30 elementary one-dimensional cellular automaton pattern",
        },
        overrides={
            "result_kind": (
                "SUPPORTED",
                "the source-stated sole satisfying pattern, derived from a shifted rule-30 evolution",
            ),
            "witness_semantics": (
                "SUPPORTED",
                "the displayed rule-30-derived pattern is the source-stated complete model",
            ),
        },
        parent_index=template3,
        route_keys=["rule-30-correspondence"],
    )

    assert len(specs) == 196, len(specs)
    return specs


def unit_literal(unit_id: str) -> str:
    # Stable symbolic marker expanded to source text after bundle loading.
    return f"@UNIT:{unit_id}"


def build_route_specs() -> list[dict[str, str]]:
    specs = [
        ("page-173-code-1022", "U000965", "page 173", "PAGE", "two-dimensional CA rule-code numbering", "WITHIN_STAGE"),
        ("page-173-code-942", "U000968", "page 173", "PAGE", "two-dimensional CA rule-code numbering", "WITHIN_STAGE"),
        ("page-60-code-comparison", "U000974", "page 60", "PAGE", "earlier cellular-automaton code convention", "CROSS_RANGE"),
        ("page-178-circle", "U000981", "page 178", "PAGE", "approximate-circle two-dimensional cellular automaton", "WITHIN_STAGE"),
        ("pages-179-181-exact3", "U000982", "pages 179–181", "PAGE", "eight-neighbor exactly-three retaining cellular automaton", "WITHIN_STAGE"),
        ("page-179-seeds", "U000983", "top of page 179", "PAGE", "seed-length sweep for exactly-three retaining CA", "WITHIN_STAGE"),
        ("page-181-row11", "U000984", "page 181", "PAGE", "row-of-eleven evolution for exactly-three retaining CA", "WITHIN_STAGE"),
        ("pages-182-183-3d", "U000995", "pages 182 and 183", "PAGE", "three-dimensional cellular-automaton examples", "WITHIN_STAGE"),
        ("page-171-3d-analogy", "U001005", "page 171", "PAGE", "two-dimensional nested cellular-automaton analog", "WITHIN_STAGE"),
        ("page-186-turing-rule", "U001016", "page 186", "PAGE", "complex four-state two-dimensional Turing-machine rule", "WITHIN_STAGE"),
        ("page-82-substitution", "U001033", "page 82", "PAGE", "one-dimensional substitution-system mechanics", "CROSS_RANGE"),
        ("page-83-substitution", "U001038", "page 83", "PAGE", "one-dimensional substitution-system nested patterns", "CROSS_RANGE"),
        ("page-85-interacting-substitution", "U001052", "page 85", "PAGE", "neighbor interaction in one-dimensional substitution systems", "CROSS_RANGE"),
        ("chapter-3-substitution-schedules", "U001057", "Chapter 3", "SECTION", "parallel and sequential one-dimensional substitution schedules", "CROSS_RANGE"),
        ("chapter-9-sequential-highd", "U001062", "Chapter 9", "SECTION", "order-independent higher-dimensional sequential substitution", "CROSS_RANGE"),
        ("chapter-9-network-physics", "U001113", "Chapter 9", "SECTION", "network-system variants for space and spacetime", "CROSS_RANGE"),
        ("page-88-sequential-substitution", "U001129", "page 88", "PAGE", "sequential substitution replacement rules", "CROSS_RANGE"),
        ("page-205-rapid-multiway", "U001147", "page 205", "PAGE", "rapid-growth multiway rule", "WITHIN_STAGE"),
        ("page-205-multiway-df", "U001150", "page 205", "PAGE", "multiway rules (d) and (f)", "WITHIN_STAGE"),
        ("previous-page-multiway-k", "U001150", "previous page", "PAGE", "multiway rule (k)", "WITHIN_STAGE"),
        ("pages-214-215-constraint-order", "U001206", "pages 214 and 215", "PAGE", "ordering of local-template constraints", "WITHIN_STAGE"),
        ("page-216-constraint-family", "U001212", "page 216", "PAGE", "required-template constraint family", "WITHIN_STAGE"),
        ("rule-60-correspondence", "U001216", "rule 60 elementary one-dimensional cellular automaton", "OTHER", "constraint correspondence with elementary cellular automaton rule 60", "CROSS_RANGE"),
        ("rule-30-correspondence", "U001217", "rule 30 cellular automaton", "OTHER", "constraint correspondence with a shifted elementary cellular automaton rule-30 pattern", "CROSS_RANGE"),
    ]
    result = []
    anchor_ordinals: dict[str, int] = defaultdict(int)
    for ordinal, (key, unit, literal, kind, topic, scope) in enumerate(specs, 1):
        anchor_ordinals[unit] += 1
        result.append(
            {
                "key": key,
                "route_id": f"WR{ordinal:04d}",
                "source_unit_id": unit,
                "source_asset_id": "",
                "discovery_epoch": EPOCH,
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": unit,
                "discovery_ordinal": str(anchor_ordinals[unit]),
                "literal_target": literal,
                "route_kind": kind,
                "expected_topic": topic,
                "owning_stage": STAGE,
                "closure_scope": scope,
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": json.dumps(
                    [
                        "Sequential blind review recorded the literal route; resolution is reserved for the coordinator."
                    ],
                    separators=(",", ":"),
                ),
                "vocabulary_terms": json.dumps(
                    sorted(set(re.findall(r"[A-Za-z0-9]+", topic.lower()))),
                    separators=(",", ":"),
                ),
                "defect_boundary": "",
            }
        )
    assert [r["route_id"] for r in result] == [f"WR{i:04d}" for i in range(1, 25)]
    return result


def asset_judgment_specs() -> dict[str, dict[str, Any]]:
    roles: dict[str, str] = {}

    def assign(role: str, ids: str) -> None:
        for asset_id in ids.split():
            assert asset_id not in roles
            roles[asset_id] = role

    assign("DECORATIVE", "A000843")
    assign("RELATION", "A000844 A000887 A000906 A000907")
    assign("CONTROL", "A000855")
    assign(
        "NATIVE_EVIDENCE",
        "A000845 A000849 A000853 A000861 A000864 A000865 A000870 "
        "A000875 A000876 A000878 A000880 A000881 A000882 A000883 "
        "A000884 A000885 A000886 A000891 A000892 A000894 "
        "A000895 A000897 A000898 A000899 A000900 A000901 A000904 "
        "A000905 A000911 A000912 A000913 A000914 "
        "A000918 A000919 A000922",
    )
    assign(
        "OBSERVER",
        "A000846 A000847 A000848 A000850 A000851 A000852 A000854 "
        "A000856 A000857 A000858 A000859 A000860 A000862 A000863 "
        "A000866 A000867 A000868 A000869 A000871 A000872 A000873 "
        "A000874 A000877 A000879 A000888 A000889 A000890 A000893 "
        "A000896 A000902 A000903 A000908 A000909 A000910 A000915 "
        "A000916 A000917 A000920 A000921",
    )
    assert set(roles) == {f"A{i:06d}" for i in range(843, 923)}

    text_bearing = {
        "A000843",
        "A000844",
        "A000846",
        "A000847",
        "A000849",
        "A000850",
        "A000851",
        "A000852",
        "A000855",
        "A000856",
        "A000857",
        "A000858",
        "A000859",
        "A000860",
        "A000862",
        "A000863",
        "A000865",
        "A000866",
        "A000867",
        "A000868",
        "A000869",
        "A000870",
        "A000871",
        "A000872",
        "A000873",
        "A000874",
        "A000876",
        "A000877",
        "A000879",
        "A000881",
        "A000882",
        "A000883",
        "A000884",
        "A000885",
        "A000887",
        "A000888",
        "A000889",
        "A000890",
        "A000891",
        "A000892",
        "A000893",
        "A000894",
        "A000895",
        "A000896",
        "A000897",
        "A000898",
        "A000899",
        "A000900",
        "A000901",
        "A000902",
        "A000903",
        "A000904",
        "A000905",
        "A000906",
        "A000907",
        "A000911",
        "A000913",
        "A000914",
        "A000915",
        "A000916",
    }
    result: dict[str, dict[str, Any]] = {}
    for asset_id in sorted(roles):
        role = roles[asset_id]
        flags = []
        if role == "NATIVE_EVIDENCE":
            flags.append("CONSTRUCTION_BEARING")
        if asset_id in text_bearing:
            flags.append("TEXT_BEARING")
        result[asset_id] = {
            "role": role,
            "risk_flags": flags,
            # Every source file was inspected either directly or in an unscaled
            # native-pixel audit sheet after the thumbnail pass.
            "original_resolution_status": "REVIEWED",
            "transcription_status": "CHECKED" if flags else "NOT_REQUIRED",
        }
    return result


def candidate_records(
    state: dict[str, Any],
    route_specs: list[dict[str, str]],
    asset_specs: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, list[str]], dict[str, list[str]], int]:
    raw_specs = build_candidate_specs()
    unit_anchor_order = {
        unit["id"]: ordinal for ordinal, unit in enumerate(state["units"], 1)
    }
    asset_anchor_order = {
        asset["asset_id"]: len(state["units"]) + ordinal
        for ordinal, asset in enumerate(state["assets"], 1)
    }
    specs = []
    for original_index, raw_spec in enumerate(raw_specs, 1):
        spec = dict(raw_spec)
        spec["_original_index"] = original_index
        spec["_anchor_order"] = (
            unit_anchor_order[spec["anchor_id"]]
            if spec["anchor_kind"] == "SOURCE_UNIT"
            else asset_anchor_order[spec["anchor_id"]]
        )
        specs.append(spec)
    specs.sort(
        key=lambda spec: (
            spec["_anchor_order"],
            spec["ordinal"],
            spec["_original_index"],
        )
    )
    candidate_anchor_counts: dict[tuple[str, str], int] = defaultdict(int)
    for spec in specs:
        anchor_key = (spec["anchor_kind"], spec["anchor_id"])
        candidate_anchor_counts[anchor_key] += 1
        spec["_anchor_ordinal"] = candidate_anchor_counts[anchor_key]

    route_by_key = {row["key"]: row["route_id"] for row in route_specs}
    candidate_ids = [f"W{i:04d}" for i in range(1, len(specs) + 1)]
    candidate_id_by_original_index = {
        spec["_original_index"]: candidate_ids[index]
        for index, spec in enumerate(specs)
    }
    evidence_counter = 0
    group_counter = 0
    unit_links: dict[str, list[str]] = defaultdict(list)
    asset_links: dict[str, list[str]] = defaultdict(list)
    records: list[dict[str, Any]] = []

    # Evidence anchors are independently ordinal within each immutable source.
    evidence_anchor_counts: dict[tuple[str, str], int] = defaultdict(int)

    for index, spec in enumerate(specs):
        candidate_id = candidate_ids[index]
        name = spec["name"]
        effective_overrides = dict(spec["overrides"])
        seed_descriptions = [
            description
            for key, description in spec["parameters"].items()
            if key in {"seed", "seed sweep"}
        ]
        if seed_descriptions and "seed" not in effective_overrides:
            effective_overrides["seed"] = (
                "SUPPORTED",
                "; ".join(seed_descriptions),
            )
        if (
            "boundary" in spec["parameters"]
            and "boundary" not in effective_overrides
        ):
            effective_overrides["boundary"] = (
                "SUPPORTED",
                spec["parameters"]["boundary"],
            )
        neighborhood_descriptions = [
            spec["parameters"][key]
            for key in ("neighborhood", "local footprint", "dependency radius")
            if key in spec["parameters"]
        ]
        if (
            neighborhood_descriptions
            and "read_dependencies_or_neighborhood" not in effective_overrides
        ):
            effective_overrides["read_dependencies_or_neighborhood"] = (
                "SUPPORTED",
                "; ".join(neighborhood_descriptions),
            )
        blueprint = profile_blueprint(
            spec["kind"], name, effective_overrides
        )
        supported_fields = [
            field for field in FIELDS if blueprint[field]["status"] == "SUPPORTED"
        ]
        evidence: list[dict[str, Any]] = []

        def add_evidence(
            kind: str,
            source_id: str,
            strength: str,
            modality: str,
            claim: str,
            fields: list[str],
        ) -> None:
            nonlocal evidence_counter, group_counter
            evidence_counter += 1
            group_counter += 1
            if kind == "SOURCE_UNIT":
                anchor_id = source_id
                source_unit_id: str | None = source_id
                image_path: str | None = None
            else:
                anchor_id = state["asset_by_id"][source_id]["physical_path"]
                source_unit_id = state["asset_by_id"][source_id]["source_unit_id"]
                image_path = anchor_id
            evidence_anchor_counts[(kind, anchor_id)] += 1
            anchor_ordinal = evidence_anchor_counts[(kind, anchor_id)]
            evidence.append(
                {
                    "evidence_id": f"WE{evidence_counter:06d}",
                    "evidence_group_id": f"WG{group_counter:06d}",
                    "discovery_anchor": {
                        "epoch": 2,
                        "kind": kind,
                        "id": anchor_id,
                        "ordinal": anchor_ordinal,
                    },
                    "source_unit_id": source_unit_id,
                    "image_path": image_path,
                    "strength": strength,
                    "modality": modality,
                    "claim": claim,
                    "fingerprint_fields": fields,
                }
            )

        prose_units = [
            unit_id
            for unit_id in spec["units"]
            if state["unit_by_id"][unit_id]["block_kind"] != "image"
        ]
        primary_mechanics_unit = (
            spec["anchor_id"]
            if spec["anchor_kind"] == "SOURCE_UNIT"
            and spec["anchor_id"] in prose_units
            else prose_units[0]
        )
        for unit_id in spec["units"]:
            block_kind = state["unit_by_id"][unit_id]["block_kind"]
            if block_kind == "image":
                continue
            modality = (
                "CODE"
                if block_kind == "fenced_code"
                else "CAPTION"
                if state["unit_by_id"][unit_id]["line_start"] > 1
                and any(
                    u["line_end"] == state["unit_by_id"][unit_id]["line_start"] - 1
                    and u["block_kind"] == "image"
                    for u in state["units"]
                )
                else "PROSE"
            )
            is_complete = (
                block_kind == "fenced_code"
                or unit_id in DIRECT_COMPLETE_SOURCE_UNITS
            )
            special_evidence = SOURCE_EVIDENCE_OVERRIDES.get(unit_id)
            if is_complete:
                strength = "DIRECT_COMPLETE_MECHANICS"
                evidence_fields = list(supported_fields)
            elif special_evidence is not None:
                strength, allowed_fields = special_evidence
                evidence_fields = [
                    field for field in supported_fields if field in allowed_fields
                ]
            elif unit_id == primary_mechanics_unit:
                strength = "DIRECT_PARTIAL_MECHANICS"
                evidence_fields = list(supported_fields)
            else:
                strength = "DIRECT_PARTIAL_MECHANICS"
                evidence_fields = [
                    field
                    for field in (
                        "parameters_and_variants",
                        "excluded_observers_and_representations",
                        "evidence_limit",
                    )
                    if field in supported_fields
                ]
                supplemental_text = unit_text(state, unit_id).lower()
                if (
                    "seed" in supported_fields
                    and any(
                        marker in supplemental_text
                        for marker in ("initial", "start", "seed")
                    )
                    and "seed" not in evidence_fields
                ):
                    evidence_fields.append("seed")
                if (
                    "boundary" in supported_fields
                    and "wrap" in supplemental_text
                    and "boundary" not in evidence_fields
                ):
                    evidence_fields.append("boundary")
            evidence_fields.sort(key=FIELDS.index)
            add_evidence(
                "SOURCE_UNIT",
                unit_id,
                strength,
                modality,
                f"{name}: {excerpt(state, unit_id)}",
                evidence_fields,
            )

        for asset_id in spec["assets"]:
            role = asset_specs[asset_id]["role"]
            strength = (
                "DIRECT_IDENTITY"
                if asset_id == "A000915"
                else
                "DIRECT_PARTIAL_MECHANICS"
                if role == "NATIVE_EVIDENCE"
                else "CORROBORATING"
                if role in {"CONTROL", "RELATION", "OBSERVER"}
                else "CONTEXTUAL"
            )
            # NATIVE_EVIDENCE is reserved for original-resolution rule/evolution
            # panels that delimit the candidate itself, including image-first
            # candidates whose adjacent prose is only a statistical summary.
            native_image_fields = set(supported_fields)
            contextual_image_fields = {
                "object_kind",
                "result_kind",
                "witness_semantics",
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            }
            image_fields = [
                field
                for field in supported_fields
                if field
                in (
                    native_image_fields
                    if role == "NATIVE_EVIDENCE"
                    else contextual_image_fields
                )
            ]
            if asset_id == "A000915":
                image_fields = [
                    field
                    for field in image_fields
                    if field
                    in {
                        "object_kind",
                        "result_kind",
                        "witness_semantics",
                        "parameters_and_variants",
                        "excluded_observers_and_representations",
                        "evidence_limit",
                    }
                ]
            add_evidence(
                "IMAGE",
                asset_id,
                strength,
                "IMAGE",
                f"Original-resolution inspection of {asset_id} "
                f"{'directly shows checked native symbols for' if role == 'NATIVE_EVIDENCE' else 'corroborates the displayed result/representation for'} {name}.",
                image_fields,
            )

        assert evidence, name
        evidence_ids_by_field = {
            field: [
                row["evidence_id"]
                for row in evidence
                if field in row["fingerprint_fields"]
            ]
            for field in FIELDS
        }
        fingerprint: dict[str, dict[str, Any]] = {}
        missing: list[str] = []
        for field in FIELDS:
            entry = dict(blueprint[field])
            entry["evidence_ids"] = (
                evidence_ids_by_field[field]
                if entry["status"] in {"SUPPORTED", "CONFLICTING_SOURCE"}
                else []
            )
            if entry["status"] == "SUPPORTED":
                assert entry["evidence_ids"], (name, field)
            if entry["status"] == "UNKNOWN_FROM_SOURCE":
                missing.append(f"The assigned source does not establish {field} for {name}.")
            fingerprint[field] = entry

        parameters = []
        all_evidence_ids = [row["evidence_id"] for row in evidence]
        for parameter_name, description in spec["parameters"].items():
            if description.startswith("@UNIT:"):
                description = unit_text(state, description[6:])
            parameters.append(
                {
                    "name": parameter_name,
                    "source_description": description,
                    "evidence_ids": all_evidence_ids,
                }
            )
        variants = [
            {
                "name": variant_name,
                "source_description": description,
                "evidence_ids": all_evidence_ids,
            }
            for variant_name, description in spec["variants"].items()
        ]
        related = []
        if spec["parent_index"] is not None:
            parent_id = candidate_id_by_original_index[spec["parent_index"]]
            related.append(
                {
                    "candidate_id": parent_id,
                    "relation": "POSSIBLE_VARIANT_OF",
                    "proof_kind": "PROVISIONAL_COMPARISON",
                    "evidence_ids": [evidence[0]["evidence_id"]],
                    "before_rationale": f"{name} is independently delimited by the source.",
                    "after_rationale": "Family/preset implementation equivalence is deliberately deferred until whole-corpus reconciliation.",
                    "uncertainty": "The blind review records a possible family relation without collapsing the preset.",
                }
            )
        route_ids = [route_by_key[key] for key in spec["route_keys"]]
        # A candidate's source-unit projection includes the immutable unit that
        # owns every image witness, not merely the prose/caption units named by
        # the semantic specification.
        source_order = {
            unit["id"]: position for position, unit in enumerate(state["units"])
        }
        record_source_units = sorted(
            {
                *spec["units"],
                *(
                    state["asset_by_id"][asset_id]["source_unit_id"]
                    for asset_id in spec["assets"]
                ),
            },
            key=source_order.__getitem__,
        )
        record = {
            "id": candidate_id,
            "record_status": "ACTIVE",
            "provisional_name": name,
            "aliases": spec["aliases"],
            "discovery_stage": 9,
            "discovery_anchor": {
                "epoch": 2,
                "kind": spec["anchor_kind"],
                "id": (
                    state["asset_by_id"][spec["anchor_id"]]["physical_path"]
                    if spec["anchor_kind"] == "IMAGE"
                    else spec["anchor_id"]
                ),
                "ordinal": spec["_anchor_ordinal"],
            },
            "source_unit_ids": record_source_units,
            "source_evidence": evidence,
            "source_status": ["CLEAR"],
            "image_witnesses": [
                state["asset_by_id"][asset_id]["physical_path"]
                for asset_id in spec["assets"]
            ],
            "evidence_strength": list(
                dict.fromkeys(row["strength"] for row in evidence)
            ),
            "field_support": {
                field: fingerprint[field]["status"] for field in FIELDS
            },
            "fingerprint": fingerprint,
            "parameters": parameters,
            "variants": variants,
            "missing_mechanics": missing,
            "uncertainties": [],
            "related_candidate_ids": related,
            "cross_reference_ids": route_ids,
            "evidence_reassignments": [],
        }
        records.append(record)
        for unit_id in spec["units"]:
            if candidate_id not in unit_links[unit_id]:
                unit_links[unit_id].append(candidate_id)
        for asset_id in spec["assets"]:
            if candidate_id not in asset_links[asset_id]:
                asset_links[asset_id].append(candidate_id)
            image_unit_id = state["asset_by_id"][asset_id]["source_unit_id"]
            if candidate_id not in unit_links[image_unit_id]:
                unit_links[image_unit_id].append(candidate_id)

    # WE/WG identifiers follow the frozen document-first discovery traversal,
    # independently of candidate grouping.  IMAGE anchors occur after all
    # source-unit anchors in the bundle's authoritative ordering.
    evidence_rows = [
        evidence
        for record in records
        for evidence in record["source_evidence"]
    ]

    def evidence_sort_key(evidence: dict[str, Any]) -> tuple[int, int]:
        anchor = evidence["discovery_anchor"]
        if anchor["kind"] == "SOURCE_UNIT":
            order = unit_anchor_order[anchor["id"]]
        else:
            asset_id = state["asset_by_path"][anchor["id"]]["asset_id"]
            order = asset_anchor_order[asset_id]
        return order, anchor["ordinal"]

    ordered_evidence = sorted(evidence_rows, key=evidence_sort_key)
    evidence_id_map = {
        evidence["evidence_id"]: f"WE{ordinal:06d}"
        for ordinal, evidence in enumerate(ordered_evidence, 1)
    }
    for ordinal, evidence in enumerate(ordered_evidence, 1):
        evidence["evidence_id"] = f"WE{ordinal:06d}"
        evidence["evidence_group_id"] = f"WG{ordinal:06d}"

    def remap_ids(values: list[str]) -> list[str]:
        return [evidence_id_map[value] for value in values]

    for record in records:
        for field in FIELDS:
            record["fingerprint"][field]["evidence_ids"] = remap_ids(
                record["fingerprint"][field]["evidence_ids"]
            )
        for collection_name in ("parameters", "variants", "related_candidate_ids"):
            for item in record[collection_name]:
                item["evidence_ids"] = remap_ids(item["evidence_ids"])

    assert [row["id"] for row in records] == candidate_ids
    assert evidence_counter == group_counter
    assert evidence_counter == len(ordered_evidence)
    return records, unit_links, asset_links, evidence_counter


def explicit_unlinked_dispositions() -> dict[str, tuple[str, list[str]]]:
    """Return the audited disposition for every unit with no candidate link.

    The sets are intentionally exhaustive and disjoint.  Candidate-linked
    units are classified separately by identity-anchor precedence.
    """

    groups: dict[str, tuple[str, list[str]]] = {}

    def assign(
        disposition: str, roles: list[str], unit_ids: str
    ) -> None:
        for unit_id in unit_ids.split():
            if unit_id in groups:
                raise ValueError(f"duplicate explicit disposition: {unit_id}")
            groups[unit_id] = (disposition, roles)

    assign(
        "CROSS_REFERENCE",
        [],
        "U000981 U000995 U001033 U001038 U001057 U001062 U001113 U001212",
    )
    assign("HISTORICAL_ONLY", ["HISTORICAL_MENTION"], "U001013")
    assign("APPLICATION_OR_EMULATION", ["APPLICATION"], "U001068")
    assign(
        "REPRESENTATION_OR_OBSERVER",
        ["REPRESENTATION", "OBSERVER_OR_ANALYZER"],
        "U000952 U000953 U000954 U000969 U000970 U000971 U000972 "
        "U000975 U000976 U000977 U000978 U000979 U000980 U000987 "
        "U001014 U001015 U001018 U001021 U001024 U001028 U001030 "
        "U001061 U001064 U001065 U001075 U001076 U001091 U001092 "
        "U001093 U001105 U001108 U001112 U001123 U001130 U001135 "
        "U001138 U001144 U001165 U001169 U001171 U001176 U001177 "
        "U001179 U001203 U001207 U001221",
    )
    assign(
        "NO_CONSTRUCTION",
        [],
        "U000947 U000948 U000949 U000950 U000951 U000955 U000956 "
        "U000957 U000958 U000959 U000985 U001009 U001032 U001063 "
        "U001089 U001122 U001125 U001159 U001160 U001170 U001172 "
        "U001189 U001211 U001222",
    )
    return groups


def reading_records(
    state: dict[str, Any],
    candidates: list[dict[str, Any]],
    routes: list[dict[str, str]],
    unit_links: dict[str, list[str]],
) -> list[dict[str, str]]:
    explicit = explicit_unlinked_dispositions()
    all_units = [unit["id"] for unit in state["units"]]
    linked_units = set(unit_links)
    expected_unlinked = set(all_units) - linked_units
    if set(explicit) != expected_unlinked:
        raise ValueError(
            "explicit disposition inventory mismatch: "
            f"missing={sorted(expected_unlinked - set(explicit))}, "
            f"extra={sorted(set(explicit) - expected_unlinked)}"
        )

    anchor_units: set[str] = set()
    for candidate in candidates:
        anchor = candidate["discovery_anchor"]
        if anchor["kind"] == "SOURCE_UNIT":
            anchor_units.add(anchor["id"])
        elif anchor["kind"] == "IMAGE":
            anchor_units.add(
                state["asset_by_path"][anchor["id"]]["source_unit_id"]
            )
        else:
            raise ValueError(f"disallowed sequential anchor: {anchor}")

    routes_by_unit: dict[str, list[str]] = defaultdict(list)
    for route in routes:
        routes_by_unit[route["source_unit_id"]].append(route["route_id"])

    records: list[dict[str, str]] = []
    for base in state["readings"]:
        unit_id = base["source_unit_id"]
        candidate_ids = unit_links.get(unit_id, [])
        if candidate_ids:
            disposition = (
                "CANDIDATE" if unit_id in anchor_units else "SUPPORTS_CANDIDATE"
            )
            secondary_roles: list[str] = []
        else:
            disposition, secondary_roles = explicit[unit_id]

        route_ids = routes_by_unit.get(unit_id, [])
        row = dict(base)
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": EPOCH,
                "review_disposition": disposition,
                "source_status": "CLEAR",
                "uncertainty": "",
                "secondary_roles": json.dumps(
                    secondary_roles, separators=(",", ":")
                ),
                "candidate_ids": json.dumps(
                    candidate_ids, separators=(",", ":")
                ),
                "route_ids": json.dumps(route_ids, separators=(",", ":")),
                "evidence_statement": (
                    f"Complete review of {unit_id} ({base['block_kind']}): "
                    f"{excerpt(state, unit_id)} "
                    f"Primary disposition: {disposition}."
                ),
                "review_stage": STAGE,
                "reviewer": REVIEWER,
            }
        )
        records.append(row)
    return records


def asset_records(
    state: dict[str, Any],
    asset_specs: dict[str, dict[str, Any]],
    asset_links: dict[str, list[str]],
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for base in state["assets"]:
        asset_id = base["asset_id"]
        judgment = asset_specs[asset_id]
        candidate_ids = asset_links.get(asset_id, [])
        flags = judgment["risk_flags"]
        role_phrase = judgment["role"].lower().replace("_", " ")
        row = dict(base)
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": EPOCH,
                "visual_role": judgment["role"],
                "source_status": "CLEAR",
                "risk_flags": json.dumps(flags, separators=(",", ":")),
                "original_resolution_status": judgment[
                    "original_resolution_status"
                ],
                "transcription_status": judgment["transcription_status"],
                "candidate_ids": json.dumps(
                    candidate_ids, separators=(",", ":")
                ),
                "route_ids": "[]",
                "evidence_statement": (
                    f"{asset_id} ({base['physical_path']}) was inspected at "
                    f"original pixel resolution and classified as {role_phrase}; "
                    f"{'construction/text symbols were independently checked' if flags else 'no construction-bearing or text-bearing transcription was required'}."
                ),
                "review_stage": STAGE,
                "reviewer": REVIEWER,
                "uncertainty": "",
            }
        )
        records.append(row)
    return records


def build_output(bundle: Path, prohibited_nonuse: bool) -> dict[str, Any]:
    state = load_bundle(bundle)
    route_specs = build_route_specs()
    asset_specs = asset_judgment_specs()
    candidates, unit_links, asset_links, _ = candidate_records(
        state, route_specs, asset_specs
    )
    readings = reading_records(state, candidates, route_specs, unit_links)
    assets = asset_records(state, asset_specs, asset_links)
    routes = [
        {key: value for key, value in row.items() if key != "key"}
        for row in route_specs
    ]
    return {
        "worker_id": WORKER_ID,
        "bundle_sha256": EXPECTED_BUNDLE_SHA,
        "allowed_manifest_sha256": EXPECTED_MANIFEST_SHA,
        "prompt_sha256": EXPECTED_PROMPT_SHA,
        "schema_sha256": EXPECTED_SCHEMA_SHA,
        "prohibited_input_nonuse": prohibited_nonuse,
        "reading_updates": readings,
        "asset_updates": assets,
        "candidate_proposals": candidates,
        "route_proposals": routes,
        "uncertainties": [],
    }


def canonical_bytes(output: dict[str, Any]) -> bytes:
    return (
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def validate_output(
    bundle: Path,
    output: dict[str, Any],
    *,
    require_finalized: bool | None = None,
) -> dict[str, int]:
    """Validate schema, provenance, link symmetry, and semantic guardrails."""

    import jsonschema

    state = load_bundle(bundle)
    schema = json.loads(
        (bundle / "input/schemas/worker-output.schema.json").read_text()
    )
    # The delivered schema intentionally requires the final declaration.  A
    # draft must pass every other schema constraint while keeping that
    # declaration false until verification and finalization are complete.
    if output["prohibited_input_nonuse"] is False:
        schema["properties"]["prohibited_input_nonuse"] = {"type": "boolean"}
    jsonschema.Draft202012Validator(schema).validate(output)

    if output["worker_id"] != WORKER_ID:
        raise ValueError("worker identity changed")
    expected_hashes = {
        "bundle_sha256": EXPECTED_BUNDLE_SHA,
        "allowed_manifest_sha256": EXPECTED_MANIFEST_SHA,
        "prompt_sha256": EXPECTED_PROMPT_SHA,
        "schema_sha256": EXPECTED_SCHEMA_SHA,
    }
    for key, value in expected_hashes.items():
        if output[key] != value:
            raise ValueError(f"{key} changed")
    if (
        require_finalized is not None
        and output["prohibited_input_nonuse"] is not require_finalized
    ):
        raise ValueError(
            "prohibited-input declaration does not match required finalization state"
        )
    if output["uncertainties"]:
        raise ValueError("bundle-level uncertainties were not expected")

    readings = output["reading_updates"]
    assets = output["asset_updates"]
    candidates = output["candidate_proposals"]
    routes = output["route_proposals"]
    if len(readings) != 276 or len(assets) != 80 or len(candidates) != 196:
        raise ValueError("unexpected output row count")
    if len(routes) != 24:
        raise ValueError("unexpected route count")
    if [row["source_unit_id"] for row in readings] != [
        row["source_unit_id"] for row in state["readings"]
    ]:
        raise ValueError("reading order changed")
    if [row["asset_id"] for row in assets] != [
        row["asset_id"] for row in state["assets"]
    ]:
        raise ValueError("asset order changed")
    if [row["id"] for row in candidates] != [
        f"W{i:04d}" for i in range(1, 197)
    ]:
        raise ValueError("candidate sequence is not contiguous")
    if [row["route_id"] for row in routes] != [
        f"WR{i:04d}" for i in range(1, 25)
    ]:
        raise ValueError("route sequence is not contiguous")

    immutable_reading_fields = [
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
    for base, row in zip(state["readings"], readings, strict=True):
        for field in immutable_reading_fields:
            if row[field] != base[field]:
                raise ValueError(f"reading projection changed: {row['source_unit_id']} {field}")
        if (
            row["review_status"] != "REVIEWED"
            or row["review_epoch"] != EPOCH
            or row["review_stage"] != STAGE
            or row["reviewer"] != REVIEWER
            or row["source_status"] != "CLEAR"
            or row["uncertainty"]
        ):
            raise ValueError(f"incomplete reading adjudication: {row['source_unit_id']}")
        as_json_array(row["secondary_roles"])
        as_json_array(row["candidate_ids"])
        as_json_array(row["route_ids"])

    immutable_asset_fields = [
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
    asset_by_id: dict[str, dict[str, str]] = {}
    asset_by_path: dict[str, dict[str, str]] = {}
    for base, row in zip(state["assets"], assets, strict=True):
        for field in immutable_asset_fields:
            if row[field] != base[field]:
                raise ValueError(f"asset projection changed: {row['asset_id']} {field}")
        if (
            row["inspection_status"] != "SCREENED"
            or row["review_epoch"] != EPOCH
            or row["review_stage"] != STAGE
            or row["reviewer"] != REVIEWER
            or row["source_status"] != "CLEAR"
            or row["uncertainty"]
            or row["original_resolution_status"] != "REVIEWED"
        ):
            raise ValueError(f"incomplete asset adjudication: {row['asset_id']}")
        flags = as_json_array(row["risk_flags"])
        as_json_array(row["candidate_ids"])
        as_json_array(row["route_ids"])
        if flags and row["transcription_status"] != "CHECKED":
            raise ValueError(f"unchecked risk-bearing asset: {row['asset_id']}")
        if (
            row["visual_role"] == "NATIVE_EVIDENCE"
            and "CONSTRUCTION_BEARING" not in flags
        ):
            raise ValueError(f"native asset lacks construction risk: {row['asset_id']}")
        asset_by_id[row["asset_id"]] = row
        asset_by_path[row["physical_path"]] = row

    evidence_ids: list[str] = []
    group_ids: list[str] = []
    candidate_by_id = {row["id"]: row for row in candidates}
    reading_by_id = {row["source_unit_id"]: row for row in readings}
    for candidate in candidates:
        if (
            candidate["record_status"] != "ACTIVE"
            or candidate["discovery_stage"] != 9
            or candidate["source_status"] != ["CLEAR"]
            or candidate["uncertainties"]
        ):
            raise ValueError(f"invalid candidate adjudication: {candidate['id']}")
        if set(candidate["field_support"]) != set(FIELDS):
            raise ValueError(f"incomplete field support: {candidate['id']}")
        if set(candidate["fingerprint"]) != set(FIELDS):
            raise ValueError(f"incomplete fingerprint: {candidate['id']}")
        anchor = candidate["discovery_anchor"]
        if anchor["epoch"] != 2:
            raise ValueError(f"wrong candidate epoch: {candidate['id']}")
        if anchor["kind"] == "SOURCE_UNIT":
            if anchor["id"] not in reading_by_id:
                raise ValueError(f"foreign source anchor: {candidate['id']}")
        elif anchor["kind"] == "IMAGE":
            if anchor["id"] not in asset_by_path:
                raise ValueError(f"foreign image anchor: {candidate['id']}")
        else:
            raise ValueError(f"search anchor in sequential review: {candidate['id']}")

        local_evidence_ids: set[str] = set()
        for evidence in candidate["source_evidence"]:
            evidence_ids.append(evidence["evidence_id"])
            group_ids.append(evidence["evidence_group_id"])
            local_evidence_ids.add(evidence["evidence_id"])
            evidence_anchor = evidence["discovery_anchor"]
            if evidence_anchor["epoch"] != 2:
                raise ValueError(f"wrong evidence epoch: {evidence['evidence_id']}")
            if evidence["source_unit_id"] not in candidate["source_unit_ids"]:
                raise ValueError(
                    f"evidence unit omitted from candidate: {evidence['evidence_id']}"
                )
            if evidence_anchor["kind"] == "IMAGE":
                asset = asset_by_path[evidence_anchor["id"]]
                if (
                    evidence["strength"]
                    in {"DIRECT_PARTIAL_MECHANICS", "DIRECT_COMPLETE_MECHANICS"}
                    and asset["visual_role"] != "NATIVE_EVIDENCE"
                ):
                    raise ValueError(
                        f"non-native image promoted to direct mechanics: {evidence['evidence_id']}"
                    )
                if evidence["image_path"] != asset["physical_path"]:
                    raise ValueError(f"image path mismatch: {evidence['evidence_id']}")
            elif evidence_anchor["kind"] == "SOURCE_UNIT":
                if evidence_anchor["id"] != evidence["source_unit_id"]:
                    raise ValueError(f"source anchor mismatch: {evidence['evidence_id']}")
            else:
                raise ValueError(f"search evidence in sequential review: {evidence['evidence_id']}")
            if not set(evidence["fingerprint_fields"]) <= set(FIELDS):
                raise ValueError(f"unknown evidence field: {evidence['evidence_id']}")

        for field in FIELDS:
            item = candidate["fingerprint"][field]
            if item["status"] != candidate["field_support"][field]:
                raise ValueError(f"field status mismatch: {candidate['id']} {field}")
            if item["status"] not in STATUSES:
                raise ValueError(f"unknown field status: {candidate['id']} {field}")
            if not set(item["evidence_ids"]) <= local_evidence_ids:
                raise ValueError(f"foreign field evidence: {candidate['id']} {field}")
            if item["status"] == "SUPPORTED":
                if item["value"] is None or not item["evidence_ids"]:
                    raise ValueError(f"unsupported supported field: {candidate['id']} {field}")
            else:
                if item["value"] is not None or item["evidence_ids"]:
                    raise ValueError(f"nonempty unresolved/N/A field: {candidate['id']} {field}")
            if item["status"] == "UNKNOWN_FROM_SOURCE":
                expected = (
                    f"The assigned source does not establish {field} for "
                    f"{candidate['provisional_name']}."
                )
                if expected not in candidate["missing_mechanics"]:
                    raise ValueError(
                        f"missing-mechanics duplication absent: {candidate['id']} {field}"
                    )
        for relation in candidate["related_candidate_ids"]:
            if relation["candidate_id"] not in candidate_by_id:
                raise ValueError(f"foreign candidate relation: {candidate['id']}")
            if relation["proof_kind"] != "PROVISIONAL_COMPARISON":
                raise ValueError(f"blind identity collapse attempted: {candidate['id']}")
        for route_id in candidate["cross_reference_ids"]:
            if route_id not in {row["route_id"] for row in routes}:
                raise ValueError(f"foreign candidate route: {candidate['id']}")

    if sorted(evidence_ids) != [
        f"WE{i:06d}" for i in range(1, len(evidence_ids) + 1)
    ]:
        raise ValueError("evidence sequence is not contiguous")
    if sorted(group_ids) != [
        f"WG{i:06d}" for i in range(1, len(group_ids) + 1)
    ]:
        raise ValueError("evidence-group sequence is not contiguous")
    if len(set(evidence_ids)) != len(evidence_ids) or len(set(group_ids)) != len(group_ids):
        raise ValueError("duplicate evidence identifiers")

    route_by_id = {row["route_id"]: row for row in routes}
    route_anchors: set[tuple[str, str, str, str]] = set()
    for route in routes:
        if (
            route["status"] != "PENDING"
            or route["discovery_epoch"] != EPOCH
            or route["owning_stage"] != STAGE
            or as_json_array(route["target_unit_ids"])
            or as_json_array(route["target_asset_ids"])
        ):
            raise ValueError(f"invalid blind route: {route['route_id']}")
        if route["source_unit_id"] not in reading_by_id:
            raise ValueError(f"foreign route source: {route['route_id']}")
        route_anchor = (
            route["discovery_epoch"],
            route["discovery_kind"],
            route["discovery_id"],
            route["discovery_ordinal"],
        )
        if route_anchor in route_anchors:
            raise ValueError(f"duplicate route discovery anchor: {route['route_id']}")
        route_anchors.add(route_anchor)
    for reading in readings:
        for route_id in as_json_array(reading["route_ids"]):
            if route_id not in route_by_id:
                raise ValueError(f"foreign reading route: {reading['source_unit_id']}")
            if route_by_id[route_id]["source_unit_id"] != reading["source_unit_id"]:
                raise ValueError(f"reading/route source mismatch: {route_id}")

    # Candidate links are symmetric across all candidate source/image rows.
    for candidate in candidates:
        candidate_id = candidate["id"]
        for unit_id in candidate["source_unit_ids"]:
            if candidate_id not in as_json_array(reading_by_id[unit_id]["candidate_ids"]):
                raise ValueError(f"missing reading link: {candidate_id} {unit_id}")
        for image_path in candidate["image_witnesses"]:
            matching = [
                row for row in assets if row["physical_path"] == image_path
            ]
            if len(matching) != 1:
                raise ValueError(f"nonunique image witness: {candidate_id} {image_path}")
            if candidate_id not in as_json_array(matching[0]["candidate_ids"]):
                raise ValueError(f"missing asset link: {candidate_id} {image_path}")
    for reading in readings:
        for candidate_id in as_json_array(reading["candidate_ids"]):
            candidate = candidate_by_id[candidate_id]
            image_units = {
                asset_by_path[evidence["discovery_anchor"]["id"]]["source_unit_id"]
                for evidence in candidate["source_evidence"]
                if evidence["discovery_anchor"]["kind"] == "IMAGE"
            }
            if (
                reading["source_unit_id"] not in candidate["source_unit_ids"]
                and reading["source_unit_id"] not in image_units
            ):
                raise ValueError(
                    f"orphan reading candidate link: {reading['source_unit_id']} {candidate_id}"
                )
    for asset in assets:
        for candidate_id in as_json_array(asset["candidate_ids"]):
            if asset["physical_path"] not in candidate_by_id[candidate_id]["image_witnesses"]:
                raise ValueError(f"orphan asset candidate link: {asset['asset_id']} {candidate_id}")

    dispositions: dict[str, int] = defaultdict(int)
    for row in readings:
        dispositions[row["review_disposition"]] += 1
    roles: dict[str, int] = defaultdict(int)
    for row in assets:
        roles[row["visual_role"]] += 1
    return {
        "readings": len(readings),
        "assets": len(assets),
        "candidates": len(candidates),
        "routes": len(routes),
        "evidence": len(evidence_ids),
        **{f"disposition:{key}": value for key, value in sorted(dispositions.items())},
        **{f"asset_role:{key}": value for key, value in sorted(roles.items())},
    }


def write_output(path: Path, output: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(output))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--author", action="store_true")
    mode.add_argument("--finalize", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--require-finalized", action="store_true")
    args = parser.parse_args()

    bundle = args.bundle.resolve()
    output_path = bundle / "output/output.json"
    if args.author:
        output = build_output(bundle, False)
        counts = validate_output(bundle, output, require_finalized=False)
        write_output(output_path, output)
    elif args.finalize:
        if not output_path.is_file():
            raise FileNotFoundError(output_path)
        current = output_path.read_bytes()
        expected_draft = build_output(bundle, False)
        if current != canonical_bytes(expected_draft):
            raise ValueError(
                "refusing finalization: current draft is not the verified deterministic author projection"
            )
        output = build_output(bundle, True)
        counts = validate_output(bundle, output, require_finalized=True)
        write_output(output_path, output)
    else:
        output = json.loads(output_path.read_text())
        counts = validate_output(
            bundle,
            output,
            require_finalized=True if args.require_finalized else None,
        )
        rebuilt = build_output(bundle, output["prohibited_input_nonuse"])
        if output_path.read_bytes() != canonical_bytes(rebuilt):
            raise ValueError("output is not the deterministic helper projection")

    print(json.dumps(counts, sort_keys=True))
    print(f"output_sha256={sha256(output_path)}")


if __name__ == "__main__":
    main()
