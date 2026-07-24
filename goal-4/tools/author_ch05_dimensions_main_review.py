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
    return {
        "manifest": manifest,
        "readings": readings,
        "assets": assets,
        "units": units,
        "source": source,
        "unit_by_id": {u["id"]: u for u in units},
        "asset_by_id": {a["asset_id"]: a for a in assets},
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
            "support": "finite active pattern represented on an unbounded or wrapped array",
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
        unknown = {"seed", "boundary", "termination_completion_failure", "witness_semantics"}
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
            "read_dependencies_or_neighborhood": "the element alone, or its checked neighboring cells for neighbor-dependent presets",
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
            "external_data",
            "termination_completion_failure",
            "witness_semantics",
        }
        unknown = {"boundary"}
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
            "successor_cardinality": "not applicable to an immutable graph",
            "determinism_branching_or_measure": "one denoted graph/class or enumerated finite set",
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
            "termination_completion_failure",
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
            "result_kind": "set of successor sequences and induced state-transition graph",
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
    elif kind == "CONSTRAINT":
        supported = {
            "object_kind": "constraint-defined model set",
            "native_time": "none; declarative satisfaction relation",
            "carrier": "one- or two-dimensional array of cells as stated",
            "support": "infinite line/grid, or finite region used as a witness/refutation",
            "topology": "nearest-neighbor line/grid or overlapping 3x3 templates as stated",
            "structural_invariants": "the same local constraint applies at every cell",
            "alphabet_or_value_schema": "black/white cell values",
            "complete_state": "a complete cell assignment",
            "boundary": "wrapping only where explicitly stated; otherwise an infinite carrier",
            "frontier_or_activation": "every cell must satisfy the relation",
            "schedule": "not applicable; constraints are simultaneous",
            "read_dependencies_or_neighborhood": "the stated neighbor count or overlapping template footprint",
            "law_kind": "declarative local constraint",
            "rule_relation_constraint_function_or_probability_law": name,
            "write_replacement_assembly_or_commit": "not applicable; acceptance is global satisfaction",
            "result_kind": "the set of satisfying assignments, possibly empty or unique",
            "successor_cardinality": "not applicable; solution-set cardinality may be zero, one, or many",
            "determinism_branching_or_measure": "declarative solution set without probability measure",
            "termination_completion_failure": "failure means no global satisfying assignment exists",
            "witness_semantics": "a complete satisfying pattern witnesses acceptance; a finite unsatisfiable region refutes global satisfiability",
            "parameters_and_variants": "neighbor counts, allowed template set, and required-occurrence template",
            "excluded_observers_and_representations": "search order, gray unknown cells, tessellation rendering, and CA correspondence are not the native constraint",
            "evidence_limit": "template contents are asserted only when checked in the assigned image",
        }
        na = {"visible_history", "control_state", "seed", "input", "external_data"}
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
            "successor_cardinality": "not applicable; the collection has 171 members",
            "determinism_branching_or_measure": "finite deterministic enumeration",
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
        }
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
        ["U000982", "U000993"],
        ["A000855"],
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

    tm2 = add(
        "illustrated three-state two-dimensional Turing machine",
        "TM2",
        "IMAGE",
        "A000865",
        1,
        ["U001010", "U001012"],
        ["A000865"],
        parameters={"head states": "three", "movement directions": "four"},
    )
    for ordinal, label in enumerate("abcde", 1):
        add(
            f"four-state two-dimensional Turing-machine rule ({label})",
            "TM2",
            "IMAGE",
            "A000870",
            ordinal,
            ["U001016", "U001026"],
            ["A000870"],
            aliases=[f"rule ({label})"],
            parameters={"head states": "four", "rule panel": label},
            parent_index=tm2,
            route_keys=["page-186-turing-rule"] if label == "e" else [],
        )

    sub2 = add(
        "two-dimensional parallel substitution-system family",
        "SUB_GRID",
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
    geom = add(
        "orientation-sensitive two-square geometrical replacement preset",
        "SUB_GEOM",
        "SOURCE_UNIT",
        "U001045",
        1,
        ["U001042", "U001045"],
        ["A000877", "A000878"],
        parameters={"replacement count": "two smaller black squares", "orientation": "carried by each square"},
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
        parent_index=geom,
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
            parent_index=geom,
        )
    neighbor_sub = add(
        "two-dimensional neighbor-dependent substitution-system family",
        "SUB_GRID",
        "SOURCE_UNIT",
        "U001056",
        1,
        ["U001056", "U001059"],
        ["A000882"],
        parameters={"boundary": "grid wraps in both dimensions", "dependency": "neighboring cells"},
        parent_index=sub2,
        route_keys=["page-85-interacting-substitution", "chapter-3-substitution-schedules"],
    )
    add(
        "illustrated neighbor-dependent substitution demonstration",
        "SUB_GRID",
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
            "SUB_GRID",
            "IMAGE",
            "A000882",
            ordinal,
            ["U001060"],
            ["A000882"],
            aliases=[f"neighbor-dependent preset ({label})"],
            parameters={"panel": label, "horizon": "eight steps"},
            parent_index=neighbor_sub,
        )

    network = add(
        "binary-outdegree network-system family",
        "NETWORK",
        "SOURCE_UNIT",
        "U001067",
        1,
        ["U001066", "U001067", "U001071", "U001090"],
        [],
        parameters={"outgoing connections per node": "two"},
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
                [["U001079", "U001080"], ["U001079", "U001081"], ["U001079", "U001082"]][ordinal - 1],
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
    for ordinal, label in enumerate("abcd", 1):
        units = ["U001095", "U001096", "U001097", "U001099"]
        add(
            f"binary-outdegree network rerouting rule ({label})",
            "NETWORK",
            "SOURCE_UNIT",
            "U001099",
            ordinal,
            units,
            ["A000888"],
            aliases=[f"network rule ({label})"],
            parameters={"rule panel": label},
            parent_index=network,
        )
    for ordinal, label in enumerate("ab", 1):
        add(
            f"node-inserting network rule ({label})",
            "NETWORK",
            "SOURCE_UNIT",
            "U001104",
            ordinal,
            ["U001100", "U001101", "U001104"],
            [f"A00088{8 + ordinal}"],
            aliases=[f"node-addition rule ({label})"],
            parameters={"rule panel": label, "seed": "single-node network"},
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
        "multiway state-deduplication demonstration rule",
        "MULTIWAY",
        "IMAGE",
        "A000905",
        1,
        ["U001151", "U001152", "U001155", "U001156", "U001158"],
        ["A000905", "A000906", "A000907"],
        parameters={
            "replacement set": "three checked graphical replacements",
            "history representation": "each sequence may be shown once with back-arrows to its first occurrence",
        },
        parent_index=multiway,
    )

    constraint_family = add(
        "constraint-specified system family",
        "CONSTRAINT",
        "SOURCE_UNIT",
        "U001161",
        1,
        ["U001161"],
        [],
    )
    add(
        "one-dimensional exact-one-black-and-one-white-neighbor constraint",
        "CONSTRAINT",
        "SOURCE_UNIT",
        "U001162",
        1,
        ["U001162", "U001164"],
        ["A000908"],
        parameters={"constraint": "every cell has exactly one black and one white neighbor"},
        parent_index=constraint_family,
    )
    add(
        "one-dimensional at-least-one-unlike-neighbor constraint",
        "CONSTRAINT",
        "SOURCE_UNIT",
        "U001166",
        1,
        ["U001166", "U001168"],
        ["A000909"],
        parameters={"constraint": "every cell has at least one neighbor of the opposite color"},
        parent_index=constraint_family,
    )
    fixed_specific = add(
        "two-dimensional neighbor-count constraint: black has one black, white has two white",
        "CONSTRAINT",
        "SOURCE_UNIT",
        "U001173",
        1,
        ["U001173", "U001175"],
        ["A000910", "A000911"],
        parameters={
            "black-center condition": "one black and three white orthogonal neighbors",
            "white-center condition": "two white and two black orthogonal neighbors",
        },
        parent_index=constraint_family,
    )
    fixed_family = add(
        "two-dimensional fixed black/white-neighbor-count constraint family",
        "CONSTRAINT",
        "SOURCE_UNIT",
        "U001178",
        1,
        ["U001178", "U001181"],
        ["A000911"],
        parameters={"neighborhood": "four orthogonal neighbors"},
        parent_index=constraint_family,
    )
    for row_black_neighbors in range(5):
        for col_white_neighbors in range(5):
            # The row/column matching the previously introduced prose preset is
            # linked as evidence there instead of duplicated.
            if row_black_neighbors == 1 and col_white_neighbors == 2:
                continue
            ordinal = row_black_neighbors * 5 + col_white_neighbors + 1
            add(
                "two-dimensional neighbor-count preset "
                f"(black-center black={row_black_neighbors}, "
                f"white-center white={col_white_neighbors})",
                "CONSTRAINT",
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
                },
                parent_index=fixed_family,
            )
    template_family = add(
        "overlapping local-template constraint family",
        "CONSTRAINT",
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
            "CONSTRAINT",
            "SOURCE_UNIT",
            "U001184",
            ordinal,
            ["U001184"],
            ["A000912"],
            aliases=[f"constraint {code}"],
            parameters={"constraint code": code, "displayed tessellation block": block},
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
        "CONSTRAINT",
        "SOURCE_UNIT",
        "U001190",
        1,
        ["U001190", "U001193"],
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
            "CONSTRAINT",
            "IMAGE",
            "A000915",
            ordinal,
            ["U001193"],
            ["A000915"],
            aliases=[f"constraint {code}"],
            parameters={"constraint code": code, "survey panel": str(ordinal)},
            parent_index=required_family,
        )
    enumeration_solver = add(
        "exhaustive complete-pattern enumeration constraint solver",
        "SOLVER",
        "SOURCE_UNIT",
        "U001197",
        1,
        ["U001197"],
        [],
        parameters={"strategy": "enumerate every possible pattern and test the constraint"},
    )
    backtracking_solver = add(
        "iterative region-growth backtracking constraint solver",
        "SOLVER",
        "SOURCE_UNIT",
        "U001198",
        1,
        ["U001198", "U001200", "U001201", "U001205"],
        ["A000916"],
        parameters={"strategy": "extend a small region in all possible ways and backtrack on violation"},
    )
    # Constraint 4670324 is already independently delimited in the ten-panel
    # survey; the later solver figure supports it rather than duplicating it.
    specs[code_to_index["4670324"] - 1]["units"].append("U001205")
    specs[code_to_index["4670324"] - 1]["assets"].append("A000916")
    for ordinal, code in enumerate(("373384574", "387520105"), 2):
        add(
            f"solver-witnessed constraint {code}",
            "CONSTRAINT",
            "SOURCE_UNIT",
            "U001205",
            ordinal,
            ["U001205"],
            ["A000916"],
            aliases=[f"constraint {code}"],
            parameters={"constraint code": code, "solver figure panel": chr(96 + ordinal)},
            parent_index=required_family,
        )
    add(
        "required-template constraint 18762389",
        "CONSTRAINT",
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
        parent_index=required_family,
        route_keys=["pages-214-215-constraint-order"],
    )
    template3 = add(
        "3x3 allowed-template constraint family",
        "CONSTRAINT",
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
        "CONSTRAINT",
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
        parent_index=template3,
    )
    add(
        "56-template rule-30-correspondence constraint",
        "CONSTRAINT",
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
        parent_index=template3,
    )

    assert len(specs) == 192, len(specs)
    return specs


def unit_literal(unit_id: str) -> str:
    # Stable symbolic marker expanded to source text after bundle loading.
    return f"@UNIT:{unit_id}"
