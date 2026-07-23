#!/usr/bin/env python3
"""Author the sealed Stage 8 Chapter 4 main-text blind review reproducibly.

This helper is bound to the exact epoch-1 bundle for
``CHAPTERS/04-Systems-Based-on-Numbers.md``.  It records the judgments made
after the 306 units were read in canonical order and all 63 assigned assets
were screened.  It refuses to modify anything except a pristine nonsemantic
worksheet for that exact assignment.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

TOOLS = Path("/home/jake/Developer/ankos/goal-4/tools")
sys.path.insert(0, str(TOOLS))

import prepare_review_output  # noqa: E402
from audit_contract import (  # noqa: E402
    CANDIDATE_FIELDS,
    FINGERPRINT_FIELDS,
    canonical_json_bytes,
)


EXPECTED_CONTENT_SET = (
    "0b5a50b9f6214e4b3600bf8ba55f2064739bf3f835113a135b0c09b7f877ab4d"
)
EXPECTED_WORKER = "ch04-main-reader-e1"
EXPECTED_PATHS = ["CHAPTERS/04-Systems-Based-on-Numbers.md"]
STAGE = 8


class AuthoringError(ValueError):
    """The assignment or worksheet is not safe for this exact authoring pass."""


def compact(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


CandidateSpec = dict[str, Any]
EvidenceSpec = dict[str, Any]
RouteSpec = dict[str, Any]
ALL_CANDIDATES: list[CandidateSpec] = []
ALL_ROUTES: list[RouteSpec] = []
_evidence_insertion = 0


def candidate(
    key: str,
    name: str,
    anchor: str,
    facts: dict[str, str],
    *,
    aliases: list[str] | None = None,
    not_applicable: dict[str, str] | None = None,
    missing: str,
    source_status: list[str] | None = None,
    uncertainties: list[str] | None = None,
    parameters: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    route_keys: list[str] | None = None,
    unknown_reasons: dict[str, str] | None = None,
) -> CandidateSpec:
    if any(item["key"] == key for item in ALL_CANDIDATES):
        raise AuthoringError(f"duplicate candidate key {key}")
    spec: CandidateSpec = {
        "key": key,
        "name": name,
        "anchor": anchor,
        "facts": facts,
        "aliases": aliases or [],
        "not_applicable": not_applicable or {},
        "missing": missing,
        "source_status": source_status or ["CLEAR"],
        "uncertainties": uncertainties or [],
        "parameters": parameters or [],
        "variants": variants or [],
        "route_keys": route_keys or [],
        "unknown_reasons": unknown_reasons or {},
        "evidence": [],
        "_insertion": len(ALL_CANDIDATES),
    }
    ALL_CANDIDATES.append(spec)
    return spec


def evidence(
    spec: CandidateSpec,
    label: str,
    unit: str,
    claim: str,
    fields: list[str],
    *,
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    modality: str = "PROSE",
    image_path: str | None = None,
) -> None:
    global _evidence_insertion
    if any(item["label"] == label for item in spec["evidence"]):
        raise AuthoringError(f"duplicate evidence label {label}")
    spec["evidence"].append(
        {
            "label": label,
            "unit": unit,
            "claim": claim,
            "fields": fields,
            "strength": strength,
            "modality": modality,
            "image_path": image_path,
            "_insertion": _evidence_insertion,
        }
    )
    _evidence_insertion += 1


def source_candidate(
    key: str,
    name: str,
    anchor: str,
    facts: dict[str, str],
    *,
    aliases: list[str] | None = None,
    not_applicable: dict[str, str] | None = None,
    missing: str,
    claim: str,
    strength: str = "DIRECT_PARTIAL_MECHANICS",
    modality: str = "PROSE",
    image_path: str | None = None,
    source_status: list[str] | None = None,
    uncertainties: list[str] | None = None,
    parameters: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    route_keys: list[str] | None = None,
    unknown_reasons: dict[str, str] | None = None,
) -> CandidateSpec:
    spec = candidate(
        key,
        name,
        anchor,
        facts,
        aliases=aliases,
        not_applicable=not_applicable,
        missing=missing,
        source_status=source_status,
        uncertainties=uncertainties,
        parameters=parameters,
        variants=variants,
        route_keys=route_keys,
        unknown_reasons=unknown_reasons,
    )
    evidence(
        spec,
        f"{key}-source",
        anchor,
        claim,
        list(facts) + list((not_applicable or {}).keys()),
        strength=strength,
        modality=("IMAGE" if image_path else modality),
        image_path=image_path,
    )
    return spec


def context_evidence(
    spec: CandidateSpec,
    label: str,
    unit: str,
    claim: str,
    *,
    fields: list[str] | None = None,
    strength: str = "CORROBORATING",
    modality: str = "PROSE",
    image_path: str | None = None,
) -> None:
    evidence(
        spec,
        label,
        unit,
        claim,
        fields or [],
        strength=strength,
        modality=("IMAGE" if image_path else modality),
        image_path=image_path,
    )


def mark_unknown(spec: CandidateSpec, reasons: dict[str, str]) -> None:
    """Move unsupported fingerprint claims to exact source-limited unknowns."""
    for field, reason in reasons.items():
        spec["facts"].pop(field, None)
        spec["not_applicable"].pop(field, None)
        for item in spec["evidence"]:
            item["fields"] = [
                present for present in item["fields"] if present != field
            ]
        spec["unknown_reasons"][field] = reason


def spec_by_key(key: str) -> CandidateSpec:
    try:
        return next(item for item in ALL_CANDIDATES if item["key"] == key)
    except StopIteration as exc:
        raise AuthoringError(f"unknown candidate key {key}") from exc


def add_route(
    key: str,
    unit: str,
    literal: str,
    topic: str,
    vocabulary: list[str],
    *,
    scope: str = "CROSS_RANGE",
    kind: str = "PAGE",
) -> None:
    if any(item["key"] == key for item in ALL_ROUTES):
        raise AuthoringError(f"duplicate route key {key}")
    ALL_ROUTES.append(
        {
            "key": key,
            "unit": unit,
            "literal": literal,
            "topic": topic,
            "vocabulary": vocabulary,
            "scope": scope,
            "kind": kind,
            "_insertion": len(ALL_ROUTES),
        }
    )


EVOLUTION_NA = {
    "control_state": "No independently stored head, instruction pointer, or control register is part of this law.",
    "external_data": "After the rule and initial state are supplied, no external data stream is read.",
}

DECLARATIVE_NA = {
    "visible_history": "This fixed denotation or query has no native trajectory.",
    "control_state": "This fixed denotation or query has no control register.",
    "seed": "This fixed denotation or query has no initial state.",
    "boundary": "No evolution boundary is part of this fixed denotation or query.",
    "external_data": "No external data stream is consumed.",
    "frontier_or_activation": "No components fire in a fixed denotation or query.",
    "schedule": "There is no update schedule.",
    "read_dependencies_or_neighborhood": "There is no local update neighborhood.",
    "write_replacement_assembly_or_commit": "No state update is committed.",
}

SEED_NA = {
    "visible_history": "An initial-state object has no native trajectory.",
    "control_state": "An initial-state object has no control register.",
    "input": "The object is supplied as input rather than consuming another input.",
    "boundary": "Any evolution boundary belongs to the associated law, not this seed object.",
    "external_data": "No external data stream is consumed.",
    "frontier_or_activation": "A seed has no update frontier.",
    "schedule": "A seed has no update schedule.",
    "read_dependencies_or_neighborhood": "A seed performs no local reads.",
    "law_kind": "A seed is data, not an update law.",
    "rule_relation_constraint_function_or_probability_law": "A seed is data, not an update law.",
    "write_replacement_assembly_or_commit": "A seed performs no writes.",
    "termination_completion_failure": "Providing the complete seed completes this object.",
}


def iterative_facts(
    *,
    kind: str,
    carrier: str,
    support: str,
    topology: str,
    invariants: str,
    alphabet: str,
    state: str,
    seed: str,
    input_value: str,
    frontier: str,
    schedule: str,
    read: str,
    law_kind: str,
    law: str,
    write: str,
    result: str,
    successor: str = "Exactly one successor follows from each complete state.",
    determinism: str = "Deterministic for a fixed rule and complete state.",
    termination: str = "The law is iterated for the requested number of steps unless its stated domain condition fails.",
    witness: str = "Every adjacent pair in a valid trajectory satisfies the stated update law.",
    variants: str,
    excluded: str,
    limit: str,
) -> dict[str, str]:
    return {
        "object_kind": kind,
        "native_time": "Discrete successive steps.",
        "carrier": carrier,
        "support": support,
        "topology": topology,
        "structural_invariants": invariants,
        "alphabet_or_value_schema": alphabet,
        "complete_state": state,
        "visible_history": "The ordered sequence of complete numeric states.",
        "seed": seed,
        "input": input_value,
        "frontier_or_activation": frontier,
        "schedule": schedule,
        "read_dependencies_or_neighborhood": read,
        "law_kind": law_kind,
        "rule_relation_constraint_function_or_probability_law": law,
        "write_replacement_assembly_or_commit": write,
        "result_kind": result,
        "successor_cardinality": successor,
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": termination,
        "witness_semantics": witness,
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": excluded,
        "evidence_limit": limit,
    }


def number_map_facts(
    name: str,
    domain: str,
    law: str,
    seed: str,
    variants: str,
) -> dict[str, str]:
    return iterative_facts(
        kind=name,
        carrier="One numeric register n.",
        support="A single scalar position.",
        topology="No spatial adjacency; the next value depends on the current scalar.",
        invariants=f"The state remains in {domain} under the stated scope.",
        alphabet=domain,
        state="The current value of n.",
        seed=seed,
        input_value="The current scalar n.",
        frontier="The one scalar register is active at each step.",
        schedule="Apply the map once per step.",
        read="Read the complete current value of n and any stated arithmetic predicate.",
        law_kind="A deterministic arithmetic map.",
        law=law,
        write="Replace n atomically by the map result.",
        result="A successor number and, under iteration, a numeric sequence.",
        variants=variants,
        excluded="Digit plots, size plots, parity traces, and behavior labels are observers of the numeric trajectory.",
        limit="Finite-precision implementation details are not stated; the mathematical values are treated exactly.",
    )


def recurrence_facts(name: str, law: str, seed: str, read: str) -> dict[str, str]:
    return iterative_facts(
        kind=name,
        carrier="An indexed sequence f[1], f[2], ... of numbers.",
        support="Positive integer indices.",
        topology="Index order supplies access to already generated sequence elements.",
        invariants="Previously generated elements are retained while one new element is appended.",
        alphabet="Integers in the displayed examples.",
        state="The generated prefix f[1] through f[n-1].",
        seed=seed,
        input_value="The current index n and the already generated prefix.",
        frontier="The next not-yet-generated index n.",
        schedule="Generate terms in increasing index order.",
        read=read,
        law_kind="A deterministic recurrence.",
        law=law,
        write="Append the computed value as f[n] without changing earlier terms.",
        result="A new sequence prefix and, by continuation, an infinite or failed recursive sequence.",
        termination="Generation continues while every referenced index is a defined positive earlier index; otherwise the rule fails.",
        variants="The recurrence formula and initial terms are the parameters.",
        excluded="Plots of growth and detrended fluctuations are observers, not recurrence state.",
        limit="The source explicitly notes that many formulas fail by requesting f[0] or negative indices.",
    )


def declarative_facts(
    *,
    kind: str,
    carrier: str,
    support: str,
    alphabet: str,
    state: str,
    input_value: str,
    law_kind: str,
    law: str,
    result: str,
    successor: str,
    determinism: str,
    termination: str,
    witness: str,
    variants: str,
    excluded: str,
    limit: str,
) -> dict[str, str]:
    return {
        "object_kind": kind,
        "native_time": "No native time; this is a fixed function, relation, representation, or query.",
        "carrier": carrier,
        "support": support,
        "topology": "No spatial topology beyond the stated ordered/indexed support.",
        "structural_invariants": "The stated domain, codomain, and relation remain fixed during evaluation.",
        "alphabet_or_value_schema": alphabet,
        "complete_state": state,
        "input": input_value,
        "law_kind": law_kind,
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "successor_cardinality": successor,
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": termination,
        "witness_semantics": witness,
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": excluded,
        "evidence_limit": limit,
    }


def seed_facts(kind: str, carrier: str, support: str, value: str, variants: str) -> dict[str, str]:
    return {
        "object_kind": kind,
        "native_time": "No native time; this object denotes initial data.",
        "carrier": carrier,
        "support": support,
        "topology": "The topology is inherited from the associated evolution law.",
        "structural_invariants": "The complete initial value is fixed as stated.",
        "alphabet_or_value_schema": value,
        "complete_state": value,
        "seed": value,
        "result_kind": "A complete initial state for an associated evolution law.",
        "successor_cardinality": "Exactly one initial state for the stated preset.",
        "determinism_branching_or_measure": "Deterministic, not sampled.",
        "witness_semantics": "The supplied initial state equals the stated value or configuration.",
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": "Its printed digits or drawn row are representations of the seed.",
        "evidence_limit": "Coordinates or finite-display conventions not stated by the source remain outside this seed object.",
    }


# ---------------------------------------------------------------------------
# Sequential-review judgments: number representations and arithmetic maps.

RADIX_FACTS = declarative_facts(
    kind="A positional radix denotation relation for numbers.",
    carrier="An ordered sequence of digits together with a radix b.",
    support="Digit positions indexed from the units position outward, with optional fractional positions.",
    alphabet="Digits 0 through b-1 and positional weights that are powers of b.",
    state="A radix b digit sequence.",
    input_value="A radix b digit sequence and its radix.",
    law_kind="A positional weighted-sum denotation relation.",
    law=(
        "Starting at the right, multiply successive digits by 1, b, b^2, ... "
        "and sum them; fractional positions use reciprocal powers of b."
    ),
    result="The number denoted by the supplied radix digit sequence.",
    successor="One value is denoted by every admitted digit sequence.",
    determinism="Deterministic for a fixed radix and digit sequence.",
    termination="Finite sequences decode by a finite sum; nonterminating fractional expansions denote limiting values.",
    witness="The weighted positional sum equals the represented number.",
    variants="The radix b varies; the source explicitly displays bases 2 through 10.",
    excluded="Typography, black/white cell rendering, and stacked histories do not change the denoted number.",
    limit="The source does not supply a number-to-digits extraction algorithm or a canonical convention for dual terminating/nonterminating fractional expansions.",
)
radix = candidate(
    "radix-family",
    "positional radix denotation relation",
    "U000653",
    RADIX_FACTS,
    aliases=["base-b digit-sequence representation"],
    not_applicable=DECLARATIVE_NA,
    missing="Number-to-digits extraction and the convention for dual terminating/nonterminating fractional expansions are not stated.",
)
evidence(
    radix,
    "radix-introduction",
    "U000653",
    "The passage identifies positional digit-sequence representations and the radix-dependent digit alphabet.",
    [
        "object_kind",
        "native_time",
        "carrier",
        "alphabet_or_value_schema",
        "complete_state",
        "input",
        "law_kind",
        "result_kind",
        *DECLARATIVE_NA,
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    radix,
    "radix-table",
    "U000654",
    "The table explicitly decomposes 3829 into positional weights in bases 2 through 10.",
    fields=[
        "support",
        "topology",
        "structural_invariants",
        "rule_relation_constraint_function_or_probability_law",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "termination_completion_failure",
        "witness_semantics",
        "parameters_and_variants",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="TABLE",
)
context_evidence(
    radix,
    "radix-caption",
    "U000655",
    "The caption states the right-to-left powers-of-base convention and digit alphabets.",
    fields=[
        "alphabet_or_value_schema",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    radix,
    "radix-fractional-assembly",
    "U000798",
    "The passage explicitly treats a digit representation as a procedure for constructing its denoted number.",
    fields=[
        "support",
        "law_kind",
        "result_kind",
        "excluded_observers_and_representations",
        "evidence_limit",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    radix,
    "radix-pi-base10-formula",
    "U000799",
    "The nested base-10 formula directly instantiates fractional positional assembly.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "termination_completion_failure",
        "witness_semantics",
        "parameters_and_variants",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)
context_evidence(
    radix,
    "radix-pi-base2-formula",
    "U000800",
    "The nested base-2 formula independently instantiates fractional positional assembly.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "termination_completion_failure",
        "witness_semantics",
        "parameters_and_variants",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)


def radix_preset(base: int) -> CandidateSpec:
    facts = deepcopy(RADIX_FACTS)
    facts["object_kind"] = f"The displayed positional base-{base} representation of 3829."
    facts["support"] = "Nonnegative whole-number digit positions in the displayed finite decomposition."
    facts["alphabet_or_value_schema"] = f"Digits 0 through {base - 1} with positional weights that are powers of {base}."
    facts["complete_state"] = f"The displayed finite base-{base} digit sequence for 3829."
    facts["input"] = f"The displayed finite base-{base} digit sequence."
    facts["result_kind"] = "The represented whole number 3829."
    facts["termination_completion_failure"] = "The displayed finite weighted sum completes after its last digit."
    facts["parameters_and_variants"] = f"The radix is fixed at b={base}; only the displayed whole-number decomposition is asserted."
    facts["evidence_limit"] = "This row does not supply fractional, inverse-conversion, or canonical-expansion mechanics."
    spec = candidate(
        f"radix-base-{base}",
        f"base-{base} positional representation",
        "U000653",
        facts,
        not_applicable=DECLARATIVE_NA,
        missing="Fractional representation, number-to-digits extraction, and canonical expansion are not established by this table row.",
    )
    evidence(
        spec,
        f"radix-base-{base}-family",
        "U000653",
        "The passage identifies base-dependent positional digit representations.",
        [
            "native_time",
            "carrier",
            "law_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
            *DECLARATIVE_NA,
        ],
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    evidence(
        spec,
        f"radix-base-{base}-table",
        "U000654",
        f"The table directly supplies the base-{base} digit sequence and weighted decomposition of 3829.",
        [
            field
            for field in facts
            if field
            not in {
                "native_time",
                "carrier",
                "law_kind",
                "excluded_observers_and_representations",
                "evidence_limit",
            }
        ],
        strength="DIRECT_COMPLETE_MECHANICS",
        modality="TABLE",
    )
    return spec


radix_presets = {base: radix_preset(base) for base in range(2, 11)}

one_seed = source_candidate(
    "numeric-one-seed",
    "numeric initial value 1",
    "U000661",
    seed_facts(
        "The scalar initial-value preset n=1.",
        "One numeric register.",
        "A single scalar position.",
        "n=1",
        "Used by the displayed addition, multiplication, and rational-power iterations.",
    ),
    not_applicable=SEED_NA,
    missing="No mechanics are missing for the scalar value itself.",
    claim="The arithmetic process is explicitly initialized with the number 1.",
    strength="DIRECT_IDENTITY",
)

ADDITION_FAMILY = number_map_facts(
    "The repeated constant-addition map family.",
    "integers",
    "For a fixed integer c, update n to n+c.",
    "The displayed experiments start from n=1.",
    "The increment c is the parameter; c=1 through 8 are explicitly displayed.",
)
addition_family = source_candidate(
    "constant-addition-family",
    "repeated constant-addition map family",
    "U000661",
    ADDITION_FAMILY,
    not_applicable=EVOLUTION_NA,
    missing="No finite-precision or stopping convention is stated.",
    claim="The passage defines iteration by progressively adding 1, and the later survey varies the fixed added constant.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    addition_family,
    "constant-addition-survey-caption",
    "U000669",
    "The caption fixes the shared seed n=1 and says a constant is successively added.",
    fields=["parameters_and_variants", "seed"],
    strength="DIRECT_COMPLETE_MECHANICS",
)


def addition_preset(c: int) -> CandidateSpec:
    facts = deepcopy(ADDITION_FAMILY)
    facts["object_kind"] = f"The repeated addition map n -> n+{c}."
    facts["rule_relation_constraint_function_or_probability_law"] = f"Update n to n+{c}."
    facts["parameters_and_variants"] = f"The increment is fixed at c={c}; the displayed seed is n=1."
    anchor = "U000661" if c == 1 else "U000668"
    kwargs: dict[str, Any] = {}
    if c != 1:
        kwargs["image_path"] = "CHAPTERS/_page_133_Picture_2.jpeg"
    spec = source_candidate(
        f"constant-add-{c}",
        f"repeated addition by {c}",
        anchor,
        facts,
        not_applicable=EVOLUTION_NA,
        missing="No finite-precision or stopping convention is stated.",
        claim=(
            f"The {'prose' if c == 1 else 'original-resolution survey panel'} "
            f"explicitly labels the update n -> n+{c} from n=1."
        ),
        strength="DIRECT_COMPLETE_MECHANICS",
        **kwargs,
    )
    return spec


addition_presets = {c: addition_preset(c) for c in range(1, 9)}

MULTIPLICATION_FAMILY = number_map_facts(
    "The repeated constant-multiplication map family.",
    "numbers closed under multiplication by the chosen constant",
    "For a fixed factor a, update n to a n.",
    "The displayed experiments start from n=1.",
    "The factor a is the parameter; 2, 3, and 3/2 are explicitly discussed.",
)
multiplication_family = source_candidate(
    "constant-multiplication-family",
    "repeated constant-multiplication map family",
    "U000670",
    MULTIPLICATION_FAMILY,
    not_applicable=EVOLUTION_NA,
    missing="No finite-precision or stopping convention is stated.",
    claim="The passage introduces repeated multiplication by a fixed factor from n=1.",
    strength="DIRECT_COMPLETE_MECHANICS",
)


def multiplication_preset(
    key: str,
    name: str,
    factor: str,
    anchor: str,
    image_path: str | None = None,
) -> CandidateSpec:
    facts = deepcopy(MULTIPLICATION_FAMILY)
    facts["object_kind"] = f"The repeated multiplication map n -> ({factor}) n."
    facts["rule_relation_constraint_function_or_probability_law"] = f"Update n to ({factor}) n."
    facts["parameters_and_variants"] = f"The factor is fixed at {factor}; the displayed seed is n=1."
    return source_candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=EVOLUTION_NA,
        missing="No finite-precision or stopping convention is stated.",
        claim=f"The source directly fixes repeated multiplication by {factor} from 1.",
        strength="DIRECT_COMPLETE_MECHANICS",
        image_path=image_path,
    )


times_two = multiplication_preset(
    "multiply-two",
    "repeated multiplication by 2",
    "2",
    "U000672",
    "CHAPTERS/_page_134_Figure_2.jpeg",
)
times_three = multiplication_preset(
    "multiply-three",
    "repeated multiplication by 3",
    "3",
    "U000673",
    "CHAPTERS/_page_134_Figure_3.jpeg",
)
times_three_halves = multiplication_preset(
    "multiply-three-halves",
    "repeated multiplication by 3/2",
    "3/2",
    "U000680",
)
context_evidence(
    times_three_halves,
    "three-halves-native-panel",
    "U000684",
    "Original-resolution inspection confirms the displayed multiplier 3/2 and the corresponding numeric/digit trajectory.",
    image_path="CHAPTERS/_page_136_Figure_2.jpeg",
    fields=[
        "object_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "parameters_and_variants",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)

DIGIT_SHIFT_NA = {
    field: reason
    for field, reason in DECLARATIVE_NA.items()
    if field != "read_dependencies_or_neighborhood"
}
binary_shift_relation = candidate(
    "binary-arithmetic-shift-relation",
    "base-2 multiplication/division shift correspondence",
    "U000671",
    {
        "object_kind": "A representation-level correspondence between factor-2 arithmetic and base-2 digit shifts.",
        "native_time": "No independent native time; one digit transformation corresponds to one arithmetic operation.",
        "carrier": "An ordered base-2 digit sequence.",
        "support": "Whole and fractional binary digit positions.",
        "topology": "Digit positions are linearly ordered by positional weight.",
        "structural_invariants": "The shifted digit sequence denotes twice or half the original represented value in the stated direction.",
        "alphabet_or_value_schema": "Binary digits 0 and 1.",
        "complete_state": "The complete positional base-2 digit sequence.",
        "input": "A base-2 digit sequence and a choice of multiplication or division by 2.",
        "read_dependencies_or_neighborhood": "A factor-2 shift reads the aligned source digit, while general arithmetic carries can make an output digit depend on arbitrarily distant input digits.",
        "law_kind": "A deterministic digit-representation transformation and arithmetic correspondence.",
        "rule_relation_constraint_function_or_probability_law": "Multiplication by 2 shifts all base-2 digits one place left and appends 0; division by 2 shifts them one place right. Multiplication by 3/2 is multiplication by 3 followed by the right shift.",
        "result_kind": "The shifted base-2 digit sequence representing the multiplied or divided number.",
        "successor_cardinality": "Exactly one shifted digit sequence for each complete input sequence and direction.",
        "determinism_branching_or_measure": "Deterministic.",
        "termination_completion_failure": "A finite displayed shift completes directly; the correspondence also applies positionwise to the stated unbounded positional representation.",
        "witness_semantics": "The positional value of the output is twice or half the positional value of the input, as selected.",
        "parameters_and_variants": "Left shift represents multiplication by 2; right shift represents division by 2; the latter is composed with multiplication by 3 in the 3/2 example.",
        "excluded_observers_and_representations": "The stacked digit histories display repeated uses of the correspondence but are not extra native state.",
        "evidence_limit": "The source does not supply a complete digitwise multiplication-by-3 algorithm; it explicitly warns that carries in general arithmetic can propagate arbitrarily far.",
    },
    not_applicable=DIGIT_SHIFT_NA,
    missing="A complete digitwise multiplication-by-3 procedure and its carry mechanics are not supplied.",
)
evidence(
    binary_shift_relation,
    "binary-shift-left",
    "U000671",
    "The prose states that multiplication by 2 shifts a base-2 digit sequence one place left and appends a zero.",
    [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "topology",
        "structural_invariants",
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
        *DIGIT_SHIFT_NA,
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    binary_shift_relation,
    "binary-shift-caption",
    "U000674",
    "The caption independently identifies the left shift as multiplication by 2.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "witness_semantics",
    ],
    strength="CORROBORATING",
)
context_evidence(
    binary_shift_relation,
    "binary-shift-right",
    "U000685",
    "The caption states that division by 2 is the opposite right shift and that multiplication by 3/2 composes multiplication by 3 with that shift.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    binary_shift_relation,
    "binary-shift-three-halves-panel",
    "U000684",
    "Original-resolution inspection confirms the factor-3/2 identity and its shifted base-2 trajectory.",
    image_path="CHAPTERS/_page_136_Figure_2.jpeg",
    fields=["result_kind", "parameters_and_variants"],
    strength="DIRECT_IDENTITY",
)
context_evidence(
    binary_shift_relation,
    "binary-arithmetic-nonlocal-carry",
    "U000707",
    "The prose states that carries may propagate arbitrarily far left and that an output digit can depend on input digits originally far away.",
    fields=["read_dependencies_or_neighborhood", "evidence_limit"],
    strength="DIRECT_PARTIAL_MECHANICS",
)

fractional_part = source_candidate(
    "fractional-part-observer",
    "fractional-part observer",
    "U000686",
    declarative_facts(
        kind="The observer that returns the fractional part of each number.",
        carrier="A numeric value or numeric trajectory.",
        support="One scalar value at each observed step.",
        alphabet="Real or rational inputs and a result between 0 and 1.",
        state="The input number x.",
        input_value="A number x, applied pointwise to a trajectory when requested.",
        law_kind="A deterministic scalar observer.",
        law="Discard the whole-number part and retain the size of the fractional part.",
        result="FractionalPart[x], or its sequence along a trajectory.",
        successor="Exactly one observed value per input number.",
        determinism="Deterministic.",
        termination="One arithmetic observation completes each evaluation.",
        witness="The input minus the result is an integer and the result lies between 0 and 1.",
        variants="The chapter applies it to successive powers of 3/2.",
        excluded="Plot shading and line segments between sampled dots are explicitly non-significant.",
        limit="The endpoint convention at negative inputs is outside the displayed positive-number scope.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="Negative-input conventions are outside the displayed scope.",
    claim="The passage explicitly defines the observed quantity as the size of each number's fractional part.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    fractional_part,
    "fractional-part-plot-caption",
    "U000688",
    "The caption identifies only the dots as significant and the connecting lines as rendering.",
    fields=["excluded_observers_and_representations"],
)

three_half_parity_map = source_candidate(
    "three-half-parity-map",
    "parity-conditioned 3/2 integer map",
    "U000690",
    number_map_facts(
        "A parity-conditioned integer map using multiplication by 3/2.",
        "whole numbers",
        "If n is even, return 3n/2; if n is odd, first add 1 and return 3(n+1)/2.",
        "The displayed trajectory starts at n=1.",
        "The two branches are selected by parity.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="No stopping condition is stated.",
    claim="The prose gives both parity branches and states that they always produce a whole number.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    three_half_parity_map,
    "three-half-parity-formula",
    "U000693",
    "The caption gives n -> If[EvenQ[n],3 n/2,3(n+1)/2].",
    fields=["rule_relation_constraint_function_or_probability_law"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)

register_arithmetic_map = source_candidate(
    "register-arithmetic-map",
    "register-machine arithmetic map",
    "U000693",
    number_map_facts(
        "The arithmetic map associated with the referenced register machine.",
        "whole numbers",
        "If n is even, return 3n/2; if n is odd, return (3n+1)/2.",
        "The source compares its trajectory after the first step to the n=1 parity-conditioned map.",
        "The two branches are selected by parity.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="The referenced register-machine state encoding and initial-state correspondence require the page-100 target.",
    claim="The caption explicitly prints the two-branch arithmetic rule and routes its machine realization to page 100.",
    strength="DIRECT_COMPLETE_MECHANICS",
    route_keys=["register-page100"],
)

parity_observer = source_candidate(
    "parity-observer",
    "integer parity observer",
    "U000693",
    declarative_facts(
        kind="The observer that classifies each integer as even/0 or odd/1.",
        carrier="One whole number.",
        support="A scalar numeric state or each element of a numeric sequence.",
        alphabet="Whole-number input and binary output 0 or 1.",
        state="The input integer n.",
        input_value="A whole number n.",
        law_kind="A deterministic divisibility predicate encoded as a bit.",
        law="Return 0 when n is divisible by 2 and 1 otherwise.",
        result="One parity bit, or a parity sequence along a trajectory.",
        successor="Exactly one bit per integer.",
        determinism="Deterministic.",
        termination="One divisibility test completes the observation.",
        witness="Even outputs have remainder 0 modulo 2; odd outputs have remainder 1.",
        variants="The chapter applies it to the parity-conditioned 3/2 trajectory.",
        excluded="The black/white digit rendering is not part of the predicate.",
        limit="Only whole-number inputs are in scope.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="No mechanics are missing on whole-number inputs.",
    claim="The caption explicitly says the rightmost digit is 0 for even and 1 for odd.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

five_half_map = source_candidate(
    "five-half-parity-map",
    "parity-conditioned 5/2-or-1/2 integer map",
    "U000697",
    number_map_facts(
        "A parity-conditioned integer map using factors 5/2 and 1/2.",
        "whole numbers",
        "If n is even, return 5n/2; if n is odd, add 1 and return (n+1)/2.",
        "The source displays trajectories from multiple integer seeds, especially n=1 and n=6.",
        "The two branches are selected by parity.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="No stopping condition is stated.",
    claim="The passage directly states both branches of the update.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    five_half_map,
    "five-half-map-formula",
    "U000700",
    "The caption prints n -> If[EvenQ[n],5 n/2,(n+1)/2].",
    fields=["rule_relation_constraint_function_or_probability_law"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)

six_seed = source_candidate(
    "numeric-six-seed",
    "numeric initial value 6 for the 5/2-or-1/2 map",
    "U000701",
    seed_facts(
        "The scalar initial-value preset n=6.",
        "One whole-number register.",
        "A single scalar position.",
        "n=6",
        "Used for the long nonrepeating displayed trajectory of the parity-conditioned 5/2-or-1/2 map.",
    ),
    not_applicable=SEED_NA,
    missing="No mechanics are missing for the scalar value itself.",
    claim="The passage explicitly starts the highlighted trajectory with 6.",
    strength="DIRECT_IDENTITY",
)

digit_length_observer = source_candidate(
    "log-digit-length-observer",
    "logarithmic size and digit-length observer",
    "U000703",
    declarative_facts(
        kind="An observer that reports numeric size on a logarithmic scale, equivalently digit-sequence length up to scale.",
        carrier="A positive whole number.",
        support="One scalar value per observed trajectory step.",
        alphabet="Positive integers mapped to real plot heights.",
        state="The input integer n.",
        input_value="A positive whole number n.",
        law_kind="A deterministic logarithmic-size observer.",
        law="Plot the size of n logarithmically, so height is essentially its digit length.",
        result="One logarithmic size/digit-length value.",
        successor="Exactly one observed value per positive input.",
        determinism="Deterministic once the plot base and scale are fixed.",
        termination="One size calculation completes the observation.",
        witness="Numbers with the same digit length occupy the corresponding logarithmic band.",
        variants="The exact logarithm base and plot scale are rendering parameters not stated.",
        excluded="The plotted polyline and axis scaling are representation choices.",
        limit="The exact log base and normalization are not given.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The exact logarithm base and plot normalization are not stated.",
    claim="The caption says the logarithmic height is essentially the length of the represented digit sequence.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
mark_unknown(
    digit_length_observer,
    {
        "parameters_and_variants": (
            "The assigned passage does not state the logarithm base or plot "
            "normalization used by the size observer."
        )
    },
)

reverse_add = source_candidate(
    "reverse-binary-add-map",
    "reverse-binary-digits-and-add map",
    "U000712",
    number_map_facts(
        "An integer map that reverses base-2 digits and adds the result.",
        "nonnegative whole numbers represented in base 2",
        "Write n in base 2, reverse its complete digit sequence, interpret the reversed sequence as a number, and add it to n.",
        "The chapter displays seeds 16 and 512.",
        "The representation base is fixed at 2.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="The treatment of leading zeros after reversal is not stated, though it does not affect numeric value.",
    claim="The caption explicitly gives the reverse-base-2-digits then add-to-original update.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

seed_16 = source_candidate(
    "numeric-sixteen-seed",
    "numeric initial value 16 for the reverse-add map",
    "U000712",
    seed_facts(
        "The scalar initial-value preset n=16.",
        "One nonnegative integer register.",
        "A single scalar position.",
        "n=16",
        "Used with the reverse-binary-digits-and-add map.",
    ),
    not_applicable=SEED_NA,
    missing="No mechanics are missing for the scalar value itself.",
    claim="The caption explicitly states that the displayed run starts with 16.",
    strength="DIRECT_IDENTITY",
)
seed_512 = source_candidate(
    "numeric-512-seed",
    "numeric initial value 512 for the reverse-add map",
    "U000714",
    seed_facts(
        "The scalar initial-value preset n=512.",
        "One nonnegative integer register.",
        "A single scalar position.",
        "n=512",
        "Used with the reverse-binary-digits-and-add map.",
    ),
    not_applicable=SEED_NA,
    missing="No mechanics are missing for the scalar value itself.",
    claim="The caption explicitly states that the displayed run starts with 512.",
    strength="DIRECT_IDENTITY",
)


# ---------------------------------------------------------------------------
# Recursive sequences.

recursive_schema = source_candidate(
    "recursive-sequence-schema",
    "recursive numeric-sequence construction schema",
    "U000719",
    recurrence_facts(
        "A recursively generated numeric sequence.",
        "A rule computes f[n] from already generated sequence elements.",
        "One or more explicitly supplied initial terms.",
        "The dependencies named by the particular recurrence, which may be fixed-lag or value-indexed.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="A particular recurrence formula and initial terms must be supplied.",
    claim="The passage defines f[n] notation and the construction of each next term from previous ones.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    recursive_schema,
    "recursive-variable-index-class",
    "U000724",
    "The passage introduces recurrences whose dependency index is computed from earlier sequence values.",
    fields=[
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    recursive_schema,
    "recursive-variable-index-partiality",
    "U000725",
    "The prose explicitly states that a computed dependency can be nonpositive and make terms such as f[0] or f[-1] meaningless.",
    fields=[
        "termination_completion_failure",
        "evidence_limit",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    recursive_schema,
    "recursive-variable-index-survival",
    "U000727",
    "The prose distinguishes the displayed recurrences as examples that avoid the common undefined-index failure.",
    fields=[
        "termination_completion_failure",
        "parameters_and_variants",
    ],
    strength="CORROBORATING",
)

fixed_recurrences = [
    ("fixed-rec-a", "fixed-lag recurrence f[n]=1+f[n-1]", "f[n]=1+f[n-1]", "f[1]=1", "Read f[n-1]."),
    ("fixed-rec-b", "fixed-lag recurrence f[n]=1-f[n-1]", "f[n]=1-f[n-1]", "f[1]=1", "Read f[n-1]."),
    ("fixed-rec-c", "fixed-lag recurrence f[n]=2 f[n-1]", "f[n]=2 f[n-1]", "f[1]=1", "Read f[n-1]."),
    ("fixed-rec-d", "Fibonacci recurrence", "f[n]=f[n-1]+f[n-2]", "f[1]=1, f[2]=1", "Read f[n-1] and f[n-2]."),
    ("fixed-rec-e", "difference recurrence f[n]=f[n-1]-f[n-2]", "f[n]=f[n-1]-f[n-2]", "f[1]=1, f[2]=1", "Read f[n-1] and f[n-2]."),
    ("fixed-rec-f", "signed difference recurrence f[n]=-f[n-1]+f[n-2]", "f[n]=-f[n-1]+f[n-2]", "f[1]=1, f[2]=1", "Read f[n-1] and f[n-2]."),
]
fixed_specs: dict[str, CandidateSpec] = {}
for key, name, law, initial, read in fixed_recurrences:
    fixed_specs[key] = source_candidate(
        key,
        name,
        "U000722",
        recurrence_facts(name, law, initial, read),
        not_applicable=EVOLUTION_NA,
        missing="No failure occurs after the displayed initial terms for this fixed-lag recurrence.",
        claim=f"Original-resolution inspection directly transcribes {law} with {initial}.",
        strength="DIRECT_COMPLETE_MECHANICS",
        image_path="CHAPTERS/_page_143_Figure_6.jpeg",
    )

variable_recurrences = [
    ("variable-rec-a", "value-indexed recurrence case (a)", "f[n]=1+f[n-f[n-1]]", "f[1]=1", "Read f[n-1], then f[n-f[n-1]]."),
    ("variable-rec-b", "value-indexed recurrence case (b)", "f[n]=2+f[n-f[n-1]]", "f[1]=1, f[2]=1", "Read f[n-1], then f[n-f[n-1]]."),
    ("variable-rec-c", "value-indexed recurrence case (c)", "f[n]=f[f[n-1]]+f[n-f[n-1]]", "f[1]=1, f[2]=1", "Read f[n-1], then f[f[n-1]] and f[n-f[n-1]]."),
    ("variable-rec-d", "value-indexed recurrence case (d)", "f[n]=f[n-f[n-1]]+f[n-f[n-2]-1]", "f[1]=1, f[2]=1", "Read f[n-1], f[n-2], and the two resulting indexed terms."),
    ("variable-rec-e", "value-indexed recurrence case (e)", "f[n]=f[n-f[n-1]]+f[n-f[n-2]]", "f[1]=1, f[2]=1", "Read f[n-1], f[n-2], and the two resulting indexed terms."),
    ("variable-rec-f", "value-indexed recurrence case (f)", "f[n]=f[n-f[n-1]-1]+f[n-f[n-2]-1]", "f[1]=1, f[2]=1", "Read f[n-1], f[n-2], and the two resulting indexed terms."),
    ("variable-rec-g", "value-indexed recurrence case (g)", "f[n]=f[f[n-1]]+f[n-f[n-2]-1]", "f[1]=1, f[2]=1", "Read f[n-1], f[n-2], then f[f[n-1]] and f[n-f[n-2]-1]."),
    ("variable-rec-h", "value-indexed recurrence case (h)", "f[n]=f[f[n-1]]+f[n-2 f[n-1]+1]", "f[1]=1, f[2]=1", "Read f[n-1], then f[f[n-1]] and f[n-2 f[n-1]+1]."),
]
variable_specs: dict[str, CandidateSpec] = {}
for key, name, law, initial, read in variable_recurrences:
    variable_specs[key] = source_candidate(
        key,
        name,
        "U000726",
        recurrence_facts(name, law, initial, read),
        not_applicable=EVOLUTION_NA,
        missing="The rule fails if a computed reference is not a defined positive earlier index; the displayed trajectory avoids this.",
        claim=f"Original-resolution inspection directly transcribes {law} with {initial}.",
        strength="DEFECT_LIMITED",
        image_path="CHAPTERS/_page_144_Figure_3.jpeg",
        source_status=["DEFECTIVE"],
        uncertainties=[
            "The recurrence formulas and shown prefixes are legible, but the asset has hard bottom-edge bleed/cut through the following plot row."
        ],
    )
    variable_specs[key]["anchor"] = "U000724"
    variable_specs[key]["evidence"][0]["fields"] = [
        field
        for field in variable_specs[key]["evidence"][0]["fields"]
        if field
        not in {
            "termination_completion_failure",
            "evidence_limit",
        }
    ]
    context_evidence(
        variable_specs[key],
        f"{key}-class-anchor",
        "U000724",
        "The passage introduces the value-indexed recurrence class to which this displayed case belongs.",
        strength="DIRECT_IDENTITY",
    )
    context_evidence(
        variable_specs[key],
        f"{key}-partiality",
        "U000725",
        "The passage states the exact undefined-index failure mode for this recurrence class.",
        fields=[
            "termination_completion_failure",
            "evidence_limit",
        ],
        strength="DIRECT_PARTIAL_MECHANICS",
    )
    context_evidence(
        variable_specs[key],
        f"{key}-survival",
        "U000727",
        "The prose states that the particular displayed rules avoid the otherwise common nonpositive-index failure.",
        fields=["termination_completion_failure"],
        strength="CORROBORATING",
    )


def observer_candidate(
    key: str,
    name: str,
    anchor: str,
    law: str,
    input_value: str,
    result: str,
    *,
    image_path: str | None = None,
    missing: str = "No mechanics are missing within the stated input scope.",
) -> CandidateSpec:
    return source_candidate(
        key,
        name,
        anchor,
        declarative_facts(
            kind=name,
            carrier="A number, index, or generated numeric sequence.",
            support="The stated scalar input or sequence index.",
            alphabet="Numeric inputs and numeric or Boolean outputs as stated.",
            state=input_value,
            input_value=input_value,
            law_kind="A deterministic observer or analyzer.",
            law=law,
            result=result,
            successor="Exactly one observation per valid input.",
            determinism="Deterministic.",
            termination="One evaluation completes the observation.",
            witness="Direct recomputation from the stated input reproduces the result.",
            variants="Parameters are those explicitly present in the formula.",
            excluded="Plot style and axis scaling do not change the observed value.",
            limit=missing,
        ),
        not_applicable=DECLARATIVE_NA,
        missing=missing,
        claim=f"The source explicitly defines {law}.",
        strength="DIRECT_COMPLETE_MECHANICS" if "not stated" not in missing else "DIRECT_PARTIAL_MECHANICS",
        image_path=image_path,
    )


detrend_half = observer_candidate(
    "recurrence-half-detrender",
    "recursive-sequence linear detrending observer",
    "U000728",
    "For cases (c) through (g), return f[n]-n/2.",
    "A recurrence output f[n] and its index n.",
    "The fluctuation around the n/2 trend.",
    image_path="CHAPTERS/_page_145_Figure_1.jpeg",
)
detrend_power = observer_candidate(
    "recurrence-power-detrender",
    "recursive-sequence power-law detrending observer",
    "U000728",
    "For case (h), return f[n]-0.42 n^0.818.",
    "Case-(h) output f[n] and its index n.",
    "The fluctuation around the fitted power-law trend.",
    image_path="CHAPTERS/_page_145_Figure_1.jpeg",
)
hamming_weight = observer_candidate(
    "binary-hamming-weight",
    "base-2 digit-one count",
    "U000735",
    "Write n in base 2 and count the digits equal to 1.",
    "A nonnegative integer n.",
    "The number of 1 digits in n's base-2 representation.",
)
cumulative_hamming = observer_candidate(
    "cumulative-binary-one-count",
    "cumulative base-2 digit-one count",
    "U000735",
    "Sum the number of 1 digits over the base-2 representations of all nonnegative integers less than n.",
    "A nonnegative integer n.",
    "The total number of 1 digits in all integers below n.",
)


# ---------------------------------------------------------------------------
# Primes, number-theoretic sequences, and declarative questions.

prime_sequence = source_candidate(
    "prime-sequence",
    "sequence of prime numbers",
    "U000739",
    declarative_facts(
        kind="The ordered sequence of prime numbers.",
        carrier="Positive whole numbers.",
        support="The positive integers ordered by size.",
        alphabet="Whole numbers and a divisibility predicate.",
        state="A candidate positive integer n or the ordered set of accepted integers.",
        input_value="A positive integer n for membership, or an index for ordered enumeration.",
        law_kind="A divisibility predicate together with increasing-order enumeration.",
        law="Accept n>1 exactly when no whole number other than 1 and n divides it; enumerate accepted n in increasing order.",
        result="A prime-membership truth value or the ordered prime sequence 2,3,5,7,...",
        successor="Each input has one truth value; every sequence index has one nth prime.",
        determinism="Deterministic.",
        termination="Membership can be decided by finite divisor checks for each finite n; enumeration continues without bound.",
        witness="A prime has no nontrivial divisor; a composite has a divisor other than 1 and itself.",
        variants="Membership and ordered enumeration are the two stated views of the same set.",
        excluded="Distribution plots and asymptotic estimates are observers of the prime sequence.",
        limit="The chapter states infinitude but does not give its proof here.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The proof that the sequence is infinite is not supplied in this passage.",
    claim="The passage defines primes by absence of nontrivial divisors and lists the increasing sequence.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

sieve = source_candidate(
    "eratosthenes-sieve",
    "sieve of Eratosthenes prime filter",
    "U000740",
    iterative_facts(
        kind="An iterative filtering procedure that leaves exactly the primes.",
        carrier="Candidate positive integers with retained/removed marks.",
        support="All positive integers, or the displayed finite interval 1 through 100.",
        topology="Integers are ordered by value; each filtering stage is indexed by the next divisor.",
        invariants="Once removed, an integer remains removed; only numbers larger than the current divisor are removed at that stage.",
        alphabet="Retained or removed status for each integer.",
        state="The current retained subset and the current divisor stage.",
        seed="Initially all candidate integers are retained.",
        input_value="The retained set and the current integer p.",
        frontier="At stage p, retained numbers larger than p that are divisible by p are eligible for removal.",
        schedule="Process p=2,3,4,... in increasing order.",
        read="For each candidate n>p, test whether p divides n.",
        law_kind="A deterministic monotone filter.",
        law="At stage p remove every n>p divisible by p; retain all other current candidates.",
        write="Commit all removals for the current p while preserving prior removals.",
        result="After unbounded continuation, the retained numbers are exactly the primes.",
        termination="The infinite construction continues forever; a bounded prefix can stop after enough divisor stages.",
        variants="The displayed finite illustration uses integers 1 through 100.",
        excluded="Gray dots and row layout display removal history but are not extra filter state.",
        limit="The treatment of 1 in the displayed top row is clear visually, while the prose identifies the surviving prime set beginning at 2.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="No mechanics are missing for the stated unbounded filter.",
    claim="The prose explicitly gives the successive removal rule and identifies the limit set as the primes.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    sieve,
    "sieve-panel",
    "U000741",
    "Original-resolution inspection confirms the row-by-row retained/removed filter through the displayed divisor stages.",
    image_path="CHAPTERS/_page_147_Figure_4.jpeg",
    fields=["visible_history", "parameters_and_variants"],
)

prime_nth = observer_candidate(
    "nth-prime-function",
    "nth-prime function",
    "U000744",
    "Return Prime[n], the nth member of the increasing prime sequence.",
    "A positive integer index n.",
    "The nth prime number.",
    image_path="CHAPTERS/_page_148_Figure_1.jpeg",
)
prime_pi = observer_candidate(
    "prime-counting-function",
    "prime-counting function",
    "U000744",
    "Return the number PrimePi[n] of primes smaller than n.",
    "A positive number n.",
    "The count of primes below n.",
    image_path="CHAPTERS/_page_148_Figure_1.jpeg",
)

prime_error_facts = declarative_facts(
    kind="The prime-counting error observer LogIntegral[n]-PrimePi[n].",
    carrier="A positive scalar n.",
    support="Positive real or integer arguments n.",
    alphabet="A positive input and a real-valued difference.",
    state="The input n.",
    input_value="A positive value n.",
    law_kind="A difference of two scalar functions.",
    law="Evaluate LogIntegral[n]-PrimePi[n].",
    result="The signed difference between the logarithmic-integral estimate and the number of primes below n.",
    successor="Exactly one difference when both component functions are fixed.",
    determinism="Deterministic.",
    termination="One evaluation completes the observation.",
    witness="Adding PrimePi[n] back to the result yields LogIntegral[n].",
    variants="The plotted range is a rendering parameter.",
    excluded="The plotted line and shaded area are representations.",
    limit="PrimePi is described, but the exact definition/convention for LogIntegral is not given in the assigned chapter.",
)
prime_error = source_candidate(
    "prime-counting-error",
    "logarithmic-integral prime-counting error",
    "U000744",
    prime_error_facts,
    not_applicable=DECLARATIVE_NA,
    missing="The exact definition and endpoint convention for LogIntegral are not supplied.",
    claim="The original-resolution panel explicitly labels the observer LogIntegral[n]-PrimePi[n].",
    strength="DIRECT_PARTIAL_MECHANICS",
    image_path="CHAPTERS/_page_148_Figure_1.jpeg",
    uncertainties=["The component LogIntegral is named but not defined in the assigned source."],
)
prime_mod3 = observer_candidate(
    "prime-mod3-excess",
    "prime residue-class excess modulo 3",
    "U000744",
    "Count primes of the form 3k-1 below the bound and subtract the count of primes of the form 3k+1.",
    "A positive bound.",
    "The signed excess of the two stated prime residue classes.",
    image_path="CHAPTERS/_page_148_Figure_1.jpeg",
)
prime_mod4 = observer_candidate(
    "prime-mod4-excess",
    "prime residue-class excess modulo 4",
    "U000744",
    "Count primes of the form 4k-1 below the bound and subtract the count of primes of the form 4k+1.",
    "A positive bound.",
    "The signed excess of the two stated prime residue classes.",
    image_path="CHAPTERS/_page_148_Figure_1.jpeg",
)
prime_gaps = observer_candidate(
    "successive-prime-gaps",
    "successive-prime gap sequence",
    "U000744",
    "For consecutive primes p_n and p_(n+1), return p_(n+1)-p_n.",
    "Two successive members of the prime sequence, or an index n.",
    "The gap between successive primes.",
    image_path="CHAPTERS/_page_148_Figure_1.jpeg",
)


def number_property_sequence(
    key: str,
    name: str,
    anchor: str,
    law: str,
    result: str,
    *,
    image_path: str | None = None,
) -> CandidateSpec:
    return source_candidate(
        key,
        name,
        anchor,
        declarative_facts(
            kind=name,
            carrier="Positive whole numbers.",
            support="One output position for each integer n.",
            alphabet="Whole-number inputs and integer counts or sums.",
            state="The input integer n.",
            input_value="A positive whole number n.",
            law_kind="A deterministic arithmetic function of n.",
            law=law,
            result=result,
            successor="Exactly one value for each n.",
            determinism="Deterministic.",
            termination="The finite divisor, tuple, or prime-pair enumeration completes for each finite n.",
            witness="The counted or summed objects satisfy the stated arithmetic condition.",
            variants="The input n ranges over the positive integers, restricted to even n where explicitly stated.",
            excluded="The plotted curve is a representation of the sequence.",
            limit="Ordering and sign conventions are only those explicitly stated in the caption.",
        ),
        not_applicable=DECLARATIVE_NA,
        missing="The source does not specify whether permutation/sign variants are counted separately beyond the plotted convention.",
        claim=f"The source explicitly defines the sequence value by: {law}",
        strength="DIRECT_PARTIAL_MECHANICS",
        image_path=image_path,
    )


divisor_count = number_property_sequence(
    "divisor-count-sequence",
    "divisor-count sequence",
    "U000753",
    "Count the divisors of n, including n.",
    "The number of divisors of n.",
    image_path="CHAPTERS/_page_150_Figure_1.jpeg",
)
proper_divisor_difference = number_property_sequence(
    "proper-divisor-difference",
    "proper-divisor-sum difference sequence",
    "U000754",
    "Sum the divisors of n excluding n, then subtract n.",
    "The sum of proper divisors minus n.",
    image_path="CHAPTERS/_page_150_Figure_2.jpeg",
)
for _exact_property in [divisor_count, proper_divisor_difference]:
    _exact_property["facts"]["evidence_limit"] = (
        "The caption fixes the divisor inclusion/exclusion convention needed "
        "for this exact scalar observer."
    )
    _exact_property["missing"] = (
        "No mechanics are missing within the stated positive-integer scope."
    )
    _exact_property["evidence"][0]["strength"] = "DIRECT_COMPLETE_MECHANICS"
three_square_count = number_property_sequence(
    "three-square-count",
    "three-square representation-count sequence",
    "U000755",
    "Count the ways of expressing n as a sum of three squares.",
    "The number of three-square representations of n.",
    image_path="CHAPTERS/_page_150_Figure_3.jpeg",
)
four_square_count = number_property_sequence(
    "four-square-count",
    "four-square representation-count sequence",
    "U000758",
    "Count the ways of expressing n as a sum of four squares.",
    "The number of four-square representations of n.",
)
goldbach_count = number_property_sequence(
    "goldbach-pair-count",
    "two-prime representation-count sequence",
    "U000759",
    "For even n, count the ways of expressing n as the sum of two primes.",
    "The number of prime-pair representations of even n.",
)

perfect_predicate = source_candidate(
    "perfect-number-predicate",
    "perfect-number predicate",
    "U000760",
    declarative_facts(
        kind="The predicate that a number is perfect.",
        carrier="Positive whole numbers.",
        support="One integer n.",
        alphabet="Whole-number input and Boolean output.",
        state="The input integer n.",
        input_value="A positive whole number n.",
        law_kind="A zero-test on the proper-divisor-sum difference.",
        law="Accept n exactly when the sum of its divisors excluding n, minus n, is zero.",
        result="True for perfect numbers and false otherwise.",
        successor="Exactly one truth value per n.",
        determinism="Deterministic.",
        termination="Finite divisor enumeration decides every finite n.",
        witness="The proper divisors of an accepted n sum exactly to n.",
        variants="Even and odd inputs are both admitted.",
        excluded="The plotted sequence is an observer used to locate zeros.",
        limit="The source states the known form of even perfect numbers but does not print that form here.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The explicit known form of even perfect numbers is not included in this passage.",
    claim="The caption states that zeros of the proper-divisor-difference sequence are perfect numbers.",
    strength="DIRECT_COMPLETE_MECHANICS",
)


def yes_no_query(
    key: str,
    name: str,
    anchor: str,
    law: str,
    witness: str,
    missing: str,
) -> CandidateSpec:
    return source_candidate(
        key,
        name,
        anchor,
        declarative_facts(
            kind=name,
            carrier="The explicitly stated mathematical domain.",
            support="All objects quantified by the question.",
            alphabet="A yes/no result with mathematical witnesses or proofs.",
            state="The complete quantified proposition.",
            input_value="The proposition as stated.",
            law_kind="A declarative existence or universal-validity query.",
            law=law,
            result="YES if the proposition holds and NO if a counterexample/nonexistence proof holds.",
            successor="Exactly one mathematically correct truth value, whether or not currently known.",
            determinism="Declarative and non-probabilistic.",
            termination="An accepted proof or counterexample completes the query; the source reports no result.",
            witness=witness,
            variants="No variants beyond the stated quantified domain.",
            excluded="Search time, historical effort, and plots are not part of the proposition.",
            limit=missing,
        ),
        not_applicable=DECLARATIVE_NA,
        missing=missing,
        claim=f"The source explicitly isolates the unresolved query: {law}",
        strength="DIRECT_COMPLETE_MECHANICS",
    )


odd_perfect_query = yes_no_query(
    "odd-perfect-existence",
    "odd perfect-number existence query",
    "U000760",
    "Determine whether any odd positive integer has proper divisors summing to itself.",
    "YES requires one odd perfect integer; NO requires a proof that none exists.",
    "The source reports that no answer is known.",
)
goldbach_query = yes_no_query(
    "goldbach-query",
    "Goldbach universal representation query",
    "U000760",
    "Determine whether every even number in the stated sequence has at least one representation as a sum of two primes.",
    "NO requires one even counterexample with zero representations; YES requires a universal proof.",
    "The source reports that no proof or counterexample is known.",
)


# ---------------------------------------------------------------------------
# Constants, digit algorithms, and alternative representations.

pi_constant = source_candidate(
    "pi-constant",
    "circle ratio constant pi",
    "U000765",
    declarative_facts(
        kind="The mathematical constant pi.",
        carrier="Circles with circumference and diameter.",
        support="The class of circles in the stated geometry.",
        alphabet="Positive real-valued lengths and their ratio.",
        state="A circle's circumference C and diameter D.",
        input_value="Any circle with circumference C and diameter D.",
        law_kind="A ratio-defined invariant constant.",
        law="pi is the ratio C/D of circumference to diameter for any circle.",
        result="The same real number pi for every admitted circle.",
        successor="Exactly one ratio value.",
        determinism="Declarative and deterministic.",
        termination="One exact ratio evaluation denotes the constant.",
        witness="A valid witness is a circle whose circumference-to-diameter ratio equals the denoted value.",
        variants="The displayed decimal and binary sequences are representations of the same constant.",
        excluded="Digit bases, finite prefixes, and pictorial walks do not alter pi.",
        limit="The geometric foundations that prove circle-independence are not developed here.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The geometric proof that the ratio is circle-independent is not supplied.",
    claim="The passage explicitly defines pi as the ratio of any circle's circumference to its diameter.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

pi_digits = source_candidate(
    "pi-digit-representation",
    "radix digit-sequence representation of pi",
    "U000766",
    declarative_facts(
        kind="The base-10 or base-2 positional digit sequence denoting pi.",
        carrier="An infinite ordered digit sequence.",
        support="One integer part followed by fractional digit positions.",
        alphabet="Digits 0 through 9 in base 10 or bits 0 and 1 in base 2.",
        state="The infinite positional expansion of pi in the selected base.",
        input_value="The constant pi and a selected base 10 or 2.",
        law_kind="Application of the positional radix representation codec.",
        law="Choose the digit sequence whose positional weighted sum denotes pi in the selected base.",
        result="The infinite base-10 or base-2 expansion of pi.",
        successor="One canonical nonterminating expansion in each selected base.",
        determinism="Deterministic for the base and canonical convention.",
        termination="The full sequence is infinite; every requested finite prefix is finite.",
        witness="Every finite prefix bounds/refines the represented value according to positional weights.",
        variants="Base 10 and base 2 are displayed.",
        excluded="The printed 4000-digit page and black/white rendering are finite representations.",
        limit="No digit-generation algorithm is supplied for pi in this section.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The source supplies the denotation and prefixes but no algorithm for generating arbitrary later digits.",
    claim="The passage explicitly presents pi's base-10 and base-2 digit sequences as representations of the defined constant.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    pi_digits,
    "pi-dense-digit-page",
    "U000769",
    "Original-resolution inspection and independent checking confirm that the dense page is a finite base-10/base-2 prefix of pi.",
    image_path="CHAPTERS/_page_152_Pi_Digits.jpeg",
    fields=[
        "result_kind",
        "parameters_and_variants",
        "excluded_observers_and_representations",
    ],
    strength="DIRECT_IDENTITY",
)
context_evidence(
    pi_digits,
    "pi-radix-assembly-principle",
    "U000798",
    "The passage identifies a digit representation as a procedure for constructing its denoted number.",
    fields=[
        "law_kind",
        "result_kind",
        "excluded_observers_and_representations",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    pi_digits,
    "pi-base10-assembly-formula",
    "U000799",
    "The nested base-10 formula directly assembles pi from the displayed decimal digits.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "witness_semantics",
        "parameters_and_variants",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)
context_evidence(
    pi_digits,
    "pi-base2-assembly-formula",
    "U000800",
    "The nested base-2 formula directly assembles pi from the displayed binary digits.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "witness_semantics",
        "parameters_and_variants",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)

pi_walk = observer_candidate(
    "pi-binary-walk",
    "binary-digit up/down walk observer",
    "U000768",
    "Scan the base-2 digits in order; move the cumulative curve up for digit 1 and down for digit 0.",
    "An ordered binary digit sequence.",
    "The cumulative signed walk after each digit.",
)

rational_class = source_candidate(
    "rational-number-class",
    "rational-number class",
    "U000773",
    declarative_facts(
        kind="The class of numbers expressible as p/q for whole numbers p and q.",
        carrier="Pairs of whole numbers p,q with nonzero denominator.",
        support="Scalar numbers.",
        alphabet="Whole-number pairs and their quotient values.",
        state="A pair (p,q) or the quotient p/q.",
        input_value="Whole numbers p and nonzero q.",
        law_kind="A quotient denotation.",
        law="Map (p,q) to the number p/q.",
        result="A rational number.",
        successor="One quotient value per valid pair; many pairs may denote the same value.",
        determinism="Deterministic.",
        termination="One exact division denotes the value.",
        witness="A number is rational when some whole-number pair p,q denotes it as p/q.",
        variants="Numerator, denominator, and display base vary.",
        excluded="A particular decimal or binary expansion is a representation.",
        limit="Sign and reduction-to-lowest-terms conventions are not discussed.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="Sign and canonical reduced-pair conventions are not stated.",
    claim="The passage explicitly identifies rational numbers as numbers obtained by dividing pairs of whole numbers.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

rational_periodicity = source_candidate(
    "rational-radix-periodicity",
    "rational radix-expansion periodicity relation",
    "U000776",
    declarative_facts(
        kind="The relation between rational numbers and eventually repeating radix digit sequences.",
        carrier="A rational p/q, a radix, and its positional digit sequence.",
        support="Fractional digit positions.",
        alphabet="Radix digits and a repetition period.",
        state="The complete radix expansion of p/q.",
        input_value="A rational number p/q and a representation base.",
        law_kind="A declarative periodicity constraint.",
        law="The digit sequence eventually repeats; in the displayed base-2/base-10 cases the period is at most q-1.",
        result="A repetitive digit sequence with the stated period bound.",
        successor="One canonical expansion per rational and base.",
        determinism="Declarative and deterministic under a canonical expansion convention.",
        termination="The property is witnessed by a finite preperiod and period.",
        witness="A finite block repeats forever after some position and its period does not exceed q-1.",
        variants="Base 10 and base 2 examples are displayed.",
        excluded="Printed truncation does not terminate the mathematical expansion.",
        limit="The q-1 bound is stated in the displayed context; exceptional terminating expansions are treated as trailing zeros.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="No mechanics are missing within the stated representation convention.",
    claim="The caption explicitly states eventual repetition and the period-at-most-q-1 bound.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

long_division = source_candidate(
    "binary-long-division",
    "binary long-division digit generator",
    "U000780",
    iterative_facts(
        kind="An iterative generator for the base-2 digits of p/q.",
        carrier="A remainder register r and an output bit sequence.",
        support="One scalar remainder plus ordered output positions.",
        topology="Output digits are appended left to right in generation order.",
        invariants="The remainder remains less than q under the stated proper-fraction scope.",
        alphabet="Whole-number remainders and output bits 0 or 1.",
        state="The current remainder r and generated output prefix.",
        seed="Initialize r=p.",
        input_value="The current r and fixed denominator q.",
        frontier="The one remainder register and next output position.",
        schedule="Generate one digit and successor remainder per step.",
        read="Compare 2r with q.",
        law_kind="A deterministic two-branch division algorithm.",
        law="If 2r<q output 0 and set r=2r; otherwise output 1 and set r=2r-q.",
        write="Append the chosen bit and atomically replace r.",
        result="The base-2 fractional digit sequence for p/q.",
        variants="The numerator p and denominator q vary.",
        excluded="Black/white remainder diagrams and column layout are representations.",
        limit="The prose assumes a range in which r starts below q; handling a whole-number part is not specified.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="Initialization when p>=q and extraction of a whole-number part are outside the stated procedure.",
    claim="The passage supplies initialization, comparison, emitted bit, and both remainder updates.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    long_division,
    "binary-long-division-panel",
    "U000778",
    "Original-resolution inspection confirms examples 1/q with remainder histories and generated bits.",
    image_path="CHAPTERS/_page_154_Figure_2.jpeg",
    fields=["visible_history", "parameters_and_variants"],
)

square_root_function = source_candidate(
    "square-root-function",
    "square-root relation on whole numbers",
    "U000782",
    declarative_facts(
        kind="The nonnegative square-root relation n -> sqrt(n).",
        carrier="Whole-number radicands and nonnegative real results.",
        support="One scalar radicand n.",
        alphabet="Whole-number inputs and real-valued outputs.",
        state="A radicand n and proposed root x.",
        input_value="A nonnegative whole number n.",
        law_kind="An inverse-squaring relation.",
        law="Return the nonnegative x whose square is n.",
        result="sqrt(n).",
        successor="Exactly one nonnegative square root per nonnegative n.",
        determinism="Declarative and deterministic under the nonnegative-root convention.",
        termination="The relation denotes a value even when its radix expansion is infinite.",
        witness="A valid result x is nonnegative and satisfies x*x=n.",
        variants="Perfect-square and nonsquare radicands are contrasted.",
        excluded="Decimal and binary digit strings are representations of the root.",
        limit="The source does not discuss negative or complex radicands.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="Negative and complex input conventions are outside the source.",
    claim="The passage contrasts perfect squares with other square roots and tabulates sqrt(n), delimiting the nonnegative root relation.",
    strength="DIRECT_COMPLETE_MECHANICS",
)

sqrt_generator = source_candidate(
    "binary-square-root-generator",
    "binary square-root digit generator",
    "U000787",
    iterative_facts(
        kind="An iterative two-register generator for binary square-root digits.",
        carrier="Numeric registers r and s.",
        support="Two scalar registers and successive output positions.",
        topology="No spatial adjacency; both registers update together.",
        invariants="The two-register form persists; the binary digits of s successively agree with sqrt(n).",
        alphabet="Whole-number register values and binary digits.",
        state="The pair (r,s).",
        seed="Initialize r=n and s=0, after scaling n into the stated range when needed.",
        input_value="The current pair (r,s).",
        frontier="Both registers are active at every step.",
        schedule="Perform one simultaneous pair update per generated digit.",
        read="Compare r and s and read both complete values.",
        law_kind="A deterministic conditional pair map.",
        law="If r>s, set (r,s)=(4(r-s-1),2(s+2)); otherwise set (r,s)=(4r,2s).",
        write="Commit the new r and s atomically.",
        result="Successive base-2 digits of s, which correspond to sqrt(n).",
        variants="If n is outside 1 through 4, first multiply or divide it by an appropriate power of 4.",
        excluded="The triangular bit histories are representations of register evolution.",
        limit="The exact rescaling exponent-selection convention is described only as 'appropriate'.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="The exact convention for choosing and undoing the preliminary power-of-4 scaling is not fully stated.",
    claim="The passage gives both initial register values, the complete conditional pair update, and the digit interpretation.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    sqrt_generator,
    "sqrt-generator-formula",
    "U000790",
    "The caption repeats the exact pair map and power-of-4 input restriction.",
    fields=["rule_relation_constraint_function_or_probability_law", "parameters_and_variants"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)


def partial_function_family(key: str, name: str, anchor: str, law: str, result: str) -> CandidateSpec:
    return source_candidate(
        key,
        name,
        anchor,
        {
            "object_kind": f"Displayed {name} expressions and their value representations.",
            "native_time": "No native time; these are fixed displayed denotations.",
            "input": "Only the named expressions and arguments printed in the table.",
            "law_kind": "A named mathematical-function denotation.",
            "rule_relation_constraint_function_or_probability_law": law,
            "result_kind": result,
            "parameters_and_variants": "Only the explicitly displayed expressions and arguments are in scope.",
            "excluded_observers_and_representations": "The decimal and binary digit strings are representations of the displayed values.",
            "evidence_limit": "The table identifies examples but does not state a full domain, branch convention, general law, or evaluator.",
        },
        not_applicable=DECLARATIVE_NA,
        missing="The full domain, branch convention, and native evaluation mechanics are not defined in the assigned source.",
        claim=f"The table identifies displayed {name} expressions and their result digit sequences, without defining a general evaluator.",
        strength="DIRECT_IDENTITY",
        unknown_reasons={
            "carrier": "The table does not delimit a carrier or full domain for this named function.",
            "support": "The table gives examples, not a support set for a general function object.",
            "topology": "No topology is specified for the displayed denotations.",
            "structural_invariants": "No structural invariant is stated for a general evaluator.",
            "alphabet_or_value_schema": "No formal input or result schema is stated beyond the displayed expressions.",
            "complete_state": "The fixed denotations have no stated operational state.",
            "successor_cardinality": "The table does not define a general successor or branch convention.",
            "determinism_branching_or_measure": "A general branch convention is not stated.",
            "termination_completion_failure": "No evaluation procedure or completion criterion is supplied.",
            "witness_semantics": "The displayed digits identify results but no general witness relation is defined.",
        },
    )


cube_root_family = partial_function_family(
    "cube-root-family", "cube-root function family", "U000793", "Take the named cube root of the input.", "The displayed cube-root value."
)
fourth_root_family = partial_function_family(
    "fourth-root-family", "fourth-root function family", "U000793", "Take the named fourth root of the input.", "The displayed fourth-root value."
)
log_family = partial_function_family(
    "natural-log-family", "natural logarithm function family", "U000793", "Apply the function denoted Log to the displayed positive input.", "The displayed logarithm value."
)
exp_family = partial_function_family(
    "exponential-family", "exponential function and constant-e family", "U000793", "Use e and its displayed powers or roots.", "The displayed exponential-derived value."
)

continued_fraction = candidate(
    "continued-fraction-representation",
    "continued-fraction coefficient-sequence denotation",
    "U000801",
    {
        **declarative_facts(
        kind="A one-way denotation from a continued-fraction coefficient sequence to a number.",
        carrier="An ordered sequence of integer coefficients.",
        support="Successive nested denominator positions.",
        alphabet="Integer coefficients.",
        state="A coefficient sequence {a0,a1,a2,...}.",
        input_value="A coefficient sequence.",
        law_kind="A nested addition-and-reciprocal assembly.",
        law="Assemble a0 + 1/(a1 + 1/(a2 + 1/(...))).",
        result="The number represented by the nested expression.",
        successor="One represented value for a fixed convergent coefficient sequence.",
        determinism="Deterministic for a fixed coefficient sequence.",
        termination="The source states that rational numbers have finite representations and other numbers have infinite representations.",
        witness="Successive finite convergents approach the represented value.",
        variants="Rational numbers yield finite sequences; other displayed constants yield infinite sequences.",
        excluded="Braces and line breaking are printed representations.",
        limit="The reverse extraction algorithm, convergence domain, and canonical finite terminal convention are not stated.",
        )
    },
    not_applicable=DECLARATIVE_NA,
    missing="The number-to-coefficients extraction algorithm, convergence domain, and canonical finite terminal convention are not stated.",
)
evidence(
    continued_fraction,
    "continued-fraction-introduction",
    "U000801",
    "The prose introduces continued fractions as a different representation of numbers.",
    [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "complete_state",
        "input",
        "law_kind",
        "result_kind",
        "excluded_observers_and_representations",
        "evidence_limit",
        *DECLARATIVE_NA,
    ],
    strength="DIRECT_IDENTITY",
)
context_evidence(
    continued_fraction,
    "continued-fraction-assembly-formula",
    "U000802",
    "The displayed nested addition-and-reciprocal formula defines assembly from coefficients to a represented value.",
    fields=[
        "rule_relation_constraint_function_or_probability_law",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "witness_semantics",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)
context_evidence(
    continued_fraction,
    "continued-fraction-caption",
    "U000804",
    "The caption identifies the coefficient-list notation as a continued-fraction representation.",
    fields=["object_kind", "complete_state", "input", "result_kind"],
    strength="CORROBORATING",
    modality="CAPTION",
)
context_evidence(
    continued_fraction,
    "continued-fraction-finite-infinite-scope",
    "U000805",
    "The prose states the finite-rational versus infinite-other-number distinction.",
    fields=["termination_completion_failure", "parameters_and_variants"],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    continued_fraction,
    "continued-fraction-properties",
    "U000808",
    "The table supplies properties of the displayed continued-fraction representations without an extraction algorithm.",
    fields=["parameters_and_variants", "evidence_limit"],
    strength="CORROBORATING",
    modality="TABLE",
)
context_evidence(
    continued_fraction,
    "continued-fraction-properties-caption",
    "U000809",
    "The caption delimits the table as properties of continued fractions.",
    fields=["parameters_and_variants"],
    strength="CORROBORATING",
    modality="CAPTION",
)

pi_cf = candidate(
    "pi-continued-fraction",
    "continued-fraction representation of pi",
    "U000802",
    {
        **deepcopy(continued_fraction["facts"]),
        "object_kind": "The displayed continued-fraction coefficient sequence denoting pi.",
        "input": "The displayed coefficient sequence beginning {3,7,15,1,292,...}.",
        "complete_state": "The displayed coefficient sequence beginning {3,7,15,1,292,...}.",
        "result_kind": "The represented value pi.",
        "parameters_and_variants": "The represented value is fixed at pi; only a displayed coefficient prefix is supplied.",
        "evidence_limit": "The source supplies the nested denotation and a coefficient prefix, but no procedure for generating arbitrary later coefficients.",
    },
    not_applicable=DECLARATIVE_NA,
    missing="The source supplies a coefficient prefix but no procedure for generating arbitrary later coefficients.",
)
evidence(
    pi_cf,
    "pi-continued-fraction-formula",
    "U000802",
    "The nested formula explicitly identifies pi as the value denoted by the continued fraction.",
    [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "alphabet_or_value_schema",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "witness_semantics",
        "excluded_observers_and_representations",
        "evidence_limit",
        *DECLARATIVE_NA,
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)
context_evidence(
    pi_cf,
    "pi-continued-fraction-coefficients",
    "U000803",
    "The following source line supplies the displayed coefficient prefix {3,7,15,1,292,...}.",
    fields=["complete_state", "input", "parameters_and_variants"],
    strength="DIRECT_IDENTITY",
    modality="FORMULA",
)
context_evidence(
    pi_cf,
    "pi-continued-fraction-caption",
    "U000804",
    "The caption explicitly labels the displayed coefficient sequence as the continued-fraction representation of pi.",
    fields=["object_kind", "result_kind"],
    strength="CORROBORATING",
    modality="CAPTION",
)
context_evidence(
    pi_cf,
    "pi-continued-fraction-finite-infinite-context",
    "U000805",
    "The prose distinguishes finite rational representations from the infinite representation used here.",
    fields=["termination_completion_failure", "parameters_and_variants"],
    strength="CORROBORATING",
)

symbolic_representation = source_candidate(
    "symbolic-number-representation",
    "symbolic-expression representation of numbers",
    "U000806",
    declarative_facts(
        kind="A representation of a number by a symbolic mathematical expression.",
        carrier="The displayed symbolic expression.",
        support="The printed positions of the displayed finite expression.",
        alphabet="The symbols occurring in the displayed example.",
        state="The displayed symbolic expression such as sqrt(2)+e^sqrt(3).",
        input_value="The displayed symbolic expression.",
        law_kind="A symbolic-expression denotation relation.",
        law="The displayed expression denotes a number assembled from its named constants and operations.",
        result="The denoted number.",
        successor="The source does not specify a general expression language or its branch semantics.",
        determinism="The source does not specify a general expression language or evaluator.",
        termination="No general evaluator or evaluation bound is supplied.",
        witness="No general proof or evaluation certificate is defined.",
        variants="Only the displayed examples are delimited; the expression grammar and available operations are left open.",
        excluded="Expression brevity is not the same as digit-sequence simplicity or evaluation cost.",
        limit="No formal grammar, branch convention, or evaluator is specified.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The expression grammar, operation set, branch semantics, and evaluator are not specified.",
    claim="The passage explicitly identifies symbolic expressions as number representations and distinguishes denotation from evaluation effort.",
    strength="DIRECT_PARTIAL_MECHANICS",
    uncertainties=["The representation class is deliberately open-ended in this source."],
)
mark_unknown(
    symbolic_representation,
    {
        "alphabet_or_value_schema": "The source does not define a formal expression alphabet or grammar.",
        "successor_cardinality": "The source does not define denotation for every member of a formal expression language.",
        "determinism_branching_or_measure": "No general branch convention or evaluator is specified.",
        "termination_completion_failure": "No evaluation procedure or completion bound is specified.",
        "witness_semantics": "No general evaluation certificate is defined.",
    },
)


# ---------------------------------------------------------------------------
# Immutable functions and function-derived encodings.

SINE_SUM_FACTS = declarative_facts(
    kind="A finite sum of sine functions.",
    carrier="A real argument x and finitely many sine terms.",
    support="The real line.",
    alphabet="Real-valued inputs, frequencies, and outputs.",
    state="The input x and fixed frequency coefficients.",
    input_value="A real number x.",
    law_kind="A deterministic real-valued function.",
    law="Evaluate and add the stated sine terms at x.",
    result="One real function value.",
    successor="Exactly one real output per x.",
    determinism="Deterministic.",
    termination="A finite number of sine evaluations and additions completes each value.",
    witness="Substituting x into every displayed term and summing reproduces the output.",
    variants="The number of terms and their frequency multipliers vary.",
    excluded="The plotted curve, waveform interpretation, and musical label are representations/applications.",
    limit="The source assumes the standard sine function without restating its independent definition.",
)
sine_sum_family = source_candidate(
    "sine-sum-family",
    "finite sine-sum function family",
    "U000816",
    SINE_SUM_FACTS,
    not_applicable=DECLARATIVE_NA,
    missing="The underlying standard sine function is assumed rather than defined in this section.",
    claim="The passage delimits combinations formed by adding standard sine functions.",
    strength="DIRECT_PARTIAL_MECHANICS",
)

sine_formulas = [
    ("sine-sum-3over2", "sine sum Sin[x]+Sin[(3/2)x]", "Sin[x]+Sin[(3/2)x]"),
    ("sine-sum-10over7", "sine sum Sin[x]+Sin[(10/7)x]", "Sin[x]+Sin[(10/7)x]"),
    ("sine-sum-sqrt2", "sine sum Sin[x]+Sin[sqrt(2)x]", "Sin[x]+Sin[sqrt(2)x]"),
    (
        "sine-sum-sqrt2-sqrt3",
        "three-term sine sum Sin[x]+Sin[sqrt(2)x]+Sin[sqrt(3)x]",
        "Sin[x]+Sin[sqrt(2)x]+Sin[sqrt(3)x]",
    ),
]
sine_specs: dict[str, CandidateSpec] = {}
for key, name, formula in sine_formulas:
    facts = deepcopy(SINE_SUM_FACTS)
    facts["object_kind"] = name
    facts["rule_relation_constraint_function_or_probability_law"] = f"Evaluate {formula}."
    facts["parameters_and_variants"] = f"The formula is fixed at {formula}."
    sine_specs[key] = source_candidate(
        key,
        name,
        "U000817",
        facts,
        not_applicable=DECLARATIVE_NA,
        missing="The underlying standard sine function is assumed rather than defined in this section.",
        claim=f"Original-resolution inspection directly transcribes {formula}.",
        strength="DIRECT_COMPLETE_MECHANICS",
        image_path="CHAPTERS/_page_161_Figure_1.jpeg",
    )

axis_crossing_encoder = source_candidate(
    "trig-axis-crossing-substitution-encoder",
    "two-frequency trigonometric axis-crossing substitution encoding",
    "U000819",
    declarative_facts(
        kind="An encoding of two-frequency sine/cosine axis crossings by a generalized substitution system.",
        carrier="A two-term trigonometric function, its real-axis intervals, a continued fraction, and a binary substitution pattern.",
        support="Successive real intervals and successive substitution stages.",
        alphabet="Black/white interval markers and continued-fraction coefficients.",
        state="The fixed frequency ratio alpha, current substitution word, and current continued-fraction term.",
        input_value="A function Sin[x]+Sin[alpha x] or the stated two-term sine/cosine variants.",
        law_kind="A deterministic representation coupling a continued fraction to generalized substitutions.",
        law=(
            "Compute the continued fraction of (alpha-1)/(alpha+1); use each "
            "successive coefficient to select the pictured generalized substitution rule. "
            "A black output element denotes an interval containing an axis crossing."
        ),
        result="A black/white interval sequence reproducing the function's axis-crossing pattern.",
        successor="Exactly one encoded stage for each supplied continued-fraction term under the pictured rule convention.",
        determinism="Deterministic once generalized-substitution mechanics and interval alignment are fixed.",
        termination="Finite prefixes generate finite encoded prefixes; the construction continues with the continued fraction.",
        witness="An interval is marked black exactly when the plotted function crosses the axis within it.",
        variants="The source states analogous encodings for sums/differences of exactly two sine or cosine functions.",
        excluded="The plotted waveform and vertical interval lines display the relation.",
        limit="The base generalized-substitution semantics and precise interval-origin convention are routed outside this assigned path.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The base generalized-substitution semantics and exact interval-origin convention require the routed prior construction.",
    claim="The prose states the continued-fraction control sequence and black-interval crossing semantics.",
    strength="DIRECT_PARTIAL_MECHANICS",
    route_keys=["generalized-substitution-term"],
)
context_evidence(
    axis_crossing_encoder,
    "axis-crossing-encoder-panel",
    "U000821",
    "Original-resolution inspection confirms the rule icons, continued-fraction term schedule, black interval encoding, and four worked functions.",
    image_path="CHAPTERS/_page_162_Figure_1.jpeg",
    fields=[
        "visible_history",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)

COS_DIFFERENCE_FACTS = declarative_facts(
    kind="A two-frequency cosine-difference function.",
    carrier="A real argument x and fixed frequency multiplier alpha.",
    support="The real line.",
    alphabet="Real-valued inputs and outputs.",
    state="The input x.",
    input_value="A real number x.",
    law_kind="A deterministic real-valued function.",
    law="Evaluate Cos[x]-Cos[alpha x].",
    result="One real function value.",
    successor="Exactly one value per x.",
    determinism="Deterministic.",
    termination="Two cosine evaluations and one subtraction complete each value.",
    witness="Direct substitution into the displayed formula reproduces the output.",
    variants="The multiplier alpha varies across the four displayed cases.",
    excluded="The axis-crossing grid and generalized substitution word are representations/observers.",
    limit="The standard cosine function is assumed rather than independently defined here.",
)
cos_cases = [
    ("cosdiff-1-sqrt2", "Cos[x]-Cos[(1+sqrt(2))x]", "1+sqrt(2)"),
    ("cosdiff-2-sqrt5", "Cos[x]-Cos[(2+sqrt(5))x]", "2+sqrt(5)"),
    ("cosdiff-2-cuberoot5", "Cos[x]-Cos[(2+cuberoot(5))x]", "2+cuberoot(5)"),
    ("cosdiff-1-sqrte", "Cos[x]-Cos[(1+sqrt(e))x]", "1+sqrt(e)"),
]
cos_specs: dict[str, CandidateSpec] = {}
for key, formula, alpha in cos_cases:
    facts = deepcopy(COS_DIFFERENCE_FACTS)
    facts["object_kind"] = f"The function {formula}."
    facts["rule_relation_constraint_function_or_probability_law"] = f"Evaluate {formula}."
    facts["parameters_and_variants"] = f"alpha is fixed at {alpha}."
    cos_specs[key] = source_candidate(
        key,
        formula,
        "U000821",
        facts,
        not_applicable=DECLARATIVE_NA,
        missing="The standard cosine function is assumed rather than independently defined here.",
        claim=f"Original-resolution inspection directly transcribes {formula}.",
        strength="DIRECT_COMPLETE_MECHANICS",
        image_path="CHAPTERS/_page_162_Figure_1.jpeg",
    )
cos_specs["cosdiff-2-sqrt5"]["route_keys"].append("fibonacci-substitution-page83")

zeta_function = source_candidate(
    "riemann-zeta-function",
    "Riemann zeta function",
    "U000826",
    declarative_facts(
        kind="The function Zeta[s] defined by an infinite reciprocal-power sum.",
        carrier="A scalar argument s and positive integer summation index k.",
        support="Positive integers k in the displayed infinite sum.",
        alphabet="Real or complex values.",
        state="The input s.",
        input_value="A value s in a domain where the displayed sum is used.",
        law_kind="An infinite-series-defined function.",
        law="Zeta[s] = Sum[1/k^s,{k,infinity}].",
        result="The value of the reciprocal-power series.",
        successor="One series value where the displayed series converges.",
        determinism="Deterministic.",
        termination="The denotation is an infinite sum; finite numerical evaluation requires an approximation not stated here.",
        witness="Partial sums converge to the stated value in the admitted domain.",
        variants="The source relates the function to prime distribution.",
        excluded="The plotted Riemann-Siegel curve is a related function, not Zeta's native representation.",
        limit="Analytic continuation and the complete complex domain are not specified.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="Analytic continuation, convergence domain, and evaluation method are not supplied.",
    claim="The caption explicitly defines Zeta[s] by Sum[1/k^s,{k,infinity}].",
    strength="DIRECT_PARTIAL_MECHANICS",
    modality="FORMULA",
)

riemann_siegel = source_candidate(
    "riemann-siegel-z",
    "Riemann-Siegel Z function",
    "U000826",
    declarative_facts(
        kind="The Riemann-Siegel Z function related to Zeta[1/2+i t].",
        carrier="A real argument t and a related complex zeta value.",
        support="The real t axis.",
        alphabet="Real input and the plotted real output.",
        state="The input t.",
        input_value="A real number t.",
        law_kind="A named real-valued transformation of the critical-line zeta function.",
        law="The source says the function is essentially Zeta[1/2+i t] but does not give the exact phase/normalization.",
        result="The plotted Riemann-Siegel Z value.",
        successor="The source treats it as single-valued.",
        determinism="Deterministic once the omitted exact definition is supplied.",
        termination="Evaluation mechanics are not supplied.",
        witness="The plotted curve is identified as this function.",
        variants="No variants are stated.",
        excluded="The plotted polyline is a representation.",
        limit="The word 'essentially' leaves the exact transformation, phase, and normalization unspecified.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The exact Riemann-Siegel phase/normalization and evaluation law are missing.",
    claim="The caption identifies the plotted function and its critical-line zeta relation but qualifies it as only 'essentially' that expression.",
    strength="DIRECT_IDENTITY",
    uncertainties=["The exact Riemann-Siegel Z definition is underdetermined by 'essentially'."],
)
mark_unknown(
    riemann_siegel,
    {
        "rule_relation_constraint_function_or_probability_law": "The word 'essentially' does not specify the exact Riemann-Siegel phase or normalization.",
        "successor_cardinality": "The assigned source does not state a complete function law from which output cardinality can be established.",
        "determinism_branching_or_measure": "Determinism cannot be documented without the omitted exact transformation.",
        "termination_completion_failure": "No evaluation procedure or completion/failure semantics are supplied.",
        "parameters_and_variants": "No parameterization or variant family is stated for the named plotted function.",
    },
)

riemann_hypothesis = yes_no_query(
    "riemann-hypothesis-query",
    "Riemann-Hypothesis peak-sign query as stated",
    "U000826",
    "Determine whether all peaks after the first in the displayed Riemann-Siegel Z curve lie above the axis.",
    "NO requires a violating peak; YES requires a proof covering every peak in the stated scope.",
    "The source reports that the claim has not been established.",
)


# ---------------------------------------------------------------------------
# Iterated maps and their initial conditions/observers.

ITERATED_MAP_FAMILY = number_map_facts(
    "An iterated self-map of the unit interval.",
    "real numbers between 0 and 1",
    "Apply a fixed function F:[0,1]->[0,1], updating x to F(x).",
    "An explicitly supplied initial x in [0,1].",
    "The map F and initial x vary.",
)
iterated_map_family = source_candidate(
    "iterated-map-family",
    "unit-interval iterated-map family",
    "U000828",
    ITERATED_MAP_FAMILY,
    not_applicable=EVOLUTION_NA,
    missing="A particular map and initial value must be supplied.",
    claim="The passage defines an iterated map as repeatedly applying a fixed self-map of [0,1].",
    strength="DIRECT_COMPLETE_MECHANICS",
)

map_cases = [
    ("iterated-map-a", "iterated map (a) FractionalPart[(3/2)x]", "FractionalPart[(3/2)x]"),
    ("iterated-map-b", "iterated map (b) tent map of height 3/4", "If[x<1/2,(3/2)x,(3/2)(1-x)]"),
    ("iterated-map-c", "iterated map (c) FractionalPart[(3/4)x]", "FractionalPart[(3/4)x]"),
    ("iterated-map-d", "iterated map (d) binary shift map", "FractionalPart[2x]"),
]
map_specs: dict[str, CandidateSpec] = {}
for key, name, formula in map_cases:
    facts = deepcopy(ITERATED_MAP_FAMILY)
    facts["object_kind"] = name
    facts["rule_relation_constraint_function_or_probability_law"] = f"Update x to {formula}."
    facts["parameters_and_variants"] = f"The map is fixed at x -> {formula}; seeds 1/2 and pi/4 are displayed."
    map_specs[key] = source_candidate(
        key,
        name,
        "U000835",
        facts,
        not_applicable=EVOLUTION_NA,
        missing="Exact real arithmetic is assumed; finite-precision conventions are not stated.",
        claim=f"Original-resolution inspection directly transcribes x -> {formula}.",
        strength="DIRECT_COMPLETE_MECHANICS",
        image_path="CHAPTERS/_page_165_Figure_1.jpeg",
    )
context_evidence(
    map_specs["iterated-map-d"],
    "shift-map-digit-semantics",
    "U000833",
    "The prose states that this map shifts every base-2 digit one position left at each step.",
    fields=["rule_relation_constraint_function_or_probability_law"],
    strength="DIRECT_COMPLETE_MECHANICS",
)

half_seed = source_candidate(
    "iterated-map-half-seed",
    "iterated-map initial value 1/2",
    "U000831",
    seed_facts(
        "The scalar initial-value preset x=1/2.",
        "One unit-interval scalar.",
        "A single scalar position.",
        "x=1/2",
        "Applied to all four displayed iterated maps.",
    ),
    not_applicable=SEED_NA,
    missing="No mechanics are missing for the scalar value itself.",
    claim="The passage explicitly fixes 1/2 as the first page's initial condition.",
    strength="DIRECT_IDENTITY",
)
pi_quarter_seed = source_candidate(
    "iterated-map-pi-quarter-seed",
    "iterated-map initial value pi/4",
    "U000831",
    seed_facts(
        "The scalar initial-value preset x=pi/4.",
        "One unit-interval scalar.",
        "A single scalar position.",
        "x=pi/4",
        "Applied to all four displayed iterated maps.",
    ),
    not_applicable=SEED_NA,
    missing="No mechanics are missing for the symbolic scalar value itself.",
    claim="The passage explicitly fixes pi/4 as the second page's initial condition.",
    strength="DIRECT_IDENTITY",
)

nearby_pair_seed = source_candidate(
    "shift-map-nearby-seed-pair",
    "nearby initial-condition pair for the shift map",
    "U000843",
    {
        **seed_facts(
            "A pair of scalar initial values differing by about one part in a billion billion.",
            "Two unit-interval scalar registers compared under the same map.",
            "A paired two-run experiment.",
            "The displayed decimals are 0.785398163397448310 and 0.785398163397448311.",
            "The pair is used with the binary shift map.",
        ),
        "successor_cardinality": "Exactly one ordered pair of initial values in the displayed preset.",
    },
    not_applicable=SEED_NA,
    missing="The prose gives the relative scale informally; the figure supplies the two decimal labels.",
    claim="The passage defines the close-pair experiment and the original-resolution panels supply both decimal values.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    nearby_pair_seed,
    "nearby-seed-first",
    "U000845",
    "Original-resolution inspection confirms initial condition 0.785398163397448310.",
    image_path="CHAPTERS/_page_168_Picture_1.jpeg",
    fields=["complete_state", "seed"],
    strength="DIRECT_IDENTITY",
)
context_evidence(
    nearby_pair_seed,
    "nearby-seed-second",
    "U000846",
    "Original-resolution inspection confirms initial condition 0.785398163397448311.",
    image_path="CHAPTERS/_page_168_Picture_2.jpeg",
    fields=["complete_state", "seed"],
    strength="DIRECT_IDENTITY",
)
nearby_pair_seed["evidence"][0]["fields"] = [
    field
    for field in nearby_pair_seed["evidence"][0]["fields"]
    if field not in {"complete_state", "seed"}
]
nearby_pair_seed["evidence"][0]["claim"] = (
    "The passage defines a paired shift-map experiment whose initial values "
    "differ by about one part in a billion billion."
)

trajectory_difference = source_candidate(
    "iterated-map-digit-difference",
    "iterated-map digit-sequence difference observer",
    "U000859",
    declarative_facts(
        kind="An observer showing differences between paired iterated-map digit sequences.",
        carrier="Two aligned base-2 digit histories.",
        support="Corresponding step and digit positions.",
        alphabet="Matching/differing status at each aligned position.",
        state="Two complete aligned digit histories.",
        input_value="Two trajectories produced by the same map from nearby seeds.",
        law_kind="A pointwise comparison observer.",
        law="Compare corresponding base-2 digit positions and display where the sequences differ.",
        result="A space-time pattern of digit differences.",
        successor="Exactly one comparison status per aligned position.",
        determinism="Deterministic once digit alignment and rendering are fixed.",
        termination="A finite displayed window compares finitely many positions.",
        witness="A marked position contains unequal source digits.",
        variants="Applied separately to maps (a), (b), (c), and (d).",
        excluded="Color/gray rendering of difference is not native map state.",
        limit="The exact visual code for equal versus unequal pixels is not stated in prose.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The exact visual code and finite alignment/cropping convention are not stated.",
    claim="The caption explicitly identifies the panels as differences in digit sequences from a small initial change.",
    strength="DIRECT_PARTIAL_MECHANICS",
    image_path="CHAPTERS/_page_170_Picture_2.jpeg",
)

random_interval_seed = source_candidate(
    "random-interval-seed-ensemble",
    "random unit-interval initial-condition ensemble",
    "U000853",
    {
        "object_kind": "A random seed generator constrained to a numeric size interval.",
        "native_time": "No native evolution time; one sample produces one initial scalar.",
        "carrier": "Real numbers in a stated interval.",
        "support": "A scalar unit-interval state.",
        "topology": "No spatial topology.",
        "structural_invariants": "Every sample lies in the stated size range.",
        "alphabet_or_value_schema": "Real-valued samples.",
        "complete_state": "One sampled scalar x.",
        "seed": "A random number subject only to a size-range constraint.",
        "input": "The allowed numeric interval.",
        "law_kind": "A qualitative range-constrained random-selection principle.",
        "rule_relation_constraint_function_or_probability_law": "Pick a number at random subject to lying in the specified range.",
        "result_kind": "A sampled initial scalar, overwhelmingly likely under the intended idealization to have an apparently random digit sequence.",
        "successor_cardinality": "The statement permits more than one number in the specified range.",
        "determinism_branching_or_measure": "The source calls the selection random but supplies no probability measure.",
        "termination_completion_failure": "No operational sampling or completion procedure is supplied.",
        "witness_semantics": "A valid sample lies inside the selected range.",
        "parameters_and_variants": "The source refers only to a specified size range; its endpoints and other sampling parameters are not given here.",
        "excluded_observers_and_representations": "The subsequent shift-map trajectory is not part of the seed generator.",
        "evidence_limit": "The probability measure, endpoint convention, and finite/infinite precision are not specified.",
    },
    not_applicable={
        "visible_history": "A one-shot seed ensemble has no trajectory.",
        "control_state": "No control register is defined.",
        "boundary": "No evolution boundary is part of the sampler.",
        "external_data": "No external stream is stated.",
        "frontier_or_activation": "A one-shot sampler has no update frontier.",
        "schedule": "A one-shot sampler has no iterative schedule.",
        "read_dependencies_or_neighborhood": "No local neighborhood is read.",
        "write_replacement_assembly_or_commit": "The sampled scalar is the result, not a committed trajectory update.",
    },
    missing="The probability measure, endpoint convention, and precision model are not specified.",
    claim="The passage explicitly describes random selection subject only to a size-range constraint.",
    strength="DIRECT_PARTIAL_MECHANICS",
    uncertainties=["The intended probability measure is not formalized."],
)
mark_unknown(
    random_interval_seed,
    {
        "determinism_branching_or_measure": "The source says 'at random' but gives no probability measure or sampling semantics.",
        "termination_completion_failure": "The source gives no operational sampler, completion criterion, or failure behavior.",
        "parameters_and_variants": "The assigned passage does not state interval endpoints, endpoint convention, or other sampler parameters.",
    },
)


# ---------------------------------------------------------------------------
# Continuous cellular automata.

CONTINUOUS_CA_FAMILY = iterative_facts(
    kind="A one-dimensional continuous-valued nearest-neighbor cellular automaton.",
    carrier="Cell positions carrying gray levels.",
    support="A one-dimensional line of discrete cells.",
    topology="Every cell has an immediate left and right neighbor.",
    invariants="The line support, three-cell neighborhood, and gray-level interval persist.",
    alphabet="A continuous gray level between white 0 and black 1.",
    state="The current gray level at every cell.",
    seed="An explicitly supplied gray-level configuration; the displayed runs start from one black cell on white.",
    input_value="The complete old gray-level field.",
    frontier="Every cell is active at every step.",
    schedule="All cells update in parallel from the preceding complete field.",
    read="Read the old gray levels of left neighbor, self, and right neighbor and form their average.",
    law_kind="A deterministic local average followed by a fixed scalar map.",
    law="For each cell compute the average of left, self, and right, then apply a fixed map F:[0,1]->[0,1].",
    write="Commit all mapped values simultaneously as the next gray-level field.",
    result="A successor gray-level field and, under iteration, a continuous-cellular-automaton trajectory.",
    variants="The scalar map F varies; averaging, fractional multiplication, and additive-constant maps are displayed.",
    excluded="Grayscale shading, difference pictures, and stacked histories represent or observe the state.",
    limit="The off-picture boundary condition and exact-arithmetic implementation are not stated.",
)
continuous_ca_family = source_candidate(
    "continuous-ca-family",
    "continuous-valued nearest-neighbor cellular-automaton family",
    "U000865",
    CONTINUOUS_CA_FAMILY,
    not_applicable=EVOLUTION_NA,
    missing="The off-picture boundary condition and numerical precision convention are not stated.",
    claim="The passage defines continuous gray-valued cells and the average-neighborhood-then-map update.",
    strength="DIRECT_COMPLETE_MECHANICS",
    route_keys=["totalistic-prior-chapter"],
)
continuous_ca_family["evidence"][0]["fields"] = [
    "object_kind",
    "native_time",
    "alphabet_or_value_schema",
    "law_kind",
    "parameters_and_variants",
    "excluded_observers_and_representations",
    *EVOLUTION_NA,
]
continuous_ca_family["evidence"][0]["strength"] = "DIRECT_IDENTITY"
continuous_ca_family["evidence"][0]["claim"] = (
    "The passage introduces continuous-gray cellular automata and says their "
    "rules combine totalistic cellular automata with the preceding iterated maps."
)
context_evidence(
    continuous_ca_family,
    "continuous-ca-family-mechanics",
    "U000866",
    "The next paragraph states the three-cell average, fixed scalar mapping, parallel next-step interpretation, and single-black-cell example.",
    fields=[
        "carrier",
        "support",
        "topology",
        "structural_invariants",
        "complete_state",
        "visible_history",
        "seed",
        "input",
        "boundary",
        "frontier_or_activation",
        "schedule",
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "write_replacement_assembly_or_commit",
        "result_kind",
        "successor_cardinality",
        "determinism_branching_or_measure",
        "termination_completion_failure",
        "witness_semantics",
        "evidence_limit",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    continuous_ca_family,
    "continuous-ca-family-native-panel",
    "U000867",
    "The original-resolution panel shows the stated one-black-cell history under the average-neighborhood rule.",
    image_path="CHAPTERS/_page_171_Picture_5.jpeg",
    fields=["visible_history", "seed", "result_kind"],
    strength="CORROBORATING",
)

continuous_single_black = source_candidate(
    "continuous-ca-single-black-seed",
    "single-black-cell continuous-CA seed",
    "U000866",
    seed_facts(
        "One cell at gray level 1 on an otherwise level-0 line.",
        "Continuous-valued cell positions.",
        "A one-dimensional cell line.",
        "One black/1 cell and white/0 elsewhere.",
        "Used by the displayed continuous-cellular-automaton rules.",
    ),
    not_applicable=SEED_NA,
    missing="The origin coordinate and finite-display boundary convention are not stated.",
    claim="The passage explicitly states that the run starts from a single black cell.",
    strength="DIRECT_IDENTITY",
)


def continuous_ca_rule_facts(name: str, map_law: str, variants: str) -> dict[str, str]:
    facts = deepcopy(CONTINUOUS_CA_FAMILY)
    facts["object_kind"] = name
    facts["rule_relation_constraint_function_or_probability_law"] = (
        "Let a=(left+self+right)/3; " + map_law
    )
    facts["parameters_and_variants"] = variants
    return facts


average_ca = source_candidate(
    "continuous-ca-average",
    "continuous CA with pure neighborhood averaging",
    "U000866",
    continuous_ca_rule_facts(
        "The continuous cellular automaton whose next value is the local average.",
        "set the new cell value to a.",
        "The scalar map is F(a)=a; the displayed seed is one black cell.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="The off-picture boundary condition and numerical precision convention are not stated.",
    claim="The prose directly defines each next gray level as the average of self and immediate neighbors.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    average_ca,
    "continuous-average-native-panel",
    "U000867",
    "The original-resolution panel shows the average rule's trajectory from one black cell.",
    image_path="CHAPTERS/_page_171_Picture_5.jpeg",
    fields=["visible_history", "seed", "result_kind"],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    average_ca,
    "continuous-average-table",
    "U000868",
    "The table gives exact early rows and corroborates simultaneous three-cell averaging.",
    fields=["visible_history", "rule_relation_constraint_function_or_probability_law"],
    strength="CORROBORATING",
    modality="TABLE",
)

fractional_three_half_ca = source_candidate(
    "continuous-ca-frac-three-halves",
    "continuous CA with fractional 3/2-scaled local average",
    "U000870",
    continuous_ca_rule_facts(
        "The continuous cellular automaton using FractionalPart[(3/2)a].",
        "set the new cell value to FractionalPart[(3/2)a].",
        "The multiplier is fixed at 3/2; the displayed seed is one black cell.",
    ),
    not_applicable=EVOLUTION_NA,
    missing="The off-picture boundary condition and numerical precision convention are not stated.",
    claim="The passage directly says to multiply the local average by 3/2 and retain only its fractional part.",
    strength="DIRECT_COMPLETE_MECHANICS",
    route_keys=["iterated-map-a-page150"],
)
fractional_three_half_ca["evidence"][0]["fields"] = [
    field
    for field in fractional_three_half_ca["evidence"][0]["fields"]
    if field
    not in {
        "object_kind",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
    }
]
fractional_three_half_ca["evidence"][0]["strength"] = "DIRECT_PARTIAL_MECHANICS"
context_evidence(
    fractional_three_half_ca,
    "continuous-three-half-native-panel",
    "U000871",
    "The original-resolution panel shows the fractional three-halves rule's trajectory from one black cell.",
    image_path="CHAPTERS/_page_172_Picture_1.jpeg",
    fields=["visible_history", "seed", "result_kind"],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    fractional_three_half_ca,
    "continuous-three-half-table",
    "U000872",
    "The table gives the first six rows under the stated rule.",
    fields=["visible_history"],
    strength="CORROBORATING",
    modality="TABLE",
)
context_evidence(
    fractional_three_half_ca,
    "continuous-three-half-caption",
    "U000873",
    "The caption states the exact rule FractionalPart[(3/2) average], the one-black-cell seed, and its relation to iterated map (a).",
    fields=[
        "object_kind",
        "rule_relation_constraint_function_or_probability_law",
        "parameters_and_variants",
        "seed",
        "read_dependencies_or_neighborhood",
        "result_kind",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CAPTION",
)

ADDITIVE_CONTINUOUS_CA = continuous_ca_rule_facts(
    "The additive-constant continuous cellular-automaton family.",
    "for a fixed c, set the new cell value to FractionalPart[a+c].",
    "The additive constant c varies; the surveys display 24 unique values.",
)
additive_ca_family = source_candidate(
    "continuous-ca-additive-family",
    "additive-constant continuous-CA family",
    "U000875",
    ADDITIVE_CONTINUOUS_CA,
    not_applicable=EVOLUTION_NA,
    missing="The off-picture boundary condition and numerical precision convention are not stated.",
    claim="The passage directly defines adding a fixed constant to the local average and taking the fractional part.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
additive_ca_family["evidence"][0]["fields"] = [
    field
    for field in additive_ca_family["evidence"][0]["fields"]
    if field != "parameters_and_variants"
]
context_evidence(
    additive_ca_family,
    "additive-ca-quarter-formula",
    "U000879",
    "The displayed formula prints FractionalPart[x+1/4] for the scalar postprocessing map.",
    fields=["rule_relation_constraint_function_or_probability_law"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)
context_evidence(
    additive_ca_family,
    "additive-ca-quarter-caption",
    "U000880",
    "The caption restates adding 1/4 to the three-cell average and taking the fractional part.",
    fields=[
        "read_dependencies_or_neighborhood",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CAPTION",
)
context_evidence(
    additive_ca_family,
    "additive-ca-family-variation",
    "U000883",
    "The caption identifies one shared rule family whose added constant varies across the displayed runs.",
    fields=["parameters_and_variants"],
    strength="DIRECT_IDENTITY",
    modality="CAPTION",
)
context_evidence(
    additive_ca_family,
    "additive-ca-quarter-native-panel",
    "U000878",
    "The original-resolution panel shows the c=1/4 cellular-automaton trajectory.",
    image_path="CHAPTERS/_page_173_Picture_4.jpeg",
    fields=["visible_history"],
    strength="CORROBORATING",
)
context_evidence(
    additive_ca_family,
    "additive-ca-survey-one-control",
    "U000884",
    "The first survey controls the additive constant while retaining the shared rule family.",
    image_path="CHAPTERS/_page_174_Picture_2.jpeg",
    fields=["parameters_and_variants"],
    strength="CORROBORATING",
)
context_evidence(
    additive_ca_family,
    "additive-ca-survey-two-control",
    "U000885",
    "The second survey continues control of the additive constant and includes longer histories.",
    image_path="CHAPTERS/_page_175_Figure_2.jpeg",
    fields=["parameters_and_variants", "visible_history"],
    strength="CORROBORATING",
)

SURVEY_ONE = "CHAPTERS/_page_174_Picture_2.jpeg"
SURVEY_TWO = "CHAPTERS/_page_175_Figure_2.jpeg"
first_constants = [
    "0",
    "0.025",
    "0.05",
    "0.075",
    "0.1",
    "0.125",
    "0.15",
    "0.175",
    "0.2",
    "0.225",
    "0.25",
    "0.275",
    "0.3",
    "0.325",
    "0.35",
    "0.375",
    "0.4",
    "0.425",
    "0.45",
    "0.475",
    "0.5",
]
second_only_constants = ["0.3299", "0.495", "0.9"]
second_repeat_constants = {"0.1", "0.3", "0.325", "0.35", "0.475"}


def constant_key(value: str) -> str:
    return value.replace(".", "p")


additive_presets: dict[str, CandidateSpec] = {}
for c in [*first_constants, *second_only_constants]:
    facts = deepcopy(ADDITIVE_CONTINUOUS_CA)
    facts["object_kind"] = (
        f"The c={c} preset of the additive-constant continuous cellular-automaton family."
    )
    facts["rule_relation_constraint_function_or_probability_law"] = (
        f"Let a=(left+self+right)/3; set the new value to FractionalPart[a+{c}]."
    )
    facts["parameters_and_variants"] = (
        f"The additive constant is fixed at c={c}; the displayed seed is one black cell."
    )
    if c == "0":
        facts["rule_relation_constraint_function_or_probability_law"] = (
            "Let a=(left+self+right)/3; set the new value to "
            "FractionalPart[a+0]. In particular, input a=1 maps to 0, unlike "
            "the pure-average rule, which leaves 1 unchanged."
        )
        facts["evidence_limit"] = (
            "The c=0 preset is the fractional-part map, not the pure-average "
            "rule: their endpoint behavior differs at a=1. The off-picture "
            "boundary and numerical precision convention are unstated."
        )
    key = f"continuous-ca-add-{constant_key(c)}"
    if c == "0.25":
        spec = source_candidate(
            key,
            "additive continuous-CA preset c=0.25",
            "U000875",
            facts,
            not_applicable=EVOLUTION_NA,
            missing="The off-picture boundary condition and numerical precision convention are not stated.",
            claim="The prose directly fixes c=1/4 in the additive fractional-part rule.",
            strength="DIRECT_COMPLETE_MECHANICS",
        )
        context_evidence(
            spec,
            f"{key}-formula",
            "U000879",
            "The displayed formula prints FractionalPart[x+1/4].",
            fields=["rule_relation_constraint_function_or_probability_law"],
            strength="DIRECT_COMPLETE_MECHANICS",
            modality="FORMULA",
        )
        context_evidence(
            spec,
            f"{key}-caption",
            "U000880",
            "The caption identifies the cellular-automaton preset, c=1/4 mechanics, and complex trajectory.",
            fields=[
                "object_kind",
                "rule_relation_constraint_function_or_probability_law",
                "parameters_and_variants",
                "visible_history",
            ],
            strength="DIRECT_COMPLETE_MECHANICS",
            modality="CAPTION",
        )
        context_evidence(
            spec,
            f"{key}-native-panel",
            "U000878",
            "The original-resolution native panel shows the c=1/4 trajectory.",
            image_path="CHAPTERS/_page_173_Picture_4.jpeg",
            fields=["visible_history", "parameters_and_variants"],
            strength="DIRECT_PARTIAL_MECHANICS",
        )
        context_evidence(
            spec,
            f"{key}-survey-one",
            "U000884",
            "Original-resolution inspection confirms the c=0.25 trajectory in the family survey.",
            image_path=SURVEY_ONE,
            fields=["parameters_and_variants", "visible_history"],
            strength="DIRECT_IDENTITY",
        )
    else:
        spec = candidate(
            key,
            f"additive continuous-CA preset c={c}",
            "U000875",
            facts,
            not_applicable=EVOLUTION_NA,
            missing="The off-picture boundary condition and numerical precision convention are not stated.",
        )
        evidence(
            spec,
            f"{key}-family-anchor",
            "U000875",
            (
                "The c=1/4 example establishes the shared three-cell-average, "
                "add-constant, fractional-part law later varied by preset."
            ),
            [
                field
                for field in [*facts, *EVOLUTION_NA]
                if field
                not in {
                    "object_kind",
                    "visible_history",
                    "parameters_and_variants",
                }
            ],
            strength="DIRECT_COMPLETE_MECHANICS",
        )
        context_evidence(
            spec,
            f"{key}-family-variation",
            "U000883",
            "The caption delimits the displayed runs as presets of one shared rule family with different constants.",
            fields=["object_kind", "parameters_and_variants"],
            strength="DIRECT_IDENTITY",
            modality="CAPTION",
        )
        panel = SURVEY_ONE if c in first_constants else SURVEY_TWO
        panel_unit = "U000884" if c in first_constants else "U000885"
        evidence(
            spec,
            f"{key}-panel",
            panel_unit,
            (
                f"Original-resolution inspection identifies c={c} as one "
                "control-labelled preset and shows its output history."
            ),
            ["object_kind", "parameters_and_variants", "visible_history"],
            strength="DIRECT_IDENTITY",
            modality="IMAGE",
            image_path=panel,
        )
    if c in second_repeat_constants:
        context_evidence(
            spec,
            f"{key}-survey-two",
            "U000885",
            f"The longer original-resolution survey independently identifies the c={c} preset.",
            image_path=SURVEY_TWO,
            fields=["parameters_and_variants", "visible_history"],
            strength="CORROBORATING",
        )
    additive_presets[c] = spec

neighbor_difference = source_candidate(
    "continuous-ca-neighbor-difference",
    "continuous-CA adjacent-cell difference observer",
    "U000886",
    declarative_facts(
        kind="An observer that replaces each displayed cell by its gray-level difference from an immediate neighbor.",
        carrier="A one-dimensional gray-level field.",
        support="Adjacent cell pairs.",
        alphabet="Real-valued gray-level differences.",
        state="A complete gray-level configuration.",
        input_value="The gray level at each cell and one immediate neighbor.",
        law_kind="A deterministic nearest-neighbor difference observer.",
        law="For each cell, compute the difference between its gray level and that of its immediate neighbor.",
        result="A one-dimensional field of adjacent differences.",
        successor="Exactly one difference per chosen adjacent pair.",
        determinism="Deterministic once left-versus-right orientation and display scaling are fixed.",
        termination="A finite displayed row is transformed in one pass.",
        witness="Adding the neighbor value to an oriented difference recovers the source value.",
        variants="The middle c=0.3299 panel is shown through this observer.",
        excluded="Gray rescaling of positive/negative differences is a rendering convention.",
        limit="The caption does not specify left-versus-right orientation or value-to-gray scaling.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="Left-versus-right orientation and gray rendering of signed differences are not specified.",
    claim="The caption explicitly says the middle picture shows the difference between each cell and its immediate neighbor.",
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    neighbor_difference,
    "continuous-difference-panel",
    "U000885",
    "Original-resolution inspection confirms the panel labelled 0.3299 (differences).",
    image_path=SURVEY_TWO,
    fields=["parameters_and_variants"],
    strength="DIRECT_IDENTITY",
)


# ---------------------------------------------------------------------------
# Partial differential equations, initial data, symbolic sampling, and solver.

PDE_FAMILY = {
    "object_kind": "A family of continuous space-time field relations specified by partial differential equations.",
    "native_time": "Continuous time.",
    "carrier": "A field u[t,x] with continuous time t and continuous position x.",
    "support": "A continuous one-dimensional spatial domain across continuous time.",
    "topology": "Spatial derivatives relate field values through infinitesimal positional change.",
    "structural_invariants": "The stated differential formula is the relation to be satisfied throughout its intended domain.",
    "alphabet_or_value_schema": "Real-valued field values and their time/space derivatives.",
    "input": "A candidate field and the field values or derivatives named in a particular equation.",
    "read_dependencies_or_neighborhood": "The local field value and spatial-change rates named by a particular equation.",
    "law_kind": "A partial differential relation.",
    "rule_relation_constraint_function_or_probability_law": "Specify the rate of time change by a formula involving the field and its spatial change rates.",
    "result_kind": "A field relation whose satisfying fields are possible solutions once suitable data and semantics are supplied.",
    "termination_completion_failure": "For many randomly chosen PDEs, infinite values or infinitely rapid variation can make the original equation cease to determine future behavior.",
    "witness_semantics": "A candidate solution must satisfy the stated differential relation.",
    "parameters_and_variants": "The symbolic differential formula and its component choices vary.",
    "excluded_observers_and_representations": "Gray plots, mesh surfaces, and numerical approximations represent candidate solutions.",
    "evidence_limit": "The family discussion does not state a general solution class, boundary conditions, well-posedness criterion, or numerical solver.",
}
PDE_RELATION_NA = {
    "control_state": "No independent discrete control register is part of the stated field relation.",
    "external_data": "No external stream is part of the stated field relation.",
    "frontier_or_activation": "A continuous differential relation has no stated discrete firing frontier.",
    "schedule": "A continuous differential relation has no stated discrete update schedule.",
    "write_replacement_assembly_or_commit": "The source states a continuous relation, not a discrete write/commit operation.",
}
pde_family = candidate(
    "pde-family",
    "partial-differential-equation evolution relation",
    "U000891",
    PDE_FAMILY,
    not_applicable=PDE_RELATION_NA,
    missing="Spatial boundary conditions, solution regularity class, and numerical realization are not specified.",
    unknown_reasons={
        "complete_state": "The family passage does not specify what data constitute a complete state for arbitrary PDE order.",
        "visible_history": "Solution pictures occur later, but the family relation does not define a native history representation.",
        "seed": "No general initial-data schema is stated for the family; the displayed Gaussian data are a separate candidate.",
        "boundary": "Spatial boundary or asymptotic conditions are not stated.",
        "successor_cardinality": "No general existence or uniqueness claim is supplied.",
        "determinism_branching_or_measure": "No general well-posedness or uniqueness semantics are supplied.",
    },
)
evidence(
    pde_family,
    "pde-family-definition",
    "U000891",
    "The passage defines PDE rules as formulas for continuous time-change rates depending on field values and spatial change rates.",
    [
        "object_kind",
        "native_time",
        "carrier",
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "input",
        "read_dependencies_or_neighborhood",
        "law_kind",
        "rule_relation_constraint_function_or_probability_law",
        "result_kind",
        "witness_semantics",
        "excluded_observers_and_representations",
        "evidence_limit",
        *PDE_RELATION_NA,
    ],
    strength="DIRECT_PARTIAL_MECHANICS",
)
context_evidence(
    pde_family,
    "pde-derivative-notation",
    "U000912",
    "The caption defines the displayed time and space derivative notation and identifies u as gray level.",
    fields=[
        "carrier",
        "support",
        "topology",
        "alphabet_or_value_schema",
        "read_dependencies_or_neighborhood",
    ],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="CAPTION",
)
context_evidence(
    pde_family,
    "pde-family-general-failure",
    "U000915",
    "The prose states only a family-level failure mode: many sampled PDEs cease determining future behavior after blow-up or infinitely rapid variation.",
    fields=["termination_completion_failure", "evidence_limit"],
    strength="DIRECT_PARTIAL_MECHANICS",
)


def pde_candidate(
    key: str,
    name: str,
    anchor: str,
    equation: str,
    time_order: str,
    *,
    route_keys: list[str] | None = None,
) -> CandidateSpec:
    time_derivative = (
        "second time derivative" if time_order == "second" else "first time derivative"
    )
    facts = {
        "object_kind": f"{name}, stated as a partial differential relation.",
        "native_time": "Continuous time t as represented by the displayed time derivative.",
        "carrier": "A scalar field u[t,x].",
        "support": "Continuous time t and one spatial coordinate x.",
        "topology": "The equation uses the second spatial derivative u_xx.",
        "alphabet_or_value_schema": "Field values and their displayed derivatives.",
        "input": f"A candidate field u[t,x] with the displayed {time_derivative} and spatial derivatives.",
        "read_dependencies_or_neighborhood": "The field terms and derivatives explicitly printed in the equation.",
        "law_kind": "A stated partial differential relation, not a numerical solver.",
        "rule_relation_constraint_function_or_probability_law": equation,
        "result_kind": "Fields satisfying the displayed equation once adequate data and solution semantics are supplied.",
        "witness_semantics": "A candidate field witnesses the relation by satisfying the displayed derivative equality.",
        "parameters_and_variants": f"This candidate records exactly the displayed equation {equation}",
        "excluded_observers_and_representations": "The adjacent gray plot and mesh are representations of a computed solution, not the equation or solver.",
        "evidence_limit": "The formula does not state boundary/asymptotic data, a solution class, existence or uniqueness, or a numerical method.",
    }
    spec = candidate(
        key,
        name,
        anchor,
        facts,
        not_applicable=PDE_RELATION_NA,
        missing="Spatial boundary/asymptotic conditions and the numerical solution method are not stated.",
        route_keys=route_keys,
        unknown_reasons={
            "structural_invariants": "The displayed formula does not state an invariant or solution regularity class.",
            "complete_state": "The displayed formula alone does not state the complete initial/boundary data required for this equation.",
            "visible_history": "The equation does not define a native visualization or stored history.",
            "seed": "The formula does not itself state initial data; the displayed Gaussian data are a separate candidate.",
            "boundary": "No spatial boundary or asymptotic conditions are stated.",
            "successor_cardinality": "The source does not establish existence or uniqueness of solutions for the stated data.",
            "determinism_branching_or_measure": "The source does not provide well-posedness or uniqueness semantics.",
            "termination_completion_failure": "No equation-specific completion or failure semantics are stated; the later failure discussion applies only to the sampled PDE family in general.",
        },
    )
    evidence(
        spec,
        f"{key}-formula",
        anchor,
        f"The source explicitly prints the equation {equation}",
        [*facts, *PDE_RELATION_NA],
        strength="DIRECT_PARTIAL_MECHANICS",
        modality="FORMULA",
    )
    return spec


diffusion_pde = pde_candidate(
    "diffusion-pde",
    "diffusion equation",
    "U000905",
    "partial_t u[t,x] = (1/4) partial_xx u[t,x].",
    "first",
    route_keys=["continuous-average-page156"],
)
wave_pde = pde_candidate(
    "wave-pde",
    "wave equation",
    "U000908",
    "partial_tt u[t,x] = partial_xx u[t,x].",
    "second",
)
sine_gordon_pde = pde_candidate(
    "sine-gordon-pde",
    "sine-Gordon soliton equation",
    "U000911",
    "partial_tt u[t,x] = partial_xx u[t,x] + Sin[u[t,x]].",
    "second",
)
nonlinear_pdes: dict[int, CandidateSpec] = {}
for coefficient, anchor in [(1, "U000922"), (2, "U000925"), (4, "U000928")]:
    nonlinear_pdes[coefficient] = pde_candidate(
        f"nonlinear-pde-{coefficient}",
        f"nonlinear wave PDE with coefficient {coefficient}",
        anchor,
        (
            "partial_tt u[t,x] = partial_xx u[t,x] + "
            f"(1-u[t,x]^2)(1+{'' if coefficient == 1 else str(coefficient)}u[t,x])."
        ),
        "second",
    )

gaussian_pde_seed = source_candidate(
    "gaussian-pde-initial-data",
    "Gaussian stationary initial data for the PDE figures",
    "U000912",
    seed_facts(
        "Initial data u[0,x]=e^(-x^2) and partial_t u[0,x]=0.",
        "A continuous scalar field and its initial time derivative.",
        "A continuous one-dimensional spatial domain.",
        "u=e^(-x^2), partial_t u=0 at the initial time.",
        "Used for the PDE figures on this and following pages.",
    ),
    not_applicable={
        **SEED_NA,
        "boundary": "Spatial boundary/asymptotic conditions belong to the PDE problem and are not included in the stated initial data.",
    },
    missing="The spatial domain and boundary/asymptotic conditions are not stated.",
    claim="The caption explicitly states u=e^(-x^2), partial_t u=0 as the initial conditions.",
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="FORMULA",
)

pde_sampler = source_candidate(
    "symbolic-pde-sampler",
    "symbolic-expression sampler for PDE formulas",
    "U000914",
    declarative_facts(
        kind="A scheme for sampling PDEs by representing formulas as symbolic expressions over discrete component sets.",
        carrier="Symbolic mathematical expressions.",
        support="The source does not delimit expression size or structure.",
        alphabet="Discrete sets of possible expression components, whose vocabulary is not listed.",
        state="The source does not define an operational sampler state.",
        input_value="The source does not state a concrete component vocabulary or generation procedure.",
        law_kind="A qualitative symbolic-formula sampling principle.",
        law="Represent possible PDE formulas as symbolic expressions built from discrete sets of possible components.",
        result="A sampled candidate PDE formula.",
        successor="The source does not specify an enumeration or probability law over expressions.",
        determinism="No enumeration or probability measure is specified.",
        termination="No expression-size control or stopping law is supplied.",
        witness="No formal grammar is supplied against which a sampled expression could be checked.",
        variants="The component vocabulary, expression size, and sampling distribution are not stated.",
        excluded="Subsequent solution behavior is not part of formula sampling.",
        limit="The grammar, component set, size control, and sampling distribution are omitted.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The expression grammar, component vocabulary, size bound, and sampling/enumeration law are not stated.",
    claim="The passage explicitly proposes symbolic expressions with discrete possible components as a PDE sampling scheme.",
    strength="DIRECT_PARTIAL_MECHANICS",
    uncertainties=["The source gives only the sampling principle, not a reproducible sampler."],
)
mark_unknown(
    pde_sampler,
    {
        "support": "The source does not delimit expression size or syntactic structure.",
        "complete_state": "No operational sampler state is specified.",
        "input": "No concrete component vocabulary or generator input schema is supplied.",
        "successor_cardinality": "No enumeration or measure over possible expressions is specified.",
        "determinism_branching_or_measure": "No enumeration order or probability measure is specified.",
        "termination_completion_failure": "No size control, stopping law, completion condition, or failure behavior is supplied.",
        "witness_semantics": "Without a formal grammar or component list, no exact membership witness is defined.",
        "parameters_and_variants": "The grammar, vocabulary, size controls, and sampling parameters are all omitted.",
    },
)

pde_numerical_scheme = source_candidate(
    "pde-numerical-scheme",
    "unspecified numerical approximation scheme for the PDE figures",
    "U000936",
    {
        "object_kind": "The numerical approximation procedure used to compute the displayed PDE solution.",
        "input": "One PDE and its initial data.",
        "law_kind": "An unnamed numerical approximation algorithm.",
        "result_kind": "The computed approximate field shown in the figures.",
        "excluded_observers_and_representations": "The grayscale solution panel is the solver output representation.",
        "evidence_limit": "Only the existence and visible consequence of a numerical approximation scheme are stated; all mechanics and validation criteria are absent.",
    },
    not_applicable={},
    missing=(
        "The stencil, grid, space/time step sizes, integrator, precision, "
        "boundary treatment, stability condition, and convergence/error checks are all missing."
    ),
    claim="The caption explicitly identifies a numerical approximation scheme as affecting computed details, but supplies none of its mechanics.",
    strength="DIRECT_IDENTITY",
    uncertainties=["The unnamed solver is construction-bearing but cannot be reproduced from the assigned source."],
    unknown_reasons={
        field: (
            "The source identifies an unspecified numerical approximation "
            f"scheme but does not state {field.replace('_', ' ')}."
        )
        for field in FINGERPRINT_FIELDS
        if field
        not in {
            "object_kind",
            "input",
            "law_kind",
            "result_kind",
            "excluded_observers_and_representations",
            "evidence_limit",
        }
    },
)
context_evidence(
    pde_numerical_scheme,
    "pde-solver-sensitive-panel",
    "U000934",
    "The final original-resolution solution panel is the one whose details the caption says are sensitive to the numerical approximation scheme.",
    image_path="CHAPTERS/_page_181_Picture_6.jpeg",
    fields=["result_kind", "excluded_observers_and_representations", "evidence_limit"],
    strength="CORROBORATING",
)


# Literal construction-bearing routes discovered during the sequential pass.
add_route(
    "register-page100",
    "U000693",
    "the register machine shown on page 100",
    "register-machine realization and state encoding for the printed arithmetic map",
    ["register machine", "page 100", "3n/2", "(3n+1)/2"],
)
add_route(
    "substitution-page83",
    "U000792",
    "the substitution systems on page 83",
    "substitution-system construction of nested digit sequences",
    ["substitution systems", "page 83", "nested digit sequence"],
)
add_route(
    "generalized-substitution-term",
    "U000819",
    "a generalized substitution system",
    "base mechanics of generalized substitution systems used by the axis-crossing encoding",
    ["generalized substitution system", "continued fraction", "axis crossing"],
    kind="OTHER",
)
add_route(
    "fibonacci-substitution-page83",
    "U000822",
    "the Fibonacci substitution system on page 83",
    "Fibonacci substitution-system mechanics and the analogous axis-crossing preset",
    ["Fibonacci substitution system", "page 83", "quadratic irrational"],
)
add_route(
    "shift-map-prev-pages",
    "U000833",
    "the so-called shift map used in case (d) on the previous two pages",
    "iterated-map case (d) formula and trajectories",
    ["shift map", "case (d)", "previous two pages"],
    scope="WITHIN_STAGE",
)
add_route(
    "shift-map-pages150-151",
    "U000850",
    "the shift map—shown as case (d) on pages 150 and 151",
    "shift-map formula and simple/random initial-condition runs",
    ["shift map", "case (d)", "pages 150 and 151"],
    scope="WITHIN_STAGE",
)
add_route(
    "intrinsic-maps-pages150-151",
    "U000857",
    "systems like (a) and (b) on pages 150 and 151",
    "iterated-map cases (a) and (b) from simple initial conditions",
    ["systems (a) and (b)", "pages 150 and 151", "simple initial conditions"],
    scope="WITHIN_STAGE",
)
add_route(
    "totalistic-prior-chapter",
    "U000865",
    "the totalistic cellular automaton rules that we discussed at the beginning of the last chapter",
    "discrete totalistic cellular-automaton base mechanics",
    ["totalistic cellular automaton", "last chapter", "average"],
    kind="SECTION",
)
add_route(
    "iterated-map-a-page150",
    "U000873",
    "exactly iterated map (a) from page 150",
    "unit-interval iterated map x -> FractionalPart[(3/2)x]",
    ["iterated map (a)", "page 150", "FractionalPart", "3/2"],
    scope="WITHIN_STAGE",
)
add_route(
    "continuous-average-page156",
    "U000897",
    "the continuous cellular automaton on page 156",
    "pure-average continuous cellular automaton and its diffusion limit",
    ["continuous cellular automaton", "page 156", "diffusion"],
    scope="WITHIN_STAGE",
)
add_route(
    "continuous-rules-previous-page",
    "U000886",
    "the same kind of rules as on the previous page",
    "additive-constant continuous-CA family and parameter presets",
    ["same kind of rules", "previous page", "continuous cellular automata"],
    scope="WITHIN_STAGE",
    kind="SECTION",
)
add_route(
    "nonlinear-pdes-previous-page",
    "U000936",
    "the same equations as on the previous page",
    "three nonlinear PDE formulas and their shorter-time solutions",
    ["same equations", "previous page", "partial differential equations"],
    scope="WITHIN_STAGE",
)

# Candidate-to-family and candidate-to-route provenance.
map_specs["iterated-map-d"]["anchor"] = "U000833"
diffusion_pde["anchor"] = "U000897"
zeta_function["anchor"] = "U000823"
context_evidence(
    zeta_function,
    "zeta-introduction",
    "U000823",
    "The passage first identifies the zeta function as the construction behind the following plotted example.",
    strength="DIRECT_IDENTITY",
)
riemann_hypothesis["anchor"] = "U000824"
context_evidence(
    riemann_hypothesis,
    "riemann-hypothesis-introduction",
    "U000824",
    "The passage first isolates the Riemann Hypothesis as the peak/valley sign proposition.",
    strength="DIRECT_IDENTITY",
)
for _spec in additive_presets.values():
    _spec["related_keys"] = ["continuous-ca-additive-family"]
for _spec in radix_presets.values():
    _spec["related_keys"] = ["radix-family"]
for _spec in addition_presets.values():
    _spec["related_keys"] = ["constant-addition-family"]
for _spec in [times_two, times_three, times_three_halves]:
    _spec["related_keys"] = ["constant-multiplication-family"]
for _spec in fixed_specs.values():
    _spec["related_keys"] = ["recursive-sequence-schema"]
for _spec in variable_specs.values():
    _spec["related_keys"] = ["recursive-sequence-schema"]
for _spec in map_specs.values():
    _spec["related_keys"] = ["iterated-map-family"]
for _spec in [average_ca, fractional_three_half_ca, additive_ca_family]:
    _spec["related_keys"] = ["continuous-ca-family"]
for _spec in [diffusion_pde, wave_pde, sine_gordon_pde, *nonlinear_pdes.values()]:
    _spec["related_keys"] = ["pde-family"]
for _spec in cos_specs.values():
    _spec["related_keys"] = ["trig-axis-crossing-substitution-encoder"]

map_specs["iterated-map-d"]["route_keys"].extend(
    ["shift-map-prev-pages", "shift-map-pages150-151"]
)
map_specs["iterated-map-a"]["route_keys"].append("intrinsic-maps-pages150-151")
map_specs["iterated-map-b"]["route_keys"].append("intrinsic-maps-pages150-151")
additive_ca_family["route_keys"].append("continuous-rules-previous-page")
for _spec in nonlinear_pdes.values():
    _spec["route_keys"].append("nonlinear-pdes-previous-page")

for _spec, _label, _unit in [
    (register_arithmetic_map, "register-page100-route", "U000693"),
    (axis_crossing_encoder, "generalized-substitution-route", "U000819"),
    (cos_specs["cosdiff-2-sqrt5"], "fibonacci-substitution-route", "U000822"),
    (map_specs["iterated-map-d"], "shift-map-route-a", "U000833"),
    (map_specs["iterated-map-d"], "shift-map-route-b", "U000850"),
    (map_specs["iterated-map-a"], "intrinsic-map-a-route", "U000857"),
    (map_specs["iterated-map-b"], "intrinsic-map-b-route", "U000857"),
    (continuous_ca_family, "totalistic-prior-route", "U000865"),
    (fractional_three_half_ca, "iterated-map-a-route", "U000873"),
    (diffusion_pde, "continuous-average-route", "U000897"),
    (additive_ca_family, "continuous-rules-route", "U000886"),
    (nonlinear_pdes[1], "nonlinear-pde-route-1", "U000936"),
    (nonlinear_pdes[2], "nonlinear-pde-route-2", "U000936"),
    (nonlinear_pdes[4], "nonlinear-pde-route-4", "U000936"),
]:
    context_evidence(
        _spec,
        _label,
        _unit,
        "This unit supplies the literal construction-bearing route attached to the candidate.",
        strength="LEAD_ONLY",
        modality="CROSS_REFERENCE",
    )


UNKNOWN_LABELS = {
    field: field.replace("_", " ") for field in FINGERPRINT_FIELDS
}


def unknown_reason(spec: CandidateSpec, field: str) -> str:
    if field in spec["unknown_reasons"]:
        return spec["unknown_reasons"][field]
    return (
        f"The assigned Chapter 4 main-text evidence for {spec['name']} does "
        f"not state {UNKNOWN_LABELS[field]} beyond the recorded facts and routes."
    )


def allocate(
    reading_input: list[dict[str, str]],
    asset_input: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, list[str]],
]:
    unit_order = {
        row["source_unit_id"]: index
        for index, row in enumerate(reading_input, 1)
    }
    image_order = {
        row["physical_path"]: len(reading_input) + index
        for index, row in enumerate(asset_input, 1)
    }
    asset_by_path = {row["physical_path"]: row for row in asset_input}

    def anchor_details(anchor: str) -> tuple[str, int]:
        if anchor in unit_order:
            return "SOURCE_UNIT", unit_order[anchor]
        if anchor in image_order:
            return "IMAGE", image_order[anchor]
        raise AuthoringError(f"unknown anchor {anchor}")

    specs = sorted(
        ALL_CANDIDATES,
        key=lambda item: (anchor_details(item["anchor"])[1], item["_insertion"]),
    )
    return _allocate_tail(
        specs,
        anchor_details,
        unit_order,
        image_order,
        asset_by_path,
    )


DEFECT_UNITS = {
    "U000726": (
        "A000796 has a hard bottom-edge bleed/cut through the following plot "
        "row. The eight recurrence formulas and displayed prefixes above it "
        "remain legible, but the asset is used only as DEFECT_LIMITED evidence "
        "and no content is inferred from the cut row."
    )
}

HISTORICAL_UNITS = {
    "U000746",
    "U000747",
    "U000748",
    "U000893",
    "U000894",
    "U000900",
    "U000943",
}
APPLICATION_UNITS = {"U000892"}
REPRESENTATION_UNITS = {
    "U000652",
    "U000656",
    "U000657",
    "U000663",
    "U000666",
    "U000683",
    "U000688",
    "U000768",
    "U000769",
    "U000770",
    "U000779",
    "U000785",
    "U000795",
    "U000800",
    "U000804",
    "U000809",
    "U000815",
    "U000818",
    "U000825",
    "U000836",
    "U000838",
    "U000850",
    "U000860",
    "U000869",
    "U000873",
    "U000880",
    "U000929",
}


def default_reading(row: dict[str, str]) -> tuple[str, list[str], str]:
    uid = row["source_unit_id"]
    kind = row["block_kind"]
    if kind == "image":
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["REPRESENTATION", "BEHAVIOR_OR_OUTCOME"],
            "Reviewed in context and at required resolution; this unlinked image is an output, trajectory, plot, or display rather than another native law.",
        )
    if uid in HISTORICAL_UNITS:
        return (
            "HISTORICAL_ONLY",
            ["HISTORICAL_MENTION", "CONTROL_OR_COMPARISON"],
            "Reviewed in full; this unit supplies provenance or historical comparison without a new identity-plus-mechanics construction.",
        )
    if uid in APPLICATION_UNITS:
        return (
            "APPLICATION_OR_EMULATION",
            ["APPLICATION", "HISTORICAL_MENTION"],
            "Reviewed in full; this unit lists scientific applications of PDEs without specifying the named equations' mechanics.",
        )
    if uid in REPRESENTATION_UNITS:
        return (
            "REPRESENTATION_OR_OBSERVER",
            ["REPRESENTATION", "OBSERVER_OR_ANALYZER", "BEHAVIOR_OR_OUTCOME"],
            "Reviewed in full; this unit explains or captions a representation/observer without independently introducing another construction.",
        )
    return (
        "NO_CONSTRUCTION",
        ["BEHAVIOR_OR_OUTCOME", "CONTROL_OR_COMPARISON"],
        "Reviewed in full; this unit supplies motivation, behavior, property, comparison, or conclusion without another separately delimited construction.",
    )


def candidate_roles(
    candidate_ids: list[str],
    specs_by_id: dict[str, CandidateSpec],
    block_kind: str,
) -> list[str]:
    roles: list[str] = []
    names = " ".join(
        specs_by_id[cid]["name"].lower() for cid in candidate_ids
    )
    if "seed" in names or "initial value" in names or "initial data" in names:
        roles.append("SEED_INPUT_OR_BOUNDARY")
    if (
        "observer" in names
        or "count" in names
        or "gap" in names
        or "difference" in names
        or "query" in names
        or "hypothesis" in names
    ):
        roles.append("OBSERVER_OR_ANALYZER")
    if (
        "representation" in names
        or "codec" in names
        or "encoding" in names
        or "digit" in names
    ):
        roles.append("REPRESENTATION")
    if "preset" in names or "family" in names or "class" in names:
        roles.append("PROPERTY_OR_RESTRICTION")
    if block_kind == "image":
        roles.append("REPRESENTATION")
    return list(dict.fromkeys(roles))


def build_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    manifest = json.loads((bundle / "allowed-manifest.json").read_text())
    if (
        manifest.get("worker_id") != EXPECTED_WORKER
        or manifest.get("content_set_sha256") != EXPECTED_CONTENT_SET
        or manifest.get("source_paths") != EXPECTED_PATHS
        or manifest.get("source_unit_count") != 306
        or manifest.get("asset_count") != 63
        or manifest.get("stage") != STAGE
        or manifest.get("discovery_epoch") != 1
    ):
        raise AuthoringError("bundle is not the exact Stage 8 epoch-1 assignment")

    output_path = bundle / "output" / "output.json"
    original_bytes = output_path.read_bytes()
    output = json.loads(original_bytes)
    readings = read_csv(bundle / "input" / "reading-input.csv")
    assets = read_csv(bundle / "input" / "asset-input.csv")
    scaffold = prepare_review_output.scaffold_output(
        prepare_review_output.expected_template(bundle, manifest),
        readings,
        assets,
    )
    if output != scaffold:
        raise AuthoringError("output is not the pristine nonsemantic scaffold")

    (
        candidates,
        routes,
        candidate_links_by_unit,
        candidate_links_by_image,
        anchor_links_by_unit,
    ) = allocate(readings, assets)
    direct_image_paths = {
        ev["image_path"]
        for proposal in candidates
        for ev in proposal["source_evidence"]
        if ev["image_path"] is not None
        and ev["strength"]
        in {
            "DIRECT_IDENTITY",
            "DIRECT_PARTIAL_MECHANICS",
            "DIRECT_COMPLETE_MECHANICS",
        }
    }
    specs_sorted = sorted(
        ALL_CANDIDATES,
        key=lambda spec: next(
            i
            for i, proposal in enumerate(candidates)
            if proposal["provisional_name"] == spec["name"]
            and proposal["discovery_anchor"]["id"] == spec["anchor"]
        ),
    )
    specs_by_id = {
        proposal["id"]: spec
        for proposal, spec in zip(candidates, specs_sorted)
    }
    route_links: defaultdict[str, list[str]] = defaultdict(list)
    for route in routes:
        route_links[route["source_unit_id"]].append(route["route_id"])

    reading_updates: list[dict[str, str]] = []
    for original in readings:
        row = deepcopy(original)
        uid = row["source_unit_id"]
        cids = candidate_links_by_unit.get(uid, [])
        rids = route_links.get(uid, [])
        if uid in DEFECT_UNITS:
            disposition = "SOURCE_DEFECT_OR_AMBIGUITY"
            secondary = ["SOURCE_DEFECT", "REPRESENTATION"]
            statement = (
                f"Reviewed in full and at original resolution; {DEFECT_UNITS[uid]} "
                f"Linked candidates: {', '.join(cids)}."
            )
            status = "DEFECTIVE"
            uncertainty = DEFECT_UNITS[uid]
        elif cids:
            is_anchor = bool(
                set(cids) & set(anchor_links_by_unit.get(uid, []))
            )
            disposition = "CANDIDATE" if is_anchor else "SUPPORTS_CANDIDATE"
            secondary = candidate_roles(cids, specs_by_id, row["block_kind"])
            statement = (
                f"This unit {'discovers' if is_anchor else 'supports'} "
                f"{', '.join(cids)} with source-grounded identity, mechanics, "
                "function, relation, seed, representation, observer, or preset evidence."
            )
            if rids:
                statement += f" It also originates {', '.join(rids)}."
            status = "CLEAR"
            uncertainty = ""
        elif rids:
            disposition = "CROSS_REFERENCE"
            secondary = ["CONTROL_OR_COMPARISON"]
            statement = (
                f"Reviewed in full; this unit originates {', '.join(rids)} "
                "to construction-bearing targets and does not independently "
                "supply another local law."
            )
            status = "CLEAR"
            uncertainty = ""
        else:
            disposition, secondary, statement = default_reading(row)
            status = "CLEAR"
            uncertainty = ""
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "1",
                "review_disposition": disposition,
                "source_status": status,
                "uncertainty": uncertainty,
                "secondary_roles": compact(secondary),
                "candidate_ids": compact(cids),
                "route_ids": compact(rids),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": EXPECTED_WORKER,
            }
        )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in assets:
        row = deepcopy(original)
        path = row["physical_path"]
        uid = row["source_unit_id"]
        cids = candidate_links_by_image.get(path, [])
        if path == "CHAPTERS/_page_130_Chapter_Opener.jpeg":
            role = "DECORATIVE"
            risks: list[str] = []
            transcription = "NOT_REQUIRED"
            status = "CLEAR"
            uncertainty = ""
            statement = "Original-resolution inspection confirms a decorative chapter opener with no construction-bearing content."
        elif uid in DEFECT_UNITS:
            role = "SOURCE_DEFECT"
            risks = [
                "CONSTRUCTION_BEARING",
                "TEXT_BEARING",
                "AMBIGUOUS",
                "CAPTION_INCOMPLETE",
            ]
            transcription = "CHECKED"
            status = "DEFECTIVE"
            uncertainty = DEFECT_UNITS[uid]
            statement = (
                "Original-resolution inspection confirms legible recurrence "
                "formulas/prefixes above a hard bottom-edge bleed/cut through "
                "the next plot row. It is linked only as DEFECT_LIMITED "
                f"evidence to {', '.join(cids)}."
            )
        elif path in direct_image_paths:
            role = "NATIVE_EVIDENCE"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            transcription = "CHECKED"
            status = "CLEAR"
            uncertainty = ""
            statement = (
                "Original-resolution inspection and independent transcription "
                "confirm direct identity or mechanics evidence"
                + (f" for {', '.join(cids)}." if cids else ".")
            )
        else:
            role = "OBSERVER"
            risks = []
            transcription = "NOT_REQUIRED"
            status = "CLEAR"
            uncertainty = ""
            statement = (
                "Thumbnail/context review and source-preserving inspection "
                "confirm an output history, plot, mesh, finite digit display, "
                "or alternative representation rather than independent mechanics"
                + (f" supporting {', '.join(cids)}." if cids else ".")
            )
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "1",
                "visual_role": role,
                "source_status": status,
                "risk_flags": compact(risks),
                "original_resolution_status": "REVIEWED",
                "transcription_status": transcription,
                "candidate_ids": compact(cids),
                "route_ids": compact(route_links.get(uid, [])),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": EXPECTED_WORKER,
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append(row)

    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": candidates,
            "asset_updates": asset_updates,
            "route_proposals": routes,
            "uncertainties": [
                "A000796 has a hard bottom-edge bleed/cut through the next plot row; its legible recurrence formulas/prefixes are retained only as DEFECT_LIMITED evidence.",
                "The Riemann-Siegel Z function is identified only as 'essentially' Zeta[1/2+i t], leaving its exact phase and normalization unknown.",
                "The random interval seed ensemble has no specified probability measure, endpoint convention, or precision model.",
                "The symbolic PDE sampler lacks its grammar, component vocabulary, size control, and sampling law.",
                "The PDE numerical approximation scheme is unnamed: stencil, space/time steps, integrator, precision, boundaries, stability, and convergence checks are all absent.",
            ],
        }
    )
    return original_bytes, proposed


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} BUNDLE", file=sys.stderr)
        return 2
    bundle = Path(sys.argv[1]).resolve()
    try:
        with prepare_review_output.output_lock(bundle):
            original_bytes, proposed = build_output(bundle)
            prepare_review_output.atomic_replace(
                bundle / "output" / "output.json",
                canonical_json_bytes(proposed),
                original_bytes,
            )
    except (
        OSError,
        csv.Error,
        json.JSONDecodeError,
        AuthoringError,
        ValueError,
    ) as exc:
        print(f"Chapter 4 main authoring failed: {exc}", file=sys.stderr)
        return 1
    print(
        "recorded Stage 8 Chapter 4 main review: "
        f"reading=306 assets=63 candidates={len(ALL_CANDIDATES)} "
        f"routes={len(ALL_ROUTES)} declaration=false"
    )
    return 0


def _allocate_tail(
    specs: list[CandidateSpec],
    anchor_details: Any,
    unit_order: dict[str, int],
    image_order: dict[str, int],
    asset_by_path: dict[str, dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, list[str]],
]:
    id_by_key = {
        item["key"]: f"W{index:04d}" for index, item in enumerate(specs, 1)
    }
    candidate_ordinals: dict[str, int] = {}
    candidate_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for item in specs:
        kind, _ = anchor_details(item["anchor"])
        identity = (kind, item["anchor"])
        candidate_counts[identity] += 1
        candidate_ordinals[item["key"]] = candidate_counts[identity]

    evidence_entries: list[tuple[CandidateSpec, EvidenceSpec, str, int]] = []
    for item in ALL_CANDIDATES:
        for ev in item["evidence"]:
            anchor = ev["image_path"] or ev["unit"]
            kind, order = anchor_details(anchor)
            evidence_entries.append((item, ev, kind, order))
    evidence_entries.sort(
        key=lambda x: (x[3], x[1]["_insertion"], x[0]["_insertion"])
    )
    ev_identity: dict[tuple[str, str], tuple[str, str, int]] = {}
    ev_counts: defaultdict[tuple[str, str], int] = defaultdict(int)
    for index, (item, ev, kind, _order) in enumerate(evidence_entries, 1):
        anchor = ev["image_path"] or ev["unit"]
        identity = (kind, anchor)
        ev_counts[identity] += 1
        ev_identity[(item["key"], ev["label"])] = (
            f"WE{index:06d}",
            f"WG{index:06d}",
            ev_counts[identity],
        )

    route_specs = sorted(
        ALL_ROUTES,
        key=lambda item: (unit_order[item["unit"]], item["_insertion"]),
    )
    route_id_by_key = {
        item["key"]: f"WR{index:04d}"
        for index, item in enumerate(route_specs, 1)
    }
    route_counts: defaultdict[str, int] = defaultdict(int)
    route_proposals: list[dict[str, str]] = []
    for item in route_specs:
        route_counts[item["unit"]] += 1
        route_proposals.append(
            {
                "route_id": route_id_by_key[item["key"]],
                "source_unit_id": item["unit"],
                "source_asset_id": "",
                "discovery_epoch": "1",
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": item["unit"],
                "discovery_ordinal": str(route_counts[item["unit"]]),
                "literal_target": item["literal"],
                "route_kind": item["kind"],
                "expected_topic": item["topic"],
                "owning_stage": str(STAGE),
                "closure_scope": item["scope"],
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": "[]",
                "vocabulary_terms": compact(item["vocabulary"]),
                "defect_boundary": "",
            }
        )

    candidate_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    candidate_links_by_image: defaultdict[str, list[str]] = defaultdict(list)
    anchor_links_by_unit: defaultdict[str, list[str]] = defaultdict(list)
    proposals: list[dict[str, Any]] = []

    for item in specs:
        cid = id_by_key[item["key"]]
        anchor_kind, anchor_order = anchor_details(item["anchor"])
        local: list[dict[str, Any]] = []
        label_to_id: dict[str, str] = {}
        for ev in item["evidence"]:
            eid, gid, ordinal = ev_identity[(item["key"], ev["label"])]
            label_to_id[ev["label"]] = eid
            ev_anchor = ev["image_path"] or ev["unit"]
            ev_kind, ev_order = anchor_details(ev_anchor)
            if ev_order < anchor_order:
                raise AuthoringError(
                    f"evidence {ev['label']} predates candidate {item['key']}"
                )
            local.append(
                {
                    "evidence_id": eid,
                    "evidence_group_id": gid,
                    "discovery_anchor": {
                        "epoch": 1,
                        "kind": ev_kind,
                        "id": ev_anchor,
                        "ordinal": ordinal,
                    },
                    "source_unit_id": ev["unit"],
                    "image_path": ev["image_path"],
                    "strength": ev["strength"],
                    "modality": ev["modality"],
                    "claim": ev["claim"],
                    "fingerprint_fields": ev["fields"],
                }
            )
        if not local:
            raise AuthoringError(f"candidate {item['key']} has no evidence")
        local.sort(key=lambda x: int(x["evidence_id"][2:]))
        units = sorted(
            {ev["source_unit_id"] for ev in local},
            key=lambda x: unit_order[x],
        )
        images = sorted(
            {ev["image_path"] for ev in local if ev["image_path"] is not None},
            key=lambda x: image_order[x],
        )
        for uid in units:
            candidate_links_by_unit[uid].append(cid)
        for path in images:
            candidate_links_by_image[path].append(cid)
        anchor_unit = (
            item["anchor"]
            if anchor_kind == "SOURCE_UNIT"
            else asset_by_path[item["anchor"]]["source_unit_id"]
        )
        if anchor_unit not in units:
            raise AuthoringError(
                f"candidate {item['key']} lacks evidence at discovery anchor {anchor_unit}"
            )
        anchor_links_by_unit[anchor_unit].append(cid)

        field_support: dict[str, str] = {}
        fingerprint: dict[str, dict[str, Any]] = {}
        unknowns: list[str] = []
        for field in FINGERPRINT_FIELDS:
            supporting = [
                ev["evidence_id"]
                for ev in local
                if field in ev["fingerprint_fields"]
            ]
            if field in item["facts"]:
                if not supporting:
                    raise AuthoringError(f"{item['key']} lacks evidence for {field}")
                field_support[field] = "SUPPORTED"
                fingerprint[field] = {
                    "status": "SUPPORTED",
                    "value": item["facts"][field],
                    "evidence_ids": supporting,
                    "reason": "",
                }
            elif field in item["not_applicable"]:
                if not supporting:
                    raise AuthoringError(f"{item['key']} lacks N/A evidence for {field}")
                field_support[field] = "NOT_APPLICABLE"
                fingerprint[field] = {
                    "status": "NOT_APPLICABLE",
                    "value": None,
                    "evidence_ids": supporting,
                    "reason": item["not_applicable"][field],
                }
            else:
                if supporting:
                    raise AuthoringError(
                        f"{item['key']} supplies evidence for absent field {field}"
                    )
                reason = unknown_reason(item, field)
                unknowns.append(reason)
                field_support[field] = "UNKNOWN_FROM_SOURCE"
                fingerprint[field] = {
                    "status": "UNKNOWN_FROM_SOURCE",
                    "value": None,
                    "evidence_ids": [],
                    "reason": reason,
                }

        def records(values: list[tuple[str, str, list[str]]]) -> list[dict[str, Any]]:
            return [
                {
                    "name": name,
                    "source_description": description,
                    "evidence_ids": [label_to_id[label] for label in labels],
                }
                for name, description, labels in values
            ]

        route_ids = [route_id_by_key[key] for key in item["route_keys"]]
        related_ids = [
            {
                "candidate_id": id_by_key[key],
                "relation": "POSSIBLE_VARIANT_OF",
                "proof_kind": "PROVISIONAL_COMPARISON",
                "evidence_ids": [
                    next(
                        ev["evidence_id"]
                        for ev in local
                        if ev["strength"] != "LEAD_ONLY"
                    )
                ],
                "before_rationale": "",
                "after_rationale": "",
                "uncertainty": (
                    "The source supports family/preset membership, but this "
                    "provisional relation is not an identity merge."
                ),
            }
            for key in item.get("related_keys", [])
        ]
        values: dict[str, Any] = {
            "id": cid,
            "record_status": "ACTIVE",
            "provisional_name": item["name"],
            "aliases": item["aliases"],
            "discovery_stage": STAGE,
            "discovery_anchor": {
                "epoch": 1,
                "kind": anchor_kind,
                "id": item["anchor"],
                "ordinal": candidate_ordinals[item["key"]],
            },
            "source_unit_ids": units,
            "source_evidence": local,
            "source_status": item["source_status"],
            "image_witnesses": images,
            "evidence_strength": list(
                dict.fromkeys(ev["strength"] for ev in local)
            ),
            "field_support": field_support,
            "fingerprint": fingerprint,
            "parameters": records(item["parameters"]),
            "variants": records(item["variants"]),
            "missing_mechanics": list(
                dict.fromkeys([item["missing"], *unknowns])
            ),
            "uncertainties": item["uncertainties"],
            "related_candidate_ids": related_ids,
            "cross_reference_ids": route_ids,
            "evidence_reassignments": [],
        }
        proposals.append({field: values[field] for field in CANDIDATE_FIELDS})

    return (
        proposals,
        route_proposals,
        dict(candidate_links_by_unit),
        dict(candidate_links_by_image),
        dict(anchor_links_by_unit),
    )


if __name__ == "__main__":
    raise SystemExit(main())
