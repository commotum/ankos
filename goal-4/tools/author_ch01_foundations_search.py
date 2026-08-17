#!/usr/bin/env python3
"""Author one closed Stage 5 Chapter 1 LOCAL-search proposal.

The first invocation appends the candidate-derived/guardrail seed pass and
repairs the already-routed Chapter 3 locator's primary disposition.  The
second invocation repeats the frozen query family with no new vocabulary or
semantic deltas, establishing the required local zero-delta closure.
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
    "CHAPTERS/01-The-Foundations-for-a-New-Kind-of-Science/01-The-Foundations-for-a-New-Kind-of-Science.md",
    "BACK-MATTER/NOTES/01-The-Foundations-for-a-New-Kind-of-Science-Notes/01-The-Foundations-for-a-New-Kind-of-Science-Notes.md",
]

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with MULTILINE semantics and query-major then "
    "canonical source-unit result order."
)

NEW_VOCABULARY = [
    "elementary cellular automata",
    "random initial conditions",
    "middle-square",
    "bouncing disks",
    "collision",
    "discrete particles",
    "square grid",
    "conservation laws",
    "particle cellular automaton",
    "register machine",
    "logic",
    "statistical physics",
]

QUERY_SPECS = [
    ("candidate subtype", "elementary cellular automata", "LITERAL"),
    ("candidate family", r"\bcellular automat(?:on|a)\b", "REGEX"),
    ("candidate seed", "random initial conditions", "LITERAL"),
    (
        "particle/disk mechanics",
        (
            r"\b(?:disks?|particles?|collid(?:e|es|ed|ing|isions?)|"
            r"square grid|conservation laws?)\b"
        ),
        "REGEX",
    ),
    ("seed generator", "middle-square", "LITERAL"),
    (
        "native evolution mechanics",
        (
            r"\b(?:initial conditions?|successive rows?|evolution steps?|"
            r"neighbou?rs?|transitions?|updates?|synchronous|asynchronous)\b"
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
            r"Turing machines?|register machines?|mobile automata|automaton)\b"
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

GOVERNED_UNITS = {
    "U000149": ["B0003"],
    "U000150": ["B0003"],
    "U000153": ["B0003"],
    "U004951": ["B0004"],
    "U004952": ["B0005"],
    "U004953": ["B0003"],
}

CONTROL_UNITS = {
    "U000100",
    "U000101",
    "U000104",
    "U000105",
    "U000106",
    "U000107",
    "U000109",
    "U000110",
    "U000111",
    "U000114",
    "U000115",
    "U004928",
    "U004932",
    "U004942",
    "U004943",
    "U004945",
    "U004946",
    "U004949",
}

EXCLUSION_UNITS = {
    "U000073",
    "U000075",
    "U000076",
    "U000077",
    "U000078",
    "U000079",
    "U000081",
    "U000082",
    "U000083",
    "U000084",
    "U000085",
    "U000086",
    "U000087",
    "U000088",
    "U000089",
    "U000090",
    "U000091",
    "U000092",
    "U000093",
    "U000094",
    "U000095",
    "U000096",
    "U000097",
    "U000098",
    "U000099",
    "U000118",
    "U000119",
    "U000121",
    "U000123",
    "U000124",
    "U000125",
    "U000126",
    "U000127",
    "U000128",
    "U000129",
    "U000130",
    "U000131",
    "U000132",
    "U000133",
    "U000134",
    "U000136",
    "U000139",
    "U000140",
    "U000141",
    "U000144",
    "U000145",
    "U000146",
    "U000147",
    "U000148",
    "U000155",
    "U000159",
    "U000161",
    "U000162",
    "U000163",
    "U000164",
    "U000171",
    "U000173",
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
    "U004941",
    "U004955",
    "U004956",
    "U004957",
}


class AuthoringError(ValueError):
    """The current state cannot safely receive the closed Stage 5 proposal."""


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
        "B0001",
        "B0002",
        "B0003",
        "B0004",
        "B0005",
    ]:
        raise AuthoringError("candidate allocation differs from B0001..B0005")
    if [row.get("route_id") for row in routes] != [
        f"R{value:06d}" for value in range(1, 12)
    ]:
        raise AuthoringError("route allocation differs from R000001..R000011")
    if len(history) < 4 or history[3].get("mode") != "INITIAL":
        raise AuthoringError("Stage 5 INITIAL history event is absent")
    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 5 cannot author against a fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list) or len(rounds) not in {2, 3}:
        raise AuthoringError("expected two Stage 4 rounds and zero/one Stage 5 round")
    if any(
        record.get("kind") != "LOCAL"
        or record.get("owning_stage") != 4
        or record.get("epoch") != 1
        for record in rounds[:2]
    ):
        raise AuthoringError("the two prior rounds are not Stage 4 LOCAL rounds")
    prior_stage_rounds = rounds[2:]
    if prior_stage_rounds and (
        prior_stage_rounds[0].get("kind") != "LOCAL"
        or prior_stage_rounds[0].get("owning_stage") != 5
        or prior_stage_rounds[0].get("epoch") != 1
        or prior_stage_rounds[0].get("new_vocabulary") != NEW_VOCABULARY
        or prior_stage_rounds[0].get("new_candidates") != []
        or prior_stage_rounds[0].get("new_evidence_groups") != []
        or prior_stage_rounds[0].get("new_routes") != []
    ):
        raise AuthoringError("prior Stage 5 round is not the expected seed pass")

    reading_by_id = {row["source_unit_id"]: row for row in reading}
    assets_by_path: dict[str, list[dict[str, str]]] = {}
    for row in assets:
        assets_by_path.setdefault(row["assignment_path"], []).append(row)
    for path in STAGE_PATHS:
        path_rows = [row for row in reading if row["path"] == path]
        if not path_rows or any(row["review_status"] != "REVIEWED" for row in path_rows):
            raise AuthoringError(f"Stage 5 source path is not fully reviewed: {path}")
        if any(
            row["inspection_status"] != "SCREENED"
            for row in assets_by_path.get(path, [])
        ):
            raise AuthoringError(f"Stage 5 assets are not fully screened: {path}")

    for unit_id, expected in GOVERNED_UNITS.items():
        actual = parse_links(
            reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
        if actual != expected:
            raise AuthoringError(
                f"{unit_id} candidate allocation differs: {actual} != {expected}"
            )

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

    result_units = {unit_id for _, unit_id in result_pairs}
    disposition_units = set(GOVERNED_UNITS) | CONTROL_UNITS | EXCLUSION_UNITS
    if result_units != disposition_units:
        raise AuthoringError(
            "explicit hit dispositions differ from frozen query results: "
            f"missing={sorted(result_units - disposition_units)} "
            f"stale={sorted(disposition_units - result_units)}"
        )

    hit_start = sum(len(record.get("hits", [])) for record in rounds) + 1
    unit_by_id = {unit["id"]: unit for unit in units}
    hits: list[dict[str, Any]] = []
    for offset, (query_id, unit_id) in enumerate(result_pairs):
        route_ids = ["R000007"] if unit_id == "U004946" else []
        if unit_id in GOVERNED_UNITS:
            disposition = "GOVERNED_CANDIDATE_OR_SUPPORT"
            candidate_ids = GOVERNED_UNITS[unit_id]
            rationale = (
                "Sequential context review already captured this hit as "
                "identity, mechanics, or support for the linked blind candidate."
            )
        elif unit_id in CONTROL_UNITS:
            disposition = "CONTROL_OR_RELATIONSHIP"
            candidate_ids = []
            rationale = (
                "Sequential context review identifies this hit as application, "
                "representation, comparison, or an already-routed locator, not "
                "a new native construction."
            )
        else:
            disposition = "EXCLUSION"
            candidate_ids = []
            rationale = (
                "Sequential context review finds framing, history, behavior, "
                "or incidental terminology without both an identity and native "
                "semantic anchor."
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
        "owning_stage": 5,
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
            raise AuthoringError("Stage 5 vocabulary already present or malformed")
        proposed_search["vocabulary"].extend(NEW_VOCABULARY)
    else:
        if proposed_search.get("vocabulary", [])[-len(NEW_VOCABULARY) :] != (
            NEW_VOCABULARY
        ):
            raise AuthoringError("prior Stage 5 vocabulary differs")
    proposed_search["rounds"].append(round_record)

    reading_updates: list[dict[str, str]] = []
    source_paths: list[str] = []
    if first_pass:
        row = deepcopy(reading_by_id["U004946"])
        if (
            row["review_disposition"] != "REPRESENTATION_OR_OBSERVER"
            or parse_links(row["route_ids"], "U004946.route_ids") != ["R000007"]
        ):
            raise AuthoringError("U004946 does not have the expected routed state")
        row["review_disposition"] = "CROSS_REFERENCE"
        row["evidence_statement"] = (
            "The unit names Turing machines and register machines only as "
            "Chapter 3 examples; R000007 routes their mechanics to that "
            "assigned range."
        )
        reading_updates.append(row)
        source_paths.append(STAGE_PATHS[1])

    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "ch01-foundations-local-search-e1",
        "epoch": 1,
        "source_paths": source_paths,
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "reading_updates": reading_updates,
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
            payload = canonical_json_bytes(proposal)
            atomic_create(output_path, payload)
    except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"Chapter 1 search authoring failed: {exc}", file=sys.stderr)
        return 1
    round_record = proposal["proposed_search"]["rounds"][-1]
    print(
        f"authored {round_record['round_id']}: "
        f"queries={len(round_record['queries'])} "
        f"hits={len(round_record['hits'])} "
        f"new_vocabulary={len(round_record['new_vocabulary'])} "
        f"reading_updates={len(proposal['reading_updates'])} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
