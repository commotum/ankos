#!/usr/bin/env python3
"""Author one closed Stage 8 Chapter 4 main-text epoch-2 LOCAL search.

The governed reopen changed only the Chapter 4 main-text review projection,
so this reproducer scopes the frozen fourteen-family Stage 8 query pass to
that path alone.  Its first invocation authors S011 with no semantic delta;
after that proposal is applied, its second invocation authors S012 and
requires an identical normalized hit projection.

This helper only creates a coordinator proposal.  It never applies a ledger
transaction.
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

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import audit_transaction  # noqa: E402
import author_ch04_numbers_search as epoch1  # noqa: E402
import merge_worker_output  # noqa: E402
import validate_audit  # noqa: E402
from audit_contract import (  # noqa: E402
    GOAL_DIR,
    REPO_ROOT,
    canonical_json_bytes,
)


STAGE_PATH = "CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md"
STAGE_PATHS = [STAGE_PATH]
STAGE = 8
EPOCH = 2
COORDINATOR_ID = "ch04-numbers-reopen-local-search-e2"

# These are aliases, not revised variants: drift in the epoch-1 source helper
# is independently caught by the frozen digests below.
QUERY_SPECS = epoch1.QUERY_SPECS
PROPOSED_VOCABULARY = epoch1.PROPOSED_VOCABULARY
ASSUMPTION = epoch1.ASSUMPTION

EXPECTED_QUERY_SPEC_DIGEST = (
    "e6e91221014bcd0e3d89aab0ca7f7e6920cbd4f6dcd40ed95b783045f2a643f5"
)
EXPECTED_STAGE_VOCABULARY_DIGEST = (
    "328ffb1b80a8ca96569df416063c4a30fb4cda914636e983c8fef2c656aa848c"
)
EXPECTED_GLOBAL_VOCABULARY_COUNT = 278
EXPECTED_GLOBAL_VOCABULARY_DIGEST = (
    "c64476dc6d098a2038f4199de3456ec2ef16150a76d05f9ebc3d28b31f5ab4ae"
)
EXPECTED_TOOL_ASSUMPTIONS_COUNT = 2
EXPECTED_TOOL_ASSUMPTIONS_DIGEST = (
    "671219eeacdded499c971a237e87b358ec687bfb6f085425d101d5d007a20afd"
)

EXPECTED_STAGE_UNIT_COUNT = 306
EXPECTED_STAGE_ASSET_COUNT = 63
EXPECTED_STAGE_CANDIDATE_COUNT = 148
EXPECTED_STAGE_UNIT_IDS_DIGEST = (
    "f217c01010760916a8f9b4be1a9120978fcc7bfdcf100d7953d6f6ccd7d0ea20"
)
EXPECTED_STAGE_READING_DIGEST = (
    "7fd995a9194f583d6c5af504bd3bda1b9106d6391556aac09bf83af0f6e6a456"
)
EXPECTED_STAGE_ASSET_DIGEST = (
    "06f08c9e05b69cf968b4ad5037482ccbd33a74429e12e7fb6c69245c3a79bc10"
)
EXPECTED_STAGE_CANDIDATE_IDS_DIGEST = (
    "8215f4540372d3eac72c07a80d9a014a991263fcbd036aa9954ba2fc284d32b4"
)

EXPECTED_RESULT_PAIR_COUNT = 856
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 285
EXPECTED_HIT_COUNTS = [
    80,
    38,
    9,
    25,
    77,
    14,
    13,
    19,
    252,
    63,
    28,
    58,
    68,
    112,
]
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "ee38595011b842b9375bfec4b21e534e26c8563c7948e879933fdd92775717bf"
)
EXPECTED_TRIAGE_DIGEST = (
    "d05c7d2308ce0d87a47b36ac6432ef2d3e7e5b1f3329096108c9bb843aa03e8d"
)
EXPECTED_CANDIDATE_COVERAGE_DIGEST = (
    "4ebbe6fe0f9b06db394cae37c545c33206fc40a674f224d127138f7f2d689ba9"
)
EXPECTED_OMISSION_CHALLENGE_COUNT = 265
EXPECTED_OMISSION_CHALLENGE_DIGEST = (
    "31daddbb7772f66579a3e307be7b0683c14daff991e607902dc4bb743dec9549"
)
EXPECTED_NORMALIZED_HIT_PROJECTION_DIGEST = (
    "09b4855a6d01cc5c157349ca917933f6f1c5b13cc11a567a80aada7d5f0d748e"
)
EXPECTED_DISPOSITION_COUNTS = {
    "CONTROL_OR_RELATIONSHIP": 80,
    "CROSS_REFERENCE": 6,
    "EXCLUSION": 335,
    "GOVERNED_CANDIDATE_OR_SUPPORT": 435,
}

EXPECTED_QUERY_START = {"S011": 121, "S012": 135}
EXPECTED_HIT_START = {"S011": 8483, "S012": 9339}
EXPECTED_ROUND_DIGESTS = {
    "S011": "70dbb5972f19d06a6ccc474abc361a4dc763bf156e6eb8fd656055b7c36fa3ab",
    "S012": "74758e6065e6fa9b69b384451f5f29dac7497bea5d398f5448c4c1653d01b924",
}
EXPECTED_PRIOR_HISTORY = {
    "S011": {
        "review_id": "V000020",
        "event_sha256": (
            "ae9280080788afb1f36aba23c41cd8d85e2c12a7b129d43728d8c34e23e54907"
        ),
        "mode": "REOPEN",
        "reviewer": "ch04-numbers-reopen-e2",
    },
    # Deterministic V000021 successor established by the S011 dry-run.
    "S012": {
        "review_id": "V000021",
        "event_sha256": (
            "4f20ac3a0232440c639a91104973c037c663e4f859d9df1bc75fc9c55fac99dc"
        ),
        "mode": "SEARCH_APPEND",
        "reviewer": COORDINATOR_ID,
    },
}

# S011 is hard-bound to the exact V000020 authoritative ledger snapshot.
# S012 is separately bound to the deterministic V000021 successor produced
# by applying that exact S011 proposal.
EXPECTED_BASE_SHA256_BY_ROUND = {
    "S011": {
        "candidate-ledger.jsonl": (
            "11c1da78335cc690161e1f65cf1a4446cfd0915409c7d7164fd7b649440d32d9"
        ),
        "cross-reference-ledger.csv": (
            "7c4b254601904a04530ae1859cd528c54e834c57fe716af043e7697bc979137f"
        ),
        "reading-ledger.csv": (
            "ffeada81cc7fd287920ba34a15a4c38ff11bc6763fc256f3f5c0942c85fa4b5b"
        ),
        "asset-ledger.csv": (
            "ebe56581896a81e638a2e39f5b6f5d8567abe055464e85613ae6a5310a39ddf5"
        ),
        "search-rounds.json": (
            "4988a7e0471a0e9fffa3377e5e99c22d4ced733083842f475f2b71e9f4713b6d"
        ),
        "review-history.jsonl": (
            "9cfe9ae503d65433598612295f3eb9086fff6a0a6a6d14460a58f5f77f9dc185"
        ),
    },
    "S012": {
        "candidate-ledger.jsonl": (
            "11c1da78335cc690161e1f65cf1a4446cfd0915409c7d7164fd7b649440d32d9"
        ),
        "cross-reference-ledger.csv": (
            "7c4b254601904a04530ae1859cd528c54e834c57fe716af043e7697bc979137f"
        ),
        "reading-ledger.csv": (
            "ffeada81cc7fd287920ba34a15a4c38ff11bc6763fc256f3f5c0942c85fa4b5b"
        ),
        "asset-ledger.csv": (
            "ebe56581896a81e638a2e39f5b6f5d8567abe055464e85613ae6a5310a39ddf5"
        ),
        "search-rounds.json": (
            "7a4cd6acf818812144cc93d00dc73d53b7ceeed6146700fb30105ead21dadbe2"
        ),
        "review-history.jsonl": (
            "caa112bb28cb010bc504b572a7034b56fa4d4cef755ea3edc45132eead6e33be"
        ),
    },
}


class AuthoringError(ValueError):
    """The live state cannot safely receive this exact search proposal."""


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def artifact_digests(goal_dir: Path) -> dict[str, str]:
    return {
        name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
        for name in merge_worker_output.WRITE_NAMES
    }


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


def parse_links(value: str, label: str) -> list[str]:
    return epoch1.parse_links(value, label)


def round_queries_match(
    round_record: dict[str, Any],
    *,
    expected_start: int,
) -> bool:
    expected = [
        {
            "query_id": f"Q{expected_start + offset:04d}",
            "family": family,
            "pattern": pattern,
            "mode": mode,
            "case_sensitive": False,
            "whole_word": False,
            "scope_paths": STAGE_PATHS,
        }
        for offset, (family, pattern, mode) in enumerate(QUERY_SPECS)
    ]
    return round_record.get("queries") == expected


def require_prior_rounds(rounds: list[dict[str, Any]]) -> str:
    if len(rounds) not in {10, 11}:
        raise AuthoringError(
            "expected ten closed epoch-1 rounds and zero/one epoch-2 "
            f"Stage 8 round, got {len(rounds)}"
        )
    expected_prefix = [
        ("S001", "LOCAL", 4, 1),
        ("S002", "LOCAL", 4, 1),
        ("S003", "LOCAL", 5, 1),
        ("S004", "LOCAL", 5, 1),
        ("S005", "LOCAL", 6, 1),
        ("S006", "LOCAL", 6, 1),
        ("S007", "LOCAL", 7, 1),
        ("S008", "LOCAL", 7, 1),
        ("S009", "LOCAL", 8, 1),
        ("S010", "LOCAL", 8, 1),
    ]
    observed_prefix = [
        (
            record.get("round_id"),
            record.get("kind"),
            record.get("owning_stage"),
            record.get("epoch"),
        )
        for record in rounds[:10]
    ]
    if observed_prefix != expected_prefix:
        raise AuthoringError(
            "the closed LOCAL-round prefix through Stage 8 epoch 1 drifted"
        )
    query_start = sum(
        len(record.get("queries", [])) for record in rounds[:8]
    ) + 1
    seed, rerun = rounds[8:10]
    if (
        not epoch1._round_queries_match(seed, expected_start=query_start)
        or not epoch1._round_queries_match(
            rerun,
            expected_start=query_start + len(QUERY_SPECS),
        )
        or seed.get("new_vocabulary") != PROPOSED_VOCABULARY
        or rerun.get("new_vocabulary") != []
        or any(
            record.get(field) != []
            for record in (seed, rerun)
            for field in (
                "new_candidates",
                "new_evidence_groups",
                "new_routes",
            )
        )
        or seed.get("result_digest")
        != epoch1.EXPECTED_ROUND_DIGESTS["S009"]
        or rerun.get("result_digest")
        != epoch1.EXPECTED_ROUND_DIGESTS["S010"]
        or epoch1._normalized_hit_projection(seed)
        != epoch1._normalized_hit_projection(rerun)
    ):
        raise AuthoringError(
            "the closed Stage 8 epoch-1 seed/rerun pair drifted"
        )
    round_id = f"S{len(rounds) + 1:03d}"
    if round_id == "S012":
        prior = rounds[10]
        if (
            prior.get("round_id") != "S011"
            or prior.get("kind") != "LOCAL"
            or prior.get("owning_stage") != STAGE
            or prior.get("epoch") != EPOCH
            or not round_queries_match(
                prior,
                expected_start=EXPECTED_QUERY_START["S011"],
            )
            or prior.get("tool_assumptions") != [ASSUMPTION]
            or prior.get("result_digest")
            != EXPECTED_ROUND_DIGESTS["S011"]
            or prior.get("rerun_digest")
            != EXPECTED_ROUND_DIGESTS["S011"]
            or any(
                prior.get(field) != []
                for field in (
                    "new_vocabulary",
                    "new_candidates",
                    "new_evidence_groups",
                    "new_routes",
                )
            )
            or digest(epoch1._normalized_hit_projection(prior))
            != EXPECTED_NORMALIZED_HIT_PROJECTION_DIGEST
        ):
            raise AuthoringError(
                "the existing Stage 8 epoch-2 S011 seed pass drifted"
            )
    return round_id


def require_prior_history(
    history: list[dict[str, Any]],
    round_id: str,
) -> None:
    expected_length = 20 if round_id == "S011" else 21
    if len(history) != expected_length:
        raise AuthoringError(
            f"{round_id} expected {expected_length} review events, "
            f"got {len(history)}"
        )
    for number, event in enumerate(history, start=1):
        if event.get("review_id") != f"V{number:06d}":
            raise AuthoringError("review-history ID sequence drifted")
    reopen = history[19]
    if (
        reopen.get("review_id") != "V000020"
        or reopen.get("stage") != STAGE
        or reopen.get("epoch") != EPOCH
        or reopen.get("mode") != "REOPEN"
        or reopen.get("reviewer") != "ch04-numbers-reopen-e2"
        or reopen.get("source_paths") != STAGE_PATHS
        or reopen.get("event_sha256")
        != EXPECTED_PRIOR_HISTORY["S011"]["event_sha256"]
    ):
        raise AuthoringError("the governed V000020 reopen event drifted")
    expected = EXPECTED_PRIOR_HISTORY[round_id]
    prior = history[-1]
    if any(
        prior.get(field) != expected[field]
        for field in ("review_id", "event_sha256", "mode", "reviewer")
    ) or prior.get("stage") != STAGE or prior.get("epoch") != EPOCH:
        raise AuthoringError(
            f"{round_id} prior review-history terminal event drifted"
        )


def require_stage_route_state(routes: list[dict[str, str]]) -> None:
    epoch1._require_stage8_route_state(routes)


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to canonical Goal 4")
    if len(QUERY_SPECS) != 14 or len(PROPOSED_VOCABULARY) != len(
        set(PROPOSED_VOCABULARY)
    ):
        raise AuthoringError("the frozen Stage 8 query/vocabulary source is malformed")
    if digest(QUERY_SPECS) != EXPECTED_QUERY_SPEC_DIGEST:
        raise AuthoringError("the frozen fourteen-family query specification drifted")
    if digest(PROPOSED_VOCABULARY) != EXPECTED_STAGE_VOCABULARY_DIGEST:
        raise AuthoringError("the frozen Stage 8 vocabulary contribution drifted")

    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    reading = read_csv(goal_dir / merge_worker_output.READING_NAME)
    assets = read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    candidates = read_jsonl(goal_dir / merge_worker_output.CANDIDATE_NAME)
    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(encoding="utf-8")
    )
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)

    if search.get("fixed_point") is not None:
        raise AuthoringError("epoch-2 LOCAL closure cannot follow a fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise AuthoringError("global search rounds are malformed")
    round_id = require_prior_rounds(rounds)
    require_prior_history(history, round_id)

    base_digests = artifact_digests(goal_dir)
    expected_base = EXPECTED_BASE_SHA256_BY_ROUND[round_id]
    if not expected_base or base_digests != expected_base:
        raise AuthoringError(
            f"{round_id} authoritative base-artifact snapshot drifted"
        )

    vocabulary = search.get("vocabulary")
    assumptions = search.get("tool_assumptions")
    if (
        not isinstance(vocabulary, list)
        or len(vocabulary) != EXPECTED_GLOBAL_VOCABULARY_COUNT
        or len(vocabulary) != len(set(vocabulary))
        or digest(vocabulary) != EXPECTED_GLOBAL_VOCABULARY_DIGEST
        or vocabulary[-len(PROPOSED_VOCABULARY) :] != PROPOSED_VOCABULARY
    ):
        raise AuthoringError("global vocabulary or its Stage 8 suffix drifted")
    if (
        not isinstance(assumptions, list)
        or len(assumptions) != EXPECTED_TOOL_ASSUMPTIONS_COUNT
        or len(assumptions) != len(set(assumptions))
        or digest(assumptions) != EXPECTED_TOOL_ASSUMPTIONS_DIGEST
        or ASSUMPTION not in assumptions
    ):
        raise AuthoringError("global search assumptions drifted")
    if [
        value for value in PROPOSED_VOCABULARY if value not in vocabulary
    ]:
        raise AuthoringError("Stage 8 vocabulary is not fully present")

    unit_by_id = {unit["id"]: unit for unit in units}
    reading_by_id = {row["source_unit_id"]: row for row in reading}
    candidates_by_id = {row["id"]: row for row in candidates}
    if len(unit_by_id) != len(units):
        raise AuthoringError("source units contain duplicate IDs")
    if len(reading_by_id) != len(reading):
        raise AuthoringError("reading ledger contains duplicate source-unit IDs")
    if len(candidates_by_id) != len(candidates):
        raise AuthoringError("candidate ledger contains duplicate IDs")
    route_ids = {row["route_id"] for row in routes}
    if len(route_ids) != len(routes):
        raise AuthoringError("cross-reference ledger contains duplicate IDs")
    require_stage_route_state(routes)

    stage_units = [unit for unit in units if unit["path"] == STAGE_PATH]
    stage_unit_ids = {unit["id"] for unit in stage_units}
    stage_reading = [
        row for row in reading if row["source_unit_id"] in stage_unit_ids
    ]
    stage_assets = [
        row for row in assets if row["assignment_path"] == STAGE_PATH
    ]
    if (
        len(stage_units) != EXPECTED_STAGE_UNIT_COUNT
        or len(stage_unit_ids) != EXPECTED_STAGE_UNIT_COUNT
        or digest([unit["id"] for unit in stage_units])
        != EXPECTED_STAGE_UNIT_IDS_DIGEST
    ):
        raise AuthoringError("reopened Chapter 4 main source-unit projection drifted")
    if (
        len(stage_reading) != EXPECTED_STAGE_UNIT_COUNT
        or any(
            row["path"] != STAGE_PATH
            or row["review_status"] != "REVIEWED"
            or row["review_epoch"] != str(EPOCH)
            or row["review_stage"] != str(STAGE)
            or row["reviewer"] != "ch04-numbers-reopen-e2"
            for row in stage_reading
        )
        or digest(stage_reading) != EXPECTED_STAGE_READING_DIGEST
    ):
        raise AuthoringError("reopened Chapter 4 main reading projection drifted")
    if (
        len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT
        or any(
            row["inspection_status"] != "SCREENED"
            or row["review_epoch"] != str(EPOCH)
            or row["review_stage"] != str(STAGE)
            or row["reviewer"] != "ch04-numbers-reopen-e2"
            for row in stage_assets
        )
        or digest(stage_assets) != EXPECTED_STAGE_ASSET_DIGEST
    ):
        raise AuthoringError("reopened Chapter 4 main asset projection drifted")

    linked_from_reading = {
        candidate_id
        for row in stage_reading
        for candidate_id in parse_links(
            row["candidate_ids"],
            f"{row['source_unit_id']}.candidate_ids",
        )
    }
    linked_from_assets = {
        candidate_id
        for row in stage_assets
        for candidate_id in parse_links(
            row["candidate_ids"],
            f"{row['asset_id']}.candidate_ids",
        )
    }
    evidenced_in_stage = {
        candidate["id"]
        for candidate in candidates
        if candidate.get("record_status") == "ACTIVE"
        and isinstance(candidate.get("source_evidence"), list)
        and any(
            evidence.get("source_unit_id") in stage_unit_ids
            for evidence in candidate["source_evidence"]
            if isinstance(evidence, dict)
        )
    }
    expected_candidates = (
        linked_from_reading | linked_from_assets | evidenced_in_stage
    )
    if (
        len(expected_candidates) != EXPECTED_STAGE_CANDIDATE_COUNT
        or digest(sorted(expected_candidates))
        != EXPECTED_STAGE_CANDIDATE_IDS_DIGEST
    ):
        raise AuthoringError(
            "dynamically derived reopened-path candidate target drifted"
        )
    unknown_or_inactive = {
        candidate_id
        for candidate_id in expected_candidates
        if candidate_id not in candidates_by_id
        or candidates_by_id[candidate_id].get("record_status") != "ACTIVE"
    }
    if unknown_or_inactive:
        raise AuthoringError(
            "reopened-path relationships reach unknown/inactive candidates: "
            f"{sorted(unknown_or_inactive)}"
        )
    for row in stage_reading:
        unknown_routes = set(
            parse_links(row["route_ids"], f"{row['source_unit_id']}.route_ids")
        ) - route_ids
        if unknown_routes:
            raise AuthoringError(
                f"{row['source_unit_id']} links unknown routes: "
                f"{sorted(unknown_routes)}"
            )

    query_start = sum(len(record.get("queries", [])) for record in rounds) + 1
    hit_start = sum(len(record.get("hits", [])) for record in rounds) + 1
    if (
        query_start != EXPECTED_QUERY_START[round_id]
        or hit_start != EXPECTED_HIT_START[round_id]
    ):
        raise AuthoringError(
            f"{round_id} query/hit sequence start drifted: "
            f"Q{query_start:04d}/H{hit_start:06d}"
        )
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
    if not round_queries_match(
        {"queries": queries},
        expected_start=query_start,
    ):
        raise AuthoringError("authored query objects differ from the frozen scope")
    result_pairs, query_errors = validate_audit.execute_frozen_queries(
        queries,
        units,
        REPO_ROOT / "ref" / "A-New-Kind-of-Science",
    )
    if query_errors:
        raise AuthoringError("; ".join(query_errors))
    if len(result_pairs) != EXPECTED_RESULT_PAIR_COUNT:
        raise AuthoringError(
            f"reopened-path result-pair count drifted: {len(result_pairs)}"
        )
    if any(unit_by_id[unit_id]["path"] != STAGE_PATH for _, unit_id in result_pairs):
        raise AuthoringError("a query result escaped the reopened Chapter 4 path")
    hit_counts = [
        sum(query_id == query["query_id"] for query_id, _ in result_pairs)
        for query in queries
    ]
    if hit_counts != EXPECTED_HIT_COUNTS:
        raise AuthoringError(
            f"reopened-path query hit counts drifted: {hit_counts}"
        )
    normalized_pairs = epoch1._normalized_result_pairs(
        result_pairs,
        query_start,
    )
    if digest(normalized_pairs) != EXPECTED_NORMALIZED_RESULT_DIGEST:
        raise AuthoringError("normalized query/result-pair projection drifted")

    result_unit_ids = sorted({unit_id for _, unit_id in result_pairs})
    if len(result_unit_ids) != EXPECTED_UNIQUE_RESULT_UNIT_COUNT:
        raise AuthoringError(
            "reopened-path unique result-unit count drifted: "
            f"{len(result_unit_ids)}"
        )
    triage_projection = [
        (
            unit_id,
            reading_by_id[unit_id]["review_disposition"],
            reading_by_id[unit_id]["source_status"],
            parse_links(
                reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            ),
            parse_links(
                reading_by_id[unit_id]["route_ids"],
                f"{unit_id}.route_ids",
            ),
        )
        for unit_id in result_unit_ids
    ]
    if digest(triage_projection) != EXPECTED_TRIAGE_DIGEST:
        raise AuthoringError("reopened-path search triage projection drifted")

    candidate_query_ids = {query["query_id"] for query in queries[:10]}
    reached_candidates = {
        candidate_id
        for query_id, unit_id in result_pairs
        if query_id in candidate_query_ids
        for candidate_id in parse_links(
            reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
    }
    if reached_candidates != expected_candidates:
        raise AuthoringError(
            "candidate-facing queries differ from the reopened-path target: "
            f"missing={sorted(expected_candidates - reached_candidates)} "
            f"unexpected={sorted(reached_candidates - expected_candidates)}"
        )
    candidate_coverage = epoch1._candidate_coverage_projection(
        expected_candidates=expected_candidates,
        candidates_by_id=candidates_by_id,
        reading_by_id=reading_by_id,
        normalized_pairs=normalized_pairs,
        stage_unit_ids=stage_unit_ids,
    )
    if (
        len(candidate_coverage) != EXPECTED_STAGE_CANDIDATE_COUNT
        or digest(candidate_coverage) != EXPECTED_CANDIDATE_COVERAGE_DIGEST
    ):
        raise AuthoringError("reopened-path candidate witness coverage drifted")

    omission_projection: list[tuple[Any, ...]] = []
    for ordinal, unit_id in normalized_pairs:
        if ordinal > 10:
            continue
        row = reading_by_id[unit_id]
        candidate_ids = parse_links(
            row["candidate_ids"], f"{unit_id}.candidate_ids"
        )
        row_route_ids = parse_links(
            row["route_ids"], f"{unit_id}.route_ids"
        )
        if not candidate_ids and not row_route_ids:
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
    if (
        len(omission_projection) != EXPECTED_OMISSION_CHALLENGE_COUNT
        or digest(omission_projection) != EXPECTED_OMISSION_CHALLENGE_DIGEST
    ):
        raise AuthoringError("reopened-path F01-F10 omission challenge drifted")

    hits: list[dict[str, Any]] = []
    for offset, (query_id, unit_id) in enumerate(result_pairs):
        family_ordinal = int(query_id[1:]) - query_start + 1
        row = reading_by_id[unit_id]
        candidate_ids = parse_links(
            row["candidate_ids"], f"{unit_id}.candidate_ids"
        )
        row_route_ids = parse_links(
            row["route_ids"], f"{unit_id}.route_ids"
        )
        if candidate_ids:
            disposition = "GOVERNED_CANDIDATE_OR_SUPPORT"
            rationale = (
                "Sequential context review already captured this hit as "
                "candidate identity, mechanics, evidence, variant, or typed "
                "support for every linked blind candidate."
            )
        elif row_route_ids:
            disposition = "CROSS_REFERENCE"
            rationale = (
                "Sequential context review identified this hit as a locator "
                "whose construction-bearing target is governed by every "
                "linked typed route."
            )
        elif row["review_disposition"] in {
            "REPRESENTATION_OR_OBSERVER",
            "APPLICATION_OR_EMULATION",
        }:
            disposition = "CONTROL_OR_RELATIONSHIP"
            rationale = epoch1._source_specific_rationale(
                family_ordinal=family_ordinal,
                row=row,
                outcome="control/relationship",
            )
        elif row["review_disposition"] == "SOURCE_DEFECT_OR_AMBIGUITY":
            disposition = "CONTROL_OR_RELATIONSHIP"
            rationale = epoch1._source_specific_rationale(
                family_ordinal=family_ordinal,
                row=row,
                outcome="source-defect control",
            )
        elif row["review_disposition"] in {
            "NO_CONSTRUCTION",
            "HISTORICAL_ONLY",
        }:
            disposition = "EXCLUSION"
            rationale = epoch1._source_specific_rationale(
                family_ordinal=family_ordinal,
                row=row,
                outcome="exclusion",
            )
        elif row["review_disposition"] in {
            "CANDIDATE",
            "SUPPORTS_CANDIDATE",
            "CROSS_REFERENCE",
        }:
            raise AuthoringError(
                f"{unit_id} has an unlinked construction-bearing disposition"
            )
        else:
            raise AuthoringError(
                f"{unit_id} has an ungoverned sequential disposition: "
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
            f"reopened-path hit dispositions drifted: {disposition_counts}"
        )

    round_record: dict[str, Any] = {
        "round_id": round_id,
        "epoch": EPOCH,
        "kind": "LOCAL",
        "owning_stage": STAGE,
        "queries": queries,
        "tool_assumptions": [ASSUMPTION],
        "result_ids": [hit["hit_id"] for hit in hits],
        "result_digest": "",
        "hits": hits,
        "new_vocabulary": [],
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    result_digest = validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = result_digest
    round_record["rerun_digest"] = result_digest
    if result_digest != EXPECTED_ROUND_DIGESTS[round_id]:
        raise AuthoringError(
            f"{round_id} result digest drifted: {result_digest}"
        )
    normalized_hit_projection = epoch1._normalized_hit_projection(round_record)
    if (
        digest(normalized_hit_projection)
        != EXPECTED_NORMALIZED_HIT_PROJECTION_DIGEST
    ):
        raise AuthoringError(f"{round_id} normalized hit projection drifted")
    if round_id == "S012" and normalized_hit_projection != (
        epoch1._normalized_hit_projection(rounds[10])
    ):
        raise AuthoringError("S012 differs from the S011 zero-delta projection")

    proposed_search = deepcopy(search)
    proposed_search["rounds"].append(round_record)
    if (
        proposed_search["vocabulary"] != vocabulary
        or proposed_search["tool_assumptions"] != assumptions
        or proposed_search.get("fixed_point") is not None
    ):
        raise AuthoringError("proposal changed global search semantics")
    if any(
        round_record[field]
        for field in (
            "new_vocabulary",
            "new_candidates",
            "new_evidence_groups",
            "new_routes",
        )
    ):
        raise AuthoringError("epoch-2 LOCAL pass has a semantic delta")

    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": COORDINATOR_ID,
        "epoch": EPOCH,
        "source_paths": [],
        "base_artifact_sha256": base_digests,
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
    except (
        OSError,
        json.JSONDecodeError,
        AuthoringError,
        ValueError,
    ) as exc:
        print(f"Chapter 4 reopen search authoring failed: {exc}", file=sys.stderr)
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
        "new_vocabulary=0 new_candidates=0 "
        "new_evidence_groups=0 new_routes=0 "
        f"dispositions={json.dumps(counts, sort_keys=True)} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
