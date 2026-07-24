#!/usr/bin/env python3
"""Author one closed Stage 9 Chapter 5 LOCAL-search proposal.

The first invocation appends the mechanically deduplicated Chapter 5
vocabulary, the frozen fifteen-family search, and the candidates recovered by
the omission challenge.  A later invocation against the applied first round
repeats the exact query family with no semantic delta.

This reproducer is deliberately bound to the canonical Goal 4 state after
V000024.  It reads only the two reviewed Stage 9 source paths plus the blind
audit artifacts and never applies its proposal.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import unicodedata
from copy import deepcopy
from pathlib import Path
from typing import Any

import audit_transaction
import ch05_dimensions_search_route_specs
import merge_worker_output
import validate_audit
from audit_contract import (
    CANDIDATE_FIELDS,
    CROSS_REFERENCE_HEADER,
    FINGERPRINT_FIELDS,
    GOAL_DIR,
    REPO_ROOT,
    canonical_json_bytes,
)


STAGE_PATHS = [
    "CHAPTERS/05-Two-Dimensions-and-Beyond.md",
    "BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md",
]
NOTES_PATH = STAGE_PATHS[1]

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with IGNORECASE and MULTILINE semantics and "
    "query-major then canonical source-unit result order."
)

SIERPINSKI_SPECS = [
    (
        "U006151",
        "binomial-parity Sierpiński array generator",
        "Mod[Array[Binomial, {2, 2}^n, 0], 2]",
        "finite binary array for step n",
    ),
    (
        "U006152",
        "bitwise-AND-complement Sierpiński array generator",
        "1 - Sign[Array[BitAnd, {2, 2}^n, 0]]",
        "finite binary array for step n",
    ),
    (
        "U006153",
        "rotate-add modulo-2 Sierpiński evolution generator",
        "NestList[Mod[RotateLeft[#] + #, 2] &, PadLeft[{1}, 2^n], 2^n - 1]",
        "finite binary array for step n",
    ),
    (
        "U006154",
        "convolution modulo-2 Sierpiński evolution generator",
        "NestList[Mod[ListConvolve[{1, 1}, #, -1], 2] &, "
        "PadLeft[{1}, 2^n], 2^n - 1]",
        "finite binary array for step n",
    ),
    (
        "U006155",
        "bit-XOR recurrence Sierpiński array generator",
        "IntegerDigits[NestList[BitXor[2 #, #] &, 1, 2^n - 1], 2, 2^n]",
        "finite binary array for step n",
    ),
    (
        "U006156",
        "cumulative-sum modulo-2 Sierpiński evolution generator",
        "NestList[Mod[Rest[FoldList[Plus, 0, #]], 2] &, "
        "Table[1, {2^n}], 2^n - 1]",
        "finite binary array for step n",
    ),
    (
        "U006157",
        "binomial-coefficient Sierpiński array generator",
        "Table[PadRight[Mod[CoefficientList[(1 + x)^(t - 1), x], 2], "
        "2^n - 1], {t, 2^n}]",
        "finite binary array for step n",
    ),
    (
        "U006158",
        "bivariate-series Sierpiński array generator",
        "Reverse[Mod[CoefficientList[Series[1/(1 - (1 + x) y), "
        "{x, 0, 2^n - 1}, {y, 0, 2^n - 1}], {x, y}], 2]]",
        "finite binary array for step n",
    ),
    (
        "U006159",
        "block-join substitution Sierpiński array generator",
        "Nest[Apply[Join, MapThread[Join, {{#, #}, {0 #, #}}, 2]] &, "
        "{{1}}, n]",
        "finite binary array for step n",
    ),
    (
        "U006161",
        "affine-tripling Sierpiński coordinate enumerator",
        "Nest[Flatten[2 # /. {x_, y_} -> {{x, y}, {x + 1, y}, "
        "{x, y + 1}}, 1] &, {{0, 0}}, n]",
        "finite list of black-square coordinates for step n",
    ),
    (
        "U006162",
        "complex-affine Sierpiński coordinate enumerator",
        "(Transpose[{Re[#], Im[#]}] &)[Flatten[Nest["
        "{2 #, 2 # + 1, 2 # + I} &, {0}, n]]]",
        "finite list of black-square coordinates for step n",
    ),
    (
        "U006163",
        "odd-multiplicity Sierpiński coordinate enumerator",
        "Position[Map[Split, NestList[Sort[Flatten[{#, # + 1}]] &, "
        "{0}, 2^n - 1]], _?(OddQ[Length[#]] &), {2}]",
        "finite list of black-square coordinates for step n",
    ),
    (
        "U006164",
        "binary-position-fold Sierpiński coordinate enumerator",
        "Flatten[Table[Map[{t, #} &, Fold[Flatten[{#1, #1 + #2}] &, "
        "0, Flatten[2^(Position[Reverse[IntegerDigits[t, 2]], 1] - 1)]]], "
        "{t, 2^n - 1}], 1]",
        "finite list of black-square coordinates for step n",
    ),
    (
        "U006165",
        "nested-tree-path Sierpiński coordinate enumerator",
        "Map[Map[FromDigits[#, 2] &, Transpose[Partition[#, 2]]] &, "
        "Position[Nest[{{#, #}, {#}} &, 1, n], 1] - 1]",
        "finite list of black-square coordinates for step n",
    ),
]


def _spec(
    name: str,
    units: list[str],
    object_kind: str,
    carrier: str,
    input_value: str,
    law: str,
    result: str,
    *,
    aliases: list[str] | None = None,
    related: list[str] | None = None,
    limit: str = (
        "Only the identity and mechanics stated in the assigned source "
        "units are asserted."
    ),
    uncertainties: list[str] | None = None,
    profile: str | None = None,
    cardinality: str | None = None,
    measure: str | None = None,
    completion: str | None = None,
    evidence_scopes: dict[str, list[str]] | None = None,
    missing_mechanics: list[str] | None = None,
    discovery_unit: str | None = None,
    identity_unit: str | None = None,
    semantic_values: dict[str, Any] | None = None,
    not_applicable_exclusions: set[str] | None = None,
    suppress_supported_fields: set[str] | None = None,
) -> dict[str, Any]:
    if profile is None:
        lowered = object_kind.lower()
        if any(
            marker in lowered
            for marker in (
                "substitution-system preset",
                "substitution system",
                "cellular-automaton rule preset",
                "multiway-system preset",
                "generative-grammar preset",
                "generative grammar preset",
            )
        ):
            profile = "ITERATED"
        elif any(
            marker in lowered
            for marker in (
                "history embedding",
                "representation function",
                "quotient representation",
            )
        ):
            profile = "REPRESENTATION"
        elif any(
            marker in lowered
            for marker in (
                "predicate",
                "relation",
                "presentation",
            )
        ):
            profile = "RELATION"
        else:
            profile = "FUNCTION"
    if profile not in {
        "FUNCTION",
        "RELATION",
        "ITERATED",
        "REPRESENTATION",
        "DENOTATION",
    }:
        raise ValueError(f"unsupported candidate profile {profile}")
    discovery_unit = discovery_unit or units[0]
    identity_unit = identity_unit or discovery_unit
    if discovery_unit not in units or identity_unit not in units:
        raise ValueError(f"{name} identity/discovery unit is outside its sources")
    return {
        "name": name,
        "units": units,
        "object_kind": object_kind,
        "carrier": carrier,
        "input": input_value,
        "law": law,
        "result": result,
        "aliases": aliases or [],
        "related": related or [],
        "limit": limit,
        "uncertainties": uncertainties or [],
        "profile": profile,
        "cardinality": cardinality,
        "measure": measure,
        "completion": completion,
        "evidence_scopes": evidence_scopes or {},
        "missing_mechanics": missing_mechanics or [],
        "discovery_unit": discovery_unit,
        "identity_unit": identity_unit,
        "semantic_values": semantic_values or {},
        "not_applicable_exclusions": not_applicable_exclusions or set(),
        "suppress_supported_fields": suppress_supported_fields or set(),
    }


def _grammar_example_scopes(unit_id: str) -> dict[str, list[str]]:
    """Keep generic derivation mechanics separate from one grammar preset."""

    return {
        "U006267": [
            "native_time",
            "frontier_or_activation",
            "schedule",
            "read_dependencies_or_neighborhood",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "determinism_branching_or_measure",
        ],
        unit_id: [
            "object_kind",
            "carrier",
            "support",
            "alphabet_or_value_schema",
            "complete_state",
            "input",
            "seed",
            "law_kind",
            "rule_relation_constraint_function_or_probability_law",
            "result_kind",
            "parameters_and_variants",
            "evidence_limit",
        ],
    }


RECOVERED_SPECS = [
    _spec(
        "centered-singleton two-dimensional binary-array seed",
        ["U006080", "U006081"],
        "deterministic initial-state constructor",
        "finite n by n binary cell array",
        "array side length n",
        "PadLeft a singleton 1 to an n by n zero array with floor-half padding",
        "one centered-singleton binary array",
        aliases=["2D single-black-square seed"],
        related=["B0014"],
        evidence_scopes={
            "U006080": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006081": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
        discovery_unit="U006081",
        identity_unit="U006081",
    ),
    _spec(
        "outer-totalistic cellular automaton code 686",
        ["U006102", "U006117", "U006118"],
        "cellular-automaton rule preset",
        "two-dimensional binary cell array",
        "the source-stated code-686 two-dimensional rule preset",
        "apply the outer-totalistic rule identified by code 686",
        "the displayed component-pattern result attributed to code 686",
        aliases=["2D outer-totalistic code 686"],
        related=["B0859", "B0868"],
        limit=(
            "The identity is explicit, but the phrase “s alone” conflicts "
            "with the p/q/r component names actually defined nearby."
        ),
        uncertainties=[
            "The source does not soundly identify which p/q/r ablation the "
            "corrupt phrase “s alone” denotes."
        ],
        missing_mechanics=[
            "The component ablation associated with the defective phrase "
            "“s alone” is unresolved; only the code-686 identity is retained."
        ],
        evidence_scopes={
            "U006102": [
                "carrier",
                "support",
                "alphabet_or_value_schema",
                "read_dependencies_or_neighborhood",
                "law_kind",
                "evidence_limit",
            ],
            "U006117": [
                "object_kind",
                "carrier",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006118": ["result_kind"],
        },
        suppress_supported_fields={
            "native_time",
            "complete_state",
            "input",
            "frontier_or_activation",
            "schedule",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "successor_cardinality",
            "determinism_branching_or_measure",
        },
        discovery_unit="U006117",
        identity_unit="U006117",
    ),
    _spec(
        "stacked two-dimensional-cellular-automaton history embedding",
        ["U000969", "U000970", "U000971", "U000996", "U000997"],
        "history embedding/representation function",
        "successive two-dimensional cellular-automaton states",
        "an ordered cellular-automaton evolution history",
        "stack each successive 2D state along a third axis in time order",
        "one three-dimensional space-time object",
        aliases=["3D stack of 2D CA states"],
        limit=(
            "The source fixes the abstract alignment of successive 2D states "
            "along a time axis; camera orientation, scale, spacing, and pixel "
            "rendering remain representational choices."
        ),
        missing_mechanics=[
            "Rendered camera orientation, scale, layer spacing, and pixel "
            "style are not part of the stated abstract stack."
        ],
        cardinality=(
            "one abstract aligned space-time stack per ordered 2D history; "
            "rendered views can vary"
        ),
        measure=(
            "deterministic at the abstract cell-coordinate/time-layer level, "
            "not as a unique rendered picture"
        ),
    ),
    _spec(
        "two-dimensional-grid total-order linearization scan",
        ["U001061"],
        "scan-order/linearization class",
        "two-dimensional grid",
        "grid elements and a selected traversal variant",
        "visit every element in a total order by snaking rows or spiralling outward",
        "one ordered one-dimensional traversal",
        aliases=["snaking 2D scan", "spiralling 2D scan"],
        related=["B0290", "B0915"],
        limit=(
            "The source identifies snaking and spiral variants but does not "
            "give a coordinate formula or tie-breaking convention."
        ),
        missing_mechanics=[
            "Start cell, orientation, turn convention, extent, and tie "
            "breaking for the snaking and spiral scans are not specified."
        ],
        cardinality=(
            "one traversal only after the omitted start, orientation, turn, "
            "extent, and tie-breaking choices are fully supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic traversal "
            "from the two-dimensional grid alone"
        ),
    ),
    _spec(
        "network evolution node-count observer",
        ["U001112", "U001114", "U001115"],
        "trajectory observer",
        "network-system evolution history",
        "the network at each retained step",
        "count the total nodes in every retained network state",
        "a node-count time series",
        aliases=["network size trajectory"],
    ),
    _spec(
        "uniform linear binary-outdegree-network layout representation",
        ["U001091", "U001092", "U001093", "U001094", "U006225"],
        "network-layout representation function",
        "directed networks with two distinguished outgoing connections per node",
        (
            "one network plus retained node-origin/order metadata when the "
            "successive-line order must be recovered"
        ),
        (
            "arrange all nodes on one line, draw one distinguished outgoing "
            "connection above and the other below, and preserve incidence"
        ),
        "one uniform comparison diagram of the input network",
        related=["B0676"],
        profile="REPRESENTATION",
        limit=(
            "The representation identity and above/below connection convention "
            "are explicit, but node ordering is not recoverable from network "
            "numbering alone and the source gives no complete layout algorithm."
        ),
        uncertainties=[
            "The node-order algorithm, origin-record schema, arc geometry, "
            "crossing policy, and uniqueness/determinism are "
            "UNKNOWN_FROM_SOURCE."
        ],
        missing_mechanics=[
            "Node ordering requires retained new-node-origin metadata whose "
            "schema and update law are not supplied.",
            "Arc routing, crossing, spacing, tie breaking, and uniqueness of "
            "the final diagram are not specified.",
        ],
        semantic_values={
            "external_data": (
                "retained origin information for each new node, required when "
                "recovering the order shown on successive picture lines"
            )
        },
        not_applicable_exclusions={"external_data"},
        cardinality=(
            "one diagram for each fully specified node ordering and routing "
            "choice; the source does not fix those choices"
        ),
        measure=(
            "the source does not establish a unique or deterministic layout "
            "from the network and origin metadata alone"
        ),
        evidence_scopes={
            "U001091": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U001092": ["result_kind"],
            "U001093": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
            ],
            "U001094": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
            ],
            "U006225": ["external_data", "evidence_limit"],
        },
        discovery_unit="U001091",
        identity_unit="U001091",
    ),
    _spec(
        "multiway state-count and first-difference observer",
        ["U001130", "U001134", "U001135", "U001138", "U001139"],
        "trajectory observer",
        "multiway-system evolution history",
        "the distinct state collection at each retained step",
        "count distinct states per step and take successive count differences",
        "a state-count series and its first-difference series",
        evidence_scopes={
            "U001130": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U001134": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
            "U001135": [
                "result_kind",
                "parameters_and_variants",
            ],
            "U001138": [
                "result_kind",
            ],
            "U001139": [
                "object_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
        identity_unit="U001139",
    ),
    _spec(
        "arbitrary-offset neighborhood-configuration enumerator",
        ["U006096", "U006097"],
        "finite configuration enumerator",
        "ordered arbitrary-dimensional cellular-automaton neighborhood",
        "offset list os and alphabet size k",
        "reverse the table of length-|os| base-k digit vectors",
        "all k^|os| neighborhood configurations in canonical order",
        related=["B0857"],
        evidence_scopes={
            "U006096": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006097": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "general cellular-automaton rule-number codec",
        ["U006096", "U006098", "U006099", "U006101"],
        "rule-table codec",
        "k-color cellular-automaton rule table over arbitrary offsets",
        "ordered output table u or rule number num, alphabet size k, and offsets os",
        (
            "encode with FromDigits[Reverse[u], k] and recover the indexed "
            "base-k output digits in the stated neighborhood order"
        ),
        "a canonical rule number or decoded rule-output table",
        related=["B0857"],
        semantic_values={
            "excluded_observers_and_representations": (
                "The Map/ListCorrelate whole-state cellular-automaton update "
                "is an application of the decoded table governed by B0857, "
                "not part of this representation codec."
            )
        },
        not_applicable_exclusions={
            "excluded_observers_and_representations",
        },
        evidence_scopes={
            "U006096": [
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006098": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            ],
            "U006099": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "excluded_observers_and_representations",
            ],
            "U006101": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "excluded_observers_and_representations",
            ],
        },
        identity_unit="U006098",
    ),
    _spec(
        "two-dimensional cellular-automaton rule-family cardinality query",
        ["U006102", "U006105"],
        "finite-family cardinality query",
        "two-dimensional binary cellular-automaton rule families",
        "neighborhood topology and symmetry/totalistic restriction class",
        "return the exact tabled number of possible rules for the selected class",
        "one finite rule-family cardinality",
        related=["B0858", "B0859", "B0860"],
        evidence_scopes={
            "U006102": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006105": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "growth-totalistic trigger-list-to-outer-totalistic-code encoder",
        ["U006103", "U006104", "U006110"],
        "rule-code encoder",
        "binary growth-totalistic cellular-automaton trigger list",
        "neighbor count s or n and the counts that turn a cell black",
        "encode forced persistence plus the trigger list using either stated equivalent power-sum parameterization",
        "one outer-totalistic code number for the growth rule",
        related=["B0859", "B0860"],
        evidence_scopes={
            "U006103": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006104": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U006110": [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "symmetric-5-neighbor-to-general-rule-code converter",
        ["U006106", "U006107", "U006108", "U006109"],
        "rule-code converter",
        "binary 5-neighbor cellular-automaton rule table",
        "a 12-bit completely symmetric rule number",
        "expand each symmetry-class bit to its 32 general-neighborhood positions and read the result as a base-2 number",
        "one equivalent general-form rule number",
        related=["B0861"],
        evidence_scopes={
            "U006106": [
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006107": [
                "carrier",
                "input",
                "parameters_and_variants",
            ],
            "U006108": [
                "object_kind",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006109": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
        },
        identity_unit="U006108",
    ),
    _spec(
        "two-dimensional Turing-machine head-position trajectory observer",
        ["U006139", "U006140"],
        "trajectory observer",
        "two-dimensional Turing-machine evolution",
        "a 2D Turing-machine run and retained step bound",
        "select the head position at each successive retained step",
        "an ordered two-dimensional position trajectory",
        limit=(
            "The assigned source states the 500-step trajectory projection "
            "but gives no standalone implementation formula."
        ),
    ),
    _spec(
        "finite-automaton digit-array substitution-pattern generator",
        ["U006147", "U006148", "U006149"],
        "uniterated finite-array generator",
        "k^n by k^n binary array",
        "step n, radix k, and excluded digit-pair pattern form",
        "test each transposed pair of position-digit sequences against form and emit 1 exactly when it is absent",
        "one complete step-n binary substitution pattern",
        related=["B0897", "B0898"],
        evidence_scopes={
            "U006147": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006148": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U006149": [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "five-dimensional cut-and-project Penrose tiling generator",
        ["U006182"],
        "cut-and-project tiling generator",
        "a two-dimensional plane through a five-dimensional hypercubic lattice",
        "a plane whose slopes are based on GoldenRatio",
        (
            "derive the tiling from how the selected two-dimensional plane "
            "cuts through the five-dimensional hypercubic lattice"
        ),
        "a Penrose tiling with approximate fivefold symmetry",
        related=["B0904"],
        missing_mechanics=[
            "The cut window, plane offset, lattice-intersection convention, "
            "and exact projection map are not specified."
        ],
        cardinality=(
            "one tiling only after the omitted cut window, plane offset, "
            "intersection convention, and projection map are fully supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic tiling "
            "without those omitted cut-and-project choices"
        ),
    ),
    _spec(
        "quadratic-irrational hyperplane cut-and-project nested-pattern family",
        ["U006183"],
        "cut-and-project pattern family",
        "hyperplanes projected from regular lattices in arbitrary dimensions",
        "a regular lattice and quadratic-irrational hyperplane slopes",
        "project the regular lattice along the selected irrational hyperplane",
        "a nested pattern representable by shape subdivision",
        missing_mechanics=[
            "The source does not specify the acceptance window, offsets, "
            "projection coordinates, or boundary convention for this family."
        ],
        cardinality=(
            "one pattern only after the omitted acceptance window, offsets, "
            "projection coordinates, and boundary convention are fully supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic pattern "
            "without those omitted cut-and-project choices"
        ),
    ),
    _spec(
        "base-(i-1) binary-digit point-set generator",
        ["U006187", "U006188", "U006189"],
        "uniterated geometric point-set generator",
        "complex plane",
        "digit length t",
        "evaluate every t-digit binary integer in complex base i-1",
        "the finite step-t dragon-curve point set",
        related=["B0905"],
        evidence_scopes={
            "U006187": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006188": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U006189": [
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
    ),
    _spec(
        "box-counting fractal-dimension observer",
        ["U006193", "U006194", "U006195"],
        "geometric scaling observer",
        "a planar pattern under successively finer grids",
        "pattern and grid edge scale a",
        "infer d from occupied-square count N(a) scaling as (1/a)^d",
        "a dimension estimate or scale-dependent exponent profile",
        limit=(
            "The exponent may fluctuate or fail to converge; the source does "
            "not fix one estimator for every nonconvergent case."
        ),
        missing_mechanics=[
            "Grid-origin dependence and the estimator/reporting convention "
            "for a fluctuating or nonconvergent small-scale exponent are open."
        ],
        cardinality=(
            "one estimate only after the omitted grid origin, sampled scales, "
            "fitting range, estimator, and reporting convention are supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic estimate "
            "when the scale-dependent exponent fluctuates or fails to converge"
        ),
    ),
    _spec(
        "grid-occupancy distribution-moment observer",
        ["U006196"],
        "geometric distribution observer",
        "gray amount distributed among grid squares",
        "a gridded pattern and selected moment orders",
        "compute mean, variance, and higher moments of grid-square gray amount",
        "generalized fractal-dimension descriptors",
        limit=(
            "The source identifies distribution moments as possible "
            "descriptors but does not fix grid origin, gray normalization, "
            "moment orders, descriptor mapping, or reporting convention."
        ),
        missing_mechanics=[
            "Grid placement, gray-mass normalization, selected moments, the "
            "moment-to-descriptor map, and reporting conventions are omitted."
        ],
        cardinality=(
            "one descriptor collection only after the omitted grid, "
            "normalization, moment, mapping, and reporting choices are supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic descriptor "
            "collection from the pattern alone"
        ),
    ),
    _spec(
        "Julia-set zero-membership to Mandelbrot-boundary relation",
        ["U006202", "U006203", "U006204"],
        "parameter-space membership relation",
        "complex parameters c and their Julia sets",
        "a parameter c",
        "accept exactly when the Julia set for c contains z=0",
        "membership in the boundary of the Mandelbrot set",
        related=["B0912", "B0913"],
        evidence_scopes={
            "U006202": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006203": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "determinism_branching_or_measure",
                "witness_semantics",
                "parameters_and_variants",
            ],
            "U006204": [
                "result_kind",
                "witness_semantics",
            ],
        },
    ),
    _spec(
        "Julia-set nearest-distance field observer",
        ["U006203", "U006204"],
        "parameter-space distance observer",
        "Julia set associated with each complex parameter c",
        "parameter c and fixed point z0",
        "minimize Abs[z-z0] over points z in the Julia set",
        "one nonnegative distance/gray-level field value",
        related=["B0912", "B0913"],
    ),
    _spec(
        "directed cyclic-network generator",
        ["U006211", "U006212"],
        "uniterated graph generator",
        "n labelled nodes with above and below directed connections",
        "positive node count n",
        "connect each node to its two cyclic neighbors using CyclicNet",
        "one directed cyclic network represented as n connection pairs",
        aliases=["CyclicNet"],
        related=["B0789", "B0916"],
        evidence_scopes={
            "U006211": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006212": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "directed-network connection-path follower",
        ["U006213", "U006214"],
        "graph path query",
        "directed above/below connection-list network",
        "network list, start node i, and connection-symbol sequence s",
        "fold the indexed connection choices over the start node",
        "the uniquely reached node",
        aliases=["Follow"],
        related=["B0916"],
    ),
    _spec(
        "directed-network cumulative-radius node-count observer",
        ["U006215", "U006216"],
        "graph neighborhood observer",
        "directed above/below connection-list network",
        "network list, start node i, and depth d",
        (
            "repeatedly expand and union reachable nodes, then count each "
            "cumulative reachable set"
        ),
        "counts of distinct nodes reachable within radii 1 through d",
        aliases=["NeighborNumbers"],
        related=["B0916"],
    ),
    _spec(
        "directed-network reachable-component query",
        ["U006219", "U006220"],
        "graph reachability query",
        "directed above/below connection-list network",
        "network list and start node i",
        "take the fixed point of adjoining all outgoing neighbors",
        "the set of all nodes reachable from i",
        aliases=["ConnectedNodes"],
        related=["B0916"],
    ),
    _spec(
        "directed-network closed-retained-sequence renumbering transform",
        ["U006221", "U006222"],
        "graph relabelling transform",
        "directed connection-list network",
        (
            "network list and a retained node sequence closed under every "
            "endpoint referenced by its selected rows"
        ),
        "select retained rows and replace every endpoint by its position in the retained sequence",
        "one compactly renumbered closed retained network",
        aliases=["RenumberNodes"],
        related=["B0916"],
        limit=(
            "The code assumes that every endpoint in the selected rows occurs "
            "in seq; the source does not state behavior when this closure "
            "precondition fails."
        ),
        missing_mechanics=[
            "Failure behavior for a retained sequence that omits a referenced "
            "endpoint is not specified."
        ],
        cardinality=(
            "one renumbered network for each valid endpoint-closed retained "
            "sequence"
        ),
        measure=(
            "deterministic on endpoint-closed inputs; behavior outside that "
            "source-unstated domain is unknown"
        ),
        completion=(
            "returns the compact renumbering when every selected endpoint is "
            "present in seq; failure behavior otherwise is unknown"
        ),
    ),
    _spec(
        "page-202(c) network node-count sequence generator",
        ["U006227", "U006228"],
        "uniterated integer-sequence generator",
        "network-size trajectory for the stated page-202(c) preset",
        "maximum step t",
        "evaluate the supplied FoldList and binary-digit recurrence d",
        "the list of node counts through step t",
        evidence_scopes={
            "U006227": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006228": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "network dimensionality observer",
        ["U006234", "U006235"],
        "graph-volume scaling observer",
        "a network at a selected evolution step",
        "network, reference node, and connection radius r",
        "count distinct nodes reachable within r connections and compare with r^d",
        "a dimension estimate or reachable-volume growth curve",
        limit=(
            "The source supplies the reachable-volume scaling criterion and "
            "plots but does not fix a fitting range, estimator, root-node "
            "aggregation, or nonconvergence convention."
        ),
        missing_mechanics=[
            "The fitting range, estimator, root-node aggregation, and behavior "
            "when the r^d exponent does not converge are not specified."
        ],
        cardinality=(
            "one estimate only after the omitted fitting range, estimator, "
            "root-node aggregation, and nonconvergence convention are supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic dimension "
            "estimate from the network and radius data alone"
        ),
    ),
    _spec(
        "polynomial-growth string-multiway preset",
        ["U006240", "U006243", "U006252"],
        "multiway-system preset",
        "strings rewritten by three bidirectional-availability replacement rules",
        "the displayed rule and an initial string containing n B symbols",
        "apply all replacements and merge equal successor strings",
        "a multiway evolution whose state count grows as t^(n+1)",
        related=["B0921"],
        evidence_scopes={
            "U006240": [
                "carrier",
                "support",
                "alphabet_or_value_schema",
                "complete_state",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006243": [
                "native_time",
                "frontier_or_activation",
                "schedule",
                "read_dependencies_or_neighborhood",
                "rule_relation_constraint_function_or_probability_law",
                "write_replacement_assembly_or_commit",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U006252": [
                "object_kind",
                "carrier",
                "complete_state",
                "seed",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
        discovery_unit="U006252",
        identity_unit="U006252",
    ),
    _spec(
        "bounded-length multiway reachability observer",
        ["U006258", "U006259"],
        "multiway reachability observer",
        "string-multiway evolution",
        "the referenced system and maximum string length 10",
        "retain which strings of length at most 10 are reached anywhere in the evolution",
        "a bounded set or incidence map of reachable strings",
        limit=(
            "OCR truncates one word in the caption and the unit does not state "
            "the plotted encoding or a standalone implementation."
        ),
        uncertainties=[
            "The source contains the defective text “shows wh” and omits the "
            "plot-axis/string encoding."
        ],
        missing_mechanics=[
            "The OCR-defective caption leaves the displayed incidence/axis "
            "encoding and any standalone bounded-reach algorithm unspecified."
        ],
    ),
    _spec(
        "multiway equivalence-class quotient representation",
        ["U006261", "U006262"],
        "quotient representation",
        "all strings under a group or semigroup rewrite relation",
        "a bidirectional rule presentation",
        "partition strings by mutual transformability under the rules",
        "group/semigroup elements as disconnected multiway-network components",
        cardinality=(
            "one quotient partition/element representation per fully "
            "specified bidirectional presentation"
        ),
        measure="deterministic declarative quotient formation",
        evidence_scopes={
            "U006261": [
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006262": [
                "object_kind",
                "carrier",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
        discovery_unit="U006262",
        identity_unit="U006262",
    ),
    _spec(
        "group-or-semigroup Cayley-graph generator family",
        ["U006263"],
        "graph generator family",
        "elements of a presented group or semigroup",
        "a presentation and its generator symbols",
        "connect each element to the element obtained by appending each generator",
        "the presentation's Cayley graph",
        profile="DENOTATION",
        limit=(
            "The source defines the Cayley graph declaratively but gives no "
            "general algorithm for enumerating quotient elements, deciding "
            "word equality, or completing an infinite presentation."
        ),
        missing_mechanics=[
            "General quotient-element enumeration, word-equality decisions, "
            "and finite/infinite completion behavior are unspecified."
        ],
        cardinality=(
            "one declarative Cayley graph for each fully specified quotient "
            "element set and generator action"
        ),
        measure=(
            "deterministic mathematical denotation, not a claimed terminating "
            "graph-enumeration procedure"
        ),
    ),
    _spec(
        "free-semigroup Cayley-tree preset",
        ["U006263"],
        "Cayley-graph preset",
        "all finite strings over the selected free generators",
        "a generator alphabet with no relations",
        "append each generator to form distinct child elements",
        "a rooted branching Cayley tree",
    ),
    _spec(
        "commutative-semigroup Cayley-grid preset",
        ["U006263"],
        "Cayley-graph preset",
        "equivalence classes of strings over A and B",
        "relations AB→BA and BA→AB",
        "quotient by permutation of A and B order and connect by generator appends",
        "a two-dimensional grid Cayley graph",
    ),
    _spec(
        "A5 icosahedral-group presentation",
        ["U006264"],
        "finite-group presentation",
        "words in generators x and y modulo relations",
        "relations x^2 = y^3 = (x y)^5 = 1",
        "identify words modulo the stated presentation",
        "the 60-element icosahedral group A5",
        profile="DENOTATION",
        cardinality="one denoted quotient group",
        measure="deterministic declarative denotation",
    ),
    _spec(
        "Monster Group finite-group denotation with source-omitted presentation",
        ["U006264", "U006265"],
        "source-limited finite-group denotation",
        "the named finite simple Monster Group",
        "the source-omitted set of about a dozen defining rules",
        (
            "take the finite group that the source says is obtained from the "
            "unstated presentation"
        ),
        (
            "the named Monster Group with the exact finite order stated in "
            "the continuation"
        ),
        profile="DENOTATION",
        cardinality="one named finite group",
        measure="deterministic named denotation",
        limit=(
            "The source names the group and gives its exact order but omits "
            "the generators, relations, rule list, and quotient construction."
        ),
        uncertainties=[
            "The actual dozen-or-so rules, generators, relations, quotient "
            "mechanics, and reconstruction procedure are "
            "UNKNOWN_FROM_SOURCE."
        ],
        missing_mechanics=[
            "No executable or declaratively complete presentation is supplied; "
            "only the named denotation and exact order are recoverable."
        ],
        semantic_values={
            "parameters_and_variants": (
                "about a dozen source-omitted defining rules; no generators "
                "or relations are supplied"
            )
        },
        suppress_supported_fields={
            "input",
            "rule_relation_constraint_function_or_probability_law",
        },
        discovery_unit="U006264",
        identity_unit="U006264",
        evidence_scopes={
            "U006264": [
                "object_kind",
                "carrier",
                "law_kind",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006265": [
                "result_kind",
                "evidence_limit",
            ],
        },
    ),
    _spec(
        "finite group-and-semigroup count-by-order observer",
        ["U006336", "U006337"],
        "size-indexed finite-structure count observer",
        "isomorphism classes of finite groups or semigroups",
        "structure class and finite order n",
        "count distinct finite groups or semigroups of order n",
        "one count value or the count sequence indexed by n",
        limit=(
            "The source gives the count curves and an asymptotic peak bound "
            "but explicitly notes that classification supplies no practical "
            "general enumeration procedure."
        ),
        missing_mechanics=[
            "No executable enumeration algorithm, isomorphism test, or "
            "completion bound is supplied for the finite-structure counts."
        ],
    ),
    _spec(
        "nim zero-XOR losing-position predicate",
        ["U006276"],
        "game-position predicate/strategy query",
        "normal-play nim pile-height vectors",
        "pile-height vector h",
        "accept exactly when Apply[BitXor,h] equals zero",
        "whether the position is the stated forced-loss target class",
        related=["B0933"],
    ),
    _spec(
        "finite-element PDE discretization family",
        ["U006280"],
        "continuous-to-discrete approximation family",
        "partial differential equation with initial or boundary data",
        "a PDE problem and discretization choices",
        "construct a finite-element discrete approximation for numerical solution",
        "a discrete algebraic approximation to the PDE problem",
        related=["B0647", "B0935", "B0936"],
        limit=(
            "The source identifies the method family and role but supplies no "
            "element basis, mesh, assembly formula, or convergence contract."
        ),
        missing_mechanics=[
            "Element family, basis, mesh construction, weak form, matrix "
            "assembly, boundary enforcement, solver, and convergence/error "
            "contract are all unspecified."
        ],
        cardinality=(
            "one discrete approximation only after the omitted element, "
            "basis, mesh, weak-form, assembly, boundary, and solver choices "
            "are fully supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic "
            "discretization from the PDE problem alone"
        ),
    ),
    _spec(
        "linear-vector forward-map evaluator",
        ["U006281"],
        "uniterated linear map",
        "continuous-number vectors and matrices",
        "matrix m and vector v",
        "compute u = m.v",
        "one vector u",
        related=["B0937"],
    ),
    _spec(
        "linear-system inverse solver",
        ["U006281"],
        "uniterated equation solver",
        "continuous-number vectors and matrices",
        (
            "matrix m and target vector u under source-unstated rank and "
            "consistency conditions"
        ),
        "evaluate LinearSolve[m,u] to find v satisfying u = m.v",
        "a solution vector v when the system is in the method's valid domain",
        aliases=["LinearSolve inverse"],
        related=["B0937"],
        limit=(
            "The source does not state singular, inconsistent, or "
            "underdetermined-system behavior."
        ),
        uncertainties=[
            "The source does not say which solution is selected for an "
            "underdetermined system or how inconsistent/singular cases fail."
        ],
        missing_mechanics=[
            "Rank, consistency, solution-selection, singularity, and failure "
            "conventions are unspecified."
        ],
        cardinality=(
            "zero, one, or many mathematical solutions depending on rank and "
            "consistency; the source does not state LinearSolve selection"
        ),
        measure=(
            "deterministic only on the unstated domain where the implementation "
            "selects one solution; other cases are unknown"
        ),
        completion=(
            "returns a solution on an unstated valid domain; singular, "
            "inconsistent, and underdetermined completion behavior is unknown"
        ),
    ),
    _spec(
        "two-dimensional constraint-number decoder",
        ["U006286", "U006287", "U006288"],
        "constraint-code decoder",
        "the canonically ordered 32 binary 5-cell templates",
        "integer constraint number n",
        "select template positions where IntegerDigits[n,2,32] has value 1",
        "the allowed-template set encoded by n",
        related=["B0943"],
        evidence_scopes={
            "U006286": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006287": [
                "result_kind",
            ],
            "U006288": [
                "carrier",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
    ),
    _spec(
        "allowed-template satisfaction predicate",
        ["U006288", "U006289"],
        "finite-array constraint predicate",
        "binary arrays and 3 by 3 template patterns",
        "array list and allowed-template pattern",
        "partition into overlapping 3 by 3 blocks and require every block to match allowed",
        "one Boolean satisfaction judgment",
        aliases=["SatisfiedQ"],
        related=["B0943"],
        profile="FUNCTION",
    ),
    _spec(
        "overlapping-corner tessellation descriptor and Fill generator",
        ["U006290", "U006291", "U006292", "U006293"],
        "repetitive-pattern codec/generator",
        "finite rectangular binary array",
        "four overlap vectors, one data tile, and output dimensions nx by ny",
        "map output coordinates through the overlap lattice and replace canonical residue positions by tile data",
        "one finite array filled by the represented repetitive tessellation",
        aliases=["Fill overlapping-corner tessellation"],
    ),
    _spec(
        "Ammann 16-symbol substitution system",
        ["U006301", "U006302", "U006303", "U006304"],
        "two-dimensional substitution system",
        "arrays over sixteen substitution symbols/colors",
        (
            "a current finite array over the sixteen symbols and the displayed "
            "16-symbol replacement table"
        ),
        "replace every symbol by its displayed block at each step",
        "one successor nested-pattern array",
        related=["B0948"],
        limit=(
            "The complete 16-symbol replacement table is explicit, but the "
            "source does not state the initial symbol or array used for the "
            "displayed nested pattern."
        ),
        uncertainties=[
            "The seed or initial condition for the displayed Ammann pattern "
            "is not stated."
        ],
        missing_mechanics=[
            "The initial symbol or finite seed array is unspecified."
        ],
        evidence_scopes={
            "U006301": [
                "object_kind",
                "native_time",
                "carrier",
                "support",
                "alphabet_or_value_schema",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006302": [
                "complete_state",
                "frontier_or_activation",
                "schedule",
                "read_dependencies_or_neighborhood",
                "rule_relation_constraint_function_or_probability_law",
                "write_replacement_assembly_or_commit",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U006303": [
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006304": [
                "result_kind",
            ],
        },
    ),
    _spec(
        "Cook-polyomino stage type-count observer",
        ["U006314", "U006316", "U006317"],
        "stage-indexed count-vector observer",
        "the stated Cook aperiodic polyomino construction",
        "construction stage n",
        "evaluate Fibonacci[2 n - {2,0,1}] / {1,2,1}",
        "the three polyomino-type counts at stage n",
        related=["B0954"],
        evidence_scopes={
            "U006314": [
                "object_kind",
                "carrier",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006316": [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006317": [
                "result_kind",
            ],
        },
        discovery_unit="U006316",
        identity_unit="U006314",
    ),
    _spec(
        "square-free sequence enumerator",
        ["U006318", "U006319"],
        "finite solution enumerator",
        "length-n sequences over k symbols",
        "alphabet size k and target length n",
        "extend every surviving sequence by each symbol and delete any containing adjacent identical blocks",
        "all length-n square-free sequences",
        related=["B0959"],
        evidence_scopes={
            "U006318": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006319": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
        },
    ),
    _spec(
        "Pell least-x continued-fraction solver",
        ["U006326", "U006327", "U006328", "U006329"],
        "Diophantine least-solution solver",
        "positive integer solutions of x^2 = a y^2 + 1",
        "positive nonsquare integer a",
        "evaluate the stated continued-fraction convergent numerator",
        "the least positive solution value x",
        related=["B0968"],
        evidence_scopes={
            "U006326": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006327": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U006328": [
                "result_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006329": [
                "result_kind",
            ],
        },
    ),
    _spec(
        "primitive Pythagorean-triple parameterization",
        ["U006330", "U006331"],
        "Diophantine solution generator",
        "integer triples satisfying x^2 + y^2 = z^2",
        "integer parameters r and s under the unstated primitive-case restrictions",
        "return {r^2-s^2, 2 r s, r^2+s^2}",
        "a Pythagorean triple for valid primitive-case parameter choices",
        related=["B0969"],
        limit=(
            "The source states the parameterization after removing common "
            "factors but does not spell out parity, ordering, or coprimality "
            "restrictions, nor a completeness convention."
        ),
        uncertainties=[
            "The valid parity, coprimality, ordering, sign, and completeness "
            "conditions on r and s are UNKNOWN_FROM_SOURCE."
        ],
        missing_mechanics=[
            "Parity, coprimality, order, sign, duplicate-removal, and "
            "completeness conditions for r and s are not specified."
        ],
    ),
    _spec(
        "four-neighbor two-dimensional mobile-automaton rule cardinality",
        ["U006143"],
        "finite rule-family cardinality function",
        "k-color 2D mobile-automaton rules with four neighbors",
        "alphabet size k",
        "evaluate (4 k)^(k^5)",
        "the number of possible rules in the stated family",
        related=["B0896"],
    ),
    _spec(
        "four-color square-array emulator of the golden-rectangle substitution",
        ["U006177"],
        "two-dimensional substitution-system preset",
        "equal-sized square cells carrying four color/orientation labels",
        "the displayed four-color rule and singleton initial array {{3}}",
        "replace every color by its displayed rectangular block",
        "a successor square-array pattern reproducing the geometric system's behavior",
        related=["B0903"],
        limit=(
            "The source asserts behavioral reproduction after encoding shape "
            "and orientation as colors; it does not identify the square-array "
            "state with the geometric native state."
        ),
    ),
    _spec(
        "random-Boolean-network node-rule cardinality",
        ["U006238"],
        "finite rule-family cardinality function",
        "Boolean node rules with s inputs",
        "input arity s",
        "evaluate 2^(2^s)",
        "the number of possible Boolean rules for one s-input node",
        related=["B0920"],
    ),
    _spec(
        "balanced-parenthesis generative-grammar preset",
        ["U006267"],
        "generative-grammar preset",
        "strings over parentheses plus nonterminal x",
        "rules x→xx, x→(x), x→() with initial string x",
        "apply every grammar production in all possible ways until terminal strings contain no x",
        "the language of balanced parenthesis strings",
    ),
    _spec(
        "no-adjacent-B regular-grammar preset",
        ["U006267", "U006268"],
        "regular generative-grammar preset",
        "strings over terminals A/B and nonterminals x/y",
        "the displayed three productions with initial symbol x",
        "apply the regular productions in all possible ways",
        "sequences in which no pair of B symbols appears together",
        related=["B0926"],
        limit=(
            "The source asserts the no-adjacent-B language, but every displayed "
            "production retains x or y even though U006267 defines final "
            "expressions as containing no nonterminal."
        ),
        uncertainties=[
            "The asserted terminal A/B language conflicts with the displayed "
            "rules, which never eliminate their sole x/y nonterminal."
        ],
        missing_mechanics=[
            "A terminalization or projection convention that removes the "
            "remaining x/y nonterminal is not supplied."
        ],
        suppress_supported_fields={
            "result_kind",
        },
        evidence_scopes=_grammar_example_scopes("U006268"),
        discovery_unit="U006268",
        identity_unit="U006268",
    ),
    _spec(
        "AxA-or-B context-free-grammar preset",
        ["U006267", "U006269"],
        "context-free generative-grammar preset",
        "strings over terminal symbols A/B and nonterminal x",
        "rules x→AxA and x→B with initial x",
        "replace any occurrence of x by AxA or B",
        "the generated context-free language",
        related=["B0927"],
        evidence_scopes=_grammar_example_scopes("U006269"),
        discovery_unit="U006269",
        identity_unit="U006269",
    ),
    _spec(
        "equal-count ABA context-sensitive-grammar preset",
        ["U006267", "U006270"],
        "context-sensitive generative-grammar preset",
        "strings over A, B, and nonterminal x",
        "the displayed three rules with initial string AAxBA",
        "apply all permitted context-sensitive replacements",
        "strings A^n B^n A^n in the source's stated form",
        related=["B0928"],
        evidence_scopes=_grammar_example_scopes("U006270"),
        discovery_unit="U006270",
        identity_unit="U006270",
    ),
    _spec(
        "numeric-multiway Fibonacci state-count function",
        ["U006273", "U006274", "U006275"],
        "exact trajectory count function",
        "distinct numbers in the n→{n+1,2n} multiway evolution",
        "step t",
        "evaluate Fibonacci[t+2]",
        "the number of distinct numeric states at step t",
        related=["B0932"],
        evidence_scopes={
            "U006273": [
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006274": [
                "carrier",
                "parameters_and_variants",
            ],
            "U006275": [
                "object_kind",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
        discovery_unit="U006275",
        identity_unit="U006275",
    ),
    _spec(
        "quadratic-vector forward-map evaluator",
        ["U006281"],
        "uniterated nonlinear map",
        "continuous-number vectors and matrices",
        "matrices m1/m2 and vector v",
        "compute u = m1.v + m2.v^2 with componentwise v^2",
        "one vector u",
        related=["B0938"],
    ),
    _spec(
        "substitution-pattern local-template occurrence extractor",
        ["U006301", "U006302", "U006303"],
        "finite local-pattern-set observer",
        "a generated two-dimensional substitution pattern",
        "a supplied finite pattern region and 2 by 2 window shape",
        (
            "collect the distinct 2 by 2 blocks observed in the supplied "
            "pattern region"
        ),
        (
            "the finite observed-template set; the source states 51 blocks "
            "for the displayed Ammann pattern"
        ),
        related=["B0948"],
        limit=(
            "The source states that the displayed nested pattern contains 51 "
            "distinct 2 by 2 blocks but gives no finite window or completion "
            "bound guaranteed to recover every block of the infinite pattern."
        ),
        missing_mechanics=[
            "No retained-region size, completeness test, or stopping bound is "
            "given for proving that all eventual 2 by 2 blocks were observed."
        ],
        evidence_scopes={
            "U006301": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006302": [
                "carrier",
                "parameters_and_variants",
            ],
            "U006303": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
    ),
    _spec(
        "ternary square-free substitution preset",
        ["U006318"],
        "one-dimensional substitution-system preset",
        "strings over symbols 0, 1, and 2",
        "rules 0→012, 1→02, 2→1 with initial symbol 0",
        "replace every symbol in parallel by its rule image",
        (
            "one finite successor word at each step; the nested infinite "
            "square-free sequence is the limiting behavior"
        ),
        related=["B0959"],
    ),
    _spec(
        "pattern-avoidance sequence-count growth observer family",
        ["U006318", "U006319", "U006320", "U006321", "U006322"],
        "parameterized solution-count observer",
        "finite sequences avoiding a selected repeated-block pattern",
        "alphabet size k, length n, and forbidden block-variable pattern",
        "count length-n sequences that avoid the selected pattern",
        "a count sequence or its asymptotic growth characterization",
        related=["B0959", "B0960", "B0961"],
        limit=(
            "The source gives approximate growth for square- and cube-free "
            "cases and qualitative variation for more general patterns, not "
            "one closed formula for every pattern."
        ),
        missing_mechanics=[
            "No exact all-pattern counting law or uniform asymptotic/error "
            "contract is given for the parameterized avoidance family."
        ],
        discovery_unit="U006322",
        identity_unit="U006322",
        evidence_scopes={
            "U006318": [
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
            ],
            "U006319": [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
            "U006320": ["result_kind", "parameters_and_variants"],
            "U006321": ["result_kind", "parameters_and_variants"],
            "U006322": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
    ),
    _spec(
        "integer square-ratio Diophantine relation",
        ["U006326"],
        "Diophantine relation",
        "integer triples (a,x,y)",
        "integers a, x, and y",
        "accept exactly when x^2 = a y^2",
        "the integer solution set; nonzero solutions require square a as stated",
        related=["B0962", "B0968"],
        limit=(
            "The source's “no solution” wording omits the universal trivial "
            "solution x=y=0; the square-a characterization is retained only "
            "for nonzero/nontrivial solutions."
        ),
    ),
    _spec(
        "odd-binomial-coefficient parity relation",
        ["U006332"],
        "integer predicate/relation",
        "integer pairs (x,y)",
        "nonnegative integers x and y",
        "accept exactly when Mod[Binomial[x,y],2] equals 1",
        "the odd-binomial-coefficient solution set",
    ),
    _spec(
        "odd-factor product to non-power-of-two relation",
        ["U006332"],
        "integer predicate/relation",
        "integer triples (x,y,z)",
        "integers x, y, and z",
        "accept exactly when (2 x + 1) y = z",
        "solutions outside the stated power-of-two obstruction under the intended positive/nontrivial domain",
        limit=(
            "The source does not delimit positivity or zero conventions. The "
            "non-power-of-two characterization is therefore recorded only as "
            "a positive/nontrivial-domain statement, with the exact domain "
            "UNKNOWN_FROM_SOURCE."
        ),
        missing_mechanics=[
            "The positivity, zero, sign, and nontriviality domain conventions "
            "needed for the power-of-two characterization are unspecified."
        ],
    ),
    _spec(
        "stacked geometric-substitution evolution representation",
        ["U006190", "U006191"],
        "history embedding/representation function",
        "successive two-dimensional geometric-substitution point patterns",
        "an ordered geometric-substitution evolution history",
        "stack successive pattern states along a third display axis",
        "one three-dimensional space-time history object",
        limit=(
            "The source identifies a stacked three-dimensional visualization "
            "of successive states but gives no unique orientation, spacing, "
            "alignment, or rendering convention."
        ),
        missing_mechanics=[
            "Within-layer alignment, axis orientation, layer spacing, and "
            "rendering geometry are not specified."
        ],
        cardinality=(
            "one layered representation only after the omitted alignment, "
            "orientation, spacing, and rendering choices are supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic rendered "
            "three-dimensional visualization from the history alone"
        ),
    ),
    _spec(
        "stacked multiway-state evolution representation",
        ["U006256", "U006257"],
        "history embedding/representation function",
        "the full state collection at each multiway evolution step",
        "an ordered multiway evolution history",
        "stack every step's generated sequences in retained step order",
        "one layered history representation of all retained states",
        related=["B0921"],
        limit=(
            "The source identifies a stacked display of all sequences by "
            "evolution step but does not give a within-layer order, string "
            "alignment, spacing, duplicate-display, or rendering convention."
        ),
        missing_mechanics=[
            "Within-layer sequence order, string alignment, inter-item and "
            "inter-layer spacing, duplicate display, and rendering are omitted."
        ],
        cardinality=(
            "one layered display only after the omitted within-layer ordering, "
            "alignment, spacing, duplicate, and rendering choices are supplied"
        ),
        measure=(
            "the source does not select a unique or deterministic rendered "
            "stack from the time-indexed state collections alone"
        ),
    ),
    _spec(
        "Ceiling[t/2] multiway state-count function",
        ["U001134"],
        "exact trajectory count function",
        "the first simple multiway preset in the referenced figure",
        "step t",
        "evaluate Ceiling[t/2]",
        "the number of distinct sequences at step t",
        related=["B0803"],
    ),
    _spec(
        "linear-t multiway state-count function",
        ["U001134"],
        "exact trajectory count function",
        "the second simple multiway preset in the referenced figure",
        "step t",
        "evaluate t",
        "the number of distinct sequences at step t",
        related=["B0804"],
    ),
    _spec(
        "Fibonacci[t+1] simple-multiway state-count function",
        ["U001134"],
        "exact trajectory count function",
        "the third simple multiway preset in the referenced figure",
        "step t",
        "evaluate Fibonacci[t+1]",
        "the number of distinct sequences at step t",
        related=["B0801"],
    ),
    _spec(
        "rapid-growth multiway Fibonacci state-count function",
        ["U001147"],
        "exact trajectory count function",
        "the referenced rapid-growth multiway preset",
        "step t",
        "evaluate Fibonacci[t+1]",
        "the number of distinct states at step t",
        related=["B0692"],
    ),
    _spec(
        "rapid-growth multiway state first-appearance function",
        ["U001147"],
        "exact first-hit-time function",
        "states of the referenced rapid-growth multiway preset",
        "state with m white cells and n black cells",
        "evaluate 2 m + n - 1",
        "the step at which the state first appears",
        related=["B0692"],
    ),
    _spec(
        "polynomial-growth multiway state-count asymptotic profile",
        ["U006252"],
        "asymptotic trajectory growth-profile observer",
        "the displayed three-rule string multiway preset",
        "step t and number n of B symbols in the initial condition",
        "the displayed rule's state count grows at rate t^(n+1)",
        "the stated polynomial growth-rate profile",
        limit=(
            "The source states a growth rate, not exact equality of the state "
            "count with t^(n+1)."
        ),
    ),
    _spec(
        "two-dimensional local-template constraint census",
        ["U001183", "U001184", "U001185", "U001186", "U001187"],
        "finite-family census query",
        "all binary five-cell-template constraint codes",
        "the complete 2^32 constraint family",
        "partition constraints into unsatisfiable and satisfiable classes and count the sufficient repetitive witness set",
        "the four stated totals: all, unsatisfiable, satisfiable, and 171 sufficient repetitive patterns",
        related=["B0699", "B0702"],
        discovery_unit="U001185",
        identity_unit="U001184",
        evidence_scopes={
            "U001183": [
                "carrier",
                "parameters_and_variants",
            ],
            "U001184": [
                "object_kind",
                "carrier",
                "input",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U001185": [
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "parameters_and_variants",
            ],
            "U001186": ["result_kind"],
            "U001187": ["result_kind"],
        },
    ),
    _spec(
        "required-template constraint-family cardinality",
        ["U001212"],
        "finite-family cardinality query",
        "the page-216 two-dimensional required-template constraint family",
        "the fixed constraint-family definition",
        "return the stated complete family size 137438953472",
        "one exact finite cardinality",
        related=["B0703"],
    ),
]

for unit_id, name, expression, result_kind in SIERPINSKI_SPECS:
    RECOVERED_SPECS.append(
        _spec(
            name,
            [
                "U006150",
                *(["U006160"] if "coordinate" in name else []),
                unit_id,
            ],
            "uniterated finite-pattern generator",
            (
                "finite two-dimensional integer-coordinate set"
                if "coordinate" in name
                else "finite two-dimensional binary array"
            ),
            "nonnegative step index n",
            expression,
            result_kind,
            related=["B0898"],
            limit=(
                "The source states output equivalence up to orientation; it "
                "does not collapse the independently delimited native formula."
            ),
            evidence_scopes={
                "U006150": [
                    "input",
                    "result_kind",
                    "parameters_and_variants",
                    "evidence_limit",
                ],
                **(
                    {
                        "U006160": [
                            "carrier",
                            "law_kind",
                            "result_kind",
                            "parameters_and_variants",
                            "evidence_limit",
                        ]
                    }
                    if "coordinate" in name
                    else {}
                ),
                unit_id: [
                    "object_kind",
                    "carrier",
                    "input",
                    "law_kind",
                    "rule_relation_constraint_function_or_probability_law",
                    "result_kind",
                    "successor_cardinality",
                    "determinism_branching_or_measure",
                    "parameters_and_variants",
                    "evidence_limit",
                ],
            },
            discovery_unit=unit_id,
            identity_unit=unit_id,
        )
    )

RELINK_SPECS = [
    {
        "candidate_id": "B0032",
        "units": {
            "U000972": [
                "input",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            ],
            "U000977": [
                "result_kind",
                "excluded_observers_and_representations",
            ],
            "U000978": [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            ],
            "U006112": [
                "input",
                "rule_relation_constraint_function_or_probability_law",
                "result_kind",
                "parameters_and_variants",
            ],
            "U006113": [
                "result_kind",
                "excluded_observers_and_representations",
            ],
        },
        "claim": (
            "The Chapter 5 center-line and offset-slice examples specialize "
            "the existing dimension-agnostic cellular-automaton spatial-slice "
            "selector without defining a new selector law."
        ),
    },
    {
        "candidate_id": "B0094",
        "units": {
            "U006117": [
                "object_kind",
                "law_kind",
                "parameters_and_variants",
                "evidence_limit",
            ]
        },
        "claim": (
            "The source independently identifies rule 90 as the one-dimensional "
            "component result while leaving the neighboring 2D attribution "
            "conflicting."
        ),
    },
    {
        "candidate_id": "B0595",
        "units": {
            "U006182": [
                "object_kind",
                "input",
                "result_kind",
                "witness_semantics",
                "parameters_and_variants",
                "evidence_limit",
            ]
        },
        "claim": (
            "The GoldenRatio lattice cut is a specific digital-slope "
            "representation preset and supplies a Fibonacci-sequence witness."
        ),
    },
    {
        "candidate_id": "B0703",
        "units": {
            "U001212": [
                "parameters_and_variants",
                "evidence_limit",
            ]
        },
        "claim": (
            "The exact family cardinality bounds the required-template "
            "constraint family but does not alter its acceptance law."
        ),
    },
    {
        "candidate_id": "B0912",
        "units": {
            "U006199": [
                "result_kind",
                "excluded_observers_and_representations",
            ]
        },
        "claim": (
            "The inspected Julia-set array corroborates outputs of the "
            "inverse-square-root Julia generator without adding update mechanics."
        ),
    },
    {
        "candidate_id": "B0913",
        "units": {
            "U006201": [
                "result_kind",
                "witness_semantics",
                "excluded_observers_and_representations",
            ]
        },
        "claim": (
            "The inspected Mandelbrot magnification sequence corroborates the "
            "bounded-orbit relation and its parameter-space witness."
        ),
    },
    {
        "candidate_id": "B0916",
        "units": {
            "U006223": [
                "native_time",
                "schedule",
                "write_replacement_assembly_or_commit",
                "result_kind",
            ]
        },
        "claim": (
            "The prose immediately preceding NetEvolveList states that each "
            "successive network applies the rules and then removes every node "
            "not connected to node 1."
        ),
    },
    {
        "candidate_id": "B0919",
        "units": {
            "U006233": [
                "result_kind",
                "excluded_observers_and_representations",
            ]
        },
        "claim": (
            "The node-count plot corroborates the stated sequential-network "
            "preset's behavior without supplying its native rule."
        ),
    },
    {
        "candidate_id": "B0921",
        "units": {
            "U006242": [
                "native_time",
                "law_kind",
            ],
            "U006244": [
                "carrier",
                "alphabet_or_value_schema",
                "law_kind",
                "parameters_and_variants",
                "excluded_observers_and_representations",
            ],
            "U006245": [
                "rule_relation_constraint_function_or_probability_law",
                "write_replacement_assembly_or_commit",
                "result_kind",
                "parameters_and_variants",
            ],
            "U006246": [
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "excluded_observers_and_representations",
            ],
            "U006251": [
                "structural_invariants",
                "write_replacement_assembly_or_commit",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "witness_semantics",
                "evidence_limit",
            ],
        },
        "claim": (
            "The lead-in, list-based alternative, and general-properties note "
            "corroborate the existing string multiway system: step functions "
            "enumerate replacements, while Union merges equal states and "
            "therefore erases path multiplicity rather than defining a "
            "distinct multiway law."
        ),
    },
    {
        "candidate_id": "B0922",
        "units": {
            "U006255": [
                "result_kind",
                "witness_semantics",
                "parameters_and_variants",
                "evidence_limit",
            ],
            "U006258": [
                "result_kind",
                "witness_semantics",
                "evidence_limit",
            ],
            "U006259": [
                "result_kind",
                "witness_semantics",
                "excluded_observers_and_representations",
            ],
            "U006260": [
                "seed",
                "result_kind",
                "termination_completion_failure",
                "parameters_and_variants",
                "evidence_limit",
            ],
        },
        "claim": (
            "The count, bounded-reachability image, and alternate-seed outcomes "
            "supply result and parameter evidence for the existing page-206 "
            "multiway preset."
        ),
    },
]

PROPOSED_VOCABULARY = list(dict.fromkeys([
    "two-dimensional cellular automaton",
    "five-neighbor cellular automaton",
    "nine-neighbor cellular automaton",
    "arbitrary-offset cellular automaton",
    "two-dimensional CA code 1022",
    "two-dimensional CA code 942",
    "two-dimensional CA code 174826",
    "two-dimensional CA code 175850",
    "two-dimensional CA code 746",
    "outer-totalistic cellular automaton code 686",
    "three-dimensional cellular automaton",
    "six-face-neighbor 3D cellular automaton",
    "26-neighbor 3D cellular automaton",
    "homogeneous-geometry cellular automaton",
    "pentagonal-tiling cellular automaton",
    "Penrose-tiling cellular automaton",
    "cellular automaton on a homogeneous network",
    "two-dimensional Turing machine",
    "Langton's ant",
    "vant",
    "turmite",
    "turning machine",
    "turn-relative Turing machine",
    "two-dimensional mobile automaton",
    "two-dimensional block substitution system",
    "non-white-background substitution system",
    "d-dimensional array substitution system",
    "geometric substitution system",
    "Sierpiński block-substitution preset",
    "Penrose triangular substitution system",
    "dragon-curve substitution system",
    "Koch-curve substitution system",
    "affine iterated transformation system",
    "Möbius iterated transformation system",
    "inverse-square-root Julia-set generator",
    "Mandelbrot-set bounded-orbit relation",
    "two-dimensional neighbor-dependent substitution system",
    "square-spiral grid enumeration",
    "parallel directed network system",
    "sequential directed network system",
    "undirected network rewriting system",
    "binary-outdegree network restriction",
    "node-rerouting network rule",
    "node-inserting network rule",
    "distance-two network rule",
    "random Boolean network",
    "network dimensionality observer",
    "string multiway system",
    "multiway state-transition network",
    "sorted-count multiway system",
    "semigroup bidirectional rewrite system",
    "group inverse-symbol rewrite system",
    "regular generative grammar",
    "context-free generative grammar",
    "context-sensitive generative grammar",
    "unrestricted generative grammar",
    "multidimensional block multiway system",
    "numeric multiway system",
    "normal-play nim",
    "equational constraint system",
    "partial-differential-equation initial-value relation",
    "partial-differential-equation boundary-value relation",
    "linear vector relation",
    "quadratic vector relation",
    "variational extremum constraint",
    "one-dimensional allowed-block constraint",
    "de Bruijn allowed-block decision",
    "two-dimensional allowed-template constraint",
    "square-spiral backtracking constraint solver",
    "every-template-must-occur constraint",
    "cellular-automaton fixed-point constraint",
    "plane-tiling constraint",
    "aperiodic polyomino constraint",
    "spin-system ground-state constraint",
    "list-valued sequence equation",
    "square-free sequence constraint",
    "cube-free sequence constraint",
    "Diophantine integer relation",
    "Pell equation",
    "Pythagorean-triple relation",
    "finite multiplication-table constraint",
    "formula-search constraint",
    "box-counting fractal-dimension observer",
    "grid-occupancy moment observer",
    *[name for _, name, _, _ in SIERPINSKI_SPECS],
    *[spec["name"] for spec in RECOVERED_SPECS],
]))

QUERY_SPECS = [
    (
        "spatial cellular automata and dimensional rule families",
        (
            r"\b(?:cellular automat(?:on|a)|CAStep|NetCAStep|"
            r"5[- ](?:cell|neighbou?r)|9[- ](?:cell|neighbou?r)|"
            r"outer totalistic|growth totalistic|totalistic rules?|"
            r"rule codes?|code numbers?|Ulam systems?|Game of Life)\b"
        ),
        "REGEX",
    ),
    (
        "two-dimensional Turing and mobile automata",
        (
            r"\b(?:Turing machines?|TM2DStep|Langton(?:'s)? ant|vants?|"
            r"turmites?|turning machines?|mobile automata|mobile turtles?|"
            r"heads?)\b"
        ),
        "REGEX",
    ),
    (
        "substitution, geometric replacement, and fractal constructions",
        (
            r"\b(?:substitution systems?|subdivid(?:e|es|ed|ing)|"
            r"replac(?:e|es|ed|ing|ement|ements)|geometrical rules?|"
            r"geometric substitution|fractal(?:s| geometry| dimensions?)?|"
            r"Sierpi[nń]ski|Penrose|dragon curve|Koch curve|"
            r"affine transformations?|M[oö]bius transformations?|"
            r"Julia sets?|Mandelbrot set|Flatten2D|SSEvolve|SS2DEvolve)\b"
        ),
        "REGEX",
    ),
    (
        "parallel, sequential, and random network systems",
        (
            r"\b(?:network systems?|CyclicNet|Follow\[|NeighborNumbers|"
            r"NetEvolve|ConnectedNodes|RenumberNodes|NetCAStep|nodes?|"
            r"connections?|rerout(?:e|ed|ing)|outgoing connections?|"
            r"sequential networks?|Boolean networks?|garbage collection)\b"
        ),
        "REGEX",
    ),
    (
        "multiway, rewriting, grammar, group, and game systems",
        (
            r"\b(?:multiway systems?|MWStep|MWEvolveList|rewrite systems?|"
            r"semi[- ]Thue systems?|production systems?|associative calculi|"
            r"semigroups?|monoids?|groups?|Cayley graphs?|"
            r"generative grammars?|regular grammars?|"
            r"context[- ]free grammars?|context[- ]sensitive grammars?|"
            r"unrestricted grammars?|nondeterministic systems?|"
            r"game systems?|nim)\b"
        ),
        "REGEX",
    ),
    (
        "local constraints, templates, and witness solvers",
        (
            r"\b(?:constraints?|allowed (?:blocks?|templates?|patterns?)|"
            r"local templates?|satisf(?:y|ies|ied|ying)|witness(?:es)?|"
            r"backtracking|enumerat(?:e|es|ed|ing|ion)|square spiral|"
            r"de Bruijn|subshifts? of finite type|fixed[- ]point|"
            r"undecidab(?:le|ility)|NP[- ]complete|SatisfiedQ|"
            r"repetitive patterns?)\b"
        ),
        "REGEX",
    ),
    (
        "PDE, vector-relation, and variational constraints",
        (
            r"\b(?:partial differential equations?|initial[- ]value|"
            r"boundary[- ]value|Laplace equation|wave equation|"
            r"diffusion equation|linear equations?|nonlinear equations?|"
            r"LinearSolve|variational principles?|minimiz(?:e|es|ed|ing)|"
            r"maximiz(?:e|es|ed|ing)|finite difference|finite element)\b|"
            r"u\s*==\s*m"
        ),
        "REGEX",
    ),
    (
        "tiling, spin, and sequence-pattern constraints",
        (
            r"\b(?:tilings?|polyominoes?|spin systems?|Ising model|"
            r"spin glass|ground states?|sequence equations?|"
            r"pattern[- ]avoiding sequences?|identical blocks?|"
            r"square[- ]free|cube[- ]free|formal languages?|"
            r"multiplication tables?|Ammann|Robinson|Cook aperiodic)\b"
        ),
        "REGEX",
    ),
    (
        "Diophantine and formula-search constraints",
        (
            r"\b(?:Diophantine equations?|Pell equation|"
            r"Pythagorean triples?|Fermat(?:'s)? Last Theorem|"
            r"integer relations?|ExtendedGCD|algebraic equations?|"
            r"constraints? on formulas|LeafCount|quadratic equations?)\b|"
            r"x\^\d|y\^\d|z\^\d"
        ),
        "REGEX",
    ),
    (
        "general construction, formula, code, and image anchors",
        (
            r"\b(?:rules?|systems?|algorithms?|generators?|solvers?|"
            r"relations?|functions?|transformations?|maps?|constraints?|"
            r"equations?|games?|initial conditions?|evolution|positions?|"
            r"patterns?|counts?|cardinalit(?:y|ies)|growth rates?|"
            r"first appears?|number of)\b|"
            r"(?:^|\n)\s*(?:!\[[^\]]*\]\([^)]+\)|```)|"
            r"`[^`\n]*(?:->|→|==|:=|:>|Nest|NestList|Map|Table|Replace|"
            r"Rule|Step|Evolve)[^`\n]*`|"
            r"`[^`\n]*\[[^`\n]*\][^`\n]*`"
        ),
        "REGEX",
    ),
    (
        "native state, step, update, and completion mechanics",
        (
            r"\b(?:states?|steps?|updates?|evol(?:ve|ves|ved|ving|ution)|"
            r"initial conditions?|seeds?|successors?|"
            r"replace(?:s|d|ment|ments)?|appl(?:y|ies|ied|ying)|parallel|"
            r"sequential|active nodes?|halts?|terminat(?:e|es|ed|ion)|"
            r"dies out|fixed points?)\b"
        ),
        "REGEX",
    ),
    (
        "carrier, topology, dimension, and neighborhood mechanics",
        (
            r"\b(?:one[- ]dimensional|two[- ]dimensional|"
            r"three[- ]dimensional|higher[- ]dimensional|d[- ]dimensional|"
            r"grids?|lattices?|arrays?|planes?|networks?|graphs?|"
            r"topolog(?:y|ical)|geometr(?:y|ical)|neighbou?rhoods?|"
            r"neighbou?rs?|offsets?|boundar(?:y|ies)|wrap around|"
            r"orientations?|connections?)\b"
        ),
        "REGEX",
    ),
    (
        "branching, merging, determinism, and witness semantics",
        (
            r"\b(?:branch(?:es|ed|ing)|multiway|possible states?|"
            r"all possible|nondeterministic|deterministic|"
            r"merg(?:e|es|ed|ing)|Union|distinct states?|solutions?|"
            r"witness(?:es)?|unique|exist(?:s|ence)|no patterns?|kept|"
            r"dropped)\b"
        ),
        "REGEX",
    ),
    (
        "representation, observer, implementation, and application boundary",
        (
            r"\b(?:pictures?|plots?|plott(?:ed|ing)|displays?|"
            r"visualiz(?:e|es|ed|ing|ation)|"
            r"represent(?:s|ed|ing|ation)?|"
            r"implement(?:s|ed|ing|ation)?|"
            r"simulat(?:e|es|ed|ing|ion)|render(?:s|ed|ing)?|"
            r"projections?|slices?|stack(?:s|ed|ing)|paths?|"
            r"measure(?:s|d|ment)|Mathematica|applications?|history)\b"
        ),
        "REGEX",
    ),
    (
        "typed cross-reference and locator obligations",
        (
            r"\b(?:pages?|page|chapter)\s+(?:\d+|[IVX]+)(?:[–-]\d+)?\b|"
            r"\b(?:the\s+)?(?:"
            r"(?:top|bottom)\s+of\s+(?:the\s+)?)?"
            r"(?:facing|previous|next)(?:\s+(?:one|two|three))?\s+pages?\b"
        ),
        "REGEX",
    ),
]

EXPECTED_STAGE_UNIT_COUNT = 539
EXPECTED_STAGE_ASSET_COUNT = 150
EXPECTED_INITIAL_STAGE_CANDIDATE_COUNT = 324
EXPECTED_RELINKED_EXISTING_STAGE_CANDIDATE_COUNT = 3
EXPECTED_ENRICHED_STAGE_CANDIDATE_COUNT = 415
EXPECTED_INITIAL_STAGE_ROUTE_COUNT = 62
EXPECTED_ENRICHED_STAGE_ROUTE_COUNT = 214
EXPECTED_NEW_ROUTE_COUNT = 151
EXPECTED_READING_UPDATE_COUNT = 154
EXPECTED_NEW_CANDIDATE_COUNT = 88
EXPECTED_NEW_EVIDENCE_COUNT = 202
EXPECTED_RESULT_PAIR_COUNT = 1553
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 524
EXPECTED_PATH_PAIR_COUNTS = {
    STAGE_PATHS[0]: 752,
    STAGE_PATHS[1]: 801,
}
EXPECTED_PATH_UNIQUE_UNIT_COUNTS = {
    STAGE_PATHS[0]: 264,
    STAGE_PATHS[1]: 260,
}
EXPECTED_HIT_COUNTS = [
    66,
    17,
    69,
    74,
    37,
    78,
    5,
    14,
    9,
    479,
    160,
    202,
    65,
    134,
    144,
]
EXPECTED_QUERY_SPEC_DIGEST = (
    "3e545dfd7b930c184489a98eccde200695cf582e38275233896ae80a1376984d"
)
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "14af3dc4c5d59f050f1dd1c05fd691d7307f6d58a78ce592b0de40e1eb5e952f"
)
EXPECTED_ROUTE_SPEC_DIGEST = (
    "bd46f6219ec51c9f9077448cfee5ff2a263882cca3d63fbe4cdd8c4116938ea0"
)
EXPECTED_ROUTE_AUDIT_DIGEST = (
    "ea4c7b2e9af1a762c6448f3314d196baaa9e515ce6904f65a7bce7234f207682"
)
EXPECTED_TRIAGE_DIGEST = (
    "1d2d0c50a27a20dd283952077f73d6fc71057ffdfa3b062a9a082ceefb33c06f"
)
EXPECTED_ACTIVE_SEMANTIC_DIGESTS = {
    "S013": (
        "d80973df9e95c8fac4b32183fac377c039eb1dab3ab69af86f9f35b5151bac90"
    ),
    "S014": "",
}
EXPECTED_CANDIDATE_COVERAGE_DIGEST = ""
EXPECTED_ROUTE_COVERAGE_DIGEST = ""
EXPECTED_OMISSION_CHALLENGE_COUNT = 0
EXPECTED_OMISSION_CHALLENGE_DIGEST = ""
EXPECTED_NEW_VOCABULARY_DIGEST = (
    "f2bb0778817ace90ee9f3e4b0d9c3a9a246f704ef77859368a2888bdfb9a115a"
)
EXPECTED_DISPOSITION_COUNTS: dict[str, int] = {}
EXPECTED_ROUND_DIGESTS: dict[str, str] = {}

DIRECT_STRENGTHS = {
    "DIRECT_IDENTITY",
    "DIRECT_PARTIAL_MECHANICS",
    "DIRECT_COMPLETE_MECHANICS",
    "DEFECT_LIMITED",
}


class AuthoringError(ValueError):
    """The current state cannot safely receive this proposal."""


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_links(value: str, label: str) -> list[str]:
    try:
        links = json.loads(value)
    except json.JSONDecodeError as exc:
        raise AuthoringError(f"{label} is not JSON") from exc
    if (
        not isinstance(links, list)
        or not all(isinstance(item, str) for item in links)
        or len(links) != len(set(links))
    ):
        raise AuthoringError(f"{label} is not a unique string array")
    return links


def atomic_create(path: Path, payload: bytes) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("short write while creating proposal")
            view = view[written:]
        os.fsync(descriptor)
    except BaseException:
        os.close(descriptor)
        try:
            path.unlink()
        except OSError:
            pass
        raise
    else:
        os.close(descriptor)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def _json_array(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def _append_links(value: str, additions: list[str], label: str) -> str:
    prior = parse_links(value, label)
    if set(prior) & set(additions) or len(additions) != len(set(additions)):
        raise AuthoringError(f"{label} additions overlap or repeat")
    return _json_array([*prior, *additions])


def _query_id(query_start: int, ordinal: int) -> str:
    return f"Q{query_start + ordinal - 1:04d}"


def _hit_for(
    hit_by_pair: dict[tuple[int, str], str],
    ordinal: int,
    unit_id: str,
) -> str:
    try:
        return hit_by_pair[(ordinal, unit_id)]
    except KeyError as exc:
        raise AuthoringError(
            f"frozen query F{ordinal:02d} does not hit {unit_id}"
        ) from exc


def _unknown_fingerprint(
    name: str,
) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    reason = f"The assigned source does not establish this field for {name}."
    return (
        {field: "UNKNOWN_FROM_SOURCE" for field in FINGERPRINT_FIELDS},
        {
            field: {
                "status": "UNKNOWN_FROM_SOURCE",
                "value": None,
                "evidence_ids": [],
                "reason": reason,
            }
            for field in FINGERPRINT_FIELDS
        },
    )


def _new_candidate(
    *,
    candidate_id: str,
    name: str,
    aliases: list[str],
    discovery_hit_id: str,
    discovery_ordinal: int,
    source_unit_ids: list[str],
    evidence: list[dict[str, Any]],
    supported_values: dict[str, Any],
    not_applicable_fields: set[str],
    parameters: list[dict[str, Any]],
    uncertainties: list[str],
    exact_missing_mechanics: list[str],
    related_candidate_ids: list[dict[str, Any]],
    source_status: list[str],
    image_witnesses: list[str],
) -> dict[str, Any]:
    field_support, fingerprint = _unknown_fingerprint(name)
    all_evidence_ids = [item["evidence_id"] for item in evidence]
    for field, value in supported_values.items():
        field_ids = [
            item["evidence_id"]
            for item in evidence
            if field in item["fingerprint_fields"]
        ]
        if not field_ids:
            raise AuthoringError(
                f"{candidate_id}.{field} has no supporting evidence"
            )
        field_support[field] = "SUPPORTED"
        fingerprint[field] = {
            "status": "SUPPORTED",
            "value": value,
            "evidence_ids": field_ids,
            "reason": "",
        }
    for field in sorted(not_applicable_fields):
        if field in supported_values:
            raise AuthoringError(
                f"{candidate_id}.{field} is both supported and not applicable"
            )
        field_support[field] = "NOT_APPLICABLE"
        fingerprint[field] = {
            "status": "NOT_APPLICABLE",
            "value": None,
            "evidence_ids": all_evidence_ids[:1],
            "reason": f"{field} is not native to {name} as delimited.",
        }
    missing = sorted(
        field
        for field, status in field_support.items()
        if status == "UNKNOWN_FROM_SOURCE"
    )
    missing_reason = (
        "The assigned source leaves these remaining fingerprint fields "
        f"UNKNOWN_FROM_SOURCE for {name}: {', '.join(missing)}"
        if missing
        else ""
    )
    for field in missing:
        fingerprint[field]["reason"] = missing_reason
    record: dict[str, Any] = {
        "id": candidate_id,
        "record_status": "ACTIVE",
        "provisional_name": name,
        "aliases": aliases,
        "discovery_stage": 9,
        "discovery_anchor": {
            "epoch": 2,
            "kind": "SEARCH_HIT",
            "id": discovery_hit_id,
            "ordinal": discovery_ordinal,
        },
        "source_unit_ids": source_unit_ids,
        "source_evidence": evidence,
        "source_status": source_status,
        "image_witnesses": image_witnesses,
        "evidence_strength": list(
            dict.fromkeys(item["strength"] for item in evidence)
        ),
        "field_support": field_support,
        "fingerprint": fingerprint,
        "parameters": parameters,
        "variants": [],
        "missing_mechanics": [
            *exact_missing_mechanics,
            *([missing_reason] if missing_reason else []),
        ],
        "uncertainties": uncertainties,
        "related_candidate_ids": related_candidate_ids,
        "cross_reference_ids": [],
        "evidence_reassignments": [],
    }
    return {field: record[field] for field in CANDIDATE_FIELDS}


def _evidence(
    *,
    evidence_number: int,
    hit_id: str,
    hit_ordinal: int,
    unit_id: str,
    strength: str,
    modality: str,
    claim: str,
    fields: list[str],
    image_path: str | None = None,
) -> dict[str, Any]:
    return {
        "evidence_id": f"E{evidence_number:06d}",
        "evidence_group_id": f"G{evidence_number:06d}",
        "discovery_anchor": {
            "epoch": 2,
            "kind": "SEARCH_HIT",
            "id": hit_id,
            "ordinal": hit_ordinal,
        },
        "source_unit_id": unit_id,
        "image_path": image_path,
        "strength": strength,
        "modality": modality,
        "claim": claim,
        "fingerprint_fields": fields,
    }


def _build_enrichment(
    *,
    reading_by_id: dict[str, dict[str, str]],
    hit_by_pair: dict[tuple[int, str], str],
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    reading_additions: dict[str, list[str]] = {
        "U006102": ["B0981"],
        "U006117": ["B0981"],
        "U006193": ["B0982"],
        "U006195": ["B0982"],
        "U006196": ["B0983"],
        "U006234": ["B0984"],
        "U006150": [f"B{number:04d}" for number in range(985, 999)],
        "U006160": [f"B{number:04d}" for number in range(994, 999)],
    }
    for offset, (unit_id, _, _, _) in enumerate(SIERPINSKI_SPECS):
        reading_additions[unit_id] = [f"B{985 + offset:04d}"]
    if len(reading_additions) != EXPECTED_READING_UPDATE_COUNT:
        raise AuthoringError("Stage 9 enrichment reading-unit set drifted")

    updated: list[dict[str, str]] = []
    for unit_id in sorted(reading_additions):
        old = reading_by_id[unit_id]
        row = dict(old)
        additions = reading_additions[unit_id]
        row["candidate_ids"] = _append_links(
            old["candidate_ids"],
            additions,
            f"{unit_id}.candidate_ids",
        )
        if unit_id == "U006117":
            row["evidence_statement"] = (
                "The unit independently identifies outer-totalistic 2D CA "
                "code 686, but its attribution to undefined “s alone” remains "
                "CONFLICTING and is not resolved by the search."
            )
        elif unit_id in {"U006150", "U006160"}:
            row["review_disposition"] = "SUPPORTS_CANDIDATE"
            row["evidence_statement"] = (
                "This header explicitly scopes the following formulas as "
                "alternate generators or coordinate enumerators for the "
                "page-187 Sierpiński step."
            )
        elif unit_id == "U006102":
            row["evidence_statement"] = (
                "Defines the two-color 2D outer-totalistic rule family used "
                "to interpret the independently stated code-686 identity."
            )
        elif unit_id == "U006193":
            row["evidence_statement"] = (
                "In addition to its linked complex maps, this unit explicitly "
                "defines the box-counting fractal-dimension observer."
            )
        elif unit_id == "U006195":
            row["review_disposition"] = "SUPPORTS_CANDIDATE"
            row["evidence_statement"] = (
                "Supplies the small-scale limit and possible "
                "nonconvergence boundary of the box-counting observer."
            )
        elif unit_id == "U006196":
            row["review_disposition"] = "CANDIDATE"
            row["evidence_statement"] = (
                "Introduces a distinct grid-occupancy distribution-moment "
                "observer as a generalization of fractal dimension."
            )
        elif unit_id == "U006234":
            row["review_disposition"] = "CANDIDATE"
            row["evidence_statement"] = (
                "Introduces a network-dimensionality observer by comparing "
                "the nodes reachable within radius r with r^d."
            )
        else:
            row["review_disposition"] = "CANDIDATE"
            row["evidence_statement"] = (
                "The explicit finite formula is itself an alternate "
                "Sierpiński step generator or black-square coordinate "
                "enumerator, not merely a rendering."
            )
        updated.append(row)

    evidence_number = 4049
    candidates: list[dict[str, Any]] = []

    outer_fields = [
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
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    outer_evidence = [
        _evidence(
            evidence_number=evidence_number,
            hit_id=_hit_for(hit_by_pair, 1, "U006102"),
            unit_id="U006102",
            strength="DIRECT_PARTIAL_MECHANICS",
            modality="PROSE",
            claim=(
                "The Notes define outer-totalistic 2D rules as depending on "
                "the center color and neighbor-count total."
            ),
            fields=outer_fields,
        ),
        _evidence(
            evidence_number=evidence_number + 1,
            hit_id=_hit_for(hit_by_pair, 1, "U006117"),
            unit_id="U006117",
            strength="DEFECT_LIMITED",
            modality="PROSE",
            claim=(
                "The prose explicitly identifies outer-totalistic code 686 "
                "in 2D, while the phrase “s alone” conflicts with the defined "
                "p/q/r components."
            ),
            fields=[
                "object_kind",
                "carrier",
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
                "evidence_limit",
            ],
        ),
    ]
    evidence_number += 2
    candidates.append(
        _new_candidate(
            candidate_id="B0981",
            name="outer-totalistic cellular automaton code 686",
            aliases=["2D outer-totalistic code 686"],
            discovery_hit_id=_hit_for(hit_by_pair, 1, "U006117"),
            source_unit_ids=["U006102", "U006117"],
            evidence=outer_evidence,
            supported_values={
                "object_kind": "cellular automaton",
                "native_time": "discrete successive steps",
                "carrier": "two-dimensional cell array",
                "alphabet_or_value_schema": "two cell colors",
                "complete_state": "all cell colors at one step",
                "frontier_or_activation": (
                    "all cells are eligible for synchronous update"
                ),
                "schedule": "synchronous parallel update",
                "read_dependencies_or_neighborhood": (
                    "center color plus total black-neighbor count"
                ),
                "law_kind": "outer-totalistic cellular-automaton rule",
                "rule_relation_constraint_function_or_probability_law": (
                    "two-dimensional outer-totalistic rule numbered 686"
                ),
                "write_replacement_assembly_or_commit": (
                    "replace each cell color with the rule result"
                ),
                "result_kind": "one successor cell array",
                "successor_cardinality": "one",
                "determinism_branching_or_measure": "deterministic",
                "parameters_and_variants": "outer-totalistic code 686",
                "excluded_observers_and_representations": (
                    "the nearby ablation image is evidence about attribution, "
                    "not the native evolution"
                ),
                "evidence_limit": (
                    "the source does not identify which defined p/q/r "
                    "ablation the corrupt phrase “s alone” denotes"
                ),
            },
            not_applicable_fields={
                "visible_history",
                "control_state",
                "input",
                "external_data",
                "termination_completion_failure",
                "witness_semantics",
            },
            parameters=[
                {
                    "name": "outer-totalistic code",
                    "source_description": "686",
                    "evidence_ids": ["E004050"],
                }
            ],
            uncertainties=[
                "The phrase “s alone” is undefined: the implementation and "
                "image define only p, q, r, p[q[]], and p[q[r[]]]."
            ],
            related_candidate_ids=[
                {
                    "candidate_id": "B0868",
                    "relation": "POSSIBLE_VARIANT_OF",
                    "proof_kind": "PROVISIONAL_COMPARISON",
                    "before_rationale": "",
                    "after_rationale": "",
                    "evidence_ids": ["E004050"],
                    "uncertainty": (
                        "The source locates code 686 among component "
                        "ablations but does not soundly identify the component."
                    ),
                }
            ],
            source_status=["CLEAR", "CONFLICTING"],
        )
    )

    observer_na = {
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
    }
    box_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "input",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "determinism_branching_or_measure",
        "witness_semantics",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    box_evidence = [
        _evidence(
            evidence_number=evidence_number,
            hit_id=_hit_for(hit_by_pair, 3, "U006193"),
            unit_id="U006193",
            strength="DIRECT_COMPLETE_MECHANICS",
            modality="PROSE",
            claim=(
                "The unit defines d from the small-grid scaling of the number "
                "of squares containing gray as (1/a)^d."
            ),
            fields=box_fields,
        ),
        _evidence(
            evidence_number=evidence_number + 1,
            hit_id=_hit_for(hit_by_pair, 14, "U006195"),
            unit_id="U006195",
            strength="DIRECT_PARTIAL_MECHANICS",
            modality="PROSE",
            claim=(
                "The continuation states the small-a limit and records that "
                "effective d may fluctuate or fail to converge."
            ),
            fields=["witness_semantics", "parameters_and_variants", "evidence_limit"],
        ),
    ]
    evidence_number += 2
    candidates.append(
        _new_candidate(
            candidate_id="B0982",
            name="box-counting fractal-dimension observer",
            aliases=["grid-square fractal-dimension measurement"],
            discovery_hit_id=_hit_for(hit_by_pair, 3, "U006193"),
            source_unit_ids=["U006193", "U006195"],
            evidence=box_evidence,
            supported_values={
                "object_kind": "observer/analyzer",
                "native_time": "uniterated measurement over grid scales",
                "carrier": "a geometric pattern under successively finer grids",
                "input": "pattern and grid edge length a",
                "law_kind": "scaling-exponent measurement",
                "rule_relation_constraint_function_or_probability_law": (
                    "infer d from N(a) varying as (1/a)^d for small a"
                ),
                "result_kind": "scalar fractal-dimension value or scale profile",
                "determinism_branching_or_measure": "deterministic measurement",
                "witness_semantics": (
                    "effective d can fluctuate with scale and need not converge"
                ),
                "parameters_and_variants": "grid scale a and limiting convention",
                "excluded_observers_and_representations": (
                    "the five pictured patterns are examples, not the observer law"
                ),
                "evidence_limit": (
                    "the source gives the scaling definition but no single "
                    "formal convention for every nonconvergent case"
                ),
            },
            not_applicable_fields=observer_na,
            parameters=[
                {
                    "name": "grid edge length",
                    "source_description": "a, taken toward small scales",
                    "evidence_ids": ["E004051", "E004052"],
                }
            ],
            uncertainties=[
                "For scale-dependent patterns the effective exponent may not "
                "converge to one definite value."
            ],
            related_candidate_ids=[],
            source_status=["CLEAR"],
        )
    )

    moment_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "input",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "determinism_branching_or_measure",
        "witness_semantics",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    moment_evidence = [
        _evidence(
            evidence_number=evidence_number,
            hit_id=_hit_for(hit_by_pair, 3, "U006196"),
            unit_id="U006196",
            strength="DIRECT_PARTIAL_MECHANICS",
            modality="PROSE",
            claim=(
                "The source introduces mean, variance, and higher moments of "
                "the grid-square gray-amount distribution as generalized "
                "fractal-dimension characterizers."
            ),
            fields=moment_fields,
        )
    ]
    evidence_number += 1
    candidates.append(
        _new_candidate(
            candidate_id="B0983",
            name="grid-occupancy moment observer",
            aliases=["generalized fractal-dimension moment analyzer"],
            discovery_hit_id=_hit_for(hit_by_pair, 3, "U006196"),
            source_unit_ids=["U006196"],
            evidence=moment_evidence,
            supported_values={
                "object_kind": "observer/analyzer",
                "native_time": "uniterated measurement over a selected grid",
                "carrier": "grid-square occupancy distribution of a pattern",
                "input": "gray amount in each grid square",
                "law_kind": "distribution-moment measurement",
                "rule_relation_constraint_function_or_probability_law": (
                    "compute mean, variance, and other moments of the "
                    "grid-square gray-amount distribution"
                ),
                "result_kind": "one or more generalized dimension descriptors",
                "determinism_branching_or_measure": "deterministic measurement",
                "witness_semantics": (
                    "distinguishes patterns that share one fractal dimension"
                ),
                "parameters_and_variants": "choice of distribution moments",
                "excluded_observers_and_representations": (
                    "the input pattern and its rendering are not this analyzer"
                ),
                "evidence_limit": (
                    "the source names the moment family without fixing one "
                    "normalization or finite set of moments"
                ),
            },
            not_applicable_fields=observer_na,
            parameters=[
                {
                    "name": "moment order",
                    "source_description": "mean, variance, and other moments",
                    "evidence_ids": ["E004053"],
                }
            ],
            uncertainties=[
                "The note leaves normalization and the selected moment orders "
                "as a family of choices."
            ],
            related_candidate_ids=[
                {
                    "candidate_id": "B0982",
                    "relation": "SOURCE_COMPARE",
                    "proof_kind": "PROVISIONAL_COMPARISON",
                    "before_rationale": "",
                    "after_rationale": "",
                    "evidence_ids": ["E004053"],
                    "uncertainty": (
                        "The source calls these quantities generalizations of "
                        "fractal dimension but does not collapse the observers."
                    ),
                }
            ],
            source_status=["CLEAR"],
        )
    )

    network_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "input",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "determinism_branching_or_measure",
        "witness_semantics",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    network_evidence = [
        _evidence(
            evidence_number=evidence_number,
            hit_id=_hit_for(hit_by_pair, 4, "U006234"),
            unit_id="U006234",
            strength="DIRECT_COMPLETE_MECHANICS",
            modality="PROSE",
            claim=(
                "The source defines dimensional form by the approximately "
                "r^d growth of distinct nodes reachable within r connections."
            ),
            fields=network_fields,
        )
    ]
    evidence_number += 1
    candidates.append(
        _new_candidate(
            candidate_id="B0984",
            name="network dimensionality observer",
            aliases=["reachable-node growth-dimension analyzer"],
            discovery_hit_id=_hit_for(hit_by_pair, 4, "U006234"),
            source_unit_ids=["U006234"],
            evidence=network_evidence,
            supported_values={
                "object_kind": "observer/analyzer",
                "native_time": "uniterated measurement at a selected network state",
                "carrier": "network graph",
                "input": "network, reference node, and connection radius r",
                "law_kind": "graph-volume scaling measurement",
                "rule_relation_constraint_function_or_probability_law": (
                    "count distinct nodes reachable within r successive "
                    "connections and compare the count with r^d"
                ),
                "result_kind": "dimension estimate or reachable-node growth curve",
                "determinism_branching_or_measure": "deterministic measurement",
                "witness_semantics": (
                    "d-dimensional form corresponds to reachable volume near r^d"
                ),
                "parameters_and_variants": "reference node, radius r, and network step",
                "excluded_observers_and_representations": (
                    "the plotted curves are outputs of the observer"
                ),
                "evidence_limit": (
                    "the source gives an approximate scaling criterion rather "
                    "than a finite-size estimator or tolerance"
                ),
            },
            not_applicable_fields=observer_na,
            parameters=[
                {
                    "name": "connection radius",
                    "source_description": "r successive connections",
                    "evidence_ids": ["E004054"],
                }
            ],
            uncertainties=[
                "No finite-size fit, tolerance, or reference-node convention "
                "is fixed by the source."
            ],
            related_candidate_ids=[],
            source_status=["CLEAR"],
        )
    )

    function_na = {
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "write_replacement_assembly_or_commit",
    }
    function_fields = [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "complete_state",
        "input",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "termination_completion_failure",
        "witness_semantics",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    ]
    for offset, (unit_id, name, expression, result_kind) in enumerate(
        SIERPINSKI_SPECS
    ):
        candidate_id = f"B{985 + offset:04d}"
        evidence_id = f"E{evidence_number:06d}"
        item = _evidence(
            evidence_number=evidence_number,
            hit_id=_hit_for(hit_by_pair, 10, unit_id),
            unit_id=unit_id,
            strength="DIRECT_COMPLETE_MECHANICS",
            modality="CODE",
            claim=(
                f"The source explicitly gives {expression} as an alternate "
                f"way to generate the page-187 Sierpiński step or its black "
                f"square positions."
            ),
            fields=function_fields,
        )
        evidence_number += 1
        candidates.append(
            _new_candidate(
                candidate_id=candidate_id,
                name=name,
                aliases=[],
                discovery_hit_id=_hit_for(hit_by_pair, 10, unit_id),
                source_unit_ids=[unit_id],
                evidence=[item],
                supported_values={
                    "object_kind": "uniterated generator function",
                    "native_time": (
                        "no native step transition; evaluate directly for n"
                    ),
                    "carrier": (
                        "two-dimensional binary array"
                        if "array" in result_kind
                        else "two-dimensional integer-coordinate set"
                    ),
                    "support": "finite step-n Sierpiński pattern",
                    "alphabet_or_value_schema": (
                        "binary array values"
                        if "array" in result_kind
                        else "integer coordinate pairs"
                    ),
                    "complete_state": result_kind,
                    "input": "nonnegative step index n",
                    "law_kind": "deterministic finite generator function",
                    "rule_relation_constraint_function_or_probability_law": (
                        expression
                    ),
                    "result_kind": result_kind,
                    "successor_cardinality": "one result per input n",
                    "determinism_branching_or_measure": "deterministic",
                    "termination_completion_failure": (
                        "finite construction for each finite n"
                    ),
                    "witness_semantics": (
                        "the source states this generates the page-187 "
                        "Sierpiński pattern, possibly in another orientation"
                    ),
                    "parameters_and_variants": "step index n",
                    "excluded_observers_and_representations": (
                        "rendering the returned array or coordinates is not "
                        "part of the generator law"
                    ),
                    "evidence_limit": (
                        "the assigned unit supplies the finite formula but "
                        "does not prove equivalence beyond the source statement"
                    ),
                },
                not_applicable_fields=function_na,
                parameters=[
                    {
                        "name": "step index",
                        "source_description": "finite nonnegative n",
                        "evidence_ids": [evidence_id],
                    }
                ],
                uncertainties=[
                    "The source allows orientation differences among the "
                    "alternate generators."
                ],
                related_candidate_ids=[
                    {
                        "candidate_id": "B0898",
                        "relation": "SOURCE_COMPARE",
                        "proof_kind": "PROVISIONAL_COMPARISON",
                        "before_rationale": "",
                        "after_rationale": "",
                        "evidence_ids": [evidence_id],
                        "uncertainty": (
                            "The source states output equivalence to the "
                            "page-187 pattern but the native function remains "
                            "independently delimited."
                        ),
                    }
                ],
                source_status=["CLEAR"],
            )
        )

    if evidence_number != 4069:
        raise AuthoringError(
            f"Stage 9 search evidence allocation drifted: {evidence_number}"
        )
    if [candidate["id"] for candidate in candidates] != [
        f"B{number:04d}" for number in range(981, 999)
    ]:
        raise AuthoringError("Stage 9 search candidate allocation drifted")
    return updated, candidates


DIRECT_FUNCTION_NA = {
    "native_time",
    "visible_history",
    "control_state",
    "seed",
    "external_data",
    "frontier_or_activation",
    "schedule",
    "read_dependencies_or_neighborhood",
    "write_replacement_assembly_or_commit",
    "witness_semantics",
}

RELATION_NA = {
    "native_time",
    "control_state",
    "seed",
    "external_data",
    "frontier_or_activation",
    "schedule",
    "read_dependencies_or_neighborhood",
    "write_replacement_assembly_or_commit",
    "successor_cardinality",
    "termination_completion_failure",
}

DENOTATION_NA = {
    "native_time",
    "visible_history",
    "control_state",
    "seed",
    "external_data",
    "frontier_or_activation",
    "schedule",
    "read_dependencies_or_neighborhood",
    "write_replacement_assembly_or_commit",
    "termination_completion_failure",
    "witness_semantics",
}

ITERATED_NA = {
    "visible_history",
    "control_state",
    "external_data",
    "witness_semantics",
}


def _typed_semantics(
    spec: dict[str, Any],
) -> tuple[dict[str, Any], set[str]]:
    """Return candidate-specific values and obvious N/A fields."""

    profile = spec["profile"]
    values: dict[str, Any] = {
        "object_kind": spec["object_kind"],
        "carrier": spec["carrier"],
        "input": spec["input"],
        "law_kind": spec["object_kind"],
        "rule_relation_constraint_function_or_probability_law": spec["law"],
        "result_kind": spec["result"],
        "parameters_and_variants": spec["input"],
        "evidence_limit": spec["limit"],
    }

    def finalize(not_applicable: set[str]) -> tuple[dict[str, Any], set[str]]:
        values.update(spec["semantic_values"])
        for field in spec["suppress_supported_fields"]:
            values.pop(field, None)
        not_applicable = (
            set(not_applicable) - set(spec["not_applicable_exclusions"])
        )
        overlap = set(values) & not_applicable
        if overlap:
            raise AuthoringError(
                f"{spec['name']} supports and excludes fields {sorted(overlap)}"
            )
        return values, not_applicable

    if profile == "FUNCTION":
        values.update(
            {
                "successor_cardinality": (
                    spec["cardinality"]
                    or "one returned value or collection per valid input"
                ),
                "determinism_branching_or_measure": (
                    spec["measure"] or "deterministic direct evaluation"
                ),
            }
        )
        if spec["completion"] is not None:
            values["termination_completion_failure"] = spec["completion"]
        return finalize(set(DIRECT_FUNCTION_NA))
    if profile == "REPRESENTATION":
        values.update(
            {
                "successor_cardinality": (
                    spec["cardinality"]
                    or "one representation per supplied retained history"
                ),
                "determinism_branching_or_measure": (
                    spec["measure"]
                    or "deterministic ordering/embedding of supplied states"
                ),
            }
        )
        if spec["completion"] is not None:
            values["termination_completion_failure"] = spec["completion"]
        return finalize(set(DIRECT_FUNCTION_NA))
    if profile == "RELATION":
        values.update(
            {
                "determinism_branching_or_measure": (
                    spec["measure"]
                    or (
                        "declarative satisfaction semantics with zero, one, "
                        "or many witnesses"
                    )
                ),
                "witness_semantics": (
                    "a witness is any supplied value tuple satisfying the "
                    "stated relation or predicate"
                ),
            }
        )
        return finalize(set(RELATION_NA))
    if profile == "DENOTATION":
        values.update(
            {
                "successor_cardinality": (
                    spec["cardinality"] or "one denoted mathematical object"
                ),
                "determinism_branching_or_measure": (
                    spec["measure"] or "deterministic declarative denotation"
                ),
            }
        )
        return finalize(set(DENOTATION_NA))
    if profile != "ITERATED":
        raise AuthoringError(f"unsupported typed profile {profile}")

    lowered = spec["object_kind"].lower()
    if "grammar" in lowered:
        frontier = (
            "each occurrence in one sentential form at which a displayed "
            "production can match"
        )
        schedule = (
            "one derivation successor applies one matching production at one "
            "matching occurrence; the source considers all such possibilities"
        )
        dependencies = (
            "the production left-hand side and any context explicitly written "
            "around its replaced nonterminal"
        )
        write = (
            "replace the selected occurrence by that production's right-hand "
            "side to form one successor sentential form"
        )
        cardinality = (
            "zero, one, or many derivation successors per sentential form"
        )
        measure = (
            "nondeterministic exhaustive branching; no probability measure "
            "or duplicate-merging policy is stated"
        )
    elif "multiway" in lowered:
        frontier = "every applicable rule occurrence in every current state"
        schedule = "retain all possible rewrites as the next aggregate state"
        dependencies = "the left-hand side and local matching context of each rule"
        write = "assemble every rewritten string and merge equal aggregate states"
        cardinality = (
            "one aggregate successor collection, with native branching inside it"
        )
        measure = "deterministic aggregate evolution with native branching"
    elif "cellular-automaton" in lowered:
        frontier = "all cells in the current configuration"
        schedule = "parallel synchronous update"
        dependencies = "the center cell and stated outer-totalistic neighborhood count"
        write = "replace every cell simultaneously by the rule result"
        cardinality = "one successor configuration"
        measure = "deterministic"
    else:
        frontier = "every symbol or element in the current substitution state"
        schedule = "parallel substitution of all current elements"
        dependencies = "the current symbol/color matched by the replacement table"
        write = "assemble the replacement blocks into the successor state"
        cardinality = "one successor substitution state"
        measure = "deterministic"
    values.update(
        {
            "native_time": "discrete successive update steps",
            "support": spec["carrier"],
            "alphabet_or_value_schema": (
                "the symbols, colors, or values explicitly fixed by the rule"
            ),
            "complete_state": "the complete current carrier configuration",
            "frontier_or_activation": frontier,
            "schedule": schedule,
            "read_dependencies_or_neighborhood": dependencies,
            "write_replacement_assembly_or_commit": write,
            "successor_cardinality": spec["cardinality"] or cardinality,
            "determinism_branching_or_measure": spec["measure"] or measure,
        }
    )
    if "seed" in spec["input"].lower() or "initial" in spec["input"].lower():
        values["seed"] = spec["input"]
    return finalize(set(ITERATED_NA))


def _typed_evidence_scopes(
    spec: dict[str, Any],
    rows: list[dict[str, str]],
    supported_fields: set[str],
    not_applicable_fields: set[str],
) -> dict[str, list[str]]:
    """Assign conservative, unit-specific fingerprint scopes."""

    explicit = spec["evidence_scopes"]
    scopes: dict[str, list[str]] = {}
    non_image = [
        row for row in rows if row["block_kind"] != "image"
    ]
    if not non_image:
        raise AuthoringError(f"{spec['name']} has no non-image identity source")
    primary_id = spec["identity_unit"]
    if primary_id not in {
        row["source_unit_id"] for row in non_image
    }:
        raise AuthoringError(
            f"{spec['name']} identity unit is absent or image-only"
        )
    identity_fields = {
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "complete_state",
        "input",
        "seed",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "parameters_and_variants",
        "evidence_limit",
    }
    exact_fields = {
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "termination_completion_failure",
        "parameters_and_variants",
        "evidence_limit",
    }
    context_fields = {
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "witness_semantics",
        "parameters_and_variants",
        "excluded_observers_and_representations",
        "evidence_limit",
    }
    image_fields = {
        "visible_history",
        "result_kind",
        "witness_semantics",
        "excluded_observers_and_representations",
    }
    for row in rows:
        unit_id = row["source_unit_id"]
        if unit_id in explicit:
            chosen = set(explicit[unit_id])
        elif row["block_kind"] == "image":
            chosen = image_fields
        elif unit_id == primary_id:
            chosen = identity_fields | context_fields
            if row["block_kind"] in {"fenced_code", "list", "table"}:
                chosen |= exact_fields
        elif row["block_kind"] in {"fenced_code", "list", "table"}:
            chosen = exact_fields
        else:
            chosen = context_fields
        scopes[unit_id] = sorted(
            chosen & (supported_fields | not_applicable_fields),
            key=FINGERPRINT_FIELDS.index,
        )

    primary_fields = set(scopes[primary_id])
    primary_fields.update(not_applicable_fields)
    if not explicit:
        primary_fields.update(
            supported_fields
            & {
                "result_kind",
                "successor_cardinality",
                "determinism_branching_or_measure",
                "termination_completion_failure",
                "witness_semantics",
            }
        )
        if spec["profile"] == "ITERATED":
            primary_fields.update(
                supported_fields
                & {
                    "rule_relation_constraint_function_or_probability_law",
                    "write_replacement_assembly_or_commit",
                }
            )
        if len(non_image) == 1:
            primary_fields.update(
                supported_fields
                & {
                    "rule_relation_constraint_function_or_probability_law",
                    "write_replacement_assembly_or_commit",
                }
            )
    scopes[primary_id] = sorted(
        primary_fields,
        key=FINGERPRINT_FIELDS.index,
    )
    for field in supported_fields | not_applicable_fields:
        if not any(field in fields for fields in scopes.values()):
            raise AuthoringError(
                f"{spec['name']} has no evidence scope for {field}"
            )
    return scopes


def _append_novel(values: list[Any], additions: list[Any]) -> list[Any]:
    """Preserve an audited array as an exact prefix and append novel values."""

    result = list(values)
    for item in additions:
        if item not in result:
            result.append(item)
    return result


def _enrich_existing_candidate(
    *,
    old: dict[str, Any],
    evidence: list[dict[str, Any]],
    reading_by_id: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Append source-grounded search evidence to one existing candidate."""

    candidate = deepcopy(old)
    candidate_id = candidate["id"]
    evidence = sorted(
        evidence,
        key=lambda item: int(item["evidence_id"][1:]),
    )
    unit_ids = [item["source_unit_id"] for item in evidence]
    candidate["source_unit_ids"] = _append_novel(
        candidate["source_unit_ids"],
        unit_ids,
    )
    candidate["source_evidence"] = [
        *candidate["source_evidence"],
        *evidence,
    ]
    candidate["source_status"] = _append_novel(
        candidate["source_status"],
        [reading_by_id[unit_id]["source_status"] for unit_id in unit_ids],
    )
    candidate["evidence_strength"] = _append_novel(
        candidate["evidence_strength"],
        [item["strength"] for item in evidence],
    )
    candidate["image_witnesses"] = _append_novel(
        candidate["image_witnesses"],
        [
            item["image_path"]
            for item in evidence
            if item["image_path"] is not None
        ],
    )
    for item in evidence:
        evidence_id = item["evidence_id"]
        for field in item["fingerprint_fields"]:
            if candidate["field_support"].get(field) != "SUPPORTED":
                raise AuthoringError(
                    f"{candidate_id} relink attempts to support non-SUPPORTED "
                    f"field {field}"
                )
            fingerprint = candidate["fingerprint"][field]
            if fingerprint["status"] != "SUPPORTED":
                raise AuthoringError(
                    f"{candidate_id}.{field} support records disagree"
                )
            fingerprint["evidence_ids"] = _append_novel(
                fingerprint["evidence_ids"],
                [evidence_id],
            )

    evidence_by_unit = {
        item["source_unit_id"]: item["evidence_id"] for item in evidence
    }
    semantic_appends: dict[str, list[dict[str, Any]]] = {}
    if candidate_id == "B0032":
        semantic_appends = {
            "parameters": [
                {
                    "name": "spatial slice selector",
                    "source_description": (
                        "middle-line selection or a sequence of offsets from "
                        "the center of a two-dimensional evolution"
                    ),
                    "evidence_ids": [
                        evidence_by_unit["U000978"],
                        evidence_by_unit["U006112"],
                    ],
                }
            ],
            "variants": [
                {
                    "name": "center-line history slice",
                    "source_description": (
                        "the one-dimensional line through the middle of each "
                        "successive two-dimensional pattern"
                    ),
                    "evidence_ids": [evidence_by_unit["U000978"]],
                },
                {
                    "name": "offset vertical-slice sequence",
                    "source_description": (
                        "vertical slices at a sequence of offsets from the "
                        "center, as stated for the code-942 example"
                    ),
                    "evidence_ids": [evidence_by_unit["U006112"]],
                },
            ],
        }
    elif candidate_id == "B0595":
        semantic_appends = {
            "variants": [
                {
                    "name": "GoldenRatio square-lattice line cut",
                    "source_description": (
                        "a line of GoldenRatio slope cuts a two-dimensional "
                        "square lattice to yield the one-dimensional Fibonacci "
                        "sequence"
                    ),
                    "evidence_ids": [evidence_by_unit["U006182"]],
                }
            ],
        }
    elif candidate_id == "B0922":
        semantic_appends = {
            "parameters": [
                {
                    "name": "alternate initial string",
                    "source_description": (
                        "ABA dies out, while ABAABABA grows exponentially "
                        "forever for the same three-rule preset"
                    ),
                    "evidence_ids": [evidence_by_unit["U006260"]],
                }
            ],
            "variants": [
                {
                    "name": "alternate-seed behavior",
                    "source_description": (
                        "the preset has source-stated extinction and "
                        "exponential-growth behaviors under alternate seeds"
                    ),
                    "evidence_ids": [evidence_by_unit["U006260"]],
                }
            ],
        }
    for collection, additions in semantic_appends.items():
        candidate[collection] = [*candidate[collection], *additions]

    if candidate_id == "B0094":
        candidate["uncertainties"] = _append_novel(
            candidate["uncertainties"],
            [
                "The Chapter 5 source calls rule 90 the one-dimensional "
                "component result but uses the undefined phrase “s alone” "
                "for the neighboring two-dimensional attribution."
            ],
        )
    if candidate_id == "B0922":
        candidate["uncertainties"] = _append_novel(
            candidate["uncertainties"],
            [
                "The bounded-reachability caption is OCR-defective (“shows "
                "wh”) and does not state its plotted axis/string encoding."
            ],
        )
    return {field: candidate[field] for field in CANDIDATE_FIELDS}


