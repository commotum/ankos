#!/usr/bin/env python3
"""Author one closed Stage 9 Chapter 5 LOCAL-search proposal.

The first invocation appends the mechanically deduplicated Chapter 5
vocabulary, the frozen fifteen-family search, and eighteen candidates recovered
by the omission challenge.  A later invocation against the applied first round
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
from copy import deepcopy
from pathlib import Path
from typing import Any

import audit_transaction
import merge_worker_output
import validate_audit
from audit_contract import (
    CANDIDATE_FIELDS,
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

PROPOSED_VOCABULARY = [
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
]

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
            r"patterns?)\b|(?:^|\n)\s*(?:!\[[^\]]*\]\([^)]+\)|```)|"
            r"`[^`\n]*(?:->|→|==|:=|:>|Nest|NestList|Map|Table|Replace|"
            r"Rule|Step|Evolve)[^`\n]*`"
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
            r"\b(?:pictures?|plots?|displays?|"
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
            r"\b(?:see|compare|discussed on|shown on|introduced on|from)\s+"
            r"(?:the )?(?:facing|previous|next)\s+page\b"
        ),
        "REGEX",
    ),
]

EXPECTED_STAGE_UNIT_COUNT = 539
EXPECTED_STAGE_ASSET_COUNT = 150
EXPECTED_INITIAL_STAGE_CANDIDATE_COUNT = 324
EXPECTED_ENRICHED_STAGE_CANDIDATE_COUNT = 342
EXPECTED_STAGE_ROUTE_COUNT = 62
EXPECTED_READING_UPDATE_COUNT = 22
EXPECTED_NEW_CANDIDATE_COUNT = 18
EXPECTED_NEW_EVIDENCE_COUNT = 20
EXPECTED_RESULT_PAIR_COUNT = 0
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 0
EXPECTED_PATH_PAIR_COUNTS: dict[str, int] = {}
EXPECTED_PATH_UNIQUE_UNIT_COUNTS: dict[str, int] = {}
EXPECTED_HIT_COUNTS: list[int] = []
EXPECTED_QUERY_SPEC_DIGEST = ""
EXPECTED_NORMALIZED_RESULT_DIGEST = ""
EXPECTED_TRIAGE_DIGEST = ""
EXPECTED_ACTIVE_SEMANTIC_DIGEST = ""
EXPECTED_CANDIDATE_COVERAGE_DIGEST = ""
EXPECTED_ROUTE_COVERAGE_DIGEST = ""
EXPECTED_OMISSION_CHALLENGE_COUNT = 0
EXPECTED_OMISSION_CHALLENGE_DIGEST = ""
EXPECTED_NEW_VOCABULARY_DIGEST = ""
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
    source_unit_ids: list[str],
    evidence: list[dict[str, Any]],
    supported_values: dict[str, Any],
    not_applicable_fields: set[str],
    parameters: list[dict[str, Any]],
    uncertainties: list[str],
    related_candidate_ids: list[dict[str, Any]],
    source_status: list[str],
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
            "ordinal": 1,
        },
        "source_unit_ids": source_unit_ids,
        "source_evidence": evidence,
        "source_status": source_status,
        "image_witnesses": [],
        "evidence_strength": list(
            dict.fromkeys(item["strength"] for item in evidence)
        ),
        "field_support": field_support,
        "fingerprint": fingerprint,
        "parameters": parameters,
        "variants": [],
        "missing_mechanics": [
            "The assigned source leaves these fields unknown: "
            + ", ".join(missing)
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
    unit_id: str,
    strength: str,
    modality: str,
    claim: str,
    fields: list[str],
) -> dict[str, Any]:
    return {
        "evidence_id": f"E{evidence_number:06d}",
        "evidence_group_id": f"G{evidence_number:06d}",
        "discovery_anchor": {
            "epoch": 2,
            "kind": "SEARCH_HIT",
            "id": hit_id,
            "ordinal": 1,
        },
        "source_unit_id": unit_id,
        "image_path": None,
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

    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    reading = read_csv(goal_dir / merge_worker_output.READING_NAME)
    assets = read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    candidates = read_jsonl(goal_dir / merge_worker_output.CANDIDATE_NAME)
    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(encoding="utf-8")
    )
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)

    if (
        not history
        or history[-1].get("review_id") != "V000024"
        or history[-1].get("stage") != 9
        or history[-1].get("mode") != "ROUTE_RESOLUTION"
        or history[-1].get("epoch") != 2
    ):
        raise AuthoringError("expected exact Stage 9 V000024 route terminal")
    rounds = search.get("rounds")
    if not isinstance(rounds, list) or len(rounds) != 12:
        raise AuthoringError("expected exactly twelve prior LOCAL rounds")
    if any(
        record.get("kind") != "LOCAL"
        for record in rounds
    ) or [
        (record.get("owning_stage"), record.get("epoch"))
        for record in rounds
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
    candidates_by_id = {candidate["id"]: candidate for candidate in candidates}
    routes_by_id = {route["route_id"]: route for route in routes}
    if (
        len(unit_by_id) != len(units)
        or len(reading_by_id) != len(reading)
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
    if len(initial_stage_candidates) != EXPECTED_INITIAL_STAGE_CANDIDATE_COUNT:
        raise AuthoringError(
            "initial Stage 9 candidate relationship count drifted: "
            f"{len(initial_stage_candidates)}"
        )
    if any(
        candidates_by_id.get(candidate_id, {}).get("record_status") != "ACTIVE"
        for candidate_id in initial_stage_candidates
    ):
        raise AuthoringError("Stage 9 reaches an unknown or inactive candidate")

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
    if len(active_route_ids) != EXPECTED_STAGE_ROUTE_COUNT:
        raise AuthoringError(
            f"Stage 9 active route count drifted: {len(active_route_ids)}"
        )
    stage_owned_routes = [
        routes_by_id[route_id]
        for route_id in active_route_ids
        if routes_by_id[route_id]["owning_stage"] == "9"
    ]
    if (
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
            for candidate_id in sorted(initial_stage_candidates)
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
    if semantic_digest != EXPECTED_ACTIVE_SEMANTIC_DIGEST:
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
    reading_updates, candidate_updates = _build_enrichment(
        reading_by_id=reading_by_id,
        hit_by_pair=hit_by_pair,
    )
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
    expected_stage_candidates = initial_stage_candidates | {
        candidate["id"] for candidate in candidate_updates
    }
    if len(expected_stage_candidates) != EXPECTED_ENRICHED_STAGE_CANDIDATE_COUNT:
        raise AuthoringError("enriched Stage 9 candidate count drifted")

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

    route_coverage: list[tuple[str, list[str]]] = []
    result_set = set(result_unit_ids)
    for route_id in sorted(active_route_ids):
        route = routes_by_id[route_id]
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
    new_vocabulary = [
        value
        for value in PROPOSED_VOCABULARY
        if value not in existing_vocabulary
    ]
    if new_vocabulary != PROPOSED_VOCABULARY:
        raise AuthoringError(
            "Stage 9 vocabulary is not a fully new frozen suffix"
        )
    if ASSUMPTION not in search.get("tool_assumptions", []):
        raise AuthoringError("prior search assumption is absent")

    round_record: dict[str, Any] = {
        "round_id": "S013",
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
            candidate["id"] for candidate in candidate_updates
        ],
        "new_evidence_groups": [
            f"G{number:06d}" for number in range(4049, 4069)
        ],
        "new_routes": [],
        "rerun_digest": "",
    }
    digest = validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = digest
    round_record["rerun_digest"] = digest
    if digest != EXPECTED_ROUND_DIGESTS.get("S013"):
        raise AuthoringError(f"S013 result digest drifted: {digest}")

    proposed_search = deepcopy(search)
    proposed_search["vocabulary"].extend(new_vocabulary)
    proposed_search["rounds"].append(round_record)
    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": "ch05-dimensions-local-search-e2",
        "epoch": 2,
        "source_paths": [NOTES_PATH],
        "base_artifact_sha256": {
            name: hashlib.sha256((goal_dir / name).read_bytes()).hexdigest()
            for name in merge_worker_output.WRITE_NAMES
        },
        "reading_updates": reading_updates,
        "asset_updates": [],
        "candidate_updates": candidate_updates,
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
