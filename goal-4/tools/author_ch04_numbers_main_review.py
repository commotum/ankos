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
    kind="A positional radix representation codec for numbers.",
    carrier="An ordered sequence of digits together with a radix b.",
    support="Digit positions indexed from the units position outward, with optional fractional positions.",
    alphabet="Digits 0 through b-1 and positional weights that are powers of b.",
    state="A radix b digit sequence, or the number it denotes.",
    input_value="A radix b digit sequence for decoding, or a number for representation.",
    law_kind="A positional weighted-sum representation and its inverse.",
    law=(
        "Starting at the right, multiply successive digits by 1, b, b^2, ... "
        "and sum them; fractional positions use reciprocal powers of b."
    ),
    result="The represented number, or its radix b digit sequence.",
    successor="One value is denoted by every digit sequence; the usual canonical expansion is intended in the reverse direction.",
    determinism="Deterministic for a fixed radix and digit sequence.",
    termination="Finite sequences decode by a finite sum; nonterminating fractional expansions denote limiting values.",
    witness="The weighted positional sum equals the represented number.",
    variants="The radix b varies; the source explicitly displays bases 2 through 10.",
    excluded="Typography, black/white cell rendering, and stacked histories do not change the denoted number.",
    limit="The source does not discuss the two-expansion ambiguity for terminating fractions.",
)
radix = source_candidate(
    "radix-family",
    "positional radix representation codec",
    "U000653",
    RADIX_FACTS,
    aliases=["base-b digit-sequence representation"],
    not_applicable=DECLARATIVE_NA,
    missing="The convention for dual terminating/nonterminating fractional expansions is not discussed.",
    claim="The passage defines a base by its digit choices and the adjacent table gives the positional weighted sums.",
    strength="DIRECT_COMPLETE_MECHANICS",
)
context_evidence(
    radix,
    "radix-table",
    "U000654",
    "The table explicitly decomposes 3829 into positional weights in bases 2 through 10.",
    fields=["parameters_and_variants"],
    strength="DIRECT_COMPLETE_MECHANICS",
    modality="TABLE",
)
context_evidence(
    radix,
    "radix-caption",
    "U000655",
    "The caption states the right-to-left powers-of-base convention and digit alphabets.",
    fields=["rule_relation_constraint_function_or_probability_law"],
    strength="DIRECT_COMPLETE_MECHANICS",
)


def radix_preset(base: int) -> CandidateSpec:
    facts = deepcopy(RADIX_FACTS)
    facts["object_kind"] = f"The positional base-{base} representation codec."
    facts["alphabet_or_value_schema"] = f"Digits 0 through {base - 1} with positional weights that are powers of {base}."
    facts["parameters_and_variants"] = f"The radix is fixed at b={base}."
    return source_candidate(
        f"radix-base-{base}",
        f"base-{base} positional representation",
        "U000654",
        facts,
        not_applicable=DECLARATIVE_NA,
        missing="The convention for dual terminating/nonterminating fractional expansions is not discussed.",
        claim=f"The table directly supplies the base-{base} weighted decomposition of 3829.",
        strength="DIRECT_COMPLETE_MECHANICS",
        modality="TABLE",
    )


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
        strength="DIRECT_COMPLETE_MECHANICS",
        image_path="CHAPTERS/_page_144_Figure_3.jpeg",
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
        declarative_facts(
            kind=name,
            carrier="Scalar numeric inputs and real outputs.",
            support="One scalar argument.",
            alphabet="Real or positive-real values as displayed.",
            state="The input scalar.",
            input_value="The displayed numeric argument.",
            law_kind="A named mathematical function.",
            law=law,
            result=result,
            successor="The source treats the function as single-valued on the displayed inputs.",
            determinism="Deterministic under the conventional branch used by the displayed real values.",
            termination="The denotation is fixed, though no evaluation algorithm is given.",
            witness="The displayed decimal and binary expansions witness the identified output values.",
            variants="The table displays multiple arguments or powers.",
            excluded="Digit expansions are representations of the results.",
            limit="The assigned source names and exemplifies the operation but does not define its full domain, branch, or evaluation law.",
        ),
        not_applicable=DECLARATIVE_NA,
        missing="The full domain, branch convention, and native evaluation mechanics are not defined in the assigned source.",
        claim=f"The table materially delimits {name} by named expressions and result digit sequences.",
        strength="DIRECT_IDENTITY",
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