def _build_final_enrichment(
    *,
    reading_by_id: dict[str, dict[str, str]],
    asset_by_unit: dict[str, dict[str, str]],
    candidates_by_id: dict[str, dict[str, Any]],
    hit_by_pair: dict[tuple[int, str], str],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, Any]],
    list[str],
]:
    """Build the final omission delta in immutable search-hit order."""

    if len(RECOVERED_SPECS) != EXPECTED_NEW_CANDIDATE_COUNT:
        raise AuthoringError(
            "recovered candidate specification count drifted: "
            f"{len(RECOVERED_SPECS)}"
        )
    hit_number = {
        pair: int(hit_id[1:]) for pair, hit_id in hit_by_pair.items()
    }

    annotated: list[dict[str, Any]] = []
    for spec_index, original in enumerate(RECOVERED_SPECS):
        spec = dict(original)
        missing_units = [
            unit_id
            for unit_id in spec["units"]
            if unit_id not in reading_by_id
        ]
        if missing_units:
            raise AuthoringError(
                f"{spec['name']} reaches unknown units {missing_units}"
            )
        candidate_pairs = [
            (rank, ordinal, unit_id)
            for (ordinal, unit_id), rank in hit_number.items()
            if (
                ordinal <= 10
                and unit_id == spec["discovery_unit"]
            )
        ]
        if not candidate_pairs:
            raise AuthoringError(
                f"{spec['name']} lacks an F01-F10 discovery hit"
            )
        rank, ordinal, unit_id = min(candidate_pairs)
        spec["_spec_index"] = spec_index
        spec["_discovery_rank"] = rank
        spec["_discovery_pair"] = (ordinal, unit_id)
        annotated.append(spec)
    annotated.sort(
        key=lambda spec: (spec["_discovery_rank"], spec["_spec_index"])
    )

    candidate_anchor_counts: dict[str, int] = {}
    for offset, spec in enumerate(annotated):
        candidate_id = f"B{981 + offset:04d}"
        hit_id = hit_by_pair[spec["_discovery_pair"]]
        candidate_anchor_counts[hit_id] = (
            candidate_anchor_counts.get(hit_id, 0) + 1
        )
        spec["_candidate_id"] = candidate_id
        spec["_discovery_hit"] = hit_id
        spec["_discovery_ordinal"] = candidate_anchor_counts[hit_id]
    expected_ids = [
        f"B{number:04d}"
        for number in range(
            981,
            981 + EXPECTED_NEW_CANDIDATE_COUNT,
        )
    ]
    if [spec["_candidate_id"] for spec in annotated] != expected_ids:
        raise AuthoringError("search candidate-ID allocation drifted")

    for spec in annotated:
        values, not_applicable = _typed_semantics(spec)
        source_rows = [reading_by_id[unit_id] for unit_id in spec["units"]]
        scopes = _typed_evidence_scopes(
            spec,
            source_rows,
            set(values),
            not_applicable,
        )
        spec["_supported_values"] = values
        spec["_not_applicable_fields"] = not_applicable
        spec["_evidence_scopes"] = scopes

    evidence_plans: list[dict[str, Any]] = []
    for spec in annotated:
        for source_index, unit_id in enumerate(spec["units"]):
            unit_pairs = [
                (rank, ordinal, pair_unit)
                for (ordinal, pair_unit), rank in hit_number.items()
                if pair_unit == unit_id
            ]
            if not unit_pairs:
                raise AuthoringError(
                    f"{spec['name']} evidence unit {unit_id} lacks a hit"
                )
            rank, ordinal, _ = min(unit_pairs)
            evidence_plans.append(
                {
                    "plan_kind": "NEW_CANDIDATE",
                    "spec": spec,
                    "candidate_id": spec["_candidate_id"],
                    "unit_id": unit_id,
                    "source_index": source_index,
                    "rank": rank,
                    "query_ordinal": ordinal,
                    "hit_id": hit_by_pair[(ordinal, unit_id)],
                }
            )
    for relink in RELINK_SPECS:
        candidate_id = relink["candidate_id"]
        old_candidate = candidates_by_id.get(candidate_id)
        if old_candidate is None or old_candidate.get("record_status") != "ACTIVE":
            raise AuthoringError(
                f"relink target {candidate_id} is absent or inactive"
            )
        for source_index, (unit_id, fields) in enumerate(
            relink["units"].items()
        ):
            if unit_id not in reading_by_id:
                raise AuthoringError(
                    f"{candidate_id} relink reaches unknown unit {unit_id}"
                )
            invalid_fields = [
                field
                for field in fields
                if old_candidate["field_support"].get(field) != "SUPPORTED"
            ]
            if invalid_fields:
                raise AuthoringError(
                    f"{candidate_id} relink fields are not already SUPPORTED: "
                    f"{invalid_fields}"
                )
            unit_pairs = [
                (rank, ordinal, pair_unit)
                for (ordinal, pair_unit), rank in hit_number.items()
                if pair_unit == unit_id
            ]
            if not unit_pairs:
                raise AuthoringError(
                    f"{candidate_id} relink unit {unit_id} lacks a hit"
                )
            rank, ordinal, _ = min(unit_pairs)
            evidence_plans.append(
                {
                    "plan_kind": "EXISTING_RELINK",
                    "candidate_id": candidate_id,
                    "unit_id": unit_id,
                    "fields": fields,
                    "claim": relink["claim"],
                    "source_index": source_index,
                    "rank": rank,
                    "query_ordinal": ordinal,
                    "hit_id": hit_by_pair[(ordinal, unit_id)],
                }
            )
    evidence_plans.sort(
        key=lambda plan: (
            plan["rank"],
            int(plan["candidate_id"][1:]),
            plan["source_index"],
        )
    )
    evidence_anchor_counts: dict[str, int] = {}
    evidence_by_candidate: dict[str, list[dict[str, Any]]] = {
        spec["_candidate_id"]: [] for spec in annotated
    }
    evidence_by_candidate.update(
        {
            relink["candidate_id"]: []
            for relink in RELINK_SPECS
        }
    )
    block_modality = {
        "fenced_code": "CODE",
        "list": "FORMULA",
        "table": "TABLE",
        "paragraph": "PROSE",
        "heading": "PROSE",
        "image": "IMAGE",
    }
    for offset, plan in enumerate(evidence_plans):
        row = reading_by_id[plan["unit_id"]]
        spec = plan.get("spec")
        hit_id = plan["hit_id"]
        evidence_anchor_counts[hit_id] = (
            evidence_anchor_counts.get(hit_id, 0) + 1
        )
        source_status = row["source_status"]
        if source_status in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"}:
            strength = "DEFECT_LIMITED"
        elif row["block_kind"] == "image":
            strength = "CORROBORATING"
        else:
            strength = "DIRECT_PARTIAL_MECHANICS"
        modality = block_modality.get(row["block_kind"])
        if modality is None:
            raise AuthoringError(
                f"unsupported evidence block kind {row['block_kind']} "
                f"at {plan['unit_id']}"
            )
        if row["block_kind"] == "image":
            asset = asset_by_unit.get(plan["unit_id"])
            if asset is None:
                raise AuthoringError(
                    f"image evidence {plan['unit_id']} lacks an asset row"
                )
            image_path = asset["physical_path"]
            if plan["plan_kind"] == "NEW_CANDIDATE":
                claim = (
                    f"Original-resolution inspection corroborates the stated "
                    f"result/history representation for {spec['name']}; "
                    f"pixels do not supply additional native law mechanics."
                )
            else:
                claim = (
                    f"{plan['claim']} Original-resolution pixels corroborate "
                    f"only the scoped result/witness representation."
                )
        elif plan["plan_kind"] == "EXISTING_RELINK":
            image_path = None
            claim = plan["claim"]
        elif row["block_kind"] in {"fenced_code", "list", "table"}:
            image_path = None
            claim = (
                f"The exact formula, code, or table supplies the scoped law "
                f"and result evidence for {spec['name']}."
            )
        elif plan["source_index"] == 0:
            image_path = None
            claim = (
                f"The source unit identifies {spec['name']} and delimits only "
                f"the scoped carrier, input, law class, and evidence boundary."
            )
        else:
            image_path = None
            claim = (
                f"The source unit supplies scoped corroborating result, "
                f"parameter, witness, or evidence-limit context for "
                f"{spec['name']}."
            )
        fields = (
            spec["_evidence_scopes"][plan["unit_id"]]
            if plan["plan_kind"] == "NEW_CANDIDATE"
            else plan["fields"]
        )
        evidence_by_candidate[plan["candidate_id"]].append(
            _evidence(
                evidence_number=4049 + offset,
                hit_id=hit_id,
                hit_ordinal=evidence_anchor_counts[hit_id],
                unit_id=plan["unit_id"],
                strength=strength,
                modality=modality,
                claim=claim,
                fields=fields,
                image_path=image_path,
            )
        )

    candidates: list[dict[str, Any]] = []
    for spec in annotated:
        candidate_id = spec["_candidate_id"]
        evidence = sorted(
            evidence_by_candidate[candidate_id],
            key=lambda item: int(item["evidence_id"][1:]),
        )
        evidence_ids = [item["evidence_id"] for item in evidence]
        relations = [
            {
                "candidate_id": related_id,
                "relation": "SOURCE_COMPARE",
                "proof_kind": "PROVISIONAL_COMPARISON",
                "before_rationale": "",
                "after_rationale": "",
                "evidence_ids": evidence_ids[:1],
                "uncertainty": (
                    "The source makes these objects related in role or output "
                    "without establishing native-law identity."
                ),
            }
            for related_id in spec["related"]
        ]
        source_status = list(
            dict.fromkeys(
                reading_by_id[unit_id]["source_status"]
                for unit_id in spec["units"]
            )
        )
        parameter_evidence_ids = [
            item["evidence_id"]
            for item in evidence
            if "parameters_and_variants" in item["fingerprint_fields"]
        ]
        if not parameter_evidence_ids:
            raise AuthoringError(
                f"{candidate_id} lacks parameter evidence"
            )
        image_witnesses = [
            item["image_path"]
            for item in evidence
            if item["image_path"] is not None
        ]
        candidates.append(
            _new_candidate(
                candidate_id=candidate_id,
                name=spec["name"],
                aliases=spec["aliases"],
                discovery_hit_id=spec["_discovery_hit"],
                discovery_ordinal=spec["_discovery_ordinal"],
                source_unit_ids=spec["units"],
                evidence=evidence,
                supported_values=spec["_supported_values"],
                not_applicable_fields=spec["_not_applicable_fields"],
                parameters=[
                    {
                        "name": "input/parameter tuple",
                        "source_description": spec["input"],
                        "evidence_ids": parameter_evidence_ids,
                    }
                ],
                uncertainties=spec["uncertainties"],
                exact_missing_mechanics=spec["missing_mechanics"],
                related_candidate_ids=relations,
                source_status=source_status,
                image_witnesses=image_witnesses,
            )
        )
    for relink in RELINK_SPECS:
        candidate_id = relink["candidate_id"]
        relink_evidence = evidence_by_candidate[candidate_id]
        if not relink_evidence:
            raise AuthoringError(f"{candidate_id} has no relink evidence")
        candidates.append(
            _enrich_existing_candidate(
                old=candidates_by_id[candidate_id],
                evidence=relink_evidence,
                reading_by_id=reading_by_id,
            )
        )

    reading_additions: dict[str, list[str]] = {}
    anchor_units: set[str] = set()
    names_by_unit: dict[str, list[str]] = {}
    for spec in annotated:
        candidate_id = spec["_candidate_id"]
        anchor_units.add(spec["_discovery_pair"][1])
        for unit_id in spec["units"]:
            reading_additions.setdefault(unit_id, []).append(candidate_id)
            names_by_unit.setdefault(unit_id, []).append(spec["name"])
    for relink in RELINK_SPECS:
        candidate_id = relink["candidate_id"]
        candidate_name = candidates_by_id[candidate_id]["provisional_name"]
        for unit_id in relink["units"]:
            current_links = parse_links(
                reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            )
            if candidate_id not in current_links:
                reading_additions.setdefault(unit_id, []).append(candidate_id)
            names_by_unit.setdefault(unit_id, []).append(candidate_name)
    updated: list[dict[str, str]] = []
    for unit_id in sorted(reading_additions):
        old = reading_by_id[unit_id]
        row = dict(old)
        additions = sorted(
            list(dict.fromkeys(reading_additions[unit_id])),
            key=lambda candidate_id: int(candidate_id[1:]),
        )
        row["candidate_ids"] = _append_links(
            old["candidate_ids"],
            additions,
            f"{unit_id}.candidate_ids",
        )
        if old["review_disposition"] != "SOURCE_DEFECT_OR_AMBIGUITY":
            if (
                old["review_disposition"] == "CANDIDATE"
                or unit_id in anchor_units
            ):
                row["review_disposition"] = "CANDIDATE"
            else:
                row["review_disposition"] = "SUPPORTS_CANDIDATE"
        names = names_by_unit[unit_id]
        role = (
            "directly anchors"
            if unit_id in anchor_units
            else "supplies supporting identity or mechanics for"
        )
        row["evidence_statement"] = (
            f"Search omission challenge {role} {len(names)} recovered "
            f"candidate(s): {'; '.join(names)}."
        )
        updated.append(row)

    asset_updates: list[dict[str, str]] = []
    for unit_id in sorted(reading_additions):
        if reading_by_id[unit_id]["block_kind"] != "image":
            continue
        old_asset = asset_by_unit.get(unit_id)
        if old_asset is None:
            raise AuthoringError(
                f"promoted image unit {unit_id} lacks an asset row"
            )
        asset = dict(old_asset)
        additions = sorted(
            list(dict.fromkeys(reading_additions[unit_id])),
            key=lambda candidate_id: int(candidate_id[1:]),
        )
        asset["candidate_ids"] = _append_links(
            old_asset["candidate_ids"],
            additions,
            f"{old_asset['asset_id']}.candidate_ids",
        )
        asset_updates.append(asset)

    new_group_ids = [
        f"G{4049 + offset:06d}" for offset in range(len(evidence_plans))
    ]
    if len(updated) != EXPECTED_READING_UPDATE_COUNT:
        raise AuthoringError(
            f"reading update count drifted: {len(updated)}"
        )
    if len(new_group_ids) != EXPECTED_NEW_EVIDENCE_COUNT:
        raise AuthoringError(
            f"new evidence count drifted: {len(new_group_ids)}"
        )
    return updated, asset_updates, candidates, new_group_ids


