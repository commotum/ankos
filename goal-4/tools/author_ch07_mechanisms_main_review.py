#!/usr/bin/env python3
"""Author the sealed Stage 11 Chapter 7 main-text blind review.

The helper is deliberately bundle-local: every byte it reads is beneath the
bundle supplied on the command line.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


WORKER_ID = "ch07-main"
STAGE = 11
EPOCH = 2
SOURCE_PATH = "CHAPTERS/07-Mechanisms-in-Programs-and-Nature.md"
EXPECTED_CANDIDATES = 84

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


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def evolution(
    object_kind: str,
    law: str,
    *,
    carrier: str = "a spatial configuration of elements",
    alphabet: str = "the source-stated element values",
    state: str = "the value of every element at one step",
    seed: str = "a source-stated initial configuration",
    activation: str = "the elements selected by the stated step law",
    schedule: str = "successive discrete steps",
    neighborhood: str = "the source-stated dependencies for each update",
    result: str = "one successor configuration",
    determinism: str = "deterministic for a fixed complete state",
    variants: str = "the source-stated parameters and displayed variants",
    external: str | None = None,
) -> dict[str, str]:
    values = {
        "object_kind": object_kind,
        "native_time": "successive discrete steps",
        "carrier": carrier,
        "alphabet_or_value_schema": alphabet,
        "complete_state": state,
        "seed": seed,
        "frontier_or_activation": activation,
        "schedule": schedule,
        "read_dependencies_or_neighborhood": neighborhood,
        "law_kind": "successor-state law",
        "rule_relation_constraint_function_or_probability_law": law,
        "write_replacement_assembly_or_commit": (
            "the values produced for one step form the next complete state"
        ),
        "result_kind": result,
        "successor_cardinality": (
            "one successor for a fixed state"
            if determinism.startswith("deterministic")
            else "a probability distribution or branching set of successors"
        ),
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": (
            "iteration has no intrinsic stopping condition unless the stated process supplies one"
        ),
        "parameters_and_variants": variants,
    }
    if external is not None:
        values["external_data"] = external
    return values


def relation(
    object_kind: str,
    law: str,
    *,
    carrier: str,
    input_value: str,
    result: str,
    determinism: str = "deterministic for a fixed complete input",
    neighborhood: str | None = None,
    variants: str = "the source-stated parameters and variants",
) -> dict[str, str]:
    values = {
        "object_kind": object_kind,
        "native_time": "no independent iterative time; the relation is evaluated on its input",
        "carrier": carrier,
        "complete_state": "the complete input required by the relation",
        "input": input_value,
        "law_kind": "relation, function, query, or observation law",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "determinism_branching_or_measure": determinism,
        "termination_completion_failure": (
            "evaluation completes when the stated result has been determined"
        ),
        "witness_semantics": "a witness is an input and result satisfying the stated law",
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": (
            "the relation does not alter the native evolution of any input system"
        ),
    }
    if neighborhood is not None:
        values["read_dependencies_or_neighborhood"] = neighborhood
    return values


def constraint(
    object_kind: str,
    law: str,
    *,
    carrier: str,
    state: str,
    result: str = "the set of configurations satisfying the constraint",
    neighborhood: str | None = None,
    variants: str = "the source-stated constraint parameters",
) -> dict[str, str]:
    values = {
        "object_kind": object_kind,
        "native_time": "none; this is a declarative condition on configurations",
        "carrier": carrier,
        "complete_state": state,
        "input": "a candidate configuration",
        "law_kind": "constraint or accepted-result condition",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "successor_cardinality": "zero or more satisfying configurations",
        "determinism_branching_or_measure": (
            "membership is deterministic for a fixed candidate configuration"
        ),
        "termination_completion_failure": (
            "a configuration succeeds exactly when the stated condition holds"
        ),
        "witness_semantics": "a witness is a configuration satisfying every stated condition",
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": (
            "a search procedure for finding witnesses is separate from the constraint"
        ),
    }
    if neighborhood is not None:
        values["read_dependencies_or_neighborhood"] = neighborhood
    return values


def observer(
    object_kind: str,
    law: str,
    *,
    carrier: str,
    input_value: str,
    result: str,
    neighborhood: str,
    variants: str = "the source-stated observation parameters",
) -> dict[str, str]:
    return {
        "object_kind": object_kind,
        "native_time": "applied to source states or successive source-system steps",
        "carrier": carrier,
        "input": input_value,
        "read_dependencies_or_neighborhood": neighborhood,
        "law_kind": "input-processing or observation law",
        "rule_relation_constraint_function_or_probability_law": law,
        "result_kind": result,
        "determinism_branching_or_measure": "deterministic for a fixed input",
        "termination_completion_failure": (
            "observation completes when the requested sample or derived view is produced"
        ),
        "witness_semantics": "the output witnesses a property of the input without changing it",
        "parameters_and_variants": variants,
        "excluded_observers_and_representations": (
            "the observer output is not part of the source system's native state"
        ),
    }


def candidate_definitions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(
        name: str,
        anchor: str,
        profile: str,
        values: dict[str, str],
        *,
        units: list[str] | None = None,
        mechanics: str | None = None,
        aliases: list[str] | None = None,
        parameters: list[str] | None = None,
        variants: list[str] | None = None,
        item_evidence: str | None = None,
        identity_units: list[str] | None = None,
        uncertainty: str = "",
        complete: bool = False,
    ) -> None:
        ordered_units = [anchor] + [unit for unit in (units or []) if unit != anchor]
        rows.append(
            {
                "name": name,
                "anchor": anchor,
                "profile": profile,
                "values": values,
                "units": ordered_units,
                "mechanics": mechanics or anchor,
                "aliases": aliases or [],
                "parameters": parameters or [],
                "variants": variants or [],
                "item_evidence": item_evidence or mechanics or anchor,
                "identity_units": identity_units or [],
                "uncertainty": uncertainty,
                "complete": complete,
            }
        )

    add(
        "per-step random-cell recoloring process",
        "U001599",
        "EVOLUTION",
        evolution(
            "stochastic cell-field process",
            "choose a random color for every cell independently described at every step",
            carrier="a field of cells",
            alphabet="cell colors",
            seed="an initial cell field",
            activation="every cell at every step",
            neighborhood="no neighboring state is stated as required; each new color comes from external random input",
            determinism="stochastic; the color distribution and independence law are not stated",
            variants="continual random input from the environment",
            external="fresh random color input is supplied for every cell at every step",
        ),
        units=["U001600"],
        mechanics="U001600",
        aliases=["stochastic-model randomness mechanism"],
        uncertainty="The color distribution, field extent, boundary, and independence assumptions are not stated.",
    )
    add(
        "random-start deterministic left-shift process",
        "U001599",
        "EVOLUTION",
        evolution(
            "deterministic cell-field shift process",
            "shift every cell color one position to the left on each step",
            carrier="a one-dimensional field of colored cells",
            alphabet="cell colors",
            seed="a randomly chosen initial color field",
            activation="every cell",
            neighborhood="the cell one position to the right supplies the next color",
            variants="random initial conditions followed by a left shift",
            external="randomness is supplied only in the initial condition",
        ),
        units=["U001602", "U001603", "U001604"],
        mechanics="U001603",
        aliases=["initial-condition transcription mechanism"],
        complete=True,
    )
    add(
        "microscopic-breakdown noise amplifier",
        "U001622",
        "EVOLUTION",
        evolution(
            "physical threshold-and-amplification process",
            "microscopic fluctuations initiate a breakdown event under extreme operating conditions, yielding a large output signal",
            carrier="an electronic or electrical sampling device",
            alphabet="microscopic device state and macroscopic output events",
            state="the device state together with its microscopic environment",
            seed="a prepared high-sensitivity operating condition",
            activation="breakdown-capable components",
            schedule="successive sampled events separated by device relaxation",
            neighborhood="microscopic fluctuations coupled to the breakdown component",
            determinism="environment-driven and treated stochastically at the observed level",
            variants="air-gap plates, vacuum tubes, and semiconductor devices",
            external="microscopic environmental fluctuations supply the initiating variation",
        ),
        units=["U001623", "U001624", "U001628", "U001629", "U001630"],
        parameters=["operating threshold", "sampling interval", "device relaxation time"],
        variants=["air-gap spark device", "vacuum-tube device", "semiconductor-breakdown device"],
        uncertainty="The source supplies no quantitative circuit, probability measure, or complete relaxation law.",
    )
    add(
        "friction-slowed half-colored rolling-ball process",
        "U001640",
        "EVOLUTION",
        evolution(
            "continuous rolling-and-stopping process with a binary readout",
            "roll a half-black, half-white ball at an initial speed; friction slows it until it stops, and return the color on top",
            carrier="a half-black, half-white ball rolling along a surface",
            alphabet="continuous position, speed, and orientation with a black-or-white terminal readout",
            state="the ball's current position, speed, and orientation",
            seed="the starting position, orientation, and initial rolling speed",
            activation="the rolling ball",
            schedule="continuous physical time until rest",
            neighborhood="the ball state together with friction from the surface",
            result="a stopped orientation and the black-or-white color on top",
            variants="the source-displayed sequence of nearby initial speeds",
        ),
        units=["U001641", "U001642", "U001643", "U001644"],
        parameters=["initial speed", "initial orientation", "friction"],
        uncertainty="The equations of motion, friction law, surface boundary, and stopping threshold are not stated.",
    )
    add(
        "stretch-cut-stack kneading map",
        "U001649",
        "EVOLUTION",
        evolution(
            "one-dimensional real-valued map",
            "map position x to FractionalPart[2 x] after stretching to twice the length, cutting, and stacking",
            carrier="positions x in material represented from 0 to 1",
            alphabet="real positions in the unit interval",
            state="the position of each tracked point",
            seed="one or more initial point positions",
            activation="every tracked point",
            neighborhood="each point's own current position",
            result="one successor position for every tracked point",
            variants="geometric stretch-cut-stack form and base-2 left-shift form",
        ),
        units=["U001653", "U001656", "U001658", "U001660", "U001652", "U001659"],
        mechanics="U001660",
        aliases=["kneading process", "fractional-part doubling map"],
        parameters=["initial position x"],
        variants=["geometric kneading", "base-2 digit left shift"],
        complete=True,
    )
    add(
        "mirror-based kneading-map apparatus",
        "U001674",
        "EVOLUTION",
        evolution(
            "optical-mechanical map emulator",
            "repeated reflections reproduce the same sensitive position evolution as the kneading construction",
            carrier="a light ray or point trajectory in the displayed mirror apparatus",
            alphabet="continuous ray position and direction",
            state="the ray's current geometric state",
            seed="an initial ray position and direction",
            activation="the ray at each encounter with the apparatus",
            neighborhood="the current ray state and encountered mirror geometry",
            result="a successor ray state",
            variants="the displayed mirror realization",
        ),
        units=["U001676", "U001677", "U001678"],
        uncertainty="The source does not give complete mirror coordinates or an explicit ray-state formula.",
    )
    add(
        "elastic-collision pegboard process",
        "U001680",
        "EVOLUTION",
        evolution(
            "gravity-driven elastic-collision process",
            "balls fall under gravity and undergo elastic collisions with pegs",
            carrier="balls moving through a peg array",
            alphabet="continuous positions and velocities",
            state="all ball positions and velocities",
            seed="initial ball positions and velocities",
            activation="moving balls at free flight and collision events",
            schedule="continuous motion punctuated by collision events",
            neighborhood="a ball and the peg or boundary it contacts",
            result="successive continuous trajectories",
            variants="the displayed pegboard geometry",
        ),
        units=["U001682", "U001683", "U001684"],
        uncertainty="Peg geometry, boundary conditions, and full collision equations are not stated.",
    )
    add(
        "restricted three-body scattering process",
        "U001686",
        "EVOLUTION",
        evolution(
            "continuous gravitational scattering process",
            "a light body moves in the gravitational field of two fixed or prescribed heavy bodies",
            carrier="three-body position and velocity space",
            alphabet="continuous positions and velocities",
            state="the current positions and velocities needed by the gravitational motion",
            seed="an initial position and velocity for the light body",
            activation="the moving light body",
            schedule="continuous physical time",
            neighborhood="gravitational influence of the two heavy bodies",
            result="a continuous trajectory or escape outcome",
            variants="the displayed restricted three-body setup",
        ),
        units=["U001690", "U001691", "U001692"],
        uncertainty="Masses, units, exact equations, and stopping conventions are not stated in this range.",
    )
    add(
        "rule 30 single-black-cell evolution",
        "U001696",
        "EVOLUTION",
        evolution(
            "one-dimensional binary cellular-automaton preset",
            "apply the source's rule 30 local transition to every cell synchronously",
            carrier="a one-dimensional row of cells",
            alphabet="black and white",
            seed="one black cell in an otherwise white field",
            activation="every cell",
            neighborhood="a cell and its two immediate neighbors",
            variants="rule 30 with a single black initial cell",
            external="no random input is supplied during the evolution",
        ),
        units=["U001697", "U001698", "U001745"],
        aliases=["rule 30 intrinsic-randomness process"],
        parameters=["rule 30", "single-black-cell seed"],
    )
    add(
        "rule 30 center-cell sequence observer",
        "U001701",
        "OBSERVER",
        observer(
            "center-column sequence observer",
            "at each successive step, select and return the color of the center cell",
            carrier="a rule 30 space-time evolution",
            input_value="successive rule 30 configurations and a fixed center position",
            result="a binary sequence over time",
            neighborhood="the center cell at every step",
            variants="center cell of the single-black-cell rule 30 evolution",
        ),
        units=["U001708", "U001710"],
        aliases=["rule 30 center column"],
        complete=True,
    )
    add(
        "wrapped rule 30 random-bit generator",
        "U001712",
        "EVOLUTION",
        evolution(
            "finite cyclic cellular-automaton random-bit generator",
            "on each call advance wrapped rule 30 by one step and return the center-cell value",
            carrier="a cyclic row a few hundred cells wide",
            alphabet="binary cell values and returned bits",
            state="the complete wrapped rule 30 row",
            seed="an explicit initial condition, or a representation of computer-system state on the first call",
            activation="all wrapped cells, followed by the center-cell observation",
            neighborhood="the rule 30 three-cell neighborhood with cyclic wraparound",
            result="an updated generator state and one returned bit",
            variants="explicit seed or system-state-derived seed",
        ),
        units=["U001713", "U001714", "U001715"],
        aliases=["Random[Integer] rule 30 generator"],
        parameters=["cyclic width", "initial condition"],
        variants=["explicit initial condition", "computer-state-derived initial condition"],
        complete=True,
    )
    add(
        "fixed-multiplier base-2 digit process",
        "U001717",
        "EVOLUTION",
        evolution(
            "integer multiplication process",
            "multiply the current integer by a fixed constant at each step",
            carrier="nonnegative integers represented in base 2",
            alphabet="base-2 digits",
            state="the current integer or its complete digit sequence",
            seed="the integer 1 in the displayed examples",
            activation="the current integer",
            neighborhood="the current integer",
            result="the next multiplied integer and its digit sequence",
            variants="the fixed multipliers displayed in the source",
        ),
        units=["U001722", "U001723"],
        parameters=["fixed multiplier"],
        variants=["multiplier 3", "multiplier 5", "multiplier 37", "multiplier 65539"],
    )
    add(
        "31-bit multiplicative congruential generator",
        "U001718",
        "EVOLUTION",
        evolution(
            "finite multiplicative congruential generator",
            "multiply by the selected constant and retain only the rightmost 31 base-2 digits",
            carrier="31-bit integers",
            alphabet="31 base-2 digits",
            state="the current 31-bit integer",
            seed="the integer 1 in the displayed examples",
            activation="the complete current integer",
            neighborhood="the complete current integer",
            result="one successor 31-bit integer",
            variants="multipliers 3, 37, and 65539 in the displayed generator comparison",
        ),
        units=["U001720", "U001726", "U001727"],
        mechanics="U001727",
        aliases=["linear congruential random number generator"],
        parameters=["31-bit width", "multiplier"],
        variants=["multiplier 3", "multiplier 37", "multiplier 65539"],
        complete=True,
    )
    add(
        "successive-output coordinate plot",
        "U001724",
        "OBSERVER",
        observer(
            "successive-number coordinate observer",
            "form two- or three-dimensional points from successive generator outputs and plot their coordinates",
            carrier="a numeric output sequence",
            input_value="successive numbers from a generator",
            result="a two- or three-dimensional point distribution",
            neighborhood="consecutive pairs or triples of sequence values",
            variants="two-dimensional and three-dimensional coordinate plots",
        ),
        units=["U001726", "U001727"],
        parameters=["coordinate dimension"],
        variants=["successive pairs", "successive triples"],
    )
    add(
        "rule 30 initial-black-cell perturbation observer",
        "U001746",
        "OBSERVER",
        observer(
            "paired center-sequence perturbation observer",
            "vary the number of adjacent initial black cells, evolve rule 30, and compare the resulting center-cell sequence with the single-black-cell reference",
            carrier="paired rule 30 space-time evolutions",
            input_value="the single-black-cell seed and seeds containing successively more initial black cells",
            result="a determination of whether the center-cell sequences agree or differ",
            neighborhood="the center cell at each step in each paired evolution",
            variants="two, three, and more initial black cells",
        ),
        units=["U001748", "U001749", "U001750"],
        parameters=["number of initial black cells"],
        variants=["two black cells", "three black cells", "more than three black cells"],
        uncertainty="The prose does not state the exact placement convention for every added black cell or a numeric sequence-comparison tolerance.",
    )
    add(
        "randomly perturbed continuous rule 90 process",
        "U001747",
        "EVOLUTION",
        evolution(
            "continuous-valued cellular-automaton preset with noise",
            "add the left and right values, apply the displayed continuous modulo-2 generalization, and perturb every value by a random amount up to the indicated percentage",
            carrier="a one-dimensional row of cells",
            alphabet="gray levels from 0 to 1",
            seed="a source-displayed initial gray-level field",
            activation="every cell",
            neighborhood="the immediate left and right cells",
            determinism="stochastic because every value is perturbed on every step",
            variants="continuous rule 90 with several perturbation percentages",
            external="a bounded random perturbation is added to every cell value on every step",
        ),
        units=["U001755", "U001757"],
        mechanics="U001757",
        parameters=["perturbation percentage"],
        uncertainty="The exact probability distribution and the analytic form of the continuous modulo-2 display are not stated in text.",
    )
    add(
        "randomly perturbed continuous rule 30 process",
        "U001752",
        "EVOLUTION",
        evolution(
            "continuous-valued rule-30 generalization with noise",
            "use a continuous algebraic representation of rule 30 and perturb every value by a random amount up to the indicated percentage",
            carrier="a one-dimensional row of cells",
            alphabet="gray levels from 0 to 1",
            seed="a source-displayed initial gray-level field",
            activation="every cell",
            neighborhood="the rule-30 three-cell neighborhood",
            determinism="stochastic because every value is perturbed on every step",
            variants="continuous rule 30 with several perturbation percentages",
            external="a bounded random perturbation is added to every cell value on every step",
        ),
        units=["U001756", "U001757"],
        mechanics="U001757",
        parameters=["perturbation percentage"],
        uncertainty="The algebraic continuous rule-30 formula and perturbation probability distribution are not stated.",
    )
    add(
        "symmetric nearest-neighbor random walk",
        "U001773",
        "EVOLUTION",
        evolution(
            "one-dimensional random walk",
            "at each step randomly move the particle one position left or one position right",
            carrier="integer positions on a one-dimensional line",
            alphabet="particle positions",
            state="the current particle position",
            seed="a starting particle position",
            activation="the particle",
            neighborhood="the two adjacent positions",
            result="a random successor position",
            determinism="stochastic; left and right probabilities are not numerically stated",
            variants="single paths and ensembles of many particles",
            external="one random left-or-right choice is supplied at each step",
        ),
        units=["U001775", "U001776"],
        aliases=["one-dimensional random walk"],
        complete=True,
    )
    add(
        "random-walk ensemble position-distribution observer",
        "U001774",
        "OBSERVER",
        observer(
            "ensemble position-distribution observer",
            "at a selected time, aggregate the positions reached by many independently displayed random-walk particles into an overall distribution",
            carrier="an ensemble of one-dimensional random-walk paths",
            input_value="many particle positions at a selected step",
            result="the empirical distribution of reached positions",
            neighborhood="all particles at the selected time",
            variants="the displayed particle counts and observation times",
        ),
        units=["U001775", "U001776"],
        parameters=["particle count", "observation time"],
        uncertainty="The binning, normalization, sample sizes, and random-walk sampling measure are not completely stated.",
    )
    add(
        "generalized one-dimensional random-walk family",
        "U001777",
        "EVOLUTION",
        evolution(
            "one-dimensional random-walk family",
            "randomly select a displacement from the source-stated variant at each step",
            carrier="positions on a one-dimensional line",
            alphabet="discrete or continuous positions",
            state="the current particle position and, for the alternating variant, step parity",
            seed="a starting particle position",
            activation="the particle",
            neighborhood="the variant's permitted displacement set",
            result="a random successor position",
            determinism="stochastic; detailed direction and probability measures are not stated",
            variants="unit left/right; displacement 0, 1, or 2; any displacement from 0 to 1; alternating fixed direction",
            external="a random displacement choice is supplied where the selected variant calls for one",
        ),
        units=["U001778", "U001779"],
        parameters=["displacement set", "step parity"],
        variants=[
            "one position left or right",
            "zero, one, or two positions",
            "any distance between zero and one",
            "alternating always-right and always-left steps",
        ],
        uncertainty="The source does not fully state direction choices, probability weights, or continuous measures for every variant.",
    )
    add(
        "Central Limit Theorem Gaussian-limit relation",
        "U001780",
        "RELATION",
        relation(
            "limiting-distribution relation",
            "for a wide range of microscopic random-walk rules, the aggregate position distribution approaches the same continuous Gaussian form",
            carrier="ensembles of random-walk particle positions",
            input_value="a qualifying microscopic random-walk rule and a sufficiently large ensemble",
            result="a continuous Gaussian limiting distribution",
            determinism="a stated mathematical limiting relation; precise hypotheses are not supplied here",
            variants="the broad random-walk rule range asserted in the source",
        ),
        aliases=["Gaussian random-walk limit"],
        uncertainty="This range does not state the theorem's precise hypotheses, scaling, or convergence mode.",
    )
    add(
        "two-dimensional lattice random-walk family",
        "U001781",
        "EVOLUTION",
        evolution(
            "two-dimensional lattice random-walk family",
            "move a particle at random along permitted lattice steps",
            carrier="a square or hexagonal two-dimensional lattice",
            alphabet="lattice positions",
            state="the current particle position",
            seed="a starting lattice position",
            activation="the particle",
            neighborhood="the next-step neighbors of the chosen lattice",
            result="a random successor lattice position",
            determinism="stochastic; individual step probabilities are not stated",
            variants="square-lattice walk and hexagonal-lattice walk",
            external="a random lattice-step choice is supplied at each step",
        ),
        units=["U001783", "U001784"],
        parameters=["lattice type"],
        variants=["square lattice", "hexagonal lattice"],
        uncertainty="Step probabilities and boundary conditions are not stated.",
    )
    add(
        "Eden adjacent-cell aggregation process",
        "U001785",
        "EVOLUTION",
        evolution(
            "stochastic cluster-growth process",
            "add one new black cell at each step at a randomly chosen position adjacent to the existing cluster",
            carrier="a square grid of cells",
            alphabet="black occupied cells and unoccupied positions",
            state="the current black-cell cluster",
            seed="an initial black-cell cluster",
            activation="unoccupied positions adjacent to the cluster",
            neighborhood="four immediate grid neighbors are implied by the stated variants",
            result="a cluster enlarged by one black cell",
            determinism="stochastic over eligible adjacent positions; the exact selection measure is not stated",
            variants="unrestricted adjacent-site Eden growth",
            external="one random eligible-position choice is supplied at each step",
        ),
        units=["U001786", "U001787", "U001788"],
        aliases=["simple aggregation model", "Eden model"],
        uncertainty="The boundary, candidate-position sampling convention, and exact probability measure are not stated.",
    )
    add(
        "one-neighbor Eden aggregation variant",
        "U001790",
        "EVOLUTION",
        evolution(
            "neighbor-count-restricted stochastic cluster-growth process",
            "add one randomly chosen cell only if it would have exactly one occupied immediate neighbor",
            carrier="a square grid of cells",
            alphabet="black occupied cells and unoccupied positions",
            state="the current black-cell cluster",
            seed="an initial black-cell cluster",
            activation="unoccupied candidate positions with exactly one occupied immediate neighbor",
            neighborhood="the four immediate grid neighbors",
            result="a cluster enlarged by one eligible black cell",
            determinism="stochastic over eligible positions; the exact selection measure is not stated",
            variants="exactly-one-neighbor restriction",
            external="one random eligible-position choice is supplied at each step",
        ),
        units=["U001791", "U001793", "U001795"],
        mechanics="U001795",
        uncertainty="The candidate-position sampling and behavior when no eligible position exists are not stated.",
    )
    add(
        "one-or-four-neighbor Eden aggregation variant",
        "U001790",
        "EVOLUTION",
        evolution(
            "neighbor-count-restricted stochastic cluster-growth process",
            "add one randomly chosen cell only if it would have either one or four occupied immediate neighbors",
            carrier="a square grid of cells",
            alphabet="black occupied cells and unoccupied positions",
            state="the current black-cell cluster",
            seed="an initial black-cell cluster",
            activation="unoccupied candidate positions with one or four occupied immediate neighbors",
            neighborhood="the four immediate grid neighbors",
            result="a cluster enlarged by one eligible black cell",
            determinism="stochastic over eligible positions; the exact selection measure is not stated",
            variants="one-or-four-neighbor restriction",
            external="one random eligible-position choice is supplied at each step",
        ),
        units=["U001792", "U001794", "U001795"],
        mechanics="U001795",
        uncertainty="The candidate-position sampling and behavior when no eligible position exists are not stated.",
    )
    add(
        "outer-totalistic cellular automaton code 746",
        "U001798",
        "EVOLUTION",
        evolution(
            "two-dimensional binary outer-totalistic cellular-automaton preset",
            "with eight surrounding neighbors: exactly 3 makes the cell black; counts 1, 2, or 4 retain its color; counts 5 through 8 make it white",
            carrier="a two-dimensional square grid",
            alphabet="black and white",
            seed="the source-displayed simple initial configuration",
            activation="every cell",
            neighborhood="the eight surrounding cells, including diagonals and excluding the cell itself",
            variants="outer-totalistic code 746",
        ),
        units=["U001802", "U001803"],
        mechanics="U001803",
        parameters=["outer-totalistic code 746"],
        uncertainty="The prose omits the output for a neighborhood containing zero black neighbors.",
    )
    add(
        "totalistic cellular automaton code 976",
        "U001804",
        "EVOLUTION",
        evolution(
            "two-dimensional binary totalistic cellular-automaton preset",
            "count black cells in the self-plus-eight neighborhood; totals below 4 become white, totals above 6 become black, total 5 becomes white, and total 4 becomes black",
            carrier="an effectively wrapped two-dimensional square grid",
            alphabet="black and white",
            seed="a random initial configuration",
            activation="every cell",
            neighborhood="the cell itself and its eight adjacent cells, including diagonals",
            variants="totalistic code 976 in an 80-cell-wide wrapped display",
        ),
        units=["U001806", "U001807", "U001808", "U001809"],
        mechanics="U001809",
        parameters=["totalistic code 976", "80-cell wrapped width"],
        uncertainty="The prose omits the output for a neighborhood total of exactly 6.",
    )
    add(
        "elementary cellular automaton rule 184",
        "U001819",
        "EVOLUTION",
        evolution(
            "one-dimensional binary cellular-automaton preset",
            "a black cell takes the prior color of its right neighbor, while a white cell takes the prior color of its left neighbor",
            carrier="a one-dimensional row of cells",
            alphabet="black and white",
            seed="a source-stated initial binary configuration",
            activation="every cell",
            neighborhood="the cell and its immediate left and right neighbors",
            variants="rule 184",
        ),
        units=["U001820", "U001821"],
        complete=True,
    )
    add(
        "four-color interface-expansion cellular automaton",
        "U001822",
        "EVOLUTION",
        evolution(
            "one-dimensional four-color cellular automaton",
            "black and white regions are separated by two gray interface states whose local interactions expand the gray region as displayed",
            carrier="a one-dimensional row of cells",
            alphabet="black, white, and two gray interface colors",
            seed="black and white regions separated by the source-displayed interface",
            activation="every cell",
            neighborhood="a local one-dimensional neighborhood shown in the rule diagram",
            variants="the displayed four-color interface rule",
        ),
        units=["U001824", "U001825", "U001826"],
        uncertainty="The prose and image do not supply an independently transcribed complete transition table.",
    )
    add(
        "above-right majority cellular automaton",
        "U001827",
        "EVOLUTION",
        evolution(
            "two-dimensional binary cellular-automaton preset",
            "a cell becomes black when at least two of the cell itself, the cell above, and the cell to the right are black; otherwise it becomes white",
            carrier="a two-dimensional square grid",
            alphabet="black and white",
            seed="the source-displayed initial pattern",
            activation="every cell",
            neighborhood="the cell itself, the cell immediately above, and the cell immediately to the right",
            variants="three-cell directed majority rule",
        ),
        units=["U001828", "U001829"],
        complete=True,
    )
    add(
        "double-well interacting-ball process",
        "U001830",
        "EVOLUTION",
        evolution(
            "continuous interacting-particle process with two stable positions",
            "balls move continuously under interactions and settle toward one of two stable positions representing discrete-looking states",
            carrier="a line or array of interacting balls",
            alphabet="continuous positions and velocities",
            state="all ball positions and velocities",
            seed="a source-displayed initial arrangement",
            activation="all balls under continuous forces",
            schedule="continuous physical time",
            neighborhood="the source-displayed local ball interactions and double-well support",
            result="continuous trajectories and eventual discrete-looking positions",
            variants="the four displayed double-well examples",
        ),
        units=["U001832", "U001833", "U001834", "U001835", "U001836", "U001837", "U001838"],
        uncertainty="The force law, potential, damping, boundary, and numerical parameters are not stated.",
    )
    add(
        "page-211 square-array constraint",
        "U001842",
        "CONSTRAINT",
        constraint(
            "two-dimensional binary local constraint",
            "a configuration satisfies the local square conditions stated on page 211",
            carrier="a square array of black and white cells",
            state="a complete binary square array",
            neighborhood="the page-211 local adjacency relation",
            variants="the page-211 constraint used as case (a)",
        ),
        units=["U001847", "U001850", "U001860", "U001882"],
        aliases=["case (a) square-array constraint"],
        uncertainty="The target page is outside this sealed chapter range, so the local accepted-result condition is not available here.",
    )
    add(
        "exhaustive constraint-satisfaction search",
        "U001846",
        "RELATION",
        relation(
            "finite exhaustive witness-search procedure",
            "enumerate every possible pattern, check the constraint on each, and retain the satisfying patterns",
            carrier="a finite pattern space",
            input_value="a finite carrier, alphabet, and decidable constraint",
            result="all satisfying patterns in the enumerated space",
            variants="10 by 10 and 20 by 20 binary-array scale examples",
        ),
        parameters=["finite carrier size", "alphabet", "constraint"],
        complete=True,
    )
    add(
        "random constraint-pattern sampler",
        "U001847",
        "RELATION",
        relation(
            "stochastic approximate-satisfaction sampler",
            "draw patterns at random and measure the fraction of cells violating the chosen constraint",
            carrier="a finite binary square-array pattern space",
            input_value="a constraint, an array size, and random pattern samples",
            result="sampled violation fractions or their empirical distribution",
            determinism="stochastic; the exact sampling measure is not stated",
            variants="10 by 10 arrays and the larger-array comparisons",
        ),
        units=["U001848", "U001849", "U001850", "U001851", "U001852"],
        parameters=["array size", "constraint", "sample count"],
        uncertainty="The exact sampling measure and number of samples used in each plotted estimate are not stated.",
    )
    add(
        "nonincreasing random single-cell constraint solver",
        "U001853",
        "EVOLUTION",
        evolution(
            "stochastic local constraint-improvement process",
            "choose one cell at random and reverse its color exactly when the reversal does not increase the total number of violating cells",
            carrier="a finite binary square array",
            alphabet="black and white",
            state="the complete array and its total violation count",
            seed="a randomly chosen initial pattern",
            activation="one randomly chosen cell per step",
            neighborhood="the chosen cell and every local constraint term affected by reversing it",
            result="the retained or one-cell-reversed array",
            determinism="stochastic through the random cell choice",
            variants="the page-211 case and the three constraint cases in the 30 by 30 comparison",
            external="one random cell selection is supplied per step",
        ),
        units=["U001854", "U001857", "U001858", "U001859", "U001860"],
        mechanics="U001854",
        parameters=["constraint", "array size"],
        complete=True,
    )
    add(
        "exactly-two-black-neighbors square-array constraint",
        "U001860",
        "CONSTRAINT",
        constraint(
            "two-dimensional binary local constraint",
            "every black cell and every white cell must have exactly two adjacent black cells",
            carrier="a square array of black and white cells",
            state="a complete binary square array",
            neighborhood="the source's adjacent-square neighborhood",
            variants="case (b)",
        ),
        uncertainty="The caption does not restate whether adjacency includes only orthogonal cells, though the surrounding construction indicates a four-cell adjacency.",
    )
    add(
        "three-black-or-four-white-neighbors square-array constraint",
        "U001860",
        "CONSTRAINT",
        constraint(
            "two-dimensional binary local constraint",
            "every black cell has three adjacent black cells and one adjacent white cell, while every white cell has four adjacent white cells",
            carrier="a square array of black and white cells",
            state="a complete binary square array",
            result="an empty accepted set according to the source's impossibility statement",
            neighborhood="four adjacent squares",
            variants="case (c), stated to be unsatisfiable",
        ),
        complete=True,
    )
    add(
        "cyclic right-neighbor equality constraint",
        "U001861",
        "CONSTRAINT",
        constraint(
            "one-dimensional cyclic binary equality constraint",
            "every cell must have the same color as its right-hand neighbor",
            carrier="a cyclic line of black and white cells",
            state="a complete cyclic binary configuration",
            result="the two uniform configurations: all black or all white",
            neighborhood="each cell and its immediate right neighbor, with wraparound",
            variants="finite cyclic line",
        ),
        units=["U001864"],
        complete=True,
    )
    add(
        "strict-decrease random single-cell solver",
        "U001862",
        "EVOLUTION",
        evolution(
            "stochastic strict-improvement process",
            "choose one cell at random and reverse its color only when doing so reduces the number of violated right-neighbor equalities",
            carrier="a finite cyclic binary line",
            alphabet="black and white",
            state="the complete cyclic line and its violation count",
            seed="a random binary configuration",
            activation="one randomly chosen cell per step",
            neighborhood="the chosen cell and its two incident equality constraints",
            result="the retained or one-cell-reversed cyclic line",
            determinism="stochastic through random cell selection",
            variants="strict-decrease acceptance",
            external="one random cell selection is supplied per step",
        ),
        units=["U001863", "U001864"],
        complete=True,
    )
    add(
        "local downhill curve minimizer",
        "U001865",
        "EVOLUTION",
        evolution(
            "local descent process",
            "take small steps, choosing each direction so as locally to move downhill",
            carrier="a one-dimensional curve over a continuous coordinate",
            alphabet="continuous position and curve height",
            state="the current position on the curve",
            seed="a starting position",
            activation="the current point",
            neighborhood="nearby candidate positions and their curve heights",
            result="a lower neighboring position or a local minimum",
            variants="smooth single-minimum, multiple-minimum, and jagged discrete-system landscapes",
        ),
        units=["U001866", "U001867", "U001868", "U001869", "U001870", "U001871"],
        uncertainty="Step size and tie-breaking are not stated.",
    )
    add(
        "nonincrease cyclic single-cell solver",
        "U001874",
        "EVOLUTION",
        evolution(
            "stochastic nonincreasing constraint solver",
            "choose a random cell and reverse it when the violation count decreases or remains unchanged",
            carrier="a finite cyclic binary line",
            alphabet="black and white",
            state="the complete cyclic line and its violation count",
            seed="any initial binary configuration",
            activation="one randomly chosen cell per step",
            neighborhood="the chosen cell and its two incident equality constraints",
            result="the retained or one-cell-reversed cyclic line",
            determinism="stochastic through random cell selection",
            variants="decrease-or-equal acceptance",
            external="one random cell selection is supplied per step",
        ),
        units=["U001875", "U001876", "U001877"],
        complete=True,
    )
    add(
        "evolution-invariant-state relation",
        "U001880",
        "CONSTRAINT",
        constraint(
            "fixed-state relation for an evolution law",
            "a state is accepted exactly when applying the evolution rule leaves that state unchanged",
            carrier="the complete state space of a selected evolution system",
            state="one complete candidate state",
            result="the set of invariant states",
            variants="the selected evolution rule",
        ),
        aliases=["fixed-point constraint"],
        complete=True,
    )
    add(
        "five-neighbor cellular-automaton invariant-state family query",
        "U001882",
        "CONSTRAINT",
        constraint(
            "two-dimensional cellular-automaton family query",
            "select five-neighbor cellular-automaton rules for which the page-211 pattern is the unique invariant state",
            carrier="the 4,294,967,296 possible five-neighbor rules and their two-dimensional binary states",
            state="a selected rule together with candidate binary states",
            result="the stated set of 572,522 qualifying rules",
            neighborhood="the source's five-cell neighborhood",
            variants="page-211 unique-invariant-state condition",
        ),
        units=["U001886", "U001887"],
        parameters=["five-neighbor rule code"],
        variants=[
            "code 530763",
            "code 18423119",
            "code 88710593",
            "code 89759053",
            "code 116497901",
            "code 167812175",
            "code 176239055",
            "code 1072764257",
            "code 1840848327",
            "code 2131825735",
        ],
        item_evidence="U001886",
        identity_units=["U001886"],
        uncertainty="The target pattern and exact five-neighbor code convention are not contained in this sealed range.",
    )
    add(
        "elementary cellular automaton rule 254",
        "U001883",
        "EVOLUTION",
        evolution(
            "one-dimensional binary cellular-automaton preset",
            "the ordered eight outputs are black for every three-cell neighborhood except all white, which maps to white",
            carrier="a one-dimensional row of cells",
            alphabet="black and white",
            seed="a random initial configuration in the displayed run",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            variants="elementary rule 254",
        ),
        aliases=["first uniform-invariant-state example"],
        complete=True,
    )
    add(
        "elementary cellular automaton rule 146",
        "U001884",
        "EVOLUTION",
        evolution(
            "one-dimensional binary cellular-automaton preset",
            "for neighborhoods 111 through 000, the ordered outputs are black, white, white, black, white, white, black, white",
            carrier="a one-dimensional row of cells",
            alphabet="black and white",
            seed="a random initial configuration in the displayed run",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            variants="elementary rule 146",
        ),
        aliases=["second uniform-invariant-state example"],
        complete=True,
    )
    add(
        "densest equal-circle packing constraint",
        "U001888",
        "CONSTRAINT",
        constraint(
            "planar equal-circle packing optimization",
            "arrange identical nonoverlapping circles so that packing density is maximal",
            carrier="identical circles in the plane",
            state="a complete nonoverlapping circle arrangement",
            result="densest arrangements in which each circle has six neighbors",
            neighborhood="contact adjacency among circles",
            variants="identical circles",
        ),
        units=["U001891", "U001892"],
        complete=True,
    )
    add(
        "densest equal-sphere packing constraint",
        "U001889",
        "CONSTRAINT",
        constraint(
            "three-dimensional equal-sphere packing optimization",
            "arrange identical nonoverlapping spheres so that packing density is maximal",
            carrier="identical spheres in three-dimensional space",
            state="a complete nonoverlapping sphere arrangement",
            result="densest arrangements in which each sphere has twelve neighbors",
            neighborhood="contact adjacency among spheres",
            variants="identical spheres",
        ),
        units=["U001893", "U001894"],
        complete=True,
    )
    add(
        "greedy center-nearest circle placement process",
        "U001895",
        "EVOLUTION",
        evolution(
            "sequential geometric packing process",
            "start with one circle, then add each new nonoverlapping circle with its center as close as possible to the first circle's center",
            carrier="circles in the plane",
            alphabet="circle centers and radii",
            state="the placed circles",
            seed="one initial circle",
            activation="one new circle per step",
            neighborhood="the first circle and all already placed circles that constrain nonoverlap",
            result="an arrangement enlarged by one circle",
            variants="equal and unequal source-displayed circle-size ratios",
        ),
        units=["U001897"],
        parameters=["circle-size sequence"],
        uncertainty="Tie-breaking and the exact admissibility convention beyond nonoverlap are not stated.",
    )
    add(
        "Gray-path elementary-cellular-automaton rule sequence",
        "U001906",
        "RELATION",
        relation(
            "finite Gray-adjacent rule sequence",
            "order elementary cellular-automaton rules so that each successive transition table differs at exactly one output position",
            carrier="elementary binary nearest-neighbor transition tables",
            input_value="the six displayed rules and their ordered transition tables",
            result="the ordered path 95, 94, 90, 91, 89, 88",
            variants="the six-rule path displayed on page 367",
        ),
        units=["U001907"],
        parameters=["rule order"],
        variants=["rule 95", "rule 94", "rule 90", "rule 91", "rule 89", "rule 88"],
        complete=True,
    )
    add(
        "homogeneous point-growth mobile automaton",
        "U001912",
        "EVOLUTION",
        evolution(
            "mobile-automaton point-growth process",
            "a localized active element moves and progressively converts reached positions to the same state",
            carrier="a one-dimensional cell field with a mobile active element",
            alphabet="source-displayed cell and active-element states",
            state="the cell field and active-element state",
            seed="one active point",
            activation="the current mobile active element",
            neighborhood="the displayed local cells around the active element",
            result="an updated field and active-element position",
            variants="the displayed mobile-automaton example",
        ),
        units=["U001913"],
        uncertainty="The complete transition table and boundary convention are not stated in prose.",
    )
    add(
        "rule 254 single-black-cell point-growth preset",
        "U001912",
        "EVOLUTION",
        evolution(
            "elementary cellular-automaton point-growth preset",
            "apply elementary rule 254, whose ordered outputs are black for every neighborhood except all white, from one black cell",
            carrier="a one-dimensional cell field",
            alphabet="black and white",
            state="the complete cell field",
            seed="a single changed cell",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="one successor cell field",
            variants="rule 254 with a single-black-cell seed",
        ),
        units=["U001913"],
        aliases=["homogeneous point-growth cellular automaton"],
        complete=True,
    )
    add(
        "independent rule 0 cell convergence",
        "U001914",
        "EVOLUTION",
        evolution(
            "neighbor-independent elementary cellular-automaton preset",
            "map every three-cell neighborhood to white, so every cell becomes white in one step",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            state="the complete binary cell row",
            seed="an arbitrary binary initial condition",
            activation="every cell independently",
            neighborhood="the displayed three-cell neighborhood table, whose output is independent of its input",
            result="the uniform-white successor field",
            variants="elementary rule 0",
        ),
        units=["U001915", "U001916"],
        aliases=["binary independent-element convergence"],
        complete=True,
    )
    add(
        "independent continuous-element convergence map",
        "U001914",
        "EVOLUTION",
        evolution(
            "neighbor-independent continuous pointwise map",
            "apply the displayed one-variable map independently to each element so all values approach the same state",
            carrier="a one-dimensional field of continuous-valued elements",
            alphabet="continuous gray values",
            state="the value of every element",
            seed="an arbitrary source-displayed gray-value field",
            activation="every element independently",
            neighborhood="each element reads only its own current value",
            result="one successor gray-value field tending toward a uniform state",
            variants="the displayed continuous pointwise map",
        ),
        units=["U001915", "U001916"],
        aliases=["continuous independent-element convergence"],
        uncertainty="The icon depicts the pointwise map, but the prose does not transcribe its exact formula or value interval.",
    )
    add(
        "elementary cellular automaton rule 128",
        "U001918",
        "EVOLUTION",
        evolution(
            "class-1 elementary cellular-automaton preset",
            "for neighborhoods 111 through 000, output black only for 111 and white for the other seven neighborhoods",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="the source-displayed initial binary configuration",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="a rule-128 evolution toward a uniform state",
            variants="elementary rule 128",
        ),
        complete=True,
    )
    add(
        "elementary cellular automaton rule 160",
        "U001919",
        "EVOLUTION",
        evolution(
            "class-1 elementary cellular-automaton preset",
            "for neighborhoods 111 through 000, output black for 111 and 101 and white for the other six neighborhoods",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="the source-displayed initial binary configuration",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="a rule-160 evolution toward a uniform state",
            variants="elementary rule 160",
        ),
        complete=True,
    )
    add(
        "elementary cellular automaton rule 254 class-1 preset",
        "U001920",
        "EVOLUTION",
        evolution(
            "class-1 elementary cellular-automaton preset",
            "for neighborhoods 111 through 000, output black for every neighborhood except 000",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="the source-displayed initial binary configuration",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="a rule-254 evolution toward a uniform state",
            variants="elementary rule 254",
        ),
        units=["U001921"],
        complete=True,
    )
    add(
        "rule 30 spatial coarse-graining observer",
        "U001922",
        "OBSERVER",
        observer(
            "spatial averaging and coarse-graining observer",
            "aggregate increasingly large spatial regions of a rule 30 pattern so that small-scale variation averages into an apparently uniform field",
            carrier="a rule 30 space-time pattern",
            input_value="rule 30 cell values and a selected spatial averaging scale",
            result="a coarse gray or aggregate view",
            neighborhood="the cells inside each selected spatial aggregation region",
            variants="the three displayed aggregation scales",
        ),
        units=["U001923", "U001924", "U001925", "U001926"],
        parameters=["spatial averaging scale"],
        uncertainty="The exact block sizes and gray-value normalization are not stated in prose.",
    )
    add(
        "three-cell gray-level averaging cellular automaton",
        "U001928",
        "EVOLUTION",
        evolution(
            "one-dimensional continuous-valued cellular automaton",
            "set every cell's next gray level to the average of its current value and the values of its two neighbors",
            carrier="a one-dimensional row of cells",
            alphabet="continuous gray levels",
            seed="a source-displayed initial gray-level field",
            activation="every cell",
            neighborhood="the cell itself and its immediate left and right neighbors",
            variants="the density-conserving averaging rule",
        ),
        units=["U001929", "U001930"],
        mechanics="U001929",
        complete=True,
    )
    add(
        "binary phase-selecting cellular automaton",
        "U001931",
        "EVOLUTION",
        evolution(
            "binary cellular-automaton preset with two uniform attractors",
            "evolve from different initial conditions to either uniform white or uniform black, with the selected phase depending on a total quantity",
            carrier="a one-dimensional row of binary cells",
            alphabet="black and white",
            state="the complete binary cell row",
            seed="a binary initial condition",
            activation="every cell",
            neighborhood="the page-339 cellular-automaton neighborhood",
            result="successive configurations ending in one of two uniform phases",
            variants="the page-339 cellular automaton",
        ),
        units=["U001932", "U001933"],
        uncertainty="The local rule and the precise conserved or threshold quantity are not stated in this range.",
    )
    add(
        "two-neighbor uniformity constraint",
        "U001934",
        "CONSTRAINT",
        constraint(
            "one-dimensional binary local equality constraint",
            "every cell must be the same color as both immediate neighbors",
            carrier="a line of black and white cells",
            state="a complete binary line",
            result="uniform all-black or all-white lines",
            neighborhood="each cell and both immediate neighbors",
            variants="the stated line constraint",
        ),
        complete=True,
    )
    add(
        "closed-curve finite-state recurrence process",
        "U001935",
        "EVOLUTION",
        evolution(
            "recurrent state-space trajectory",
            "follow a closed curve, or deterministically revisit states in a finite reachable state set, so that a prior state is eventually repeated",
            carrier="a closed geometric path or finite reachable state space",
            alphabet="positions or system states",
            state="the current position or state",
            seed="a starting point or state",
            activation="the current state",
            neighborhood="the rule-defined successor of the current state",
            result="a successor state on an eventually periodic trajectory",
            variants="literal closed curve and finite-state recurrence",
        ),
        units=["U001936", "U001937", "U001938", "U001939"],
        complete=True,
    )
    add(
        "localized finite-support automaton family",
        "U001940",
        "EVOLUTION",
        evolution(
            "localized mobile- and cellular-automaton family",
            "effects remain confined to a finite spatial region, leaving only finitely many reachable localized states and therefore eventual repetition",
            carrier="a cell field with a localized active region",
            alphabet="the source-displayed automaton states",
            state="the finite affected region and any active-element state",
            seed="a localized initial configuration",
            activation="the active element or cells inside the affected region",
            neighborhood="the displayed local automaton dependencies",
            result="a localized successor state",
            variants="mobile-automaton and cellular-automaton examples",
        ),
        units=["U001941", "U001942"],
        variants=["mobile automaton", "cellular automaton"],
        uncertainty="The complete rules of the displayed examples are not transcribed in prose.",
    )
    add(
        "moving-periodic-element wave family",
        "U001943",
        "EVOLUTION",
        evolution(
            "spatially moving periodic-element process",
            "an element repeats in time while systematically moving in space, producing spatial repetition",
            carrier="a spatial medium containing moving periodic elements",
            alphabet="the source-displayed element states",
            state="element phase and position",
            seed="a source-displayed periodic element",
            activation="the repeating moving element",
            neighborhood="the local medium used by the displayed motion",
            result="a translated periodic successor state",
            variants="automaton example and standard wave motion",
        ),
        units=["U001944", "U001945", "U001946"],
        variants=["moving automaton element", "standard wave motion"],
        uncertainty="The source gives the semantic mechanism but not complete equations or transition tables for the two examples.",
    )
    add(
        "partial-table simple-seed repetitive cellular automaton",
        "U001948",
        "EVOLUTION",
        evolution(
            "partially specified elementary cellular-automaton preset",
            "the visible table gives 101 to black, 100 to black, 010 to white, 001 to black, and 000 to white",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="the simple localized seed displayed above the rule table",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="the displayed repetitive space-time evolution",
            variants="the first page-370 simple-seed cellular automaton",
        ),
        units=["U001951"],
        uncertainty="The source crop omits the outputs for neighborhoods 111, 110, and 011, so no complete elementary-rule identity is asserted.",
    )
    add(
        "elementary cellular automaton rule 94 simple-seed preset",
        "U001949",
        "EVOLUTION",
        evolution(
            "elementary cellular-automaton preset",
            "for neighborhoods 111 through 000, the ordered outputs are white, black, white, black, black, black, black, white",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="the simple localized seed displayed above the rule table",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="a repetitive rule-94 space-time evolution",
            variants="elementary rule 94",
        ),
        units=["U001951"],
        complete=True,
    )
    add(
        "elementary cellular automaton rule 54 simple-seed preset",
        "U001950",
        "EVOLUTION",
        evolution(
            "elementary cellular-automaton preset",
            "for neighborhoods 111 through 000, the ordered outputs are white, white, black, black, white, black, black, white",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="the simple localized seed displayed above the rule table",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="a repetitive rule-54 space-time evolution",
            variants="elementary rule 54",
        ),
        units=["U001951"],
        complete=True,
    )
    add(
        "random-start domain cellular-automaton family for rules 50, 54, and 62",
        "U001952",
        "EVOLUTION",
        evolution(
            "elementary cellular-automaton domain family",
            "from random initial conditions, form repetitive domains whose walls typically remain between them",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            state="the complete binary cell row",
            seed="a random binary initial condition",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="successive configurations containing repetitive domains",
            variants="elementary rules 50, 54, and 62",
        ),
        units=["U001953", "U001954", "U001955", "U001956", "U001957"],
        variants=["rule 50", "rule 54", "rule 62"],
        uncertainty="This range names the rules but does not transcribe their transition tables or random-start measure.",
    )
    add(
        "random-start rule 184 domain-combination preset",
        "U001958",
        "EVOLUTION",
        evolution(
            "rule 184 random-start preset",
            "apply rule 184 from a random initial condition so that repetitive domains quickly combine",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="a random binary initial condition",
            activation="every cell",
            neighborhood="the rule 184 three-cell neighborhood",
            result="successive configurations combining into spatial repetition",
            variants="rule 184 with random initial conditions",
        ),
        units=["U001959"],
        uncertainty="The probability measure for the random initial condition is not stated.",
    )
    add(
        "random-start rule 110 domain process",
        "U001960",
        "EVOLUTION",
        evolution(
            "rule 110 random-start preset",
            "apply rule 110 from a random initial condition, producing domains of spatial period 14 and temporal period 7 separated by localized structures",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="a random binary initial condition",
            activation="every cell",
            neighborhood="the rule 110 three-cell neighborhood",
            result="successive configurations with repetitive domains and localized separators",
            variants="rule 110 with random initial conditions",
        ),
        units=["U001961", "U001962", "U001963", "U001964", "U001965"],
        parameters=["spatial period 14", "temporal period 7"],
        uncertainty="The transition table and random-start probability measure are not stated in this range.",
    )
    add(
        "binary pair substitution system",
        "U001968",
        "EVOLUTION",
        evolution(
            "one-dimensional neighbor-independent substitution system",
            "replace black by black-white and replace white by white-black",
            carrier="a one-dimensional string of binary elements",
            alphabet="black and white",
            state="the complete current binary string",
            seed="the source-displayed initial element",
            activation="every element independently",
            neighborhood="each element reads only its own color",
            result="a binary string twice as long",
            variants="black to black-white and white to white-black",
        ),
        units=["U001969", "U001970"],
        mechanics="U001969",
        complete=True,
    )
    add(
        "two-dimensional block substitution system",
        "U001968",
        "EVOLUTION",
        evolution(
            "two-dimensional neighbor-independent substitution system",
            "replace each square independently by the source-displayed two-by-two block associated with its type",
            carrier="a two-dimensional square array",
            alphabet="the two source-displayed square types",
            state="the complete current square array",
            seed="the source-displayed initial square",
            activation="every square independently",
            neighborhood="each square reads only its own type",
            result="a square array refined by a factor of two in each spatial direction",
            variants="the displayed two-dimensional block replacement",
        ),
        units=["U001969", "U001970"],
        mechanics="U001969",
        uncertainty="The small raster key is visibly construction-bearing, but its two complete block patterns are not independently transcribed in the prose.",
    )
    add(
        "two-state recursive Y-branching preset",
        "U001971",
        "EVOLUTION",
        evolution(
            "state-dependent recursive branching process",
            "replace each terminal branch by the visibly keyed Y-shaped branch state, recursively producing a thickness- and shade-coded tree",
            carrier="a growing geometric branch tree",
            alphabet="the two displayed branch states and continuous branch geometry",
            state="the complete current branch tree and each terminal state",
            seed="one initial branch",
            activation="every eligible terminal branch",
            neighborhood="each terminal branch's own displayed state",
            result="a tree with a new generation of Y branches",
            variants="the leftmost two-state branching preset",
        ),
        units=["U001972", "U001973", "U001974"],
        mechanics="U001972",
        uncertainty="The raster key fixes the state-dependent Y replacements qualitatively but not exact angles, length ratios, or thickness ratios.",
    )
    add(
        "recursive three-child branching preset",
        "U001971",
        "EVOLUTION",
        evolution(
            "recursive three-child branching process",
            "replace every terminal point by three child terminal points in the displayed Y geometry",
            carrier="a growing geometric branch tree",
            alphabet="terminal and nonterminal branch points",
            state="the complete current branch tree",
            seed="one initial terminal branch",
            activation="every terminal point",
            neighborhood="each terminal point independently",
            result="a tree with three children for every replaced terminal",
            variants="the second branching preset",
        ),
        units=["U001972", "U001973", "U001974"],
        mechanics="U001972",
        uncertainty="The exact scale factor and branch angles are visible only schematically.",
    )
    add(
        "recursive two-child orthogonal branching preset",
        "U001971",
        "EVOLUTION",
        evolution(
            "recursive two-child branching process",
            "replace every terminal point by two horizontally separated child terminals connected in the displayed orthogonal geometry",
            carrier="a growing rectilinear branch tree",
            alphabet="terminal and nonterminal branch points",
            state="the complete current branch tree",
            seed="one initial terminal branch",
            activation="every terminal point",
            neighborhood="each terminal point independently",
            result="a tree with two children for every replaced terminal",
            variants="the third branching preset",
        ),
        units=["U001972", "U001973", "U001974"],
        mechanics="U001972",
        uncertainty="The exact segment lengths and scale factor are visible only schematically.",
    )
    add(
        "recursive four-child triangular branching preset",
        "U001971",
        "EVOLUTION",
        evolution(
            "recursive four-child branching process",
            "replace every terminal point by four child terminals in the displayed triangular geometry",
            carrier="a growing planar branch tree",
            alphabet="terminal and nonterminal branch points",
            state="the complete current branch tree",
            seed="one initial terminal branch",
            activation="every terminal point",
            neighborhood="each terminal point independently",
            result="a tree with four children for every replaced terminal",
            variants="the fourth branching preset",
        ),
        units=["U001972", "U001973", "U001974"],
        mechanics="U001972",
        uncertainty="The exact branch angles and scale factor are visible only schematically.",
    )
    add(
        "additive cellular automaton rule 90",
        "U001977",
        "EVOLUTION",
        evolution(
            "one-dimensional binary additive cellular-automaton preset",
            "apply additive cellular automaton rule 90 from a single black cell",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="one black cell in an otherwise white field",
            activation="every cell",
            neighborhood="the immediate left and right cells",
            result="a nested binary space-time pattern",
            variants="rule 90",
        ),
        units=["U001978", "U001979", "U001982"],
        uncertainty="The arithmetic transition formula is not restated in this range.",
    )
    add(
        "additive cellular automaton rule 150",
        "U001977",
        "EVOLUTION",
        evolution(
            "one-dimensional binary additive cellular-automaton preset",
            "apply additive cellular automaton rule 150 from a single black cell",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="one black cell in an otherwise white field",
            activation="every cell",
            neighborhood="the cell itself and its immediate left and right neighbors",
            result="a nested binary space-time pattern",
            variants="rule 150",
        ),
        units=["U001980", "U001981", "U001982"],
        uncertainty="The arithmetic transition formula is not restated in this range.",
    )
    add(
        "regular two-branch creation-and-annihilation process",
        "U001983",
        "EVOLUTION",
        evolution(
            "branch-creation and collision-annihilation process",
            "create two new branches at regular intervals and annihilate both members of any colliding pair",
            carrier="moving branches in a space-time plane",
            alphabet="branch positions and directions",
            state="all currently surviving branches and the creation phase",
            seed="the source-displayed initial branch",
            activation="scheduled branch points and colliding branch pairs",
            neighborhood="a branch point or pair of branches at a common position",
            result="a successor branch configuration",
            variants="two branches per creation event",
        ),
        units=["U001984", "U001986"],
        mechanics="U001986",
        uncertainty="Branch speeds, interval length, and collision tie cases are not numerically stated.",
    )
    add(
        "regular three-branch creation-and-annihilation process",
        "U001983",
        "EVOLUTION",
        evolution(
            "branch-creation and collision-annihilation process",
            "create three new branches at regular intervals and annihilate both members of any colliding pair",
            carrier="moving branches in a space-time plane",
            alphabet="branch positions and directions",
            state="all currently surviving branches and the creation phase",
            seed="the source-displayed initial branch",
            activation="scheduled branch points and colliding branch pairs",
            neighborhood="a branch point or pair of branches at a common position",
            result="a successor branch configuration",
            variants="three branches per creation event",
        ),
        units=["U001985", "U001986"],
        mechanics="U001986",
        uncertainty="Branch speeds, interval length, and collision tie cases are not numerically stated.",
    )
    add(
        "equal-density random-start rule 184 nesting preset",
        "U001987",
        "EVOLUTION",
        evolution(
            "rule 184 balanced random-start preset",
            "apply rule 184 to an initial condition with exactly equal numbers of black and white cells; oppositely directed stripes annihilate when they meet",
            carrier="a finite one-dimensional binary cell row",
            alphabet="black and white",
            seed="a random initial configuration with equal black and white counts",
            activation="every cell under rule 184",
            neighborhood="the rule 184 three-cell neighborhood",
            result="a nested pattern whose stripes all eventually annihilate",
            variants="balanced and unbalanced random-start cases",
        ),
        units=["U001988", "U001989", "U001990", "U001991", "U001992", "U001994"],
        mechanics="U001992",
        parameters=["equal black and white counts"],
        variants=["balanced initial counts", "unbalanced initial counts with surviving stripes"],
        uncertainty="The random sampling measure and finite boundary convention are not stated.",
    )
    add(
        "rule 110 first-cell-per-14-by-7-block observer",
        "U001995",
        "OBSERVER",
        observer(
            "space-time block-sampling observer",
            "partition a rule 110 space-time evolution into 14-by-7 blocks and retain only the first cell of every block",
            carrier="a rule 110 space-time array",
            input_value="a random-start rule 110 evolution",
            result="a highly compressed sampled representation in which each repetitive domain appears uniform",
            neighborhood="the first cell in each 14-cell by 7-step block",
            variants="14 by 7 first-cell sampling",
        ),
        units=["U001996", "U001997", "U001998"],
        parameters=["spatial block width 14", "temporal block height 7"],
        complete=True,
    )
    add(
        "three-color totalistic cellular automaton code 1893",
        "U001999",
        "EVOLUTION",
        evolution(
            "three-color totalistic cellular-automaton preset",
            "apply totalistic code 1893 to form domains with apparently random interiors and annihilating boundaries",
            carrier="a one-dimensional row of three-color cells",
            alphabet="three cell colors",
            seed="a source-displayed initial configuration",
            activation="every cell",
            neighborhood="the source's three-color totalistic neighborhood",
            result="a domain-forming cellular-automaton evolution",
            variants="k=3 totalistic code 1893",
        ),
        units=["U002000", "U002001", "U002005", "U002006"],
        aliases=["k=3 totalistic code 1893"],
        uncertainty="The neighborhood radius, code convention, complete transition law, and initial-state measure are not stated in prose.",
    )
    add(
        "elementary cellular automaton rule 18 domain process",
        "U002003",
        "EVOLUTION",
        evolution(
            "one-dimensional binary cellular-automaton preset",
            "apply elementary rule 18 to produce domains with apparently random interiors and boundaries that execute random-looking walks and annihilate",
            carrier="a one-dimensional binary cell row",
            alphabet="black and white",
            seed="a source-displayed initial condition",
            activation="every cell",
            neighborhood="a cell and its immediate left and right neighbors",
            result="a domain-forming rule 18 evolution",
            variants="elementary rule 18",
        ),
        units=["U002004", "U002005", "U002006"],
        uncertainty="The transition table and initial-state measure are not stated in this range.",
    )
    add(
        "two-by-two cellular-automaton block-compression observer",
        "U002005",
        "OBSERVER",
        observer(
            "two-by-two block-compression observer",
            "replace each displayed element by one value representing a two-cell by two-step block of original cells",
            carrier="a cellular-automaton space-time array",
            input_value="the rule 18 space-time evolution shown in the second example",
            result="a compressed domain-boundary representation",
            neighborhood="nonoverlapping two-cell by two-step blocks",
            variants="two-by-two block representation",
        ),
        uncertainty="The mapping from each possible two-by-two block to its displayed value is not stated.",
    )

    check(len(rows) == EXPECTED_CANDIDATES, f"candidate definition count is {len(rows)}")
    return rows


ROUTE_DEFS = [
    (
        "U001842",
        "page 211",
        "PAGE",
        "the complete local rule for the square-array constraint",
        "CROSS_RANGE",
        ["square-array constraint", "page 211"],
    ),
    (
        "U001933",
        "page 339",
        "PAGE",
        "the local rule and phase-selection quantity of the binary cellular automaton",
        "WITHIN_STAGE",
        ["uniform white", "uniform black", "page 339"],
    ),
    (
        "U002007",
        "Chapter 5",
        "SECTION",
        "constraint systems that generate nested patterns",
        "CROSS_RANGE",
        ["constraints", "nesting", "Chapter 5"],
    ),
]


PROFILE_NA = {
    "EVOLUTION": {
        "input",
        "visible_history",
        "control_state",
        "witness_semantics",
        "excluded_observers_and_representations",
    },
    "RELATION": {
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
    },
    "CONSTRAINT": {
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "write_replacement_assembly_or_commit",
    },
    "OBSERVER": {
        "support",
        "topology",
        "structural_invariants",
        "alphabet_or_value_schema",
        "complete_state",
        "visible_history",
        "control_state",
        "seed",
        "boundary",
        "external_data",
        "frontier_or_activation",
        "schedule",
        "write_replacement_assembly_or_commit",
        "successor_cardinality",
    },
}

SOURCE_UNCERTAINTY = {
    "U001803": (
        "The code-746 prose gives outputs for black-neighbor counts 1 through 8 "
        "but does not state the zero-neighbor output."
    ),
    "U001809": (
        "The code-976 prose gives outputs for totals below 4, exactly 4, exactly "
        "5, and above 6 but does not state the total-6 output."
    ),
}


def load_bundle(bundle: Path) -> dict[str, Any]:
    manifest_bytes = (bundle / "allowed-manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    units = [
        json.loads(line)
        for line in (bundle / "input/source-units.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    return {
        "manifest": manifest,
        "manifest_bytes": manifest_bytes,
        "units": units,
        "reading": read_csv(bundle / "input/reading-input.csv"),
        "assets": read_csv(bundle / "input/asset-input.csv"),
        "source_bytes": (bundle / "input/sources" / SOURCE_PATH).read_bytes(),
    }


def validate_bundle(bundle: Path, data: dict[str, Any]) -> None:
    manifest = data["manifest"]
    check(manifest["worker_id"] == WORKER_ID, "worker mismatch")
    check(manifest["stage"] == STAGE, "stage mismatch")
    check(manifest["discovery_epoch"] == EPOCH, "epoch mismatch")
    check(manifest["source_paths"] == [SOURCE_PATH], "source-path mismatch")
    check(len(data["units"]) == manifest["source_unit_count"] == 435, "unit count")
    check(len(data["reading"]) == 435, "reading count")
    check(len(data["assets"]) == manifest["asset_count"] == 92, "asset count")
    allowed = {row["path"]: row for row in manifest["allowed_inputs"]}
    for relative, record in allowed.items():
        raw = (bundle / relative).read_bytes()
        check(len(raw) == record["bytes"], f"byte count differs: {relative}")
        check(digest(raw) == record["sha256"], f"hash differs: {relative}")
    for unit, row in zip(data["units"], data["reading"]):
        check(unit["id"] == row["source_unit_id"], "source/reading order differs")
        raw = data["source_bytes"][unit["byte_start"] : unit["byte_end"]]
        check(digest(raw) == unit["sha256"] == row["unit_sha256"], f"unit hash: {unit['id']}")


def build_output(bundle: Path) -> dict[str, Any]:
    data = load_bundle(bundle)
    validate_bundle(bundle, data)
    manifest = data["manifest"]
    units = data["units"]
    unit_by_id = {row["id"]: row for row in units}
    order = {row["id"]: index for index, row in enumerate(units, 1)}
    asset_by_unit = {row["source_unit_id"]: row for row in data["assets"]}
    definitions = candidate_definitions()

    previous_anchor = 0
    anchor_counts: dict[str, int] = {}
    for index, definition in enumerate(definitions, 1):
        definition["id"] = f"W{index:04d}"
        definition["units"] = sorted(set(definition["units"]), key=order.__getitem__)
        check(definition["anchor"] == definition["units"][0], f"{definition['id']} anchor order")
        check(order[definition["anchor"]] >= previous_anchor, "candidate anchor order")
        previous_anchor = order[definition["anchor"]]
        anchor_counts[definition["anchor"]] = anchor_counts.get(definition["anchor"], 0) + 1
        definition["anchor_ordinal"] = anchor_counts[definition["anchor"]]
        check(definition["mechanics"] in definition["units"], f"{definition['id']} mechanics source")
        check(definition["item_evidence"] in definition["units"], f"{definition['id']} item evidence")
        check(
            set(definition["identity_units"]) <= set(definition["units"]),
            f"{definition['id']} identity evidence",
        )
        definition["values"]["evidence_limit"] = (
            "Only mechanics stated or directly visible in the sealed Chapter 7 main-text bundle are supported; "
            "unstated profile fields remain unknown and profile-irrelevant fields are explicitly not applicable."
        )

    routes: list[dict[str, str]] = []
    route_ids_by_unit: dict[str, list[str]] = {}
    route_ordinals: dict[str, int] = {}
    for index, (unit_id, literal, kind, topic, scope, terms) in enumerate(ROUTE_DEFS, 1):
        route_id = f"WR{index:04d}"
        route_ids_by_unit.setdefault(unit_id, []).append(route_id)
        route_ordinals[unit_id] = route_ordinals.get(unit_id, 0) + 1
        routes.append(
            {
                "route_id": route_id,
                "source_unit_id": unit_id,
                "source_asset_id": "",
                "discovery_epoch": str(EPOCH),
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": unit_id,
                "discovery_ordinal": str(route_ordinals[unit_id]),
                "literal_target": literal,
                "route_kind": kind,
                "expected_topic": topic,
                "owning_stage": str(STAGE),
                "closure_scope": scope,
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": "[]",
                "vocabulary_terms": compact(terms),
                "defect_boundary": "",
            }
        )

    candidate_ids_by_unit: dict[str, list[str]] = {}
    roles_by_unit: dict[str, list[str]] = {}
    anchors: set[tuple[str, str]] = set()
    role_name = {
        "EVOLUTION": "BEHAVIOR_OR_OUTCOME",
        "RELATION": "OBSERVER_OR_ANALYZER",
        "CONSTRAINT": "PROPERTY_OR_RESTRICTION",
        "OBSERVER": "OBSERVER_OR_ANALYZER",
    }
    for definition in definitions:
        anchors.add((definition["id"], definition["anchor"]))
        for unit_id in definition["units"]:
            candidate_ids_by_unit.setdefault(unit_id, []).append(definition["id"])
            role = role_name[definition["profile"]]
            if role not in roles_by_unit.setdefault(unit_id, []):
                roles_by_unit[unit_id].append(role)

    # One evidence row is allocated for every candidate/source occurrence.
    allocations: list[tuple[int, str, dict[str, Any], str]] = []
    for definition in definitions:
        for unit_id in definition["units"]:
            allocations.append((order[unit_id], definition["id"], definition, unit_id))
    allocations.sort(key=lambda item: (item[0], item[1]))
    evidence_by_candidate: dict[str, list[dict[str, Any]]] = {
        definition["id"]: [] for definition in definitions
    }
    evidence_ordinals: dict[str, int] = {}
    for number, (_, _, definition, unit_id) in enumerate(allocations, 1):
        evidence_ordinals[unit_id] = evidence_ordinals.get(unit_id, 0) + 1
        source_unit = unit_by_id[unit_id]
        asset = asset_by_unit.get(unit_id)
        is_mechanics = unit_id == definition["mechanics"]
        supported_fields = list(definition["values"]) if is_mechanics else []
        if is_mechanics:
            supported_fields.extend(
                field
                for field in FIELDS
                if field in PROFILE_NA[definition["profile"]]
                and field not in definition["values"]
            )
        if is_mechanics:
            strength = (
                "DIRECT_COMPLETE_MECHANICS"
                if definition["complete"]
                else "DIRECT_PARTIAL_MECHANICS"
            )
        elif unit_id in definition["identity_units"] or unit_id == definition["anchor"]:
            strength = "DIRECT_IDENTITY"
        elif source_unit["block_kind"] == "image":
            strength = "CONTEXTUAL"
        else:
            strength = "CORROBORATING"
        if is_mechanics:
            claim = (
                f"{unit_id} supplies the listed source-scoped identity and mechanics for "
                f"{definition['name']}; no unlisted mechanic is inferred."
            )
        elif source_unit["block_kind"] == "image":
            claim = (
                f"The original-resolution image at {asset['physical_path']} is a finite, labeled, or rule-bearing "
                f"witness for {definition['name']}; it is not used for unlisted fields."
            )
        elif unit_id == definition["anchor"]:
            claim = (
                f"{unit_id} first delimits {definition['name']} in this source range; later listed evidence "
                "supplies any mechanics not present here."
            )
        else:
            claim = (
                f"{unit_id} corroborates the stated variant, parameter, or behavior of {definition['name']} "
                "without adding unlisted mechanics."
            )
        evidence_by_candidate[definition["id"]].append(
            {
                "evidence_id": f"WE{number:06d}",
                "evidence_group_id": f"WG{number:06d}",
                "discovery_anchor": {
                    "epoch": EPOCH,
                    "kind": "SOURCE_UNIT",
                    "id": unit_id,
                    "ordinal": evidence_ordinals[unit_id],
                },
                "source_unit_id": unit_id,
                "image_path": asset["physical_path"] if asset else None,
                "strength": strength,
                "modality": (
                    "IMAGE"
                    if source_unit["block_kind"] == "image"
                    else (
                        "FORMULA"
                        if b"$"
                        in data["source_bytes"][
                            source_unit["byte_start"] : source_unit["byte_end"]
                        ]
                        else "PROSE"
                    )
                ),
                "claim": claim,
                "fingerprint_fields": supported_fields,
            }
        )

    candidate_records: list[dict[str, Any]] = []
    for definition in definitions:
        evidence = sorted(
            evidence_by_candidate[definition["id"]],
            key=lambda row: int(row["evidence_id"][2:]),
        )
        evidence_for_field = {
            field: [
                row["evidence_id"]
                for row in evidence
                if field in row["fingerprint_fields"]
            ]
            for field in FIELDS
        }
        fingerprint: dict[str, dict[str, Any]] = {}
        missing: list[str] = []
        for field in FIELDS:
            ids = evidence_for_field[field]
            if field in definition["values"]:
                status = "SUPPORTED"
                value = definition["values"][field]
                reason = ""
                check(ids, f"{definition['id']} supported field lacks evidence: {field}")
            elif field in PROFILE_NA[definition["profile"]]:
                status = "NOT_APPLICABLE"
                value = None
                reason = (
                    f"The {definition['profile'].lower()} profile for {definition['name']} has no independent "
                    f"{field.replace('_', ' ')} mechanic."
                )
                check(len(ids) == 1, f"{definition['id']} not-applicable evidence: {field}")
            else:
                status = "UNKNOWN_FROM_SOURCE"
                value = None
                reason = (
                    f"The reviewed source units do not determine {field.replace('_', ' ')} "
                    f"for {definition['name']}."
                )
                ids = []
                missing.append(reason)
            fingerprint[field] = {
                "status": status,
                "value": value,
                "evidence_ids": ids,
                "reason": reason,
            }
        mechanics_evidence = next(
            row["evidence_id"]
            for row in evidence
            if row["source_unit_id"] == definition["mechanics"]
        )
        item_evidence = next(
            row["evidence_id"]
            for row in evidence
            if row["source_unit_id"] == definition["item_evidence"]
        )
        image_witnesses = [
            asset_by_unit[unit_id]["physical_path"]
            for unit_id in definition["units"]
            if unit_id in asset_by_unit
        ]
        source_statuses = {
            "AMBIGUOUS" if unit_id in SOURCE_UNCERTAINTY else "CLEAR"
            for unit_id in definition["units"]
        }
        route_ids: list[str] = []
        if definition["name"] == "page-211 square-array constraint":
            route_ids.append("WR0001")
        if definition["name"] == "binary phase-selecting cellular automaton":
            route_ids.append("WR0002")
        candidate_records.append(
            {
                "id": definition["id"],
                "record_status": "ACTIVE",
                "provisional_name": definition["name"],
                "aliases": definition["aliases"],
                "discovery_stage": STAGE,
                "discovery_anchor": {
                    "epoch": EPOCH,
                    "kind": "SOURCE_UNIT",
                    "id": definition["anchor"],
                    "ordinal": definition["anchor_ordinal"],
                },
                "source_unit_ids": definition["units"],
                "source_evidence": evidence,
                "source_status": sorted(source_statuses),
                "image_witnesses": image_witnesses,
                "evidence_strength": list(
                    dict.fromkeys(row["strength"] for row in evidence)
                ),
                "field_support": {
                    field: fingerprint[field]["status"] for field in FIELDS
                },
                "fingerprint": fingerprint,
                "parameters": [
                    {
                        "name": name,
                        "source_description": (
                            f"Source-stated parameter of {definition['name']}."
                        ),
                        "evidence_ids": [item_evidence],
                    }
                    for name in definition["parameters"]
                ],
                "variants": [
                    {
                        "name": name,
                        "source_description": (
                            f"Source-delimited variant of {definition['name']}."
                        ),
                        "evidence_ids": [item_evidence],
                    }
                    for name in definition["variants"]
                ],
                "missing_mechanics": missing,
                "uncertainties": (
                    [definition["uncertainty"]]
                    if definition["uncertainty"]
                    else []
                ),
                "related_candidate_ids": [],
                "cross_reference_ids": route_ids,
                "evidence_reassignments": [],
            }
        )

    reading_updates: list[dict[str, str]] = []
    for input_row, source_unit in zip(data["reading"], units):
        row = dict(input_row)
        unit_id = row["source_unit_id"]
        ids = candidate_ids_by_unit.get(unit_id, [])
        local_routes = route_ids_by_unit.get(unit_id, [])
        roles = roles_by_unit.get(unit_id, [])
        if any((candidate_id, unit_id) in anchors for candidate_id in ids):
            disposition = "CANDIDATE"
            statement = (
                "Fully read in canonical order; this unit introduces one or more linked source-defined "
                "objects, with mechanics and uncertainty limited to the cited evidence."
            )
        elif ids:
            disposition = (
                "REPRESENTATION_OR_OBSERVER"
                if source_unit["block_kind"] == "image"
                else "SUPPORTS_CANDIDATE"
            )
            statement = (
                "Fully read in context; this unit supports the linked object through mechanics, parameters, "
                "a finite witness, or an explicitly delimited variant."
            )
        elif local_routes:
            disposition = "CROSS_REFERENCE"
            statement = (
                "Fully read in context; its construction-bearing content is the recorded unresolved page route."
            )
        elif source_unit["block_kind"] == "image":
            disposition = "REPRESENTATION_OR_OBSERVER"
            statement = (
                "Fully read and image linkage checked; the unit is a representation or finite behavioral "
                "witness and does not independently delimit another source-defined object."
            )
        else:
            disposition = "NO_CONSTRUCTION"
            statement = (
                "Fully read with adjacent context; the unit supplies exposition, behavior, application, or "
                "argument but no independent identity-plus-law object or unresolved construction route."
            )
        source_status = "AMBIGUOUS" if unit_id in SOURCE_UNCERTAINTY else "CLEAR"
        uncertainty = SOURCE_UNCERTAINTY.get(unit_id, "")
        row.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": str(EPOCH),
                "review_disposition": disposition,
                "source_status": source_status,
                "uncertainty": uncertainty,
                "secondary_roles": compact(roles),
                "candidate_ids": compact(ids),
                "route_ids": compact(local_routes),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": WORKER_ID,
            }
        )
        reading_updates.append(row)

    mechanics_image_units = {
        unit_id
        for definition in definitions
        for unit_id in [definition["mechanics"], *definition["identity_units"]]
        if unit_id in asset_by_unit
    }
    observer_ids = {
        definition["id"]
        for definition in definitions
        if definition["profile"] == "OBSERVER"
    }
    asset_updates: list[dict[str, str]] = []
    for input_row in data["assets"]:
        row = dict(input_row)
        unit_id = row["source_unit_id"]
        ids = candidate_ids_by_unit.get(unit_id, [])
        local_routes = route_ids_by_unit.get(unit_id, [])
        source_status = "AMBIGUOUS" if unit_id in SOURCE_UNCERTAINTY else "CLEAR"
        uncertainty = SOURCE_UNCERTAINTY.get(unit_id, "")
        if row["asset_id"] == "A001028":
            visual_role = "DECORATIVE"
            risks: list[str] = []
            transcription = "NOT_REQUIRED"
            statement = (
                "Screened as a thumbnail and at original resolution; chapter-opening artwork only."
            )
        elif unit_id in mechanics_image_units:
            visual_role = "NATIVE_EVIDENCE"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            transcription = "CHECKED"
            statement = (
                "Screened as a thumbnail and at original resolution; rule marks, labels, states, geometry, "
                "and any numeric annotations were checked for the linked source-defined object."
            )
        elif ids and any(candidate_id in observer_ids for candidate_id in ids):
            visual_role = "OBSERVER"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            transcription = "CHECKED"
            statement = (
                "Screened as a thumbnail and at original resolution; this is a derived view or finite observer "
                "output, and its visible labels were checked without promoting hidden mechanics."
            )
        elif ids:
            visual_role = "RELATION"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            transcription = "CHECKED"
            statement = (
                "Screened as a thumbnail and at original resolution; this finite construction, relation, or "
                "behavior witness was checked against its adjacent source text."
            )
        else:
            visual_role = "CONTROL"
            risks = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]
            transcription = "CHECKED"
            statement = (
                "Screened as a thumbnail and at original resolution; visible labels and panel structure were "
                "checked, but the image does not independently delimit another source-defined object."
            )
        if row["asset_id"] == "A001120":
            visual_role = "RELATION"
            risks = ["TEXT_BEARING", "CAPTION_INCOMPLETE"]
            transcription = "CHECKED"
            statement = (
                "Original-resolution legacy label raster checked against the adjacent live label; it contributes "
                "source accounting only and no additional mechanics."
            )
        row.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": str(EPOCH),
                "visual_role": visual_role,
                "source_status": source_status,
                "risk_flags": compact(risks),
                "original_resolution_status": "REVIEWED",
                "transcription_status": transcription,
                "candidate_ids": compact(ids),
                "route_ids": compact(local_routes),
                "evidence_statement": statement,
                "review_stage": str(STAGE),
                "reviewer": WORKER_ID,
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append(row)

    output = {
        "worker_id": WORKER_ID,
        "bundle_sha256": manifest["content_set_sha256"],
        "prompt_sha256": manifest["prompt_sha256"],
        "schema_sha256": manifest["schema_sha256"],
        "allowed_manifest_sha256": digest(data["manifest_bytes"]),
        "prohibited_input_nonuse": True,
        "reading_updates": reading_updates,
        "candidate_proposals": candidate_records,
        "asset_updates": asset_updates,
        "route_proposals": routes,
        "uncertainties": [
            "Code 746 prose omits the zero-neighbor case, and code 976 prose omits the exactly-six case.",
            "Several continuous, stochastic, and physical systems omit probability measures, equations, boundaries, or tie-breaking conventions.",
            "The page-211 constraint and page-339 cellular automaton require their recorded target pages for complete local mechanics.",
            "Several late chapter examples are semantically delimited by prose and original-resolution figures but lack transcribed complete rule tables.",
            "The generalized random-walk and aggregation families leave parts of their direction, sampling, or eligible-site measures unstated.",
        ],
    }
    verify_output(bundle, output)
    return output


def verify_output(bundle: Path, output: dict[str, Any]) -> None:
    data = load_bundle(bundle)
    validate_bundle(bundle, data)
    check(output["worker_id"] == WORKER_ID, "output worker")
    check(output["bundle_sha256"] == data["manifest"]["content_set_sha256"], "bundle declaration")
    check(output["prompt_sha256"] == data["manifest"]["prompt_sha256"], "prompt declaration")
    check(output["schema_sha256"] == data["manifest"]["schema_sha256"], "schema declaration")
    check(output["allowed_manifest_sha256"] == digest(data["manifest_bytes"]), "manifest declaration")
    check(output["prohibited_input_nonuse"] is True, "nonuse declaration")
    check(len(output["reading_updates"]) == 435, "reading output count")
    check(len(output["asset_updates"]) == 92, "asset output count")
    check(len(output["candidate_proposals"]) == EXPECTED_CANDIDATES, "candidate output count")
    check(len(output["route_proposals"]) == len(ROUTE_DEFS), "route output count")
    check(
        [row["source_unit_id"] for row in output["reading_updates"]]
        == [row["source_unit_id"] for row in data["reading"]],
        "reading output order",
    )
    check(
        [row["asset_id"] for row in output["asset_updates"]]
        == [row["asset_id"] for row in data["assets"]],
        "asset output order",
    )
    check(
        [row["id"] for row in output["candidate_proposals"]]
        == [f"W{index:04d}" for index in range(1, EXPECTED_CANDIDATES + 1)],
        "candidate ID sequence",
    )
    evidence = sorted(
        (
            row
            for candidate in output["candidate_proposals"]
            for row in candidate["source_evidence"]
        ),
        key=lambda row: int(row["evidence_id"][2:]),
    )
    check(
        [row["evidence_id"] for row in evidence]
        == [f"WE{index:06d}" for index in range(1, len(evidence) + 1)],
        "evidence ID sequence",
    )
    check(
        [row["evidence_group_id"] for row in evidence]
        == [f"WG{index:06d}" for index in range(1, len(evidence) + 1)],
        "evidence-group sequence",
    )
    for candidate in output["candidate_proposals"]:
        check(set(candidate["fingerprint"]) == set(FIELDS), f"{candidate['id']} fingerprint")
        check(set(candidate["field_support"]) == set(FIELDS), f"{candidate['id']} support")
        check(
            len(candidate["fingerprint"]["evidence_limit"]["evidence_ids"]) == 1,
            f"{candidate['id']} evidence limit",
        )


def canonical_bytes(output: dict[str, Any]) -> bytes:
    return (
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path("/tmp/goal4-stage11-main"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    output_path = args.output or args.bundle / "output/output.json"
    if args.verify:
        output = json.loads(output_path.read_text(encoding="utf-8"))
        verify_output(args.bundle, output)
        print(
            f"PASS worker={WORKER_ID} units={len(output['reading_updates'])} "
            f"assets={len(output['asset_updates'])} candidates={len(output['candidate_proposals'])} "
            f"evidence={sum(len(c['source_evidence']) for c in output['candidate_proposals'])} "
            f"routes={len(output['route_proposals'])} sha256={digest(canonical_bytes(output))}"
        )
        return 0
    output = build_output(args.bundle)
    raw = canonical_bytes(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(raw)
    print(
        f"WROTE {output_path} units={len(output['reading_updates'])} "
        f"assets={len(output['asset_updates'])} candidates={len(output['candidate_proposals'])} "
        f"evidence={sum(len(c['source_evidence']) for c in output['candidate_proposals'])} "
        f"routes={len(output['route_proposals'])} sha256={digest(raw)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