continued_fraction = source_candidate(
    "continued-fraction-representation",
    "continued-fraction representation codec",
    "U000801",
    declarative_facts(
        kind="A continued-fraction representation of a number.",
        carrier="An ordered sequence of integer coefficients.",
        support="Successive nested denominator positions.",
        alphabet="Integer coefficients.",
        state="A coefficient sequence {a0,a1,a2,...}.",
        input_value="A coefficient sequence for decoding, or a number for representation.",
        law_kind="A nested addition-and-reciprocal assembly.",
        law="Assemble a0 + 1/(a1 + 1/(a2 + 1/(...))).",
        result="The represented number, or its coefficient sequence.",
        successor="One value per convergent/infinite coefficient sequence under the stated convention.",
        determinism="Deterministic for a fixed coefficient sequence.",
        termination="Finite sequences evaluate finitely; infinite sequences denote a limit when convergent.",
        witness="Successive finite convergents approach the represented value.",
        variants="Rational numbers yield finite sequences; other displayed constants yield infinite sequences.",
        excluded="Braces and line breaking are printed representations.",
        limit="The extraction algorithm from a number to coefficients is not stated.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The coefficient-extraction algorithm and canonical terminal convention are not stated.",
    claim="The passage and formula explicitly define construction by successive additions and divisions.",
    strength="DIRECT_PARTIAL_MECHANICS",
)

pi_cf = source_candidate(
    "pi-continued-fraction",
    "continued-fraction representation of pi",
    "U000802",
    {**deepcopy(continued_fraction["facts"]), "object_kind": "The continued-fraction representation of pi.", "input": "The constant pi.", "complete_state": "The displayed coefficient sequence beginning {3,7,15,1,292,...}.", "parameters_and_variants": "The represented value is fixed at pi."},
    not_applicable=DECLARATIVE_NA,
    missing="The source supplies a coefficient prefix but no procedure for generating arbitrary later coefficients.",
    claim="The nested formula and following coefficient list explicitly give pi's continued fraction.",
    strength="DIRECT_PARTIAL_MECHANICS",
    modality="FORMULA",
)

symbolic_representation = source_candidate(
    "symbolic-number-representation",
    "symbolic-expression representation of numbers",
    "U000806",
    declarative_facts(
        kind="A representation of a number by a symbolic mathematical expression.",
        carrier="Expression trees built from constants and mathematical operations.",
        support="The syntactic positions of a finite expression.",
        alphabet="Numbers, operation symbols, and grouping.",
        state="A symbolic expression such as sqrt(2)+e^sqrt(3).",
        input_value="A well-formed symbolic expression.",
        law_kind="Expression evaluation.",
        law="Evaluate the represented operations to obtain the number denoted by the expression.",
        result="The denoted number.",
        successor="The source intends one value for each valid expression.",
        determinism="Deterministic when every operation and branch is fixed.",
        termination="Evaluation effort may be difficult; no uniform algorithm or bound is supplied.",
        witness="A correct evaluation derives the denoted numeric value.",
        variants="The expression grammar and available operations are left open.",
        excluded="Expression brevity is not the same as digit-sequence simplicity or evaluation cost.",
        limit="No formal grammar, branch convention, or evaluator is specified.",
    ),
    not_applicable=DECLARATIVE_NA,
    missing="The expression grammar, operation set, branch semantics, and evaluator are not specified.",
    claim="The passage explicitly identifies symbolic expressions as number representations and distinguishes denotation from evaluation effort.",
    strength="DIRECT_PARTIAL_MECHANICS",
    uncertainties=["The representation class is deliberately open-ended in this source."],
)
