#!/usr/bin/env python3
"""Author one closed Stage 8 Chapter 4 LOCAL-search proposal.

The first invocation appends the mechanically deduplicated Chapter 4
vocabulary and the frozen fourteen-family seed pass.  The second invocation
repeats that exact family with no vocabulary or semantic delta, establishing
the required stage-local zero-delta closure.

The author derives its candidate target from the live Stage 8 reading, asset,
and evidence relationships.  It never assumes a numeric B-ID range.
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
    "CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md",
    "BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md",
]

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with IGNORECASE and MULTILINE semantics and "
    "query-major then canonical source-unit result order."
)

PROPOSED_VOCABULARY = [
    "positional radix denotation relation",
    "positional digit encoder",
    "positional digit decoder",
    "fractional positional digit generator",
    "negative-base positional representation",
    "non-power place-value representation",
    "multiplicative prime-exponent representation",
    "Gray-code ordering generator",
    "repeated constant-addition map",
    "repeated constant-multiplication map",
    "parity-conditioned integer map",
    "3n+1 map",
    "binary reversal-addition map",
    "run-length encoder",
    "digit-count append system",
    "fractional-parts power sequence",
    "irrational-rotation sequence",
    "Beatty-difference sequence",
    "continued-fraction substitution generator",
    "recursive numeric sequence",
    "linear recurrence",
    "factorial recurrence",
    "logistic recurrence",
    "Ackermann function",
    "primitive-recursive calculus",
    "unbounded mu-search",
    "prime sequence",
    "sieve of Eratosthenes",
    "prime-counting function",
    "divisor-count function",
    "aliquot-sum map",
    "sum-of-squares constraint",
    "Goldbach representation",
    "perfect-number constraint",
    "Lucas-Lehmer test",
    "Riemann zeta function",
    "Riemann-Siegel Z function",
    "normal-number constraint",
    "Stoneham number",
    "Leibniz pi approximation",
    "arithmetic-geometric-mean pi solver",
    "Bailey-Borwein-Plouffe relation",
    "digit-by-digit square-root solver",
    "continued-fraction digit extractor",
    "Gauss map",
    "subtractive Euclidean algorithm",
    "Farey-sequence generator",
    "Egyptian-fraction relation",
    "nested-radical representation",
    "operator-tree integer representation",
    "Lissajous curve map",
    "finite sine-sum function",
    "cosine-difference zero spacing",
    "Fourier partial sum",
    "iterated shift map",
    "tent map",
    "logistic map",
    "finite-precision shift simulation",
    "Anosov torus map",
    "Lyapunov-exponent observer",
    "continuous cellular automaton",
    "continuous-CA averaging rule",
    "continuous-CA additive rule",
    "probabilistic cellular automaton",
    "partial-differential-equation relation",
    "diffusion equation",
    "wave equation",
    "sine-Gordon equation",
    "Klein-Gordon equation",
    "scalar-field potential",
    "Lagrangian density",
    "Hamiltonian functional",
    "finite-difference PDE solver",
    "Courant stability constraint",
    "Kardar-Parisi-Zhang equation",
    "Burgers equation",
    "nonlinear Schrodinger equation",
    "Kuramoto-Sivashinsky equation",
    "register-machine arithmetic realization",
    "nested digit substitution",
    "axis-crossing substitution encoding",
    "rotated digit substitution preset",
    "base-6 powers-of-three automaton",
    "zero-spacing substitution",
]

QUERY_SPECS = [
    (
        "positional, digit, radix, and continued-fraction representations",
        (
            r"\b(?:positional|radix|bases?|binary|ternary|decimal|digits?|"
            r"DigitCount|IntegerDigits|IntegerReverse|continued fractions?|"
            r"Gray codes?|place values?|prime exponents?|negative bases?|"
            r"representations?)\b"
        ),
        "REGEX",
    ),
    (
        "discrete arithmetic, parity, reversal, and bitwise maps",
        (
            r"\b(?:repeated (?:addition|multiplication)|multiply|multiplies|"
            r"multiplying|multiplication|Collatz|3\s*n\s*\+\s*1|parity|"
            r"revers(?:e|al|ing)|run[- ]length|look[- ]and[- ]say|BitXor|"
            r"BitOr|fractional parts?|integer maps?|iterations?|maps?)\b"
        ),
        "REGEX",
    ),
    (
        "recurrence, recursion, and computable-function constructions",
        (
            r"\b(?:recurrences?|recursive|recursion|Fibonacci|factorial|"
            r"Ackermann|primitive recursive|mu[- ]search|self[- ]indexed|"
            r"triangular|plus|times|Fold|Jacobi|memoiz(?:e|ed|ation)|"
            r"evaluation polic(?:y|ies)|composition)\b|μ"
        ),
        "REGEX",
    ),
    (
        "prime, divisor, Diophantine, and number-theory constructions",
        (
            r"\b(?:primes?|sieve|divisors?|aliquot|perfect numbers?|"
            r"Goldbach|Mersenne|Lucas[- ]Lehmer|M[oö]bius|Mertens|"
            r"relatively prime|squares?|Waring|Fermat|Josephus|"
            r"Ulam sequence)\b"
        ),
        "REGEX",
    ),
    (
        "constants, roots, normality, approximations, and digit extraction",
        (
            r"(?:\b(?:Pi|constants?|square roots?|cube roots?|fourth roots?|"
            r"logarithm|exponential|normal numbers?|Stoneham|Benford|"
            r"digit(?:s| sequences?| generators?| extractors?)|Bailey|"
            r"Borwein|Plouffe|Newton|arithmetic[- ]geometric)\b|π|Log\[)"
        ),
        "REGEX",
    ),
    (
        "rational, continued-fraction, Euclidean, and alternate denotations",
        (
            r"\b(?:continued fractions?|rational|Euclidean|Farey|"
            r"Egyptian fractions?|nested radicals?|digital slopes?|"
            r"operator trees?|Lissajous|special functions?)\b"
        ),
        "REGEX",
    ),
    (
        "trigonometric, Fourier, zeta, and zero-set constructions",
        (
            r"\b(?:sine|cosine|Sin|Cos|Fourier|Riemann|zeta|"
            r"Riemann[- ]Siegel|zeros?|trigonometric|Weierstrass|"
            r"harmonic|lacunary)\b"
        ),
        "REGEX",
    ),
    (
        "iterated-map, finite-precision, and chaos constructions",
        (
            r"\b(?:iterated maps?|shift maps?|tent maps?|logistic maps?|"
            r"Gauss maps?|Anosov|Lyapunov|unit interval|finite precision|"
            r"FractionalPart|chaos|trajector(?:y|ies))\b"
        ),
        "REGEX",
    ),
    (
        "general numeric and continuous construction identities",
        (
            r"\b(?:functions?|sequences?|relations?|equations?|constraints?|"
            r"systems?|rules?|maps?|algorithms?|generators?|solvers?|"
            r"predicates?|obligations?|solutions?|"
            r"approximat(?:e|es|ed|ing|ion)|continuous cellular "
            r"automat(?:on|a)|partial differential|PDE|ordinary differential|"
            r"ODE|diffusion|sine[- ]Gordon|Klein[- ]Gordon|finite difference|"
            r"Courant|Kardar|Parisi|Zhang|Burgers|Schr[oö]dinger|Kuramoto|"
            r"Sivashinsky|scalar fields?|Lagrangian|Hamiltonian|"
            r"single black cell|unbounded|growth|"
            r"increas(?:e|es|ed|ing))\b|"
            r"(?:^|\n)\s*(?:!\[[^\]]*\]\([^)]+\)|```|<table>)|"
            r"Mod\[|Integrate\["
        ),
        "REGEX",
    ),
    (
        "nonprose formula, code, table, and image identity anchors",
        (
            r"(?:^|\n)\s*(?:```|!\[[^\]]*\]\([^)]+\))|"
            r"`[^`\n]*(?:->|→|==|:=|Mod\[|Floor\[|Sqrt\[|Nest|Table|"
            r"IntegerDigits|DigitCount|BitXor|BitOr|FractionalPart|"
            r"Sin\[|Cos\[|D\[)[^`\n]*`"
        ),
        "REGEX",
    ),
    (
        "continuous automata, differential equations, and numerical solvers",
        (
            r"\b(?:continuous(?:ly)?[- ]valued|continuous cellular "
            r"automat(?:on|a)|probabilistic cellular automat(?:on|a)|"
            r"partial differential equations?|PDE|ordinary differential "
            r"equations?|ODE|diffusion|wave equation|sine[- ]Gordon|"
            r"Klein[- ]Gordon|finite difference|Courant|Kardar|Parisi|"
            r"Zhang|Burgers|Schr[oö]dinger|Kuramoto|Sivashinsky)\b"
        ),
        "REGEX",
    ),
    (
        "native state, iteration, update, and completion mechanics",
        (
            r"\b(?:initial conditions?|initial values?|initial states?|seeds?|"
            r"backgrounds?|boundar(?:y|ies)|current states?|successors?|"
            r"steps?|evol(?:ve|ves|ved|ving|ution)|iterations?|updates?|"
            r"recurrences?|rewrit(?:e|es|ing)|moves?|neighbou?rs?|"
            r"fixed points?|halts?|termination|converges?|diverges?)\b"
        ),
        "REGEX",
    ),
    (
        "stochastic, declarative, constraint, and relation guardrails",
        (
            r"\b(?:random(?:ness|ly|ization)?|probabilistic|probability|"
            r"stochastic|Bernoulli|sample[sd]?|sampling|constraints?|"
            r"equations?|solutions?|relations?|inequalit(?:y|ies)|"
            r"boundary values?|initial values?|existence|universal|"
            r"necessary and sufficient)\b"
        ),
        "REGEX",
    ),
    (
        "representation, observer, application, and implementation boundary",
        (
            r"\b(?:plots?|displays?|pictures?|render(?:s|ed|ing)?|"
            r"represent(?:s|ed|ing|ation)?|implement(?:s|ed|ing|ation)?|"
            r"simulat(?:e|es|ed|ing|ion)|emulat(?:e|es|ed|ing|ion)|"
            r"observers?|analy[sz](?:e|es|ed|ing)|"
            r"measur(?:e|es|ed|ing|ement)|"
            r"approximat(?:e|es|ed|ing|ion)|digits?|"
            r"trajector(?:y|ies)|Mathematica)\b"
        ),
        "REGEX",
    ),
]

EXPECTED_STAGE_UNIT_COUNT = 745
EXPECTED_STAGE_ASSET_COUNT = 145
EXPECTED_STAGE_CANDIDATE_COUNT = 336
EXPECTED_RESULT_PAIR_COUNT = 2192
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 694
EXPECTED_PATH_PAIR_COUNTS = {
    STAGE_PATHS[0]: 856,
    STAGE_PATHS[1]: 1336,
}
EXPECTED_PATH_UNIQUE_UNIT_COUNTS = {
    STAGE_PATHS[0]: 285,
    STAGE_PATHS[1]: 409,
}
EXPECTED_QUERY_SPEC_DIGEST = (
    "e6e91221014bcd0e3d89aab0ca7f7e6920cbd4f6dcd40ed95b783045f2a643f5"
)
EXPECTED_HIT_COUNTS = [
    201,
    88,
    82,
    69,
    198,
    54,
    55,
    44,
    584,
    228,
    51,
    127,
    156,
    255,
]
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "291116f6c782b12852bd9746c5c3c3125269007fe3503b46f042c34dd0d24fe5"
)
EXPECTED_TRIAGE_DIGEST = (
    "27fcf8228efd9b88de58b19c92684a136ee62a1febe87b185eaf50454fd60140"
)
EXPECTED_CANDIDATE_COVERAGE_DIGEST = (
    "df361d7e57a34ae31094566d556e77653d0e2990e4955d83ea863055e1bde600"
)
EXPECTED_OMISSION_CHALLENGE_COUNT = 562
EXPECTED_OMISSION_CHALLENGE_DIGEST = (
    "44c22373eac85107f7a0cc5eac3651bd7a387c271fae9f860dab37cc33081ff7"
)
EXPECTED_NEW_VOCABULARY = list(PROPOSED_VOCABULARY)
EXPECTED_NEW_VOCABULARY_DIGEST = (
    "328ffb1b80a8ca96569df416063c4a30fb4cda914636e983c8fef2c656aa848c"
)
EXPECTED_DISPOSITION_COUNTS = {
    "CONTROL_OR_RELATIONSHIP": 367,
    "CROSS_REFERENCE": 6,
    "EXCLUSION": 436,
    "GOVERNED_CANDIDATE_OR_SUPPORT": 1383,
}
EXPECTED_ROUND_DIGESTS = {
    "S009": "2dd1df7cd31432184ade51ee78f1f14f84abf252d4fa6219e5b5b081c235cae1",
    "S010": "26aafc5d678c793899766e1595ad3b51897db6ec499959fdaad4faff5cb50d07",
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
        raise AuthoringError("Stage 8 round lacks its closed query/hit arrays")
    ordinal_by_query_id = {
        query["query_id"]: ordinal
        for ordinal, query in enumerate(queries, start=1)
        if isinstance(query, dict) and isinstance(query.get("query_id"), str)
    }
    if len(ordinal_by_query_id) != len(queries):
        raise AuthoringError("Stage 8 round query IDs are malformed")
    projection: list[tuple[Any, ...]] = []
    for hit in hits:
        if (
            not isinstance(hit, dict)
            or hit.get("query_id") not in ordinal_by_query_id
        ):
            raise AuthoringError("Stage 8 round hit/query join is malformed")
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
            if pair[0] <= 9 and pair[1] in prose_direct_units
        ]
        if prose_direct_units and not prose_witnesses:
            raise AuthoringError(
                f"{candidate_id} has direct prose semantics but no F01-F09 "
                "witness on one of its direct-PROSE evidence units"
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


def _require_stage8_route_state(routes: list[dict[str, str]]) -> None:
    stage_routes = [row for row in routes if row["owning_stage"] == "8"]
    if len(stage_routes) != 24:
        raise AuthoringError(
            f"Stage 8 route count drifted: {len(stage_routes)}"
        )
    within = [
        row for row in stage_routes if row["closure_scope"] == "WITHIN_STAGE"
    ]
    cross = [
        row for row in stage_routes if row["closure_scope"] == "CROSS_RANGE"
    ]
    if (
        len(within) != 15
        or any(row["status"] != "RESOLVED" for row in within)
        or len(cross) != 9
        or any(row["status"] != "PENDING" for row in cross)
    ):
        raise AuthoringError(
            "Stage 8 route closure differs from 15 resolved local and "
            "9 pending cross-range routes"
        )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to canonical Goal 4")
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
            f"frozen Stage 8 vocabulary drifted: {vocabulary_digest}"
        )
    query_spec_digest = hashlib.sha256(
        canonical_json_bytes(QUERY_SPECS)
    ).hexdigest()
    if query_spec_digest != EXPECTED_QUERY_SPEC_DIGEST:
        raise AuthoringError(
            f"frozen Stage 8 query family drifted: {query_spec_digest}"
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
        history[-1].get("stage") != 8
        or history[-1].get("mode")
        not in {"ROUTE_RESOLUTION", "SEARCH_APPEND"}
    ):
        raise AuthoringError(
            "expected Stage 8 route/search terminal history"
        )
    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 8 cannot author against a global fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list) or len(rounds) not in {8, 9}:
        raise AuthoringError(
            "expected eight prior rounds and zero/one Stage 8 round"
        )
    if [
        (record.get("kind"), record.get("owning_stage"), record.get("epoch"))
        for record in rounds[:8]
    ] != [
        ("LOCAL", 4, 1),
        ("LOCAL", 4, 1),
        ("LOCAL", 5, 1),
        ("LOCAL", 5, 1),
        ("LOCAL", 6, 1),
        ("LOCAL", 6, 1),
        ("LOCAL", 7, 1),
        ("LOCAL", 7, 1),
    ]:
        raise AuthoringError("prior LOCAL round sequence differs")
    prior_stage_rounds = rounds[8:]
    if prior_stage_rounds:
        prior = prior_stage_rounds[0]
        prior_query_start = sum(
            len(record.get("queries", [])) for record in rounds[:8]
        ) + 1
        if (
            prior.get("kind") != "LOCAL"
            or prior.get("owning_stage") != 8
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
                "prior Stage 8 round is not the expected seed pass"
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
    _require_stage8_route_state(routes)

    stage_unit_ids = {
        unit["id"] for unit in units if unit["path"] in STAGE_PATHS
    }
    if len(stage_unit_ids) != EXPECTED_STAGE_UNIT_COUNT:
        raise AuthoringError(
            f"Stage 8 unit count drifted: {len(stage_unit_ids)}"
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
            or row["review_stage"] != "8"
            for row in stage_reading
        )
    ):
        raise AuthoringError("Stage 8 source paths are not fully reviewed")
    stage_assets = [
        row for row in assets if row["assignment_path"] in STAGE_PATHS
    ]
    if len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT or any(
        row["inspection_status"] != "SCREENED"
        or row["review_epoch"] != "1"
        or row["review_stage"] != "8"
        for row in stage_assets
    ):
        raise AuthoringError("Stage 8 assets are not fully screened")

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
            "dynamically derived Stage 8 candidate count drifted: "
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
            "Stage 8 relationships reach unknown/inactive candidates: "
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
            f"Stage 8 result-pair count drifted: {len(result_pairs)}"
        )
    hit_counts = [
        sum(query_id == query["query_id"] for query_id, _ in result_pairs)
        for query in queries
    ]
    if hit_counts != EXPECTED_HIT_COUNTS:
        raise AuthoringError(f"Stage 8 query hit counts drifted: {hit_counts}")
    normalized_pairs = _normalized_result_pairs(result_pairs, query_start)
    normalized_digest = hashlib.sha256(
        canonical_json_bytes(normalized_pairs)
    ).hexdigest()
    if normalized_digest != EXPECTED_NORMALIZED_RESULT_DIGEST:
        raise AuthoringError(
            "Stage 8 normalized query/result pairs drifted: "
            f"{normalized_digest}"
        )

    result_unit_ids = sorted({unit_id for _, unit_id in result_pairs})
    if len(result_unit_ids) != EXPECTED_UNIQUE_RESULT_UNIT_COUNT:
        raise AuthoringError(
            f"Stage 8 unique result-unit count drifted: {len(result_unit_ids)}"
        )
    path_pair_counts = {
        path: sum(
            unit_by_id[unit_id]["path"] == path
            for _, unit_id in result_pairs
        )
        for path in STAGE_PATHS
    }
    path_unique_unit_counts = {
        path: sum(
            unit_by_id[unit_id]["path"] == path
            for unit_id in result_unit_ids
        )
        for path in STAGE_PATHS
    }
    if (
        path_pair_counts != EXPECTED_PATH_PAIR_COUNTS
        or path_unique_unit_counts != EXPECTED_PATH_UNIQUE_UNIT_COUNTS
    ):
        raise AuthoringError(
            "Stage 8 path-local result counts drifted: "
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
            f"Stage 8 search triage projection drifted: {triage_digest}"
        )

    candidate_query_ids = {query["query_id"] for query in queries[:10]}
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
            "candidate-facing Stage 8 queries differ from the dynamically "
            "derived target: "
            f"missing={sorted(expected_stage_candidates - reached_stage_candidates)} "
            f"unexpected={sorted(reached_stage_candidates - expected_stage_candidates)}"
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
            f"Stage 8 candidate coverage drifted: {coverage_digest}"
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
            "Stage 8 F01-F10 omission challenge drifted: "
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
    if not isinstance(existing_vocabulary, list) or len(
        existing_vocabulary
    ) != len(set(existing_vocabulary)):
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
                "Stage 8 live vocabulary deduplication drifted: "
                f"{mechanically_deduplicated}"
            )
        new_vocabulary = mechanically_deduplicated
    else:
        if mechanically_deduplicated:
            raise AuthoringError(
                "prior Stage 8 seed vocabulary is not fully present"
            )
        new_vocabulary = []

    round_record: dict[str, Any] = {
        "round_id": f"S{len(rounds) + 1:03d}",
        "epoch": 1,
        "kind": "LOCAL",
        "owning_stage": 8,
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
            f"Stage 8 hit dispositions drifted: {disposition_counts}"
        )
    if prior_stage_rounds and _normalized_hit_projection(
        prior_stage_rounds[0]
    ) != _normalized_hit_projection(round_record):
        raise AuthoringError(
            "Stage 8 zero-delta rerun differs from the seed hit projection"
        )

    proposed_search = deepcopy(search)
    tool_assumptions = proposed_search.get("tool_assumptions")
    if not isinstance(tool_assumptions, list) or len(tool_assumptions) != len(
        set(tool_assumptions)
    ):
        raise AuthoringError("global search assumptions are malformed")
    if ASSUMPTION not in tool_assumptions:
        raise AuthoringError(
            "the Stage 7 IGNORECASE search assumption is absent"
        )
    if first_pass:
        proposed_search["vocabulary"].extend(new_vocabulary)
    elif proposed_search["vocabulary"][
        -len(EXPECTED_NEW_VOCABULARY) :
    ] != EXPECTED_NEW_VOCABULARY:
        raise AuthoringError("prior Stage 8 vocabulary suffix differs")
    proposed_search["rounds"].append(round_record)

    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "ch04-numbers-local-search-e1",
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
        print(f"Chapter 4 search authoring failed: {exc}", file=sys.stderr)
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
