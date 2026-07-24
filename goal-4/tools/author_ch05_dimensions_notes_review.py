#!/usr/bin/env python3
"""Author the blind Stage 9 Chapter 5 Notes review deterministically.

This helper is intentionally sealed-bundle driven.  It verifies the immutable
assignment projection, writes only the prepared worker output, and contains
the human semantic judgments from the complete sequential and visual review.
It does not inspect or merge the global audit ledger.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


WORKER = "ch05-dimensions-notes-reader-e2"
STAGE = "9"
EPOCH = "2"
SOURCE_PATH = "BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes.md"
EXPECTED = {
    "input/reading-input.csv": "2d34c7161c30c90d69a57a461703209750af3c371b523e8fb1d33a53d2bbfd92",
    "input/asset-input.csv": "eacf77ccc7c765f44c00dec4dc943ef2a9ffb25d25c219f081057560538452c4",
    "input/source-units.jsonl": "d10cd5cd261e5779a0b3342c5afca2f225752d80912eac15c178ed60efde9aae",
    f"input/sources/{SOURCE_PATH}": "f4d1fdeddedb3b18438a473661c8f82dc389b76cca22130a6d271e68733236b9",
    "allowed-manifest.json": "939ceb792fe3f91aa7999a5b76877d924bc8a05ea139462f3030b34f3d5b04a5",
}

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

NA = "NOT_APPLICABLE"
UNK = "UNKNOWN_FROM_SOURCE"
SUP = "SUPPORTED"
CONFLICT = "CONFLICTING_SOURCE"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jlist(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def ev(
    unit: str | None,
    claim: str,
    *,
    modality: str = "PROSE",
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    image: str | None = None,
    fields: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "unit": unit,
        "claim": claim,
        "modality": modality,
        "strength": strength,
        "image": image,
        "fields": fields,
    }


CORE = {
    "CA": {
        "object_kind": "cellular-automaton construction",
        "native_time": "discrete evolution steps",
        "carrier": "cells on the stated lattice, tiling, or network",
        "support": "the carrier's cells",
        "topology": "the stated adjacency/neighborhood topology",
        "structural_invariants": "cell identity and carrier adjacency persist across updates",
        "alphabet_or_value_schema": "a finite cell-color alphabet",
        "complete_state": "one color for every cell",
        "visible_history": None,
        "control_state": None,
        "seed": "an initial cell-color configuration",
        "input": None,
        "boundary": "finite-array boundary handling is not fully fixed by all formulations",
        "external_data": None,
        "frontier_or_activation": "all carrier cells are rule sites each step",
        "schedule": "parallel synchronous update",
        "read_dependencies_or_neighborhood": "the stated local neighborhood",
        "law_kind": "local transition rule",
        "rule_relation_constraint_function_or_probability_law": "look up the next color from the neighborhood configuration",
        "write_replacement_assembly_or_commit": "replace cell colors simultaneously",
        "result_kind": "a successor cell-color configuration",
        "successor_cardinality": "one successor for a fixed rule and state",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "iterate for a requested number of steps or indefinitely",
        "witness_semantics": None,
        "parameters_and_variants": "rule code, dimension, alphabet size, topology, and seed",
        "excluded_observers_and_representations": "projections, slices, plots, and rendered histories are not native state laws",
        "evidence_limit": "only mechanics explicitly fixed in the assigned Notes and owned images are claimed",
    },
    "TM": {
        "object_kind": "two-dimensional Turing-machine construction",
        "native_time": "discrete head transitions",
        "carrier": "a two-dimensional tape plus one head",
        "support": "tape cells and the current head location",
        "topology": "the stated two-dimensional grid adjacency",
        "structural_invariants": "tape-cell identity and one-head identity persist",
        "alphabet_or_value_schema": "finite tape colors and finite head states",
        "complete_state": "head state, tape coloring, and head position",
        "visible_history": None,
        "control_state": "the finite head state",
        "seed": "initial tape coloring, head state, and head position",
        "input": None,
        "boundary": "the in-scope source does not fix all finite-tape boundary behavior",
        "external_data": None,
        "frontier_or_activation": "the cell under the single head",
        "schedule": "one head transition per step",
        "read_dependencies_or_neighborhood": "head state and color under the head",
        "law_kind": "state/write/move transition rule",
        "rule_relation_constraint_function_or_probability_law": "map current state and scanned color to new state, written color, and displacement or turn",
        "write_replacement_assembly_or_commit": "write the scanned cell and move the head atomically",
        "result_kind": "one successor machine configuration",
        "successor_cardinality": "one successor per covered state/color case",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "no native halt condition is supplied",
        "witness_semantics": None,
        "parameters_and_variants": "state count, tape colors, displacement convention, and rule table",
        "excluded_observers_and_representations": "head-path plots are histories, not transition laws",
        "evidence_limit": "icon semantics and external main-text rules are not inferred beyond the assigned evidence",
    },
    "SUB": {
        "object_kind": "substitution-system construction",
        "native_time": "discrete replacement rounds",
        "carrier": "an array or geometrical assembly of typed pieces",
        "support": "all current pieces or array elements",
        "topology": "the stated array nesting or geometric incidence",
        "structural_invariants": "replacement preserves the assembly convention stated by the construction",
        "alphabet_or_value_schema": "finite element or shape labels",
        "complete_state": "the complete current array or geometric assembly",
        "visible_history": None,
        "control_state": None,
        "seed": "the stated initial element or assembly",
        "input": None,
        "boundary": None,
        "external_data": None,
        "frontier_or_activation": "all replaceable elements",
        "schedule": "parallel replacement round",
        "read_dependencies_or_neighborhood": "the replaced element, or its stated neighborhood for neighbor-dependent variants",
        "law_kind": "structural replacement rule",
        "rule_relation_constraint_function_or_probability_law": "replace each matched element or block by its stated assembly",
        "write_replacement_assembly_or_commit": "assemble and flatten the replacement blocks consistently",
        "result_kind": "a successor array or geometric assembly",
        "successor_cardinality": "one successor for a deterministic replacement set",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "iterate for a requested number of rounds",
        "witness_semantics": None,
        "parameters_and_variants": "replacement set, dimension, shapes, orientations, and seed",
        "excluded_observers_and_representations": "digit evaluators, stacked renderings, and alternate encodings are not native replacement laws",
        "evidence_limit": "unlabelled external panel rules are left unresolved",
    },
    "NETWORK": {
        "object_kind": "network-rewriting construction",
        "native_time": "discrete network updates",
        "carrier": "nodes with directed above/below connections",
        "support": "the current reachable network",
        "topology": "a directed graph with two outgoing connections per represented node",
        "structural_invariants": "node identity is retained except where rules insert or disconnected-node removal deletes nodes",
        "alphabet_or_value_schema": "node identifiers and connection labels",
        "complete_state": "network connectivity and any active-node designation",
        "visible_history": None,
        "control_state": "an active node only for sequential variants",
        "seed": "an initial network",
        "input": None,
        "boundary": None,
        "external_data": None,
        "frontier_or_activation": "all nodes in parallel variants or one active node in sequential variants",
        "schedule": "parallel or single-active-node schedule as stated",
        "read_dependencies_or_neighborhood": "bounded connection-following structure around each updated node",
        "law_kind": "local connection-rerouting and optional node-insertion rule",
        "rule_relation_constraint_function_or_probability_law": "match local neighbor counts and replace outgoing connections",
        "write_replacement_assembly_or_commit": "reroute connections, append new nodes, then remove unreachable nodes when specified",
        "result_kind": "a successor network and, when applicable, active node",
        "successor_cardinality": "one successor for a fixed deterministic rule",
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "iteration may continue or the active node may become trapped",
        "witness_semantics": None,
        "parameters_and_variants": "lookup depth, rewrite table, initial network, and schedule",
        "excluded_observers_and_representations": "layered drawings and node-count/dimension plots are not update laws",
        "evidence_limit": "undirected and externally routed rules remain incomplete",
    },
    "MULTI": {
        "object_kind": "multiway rewriting construction",
        "native_time": "discrete branching replacement steps",
        "carrier": "a set of strings, arrays, or numbers",
        "support": "all states present at the current step",
        "topology": "replacement occurrences within each state",
        "structural_invariants": "equal successor states merge by set union",
        "alphabet_or_value_schema": "the stated symbols, blocks, or numeric domain",
        "complete_state": "the deduplicated set of current states",
        "visible_history": None,
        "control_state": None,
        "seed": "the stated initial state set",
        "input": None,
        "boundary": None,
        "external_data": None,
        "frontier_or_activation": "every applicable match in every current state",
        "schedule": "one global replacement layer per step",
        "read_dependencies_or_neighborhood": "each left-hand-side match",
        "law_kind": "nondeterministic replacement rule",
        "rule_relation_constraint_function_or_probability_law": "enumerate every single applicable replacement outcome",
        "write_replacement_assembly_or_commit": "union and deduplicate the resulting states; drop states with no match where stated",
        "result_kind": "a successor set of states",
        "successor_cardinality": "zero, one, or many distinct successors",
        "determinism_branching_or_measure": "branching is exhaustively retained rather than sampled",
        "termination_completion_failure": "a branch fails when no rule applies; the whole layer may become empty",
        "witness_semantics": "each retained state witnesses a reachable replacement history",
        "parameters_and_variants": "rule set, seed, domain, sorting restriction, and cyclic boundary option",
        "excluded_observers_and_representations": "stacked plots and reachability diagrams are not replacement rules",
        "evidence_limit": "multiplicity of distinct derivations is intentionally erased by set union",
    },
    "GRAMMAR": {
        "object_kind": "generative-grammar construction",
        "native_time": "discrete derivation steps",
        "carrier": "strings containing terminal and nonterminal symbols",
        "support": "all currently derivable sentential forms",
        "topology": "substring occurrence and replacement",
        "structural_invariants": "the stated grammar-class restriction on rule sides",
        "alphabet_or_value_schema": "terminal and nonterminal symbols",
        "complete_state": "a current sentential form or the set of derivable forms",
        "visible_history": None,
        "control_state": None,
        "seed": "the start symbol or start string",
        "input": None,
        "boundary": None,
        "external_data": None,
        "frontier_or_activation": "all applicable nonterminal/rewrite occurrences",
        "schedule": "all derivations may be followed",
        "read_dependencies_or_neighborhood": "the rule's left-hand side",
        "law_kind": "formal string-replacement grammar",
        "rule_relation_constraint_function_or_probability_law": "replace an allowed left side by an allowed right side",
        "write_replacement_assembly_or_commit": "form each resulting string",
        "result_kind": "the generated formal language",
        "successor_cardinality": "zero, one, or many derivations",
        "determinism_branching_or_measure": "nondeterministic exhaustive generation",
        "termination_completion_failure": "a final expression contains no nonterminal symbol",
        "witness_semantics": "a derivation witnesses membership in the generated language",
        "parameters_and_variants": "grammar class, productions, terminals, nonterminals, and start symbol",
        "excluded_observers_and_representations": "recognizers and stack implementations are not the grammar's generation law",
        "evidence_limit": "only the stated Chomsky-class restrictions and examples are claimed",
    },
    "CONSTRAINT": {
        "object_kind": "declarative relation or constraint system",
        "native_time": None,
        "carrier": "the stated assignment, sequence, array, tiling, or numerical domain",
        "support": "the variables or positions constrained by the relation",
        "topology": "the overlap, adjacency, incidence, or variable relation stated by the constraint",
        "structural_invariants": "accepted objects must satisfy every stated relation",
        "alphabet_or_value_schema": "the stated colors, symbols, tiles, spins, integers, or numbers",
        "complete_state": "a complete candidate assignment or object",
        "visible_history": None,
        "control_state": None,
        "seed": None,
        "input": "the relation and any boundary, initial, or parameter data",
        "boundary": "boundary or initial data only where stated",
        "external_data": None,
        "frontier_or_activation": None,
        "schedule": None,
        "read_dependencies_or_neighborhood": "the variables or local templates named by the relation",
        "law_kind": "declarative relation/constraint",
        "rule_relation_constraint_function_or_probability_law": "accept exactly objects satisfying the stated relation",
        "write_replacement_assembly_or_commit": None,
        "result_kind": "the model/solution set or accepted-result judgment",
        "successor_cardinality": None,
        "determinism_branching_or_measure": "the solution set can contain zero, one, or many objects",
        "termination_completion_failure": None,
        "witness_semantics": "a satisfying assignment is a witness; unsatisfiability may lack a bounded finite witness",
        "parameters_and_variants": "the relation's coefficients, templates, domain, and boundary/initial data",
        "excluded_observers_and_representations": "search procedures and plots of solutions are not the declarative law",
        "evidence_limit": "solution methods and externally referenced definitions are not inferred",
    },
    "SOLVER": {
        "object_kind": "constraint-search or enumeration procedure",
        "native_time": "algorithmic search steps",
        "carrier": "partial assignments and a search/backtracking state",
        "support": "the currently built finite region or path",
        "topology": "the stated extension order and dependency graph",
        "structural_invariants": "every retained partial assignment satisfies all currently checkable constraints",
        "alphabet_or_value_schema": "the constrained system's value alphabet",
        "complete_state": "partial assignment, choice stack, memoized facts, and current position",
        "visible_history": None,
        "control_state": "current extension point and backtracking choices",
        "seed": "a small satisfying region or start node",
        "input": "a constraint specification",
        "boundary": "the requested finite region or infinite-extension target",
        "external_data": None,
        "frontier_or_activation": "the next position or path edge to extend",
        "schedule": "the stated spiral/path order with backtracking",
        "read_dependencies_or_neighborhood": "constraints affected by the latest choice",
        "law_kind": "search, checking, and backtracking procedure",
        "rule_relation_constraint_function_or_probability_law": "extend consistent assignments, branch on choices, and backtrack on inconsistency",
        "write_replacement_assembly_or_commit": "commit a choice provisionally and retract it on backtracking",
        "result_kind": "a satisfying witness, a finite failure, or continuing search",
        "successor_cardinality": "one or more search branches",
        "determinism_branching_or_measure": "deterministic under the stated choice ordering",
        "termination_completion_failure": "may not terminate for an infinite unsatisfiable target",
        "witness_semantics": "a completed assignment/path witnesses satisfiability",
        "parameters_and_variants": "constraint, extension order, heuristics, and target region",
        "excluded_observers_and_representations": "rendering a witness is not part of the solver",
        "evidence_limit": "the prose specifies procedure structure but not executable pseudocode for every heuristic",
    },
    "GAME": {
        "object_kind": "finite-configuration game system",
        "native_time": "alternating player moves",
        "carrier": "a tuple of pile heights",
        "support": "the k piles",
        "topology": "one move changes exactly one pile",
        "structural_invariants": "pile heights remain nonnegative integers",
        "alphabet_or_value_schema": "whole-number pile heights and player-to-move",
        "complete_state": "pile heights and whose turn it is",
        "visible_history": None,
        "control_state": "player to move",
        "seed": "initial pile heights",
        "input": None,
        "boundary": None,
        "external_data": None,
        "frontier_or_activation": "one chosen pile",
        "schedule": "players alternate",
        "read_dependencies_or_neighborhood": "all pile heights determine legal choices and winning status",
        "law_kind": "legal-move and terminal/winner rule",
        "rule_relation_constraint_function_or_probability_law": "remove any positive number of objects from one pile",
        "write_replacement_assembly_or_commit": "decrease the chosen pile",
        "result_kind": "a successor game position",
        "successor_cardinality": "one successor per legal move; generally many legal moves",
        "determinism_branching_or_measure": "players choose branches adversarially",
        "termination_completion_failure": "the player taking the last object wins",
        "witness_semantics": "BitXor of heights equal to zero characterizes the stated losing-position strategy",
        "parameters_and_variants": "pile count, initial heights, and allowed removal amounts",
        "excluded_observers_and_representations": "the game graph is a representation of positions and moves",
        "evidence_limit": "only normal-play nim and stated variants are covered",
    },
    "FUNCTION": {
        "object_kind": "immutable function or explicit witness construction",
        "native_time": None,
        "carrier": "the stated numerical or coordinate domain",
        "support": "the function's complete input domain",
        "topology": "coordinate or index relations fixed by the formula",
        "structural_invariants": "equal inputs have equal outputs",
        "alphabet_or_value_schema": "the stated integer, real, complex, or array values",
        "complete_state": "an input value",
        "visible_history": None,
        "control_state": None,
        "seed": None,
        "input": "the stated function arguments",
        "boundary": None,
        "external_data": None,
        "frontier_or_activation": None,
        "schedule": None,
        "read_dependencies_or_neighborhood": "the stated function arguments",
        "law_kind": "immutable function",
        "rule_relation_constraint_function_or_probability_law": "evaluate the explicit piecewise or closed formula",
        "write_replacement_assembly_or_commit": None,
        "result_kind": "the function value or explicitly generated witness",
        "successor_cardinality": None,
        "determinism_branching_or_measure": "deterministic",
        "termination_completion_failure": "defined on the stated domain",
        "witness_semantics": "the produced object witnesses the associated claim where stated",
        "parameters_and_variants": "the formula's stated parameters and coordinate-origin freedom",
        "excluded_observers_and_representations": "uses as a scan, drawing, or alternate encoding remain distinguished from the function itself",
        "evidence_limit": "only the explicit formula and stated domain are claimed",
    },
}


def add_spec(
    specs: list[dict[str, Any]],
    name: str,
    profile: str,
    anchor: tuple[str, str],
    evidence: list[dict[str, Any]],
    *,
    aliases: list[str] | None = None,
    params: list[tuple[str, str]] | None = None,
    variants: list[tuple[str, str]] | None = None,
    missing: list[str] | None = None,
    uncertainty: list[str] | None = None,
    overrides: dict[str, str | None] | None = None,
    source_status: list[str] | None = None,
) -> None:
    specs.append(
        {
            "name": name,
            "profile": profile,
            "anchor": anchor,
            "evidence": evidence,
            "aliases": aliases or [],
            "params": params or [],
            "variants": variants or [],
            "missing": missing or [],
            "uncertainty": uncertainty or [],
            "overrides": overrides or {},
            "source_status": source_status or ["CLEAR"],
        }
    )


def candidate_specs() -> list[dict[str, Any]]:
    s: list[dict[str, Any]] = []
    add = lambda *a, **k: add_spec(s, *a, **k)

    add("two-dimensional 5-neighbor cellular automaton", "CA", ("SOURCE_UNIT", "U006082"),
        [ev("U006082", "The Notes identify the 5-neighbor 2D rule family."),
         ev("U006083", "ListConvolve encodes center weight 1 and four axial neighbors weight 2, followed by the rule lookup.", modality="CODE"),
         ev("U006084", "A ten-digit binary code supplies the outer-totalistic lookup.", modality="PROSE")],
        params=[("code", "binary rule code"), ("neighborhood", "center plus four axial neighbors")])
    add("two-dimensional 9-neighbor cellular automaton", "CA", ("SOURCE_UNIT", "U006085"),
        [ev("U006085", "The Notes identify the 9-neighbor 2D rule family."),
         ev("U006086", "ListConvolve encodes the center and all eight surrounding cells before rule lookup.", modality="CODE"),
         ev("U006087", "An eighteen-digit binary code supplies the outer-totalistic lookup.")],
        params=[("code", "binary rule code"), ("neighborhood", "3 by 3 Moore neighborhood")])
    add("d-dimensional axial-neighbor cellular automaton", "CA", ("SOURCE_UNIT", "U006088"),
        [ev("U006088", "The 5-neighbor family is generalized to 2d+1 axial neighbors and k colors."),
         ev("U006089", "CAStep and AxesTotal state the complete axial aggregation/update computation.", modality="CODE"),
         ev("U006090", "The base-k rule-code length is stated.")],
        params=[("d", "dimension"), ("k", "number of colors"), ("code", "base-k rule code")])
    add("d-dimensional full 3^d-neighbor cellular automaton", "CA", ("SOURCE_UNIT", "U006091"),
        [ev("U006091", "The 9-neighbor family is generalized to the full 3^d block."),
         ev("U006092", "CAStep and FullTotal state the complete full-block aggregation/update computation.", modality="CODE"),
         ev("U006093", "The base-k rule-code length is stated.")],
        params=[("d", "dimension"), ("k", "number of colors"), ("code", "base-k rule code")])
    add("arbitrary-offset general cellular automaton", "CA", ("SOURCE_UNIT", "U006096"),
        [ev("U006096", "An ordered offset list specifies an arbitrary neighborhood in any dimension."),
         ev("U006098", "The rule-number convention and neighborhood-to-color denotation are stated."),
         ev("U006099", "The first general step implementation is explicit.", modality="CODE"),
         ev("U006101", "An equivalent ListCorrelate implementation is explicit.", modality="CODE")],
        params=[("offset list", "ordered relative cell coordinates"), ("k", "colors"), ("num", "rule number")])
    add("two-dimensional outer-totalistic cellular-automaton family", "CA", ("SOURCE_UNIT", "U006102"),
        [ev("U006102", "Outer-totalistic rules depend on neighbor total and center color."),
         ev("U006103", "The black-neighbor trigger list is mapped to an outer-totalistic code."),
         ev("U006104", "The exact code formula is supplied.", modality="CODE")],
        params=[("trigger list", "neighbor counts that turn the cell black"), ("center color", "separate center-cell input")])
    add("two-dimensional totalistic cellular-automaton family", "CA", ("SOURCE_UNIT", "U006102"),
        [ev("U006102", "Totalistic rules are independently delimited as depending only on the total black-cell count."),
         ev("U006105", "The table enumerates totalistic family sizes for three 2D neighborhoods.", modality="TABLE")],
        params=[("neighborhood", "5-neighbor square, 9-neighbor square, or hexagonal")])
    add("two-dimensional growth-totalistic cellular-automaton family", "CA", ("SOURCE_UNIT", "U006102"),
        [ev("U006102", "Growth totalistic rules keep every black cell black forever."),
         ev("U006110", "A cell becomes black for specified exact neighbor counts; a code formula and minimal growth seeds are stated.")],
        params=[("neighbor-count set", "exact counts causing black"), ("seed", "minimal black-cell seed for growth")],
        overrides={"structural_invariants": "black cells are persistent once created"})
    add("completely symmetric 5-neighbor cellular-automaton family", "CA", ("SOURCE_UNIT", "U006106"),
        [ev("U006106", "The 32 neighborhoods are partitioned into twelve symmetry classes."),
         ev("U006107", "The exact twelve equivalence classes are listed.", modality="CODE"),
         ev("U006108", "Twelve binary digits number rules 0 through 4095."),
         ev("U006109", "The conversion to the general rule code is explicit.", modality="CODE")],
        params=[("symmetric code", "12-bit rule number")])

    growth_presets = [
        ("exact-neighbor growth rule {1}", "{1}"),
        ("exact-neighbor growth rule {1,2}", "{1,2}"),
        ("exact-neighbor growth rule {1,3}", "{1,3}"),
        ("exact-neighbor growth rule {1,4}", "{1,4}"),
        ("exact-neighbor growth rule {1,3,4}", "{1,3,4}"),
    ]
    for name, label in growth_presets:
        add(name, "CA", ("IMAGE", "A000520"),
            [ev("U006110", f"The growth-rule law makes a cell black exactly for the displayed neighbor-count set {label}."),
             ev("U006111", f"The composite labels the preset {label} and shows its growth.", modality="IMAGE",
                image="BACK-MATTER/NOTES/_page_943_Growth_Rules_Five_Panel_Row.jpeg",
                strength="DIRECT_PARTIAL_MECHANICS")],
            params=[("neighbor-count set", label)],
            overrides={"structural_invariants": "black cells remain black once created"})

    add("Ulam history-dependent two-dimensional growth system", "CA", ("SOURCE_UNIT", "U006114"),
        [ev("U006114", "The Notes identify Ulam's system and describe its historical construction."),
         ev("U006115", "UStep with p, q, and r supplies the explicit history-dependent growth computation.", modality="CODE"),
         ev("U006116", "Steps 1 through 10 and 50 show the state history.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_943_Picture_21.jpeg", strength="CORROBORATING")],
        overrides={"complete_state": "the accumulated black positions plus the retained prior-step/history data",
                   "schedule": "one global history-dependent growth step",
                   "read_dependencies_or_neighborhood": "the current candidate positions, prior growth set, and four axial offsets",
                   "structural_invariants": "black positions accumulate while auxiliary history is retained"})
    add("Ulam component subrule ablation", "CA", ("SOURCE_UNIT", "U006117"),
        [ev("U006117", "The prose claims that an undefined component “s alone” yields outer-totalistic code 686 and rule 90.", strength="DEFECT_LIMITED"),
         ev("U006118", "The image instead labels only r[], q[], p[], p[q[]], and p[q[r[]]].", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_944_Simple_Rules_Five_Panel_Row.jpeg", strength="DEFECT_LIMITED")],
        missing=["Whether the prose's “s alone” means the defined r component cannot be resolved from the assigned canonical source."],
        uncertainty=["Prose says “s alone”, while the implementation defines only p, q, and r and the image labels r/q/p compositions."],
        source_status=["CONFLICTING"],
        overrides={"rule_relation_constraint_function_or_probability_law": None,
                   "parameters_and_variants": "r, q, p, and their displayed compositions; prose conflicts on “s”",
                   "evidence_limit": "the source conflict prevents identifying which isolated component is asserted to equal code 686/rule 90"})
    add("outer-totalistic cellular automaton code 12", "CA", ("SOURCE_UNIT", "U006119"),
        [ev("U006119", "Outer-totalistic code 12 is identified as Ulam's pure 2D cellular automaton."),
         ev("U006120", "The image varies square-block seeds from 1x1 through 10x10.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_944_Picture_9.jpeg", strength="CORROBORATING")],
        params=[("code", "12"), ("seed", "square blocks of sizes 1x1 through 10x10")])
    add("three-dimensional exact-3-of-26 growth cellular automaton", "CA", ("SOURCE_UNIT", "U006123"),
        [ev("U006123", "A 3D rule turns a cell black when exactly 3 of its 26 neighbors were black; two seeds are stated."),
         ev("U006124", "Panels (c) and (d) project the two seed variants.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_944_3D_Projections_Four_Panel_Row.jpeg", strength="CORROBORATING")],
        variants=[("3x1x1 seed", "panel c"), ("3x3x1 seed", "panel d")],
        overrides={"topology": "three-dimensional cubic lattice with 26 surrounding neighbors",
                   "read_dependencies_or_neighborhood": "all 26 cells surrounding the updated cell"})
    add("homogeneous-geometry cellular automaton carrier family", "CA", ("SOURCE_UNIT", "U006125"),
        [ev("U006125", "The carrier may be any geometry with finitely many cell types and uniform neighborhoods."),
         ev("U006126", "Voronoi adjacency rather than metric embedding determines nearest-neighbor topology."),
         ev("U006127", "The image directly depicts five admissible regular 3D Voronoi/lattice carrier geometries.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_945_Picture_2.jpeg")],
        overrides={"carrier": "a homogeneous lattice or tiling with finitely many cell types",
                   "topology": "adjacency determined by cell incidence/Voronoi neighbors"})
    add("cellular automaton on a congruent pentagonal tiling", "CA", ("SOURCE_UNIT", "U006128"),
        [ev("U006128", "Congruent pentagons with varying orientations carry outer-totalistic rules; code 4094 is specified."),
         ev("U006129", "The image supplies the pentagonal adjacency carrier, evolution, and six labeled code examples.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_945_Picture_4.jpeg")],
        params=[("carrier", "congruent pentagonal tiling"), ("code", "outer-totalistic code")],
        overrides={"topology": "pentagonal-tile edge adjacency with five neighbors"})
    for code in ["38", "564", "700", "966", "2990", "4094"]:
        add(f"pentagonal-tiling outer-totalistic code {code}", "CA", ("IMAGE", "A000544"),
            [ev("U006128", "The surrounding prose fixes the pentagonal carrier and outer-totalistic code convention."),
             ev("U006129", f"The image independently labels pentagonal-tiling preset code {code}.", modality="IMAGE",
                image="BACK-MATTER/NOTES/_page_945_Picture_4.jpeg")],
            params=[("code", code), ("carrier", "congruent pentagonal tiling")],
            overrides={"topology": "pentagonal-tile edge adjacency with five neighbors"})
    add("cellular automaton on a nested Penrose tiling", "CA", ("SOURCE_UNIT", "U006130"),
        [ev("U006130", "Two Penrose tile shapes are treated alike by an outer-totalistic cellular-automaton rule; code 254 is specified."),
         ev("U006131", "The image supplies the nonrepetitive carrier, evolution, and six labeled code examples.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_945_Picture_6.jpeg")],
        params=[("carrier", "nested Penrose tiling"), ("code", "outer-totalistic code")],
        overrides={"topology": "edge adjacency on a two-shape nested Penrose tiling"})
    for code in ["22", "54", "174", "214", "220", "254"]:
        add(f"Penrose-tiling outer-totalistic code {code}", "CA", ("IMAGE", "A000545"),
            [ev("U006130", "The surrounding prose fixes the Penrose carrier and outer-totalistic code convention."),
             ev("U006131", f"The image independently labels Penrose-tiling preset code {code}.", modality="IMAGE",
                image="BACK-MATTER/NOTES/_page_945_Picture_6.jpeg")],
            params=[("code", code), ("carrier", "nested Penrose tiling")],
            overrides={"topology": "edge adjacency on a two-shape nested Penrose tiling"})
    add("cellular automaton on a homogeneous network", "CA", ("SOURCE_UNIT", "U006132"),
        [ev("U006132", "Cells may be graph nodes; nearest-neighbor rules need uniform degree and unlabelled edges restrict rules to totalistic ones."),
         ev("U006236", "Arbitrary network nodes receive colors updated from the colors at connected nodes."),
         ev("U006237", "NetCAStep states the explicit connection-indexed update.", modality="CODE")],
        overrides={"carrier": "nodes of a homogeneous or arbitrary network",
                   "topology": "network connections define cell neighborhoods",
                   "read_dependencies_or_neighborhood": "colors of nodes reached by the current node's connections"})

    add("two-dimensional Turing machine", "TM", ("SOURCE_UNIT", "U006134"),
        [ev("U006134", "A rule maps head state and scanned color to new state, new color, and a 2D displacement."),
         ev("U006135", "TM2DStep reads, writes, and moves atomically.", modality="CODE")])
    add("Langton's ant", "TM", ("SOURCE_UNIT", "U006136"),
        [ev("U006136", "The historical passage introduces a specific four-state two-color turning rule."),
         ev("U006137", "The complete state/color transition formula writes the complement and moves in the new complex direction.", modality="CODE"),
         ev("U006138", "The rule is directly named Langton's ant.")],
        aliases=["Langton ant"])
    add("pictographic 3-state two-dimensional Turing-machine rule", "TM", ("IMAGE", "A000547"),
        [ev("U006141", "The prose identifies the displayed object as a 3-state 2D Turing-machine rule."),
         ev("U006142", "The six-case pictographic strip supplies one case for every three-state/two-color input.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_946_Turing_3_State_Rule_Strip.jpeg",
            strength="DIRECT_COMPLETE_MECHANICS")],
        params=[("head states", "3 pictographic directions"), ("tape colors", "2")])
    add("turn-relative two-dimensional Turing machine", "TM", ("SOURCE_UNIT", "U006143"),
        [ev("U006143", "The rule specifies turns relative to the current motion rather than fixed-grid displacements.")],
        missing=["The assigned Notes do not give a complete turn table for a concrete rule."])
    add("two-dimensional mobile automaton", "TM", ("SOURCE_UNIT", "U006143"),
        [ev("U006143", "The Notes delimit the 2D mobile-automaton family, its four-neighbor simplest case, k colors, and rule-count formula.")],
        missing=["A concrete two-dimensional mobile-automaton transition table is not supplied."],
        overrides={"object_kind": "two-dimensional mobile-automaton construction",
                   "control_state": "the single active cell/location",
                   "frontier_or_activation": "one active location",
                   "read_dependencies_or_neighborhood": "the active cell and four neighbors in the simplest case",
                   "write_replacement_assembly_or_commit": "the exact writable region is not fixed by this note"})

    add("two-dimensional block substitution system", "SUB", ("SOURCE_UNIT", "U006145"),
        [ev("U006145", "A two-color 2D block-replacement rule and one-cell seed are explicit."),
         ev("U006146", "SS2DEvolve performs parallel replacement and two-dimensional flattening.", modality="CODE")])
    add("non-white-background two-dimensional substitution-system family", "SUB", ("SOURCE_UNIT", "U006168"),
        [ev("U006168", "White elements are replaced by blocks that themselves contain black elements."),
         ev("U006169", "The image shows the resulting histories but does not isolate the panel rules.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_947_Figure_4.jpeg", strength="CONTEXTUAL")],
        missing=["Exact replacement tables for the displayed panels are outside the assigned Notes."])
    add("d-dimensional array substitution system", "SUB", ("SOURCE_UNIT", "U006170"),
        [ev("U006170", "A d-dimensional state is a depth-d nested list."),
         ev("U006171", "SSEvolve and FlattenArray state the d-dimensional replacement/assembly law.", modality="CODE")],
        params=[("d", "dimension"), ("rule", "element-to-depth-d-array replacements")])
    add("three-dimensional two-color substitution preset", "SUB", ("SOURCE_UNIT", "U006172"),
        [ev("U006172", "The construction is identified as the 3D analog of the 2D rule."),
         ev("U006173", "The exact two replacement arrays are given.", modality="CODE"),
         ev("U006174", "At least d+1 black replacements are required to avoid confinement to a hyperplane.")],
        params=[("dimension", "3"), ("colors", "2")])
    add("square-and-golden-rectangle geometric substitution", "SUB", ("SOURCE_UNIT", "U006175"),
        [ev("U006175", "Substitution systems are extended from squares to other geometric figures."),
         ev("U006176", "The image shows direct shape subdivision/replacement histories.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_947_Picture_10.jpeg"),
         ev("U006177", "The second system's square/GoldenRatio shapes, orientation labels, exact equal-square rule, and seed are stated.")],
        overrides={"carrier": "a square and a GoldenRatio-aspect rectangle with orientation types",
                   "alphabet_or_value_schema": "four labels encode shape and orientation"})
    add("Penrose triangular substitution system", "SUB", ("SOURCE_UNIT", "U006178"),
        [ev("U006178", "The nested Penrose triangular subdivision is identified."),
         ev("U006179", "Successive subdivisions directly show structural replacement.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_947_Picture_14.jpeg"),
         ev("U006180", "The arrangement at step t is explicitly attributed to a substitution system."),
         ev("U006181", "The complete a/b triangle replacement computation is given.", modality="CODE")],
        params=[("scale", "GoldenRatio"), ("seed", "the stated initial triangle")])
    add("dragon-curve geometric substitution", "SUB", ("SOURCE_UNIT", "U006184"),
        [ev("U006184", "The Dragon curve is independently identified and its dimension stated."),
         ev("U006185", "Its complex-map replacement law and seed representation are explicit.")],
        params=[("map", "1/2 (1-I){z+1/2,z-1/2}"), ("seed", "{0}")])
    add("page-190 geometric substitution map", "SUB", ("SOURCE_UNIT", "U006185"),
        [ev("U006185", "The page-190 system is independently assigned f[z]=1/2(1-I){Iz+1/2,z-1/2}.")],
        params=[("map", "1/2 (1-I){I z+1/2,z-1/2}")])
    for label, formula in [
        ("page-191 geometric substitution (a)", "(0.296-0.57 I) z -0.067 I - I {1.04,0.237}"),
        ("page-191 geometric substitution (b)", "1/40 {17(Sqrt[3]-I)z,-24+14z}"),
        ("Koch-curve geometric substitution (page-191 c)", "the third explicit complex affine pair"),
    ]:
        add(label, "SUB", ("SOURCE_UNIT", "U006185"),
            [ev("U006185", f"The prose independently maps panel labels (a), (b), and (c) to the following ordered formulas; {label} is delimited."),
             ev("U006186", f"The formula block supplies {formula}.", modality="CODE")],
            params=[("replacement map", formula)])
    add("affine iterated transformation system", "SUB", ("SOURCE_UNIT", "U006192"),
        [ev("U006192", "A set of affine maps multiplies each point vector by a fixed matrix then adds a fixed vector, in any dimension.")],
        overrides={"carrier": "points/vectors in a stated dimension",
                   "alphabet_or_value_schema": "real vectors and affine maps",
                   "read_dependencies_or_neighborhood": "each current point independently"})
    add("Möbius iterated transformation system", "SUB", ("SOURCE_UNIT", "U006193"),
        [ev("U006193", "Sets of maps z -> (az+b)/(cz+d) are independently stated to yield nested patterns.")],
        params=[("a,b,c,d", "complex transformation coefficients")],
        overrides={"carrier": "complex points", "alphabet_or_value_schema": "complex numbers"})
    add("inverse-square-root Julia-set generator", "SUB", ("SOURCE_UNIT", "U006193"),
        [ev("U006193", "The branching map z -> {Sqrt[z-c],-Sqrt[z-c]} is explicitly identified as generating Julia sets for many c."),
         ev("U006198", "The map is iterated from z=0 over an array of c values.")],
        params=[("c", "complex parameter"), ("seed", "z=0")],
        overrides={"carrier": "finite sets of complex points",
                   "alphabet_or_value_schema": "complex numbers",
                   "successor_cardinality": "two image points per current point before set merging",
                   "determinism_branching_or_measure": "exhaustive two-branch inverse iteration"})
    add("Mandelbrot-set bounded-orbit relation", "CONSTRAINT", ("SOURCE_UNIT", "U006198"),
        [ev("U006198", "The surrounding Julia construction provides the c-parameter context."),
         ev("U006200", "The Mandelbrot set is defined both by Julia connectedness and equivalently bounded iteration of z -> z^2+c from z=0.")],
        params=[("c", "complex parameter"), ("seed", "z=0")],
        overrides={"carrier": "complex parameter c and the orbit of z=0",
                   "topology": "connectedness of the corresponding Julia set, equivalently orbit boundedness",
                   "rule_relation_constraint_function_or_probability_law": "accept c exactly when z=0 under z -> z^2+c remains bounded"})
    add("neighbor-dependent two-dimensional substitution system", "SUB", ("SOURCE_UNIT", "U006205"),
        [ev("U006205", "A replacement is selected by a 2x2 neighborhood pattern."),
         ev("U006206", "Partition, rule replacement, and Flatten2D state one evolution step.", modality="CODE"),
         ev("U006207", "Mixed subdivision/no-subdivision variants can have unboundedly many neighborhood configurations.")],
        overrides={"read_dependencies_or_neighborhood": "overlapping 2x2 blocks in the stated example",
                   "write_replacement_assembly_or_commit": "replace matched blocks and flatten the resulting 2D assembly"})
    add("square-spiral enumeration of the integer grid", "FUNCTION", ("SOURCE_UNIT", "U006208"),
        [ev("U006208", "The function is independently delimited as a whole-grid scan reaching one 2D position at each step t."),
         ev("U006209", "The exact t-to-coordinate formula is given.", modality="CODE")],
        params=[("t", "nonnegative scan step")],
        overrides={"carrier": "integer step indices and 2D integer coordinates",
                   "result_kind": "one integer-grid coordinate"})

    add("parallel directed network system", "NETWORK", ("SOURCE_UNIT", "U006211"),
        [ev("U006211", "Networks are lists of above/below destinations; one-node and cyclic seeds are defined."),
         ev("U006214", "Follow resolves labelled connection paths.", modality="CODE"),
         ev("U006216", "NeighborNumbers defines bounded local structure.", modality="CODE"),
         ev("U006217", "Rules reroute connections and can insert nodes."),
         ev("U006218", "NetEvolveStep states parallel local rewriting and node insertion.", modality="CODE"),
         ev("U006224", "NetEvolveList applies rules and removes nodes unreachable from node 1.", modality="CODE")])
    add("undirected network rewriting system", "NETWORK", ("SOURCE_UNIT", "U006226"),
        [ev("U006226", "Undirected-connection networks are independently delimited, but their update rules are routed to Chapter 9.")],
        missing=["The assigned Notes do not state the undirected-network rewrite/commit law."],
        overrides={"topology": "undirected graph connections",
                   "alphabet_or_value_schema": "nodes and undirected edges",
                   "rule_relation_constraint_function_or_probability_law": "unknown from this source"})
    add("sequential directed network system", "NETWORK", ("SOURCE_UNIT", "U006229"),
        [ev("U006229", "Exactly one active node is updated; it moves along labelled connections according to local structure."),
         ev("U006230", "Layered graphs preserve node/edge identity and show the thick active trajectory.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_951_Sequential_Networks_Three_Panel_Row.jpeg"),
         ev("U006231", "The final displayed system and active-node trapping are identified."),
         ev("U006232", "A complete six-case local rewrite/move rule is given.", modality="CODE")],
        overrides={"frontier_or_activation": "one active node",
                   "schedule": "one active-node rewrite and move per step",
                   "complete_state": "directed network plus active node"})
    add("random Boolean network", "CA", ("SOURCE_UNIT", "U006238"),
        [ev("U006238", "Each node receives a rule randomly chosen from all 2^(2^s) Boolean rules with s inputs, then evolves like a network cellular automaton.")],
        overrides={"alphabet_or_value_schema": "Boolean node colors",
                   "topology": "a fixed input network with s inputs per node",
                   "parameters_and_variants": "input count s, network, and one randomly drawn Boolean rule per node",
                   "external_data": "random rule assignment at setup",
                   "determinism_branching_or_measure": "randomly instantiated, then deterministic for the fixed sampled rules"})

    add("string multiway system", "MULTI", ("SOURCE_UNIT", "U006240"),
        [ev("U006240", "A layer is a list of strings and the rule set is a list of string replacements."),
         ev("U006241", "An explicit two-rule example is supplied.", modality="CODE"),
         ev("U006243", "MWStep enumerates every match, unions duplicate strings, and MWEvolveList iterates layers.", modality="CODE"),
         ev("U006247", "ReplaceList supplies an equivalent list-based implementation.", modality="CODE"),
         ev("U006250", "States with no applicable replacement are explicitly dropped.")])
    add("page-206 three-rule multiway preset", "MULTI", ("SOURCE_UNIT", "U006248"),
        [ev("U006248", "The page-206 case is independently identified."),
         ev("U006249", "The three exact string replacements are listed.", modality="CODE"),
         ev("U006250", "The seed ABABAB and branch-drop behavior are stated.")],
        params=[("seed", "ABABAB")])
    add("sorted-count multiway system", "MULTI", ("SOURCE_UNIT", "U006253"),
        [ev("U006253", "Sorted strings are represented by symbol counts and rules by difference vectors."),
         ev("U006254", "The step adds every difference vector, unions results, and removes negative counts.", modality="CODE")],
        overrides={"carrier": "nonnegative integer count vectors",
                   "alphabet_or_value_schema": "one nonnegative count per sorted symbol",
                   "read_dependencies_or_neighborhood": "the whole count vector"})
    add("semigroup bidirectional rewrite system", "MULTI", ("SOURCE_UNIT", "U006261"),
        [ev("U006261", "A semigroup representation requires each rewrite rule and its reverse; concatenation is the operation and the empty string is identity.")],
        overrides={"structural_invariants": "rewrite reachability defines equivalence classes of strings",
                   "result_kind": "equivalence classes/elements and their rewrite graph"})
    add("group inverse-symbol bidirectional rewrite system", "MULTI", ("SOURCE_UNIT", "U006261"),
        [ev("U006261", "A group representation adds inverse symbol pairs and cancellation rules in both directions.")],
        overrides={"alphabet_or_value_schema": "generators paired with inverse symbols",
                   "structural_invariants": "bidirectional relations and inverse cancellations define group elements"})
    grammar_evidence = {
        "regular generative grammar": ("U006268", "one nonterminal on the left and at most one on the right"),
        "context-free generative grammar": ("U006269", "one nonterminal on the left and unrestricted multiple nonterminals on the right"),
        "context-sensitive generative grammar": ("U006270", "left side no longer than right side"),
        "unrestricted generative grammar": ("U006271", "arbitrary rewrite rules"),
    }
    for name, (unit, restriction) in grammar_evidence.items():
        add(name, "GRAMMAR", ("SOURCE_UNIT", unit),
            [ev("U006267", "Generative grammars apply replacements in all possible ways from a start expression."),
             ev(unit, f"The class is independently delimited by the restriction: {restriction}.")],
            overrides={"structural_invariants": restriction})
    add("multidimensional block multiway system", "MULTI", ("SOURCE_UNIT", "U006273"),
        [ev("U006273", "Rules operate on arbitrary blocks in arrays of any dimension.")],
        overrides={"carrier": "multidimensional arrays",
                   "topology": "arbitrary matching blocks in the array"})
    add("cyclic limited-size multiway system", "MULTI", ("SOURCE_UNIT", "U006273"),
        [ev("U006273", "A limited-size variant applies transformations cyclically to strings.")],
        overrides={"boundary": "cyclic string boundary",
                   "structural_invariants": "string size is limited by the cyclic representation"})
    add("numeric multiway system n -> {n+1,2n}", "MULTI", ("SOURCE_UNIT", "U006273"),
        [ev("U006273", "The independently delimited numeric rule maps n to both n+1 and 2n."),
         ev("U006274", "NestList unions both arithmetic successors from seed 0.", modality="CODE"),
         ev("U006275", "The layer at step t contains Fibonacci[t+2] distinct numbers.")],
        params=[("seed", "0")],
        overrides={"carrier": "sets of nonnegative integers",
                   "alphabet_or_value_schema": "integers",
                   "read_dependencies_or_neighborhood": "each current number"})
    add("normal-play nim", "GAME", ("SOURCE_UNIT", "U006276"),
        [ev("U006276", "The complete pile-removal move law, alternating schedule, last-object winner, and BitXor losing-position criterion are stated.")],
        aliases=["nim"])

    add("equational constraint system", "CONSTRAINT", ("SOURCE_UNIT", "U006278"),
        [ev("U006278", "Equations are explicitly characterized as constraints selecting systems that satisfy them, distinct from explicit evolution when features at one time are related.")])
    add("partial-differential-equation initial-value relation", "CONSTRAINT", ("SOURCE_UNIT", "U006279"),
        [ev("U006279", "Initial-value problems are independently delimited; hyperbolic/parabolic examples require initial values.")],
        variants=[("wave equation", "hyperbolic example"), ("diffusion equation", "parabolic example")],
        missing=["No concrete PDE formula or exact initial-data schema is supplied in this note."])
    add("partial-differential-equation boundary-value relation", "CONSTRAINT", ("SOURCE_UNIT", "U006279"),
        [ev("U006279", "Boundary-value problems are independently delimited; the elliptic Laplace equation requires boundary values.")],
        variants=[("Laplace equation", "elliptic example")],
        missing=["No concrete PDE formula or exact boundary domain is supplied in this note."])
    add("linear vector relation u == m.v", "CONSTRAINT", ("SOURCE_UNIT", "U006281"),
        [ev("U006281", "The exact linear relation is stated, with forward evaluation from v and inverse solution for v from u.")],
        params=[("m", "matrix"), ("u,v", "continuous-number vectors")])
    add("quadratic vector relation u == m1.v + m2.v^2", "CONSTRAINT", ("SOURCE_UNIT", "U006281"),
        [ev("U006281", "The exact nonlinear relation is independently stated and contrasted with the linear case; it generically has 2^n solutions for v.")],
        params=[("m1,m2", "matrices"), ("u,v", "continuous-number vectors")])
    add("variational extremum constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006282"),
        [ev("U006282", "A variational principle accepts behavior/configurations that minimize or maximize a stated quantity; molecular energy minimization is the explicit example.")],
        overrides={"rule_relation_constraint_function_or_probability_law": "accept configurations attaining the stated minimum or maximum",
                   "result_kind": "the extremizing configuration set"})
    add("binary de Bruijn allowed-block path solver", "SOLVER", ("SOURCE_UNIT", "U006282"),
        [ev("U006282", "Overlapping length-n blocks become paths in a de Bruijn network."),
         ev("U006283", "Exact labelled binary de Bruijn graphs for n=2 through 5 supply graph identity and transitions.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_956_Picture_2.jpeg"),
         ev("U006284", "Dropping forbidden arcs and finding an infinite path decides/constructs allowed sequences; a repeated node yields a periodic witness.")],
        overrides={"carrier": "the k^(n-1) overlap states of length-n blocks",
                   "topology": "directed overlap graph",
                   "frontier_or_activation": "current graph node and outgoing allowed arcs",
                   "schedule": "follow an allowed path",
                   "result_kind": "an infinite allowed path/sequence or failure"})
    add("one-dimensional allowed-block constraint system", "CONSTRAINT", ("SOURCE_UNIT", "U006282"),
        [ev("U006282", "Only a selected subset of k^n length-n color blocks is allowed, with n-1 overlap."),
         ev("U006284", "An infinite sequence satisfies the constraint exactly when it is an infinite path through retained de Bruijn arcs.")],
        params=[("k", "number of colors"), ("n", "block length"), ("allowed blocks", "accepted local words")],
        overrides={"carrier": "one-dimensional color sequences",
                   "topology": "overlapping length-n windows"})
    add("two-dimensional 5-cell allowed-template constraint system", "CONSTRAINT", ("SOURCE_UNIT", "U006285"),
        [ev("U006285", "The 2D constraints are sets of allowed 5-cell templates, modulo stated symmetries."),
         ev("U006286", "A 32-bit number selects allowed templates by bit position."),
         ev("U006287", "The ordered 32-template alphabet is direct mechanics.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_956_Picture_8.jpeg"),
         ev("U006288", "A concrete Mathematica pattern represents the allowed-template disjunction."),
         ev("U006289", "SatisfiedQ checks every overlapping 3x3 window against the allowed pattern.", modality="CODE")],
        params=[("constraint number", "32-bit allowed-template mask")],
        overrides={"carrier": "two-dimensional binary cell arrays",
                   "topology": "overlapping 5-cell cross templates"})
    add("square-spiral backtracking constraint solver", "SOLVER", ("SOURCE_UNIT", "U006294"),
        [ev("U006294", "The complete prose algorithm extends along a square spiral, branches, backtracks to causally relevant choices, detects regularity, and memoizes prior work.", strength="DIRECT_COMPLETE_MECHANICS")])
    add("explicit nonperiodic constraint-witness function", "FUNCTION", ("SOURCE_UNIT", "U006295"),
        [ev("U006295", "The page-219 witness is independently identified as a nonperiodic pattern with an explicit coordinate law."),
         ev("U006296", "Four piecewise formulas determine the color a[x,y].", modality="CODE", strength="DIRECT_COMPLETE_MECHANICS"),
         ev("U006297", "Coordinate-origin choice is the only freedom and the pattern is a satisfying witness.")],
        overrides={"carrier": "integer coordinate pairs",
                   "alphabet_or_value_schema": "binary cell colors",
                   "result_kind": "the color at coordinate (x,y)"})
    add("smaller-template local constraint family", "CONSTRAINT", ("SOURCE_UNIT", "U006298"),
        [ev("U006298", "Constraints based on smaller templates are independently delimited."),
         ev("U006299", "Five exact template shapes are related to counts 4,7,17,11,12 of required repetitive patterns.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_957_Constraint_Template_Icons_and_Ratios.jpeg", strength="CORROBORATING")],
        params=[("template shape", "one of the five displayed smaller neighborhoods")])
    add("every-allowed-template-must-occur constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006300"),
        [ev("U006300", "The variant requires not only that every local block be allowed, but also that every template in the selected set occur somewhere.")],
        overrides={"rule_relation_constraint_function_or_probability_law": "accept arrays whose local blocks are allowed and which globally realize every template in the selected set"})
    add("Ammann-derived 16-color nested-pattern constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006301"),
        [ev("U006301", "The 16-color construction is independently identified as forcing a nested pattern."),
         ev("U006302", "The complete sixteen-symbol substitution system is listed.", modality="CODE"),
         ev("U006303", "Exactly the 51 occurring 2x2 blocks out of 65,536 become the allowed local templates."),
         ev("U006304", "The image is the resulting nested witness.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_957_Picture_14.jpeg", strength="CORROBORATING")],
        params=[("colors", "16"), ("allowed 2x2 blocks", "the 51 blocks induced by the stated substitution")],
        overrides={"carrier": "two-dimensional arrays of 16 colors",
                   "topology": "overlapping 2x2 blocks"})
    add("rule-30 history as a two-dimensional constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006306"),
        [ev("U006306", "A 1D cellular-automaton history is reinterpreted as a 2D array constrained by the rule above each cell."),
         ev("U006307", "The exact allowed template set for rule 30 is displayed.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_958_Picture_4.jpeg"),
         ev("U006308", "A specified initial row gives a unique pattern below it; predecessor existence above is not guaranteed."),
         ev("U006309", "With no or few fixed cells, periodic satisfying patterns can be constructed from periodic CA behavior.")],
        overrides={"carrier": "two-dimensional binary arrays interpreted as space-time histories",
                   "topology": "each cell relates to its predecessor neighborhood above"})
    add("plane-tiling constraint system", "CONSTRAINT", ("SOURCE_UNIT", "U006310"),
        [ev("U006310", "A tiling constraint accepts coverings of the plane by the stated tile shapes with edge distinctions where required.")],
        overrides={"carrier": "tile placements covering the plane",
                   "topology": "edge-to-edge incidence and nonoverlap/coverage",
                   "alphabet_or_value_schema": "the selected tile shapes and distinguished edges"})
    add("Penrose two-tile aperiodic tiling constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006310"),
        [ev("U006310", "Two Penrose tiles are stated to cover the plane only in a nested pattern generated by subdivision; edge distinctions prevent trivial periodic arrangements.")],
        missing=["Exact tile geometry/subdivision is routed to page 932."],
        params=[("tile count", "2")])
    add("Penrose 1994 aperiodic polyomino constraint set", "CONSTRAINT", ("SOURCE_UNIT", "U006314"),
        [ev("U006314", "Set (a) is independently attributed and stated to force nonperiodic patterns."),
         ev("U006315", "Panel (a) directly specifies its three polyomino tile shapes.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_958_Polyomino_Sets_Two_Panel_Row.jpeg")],
        overrides={"carrier": "edge-to-edge placements of the three displayed polyominoes",
                   "alphabet_or_value_schema": "the three set-(a) polyomino shapes"})
    add("Cook aperiodic polyomino constraint set", "CONSTRAINT", ("SOURCE_UNIT", "U006314"),
        [ev("U006314", "Set (b) is independently attributed to Matthew Cook and stated to force nonperiodic patterns."),
         ev("U006315", "Panel (b) directly specifies its four polyomino tile shapes.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_958_Polyomino_Sets_Two_Panel_Row.jpeg"),
         ev("U006316", "The construction is nested and its stage-n tile counts are stated."),
         ev("U006317", "The image directly shows recursive assembly from the set-(b) tiles.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_958_Picture_17.jpeg")],
        overrides={"carrier": "edge-to-edge placements of the four displayed polyominoes",
                   "alphabet_or_value_schema": "the four set-(b) polyomino shapes"})
    add("generalized spin-system ground-state constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006318"),
        [ev("U006318", "Binary spins have local neighborhood-dependent energies; accepted ground states minimize total energy.")],
        overrides={"carrier": "two-dimensional arrays of spins",
                   "alphabet_or_value_schema": "up/down spins",
                   "rule_relation_constraint_function_or_probability_law": "accept spin arrays with the smallest total neighborhood-dependent energy"})
    add("ordinary Ising ground-state constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006318"),
        [ev("U006318", "The ordinary Ising model is independently named and its ground-state result is all-up or all-down.")],
        missing=["The exact Ising energy formula is routed to page 981."],
        overrides={"carrier": "two-dimensional arrays of spins",
                   "alphabet_or_value_schema": "up/down spins",
                   "result_kind": "the all-up and all-down ground-state configurations"})
    add("spin-glass random-sign ground-state constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006318"),
        [ev("U006318", "A spin glass multiplies the standard Ising energy contribution by independently random -1 or +1 signs for each spin.")],
        overrides={"carrier": "two-dimensional arrays of spins with quenched random signs",
                   "alphabet_or_value_schema": "up/down spins plus per-spin signs",
                   "external_data": "a fixed random -1/+1 sign assigned to each spin"})
    add("list-valued sequence equation constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006318"),
        [ev("U006318", "The exact Flatten[{x,1,x,0,y}] === Flatten[{0,y,0,y,x}] relation is stated with variables ranging over lists.")],
        overrides={"carrier": "finite lists substituted for x and y",
                   "alphabet_or_value_schema": "lists containing the constants 0 and 1",
                   "topology": "concatenation order in the two flattened expressions"})
    add("adjacent-square-free sequence constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006318"),
        [ev("U006318", "The sequence must not match two adjacent identical nonempty blocks; k=3 admits the stated infinite substitution witness."),
         ev("U006319", "The enumerator appends each symbol then deletes sequences with adjacent repeated blocks.", modality="CODE"),
         ev("U006320", "The accepted-count growth is stated.")],
        aliases=["no-pair-of-identical-blocks constraint"],
        overrides={"carrier": "one-dimensional sequences",
                   "topology": "contiguous substring equality"})
    add("cube-free sequence constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006321"),
        [ev("U006321", "The sequence must contain no three adjacent identical blocks; the Thue-Morse sequence is a stated infinite witness.")],
        aliases=["no-triple-of-identical-blocks constraint"],
        overrides={"carrier": "one-dimensional sequences",
                   "topology": "contiguous triple-block equality"})
    add("general pattern-avoidance sequence constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006322"),
        [ev("U006322", "Patterns of repeated variables are explicitly treated as forbidden substring schemas over k symbols.")],
        params=[("k", "alphabet size"), ("forbidden variable pattern", "block-variable schema")],
        overrides={"carrier": "one-dimensional sequences",
                   "topology": "contiguous matches of the forbidden block-variable schema"})
    add("Diophantine integer-relation family", "CONSTRAINT", ("SOURCE_UNIT", "U006323"),
        [ev("U006323", "A Diophantine equation is independently delimited as an algebraic relation whose variables are required to be whole numbers.")],
        overrides={"carrier": "tuples of whole-number variable assignments",
                   "alphabet_or_value_schema": "whole numbers"})
    add("linear Diophantine relation a x == b y + c", "CONSTRAINT", ("SOURCE_UNIT", "U006324"),
        [ev("U006324", "The general linear relation ax=by+c and ExtendedGCD solvability method are stated."),
         ev("U006325", "Four labelled exact relation examples and integer-solution witnesses are displayed.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_959_Linear_Diophantine_Four_Panel_Row.jpeg")],
        params=[("a,b,c", "integer coefficients")],
        overrides={"carrier": "integer pairs (x,y)", "alphabet_or_value_schema": "integers"})
    for formula in ["3 x == 4 y", "4 x == 5 y", "3 x == 4 y + 1", "4 x == 5 y + 3"]:
        add(f"linear Diophantine relation {formula}", "CONSTRAINT", ("IMAGE", "A000580"),
            [ev("U006324", "The prose fixes integer-domain linear Diophantine semantics."),
             ev("U006325", f"The image independently labels the exact constraint {formula} and plots its integer solutions.", modality="IMAGE",
                image="BACK-MATTER/NOTES/_page_959_Linear_Diophantine_Four_Panel_Row.jpeg",
                strength="DIRECT_COMPLETE_MECHANICS")],
            overrides={"carrier": "integer pairs (x,y)", "alphabet_or_value_schema": "integers",
                       "rule_relation_constraint_function_or_probability_law": f"accept exactly integer pairs satisfying {formula}"})
    add("Pell equation x^2 == a y^2 + 1", "CONSTRAINT", ("SOURCE_UNIT", "U006326"),
        [ev("U006326", "The Pell relation and positive nonsquare-a condition for infinitely many solutions are stated."),
         ev("U006327", "A continued-fraction formula computes the smallest x.", modality="CODE"),
         ev("U006328", "The a=61 example and plotted observable are stated."),
         ev("U006329", "The image plots the least-solution magnitude over a.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_960_Figure_3.jpeg", strength="CONTEXTUAL")],
        params=[("a", "positive nonsquare integer")],
        overrides={"carrier": "integer pairs (x,y)", "alphabet_or_value_schema": "integers"})
    add("Pythagorean-triple relation x^2 + y^2 == z^2", "CONSTRAINT", ("SOURCE_UNIT", "U006330"),
        [ev("U006330", "The relation, example triples, and complete primitive parameterization are stated."),
         ev("U006331", "The image plots reduced and all integer-solution witnesses.", modality="IMAGE",
            image="BACK-MATTER/NOTES/_page_960_Figure_5.jpeg", strength="CORROBORATING")],
        overrides={"carrier": "integer triples (x,y,z)", "alphabet_or_value_schema": "integers"})
    equations = [
        "x + 3 y == 11 z",
        "x == y z",
        "x y == z^2",
        "x y == z^3",
        "x^2 + y^2 == z^2 - 1",
        "x^2 + y^2 == z^2 + 1",
        "x^3 + y^2 == z^2",
        "x^3 + y^3 == z^2",
    ]
    for formula in equations:
        add(f"Diophantine relation {formula}", "CONSTRAINT", ("IMAGE", "A000588"),
            [ev("U006332", "The prose identifies the displayed objects as Diophantine equations and their possible integer solutions."),
             ev("U006333", f"The image independently labels the exact constraint {formula} and plots integer-solution witnesses.", modality="IMAGE",
                image="BACK-MATTER/NOTES/_page_960_Picture_7.jpeg", strength="DIRECT_COMPLETE_MECHANICS")],
            overrides={"carrier": "integer triples (x,y,z)", "alphabet_or_value_schema": "integers",
                       "rule_relation_constraint_function_or_probability_law": f"accept exactly integer triples satisfying {formula}"})
    add("Fermat relation x^n + y^n == z^n for n > 2", "CONSTRAINT", ("SOURCE_UNIT", "U006334"),
        [ev("U006334", "The exact integer relation with n>2 is independently stated together with the accepted-result fact that no solutions exist.")],
        params=[("n", "integer exponent greater than 2")],
        overrides={"carrier": "positive whole-number tuples (x,y,z,n)",
                   "alphabet_or_value_schema": "positive whole numbers",
                   "result_kind": "the empty positive-integer solution set for n>2"})
    add("finite group-or-semigroup multiplication-table constraint", "CONSTRAINT", ("SOURCE_UNIT", "U006336"),
        [ev("U006336", "A finite group or semigroup is characterized by a finite multiplication table satisfying externally routed constraints.")],
        missing=["The exact multiplication-table axioms are routed to page 887."],
        overrides={"carrier": "finite multiplication tables",
                   "alphabet_or_value_schema": "finite element labels",
                   "topology": "ordered pairs of elements map to table entries"})
    add("formula-search constraint for algebraic roots", "CONSTRAINT", ("SOURCE_UNIT", "U006338"),
        [ev("U006338", "The object is independently delimited as finding formulas satisfying exact root constraints, with allowed function families and degree-dependent existence facts.")],
        params=[("polynomial degree", "n"), ("allowed functions", "roots or stated special functions")],
        overrides={"carrier": "symbolic formulas over the allowed function vocabulary",
                   "alphabet_or_value_schema": "symbolic expressions and polynomial coefficients",
                   "rule_relation_constraint_function_or_probability_law": "accept formulas that return roots for arbitrary coefficients of the stated degree",
                   "result_kind": "a satisfying symbolic formula or proof that the restricted vocabulary is insufficient"})

    return s


ROUTES = [
    ("U006078", "", "page 929", "PAGE", "other lattice constructions", "WR0001"),
    ("U006121", "", "page 1092", "PAGE", "additive cellular-automaton rules", "WR0002"),
    ("U006121", "", "page 980", "PAGE", "cellular automaton code 175850", "WR0003"),
    ("U006123", "A000527", "page 183", "PAGE", "underlying rules for 3D projection panels (a) and (b)", "WR0004"),
    ("U006139", "A000546", "page 185", "PAGE", "rules for 2D Turing-machine head paths (a) through (e)", "WR0005"),
    ("U006168", "A000548", "main-text rules underlying the non-white-background panels", "SECTION", "exact replacement tables for the displayed panels", "WR0006"),
    ("U006192", "", "pages 407 and 1006", "PAGE", "parameter-space sets for geometric substitution systems", "WR0007"),
    ("U006208", "", "page 1127", "PAGE", "sigma-function scan of an infinite grid quadrant", "WR0008"),
    ("U006226", "", "Chapter 9", "SECTION", "undirected-network update rules", "WR0009"),
    ("U006273", "", "page 508", "PAGE", "network substitution systems", "WR0010"),
    ("U006273", "", "page 1141", "PAGE", "multiway tag systems", "WR0011"),
    ("U006276", "", "page 504", "PAGE", "multiway systems in fundamental physics", "WR0012"),
    ("U006310", "", "page 932", "PAGE", "exact Penrose tile subdivision", "WR0013"),
    ("U006318", "", "page 981", "PAGE", "exact Ising-model energy law", "WR0014"),
    ("U006318", "", "page 757", "PAGE", "correspondence systems", "WR0015"),
    ("U006336", "", "page 887", "PAGE", "finite group/semigroup multiplication-table constraints", "WR0016"),
    ("U006336", "", "page 1073", "PAGE", "Hadamard matrix property", "WR0017"),
    ("U006338", "", "page 1129", "PAGE", "formula constraints and expression complexity", "WR0018"),
]


ROLE_MAP = {
    "A000519": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000520": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000526": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000527": ("RELATION", ["TEXT_BEARING", "CAPTION_INCOMPLETE"], "CHECKED", "CLEAR"),
    "A000528": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000541": ("CONTROL", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000542": ("CONTROL", ["TEXT_BEARING", "AMBIGUOUS", "CAPTION_INCOMPLETE"], "CHECKED", "CONFLICTING"),
    "A000543": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING"], "CHECKED", "CLEAR"),
    "A000544": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000545": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000546": ("OBSERVER", ["TEXT_BEARING", "CAPTION_INCOMPLETE"], "CHECKED", "CLEAR"),
    "A000547": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING"], "CHECKED", "CLEAR"),
    "A000548": ("OBSERVER", ["CAPTION_INCOMPLETE"], "NOT_REQUIRED", "CLEAR"),
    "A000549": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "CAPTION_INCOMPLETE"], "CHECKED", "CLEAR"),
    "A000550": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING"], "CHECKED", "CLEAR"),
    "A000551": ("RELATION", [], "NOT_REQUIRED", "CLEAR"),
    "A000552": ("OBSERVER", ["CAPTION_INCOMPLETE"], "NOT_REQUIRED", "CLEAR"),
    "A000553": ("CONTROL", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000554": ("OBSERVER", [], "NOT_REQUIRED", "CLEAR"),
    "A000556": ("CONTROL", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000559": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000560": ("RELATION", ["TEXT_BEARING", "CAPTION_INCOMPLETE"], "CHECKED", "CLEAR"),
    "A000564": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "CAPTION_INCOMPLETE"], "CHECKED", "CLEAR"),
    "A000565": ("RELATION", ["TEXT_BEARING", "AMBIGUOUS", "CAPTION_INCOMPLETE"], "CHECKED", "DEFECTIVE"),
    "A000566": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000571": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000572": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING"], "CHECKED", "CLEAR"),
    "A000573": ("RELATION", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000574": ("OBSERVER", [], "NOT_REQUIRED", "CLEAR"),
    "A000577": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING"], "CHECKED", "CLEAR"),
    "A000578": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING"], "CHECKED", "CLEAR"),
    "A000579": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000580": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000585": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000586": ("OBSERVER", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000587": ("RELATION", ["TEXT_BEARING"], "CHECKED", "CLEAR"),
    "A000588": ("NATIVE_EVIDENCE", ["CONSTRUCTION_BEARING", "TEXT_BEARING"], "CHECKED", "CLEAR"),
}

ORPHANS = {
    **{f"A00052{i}": "A000520" for i in range(1, 6)},
    **{f"A0005{i}": "A000528" for i in range(29, 32)},
    **{f"A0005{i}": "A000527" for i in range(32, 36)},
    **{f"A0005{i}": "A000542" for i in range(36, 41)},
    "A000555": "A000556",
    "A000557": "A000556",
    "A000558": "A000556",
    "A000561": "A000564",
    "A000562": "A000564",
    "A000563": "A000564",
    "A000567": "A000566",
    "A000568": "A000566",
    "A000569": "A000566",
    "A000570": "A000566",
    "A000575": "A000579",
    "A000576": "A000579",
    "A000581": "A000580",
    "A000582": "A000580",
    "A000583": "A000580",
    "A000584": "A000580",
}

REPRESENTATION_UNITS = {
    "U006094", "U006095", "U006112", "U006113", "U006121", "U006122",
    "U006123", "U006124", "U006139", "U006140", "U006147", "U006148",
    "U006149", "U006150", "U006151", "U006152", "U006153", "U006154",
    "U006155", "U006156", "U006157", "U006158", "U006159", "U006160",
    "U006161", "U006162", "U006163", "U006164", "U006165", "U006166",
    "U006167", "U006187", "U006188", "U006189", "U006190", "U006191",
    "U006194", "U006195", "U006196", "U006199", "U006201", "U006202",
    "U006203", "U006204", "U006208", "U006209", "U006225", "U006228",
    "U006233", "U006234", "U006235", "U006255", "U006256", "U006257",
    "U006258", "U006259", "U006260", "U006262", "U006263", "U006264",
    "U006265", "U006266", "U006283", "U006290", "U006291", "U006292",
    "U006293", "U006297", "U006299", "U006304", "U006305", "U006308",
    "U006309", "U006316", "U006317", "U006320", "U006328", "U006329",
    "U006331", "U006337",
}

HISTORY_UNITS = {"U006114", "U006136", "U006138", "U006197", "U006261", "U006264", "U006265", "U006266"}
APPLICATION_UNITS = {"U006121", "U006227"}
DEFECT_UNITS = {
    "U006117": "The prose says undefined “s alone” although the code defines only p/q/r and the image labels r/q/p compositions.",
    "U006118": "The image labels r/q/p compositions while its governing prose says undefined “s alone”.",
    "U006258": "The caption contains OCR truncation “shows wh” and does not specify the plotted axis/string encoding.",
}


def profile_values(spec: dict[str, Any]) -> dict[str, str | None]:
    values = dict(CORE[spec["profile"]])
    values.update(spec["overrides"])
    if set(values) != set(FIELDS):
        raise AssertionError(f"incomplete profile fields for {spec['name']}")
    return values


def author(bundle: Path, check_spec: bool) -> dict[str, Any]:
    for rel, digest in EXPECTED.items():
        actual = sha256(bundle / rel)
        if actual != digest:
            raise SystemExit(f"sealed input mismatch: {rel}: {actual} != {digest}")

    out_path = bundle / "output/output.json"
    output = json.loads(out_path.read_text())
    if output["worker_id"] != WORKER:
        raise SystemExit("worker id mismatch")
    if output["allowed_manifest_sha256"] != EXPECTED["allowed-manifest.json"]:
        raise SystemExit("manifest declaration mismatch")

    reading_rows = list(csv.DictReader((bundle / "input/reading-input.csv").open()))
    asset_rows = list(csv.DictReader((bundle / "input/asset-input.csv").open()))
    if len(reading_rows) != 263 or [r["source_unit_id"] for r in reading_rows] != [
        f"U{i:06d}" for i in range(6076, 6339)
    ]:
        raise SystemExit("reading projection is not the exact assigned contiguous range")
    if len(asset_rows) != 70 or [r["asset_id"] for r in asset_rows] != [
        f"A{i:06d}" for i in range(519, 589)
    ]:
        raise SystemExit("asset projection is not the exact assigned contiguous range")

    specs = candidate_specs()
    candidate_ids: dict[int, str] = {i: f"W{i + 1:04d}" for i in range(len(specs))}
    unit_candidates: dict[str, list[str]] = {}
    asset_candidates: dict[str, list[str]] = {}
    proposals: list[dict[str, Any]] = []

    unit_order = {row["source_unit_id"]: i + 1 for i, row in enumerate(reading_rows)}
    asset_by_id = {row["asset_id"]: row for row in asset_rows}
    asset_by_path = {row["physical_path"]: row for row in asset_rows}
    image_order = {
        row["physical_path"]: len(reading_rows) + i + 1
        for i, row in enumerate(asset_rows)
    }

    # Candidate discovery uses the image-link source unit even when the
    # decisive identity is visually carried by that unit's owned image.  This
    # preserves the document-first source traversal; image evidence itself
    # retains an IMAGE anchor.
    candidate_anchors: list[tuple[str, str, int]] = []
    candidate_ordinals: dict[str, int] = {}
    for spec in specs:
        kind, anchor_id = spec["anchor"]
        if kind == "IMAGE":
            anchor_unit = asset_by_id[anchor_id]["source_unit_id"]
            if not anchor_unit:
                raise AssertionError(f"image candidate anchor {anchor_id} has no source unit")
        else:
            anchor_unit = anchor_id
        candidate_ordinals[anchor_unit] = candidate_ordinals.get(anchor_unit, 0) + 1
        candidate_anchors.append(
            ("SOURCE_UNIT", anchor_unit, candidate_ordinals[anchor_unit])
        )
    candidate_keys = [
        (unit_order[anchor_id], ordinal)
        for _, anchor_id, ordinal in candidate_anchors
    ]
    if candidate_keys != sorted(candidate_keys):
        raise AssertionError("candidate specs are not in frozen source traversal order")

    # Evidence IDs are globally ordered by immutable anchor traversal rather
    # than candidate grouping.  Ordinals restart at one for each exact anchor.
    evidence_occurrences: list[tuple[int, int, int, str, str]] = []
    for spec_index, spec in enumerate(specs):
        for raw_index, raw in enumerate(spec["evidence"]):
            if raw["image"]:
                anchor_kind = "IMAGE"
                anchor_id = raw["image"]
                anchor_order = image_order[anchor_id]
            else:
                anchor_kind = "SOURCE_UNIT"
                anchor_id = raw["unit"]
                anchor_order = unit_order[anchor_id]
            evidence_occurrences.append(
                (anchor_order, spec_index, raw_index, anchor_kind, anchor_id)
            )
    evidence_occurrences.sort()
    evidence_assignments: dict[tuple[int, int], tuple[str, str, str, str, int]] = {}
    evidence_anchor_ordinals: dict[tuple[str, str], int] = {}
    for global_ordinal, (_, spec_index, raw_index, anchor_kind, anchor_id) in enumerate(
        evidence_occurrences, 1
    ):
        anchor_key = (anchor_kind, anchor_id)
        evidence_anchor_ordinals[anchor_key] = evidence_anchor_ordinals.get(anchor_key, 0) + 1
        evidence_assignments[(spec_index, raw_index)] = (
            f"WE{global_ordinal:06d}",
            f"WG{global_ordinal:06d}",
            anchor_kind,
            anchor_id,
            evidence_anchor_ordinals[anchor_key],
        )

    for i, spec in enumerate(specs):
        cid = candidate_ids[i]
        values = profile_values(spec)
        records: list[dict[str, Any]] = []
        for raw_index, raw in enumerate(spec["evidence"]):
            eid, gid, anchor_kind, anchor_id, anchor_ordinal = evidence_assignments[
                (i, raw_index)
            ]
            supported_fields = raw["fields"] or [f for f, value in values.items() if value is not None]
            records.append(
                {
                    "evidence_id": eid,
                    "evidence_group_id": gid,
                    "discovery_anchor": {
                        "epoch": 2,
                        "kind": anchor_kind,
                        "id": anchor_id,
                        "ordinal": anchor_ordinal,
                    },
                    "source_unit_id": raw["unit"],
                    "image_path": raw["image"],
                    "strength": raw["strength"],
                    "modality": raw["modality"],
                    "claim": raw["claim"],
                    "fingerprint_fields": supported_fields,
                }
            )
            if raw["unit"]:
                unit_candidates.setdefault(raw["unit"], []).append(cid)
            if raw["image"]:
                asset_candidates.setdefault(asset_by_path[raw["image"]]["asset_id"], []).append(cid)

        statuses: dict[str, str] = {}
        fingerprint: dict[str, dict[str, Any]] = {}
        missing = list(spec["missing"])
        for field in FIELDS:
            value = values[field]
            field_eids = [r["evidence_id"] for r in records if field in r["fingerprint_fields"]]
            if value is None:
                status = NA
                reason = f"{field} is not part of the native semantics of this {spec['profile'].lower()} object."
                field_eids = []
            elif field in {"boundary"} and "not fully" in value:
                status = UNK
                reason = value
                value = None
                missing.append(reason)
                field_eids = []
            elif spec["source_status"] == ["CONFLICTING"] and field == "rule_relation_constraint_function_or_probability_law":
                status = CONFLICT
                reason = spec["uncertainty"][0]
                value = None
            elif value in {"unknown from this source"}:
                status = UNK
                reason = f"{field} is not fixed by the assigned source."
                value = None
                missing.append(reason)
                field_eids = []
            else:
                status = SUP
                reason = f"The assigned evidence supports: {value}."
                if not field_eids:
                    raise AssertionError(f"{cid} {field} lacks evidence")
            statuses[field] = status
            fingerprint[field] = {
                "status": status,
                "value": value,
                "evidence_ids": field_eids,
                "reason": reason,
            }

        # Make the evidence-to-fingerprint join exact after unknown,
        # not-applicable, and conflicting fields have been adjudicated.
        for record in records:
            record["fingerprint_fields"] = [
                field
                for field in FIELDS
                if record["evidence_id"] in fingerprint[field]["evidence_ids"]
            ]

        anchor_kind, anchor_id, anchor_ordinal = candidate_anchors[i]
        image_paths = sorted({r["image_path"] for r in records if r["image_path"]})
        unit_ids = sorted({r["source_unit_id"] for r in records if r["source_unit_id"]})
        evidence_ids = sorted(r["evidence_id"] for r in records)
        proposals.append(
            {
                "id": cid,
                "record_status": "ACTIVE",
                "provisional_name": spec["name"],
                "aliases": spec["aliases"],
                "discovery_stage": 9,
                "discovery_anchor": {
                    "epoch": 2,
                    "kind": anchor_kind,
                    "id": anchor_id,
                    "ordinal": anchor_ordinal,
                },
                "source_unit_ids": unit_ids,
                "source_evidence": records,
                "source_status": spec["source_status"],
                "image_witnesses": image_paths,
                "evidence_strength": list(dict.fromkeys(r["strength"] for r in records)),
                "field_support": statuses,
                "fingerprint": fingerprint,
                "parameters": [
                    {"name": name, "source_description": desc, "evidence_ids": evidence_ids}
                    for name, desc in spec["params"]
                ],
                "variants": [
                    {"name": name, "source_description": desc, "evidence_ids": evidence_ids}
                    for name, desc in spec["variants"]
                ],
                "missing_mechanics": list(dict.fromkeys(missing)),
                "uncertainties": spec["uncertainty"],
                "related_candidate_ids": [],
                "cross_reference_ids": [],
                "evidence_reassignments": [],
            }
        )

    # Routes are deliberately unresolved worker proposals.
    unit_routes: dict[str, list[str]] = {}
    asset_routes: dict[str, list[str]] = {}
    route_proposals: list[dict[str, str]] = []
    ordered_routes = sorted(
        ROUTES,
        key=lambda row: (
            len(reading_rows) + int(row[1][1:]) - 518
            if row[1]
            else unit_order[row[0]]
        ),
    )
    route_anchor_ordinals: dict[tuple[str, str], int] = {}
    for route_index, (unit, asset, target, kind, topic, _) in enumerate(ordered_routes, 1):
        rid = f"WR{route_index:04d}"
        if asset:
            discovery_kind = "IMAGE"
            discovery_id = asset
            source_unit_id = ""
            source_asset_id = asset
            asset_routes.setdefault(asset, []).append(rid)
            anchor_key = (discovery_kind, asset)
        else:
            discovery_kind = "SOURCE_UNIT"
            discovery_id = unit
            source_unit_id = unit
            source_asset_id = ""
            unit_routes.setdefault(unit, []).append(rid)
            anchor_key = (discovery_kind, unit)
        route_anchor_ordinals[anchor_key] = route_anchor_ordinals.get(anchor_key, 0) + 1
        route_proposals.append(
            {
                "route_id": rid,
                "source_unit_id": source_unit_id,
                "source_asset_id": source_asset_id,
                "discovery_epoch": EPOCH,
                "discovery_kind": discovery_kind,
                "discovery_id": discovery_id,
                "discovery_ordinal": str(route_anchor_ordinals[anchor_key]),
                "literal_target": target,
                "route_kind": kind,
                "expected_topic": topic,
                "owning_stage": STAGE,
                "closure_scope": "CROSS_RANGE",
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": jlist(["Blind sequential review recorded the literal target; coordinator routing is required."]),
                "vocabulary_terms": jlist(sorted(set(topic.lower().replace("/", " ").replace("-", " ").split()))),
                "defect_boundary": "",
            }
        )

    reading_updates: list[dict[str, str]] = []
    candidate_anchor_units = {
        spec["anchor"][1]
        for spec in specs
        if spec["anchor"][0] == "SOURCE_UNIT"
    }
    image_anchor_assets = {
        spec["anchor"][1]
        for spec in specs
        if spec["anchor"][0] == "IMAGE"
    }
    asset_by_unit = {r["source_unit_id"]: r["asset_id"] for r in asset_rows if r["source_unit_id"]}
    for row in reading_rows:
        u = row["source_unit_id"]
        cids = list(dict.fromkeys(unit_candidates.get(u, [])))
        if u in asset_by_unit:
            cids = list(dict.fromkeys(cids + asset_candidates.get(asset_by_unit[u], [])))
        rids = unit_routes.get(u, [])
        uncertainty = DEFECT_UNITS.get(u, "")
        source_status = (
            "CONFLICTING"
            if u in {"U006117", "U006118"}
            else "DEFECTIVE"
            if uncertainty
            else "CLEAR"
        )
        if uncertainty:
            disposition = "SOURCE_DEFECT_OR_AMBIGUITY"
            statement = uncertainty
        elif u in candidate_anchor_units or asset_by_unit.get(u) in image_anchor_assets:
            disposition = "CANDIDATE"
            statement = "Introduces one or more independently delimited construction or relation candidates linked in candidate_ids."
        elif cids:
            disposition = "SUPPORTS_CANDIDATE"
            statement = "Supplies identity, mechanics, parameters, witness semantics, or bounded context for the linked candidate(s)."
        elif rids:
            disposition = "CROSS_REFERENCE"
            statement = "Construction-relevant content is principally an unresolved literal route recorded in route_ids."
        elif u in REPRESENTATION_UNITS:
            disposition = "REPRESENTATION_OR_OBSERVER"
            statement = "This unit is a rendering, history, measurement, alternate encoding, solver output, or witness representation rather than a new native law."
        elif u in APPLICATION_UNITS:
            disposition = "APPLICATION_OR_EMULATION"
            statement = "This unit principally applies or analogizes an already identified construction."
        elif u in HISTORY_UNITS:
            disposition = "HISTORICAL_ONLY"
            statement = "This unit supplies attribution or chronology without an independently new native law."
        else:
            disposition = "NO_CONSTRUCTION"
            statement = "Complete in-context review found no independently delimited construction, relation, route, or source defect in this unit."

        roles: list[str] = []
        if disposition == "REPRESENTATION_OR_OBSERVER":
            roles.append("REPRESENTATION")
        if disposition == "HISTORICAL_ONLY":
            roles.append("HISTORICAL_MENTION")
        if disposition == "APPLICATION_OR_EMULATION":
            roles.append("APPLICATION")
        if row["block_kind"] == "fenced_code" and not cids:
            roles.append("IMPLEMENTATION_DETAIL")
        if u in {"U006080", "U006081", "U006119", "U006120", "U006250", "U006260"}:
            roles.append("SEED_INPUT_OR_BOUNDARY")
        if uncertainty:
            roles.append("SOURCE_DEFECT")
        update = dict(row)
        update.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": EPOCH,
                "review_disposition": disposition,
                "source_status": source_status,
                "uncertainty": uncertainty,
                "secondary_roles": jlist(list(dict.fromkeys(roles))),
                "candidate_ids": jlist(cids),
                "route_ids": jlist(rids),
                "evidence_statement": statement,
                "review_stage": STAGE,
                "reviewer": WORKER,
            }
        )
        reading_updates.append(update)

    asset_updates: list[dict[str, str]] = []
    for row in asset_rows:
        aid = row["asset_id"]
        if aid in ORPHANS:
            role = "SOURCE_DEFECT"
            parent = ORPHANS[aid]
            flags = ["CAPTION_INCOMPLETE"]
            # Retain visible text/construction risk exactly where the crop carries it.
            if aid not in {"A000561", "A000562", "A000563", "A000581"}:
                flags.append("TEXT_BEARING")
            if aid in {"A000521", "A000522", "A000523", "A000524", "A000525",
                       "A000561", "A000562", "A000563", "A000575", "A000576", "A000584"}:
                flags.insert(0, "CONSTRUCTION_BEARING")
            transcription = "NOT_REQUIRED" if aid == "A000581" else "CHECKED"
            status = "DEFECTIVE"
            uncertainty = (
                f"Orphaned redundant panel crop of {parent} with no Markdown reference "
                "or independent caption; semantic context comes only from the referenced composite."
            )
            statement = uncertainty
            cids: list[str] = []
        else:
            role, flags, transcription, status = ROLE_MAP[aid]
            cids = list(dict.fromkeys(asset_candidates.get(aid, [])))
            if aid == "A000542":
                uncertainty = (
                    "Caption/prose says undefined “s alone”, while code and image contain "
                    "only r, q, p, and their compositions."
                )
            elif aid == "A000565":
                uncertainty = (
                    "Caption OCR truncates “shows wh” and never defines the plot's axis/string encoding."
                )
            else:
                uncertainty = ""
            if role == "NATIVE_EVIDENCE":
                statement = "Native-resolution review found direct carrier, topology, rule, relation, replacement, schedule, or constraint evidence as linked."
            elif role == "RELATION":
                statement = "Native-resolution review found a relation, measurement, projection, or witness linkage rather than a standalone native update law."
            elif role == "CONTROL":
                statement = "Native-resolution review found a parameter/seed/control sweep supporting but not redefining the underlying law."
            elif role == "OBSERVER":
                statement = "Native-resolution review found a history, rendering, or observable without standalone native mechanics."
            else:
                statement = "Native-resolution review completed."

        update = dict(row)
        update.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": EPOCH,
                "visual_role": role,
                "source_status": status,
                "risk_flags": jlist(flags),
                "original_resolution_status": "REVIEWED",
                "transcription_status": transcription,
                "candidate_ids": jlist(cids),
                "route_ids": jlist(asset_routes.get(aid, [])),
                "evidence_statement": statement,
                "review_stage": STAGE,
                "reviewer": WORKER,
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append(update)

    # Candidate cross-reference links are derived from shared source or image
    # provenance; routes themselves remain unresolved.
    routes_by_unit = {u: ids for u, ids in unit_routes.items()}
    for proposal in proposals:
        linked: list[str] = []
        for unit in proposal["source_unit_ids"]:
            linked.extend(routes_by_unit.get(unit, []))
        for image_path in proposal["image_witnesses"]:
            linked.extend(asset_routes.get(asset_by_path[image_path]["asset_id"], []))
        proposal["cross_reference_ids"] = list(dict.fromkeys(linked))

    defect_uncertainties = [
        f"{unit}: {text}" for unit, text in DEFECT_UNITS.items()
    ] + [
        f"{aid}: {next(a['uncertainty'] for a in asset_updates if a['asset_id'] == aid)}"
        for aid in sorted(set(ORPHANS) | {"A000542", "A000565"})
    ]

    output["reading_updates"] = reading_updates
    output["asset_updates"] = asset_updates
    output["candidate_proposals"] = proposals
    output["route_proposals"] = route_proposals
    output["uncertainties"] = defect_uncertainties
    output["prohibited_input_nonuse"] = False

    # Hostile local invariants supplement the bundle verifier.
    assert len(proposals) == len({p["id"] for p in proposals})
    assert [p["id"] for p in proposals] == [f"W{i:04d}" for i in range(1, len(proposals) + 1)]
    assert [r["route_id"] for r in route_proposals] == [f"WR{i:04d}" for i in range(1, len(route_proposals) + 1)]
    all_evidence = sorted(
        (e for p in proposals for e in p["source_evidence"]),
        key=lambda row: row["evidence_id"],
    )
    assert [e["evidence_id"] for e in all_evidence] == [f"WE{i:06d}" for i in range(1, len(all_evidence) + 1)]
    assert [e["evidence_group_id"] for e in all_evidence] == [f"WG{i:06d}" for i in range(1, len(all_evidence) + 1)]
    assert all(r["review_status"] == "REVIEWED" and r["review_epoch"] == EPOCH for r in reading_updates)
    assert all(a["inspection_status"] == "SCREENED" and a["original_resolution_status"] == "REVIEWED" for a in asset_updates)
    assert len(ORPHANS) == 33
    assert all(next(a for a in asset_updates if a["asset_id"] == aid)["visual_role"] == "SOURCE_DEFECT" for aid in ORPHANS)
    assert next(r for r in reading_updates if r["source_unit_id"] == "U006117")["source_status"] == "CONFLICTING"
    assert next(a for a in asset_updates if a["asset_id"] == "A000542")["source_status"] == "CONFLICTING"
    assert next(a for a in asset_updates if a["asset_id"] == "A000565")["source_status"] == "DEFECTIVE"
    assert all(
        not (
            a["visual_role"] != "NATIVE_EVIDENCE"
            and any(
                e["image_path"] == a["physical_path"]
                and e["strength"] in {"DIRECT_IDENTITY", "DIRECT_PARTIAL_MECHANICS", "DIRECT_COMPLETE_MECHANICS"}
                for e in all_evidence
            )
        )
        for a in asset_updates
    )

    if check_spec:
        print(
            json.dumps(
                {
                    "units": len(reading_updates),
                    "assets": len(asset_updates),
                    "unreferenced_assets": sum(a["reference_status"] == "UNREFERENCED_PHYSICAL" for a in asset_updates),
                    "candidates": len(proposals),
                    "evidence": len(all_evidence),
                    "evidence_groups": len(all_evidence),
                    "routes": len(route_proposals),
                    "defects": len(defect_uncertainties),
                },
                sort_keys=True,
            )
        )
    else:
        out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--check-spec", action="store_true")
    args = parser.parse_args()
    author(args.bundle.resolve(), args.check_spec)


if __name__ == "__main__":
    main()
