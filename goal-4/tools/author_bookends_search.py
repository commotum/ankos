#!/usr/bin/env python3
"""Author one closed Stage 4 LOCAL-search proposal.

The sequential bookends review is the semantic authority for every hit
disposition below.  This helper only reproduces that explicit review over the
frozen search language, allocates append-only search IDs, and closes the
coordinator proposal against the current six-ledger snapshot.

Run it once after the Stage 4 INITIAL merge and once more after applying the
first proposal.  The first pass introduces the frozen Stage 4 search
vocabulary; the second is the required zero-delta rerun.
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
from audit_contract import (
    ASSET_HEADER,
    GOAL_DIR,
    READING_HEADER,
    REPO_ROOT,
    canonical_json_bytes,
)


STAGE_PATHS = [
    "FRONT-MATTER/00-Publication-and-Contents.md",
    "FRONT-MATTER/01-Preface.md",
    "BACK-MATTER/NOTES/00-General-Notes/00-General-Notes.md",
    "BACK-MATTER/Colophon.md",
]

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with MULTILINE semantics and query-major then "
    "canonical source-unit result order."
)

SEED_VOCABULARY = [
    "rule 30",
    "rule 110",
    "cellular automaton",
    "initial condition",
    "successive row",
    "evolution step",
    "neighbor",
    "transition",
    "update",
    "synchronous",
    "asynchronous",
    "random",
    "randomness",
    "probabilistic",
    "probability",
    "stochastic",
    "Bernoulli",
    "constraint",
    "equation",
    "solution",
    "function",
    "relation",
    "inequality",
    "differential",
    "input",
    "output",
    "generator",
    "substitution",
    "network",
    "Turing machine",
    "mobile automaton",
    "algorithm",
    "program",
    "rule",
    "system",
    "process",
    "simulation",
    "emulation",
    "implementation",
    "representation",
    "display",
    "render",
]

QUERY_SPECS = [
    ("candidate alias", "rule 30", "LITERAL"),
    ("candidate alias", "rule 110", "LITERAL"),
    ("candidate family", "cellular automaton", "LITERAL"),
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
            r"\b(?:random(?:ness)?|probabilistic|probability|stochastic|"
            r"Bernoulli)\b"
        ),
        "REGEX",
    ),
    (
        "declarative-function guardrail",
        (
            r"\b(?:constraints?|equations?|solutions?|functions?|relations?|"
            r"inequalit(?:y|ies)|differential)\b"
        ),
        "REGEX",
    ),
    (
        "input-generator-structure guardrail",
        (
            r"\b(?:inputs?|outputs?|generators?|substitutions?|networks?|"
            r"Turing machines?|mobile automata|automaton)\b"
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

# Every unique Stage 4 hit was inspected in source context.  Keeping these
# identities closed makes a changed query, corpus, or accidental default fail
# before a proposal is written.
GOVERNED_UNITS = {
    "U004864": ["B0001"],
    "U004871": ["B0002"],
    "U004873": ["B0001"],
}

CONTROL_UNITS = {
    "U000024",
    "U000025",
    "U000033",
    "U000068",
    "U004876",
    "U004878",
    "U004880",
    "U004882",
    "U004883",
    "U004884",
    "U004887",
    "U004892",
    "U004895",
    "U004897",
    "U004899",
    "U004901",
    "U004902",
    "U014293",
    "U014295",
    "U014296",
    "U014306",
}

EXCLUSION_UNITS = {
    "U000022",
    "U000027",
    "U000045",
    "U000051",
    "U000059",
    "U000061",
    "U000062",
    "U000063",
    "U004861",
    "U004863",
    "U004903",
    "U004904",
    "U004907",
    "U004913",
    "U004914",
    "U004917",
    "U004921",
    "U004923",
}


class AuthoringError(ValueError):
    """The current state cannot safely receive the closed Stage 4 proposal."""


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

    if [row.get("id") for row in candidates] != ["B0001", "B0002"]:
        raise AuthoringError("Stage 4 candidate allocation differs from B0001/B0002")
    if [row.get("route_id") for row in routes] != [
        "R000001",
        "R000002",
        "R000003",
        "R000004",
    ]:
        raise AuthoringError("Stage 4 route allocation differs from R000001..R000004")
    if not history or history[0].get("mode") != "INITIAL":
        raise AuthoringError("Stage 4 INITIAL history event is absent")
    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 4 cannot author against a fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list) or len(rounds) not in {0, 1}:
        raise AuthoringError("expected zero or one prior Stage 4 LOCAL round")
    if rounds and (
        rounds[0].get("kind") != "LOCAL"
        or rounds[0].get("owning_stage") != 4
        or rounds[0].get("epoch") != 1
        or rounds[0].get("new_vocabulary") != SEED_VOCABULARY
        or rounds[0].get("new_candidates") != []
        or rounds[0].get("new_evidence_groups") != []
        or rounds[0].get("new_routes") != []
    ):
        raise AuthoringError("prior search round is not the expected seed pass")

    reading_by_id = {row["source_unit_id"]: row for row in reading}
    assets_by_path: dict[str, list[dict[str, str]]] = {}
    for row in assets:
        assets_by_path.setdefault(row["assignment_path"], []).append(row)
    for path in STAGE_PATHS:
        path_rows = [row for row in reading if row["path"] == path]
        if not path_rows or any(row["review_status"] != "REVIEWED" for row in path_rows):
            raise AuthoringError(f"Stage 4 source path is not fully reviewed: {path}")
        if any(
            row["inspection_status"] != "SCREENED"
            for row in assets_by_path.get(path, [])
        ):
            raise AuthoringError(f"Stage 4 assets are not fully screened: {path}")

    for unit_id, expected in GOVERNED_UNITS.items():
        actual = parse_links(
            reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
        if actual != expected:
            raise AuthoringError(
                f"{unit_id} candidate allocation differs: {actual} != {expected}"
            )

    query_start = sum(
        len(record.get("queries", []))
        for record in rounds
        if isinstance(record, dict)
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
    source_root = REPO_ROOT / "ref" / "A-New-Kind-of-Science"
    result_pairs, query_errors = validate_audit.execute_frozen_queries(
        queries,
        units,
        source_root,
    )
    if query_errors:
        raise AuthoringError("; ".join(query_errors))

    result_units = {unit_id for _, unit_id in result_pairs}
    disposition_units = (
        set(GOVERNED_UNITS) | CONTROL_UNITS | EXCLUSION_UNITS
    )
    if result_units != disposition_units:
        raise AuthoringError(
            "explicit hit dispositions differ from frozen query results: "
            f"missing={sorted(result_units - disposition_units)} "
            f"stale={sorted(disposition_units - result_units)}"
        )

    hit_start = sum(
        len(record.get("hits", []))
        for record in rounds
        if isinstance(record, dict)
    ) + 1
    unit_by_id = {unit["id"]: unit for unit in units}
    hits: list[dict[str, Any]] = []
    for offset, (query_id, unit_id) in enumerate(result_pairs):
        if unit_id in GOVERNED_UNITS:
            disposition = "GOVERNED_CANDIDATE_OR_SUPPORT"
            candidate_ids = GOVERNED_UNITS[unit_id]
            rationale = (
                "Sequential context review already captured this unit as "
                "identity, mechanics, or support for the linked blind candidate."
            )
        elif unit_id in CONTROL_UNITS:
            disposition = "CONTROL_OR_RELATIONSHIP"
            candidate_ids = []
            rationale = (
                "Sequential context review identifies this match as notation, "
                "tooling, production, representation, experiment control, or "
                "other non-native relationship rather than a new construction."
            )
        else:
            disposition = "EXCLUSION"
            candidate_ids = []
            rationale = (
                "Sequential context review finds framing, history, education, "
                "application, navigation, or incidental wording without both "
                "a construction identity and semantic anchor."
            )
        hits.append(
            {
                "hit_id": f"H{hit_start + offset:06d}",
                "query_id": query_id,
                "source_unit_id": unit_id,
                "context_sha256": unit_by_id[unit_id]["sha256"],
                "disposition": disposition,
                "candidate_ids": candidate_ids,
                "route_ids": [],
                "rationale": rationale,
            }
        )

    first_pass = len(rounds) == 0
    new_vocabulary = SEED_VOCABULARY if first_pass else []
    round_record: dict[str, Any] = {
        "round_id": f"S{len(rounds) + 1:03d}",
        "epoch": 1,
        "kind": "LOCAL",
        "owning_stage": 4,
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
    if first_pass:
        if proposed_search.get("tool_assumptions") != []:
            raise AuthoringError("unexpected preexisting search assumptions")
        if proposed_search.get("vocabulary") != []:
            raise AuthoringError("unexpected preexisting search vocabulary")
        proposed_search["tool_assumptions"].append(ASSUMPTION)
        proposed_search["vocabulary"].extend(SEED_VOCABULARY)
    elif (
        proposed_search.get("tool_assumptions") != [ASSUMPTION]
        or proposed_search.get("vocabulary") != SEED_VOCABULARY
    ):
        raise AuthoringError("prior search assumptions/vocabulary differ")
    proposed_search["rounds"].append(round_record)

    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "bookends-local-search-e1",
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
            payload = canonical_json_bytes(proposal)
            atomic_create(output_path, payload)
    except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"bookends search authoring failed: {exc}", file=sys.stderr)
        return 1
    round_record = proposal["proposed_search"]["rounds"][-1]
    print(
        f"authored {round_record['round_id']}: "
        f"queries={len(round_record['queries'])} "
        f"hits={len(round_record['hits'])} "
        f"new_vocabulary={len(round_record['new_vocabulary'])} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
