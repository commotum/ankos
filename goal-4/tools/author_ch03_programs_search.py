#!/usr/bin/env python3
"""Author one closed Stage 7 Chapter 3 LOCAL-search proposal.

The first invocation appends the mechanically deduplicated Chapter 3
vocabulary and the frozen fourteen-family seed pass.  The second invocation
repeats that exact family with no vocabulary or semantic delta, establishing
the required stage-local zero-delta closure.

This author deliberately derives its candidate coverage target from the live
Stage 7 reading, asset, and evidence relationships.  It never assumes a
numeric B-ID range.
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
    "CHAPTERS/03-The-World-of-Simple-Programs.md",
    "BACK-MATTER/NOTES/03-The-World-of-Simple-Programs-Notes.md",
]

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with IGNORECASE and MULTILINE semantics and "
    "query-major then canonical source-unit result order."
)

PROPOSED_VOCABULARY = [
    "elementary-rule color/reflection equivalence",
    "Boolean-expression rule lookup",
    "rule 51",
    "rule 204",
    "rule 240",
    "rule 22",
    "rule 105",
    "rule 129",
    "rule 150",
    "rule 225",
    "rule 45",
    "rule 73",
    "staggered two-cell-neighborhood cellular automaton",
    "two-cell rule 3826",
    "two-cell rule 5451",
    "two-cell rule 6385",
    "two-cell rule 7743",
    "two-cell rule 8364",
    "two-cell rule 8701",
    "two-cell rule 12294",
    "two-cell rule 16963",
    "two-cell rule 17989",
    "three-color totalistic rule",
    "totalistic code 420",
    "totalistic code 1329",
    "totalistic code 1599",
    "finite-algebraic-system cellular automaton",
    "multiplication-table cellular automaton",
    "S3 cellular automaton",
    "generalized mobile automaton",
    "single active cell",
    "active-cell displacement",
    "multiple active cells",
    "compressed mobile-automaton evolution",
    "Turing-machine rule numbering",
    "blank tape",
    "Busy Beaver",
    "halting-time optimization",
    "neighbor-independent substitution system",
    "neighbor-dependent substitution system",
    "creation-and-destruction substitution",
    "Thue-Morse sequence",
    "Fibonacci substitution sequence",
    "Cantor-set membership sequence",
    "substitution color-count matrix",
    "GoldenRatio constant",
    "Lucas sequence",
    "Perrin sequence",
    "finite-automaton digit transducer",
    "Fibonacci-weighted binary representation",
    "paperfolding sequence",
    "period-doubling sequence",
    "Sturmian sequence",
    "sequential substitution system",
    "ordered replacement",
    "left-to-right scan",
    "tag system",
    "deletion number",
    "append block",
    "Post tag system",
    "cyclic tag system",
    "Kolakoski sequence",
    "increment instruction",
    "decrement-jump instruction",
    "program counter",
    "beyond-program halt",
    "symbolic expression rewriting",
    "fixed-leaf-count expression enumerator",
    "nested-r symbolic rewrite",
    "operator-pattern rewriting",
    "Gray-code rule ordering",
    "multiway rewriting",
    "Church-Rosser confluence",
    "network substitution",
    "L-system",
    "Lorenz equations",
    "iterated map",
]

# The design file was explicitly a pre-main-review draft.  The merged
# candidate-specific witness proof found these five minimal alias additions
# before the family was frozen:
#
# - F03 `states?`: B0157/U000444 and B0257/U005411;
# - F05 `replacements?`: B0178/U000505;
# - F06 `remove[ds]?|removing`: B0184/U000526;
# - F06 `leading elements?`: B0298/U005562 and B0300/U005566; and
# - F07 `registers?|instructions?`: B0197/U000555 and B0201/U000565.
# No family was added, removed, reordered, or broadened after this final
# 229-candidate witness reconciliation.
QUERY_SPECS = [
    (
        "cellular-automaton families, rule codes, and algebraic variants",
        (
            r"\b(?:cellular automat(?:on|a)|CellularAutomaton|"
            r"CA(?:Step|EvolveList)|elementary rules?|totalistic|"
            r"two[- ]cell(?:[- ]neighbou?rhood)?|staggered|"
            r"algebraic systems?|Times|quaternions?|multiplication tables?|"
            r"S[₃3]|BooleanFunction|rules?\s*(?:number\s*)?\d+|"
            r"codes?\s*(?:number\s*)?\d+)\b"
        ),
        "REGEX",
    ),
    (
        "mobile and generalized active-cell automata",
        (
            r"\b(?:mobile automat(?:on|a)|generalized mobile "
            r"automat(?:on|a)|active cells?|MA(?:Step|EvolveList)|GMAStep|"
            r"active[- ]cell (?:position|motion|displacement)|split in two)\b"
        ),
        "REGEX",
    ),
    (
        "Turing machines, numbering, tapes, and halting optimization",
        (
            r"\b(?:Turing machines?|TM(?:Step|EvolveList|Rule)|tapes?|"
            r"head states?|blank tape|halt states?|halting|Busy Beaver|"
            r"rule 1953|states?)\b"
        ),
        "REGEX",
    ),
    (
        "parallel substitution systems and named morphic sequences",
        (
            r"\b(?:substitution systems?|neighbor[- ]independent|"
            r"neighbor[- ]dependent|SS(?:2)?EvolveList|Thue[- ]Morse|"
            r"Fibonacci|Lucas|Perrin|Cantor|paperfolding|"
            r"period[- ]doubling|Sturmian)\b"
        ),
        "REGEX",
    ),
    (
        "sequential substitution and ordered search-replace mechanics",
        (
            r"\b(?:sequential substitution systems?|SSSEvolveList|"
            r"search[- ]and[- ]replace|scan(?:ned|ning)? (?:the )?string|"
            r"left to right|first (?:matching )?(?:sequence|replacement)|"
            r"replacement order|replacements?)\b"
        ),
        "REGEX",
    ),
    (
        "tag, Post, cyclic-tag, and self-descriptive sequence systems",
        (
            r"\b(?:tag systems?|Post(?: tag)?|cyclic tag systems?|"
            r"CT(?:Step|EvolveList)|TSEvolveList|deletion number|"
            r"append(?:ed)? blocks?|tagged onto|Kolakoski|remove[ds]?|"
            r"removing|leading elements?)\b"
        ),
        "REGEX",
    ),
    (
        "register machines and instruction semantics",
        (
            r"\b(?:register machines?|RM(?:Step|Execute)|program counter|"
            r"increment instructions?|decrement[- ]jumps?|"
            r"instruction lists?|register vectors?|registers?|instructions?)\b"
        ),
        "REGEX",
    ),
    (
        "symbolic-expression and operator-pattern rewriting",
        (
            r"\b(?:symbolic systems?|symbolic expressions?|"
            r"operator systems?|expression\s*/\.\s*rule|LeafCount|"
            r"Church[- ]Rosser|Church numerals?|combinators?|"
            r"Polish notation|opening and closing brackets|"
            r"fixed configurations?)\b|e\[x_?\]\[y_?\]"
        ),
        "REGEX",
    ),
    (
        "direct functions, sequences, recurrences, representations, and decoders",
        (
            r"\b(?:sequences?|functions?|recurrences?|representations?|"
            r"transducers?|finite automat(?:on|a)|rule[- ]number"
            r"(?:ing| decoder)?|decod(?:e|es|ed|ing)|GegenbauerC|"
            r"GoldenRatio|DigitCount|IntegerDigits|"
            r"maximi[sz](?:e|es|ed|ing|ation))\b"
        ),
        "REGEX",
    ),
    (
        "nonprose rule, formula, table, and image identity anchors",
        (
            r"(?:^|\n)\s*(?:```|!\[[^\]]*\]\([^)]+\))|"
            r"`[^`\n]*(?:->|∘|Mod\[|Floor\[|Sqrt\[|Nest|Table|"
            r"IntegerDigits|DigitCount|GegenbauerC)[^`\n]*`"
        ),
        "REGEX",
    ),
    (
        "native state, evolution, activation, update, and completion mechanics",
        (
            r"\b(?:initial conditions?|initial states?|seeds?|backgrounds?|"
            r"boundar(?:y|ies)|current states?|successors?|steps?|"
            r"evol(?:ve|ves|ved|ving|ution)|updates?|replacements?|"
            r"rewrit(?:e|es|ing)|remove[ds]?|append(?:s|ed|ing)?|moves?|"
            r"scans?|neighbou?rs?|active|heads?|registers?|fixed points?|"
            r"halts?|termination)\b"
        ),
        "REGEX",
    ),
    (
        "enumeration, preset identity, lookup, and finite rule-space search",
        (
            r"\b(?:enumerat(?:e|es|ed|ing|ion)|possible rules?|"
            r"rule numbers?|code numbers?|lookup(?: table)?|"
            r"multiplication tables?|base[- ]?[234k]|"
            r"randomly (?:chosen|selected) rules?|programs? (?:of )?length|"
            r"states? and (?:two|three|four|five) "
            r"(?:colors?|states?))\b"
        ),
        "REGEX",
    ),
    (
        "stochastic, declarative, constraint, and continuous guardrails",
        (
            r"\b(?:random(?:ness|ly|ization)?|probabilistic|probability|"
            r"stochastic|Bernoulli|sample[sd]?|sampling|constraints?|"
            r"equations?|solutions?|relations?|inequalit(?:y|ies)|"
            r"differential equations?|partial differential|Lorenz|"
            r"iterated maps?|algebraic constants?)\b"
        ),
        "REGEX",
    ),
    (
        "representation, observer, application, and implementation boundary",
        (
            r"\b(?:compress(?:ed|ion)|plots?|displays?|pictures?|"
            r"render(?:s|ed|ing)?|represent(?:s|ed|ing|ation)?|"
            r"implement(?:s|ed|ing|ation)?|"
            r"simulat(?:e|es|ed|ing|ion)|emulat(?:e|es|ed|ing|ion)|"
            r"observers?|analy[sz](?:e|es|ed|ing)|"
            r"measur(?:e|es|ed|ing|ement)|trees?|boxes?|brackets?|"
            r"Mathematica)\b"
        ),
        "REGEX",
    ),
]

# These values are intentionally frozen only after the merged Stage 7 reading,
# asset, candidate, route, and evidence projections exist.  They make source,
# triage, challenge, and candidate-reach drift fail before proposal creation.
EXPECTED_STAGE_UNIT_COUNT = 653
EXPECTED_STAGE_ASSET_COUNT = 133
EXPECTED_STAGE_CANDIDATE_COUNT = 229
EXPECTED_RESULT_PAIR_COUNT = 1247
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 595
EXPECTED_PATH_PAIR_COUNTS = {
    STAGE_PATHS[0]: 606,
    STAGE_PATHS[1]: 641,
}
EXPECTED_PATH_UNIQUE_UNIT_COUNTS = {
    STAGE_PATHS[0]: 297,
    STAGE_PATHS[1]: 298,
}
EXPECTED_QUERY_SPEC_DIGEST = (
    "ecfc9057c4cbfe9dbae6d31b7fcfe43e3d2a453891e0937098c4562c338f33a7"
)
EXPECTED_HIT_COUNTS = [
    134,
    46,
    49,
    83,
    22,
    33,
    37,
    27,
    112,
    254,
    221,
    32,
    43,
    154,
]
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "003108dea049abf52948d1e648ac52688e51ba7f239a2c5cdfaf127fdd268eed"
)
EXPECTED_TRIAGE_DIGEST = (
    "6b6d104ab3428ac7cf626f1999b44c6856826f6a4d96ad763100a9b1e228e3df"
)
EXPECTED_CANDIDATE_COVERAGE_DIGEST = (
    "6328791ffc002cf6dd18282c30ada2c2a92fa6995d03dadf27039f6ddf07a880"
)
EXPECTED_OMISSION_CHALLENGE_COUNT = 266
EXPECTED_OMISSION_CHALLENGE_DIGEST = (
    "1e8b273abca746fbdd4b041205f8e0952db133de23bcff7c3e4296d07d0f067c"
)
EXPECTED_NEW_VOCABULARY = list(PROPOSED_VOCABULARY)
EXPECTED_NEW_VOCABULARY_DIGEST = (
    "926797eedb6db057505a4d86d73b7d049ffb8caab0faa6d6d4daeb0c7d671c94"
)
EXPECTED_DISPOSITION_COUNTS = {
    "CONTROL_OR_RELATIONSHIP": 170,
    "CROSS_REFERENCE": 65,
    "EXCLUSION": 303,
    "GOVERNED_CANDIDATE_OR_SUPPORT": 709,
}
EXPECTED_ROUND_DIGESTS = {
    "S007": "9ebedd6626f35563b89498f2f4328a0cd28b1b5f0c57d14e75502a191456781f",
    "S008": "795ef68adc15ffa229d14dfe27b58e419037352e3cde3a100fa75254b6c6ca11",
}

DIRECT_MECHANICS_STRENGTHS = {
    "DIRECT_IDENTITY",
    "DIRECT_PARTIAL_MECHANICS",
    "DIRECT_COMPLETE_MECHANICS",
}
NONPROSE_IDENTITY_MODALITIES = {"CODE", "FORMULA", "TABLE", "IMAGE"}


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


def _round_queries_match(
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


def _normalized_result_pairs(
    result_pairs: list[tuple[str, str]],
    query_start: int,
) -> list[tuple[int, str]]:
    return [
        (int(query_id[1:]) - query_start + 1, unit_id)
        for query_id, unit_id in result_pairs
    ]


def _normalized_hit_projection(
    round_record: dict[str, Any],
) -> list[tuple[Any, ...]]:
    queries = round_record.get("queries")
    hits = round_record.get("hits")
    if (
        not isinstance(queries, list)
        or len(queries) != len(QUERY_SPECS)
        or not isinstance(hits, list)
    ):
        raise AuthoringError("Stage 7 round lacks its closed query/hit arrays")
    ordinal_by_query_id = {
        query["query_id"]: ordinal
        for ordinal, query in enumerate(queries, start=1)
        if isinstance(query, dict) and isinstance(query.get("query_id"), str)
    }
    if len(ordinal_by_query_id) != len(queries):
        raise AuthoringError("Stage 7 round query IDs are malformed")
    projection: list[tuple[Any, ...]] = []
    for hit in hits:
        if not isinstance(hit, dict) or hit.get("query_id") not in ordinal_by_query_id:
            raise AuthoringError("Stage 7 round hit/query join is malformed")
        projection.append(
            (
                ordinal_by_query_id[hit["query_id"]],
                hit.get("source_unit_id"),
                hit.get("context_sha256"),
                hit.get("disposition"),
                hit.get("candidate_ids"),
                hit.get("route_ids"),
                hit.get("rationale"),
            )
        )
    return projection


def _candidate_coverage_projection(
    *,
    expected_candidates: set[str],
    candidates_by_id: dict[str, dict[str, Any]],
    reading_by_id: dict[str, dict[str, str]],
    normalized_pairs: list[tuple[int, str]],
    stage_unit_ids: set[str],
) -> list[dict[str, Any]]:
    projection: list[dict[str, Any]] = []
    for candidate_id in sorted(expected_candidates):
        candidate = candidates_by_id[candidate_id]
        candidate_units = set(candidate.get("source_unit_ids", []))
        evidence = candidate.get("source_evidence")
        if not isinstance(evidence, list):
            raise AuthoringError(
                f"{candidate_id}.source_evidence is not an array"
            )
        for item in evidence:
            if not isinstance(item, dict):
                raise AuthoringError(
                    f"{candidate_id}.source_evidence has a non-object"
                )
            source_unit_id = item.get("source_unit_id")
            if isinstance(source_unit_id, str):
                candidate_units.add(source_unit_id)
        witnesses = sorted(
            {
                (ordinal, unit_id)
                for ordinal, unit_id in normalized_pairs
                if ordinal <= 10
                and candidate_id
                in parse_links(
                    reading_by_id[unit_id]["candidate_ids"],
                    f"{unit_id}.candidate_ids",
                )
                and unit_id in candidate_units
            }
        )
        if not witnesses:
            raise AuthoringError(
                f"{candidate_id} lacks a candidate-specific F01-F10 witness"
            )
        prose_direct_units = {
            item["source_unit_id"]
            for item in evidence
            if item.get("source_unit_id") in stage_unit_ids
            and item.get("modality") == "PROSE"
            and item.get("strength") in DIRECT_MECHANICS_STRENGTHS
        }
        prose_witnesses = [
            pair
            for pair in witnesses
            if pair[0] <= 9
        ]
        if prose_direct_units and not prose_witnesses:
            raise AuthoringError(
                f"{candidate_id} has direct prose semantics but no F01-F09 "
                "witness on that evidence"
            )
        nonprose_direct_units = {
            item["source_unit_id"]
            for item in evidence
            if item.get("source_unit_id") in stage_unit_ids
            and item.get("modality") in NONPROSE_IDENTITY_MODALITIES
            and item.get("strength") in DIRECT_MECHANICS_STRENGTHS
        }
        if not any(ordinal <= 9 for ordinal, _ in witnesses) and not any(
            ordinal == 10 and unit_id in nonprose_direct_units
            for ordinal, unit_id in witnesses
        ):
            raise AuthoringError(
                f"{candidate_id} relies on F10 without direct nonprose "
                "identity/mechanics evidence"
            )
        projection.append(
            {
                "candidate_id": candidate_id,
                "witnesses": [
                    [ordinal, unit_id] for ordinal, unit_id in witnesses
                ],
                "direct_prose_witnesses": [
                    [ordinal, unit_id]
                    for ordinal, unit_id in prose_witnesses
                ],
            }
        )
    return projection


def _source_specific_rationale(
    *,
    family_ordinal: int,
    row: dict[str, str],
    outcome: str,
) -> str:
    statement = " ".join(row["evidence_statement"].split())
    if not statement:
        raise AuthoringError(
            f"{row['source_unit_id']} lacks a source-specific evidence statement"
        )
    if family_ordinal <= 10:
        family = QUERY_SPECS[family_ordinal - 1][0]
        lead = (
            f"Omission challenge F{family_ordinal:02d} ({family}) at "
            f"{row['source_unit_id']} [{row['block_kind']}] retains "
            f"{outcome}: "
        )
    else:
        lead = ""
    if row["review_disposition"] == "SOURCE_DEFECT_OR_AMBIGUITY":
        uncertainty = " ".join(row["uncertainty"].split())
        if not uncertainty:
            raise AuthoringError(
                f"{row['source_unit_id']} lacks its defect uncertainty boundary"
            )
        return (
            f"{lead}sequential review records source_status="
            f"{row['source_status']} and uncertainty={uncertainty}. {statement}"
        )
    return f"{lead}{statement}"


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to its canonical Goal 4")
    if (
        len(PROPOSED_VOCABULARY) != len(set(PROPOSED_VOCABULARY))
        or len(QUERY_SPECS) != 14
    ):
        raise AuthoringError("frozen vocabulary/query family is malformed")
    vocabulary_digest = hashlib.sha256(
        canonical_json_bytes(PROPOSED_VOCABULARY)
    ).hexdigest()
    if vocabulary_digest != EXPECTED_NEW_VOCABULARY_DIGEST:
        raise AuthoringError(
            f"frozen Stage 7 vocabulary drifted: {vocabulary_digest}"
        )
    query_spec_digest = hashlib.sha256(
        canonical_json_bytes(QUERY_SPECS)
    ).hexdigest()
    if query_spec_digest != EXPECTED_QUERY_SPEC_DIGEST:
        raise AuthoringError(
            f"frozen Stage 7 query family drifted: {query_spec_digest}"
        )

    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    reading = read_csv(goal_dir / merge_worker_output.READING_NAME)
    assets = read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    candidates = read_jsonl(goal_dir / merge_worker_output.CANDIDATE_NAME)
    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(encoding="utf-8")
    )
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)

    if not history:
        raise AuthoringError("review history is empty")
    if (
        history[-1].get("stage") != 7
        or history[-1].get("mode") not in {
            "ROUTE_RESOLUTION",
            "SEARCH_APPEND",
        }
    ):
        raise AuthoringError(
            "expected Stage 7 route/search terminal history"
        )
    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 7 cannot author against a global fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list) or len(rounds) not in {6, 7}:
        raise AuthoringError(
            "expected six prior rounds and zero/one Stage 7 round"
        )
    if [
        (record.get("kind"), record.get("owning_stage"), record.get("epoch"))
        for record in rounds[:6]
    ] != [
        ("LOCAL", 4, 1),
        ("LOCAL", 4, 1),
        ("LOCAL", 5, 1),
        ("LOCAL", 5, 1),
        ("LOCAL", 6, 1),
        ("LOCAL", 6, 1),
    ]:
        raise AuthoringError("prior LOCAL round sequence differs")
    prior_stage_rounds = rounds[6:]
    if prior_stage_rounds:
        prior = prior_stage_rounds[0]
        prior_query_start = sum(
            len(record.get("queries", [])) for record in rounds[:6]
        ) + 1
        if (
            prior.get("kind") != "LOCAL"
            or prior.get("owning_stage") != 7
            or prior.get("epoch") != 1
            or not _round_queries_match(
                prior,
                expected_start=prior_query_start,
            )
            or prior.get("new_vocabulary") != EXPECTED_NEW_VOCABULARY
            or prior.get("new_candidates") != []
            or prior.get("new_evidence_groups") != []
            or prior.get("new_routes") != []
        ):
            raise AuthoringError(
                "prior Stage 7 round is not the expected seed pass"
            )

    unit_by_id = {unit["id"]: unit for unit in units}
    if len(unit_by_id) != len(units):
        raise AuthoringError("source units contain duplicate IDs")
    reading_by_id = {row["source_unit_id"]: row for row in reading}
    if len(reading_by_id) != len(reading):
        raise AuthoringError("reading ledger contains duplicate source-unit IDs")
    candidates_by_id = {row["id"]: row for row in candidates}
    if len(candidates_by_id) != len(candidates):
        raise AuthoringError("candidate ledger contains duplicate IDs")
    route_ids = {row["route_id"] for row in routes}
    if len(route_ids) != len(routes):
        raise AuthoringError("cross-reference ledger contains duplicate IDs")

    stage_unit_ids = {
        unit["id"] for unit in units if unit["path"] in STAGE_PATHS
    }
    if len(stage_unit_ids) != EXPECTED_STAGE_UNIT_COUNT:
        raise AuthoringError(
            f"Stage 7 unit count drifted: {len(stage_unit_ids)}"
        )
    stage_reading = [
        row for row in reading if row["source_unit_id"] in stage_unit_ids
    ]
    if (
        len(stage_reading) != len(stage_unit_ids)
        or any(
            row["path"] not in STAGE_PATHS
            or row["review_status"] != "REVIEWED"
            or row["review_epoch"] != "1"
            or row["review_stage"] != "7"
            for row in stage_reading
        )
    ):
        raise AuthoringError("Stage 7 source paths are not fully reviewed")
    stage_assets = [
        row for row in assets if row["assignment_path"] in STAGE_PATHS
    ]
    if len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT or any(
        row["inspection_status"] != "SCREENED"
        or row["review_epoch"] != "1"
        or row["review_stage"] != "7"
        for row in stage_assets
    ):
        raise AuthoringError("Stage 7 assets are not fully screened")

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
    expected_stage_candidates = (
        linked_from_reading | linked_from_assets | evidenced_in_stage
    )
    if len(expected_stage_candidates) != EXPECTED_STAGE_CANDIDATE_COUNT:
        raise AuthoringError(
            "dynamically derived Stage 7 candidate count drifted: "
            f"{len(expected_stage_candidates)}"
        )
    unknown_or_inactive_candidates = {
        candidate_id
        for candidate_id in expected_stage_candidates
        if candidate_id not in candidates_by_id
        or candidates_by_id[candidate_id].get("record_status") != "ACTIVE"
    }
    if unknown_or_inactive_candidates:
        raise AuthoringError(
            "Stage 7 relationships reach unknown/inactive candidates: "
            f"{sorted(unknown_or_inactive_candidates)}"
        )
    for row in stage_reading:
        unknown_routes = set(
            parse_links(
                row["route_ids"],
                f"{row['source_unit_id']}.route_ids",
            )
        ) - route_ids
        if unknown_routes:
            raise AuthoringError(
                f"{row['source_unit_id']} links unknown routes: "
                f"{sorted(unknown_routes)}"
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

    if len(result_pairs) != EXPECTED_RESULT_PAIR_COUNT:
        raise AuthoringError(
            f"Stage 7 result-pair count drifted: {len(result_pairs)}"
        )
    hit_counts = [
        sum(query_id == query["query_id"] for query_id, _ in result_pairs)
        for query in queries
    ]
    if hit_counts != EXPECTED_HIT_COUNTS:
        raise AuthoringError(f"Stage 7 query hit counts drifted: {hit_counts}")
    normalized_pairs = _normalized_result_pairs(result_pairs, query_start)
    normalized_digest = hashlib.sha256(
        canonical_json_bytes(normalized_pairs)
    ).hexdigest()
    if normalized_digest != EXPECTED_NORMALIZED_RESULT_DIGEST:
        raise AuthoringError(
            "Stage 7 normalized query/result pairs drifted: "
            f"{normalized_digest}"
        )

    result_unit_ids = sorted({unit_id for _, unit_id in result_pairs})
    if len(result_unit_ids) != EXPECTED_UNIQUE_RESULT_UNIT_COUNT:
        raise AuthoringError(
            f"Stage 7 unique result-unit count drifted: {len(result_unit_ids)}"
        )
    path_pair_counts = {
        path: sum(
            unit_by_id[unit_id]["path"] == path
            for _, unit_id in result_pairs
        )
        for path in STAGE_PATHS
    }
    path_unique_unit_counts = {
        path: sum(unit_by_id[unit_id]["path"] == path for unit_id in result_unit_ids)
        for path in STAGE_PATHS
    }
    if (
        path_pair_counts != EXPECTED_PATH_PAIR_COUNTS
        or path_unique_unit_counts != EXPECTED_PATH_UNIQUE_UNIT_COUNTS
    ):
        raise AuthoringError(
            "Stage 7 path-local result counts drifted: "
            f"pairs={path_pair_counts} unique={path_unique_unit_counts}"
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
    triage_digest = hashlib.sha256(
        canonical_json_bytes(triage_projection)
    ).hexdigest()
    if triage_digest != EXPECTED_TRIAGE_DIGEST:
        raise AuthoringError(
            f"Stage 7 search triage projection drifted: {triage_digest}"
        )

    candidate_query_ids = {
        query["query_id"] for query in queries[:10]
    }
    reached_stage_candidates = {
        candidate_id
        for query_id, unit_id in result_pairs
        if query_id in candidate_query_ids
        for candidate_id in parse_links(
            reading_by_id[unit_id]["candidate_ids"],
            f"{unit_id}.candidate_ids",
        )
    }
    if reached_stage_candidates != expected_stage_candidates:
        raise AuthoringError(
            "candidate-facing Stage 7 queries differ from the dynamically "
            "derived target: "
            f"missing={sorted(expected_stage_candidates - reached_stage_candidates)} "
            f"unexpected={sorted(reached_stage_candidates - expected_stage_candidates)}"
        )
    if len(reached_stage_candidates) != EXPECTED_STAGE_CANDIDATE_COUNT:
        raise AuthoringError(
            "candidate-facing queries do not reach the frozen 229/229 total"
        )
    candidate_coverage = _candidate_coverage_projection(
        expected_candidates=expected_stage_candidates,
        candidates_by_id=candidates_by_id,
        reading_by_id=reading_by_id,
        normalized_pairs=normalized_pairs,
        stage_unit_ids=stage_unit_ids,
    )
    coverage_digest = hashlib.sha256(
        canonical_json_bytes(candidate_coverage)
    ).hexdigest()
    if coverage_digest != EXPECTED_CANDIDATE_COVERAGE_DIGEST:
        raise AuthoringError(
            f"Stage 7 candidate coverage drifted: {coverage_digest}"
        )

    omission_challenge_projection: list[tuple[Any, ...]] = []
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
            omission_challenge_projection.append(
                (
                    ordinal,
                    unit_id,
                    row["review_disposition"],
                    row["source_status"],
                    row["uncertainty"],
                    row["evidence_statement"],
                )
            )
    challenge_digest = hashlib.sha256(
        canonical_json_bytes(omission_challenge_projection)
    ).hexdigest()
    if (
        len(omission_challenge_projection)
        != EXPECTED_OMISSION_CHALLENGE_COUNT
        or challenge_digest != EXPECTED_OMISSION_CHALLENGE_DIGEST
    ):
        raise AuthoringError(
            "Stage 7 F01-F10 omission challenge drifted: "
            f"count={len(omission_challenge_projection)} "
            f"digest={challenge_digest}"
        )

    hit_start = sum(len(record.get("hits", [])) for record in rounds) + 1
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
            rationale = _source_specific_rationale(
                family_ordinal=family_ordinal,
                row=row,
                outcome="control/relationship",
            )
        elif row["review_disposition"] == "SOURCE_DEFECT_OR_AMBIGUITY":
            disposition = "CONTROL_OR_RELATIONSHIP"
            rationale = _source_specific_rationale(
                family_ordinal=family_ordinal,
                row=row,
                outcome="source-defect control",
            )
        elif row["review_disposition"] in {
            "NO_CONSTRUCTION",
            "HISTORICAL_ONLY",
        }:
            disposition = "EXCLUSION"
            rationale = _source_specific_rationale(
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
                f"search hit {unit_id} has an unlinked construction-bearing "
                f"disposition: {row['review_disposition']}"
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
                "route_ids": row_route_ids,
                "rationale": rationale,
            }
        )

    existing_vocabulary = search.get("vocabulary")
    if not isinstance(existing_vocabulary, list) or len(existing_vocabulary) != len(
        set(existing_vocabulary)
    ):
        raise AuthoringError("global search vocabulary is malformed")
    mechanically_deduplicated = [
        value
        for value in PROPOSED_VOCABULARY
        if value not in existing_vocabulary
    ]
    first_pass = len(prior_stage_rounds) == 0
    if first_pass:
        if mechanically_deduplicated != EXPECTED_NEW_VOCABULARY:
            raise AuthoringError(
                "Stage 7 live vocabulary deduplication drifted: "
                f"{mechanically_deduplicated}"
            )
        new_vocabulary = mechanically_deduplicated
    else:
        if mechanically_deduplicated:
            raise AuthoringError(
                "prior Stage 7 seed vocabulary is not fully present"
            )
        new_vocabulary = []

    round_record: dict[str, Any] = {
        "round_id": f"S{len(rounds) + 1:03d}",
        "epoch": 1,
        "kind": "LOCAL",
        "owning_stage": 7,
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
    expected_round_digest = EXPECTED_ROUND_DIGESTS.get(
        round_record["round_id"]
    )
    if digest != expected_round_digest:
        raise AuthoringError(
            f"{round_record['round_id']} result digest drifted: {digest}"
        )
    disposition_counts: dict[str, int] = {}
    for hit in hits:
        disposition = hit["disposition"]
        disposition_counts[disposition] = (
            disposition_counts.get(disposition, 0) + 1
        )
    if disposition_counts != EXPECTED_DISPOSITION_COUNTS:
        raise AuthoringError(
            f"Stage 7 hit dispositions drifted: {disposition_counts}"
        )
    if prior_stage_rounds and _normalized_hit_projection(
        prior_stage_rounds[0]
    ) != _normalized_hit_projection(round_record):
        raise AuthoringError(
            "Stage 7 zero-delta rerun differs from the seed hit projection"
        )

    proposed_search = deepcopy(search)
    tool_assumptions = proposed_search.get("tool_assumptions")
    if not isinstance(tool_assumptions, list) or len(tool_assumptions) != len(
        set(tool_assumptions)
    ):
        raise AuthoringError("global search assumptions are malformed")
    if first_pass:
        if ASSUMPTION in tool_assumptions:
            raise AuthoringError(
                "Stage 7 IGNORECASE assumption is already present"
            )
        proposed_search["tool_assumptions"].append(ASSUMPTION)
        proposed_search["vocabulary"].extend(new_vocabulary)
    else:
        if ASSUMPTION not in tool_assumptions:
            raise AuthoringError(
                "prior Stage 7 IGNORECASE assumption is absent"
            )
        if proposed_search["vocabulary"][-len(EXPECTED_NEW_VOCABULARY) :] != (
            EXPECTED_NEW_VOCABULARY
        ):
            raise AuthoringError("prior Stage 7 vocabulary suffix differs")
    proposed_search["rounds"].append(round_record)

    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "ch03-programs-local-search-e1",
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
        print(f"Chapter 3 search authoring failed: {exc}", file=sys.stderr)
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
        f"dispositions={json.dumps(counts, sort_keys=True)} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