def _materialize_route_delta(
    *,
    route_specs: list[dict[str, Any]],
    routes: list[dict[str, str]],
    reading_by_id: dict[str, dict[str, str]],
    reading_updates: list[dict[str, str]],
    candidates_by_id: dict[str, dict[str, Any]],
    candidate_updates: list[dict[str, Any]],
    new_evidence_group_ids: list[str],
    assets_by_id: dict[str, dict[str, str]],
    unit_text_by_id: dict[str, str],
    hit_by_pair: dict[tuple[int, str], str],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, Any]],
    list[dict[str, str]],
    dict[str, list[str]],
    list[str],
]:
    """Materialize frozen data-only route specs and bidirectional links."""

    if len(routes) != 248:
        raise AuthoringError(
            f"pre-search route count drifted: {len(routes)}"
        )
    update_by_id = {
        candidate["id"]: deepcopy(candidate)
        for candidate in candidate_updates
    }
    recovered_by_name = {
        candidate["provisional_name"]: candidate["id"]
        for candidate in candidate_updates
        if candidate["id"] not in candidates_by_id
    }
    if len(recovered_by_name) != EXPECTED_NEW_CANDIDATE_COUNT:
        raise AuthoringError("recovered candidate names are not unique")

    route_rows: list[dict[str, str]] = []
    route_ids_by_source: dict[str, list[str]] = {}
    route_candidates_by_source: dict[str, list[str]] = {}
    candidate_route_additions: dict[str, list[str]] = {}
    within_hit_counts: dict[str, int] = {}
    for offset, spec in enumerate(route_specs, start=249):
        route_id = f"R{offset:06d}"
        source_unit_id = spec["source_unit_id"]
        if source_unit_id not in reading_by_id:
            raise AuthoringError(
                f"{route_id} reaches unknown source {source_unit_id}"
            )
        source_asset_id = spec["source_asset_id"]
        if source_asset_id and source_asset_id not in assets_by_id:
            raise AuthoringError(
                f"{route_id} reaches unknown source asset {source_asset_id}"
            )
        hit_id = _hit_for(hit_by_pair, 15, source_unit_id)
        if spec["discovery_id"] != hit_id:
            raise AuthoringError(
                f"{route_id} frozen discovery hit drifted: "
                f"{spec['discovery_id']} != {hit_id}"
            )
        within_hit_counts[hit_id] = within_hit_counts.get(hit_id, 0) + 1
        if spec["discovery_ordinal"] != within_hit_counts[hit_id]:
            raise AuthoringError(
                f"{route_id} within-hit route ordinal is not contiguous"
            )
        source_text = unit_text_by_id.get(source_unit_id)
        if source_text is None:
            raise AuthoringError(f"{route_id} lacks source-bound text")
        normalize_locator = lambda value: " ".join(  # noqa: E731
            "".join(
                " "
                if unicodedata.category(character).startswith("P")
                else character.casefold()
                for character in unicodedata.normalize("NFKC", value)
            ).split()
        )
        if normalize_locator(spec["literal_target"]) not in normalize_locator(
            source_text
        ):
            raise AuthoringError(
                f"{route_id} literal target is absent from {source_unit_id} "
                "under NFKC/casefold/punctuation/whitespace normalization"
            )
        candidate_ids = [
            *spec["candidate_ids"],
            *[
                recovered_by_name[name]
                for name in spec["recovered_candidate_names"]
            ],
        ]
        candidate_ids = list(dict.fromkeys(candidate_ids))
        for candidate_id in candidate_ids:
            if (
                candidate_id not in candidates_by_id
                and candidate_id not in update_by_id
            ):
                raise AuthoringError(
                    f"{route_id} targets unknown candidate {candidate_id}"
                )
            candidate_route_additions.setdefault(
                candidate_id,
                [],
            ).append(route_id)
        route_ids_by_source.setdefault(source_unit_id, []).append(route_id)
        route_candidates_by_source.setdefault(
            source_unit_id,
            [],
        ).extend(candidate_ids)

        target_unit_ids = list(spec["target_unit_ids"])
        target_asset_ids = list(spec["target_asset_ids"])
        if any(unit_id not in reading_by_id for unit_id in target_unit_ids):
            raise AuthoringError(f"{route_id} has an unknown target unit")
        if any(asset_id not in assets_by_id for asset_id in target_asset_ids):
            raise AuthoringError(f"{route_id} has an unknown target asset")
        if spec["closure_scope"] == "WITHIN_STAGE" and (
            any(
                reading_by_id[unit_id]["path"] not in STAGE_PATHS
                for unit_id in target_unit_ids
            )
            or any(
                assets_by_id[asset_id]["assignment_path"] not in STAGE_PATHS
                for asset_id in target_asset_ids
            )
        ):
            raise AuthoringError(
                f"{route_id} WITHIN_STAGE target leaves Stage 9"
            )
        raw_row: dict[str, Any] = {
            "route_id": route_id,
            "source_unit_id": source_unit_id,
            "source_asset_id": source_asset_id,
            "discovery_epoch": spec["discovery_epoch"],
            "discovery_kind": spec["discovery_kind"],
            "discovery_id": hit_id,
            "discovery_ordinal": spec["discovery_ordinal"],
            "literal_target": spec["literal_target"],
            "route_kind": spec["route_kind"],
            "expected_topic": spec["expected_topic"],
            "owning_stage": spec["owning_stage"],
            "closure_scope": spec["closure_scope"],
            "status": spec["status"],
            "target_unit_ids": target_unit_ids,
            "target_asset_ids": target_asset_ids,
            "attempts": list(spec["attempts"]),
            "vocabulary_terms": list(spec["vocabulary_terms"]),
            "defect_boundary": spec["defect_boundary"],
        }
        row = {
            field: (
                _json_array(raw_row[field])
                if field
                in {
                    "target_unit_ids",
                    "target_asset_ids",
                    "attempts",
                    "vocabulary_terms",
                }
                else str(raw_row[field])
            )
            for field in CROSS_REFERENCE_HEADER
        }
        route_rows.append(row)

    if [row["route_id"] for row in route_rows] != [
        f"R{number:06d}"
        for number in range(249, 249 + len(route_specs))
    ]:
        raise AuthoringError("new route allocation is not contiguous")

    for unit_id in route_candidates_by_source:
        route_candidates_by_source[unit_id] = sorted(
            set(route_candidates_by_source[unit_id]),
            key=lambda value: int(value[1:]),
        )

    evidence_anchor_counts: dict[str, int] = {}
    for candidate in update_by_id.values():
        for evidence in candidate["source_evidence"]:
            anchor = evidence["discovery_anchor"]
            if anchor["kind"] == "SEARCH_HIT":
                evidence_anchor_counts[anchor["id"]] = max(
                    evidence_anchor_counts.get(anchor["id"], 0),
                    int(anchor["ordinal"]),
                )
    route_evidence_plans: list[tuple[str, str]] = []
    for unit_id in route_ids_by_source:
        for candidate_id in route_candidates_by_source[unit_id]:
            candidate = update_by_id.get(candidate_id)
            if candidate is None:
                candidate = candidates_by_id.get(candidate_id)
            if candidate is None:
                raise AuthoringError(
                    f"route provenance reaches unknown {candidate_id}"
                )
            if unit_id not in candidate["source_unit_ids"]:
                route_evidence_plans.append((unit_id, candidate_id))

    next_evidence_number = 4049 + len(new_evidence_group_ids)
    modality_by_block = {
        "fenced_code": "CODE",
        "list": "FORMULA",
        "table": "TABLE",
        "paragraph": "PROSE",
        "heading": "PROSE",
        "image": "IMAGE",
    }
    appended_route_group_ids: list[str] = []
    for offset, (unit_id, candidate_id) in enumerate(route_evidence_plans):
        candidate = update_by_id.get(candidate_id)
        if candidate is None:
            candidate = candidates_by_id.get(candidate_id)
        if candidate is None:
            raise AuthoringError(
                f"route evidence reaches unknown {candidate_id}"
            )
        candidate = deepcopy(candidate)
        hit_id = _hit_for(hit_by_pair, 15, unit_id)
        evidence_anchor_counts[hit_id] = (
            evidence_anchor_counts.get(hit_id, 0) + 1
        )
        row = reading_by_id[unit_id]
        modality = modality_by_block.get(row["block_kind"])
        if modality is None:
            raise AuthoringError(
                f"unsupported route-evidence block {row['block_kind']}"
            )
        evidence_number = next_evidence_number + offset
        evidence = _evidence(
            evidence_number=evidence_number,
            hit_id=hit_id,
            hit_ordinal=evidence_anchor_counts[hit_id],
            unit_id=unit_id,
            strength="CONTEXTUAL",
            modality=modality,
            claim=(
                "The literal F15 locator ties this already delimited "
                "candidate to the appended typed route; it supplies no "
                "additional native mechanics."
            ),
            fields=[],
        )
        candidate["source_unit_ids"] = [
            *candidate["source_unit_ids"],
            unit_id,
        ]
        candidate["source_evidence"] = [
            *candidate["source_evidence"],
            evidence,
        ]
        candidate["source_status"] = _append_novel(
            candidate["source_status"],
            [row["source_status"]],
        )
        candidate["evidence_strength"] = _append_novel(
            candidate["evidence_strength"],
            ["CONTEXTUAL"],
        )
        update_by_id[candidate_id] = {
            field: candidate[field] for field in CANDIDATE_FIELDS
        }
        appended_route_group_ids.append(f"G{evidence_number:06d}")

    for candidate_id, additions in candidate_route_additions.items():
        if candidate_id in update_by_id:
            candidate = update_by_id[candidate_id]
        else:
            candidate = deepcopy(candidates_by_id[candidate_id])
        prior = candidate["cross_reference_ids"]
        if set(prior) & set(additions):
            raise AuthoringError(
                f"{candidate_id} repeats a new route link"
            )
        candidate["cross_reference_ids"] = [*prior, *additions]
        update_by_id[candidate_id] = {
            field: candidate[field] for field in CANDIDATE_FIELDS
        }

    ordered_candidate_updates: list[dict[str, Any]] = []
    seen_candidate_ids: set[str] = set()
    for candidate in candidate_updates:
        candidate_id = candidate["id"]
        ordered_candidate_updates.append(update_by_id[candidate_id])
        seen_candidate_ids.add(candidate_id)
    for candidate_id in sorted(
        set(update_by_id) - seen_candidate_ids,
        key=lambda value: int(value[1:]),
    ):
        ordered_candidate_updates.append(update_by_id[candidate_id])

    reading_update_by_id = {
        row["source_unit_id"]: dict(row) for row in reading_updates
    }
    for unit_id, candidate_ids in route_candidates_by_source.items():
        old = reading_by_id[unit_id]
        row = reading_update_by_id.get(unit_id, dict(old))
        present = parse_links(
            row["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
        additions = [
            candidate_id
            for candidate_id in candidate_ids
            if candidate_id not in present
        ]
        if additions:
            row["candidate_ids"] = _append_links(
                row["candidate_ids"],
                additions,
                f"{unit_id}.candidate_ids",
            )
            if row["review_disposition"] != "SOURCE_DEFECT_OR_AMBIGUITY":
                row["review_disposition"] = (
                    "CANDIDATE"
                    if row["review_disposition"] == "CANDIDATE"
                    else "SUPPORTS_CANDIDATE"
                )
            support_sentence = (
                f"F15 route provenance contextually supports "
                f"{len(additions)} route-linked candidate(s)."
            )
            if unit_id in reading_update_by_id:
                row["evidence_statement"] = (
                    row["evidence_statement"].rstrip()
                    + " "
                    + support_sentence
                )
            else:
                row["evidence_statement"] = support_sentence
            reading_update_by_id[unit_id] = row
    for unit_id, additions in route_ids_by_source.items():
        old = reading_by_id[unit_id]
        row = reading_update_by_id.get(unit_id, dict(old))
        row["route_ids"] = _append_links(
            row["route_ids"],
            additions,
            f"{unit_id}.route_ids",
        )
        if (
            not parse_links(
                row["candidate_ids"],
                f"{unit_id}.candidate_ids",
            )
            and row["review_disposition"] != "SOURCE_DEFECT_OR_AMBIGUITY"
        ):
            row["review_disposition"] = "CROSS_REFERENCE"
        route_sentence = (
            f"Frozen locator search governs {len(additions)} typed "
            f"cross-reference route(s): {', '.join(additions)}."
        )
        if unit_id in reading_update_by_id:
            row["evidence_statement"] = (
                row["evidence_statement"].rstrip() + " " + route_sentence
            )
        else:
            row["evidence_statement"] = route_sentence
        reading_update_by_id[unit_id] = row

    return (
        [
            reading_update_by_id[unit_id]
            for unit_id in sorted(reading_update_by_id)
        ],
        ordered_candidate_updates,
        route_rows,
        route_candidates_by_source,
        [*new_evidence_group_ids, *appended_route_group_ids],
    )


def _normalized_hit_projection(
    round_record: dict[str, Any],
) -> list[tuple[Any, ...]]:
    queries = round_record["queries"]
    ordinal_by_query_id = {
        query["query_id"]: ordinal
        for ordinal, query in enumerate(queries, start=1)
    }
    return [
        (
            ordinal_by_query_id[hit["query_id"]],
            hit["source_unit_id"],
            hit["context_sha256"],
            hit["disposition"],
            hit["candidate_ids"],
            hit["route_ids"],
            hit["rationale"],
        )
        for hit in round_record["hits"]
    ]


def _source_rationale(
    row: dict[str, str],
    *,
    family_ordinal: int,
    outcome: str,
) -> str:
    statement = " ".join(row["evidence_statement"].split())
    if not statement:
        raise AuthoringError(
            f"{row['source_unit_id']} lacks an evidence statement"
        )
    lead = (
        f"Omission challenge F{family_ordinal:02d} "
        f"({QUERY_SPECS[family_ordinal - 1][0]}) at "
        f"{row['source_unit_id']} [{row['block_kind']}] retains {outcome}: "
        if family_ordinal <= 10
        else ""
    )
    if row["source_status"] in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"}:
        uncertainty = " ".join(row["uncertainty"].split())
        return (
            f"{lead}source_status={row['source_status']}; "
            f"uncertainty={uncertainty}. {statement}"
        )
    return f"{lead}{statement}"


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to canonical Goal 4")
    if (
        len(PROPOSED_VOCABULARY) != len(set(PROPOSED_VOCABULARY))
        or len(QUERY_SPECS) != 15
    ):
        raise AuthoringError("frozen vocabulary/query family is malformed")

    vocabulary_digest = hashlib.sha256(
        canonical_json_bytes(PROPOSED_VOCABULARY)
    ).hexdigest()
    if vocabulary_digest != EXPECTED_NEW_VOCABULARY_DIGEST:
        raise AuthoringError(
            f"frozen Stage 9 vocabulary drifted: {vocabulary_digest}"
        )
    query_spec_digest = hashlib.sha256(
        canonical_json_bytes(QUERY_SPECS)
    ).hexdigest()
    if query_spec_digest != EXPECTED_QUERY_SPEC_DIGEST:
        raise AuthoringError(
            f"frozen Stage 9 query family drifted: {query_spec_digest}"
        )
    try:
        route_audit_digest = (
            ch05_dimensions_search_route_specs.assert_frozen_spec()
        )
    except AssertionError as exc:
        raise AuthoringError(f"frozen F15 route audit failed: {exc}") from exc
    if (
        ch05_dimensions_search_route_specs.ROUTE_SPEC_DIGEST
        != EXPECTED_ROUTE_SPEC_DIGEST
        or route_audit_digest != EXPECTED_ROUTE_AUDIT_DIGEST
    ):
        raise AuthoringError(
            "frozen F15 route-spec or inventory digest drifted"
        )
    expected_route_counts = (
        ch05_dimensions_search_route_specs.EXPECTED_COUNTS
    )
    if expected_route_counts != {
        "f15_hit_units": 144,
        "new_routes": EXPECTED_NEW_ROUTE_COUNT,
        "new_route_source_units": 117,
        "within_stage_routes": 86,
        "cross_range_routes": 65,
        "stage_existing_routes": 46,
        "f15_existing_route_uses": 45,
        "f15_existing_route_source_units": 37,
        "non_bearing_locators": 17,
        "non_bearing_source_units": 6,
        "locator_dispositions": 213,
    }:
        raise AuthoringError("frozen F15 route inventory counts drifted")

    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    reading = read_csv(goal_dir / merge_worker_output.READING_NAME)
    assets = read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    candidates = read_jsonl(goal_dir / merge_worker_output.CANDIDATE_NAME)
    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(encoding="utf-8")
    )
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)

    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise AuthoringError("search rounds are not an array")
    prior_stage_rounds = [
        record
        for record in rounds
        if record.get("owning_stage") == 9 and record.get("epoch") == 2
    ]
    if len(prior_stage_rounds) not in {0, 1}:
        raise AuthoringError("expected zero or one prior Stage 9 LOCAL round")
    first_pass = not prior_stage_rounds
    expected_round_count = 12 if first_pass else 13
    if len(rounds) != expected_round_count:
        raise AuthoringError(
            f"expected exactly {expected_round_count} prior LOCAL rounds"
        )
    terminal = history[-1] if history else {}
    if first_pass:
        terminal_ok = (
            terminal.get("review_id") == "V000024"
            and terminal.get("stage") == 9
            and terminal.get("mode") == "ROUTE_RESOLUTION"
            and terminal.get("epoch") == 2
        )
    else:
        terminal_ok = (
            terminal.get("review_id") == "V000025"
            and terminal.get("stage") == 9
            and terminal.get("mode") == "SEARCH_APPEND"
            and terminal.get("epoch") == 2
            and terminal.get("reviewer")
            == "ch05-dimensions-local-search-e2"
            and prior_stage_rounds[0].get("round_id") == "S013"
        )
    if not terminal_ok:
        raise AuthoringError(
            "Stage 9 search authoring terminal state is not recognized"
        )
    if any(
        record.get("kind") != "LOCAL"
        for record in rounds
    ) or [
        (record.get("owning_stage"), record.get("epoch"))
        for record in rounds[:12]
    ] != [
        (4, 1),
        (4, 1),
        (5, 1),
        (5, 1),
        (6, 1),
        (6, 1),
        (7, 1),
        (7, 1),
        (8, 1),
        (8, 1),
        (8, 2),
        (8, 2),
    ]:
        raise AuthoringError("prior LOCAL round sequence differs")
    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 9 cannot author against a global fixed point")

    unit_by_id = {unit["id"]: unit for unit in units}
    reading_by_id = {row["source_unit_id"]: row for row in reading}
    asset_by_unit = {
        row["source_unit_id"]: row
        for row in assets
        if row["source_unit_id"] and row["assignment_path"] in STAGE_PATHS
    }
    assets_by_id = {row["asset_id"]: row for row in assets}
    candidates_by_id = {candidate["id"]: candidate for candidate in candidates}
    routes_by_id = {route["route_id"]: route for route in routes}
    if (
        len(unit_by_id) != len(units)
        or len(reading_by_id) != len(reading)
        or len(assets_by_id) != len(assets)
        or len(asset_by_unit)
        != sum(
            bool(row["source_unit_id"])
            and row["assignment_path"] in STAGE_PATHS
            for row in assets
        )
        or len(candidates_by_id) != len(candidates)
        or len(routes_by_id) != len(routes)
    ):
        raise AuthoringError("current blind ledgers contain duplicate IDs")

    stage_unit_ids = {
        unit["id"] for unit in units if unit["path"] in STAGE_PATHS
    }
    if len(stage_unit_ids) != EXPECTED_STAGE_UNIT_COUNT:
        raise AuthoringError(
            f"Stage 9 unit count drifted: {len(stage_unit_ids)}"
        )
    source_bytes_by_path = {
        path: (
            REPO_ROOT / "ref" / "A-New-Kind-of-Science" / path
        ).read_bytes()
        for path in STAGE_PATHS
    }
    unit_text_by_id = {
        unit["id"]: source_bytes_by_path[unit["path"]][
            unit["byte_start"] : unit["byte_end"]
        ].decode("utf-8")
        for unit in units
        if unit["id"] in stage_unit_ids
    }
    stage_reading = [
        row for row in reading if row["source_unit_id"] in stage_unit_ids
    ]
    if (
        len(stage_reading) != len(stage_unit_ids)
        or any(
            row["path"] not in STAGE_PATHS
            or row["review_status"] != "REVIEWED"
            or row["review_epoch"] != "2"
            or row["review_stage"] != "9"
            for row in stage_reading
        )
    ):
        raise AuthoringError("Stage 9 source paths are not fully reviewed")
    stage_assets = [
        row for row in assets if row["assignment_path"] in STAGE_PATHS
    ]
    if len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT or any(
        row["inspection_status"] != "SCREENED"
        or row["review_epoch"] != "2"
        or row["review_stage"] != "9"
        for row in stage_assets
    ):
        raise AuthoringError("Stage 9 assets are not fully screened")

    initial_stage_candidates = {
        candidate_id
        for row in stage_reading
        for candidate_id in parse_links(
            row["candidate_ids"],
            f"{row['source_unit_id']}.candidate_ids",
        )
    }
    expected_current_candidate_count = (
        EXPECTED_INITIAL_STAGE_CANDIDATE_COUNT
        if first_pass
        else EXPECTED_ENRICHED_STAGE_CANDIDATE_COUNT
    )
    if len(initial_stage_candidates) != expected_current_candidate_count:
        raise AuthoringError(
            "current Stage 9 candidate relationship count drifted: "
            f"{len(initial_stage_candidates)}"
        )
    if any(
        candidates_by_id.get(candidate_id, {}).get("record_status") != "ACTIVE"
        for candidate_id in initial_stage_candidates
    ):
        raise AuthoringError("Stage 9 reaches an unknown or inactive candidate")
    recovered_candidate_ids = {
        f"B{number:04d}"
        for number in range(
            981,
            981 + EXPECTED_NEW_CANDIDATE_COUNT,
        )
    }
    base_stage_candidates = (
        initial_stage_candidates - recovered_candidate_ids
    )
    expected_base_stage_candidate_count = (
        EXPECTED_INITIAL_STAGE_CANDIDATE_COUNT
        if first_pass
        else (
            EXPECTED_INITIAL_STAGE_CANDIDATE_COUNT
            + EXPECTED_RELINKED_EXISTING_STAGE_CANDIDATE_COUNT
        )
    )
    if len(base_stage_candidates) != expected_base_stage_candidate_count:
        raise AuthoringError("pre-search Stage 9 candidate set drifted")
    if not first_pass and not (
        recovered_candidate_ids <= initial_stage_candidates
        and prior_stage_rounds[0].get("new_candidates")
        == sorted(
            recovered_candidate_ids,
            key=lambda candidate_id: int(candidate_id[1:]),
        )
    ):
        raise AuthoringError("applied S013 recovered-candidate suffix differs")

    active_route_ids = {
        route_id
        for row in stage_reading
        for route_id in parse_links(
            row["route_ids"],
            f"{row['source_unit_id']}.route_ids",
        )
    }
    for candidate_id in initial_stage_candidates:
        active_route_ids.update(
            candidates_by_id[candidate_id]["cross_reference_ids"]
        )
    for route in routes:
        target_units = set(
            parse_links(
                route["target_unit_ids"],
                f"{route['route_id']}.target_unit_ids",
            )
        )
        if route["owning_stage"] == "9" or target_units & stage_unit_ids:
            active_route_ids.add(route["route_id"])
    expected_active_route_count = (
        EXPECTED_INITIAL_STAGE_ROUTE_COUNT
        if first_pass
        else EXPECTED_ENRICHED_STAGE_ROUTE_COUNT
    )
    if len(active_route_ids) != expected_active_route_count:
        raise AuthoringError(
            f"Stage 9 active route count drifted: {len(active_route_ids)}"
        )
    stage_owned_routes = [
        routes_by_id[route_id]
        for route_id in active_route_ids
        if routes_by_id[route_id]["owning_stage"] == "9"
    ]
    if first_pass and (
        len(stage_owned_routes) != 46
        or sum(
            row["closure_scope"] == "WITHIN_STAGE"
            and row["status"] == "RESOLVED"
            for row in stage_owned_routes
        )
        != 20
        or sum(
            row["closure_scope"] == "CROSS_RANGE"
            and row["status"] == "PENDING"
            for row in stage_owned_routes
        )
        != 26
    ):
        raise AuthoringError("Stage 9 route closure differs from 20/26")

    semantic_projection = {
        "candidates": [
            {
                "id": candidate_id,
                "name": candidates_by_id[candidate_id]["provisional_name"],
                "aliases": candidates_by_id[candidate_id]["aliases"],
                "mechanics": {
                    field: candidates_by_id[candidate_id]["fingerprint"][field][
                        "value"
                    ]
                    for field in (
                        "object_kind",
                        "carrier",
                        "input",
                        "frontier_or_activation",
                        "schedule",
                        "read_dependencies_or_neighborhood",
                        "law_kind",
                        "rule_relation_constraint_function_or_probability_law",
                        "result_kind",
                        "determinism_branching_or_measure",
                        "termination_completion_failure",
                        "witness_semantics",
                    )
                },
                "cross_reference_ids": candidates_by_id[candidate_id][
                    "cross_reference_ids"
                ],
            }
            for candidate_id in sorted(base_stage_candidates)
        ],
        "routes": [
            {
                key: routes_by_id[route_id][key]
                for key in (
                    "route_id",
                    "literal_target",
                    "route_kind",
                    "expected_topic",
                    "closure_scope",
                    "status",
                    "target_unit_ids",
                    "vocabulary_terms",
                    "defect_boundary",
                )
            }
            for route_id in sorted(active_route_ids)
        ],
    }
    semantic_digest = hashlib.sha256(
        canonical_json_bytes(semantic_projection)
    ).hexdigest()
    expected_semantic_digest = EXPECTED_ACTIVE_SEMANTIC_DIGESTS[
        f"S{len(rounds) + 1:03d}"
    ]
    if semantic_digest != expected_semantic_digest:
        raise AuthoringError(
            f"Stage 9 active semantic projection drifted: {semantic_digest}"
        )

    query_start = sum(
        len(record.get("queries", [])) for record in rounds
    ) + 1
    queries = [
        {
            "query_id": f"Q{query_start + offset:04d}",
            "family": family,
            "pattern": pattern,
            "mode": mode,
            "case_sensitive": False,
            "whole_word": False,
            "scope_paths": STAGE_PATHS,
        }
        for offset, (family, pattern, mode) in enumerate(QUERY_SPECS)
    ]
    result_pairs, query_errors = validate_audit.execute_frozen_queries(
        queries,
        units,
        REPO_ROOT / "ref" / "A-New-Kind-of-Science",
    )
    if query_errors:
        raise AuthoringError("; ".join(query_errors))
    if len(result_pairs) != EXPECTED_RESULT_PAIR_COUNT:
        raise AuthoringError(
            f"Stage 9 result-pair count drifted: {len(result_pairs)}"
        )
    hit_counts = [
        sum(query_id == query["query_id"] for query_id, _ in result_pairs)
        for query in queries
    ]
    if hit_counts != EXPECTED_HIT_COUNTS:
        raise AuthoringError(f"Stage 9 query hit counts drifted: {hit_counts}")
    normalized_pairs = [
        (int(query_id[1:]) - query_start + 1, unit_id)
        for query_id, unit_id in result_pairs
    ]
    normalized_digest = hashlib.sha256(
        canonical_json_bytes(normalized_pairs)
    ).hexdigest()
    if normalized_digest != EXPECTED_NORMALIZED_RESULT_DIGEST:
        raise AuthoringError(
            f"Stage 9 normalized result pairs drifted: {normalized_digest}"
        )

    result_unit_ids = sorted({unit_id for _, unit_id in result_pairs})
    if len(result_unit_ids) != EXPECTED_UNIQUE_RESULT_UNIT_COUNT:
        raise AuthoringError(
            f"Stage 9 unique result-unit count drifted: {len(result_unit_ids)}"
        )
    path_pair_counts = {
        path: sum(
            unit_by_id[unit_id]["path"] == path
            for _, unit_id in result_pairs
        )
        for path in STAGE_PATHS
    }
    path_unique_counts = {
        path: sum(
            unit_by_id[unit_id]["path"] == path
            for unit_id in result_unit_ids
        )
        for path in STAGE_PATHS
    }
    if (
        path_pair_counts != EXPECTED_PATH_PAIR_COUNTS
        or path_unique_counts != EXPECTED_PATH_UNIQUE_UNIT_COUNTS
    ):
        raise AuthoringError(
            "Stage 9 path-local result counts drifted: "
            f"pairs={path_pair_counts} unique={path_unique_counts}"
        )

    hit_start = sum(
        len(record.get("hits", [])) for record in rounds
    ) + 1
    hit_by_pair = {
        (ordinal, unit_id): f"H{hit_start + offset:06d}"
        for offset, (ordinal, unit_id) in enumerate(normalized_pairs)
    }
    if first_pass:
        (
            reading_updates,
            asset_updates,
            candidate_updates,
            new_evidence_group_ids,
        ) = _build_final_enrichment(
            reading_by_id=reading_by_id,
            asset_by_unit=asset_by_unit,
            candidates_by_id=candidates_by_id,
            hit_by_pair=hit_by_pair,
        )
        route_specs = [
            deepcopy(spec)
            for spec in ch05_dimensions_search_route_specs.ROUTE_SPECS
        ]
        if len(route_specs) != EXPECTED_NEW_ROUTE_COUNT:
            raise AuthoringError(
                "frozen F15 route-spec count drifted: "
                f"{len(route_specs)}"
            )
        (
            reading_updates,
            candidate_updates,
            route_appends,
            route_candidates_by_source,
            new_evidence_group_ids,
        ) = _materialize_route_delta(
            route_specs=route_specs,
            routes=routes,
            reading_by_id=reading_by_id,
            reading_updates=reading_updates,
            candidates_by_id=candidates_by_id,
            candidate_updates=candidate_updates,
            new_evidence_group_ids=new_evidence_group_ids,
            assets_by_id=assets_by_id,
            unit_text_by_id=unit_text_by_id,
            hit_by_pair=hit_by_pair,
        )
    else:
        reading_updates = []
        asset_updates = []
        candidate_updates = []
        route_appends = []
        route_candidates_by_source = {}
        new_evidence_group_ids = []
    update_by_id = {
        row["source_unit_id"]: row for row in reading_updates
    }
    proposed_reading_by_id = {
        row["source_unit_id"]: update_by_id.get(row["source_unit_id"], row)
        for row in reading
    }
    enriched_candidates_by_id = {
        **candidates_by_id,
        **{candidate["id"]: candidate for candidate in candidate_updates},
    }
    expected_stage_candidates = {
        candidate_id
        for unit_id in stage_unit_ids
        for candidate_id in parse_links(
            proposed_reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
    }
    if len(expected_stage_candidates) != EXPECTED_ENRICHED_STAGE_CANDIDATE_COUNT:
        raise AuthoringError("enriched Stage 9 candidate count drifted")

    proposed_routes_by_id = {
        **routes_by_id,
        **{route["route_id"]: route for route in route_appends},
    }
    proposed_active_route_ids = {
        route_id
        for unit_id in stage_unit_ids
        for route_id in parse_links(
            proposed_reading_by_id[unit_id]["route_ids"],
            f"{unit_id}.route_ids",
        )
    }
    for candidate_id in expected_stage_candidates:
        proposed_active_route_ids.update(
            enriched_candidates_by_id[candidate_id]["cross_reference_ids"]
        )
    for route in proposed_routes_by_id.values():
        target_units = set(
            parse_links(
                route["target_unit_ids"],
                f"{route['route_id']}.target_unit_ids",
            )
        )
        if route["owning_stage"] == "9" or target_units & stage_unit_ids:
            proposed_active_route_ids.add(route["route_id"])
    if len(proposed_active_route_ids) != EXPECTED_ENRICHED_STAGE_ROUTE_COUNT:
        raise AuthoringError(
            "enriched Stage 9 active route count drifted: "
            f"{len(proposed_active_route_ids)}"
        )

    triage_projection = [
        (
            unit_id,
            proposed_reading_by_id[unit_id]["review_disposition"],
            proposed_reading_by_id[unit_id]["source_status"],
            parse_links(
                proposed_reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            ),
            parse_links(
                proposed_reading_by_id[unit_id]["route_ids"],
                f"{unit_id}.route_ids",
            ),
        )
        for unit_id in result_unit_ids
    ]
    triage_digest = hashlib.sha256(
        canonical_json_bytes(triage_projection)
    ).hexdigest()
    if triage_digest != EXPECTED_TRIAGE_DIGEST:
        raise AuthoringError(
            f"Stage 9 search triage projection drifted: {triage_digest}"
        )

    reached_candidates = {
        candidate_id
        for ordinal, unit_id in normalized_pairs
        if ordinal <= 10
        for candidate_id in parse_links(
            proposed_reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
    }
    if reached_candidates != expected_stage_candidates:
        raise AuthoringError(
            "candidate-facing Stage 9 search differs from its target: "
            f"missing={sorted(expected_stage_candidates - reached_candidates)} "
            f"unexpected={sorted(reached_candidates - expected_stage_candidates)}"
        )
    candidate_coverage: list[dict[str, Any]] = []
    pair_set = set(normalized_pairs)
    for candidate_id in sorted(expected_stage_candidates):
        candidate = enriched_candidates_by_id[candidate_id]
        candidate_units = set(candidate["source_unit_ids"])
        candidate_units.update(
            item["source_unit_id"]
            for item in candidate["source_evidence"]
            if isinstance(item.get("source_unit_id"), str)
        )
        witnesses = sorted(
            (ordinal, unit_id)
            for ordinal, unit_id in pair_set
            if ordinal <= 10
            and unit_id in candidate_units
            and candidate_id
            in parse_links(
                proposed_reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            )
        )
        if not witnesses:
            raise AuthoringError(
                f"{candidate_id} lacks a candidate-specific F01-F10 witness"
            )
        direct_units = {
            item["source_unit_id"]
            for item in candidate["source_evidence"]
            if item.get("source_unit_id") in stage_unit_ids
            and item.get("strength") in DIRECT_STRENGTHS
        }
        if direct_units and not any(
            unit_id in direct_units for _, unit_id in witnesses
        ):
            raise AuthoringError(
                f"{candidate_id} lacks a direct-evidence search witness"
            )
        candidate_coverage.append(
            {
                "candidate_id": candidate_id,
                "witnesses": [
                    [ordinal, unit_id] for ordinal, unit_id in witnesses
                ],
                "direct_units": sorted(direct_units),
            }
        )
    coverage_digest = hashlib.sha256(
        canonical_json_bytes(candidate_coverage)
    ).hexdigest()
    if coverage_digest != EXPECTED_CANDIDATE_COVERAGE_DIGEST:
        raise AuthoringError(
            f"Stage 9 candidate coverage drifted: {coverage_digest}"
        )

    result_set = set(result_unit_ids)
    candidate_route_witnesses: dict[str, set[str]] = {}
    for candidate_id in expected_stage_candidates:
        candidate_route_ids = enriched_candidates_by_id[candidate_id][
            "cross_reference_ids"
        ]
        if not candidate_route_ids:
            continue
        candidate_witnesses = {
            unit_id
            for unit_id in result_set & stage_unit_ids
            if candidate_id
            in parse_links(
                proposed_reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            )
        }
        for route_id in candidate_route_ids:
            candidate_route_witnesses.setdefault(route_id, set()).update(
                candidate_witnesses
            )

    route_coverage: list[tuple[str, list[str]]] = []
    for route_id in sorted(proposed_active_route_ids):
        route = proposed_routes_by_id[route_id]
        witnesses: set[str] = set()
        if route["source_unit_id"] in stage_unit_ids:
            witnesses.add(route["source_unit_id"])
        witnesses.update(
            set(
                parse_links(
                    route["target_unit_ids"],
                    f"{route_id}.target_unit_ids",
                )
            )
            & stage_unit_ids
        )
        witnesses.update(candidate_route_witnesses.get(route_id, set()))
        witnesses &= result_set
        if not witnesses:
            raise AuthoringError(
                f"{route_id} lacks an in-scope frozen-query witness"
            )
        route_coverage.append((route_id, sorted(witnesses)))
    route_coverage_digest = hashlib.sha256(
        canonical_json_bytes(route_coverage)
    ).hexdigest()
    if route_coverage_digest != EXPECTED_ROUTE_COVERAGE_DIGEST:
        raise AuthoringError(
            f"Stage 9 route coverage drifted: {route_coverage_digest}"
        )

    omission_projection: list[tuple[Any, ...]] = []
    for ordinal, unit_id in normalized_pairs:
        if ordinal > 10:
            continue
        row = proposed_reading_by_id[unit_id]
        if not parse_links(
            row["candidate_ids"], f"{unit_id}.candidate_ids"
        ) and not parse_links(row["route_ids"], f"{unit_id}.route_ids"):
            omission_projection.append(
                (
                    ordinal,
                    unit_id,
                    row["review_disposition"],
                    row["source_status"],
                    row["uncertainty"],
                    row["evidence_statement"],
                )
            )
    omission_digest = hashlib.sha256(
        canonical_json_bytes(omission_projection)
    ).hexdigest()
    if (
        len(omission_projection) != EXPECTED_OMISSION_CHALLENGE_COUNT
        or omission_digest != EXPECTED_OMISSION_CHALLENGE_DIGEST
    ):
        raise AuthoringError(
            "Stage 9 omission challenge drifted: "
            f"count={len(omission_projection)} digest={omission_digest}"
        )

    hits: list[dict[str, Any]] = []
    for offset, (query_id, unit_id) in enumerate(result_pairs):
        family_ordinal = int(query_id[1:]) - query_start + 1
        row = proposed_reading_by_id[unit_id]
        candidate_ids = parse_links(
            row["candidate_ids"], f"{unit_id}.candidate_ids"
        )
        row_route_ids = parse_links(
            row["route_ids"], f"{unit_id}.route_ids"
        )
        if candidate_ids:
            disposition = "GOVERNED_CANDIDATE_OR_SUPPORT"
            rationale = _source_rationale(
                row,
                family_ordinal=family_ordinal,
                outcome="governed candidate/support",
            )
        elif row_route_ids:
            disposition = "CROSS_REFERENCE"
            rationale = _source_rationale(
                row,
                family_ordinal=family_ordinal,
                outcome="typed cross-reference",
            )
        elif row["review_disposition"] in {
            "REPRESENTATION_OR_OBSERVER",
            "APPLICATION_OR_EMULATION",
            "SOURCE_DEFECT_OR_AMBIGUITY",
        }:
            disposition = "CONTROL_OR_RELATIONSHIP"
            rationale = _source_rationale(
                row,
                family_ordinal=family_ordinal,
                outcome="control/relationship",
            )
        elif row["review_disposition"] in {
            "NO_CONSTRUCTION",
            "HISTORICAL_ONLY",
        }:
            disposition = "EXCLUSION"
            rationale = _source_rationale(
                row,
                family_ordinal=family_ordinal,
                outcome="exclusion",
            )
        else:
            raise AuthoringError(
                f"{unit_id} has ungoverned construction disposition "
                f"{row['review_disposition']}"
            )
        hits.append(
            {
                "hit_id": f"H{hit_start + offset:06d}",
                "query_id": query_id,
                "source_unit_id": unit_id,
                "context_sha256": unit_by_id[unit_id]["sha256"],
                "disposition": disposition,
                "candidate_ids": candidate_ids,
                "route_ids": row_route_ids,
                "rationale": rationale,
            }
        )

    disposition_counts: dict[str, int] = {}
    for hit in hits:
        disposition = hit["disposition"]
        disposition_counts[disposition] = (
            disposition_counts.get(disposition, 0) + 1
        )
    if disposition_counts != EXPECTED_DISPOSITION_COUNTS:
        raise AuthoringError(
            f"Stage 9 hit dispositions drifted: {disposition_counts}"
        )

    existing_vocabulary = search.get("vocabulary")
    if not isinstance(existing_vocabulary, list) or len(
        existing_vocabulary
    ) != len(set(existing_vocabulary)):
        raise AuthoringError("global search vocabulary is malformed")
    mechanically_deduplicated = [
        value
        for value in PROPOSED_VOCABULARY
        if value not in existing_vocabulary
    ]
    if first_pass:
        if mechanically_deduplicated != PROPOSED_VOCABULARY:
            raise AuthoringError(
                "Stage 9 vocabulary is not a fully new frozen suffix"
            )
        new_vocabulary = mechanically_deduplicated
    else:
        if mechanically_deduplicated:
            raise AuthoringError(
                "applied S013 vocabulary is not fully present"
            )
        if existing_vocabulary[-len(PROPOSED_VOCABULARY) :] != (
            PROPOSED_VOCABULARY
        ):
            raise AuthoringError("applied S013 vocabulary suffix differs")
        new_vocabulary = []
    if ASSUMPTION not in search.get("tool_assumptions", []):
        raise AuthoringError("prior search assumption is absent")

    round_record: dict[str, Any] = {
        "round_id": f"S{len(rounds) + 1:03d}",
        "epoch": 2,
        "kind": "LOCAL",
        "owning_stage": 9,
        "queries": queries,
        "tool_assumptions": [ASSUMPTION],
        "result_ids": [hit["hit_id"] for hit in hits],
        "result_digest": "",
        "hits": hits,
        "new_vocabulary": new_vocabulary,
        "new_candidates": [
            candidate["id"]
            for candidate in candidate_updates
            if candidate["id"] not in candidates_by_id
        ],
        "new_evidence_groups": new_evidence_group_ids,
        "new_routes": [route["route_id"] for route in route_appends],
        "rerun_digest": "",
    }
    digest = validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    if digest != EXPECTED_ROUND_DIGESTS.get(round_record["round_id"]):
        raise AuthoringError(
            f"{round_record['round_id']} result digest drifted: {digest}"
        )
    if prior_stage_rounds and _normalized_hit_projection(
        prior_stage_rounds[0]
    ) != _normalized_hit_projection(round_record):
        raise AuthoringError(
            "Stage 9 zero-delta rerun differs from the S013 hit projection"
        )

    proposed_search = deepcopy(search)
    proposed_search["vocabulary"].extend(new_vocabulary)
    proposed_search["rounds"].append(round_record)
    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "ch05-dimensions-local-search-e2",
        "epoch": 2,
        "source_paths": STAGE_PATHS if first_pass else [],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "reading_updates": reading_updates,
        "asset_updates": asset_updates,
        "candidate_updates": candidate_updates,
        "route_appends": route_appends,
        "proposed_search": proposed_search,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} OUTPUT_JSON", file=sys.stderr)
        return 2
    output_path = Path(sys.argv[1])
    try:
        with audit_transaction.read_guard(GOAL_DIR):
            proposal = build_proposal(GOAL_DIR)
            atomic_create(output_path, canonical_json_bytes(proposal))
    except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"Chapter 5 search authoring failed: {exc}", file=sys.stderr)
        return 1
    round_record = proposal["proposed_search"]["rounds"][-1]
    counts: dict[str, int] = {}
    for hit in round_record["hits"]:
        disposition = hit["disposition"]
        counts[disposition] = counts.get(disposition, 0) + 1
    print(
        f"authored {round_record['round_id']}: "
        f"queries={len(round_record['queries'])} "
        f"hits={len(round_record['hits'])} "
        f"new_vocabulary={len(round_record['new_vocabulary'])} "
        f"new_candidates={len(round_record['new_candidates'])} "
        f"new_evidence_groups={len(round_record['new_evidence_groups'])} "
        f"reading_updates={len(proposal['reading_updates'])} "
        f"dispositions={json.dumps(counts, sort_keys=True)} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
