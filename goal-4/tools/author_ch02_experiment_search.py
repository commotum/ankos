#!/usr/bin/env python3
"""Author one closed Stage 6 Chapter 2 LOCAL-search proposal.

The first invocation appends the candidate-derived and guardrail-derived seed
pass.  The second repeats the frozen query family with no vocabulary or
semantic delta, establishing the required local zero-delta closure.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import audit_transaction
import merge_worker_output
import validate_audit
from audit_contract import GOAL_DIR, REPO_ROOT, canonical_json_bytes


STAGE_PATHS = [
    "CHAPTERS/02-The-Crucial-Experiment/02-The-Crucial-Experiment.md",
    "BACK-MATTER/NOTES/02-The-Crucial-Experiment-Notes/02-The-Crucial-Experiment-Notes.md",
]

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with MULTILINE semantics and query-major then "
    "canonical source-unit result order."
)

NEW_VOCABULARY = [
    "computer experiment on possible simple programs",
    "elementary cellular automaton",
    "rule 254",
    "rule 250",
    "rule 90",
    "Game of Life",
    "single-black-cell seed",
    "cyclic boundary",
    "GeneralCARule",
    "FunctionCARule",
    "CellularAutomaton",
    "totalistic cellular automata",
    "outer-totalistic cellular automata",
    "weighted cellular automata",
    "additive cellular automata",
    "time slice",
    "spatial slice",
    "center column",
    "row population",
    "black positions",
    "rule 921408",
    "totalistic code 867",
    "totalistic code 3702",
    "symbolic cellular-automaton formula",
    "Cantor set",
    "rule 170",
    "Pascal's triangle",
    "rule 60",
    "binomial modulo",
    "multinomial modulo",
    "StirlingS1",
    "StirlingS2",
    "DigitCount",
    "PolynomialMod",
    "GCD",
    "JacobiSymbol",
    "bitwise functions",
    "BitAnd",
    "BitOr",
    "BitXor",
    "munching squares",
    "rule 102",
    "Pylos labyrinth",
    "Desborough ornament",
    "Roman rosette",
    "Cosmati triangles",
    "Persian garden",
    "wire rope",
    "sestina",
    "terza rima",
    "game process",
    "Go",
    "constraint puzzle",
    "Truchet tiles",
    "self-reproduction",
    "Ulam cellular automata",
    "Fredkin Rule 90 analog",
    "feedback shift register",
    "nonlinear feedback shift register",
    "symbolic dynamics",
    "block map",
    "totalistic code 20",
    "totalistic code 10",
]

QUERY_SPECS = [
    (
        "experiment and enumeration protocol",
        (
            r"\b(?:computer experiments?|possible simple programs?|"
            r"enumerat(?:e|es|ed|ing|ion)|systematic surveys?|survey of)\b"
        ),
        "REGEX",
    ),
    (
        "cellular-automaton aliases and profiles",
        (
            r"\b(?:CellularAutomaton|GeneralCARule|FunctionCARule|CAStep|"
            r"CAEvolveList|rules?\s*(?:10|20|30|60|90|102|110|170|250|"
            r"254|3702|921408)|totalistic code\s*(?:10|20|867|3702)|"
            r"totalistic|outer[- ]totalistic|additive|weighted)\b"
        ),
        "REGEX",
    ),
    (
        "seed boundary and query classes",
        (
            r"\b(?:CenterList|single black cell|seeds?|backgrounds?|cyclic|"
            r"periodic|offsets?|time slices?|space slices?|center columns?|"
            r"row populations?|black positions?)\b"
        ),
        "REGEX",
    ),
    (
        "arithmetic formula and bitwise constructions",
        (
            r"\b(?:Pascal(?:'s)? triangle|binomial|multinomial|StirlingS[12]|"
            r"DigitCount|PolynomialMod|Cantor(?: set)?|GCD|JacobiSymbol|"
            r"modulo|BitAnd|BitOr|BitXor|bitwise functions?|"
            r"munching squares?|munching foos?|formulas?)\b"
        ),
        "REGEX",
    ),
    (
        "cultural geometric game and verse constructions",
        (
            r"\b(?:labyrinths?|mazes?|rosettes?|mosaics?|Cosmati|"
            r"Alc[aá]zar|Persian gardens?|Truchet|Pylos|Desborough|"
            r"Phoenician|paperfolding|wire ropes?|sestina|terza rima|"
            r"rhymes?|games?|puzzles?|Game of Life|Conway)\b"
        ),
        "REGEX",
    ),
    (
        "historical automaton constructions",
        (
            r"\b(?:von Neumann|self[- ]reproduc(?:e|es|ed|ing|tion)|Ulam|"
            r"Fredkin|feedback shift registers?|LFSR|nonlinear FSR|"
            r"symbolic dynamics|block maps?)\b"
        ),
        "REGEX",
    ),
    (
        "native evolution mechanics",
        (
            r"\b(?:initial conditions?|initial states?|successive rows?|"
            r"evolution steps?|neighbou?rs?|transitions?|updates?|"
            r"synchronous|asynchronous)\b"
        ),
        "REGEX",
    ),
    (
        "stochasticity guardrail",
        (
            r"\b(?:random(?:ness)?|randomization|probabilistic|probability|"
            r"stochastic|Bernoulli)\b"
        ),
        "REGEX",
    ),
    (
        "declarative-function guardrail",
        (
            r"\b(?:constraints?|equations?|solutions?|functions?|relations?|"
            r"inequalit(?:y|ies)|differential|logic)\b"
        ),
        "REGEX",
    ),
    (
        "input-generator-structure guardrail",
        (
            r"\b(?:inputs?|outputs?|generators?|substitutions?|networks?|"
            r"Turing machines?|register machines?|mobile automata)\b"
        ),
        "REGEX",
    ),
    (
        "general construction nouns",
        r"\b(?:algorithms?|programs?|rules?|systems?|process(?:es)?)\b",
        "REGEX",
    ),
    (
        "representation-application boundary",
        (
            r"\b(?:simulat(?:e|es|ed|ing|ion)|"
            r"emulat(?:e|es|ed|ing|ion)|"
            r"implement(?:s|ed|ing|ation)?|"
            r"represent(?:s|ed|ing|ation)?|"
            r"displays?|render(?:s|ed|ing)?)\b"
        ),
        "REGEX",
    ),
]

EXPECTED_HIT_COUNTS = [9, 99, 37, 24, 20, 10, 45, 33, 43, 16, 205, 36]
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "ea7a8bd9d49502ddbcd34dbc95855694fee80b64c99679b81479a0eb517c6daa"
)
EXPECTED_TRIAGE_DIGEST = (
    "b35ff4b8cd61941b52bab5ebcbda9cfd90bbf2358aff1d150e4b5714e886ecb5"
)


class AuthoringError(ValueError):
    """The current state cannot safely receive this search proposal."""


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


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to the canonical Goal 4")

    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    reading = read_csv(goal_dir / merge_worker_output.READING_NAME)
    assets = read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    candidates = read_jsonl(goal_dir / merge_worker_output.CANDIDATE_NAME)
    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(encoding="utf-8")
    )
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)

    if [row.get("id") for row in candidates] != [
        f"B{value:04d}" for value in range(1, 92)
    ]:
        raise AuthoringError("candidate allocation differs from B0001..B0091")
    if [row.get("route_id") for row in routes] != [
        f"R{value:06d}" for value in range(1, 102)
    ]:
        raise AuthoringError("route allocation differs from R000001..R000101")
    if not history or history[-1].get("mode") not in {
        "ROUTE_RESOLUTION",
        "SEARCH_APPEND",
    }:
        raise AuthoringError("expected Stage 6 route/search terminal history")
    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 6 cannot author against a global fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list) or len(rounds) not in {4, 5}:
        raise AuthoringError("expected four prior rounds and zero/one Stage 6 round")
    if any(
        record.get("kind") != "LOCAL"
        or record.get("owning_stage") != stage
        or record.get("epoch") != 1
        for record, stage in zip(rounds[:4], [4, 4, 5, 5])
    ):
        raise AuthoringError("prior LOCAL round sequence differs")
    prior_stage_rounds = rounds[4:]
    if prior_stage_rounds:
        prior = prior_stage_rounds[0]
        if (
            prior.get("kind") != "LOCAL"
            or prior.get("owning_stage") != 6
            or prior.get("epoch") != 1
            or prior.get("new_vocabulary") != NEW_VOCABULARY
            or prior.get("new_candidates") != []
            or prior.get("new_evidence_groups") != []
            or prior.get("new_routes") != []
        ):
            raise AuthoringError("prior Stage 6 round is not the expected seed pass")

    reading_by_id = {row["source_unit_id"]: row for row in reading}
    assets_by_path: dict[str, list[dict[str, str]]] = {}
    for row in assets:
        assets_by_path.setdefault(row["assignment_path"], []).append(row)
    for path in STAGE_PATHS:
        path_rows = [row for row in reading if row["path"] == path]
        if not path_rows or any(
            row["review_status"] != "REVIEWED" for row in path_rows
        ):
            raise AuthoringError(f"Stage 6 source path is not fully reviewed: {path}")
        if any(
            row["inspection_status"] != "SCREENED"
            for row in assets_by_path.get(path, [])
        ):
            raise AuthoringError(f"Stage 6 assets are not fully screened: {path}")

    query_start = sum(len(record.get("queries", [])) for record in rounds) + 1
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
    source_root = REPO_ROOT / "ref" / "A-New-Kind-of-Science"
    result_pairs, query_errors = validate_audit.execute_frozen_queries(
        queries,
        units,
        source_root,
    )
    if query_errors:
        raise AuthoringError("; ".join(query_errors))

    unit_by_id = {unit["id"]: unit for unit in units}
    hit_counts = [
        sum(query_id == query["query_id"] for query_id, _ in result_pairs)
        for query in queries
    ]
    if hit_counts != EXPECTED_HIT_COUNTS:
        raise AuthoringError(
            f"Stage 6 query hit counts drifted: {hit_counts}"
        )
    normalized_pairs = [
        (int(query_id[1:]) - query_start + 1, unit_id)
        for query_id, unit_id in result_pairs
    ]
    normalized_digest = hashlib.sha256(
        canonical_json_bytes(normalized_pairs)
    ).hexdigest()
    if normalized_digest != EXPECTED_NORMALIZED_RESULT_DIGEST:
        raise AuthoringError(
            "Stage 6 normalized query/result pairs drifted: "
            f"{normalized_digest}"
        )
    triage_projection = [
        (
            unit_id,
            reading_by_id[unit_id]["review_disposition"],
            parse_links(
                reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            ),
            parse_links(
                reading_by_id[unit_id]["route_ids"],
                f"{unit_id}.route_ids",
            ),
        )
        for unit_id in sorted({unit_id for _, unit_id in result_pairs})
    ]
    triage_digest = hashlib.sha256(
        canonical_json_bytes(triage_projection)
    ).hexdigest()
    if triage_digest != EXPECTED_TRIAGE_DIGEST:
        raise AuthoringError(
            f"Stage 6 search triage projection drifted: {triage_digest}"
        )
    candidate_query_ids = {
        query["query_id"] for query in queries[:6]
    }
    reached_candidates = {
        candidate_id
        for query_id, unit_id in result_pairs
        if query_id in candidate_query_ids
        for candidate_id in parse_links(
            reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
    }
    expected_candidates = {
        f"B{value:04d}" for value in range(6, 92)
    }
    if reached_candidates != expected_candidates:
        raise AuthoringError(
            "candidate-derived Stage 6 queries do not reach exactly "
            "B0006..B0091: "
            f"missing={sorted(expected_candidates - reached_candidates)} "
            f"unexpected={sorted(reached_candidates - expected_candidates)}"
        )
    hit_start = sum(len(record.get("hits", [])) for record in rounds) + 1
    hits: list[dict[str, Any]] = []
    for offset, (query_id, unit_id) in enumerate(result_pairs):
        row = reading_by_id[unit_id]
        candidate_ids = parse_links(
            row["candidate_ids"], f"{unit_id}.candidate_ids"
        )
        route_ids = parse_links(row["route_ids"], f"{unit_id}.route_ids")
        if candidate_ids:
            disposition = "GOVERNED_CANDIDATE_OR_SUPPORT"
            rationale = (
                "Sequential context review already captured this hit as "
                "candidate identity, mechanics, evidence, or a typed support "
                "relation for the linked blind candidate."
            )
        elif route_ids:
            disposition = "CROSS_REFERENCE"
            rationale = (
                "Sequential context review identified this hit as a locator "
                "whose construction-bearing target is governed by the linked "
                "route rather than by a new local candidate."
            )
        elif row["review_disposition"] == "REPRESENTATION_OR_OBSERVER":
            disposition = "CONTROL_OR_RELATIONSHIP"
            rationale = (
                "Sequential context review identifies this hit as a display, "
                "implementation, representation, application, comparison, or "
                "other non-native relationship."
            )
        elif row["review_disposition"] in {
            "NO_CONSTRUCTION",
            "HISTORICAL_ONLY",
        }:
            disposition = "EXCLUSION"
            rationale = (
                "Sequential context review finds framing, behavior, history, "
                "or incidental terminology without both an identity and a "
                "native semantic anchor."
            )
        else:
            raise AuthoringError(
                f"search hit {unit_id} has an ungoverned sequential "
                f"disposition: {row['review_disposition']}"
            )
        hits.append(
            {
                "hit_id": f"H{hit_start + offset:06d}",
                "query_id": query_id,
                "source_unit_id": unit_id,
                "context_sha256": unit_by_id[unit_id]["sha256"],
                "disposition": disposition,
                "candidate_ids": candidate_ids,
                "route_ids": route_ids,
                "rationale": rationale,
            }
        )

    first_pass = len(prior_stage_rounds) == 0
    new_vocabulary = NEW_VOCABULARY if first_pass else []
    round_record: dict[str, Any] = {
        "round_id": f"S{len(rounds) + 1:03d}",
        "epoch": 1,
        "kind": "LOCAL",
        "owning_stage": 6,
        "queries": queries,
        "tool_assumptions": [ASSUMPTION],
        "result_ids": [hit["hit_id"] for hit in hits],
        "result_digest": "",
        "hits": hits,
        "new_vocabulary": new_vocabulary,
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest

    proposed_search = deepcopy(search)
    if proposed_search.get("tool_assumptions") != [ASSUMPTION]:
        raise AuthoringError("unexpected global search assumptions")
    if first_pass:
        existing = proposed_search.get("vocabulary")
        if not isinstance(existing, list) or any(
            item in existing for item in NEW_VOCABULARY
        ):
            raise AuthoringError("Stage 6 vocabulary already present or malformed")
        proposed_search["vocabulary"].extend(NEW_VOCABULARY)
    elif proposed_search.get("vocabulary", [])[-len(NEW_VOCABULARY) :] != (
        NEW_VOCABULARY
    ):
        raise AuthoringError("prior Stage 6 vocabulary differs")
    proposed_search["rounds"].append(round_record)

    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "ch02-experiment-local-search-e1",
        "epoch": 1,
        "source_paths": [],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "reading_updates": [],
        "asset_updates": [],
        "candidate_updates": [],
        "route_appends": [],
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
        print(f"Chapter 2 search authoring failed: {exc}", file=sys.stderr)
        return 1
    round_record = proposal["proposed_search"]["rounds"][-1]
    counts: dict[str, int] = {}
    for hit in round_record["hits"]:
        counts[hit["disposition"]] = counts.get(hit["disposition"], 0) + 1
    print(
        f"authored {round_record['round_id']}: "
        f"queries={len(round_record['queries'])} "
        f"hits={len(round_record['hits'])} "
        f"new_vocabulary={len(round_record['new_vocabulary'])} "
        f"dispositions={json.dumps(counts, sort_keys=True)} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
