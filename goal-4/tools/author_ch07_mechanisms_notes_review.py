#!/usr/bin/env python3
"""Author the sealed Chapter 7 notes blind-review worksheet.

The semantic specification in this file was derived only from the assigned
sealed bundle.  It deliberately does not read or mutate any canonical Goal 4
ledger and can be run independently against the original and fresh bundles.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any


FIELDS = (
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
)

READING_FIELDS = (
    "source_unit_id",
    "document_order",
    "path",
    "block_kind",
    "byte_start",
    "byte_end",
    "line_start",
    "line_end",
    "global_line_start",
    "global_line_end",
    "unit_sha256",
    "review_status",
    "review_epoch",
    "review_disposition",
    "source_status",
    "uncertainty",
    "secondary_roles",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
)

ASSET_FIELDS = (
    "asset_id",
    "link_id",
    "physical_path",
    "sha256",
    "bytes",
    "source_path",
    "source_unit_id",
    "assignment_path",
    "assignment_stage",
    "assignment_basis",
    "reference_status",
    "inspection_status",
    "review_epoch",
    "visual_role",
    "source_status",
    "risk_flags",
    "original_resolution_status",
    "transcription_status",
    "candidate_ids",
    "route_ids",
    "evidence_statement",
    "review_stage",
    "reviewer",
    "uncertainty",
)


def C(
    name: str,
    anchor: str,
    sources: list[str],
    *,
    template: str,
    carrier: str,
    state: str,
    law: str | None,
    support: str = "the carrier described by the source",
    topology: str | None = None,
    alphabet: str | None = None,
    seed: str | None = None,
    input_value: str | None = "N/A",
    boundary: str | None = None,
    external: str | None = "none",
    frontier: str | None = None,
    schedule: str | None = None,
    read: str | None = None,
    write: str | None = None,
    result: str = "the state, value, configuration, or accepted object specified by the law",
    successor: str | None = None,
    determinism: str | None = None,
    termination: str | None = None,
    invariants: str | None = None,
    control: str | None = "N/A",
    witness: str | None = None,
    aliases: list[str] | None = None,
    law_sources: list[str] | None = None,
    params: list[tuple[str, str, list[str]]] | None = None,
    variants: list[tuple[str, str, list[str]]] | None = None,
    images: list[tuple[str, str, str]] | None = None,
    uncertainties: list[str] | None = None,
    conflicting_fields: list[str] | None = None,
    conflict_sources: list[str] | None = None,
    unknown_fields: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "anchor": anchor,
        "sources": sources,
        "template": template,
        "carrier": carrier,
        "state": state,
        "law": law,
        "support": support,
        "topology": topology,
        "alphabet": alphabet,
        "seed": seed,
        "input": input_value,
        "boundary": boundary,
        "external": external,
        "frontier": frontier,
        "schedule": schedule,
        "read": read,
        "write": write,
        "result": result,
        "successor": successor,
        "determinism": determinism,
        "termination": termination,
        "invariants": invariants,
        "control": control,
        "witness": witness,
        "aliases": aliases or [],
        "law_sources": law_sources or [anchor],
        "params": params or [],
        "variants": variants or [],
        "images": images or [],
        "uncertainties": uncertainties or [],
        "conflicting_fields": conflicting_fields or [],
        "conflict_sources": conflict_sources or [],
        "unknown_fields": unknown_fields or {},
    }


CANDIDATES = [
    C(
        "mechanical toss-or-mix randomness source",
        "U006598",
        ["U006598", "U006606", "U006607", "U006608"],
        template="stochastic",
        carrier="a tossed object or a mixed collection of selectable objects",
        state="object orientation/landing position or collection arrangement",
        law="toss and observe the landing, or mix a collection and select one object",
        topology="ordinary physical space",
        alphabet="the finite or spatial set of observable outcomes",
        seed="an object and launch condition, or a collection before mixing",
        boundary=None,
        external="uncontrolled microscopic physical details",
        frontier="the tossed object or the mixed collection",
        schedule="one toss or one mix-and-draw event per output",
        read="landing orientation/position or selected object",
        write="emit the observed outcome",
        successor="a probability measure over observable outcomes",
        determinism="stochastic at the modeled level",
        termination="each event completes on landing or selection",
        witness="the emitted toss/draw outcome",
        variants=[
            ("toss-and-observe", "Toss an object and observe which way up or where it lands.", ["U006598"]),
            ("mix-and-draw", "Mix a collection by shaking and select an object.", ["U006598", "U006607"]),
            ("bouncing-object source", "Bounce balls in air or fluid to randomize selection.", ["U006608"]),
        ],
    ),
    C(
        "stochastic model",
        "U006600",
        ["U006600"],
        template="stochastic_partial",
        carrier="a scientific model with uncertain elements represented by random variables",
        state="the model variables and their sampled values",
        law="replace poorly known elements by random variables",
        alphabet="variable-specific value spaces",
        external="random-variable draws",
        result="a probability distribution or sampled model outcome",
        determinism="probability law; the exact law is model-specific",
        termination="model-specific",
        witness="a sampled outcome or analytically derived outcome probability",
        uncertainties=["The source defines the stochastic modeling pattern but no single variable distribution or transition law."],
    ),
    C(
        "Monte Carlo simulation-and-average method",
        "U006600",
        ["U006600"],
        template="stochastic",
        carrier="a simulatable model and an ensemble of independent random-variable choices",
        state="the accumulated simulations and aggregate statistics",
        law="simulate repeatedly with different random-variable choices, then compute statistical averages",
        alphabet="model outcomes and numerical aggregate statistics",
        seed="a model plus a sampling setup",
        external="successive random-variable draws",
        frontier="the next simulation trial",
        schedule="repeat trials, then aggregate",
        read="the model and the current trial's random choices",
        write="append a trial outcome and update the aggregate",
        successor="a measure over trial outcomes; one aggregate for a fixed sample",
        determinism="stochastic trials with deterministic aggregation",
        termination="after a chosen number of trials",
        witness="the reported statistical average and its sampled outcomes",
    ),
    C(
        "shot-noise process",
        "U006601",
        ["U006601", "U006609"],
        template="physical_partial",
        carrier="a flow of discrete charge carriers",
        state="carrier arrivals or current over time",
        law="statistical fluctuations in the flow of discrete charge carriers",
        support="an electrical current or sampled discharge tube",
        topology="time",
        alphabet="current values or sampled output symbols",
        external="microscopic carrier motion",
        result="a noisy waveform with a flat frequency spectrum",
        determinism="stochastic at the modeled level",
        witness="flat-spectrum current fluctuations",
        params=[("carrier count", "A 10,000-electron bit is said to show fluctuations of about 1%.", ["U006601"])],
    ),
    C(
        "thermal (Johnson) noise process",
        "U006602",
        ["U006602", "U006609"],
        template="physical_partial",
        carrier="charge carriers in material at nonzero temperature",
        state="microscopic carrier motions and resulting current over time",
        law="thermal motion produces current fluctuations whose intensity is essentially proportional to temperature",
        support="an electrical material or sampled on-chip resistor",
        topology="time",
        alphabet="current values or sampled output symbols",
        external="thermal microscopic motion",
        result="a flat-spectrum noisy waveform",
        determinism="stochastic at the modeled level",
        witness="flat-spectrum fluctuations with temperature-dependent intensity",
        params=[("temperature", "Noise intensity is essentially proportional to temperature.", ["U006602"])],
    ),
    C(
        "flicker (1/f) noise process",
        "U006603",
        ["U006603", "U006609"],
        template="physical_partial",
        carrier="a device or natural process observed as a time series",
        state="the observed quantity over time",
        law="a process whose power spectrum is approximately proportional to 1/f over a broad frequency range",
        support="time-series observations",
        topology="time/frequency",
        alphabet="real-valued observations",
        external=None,
        result="large low-frequency fluctuations and an approximate 1/f spectrum",
        determinism="the source does not identify a unique generating law",
        witness="the measured power-law spectrum",
        uncertainties=["The source explicitly says the microscopic origin of flicker noise remains mysterious."],
    ),
    C(
        "discrete power-spectrum analyzer",
        "U006604",
        ["U006604", "U006605"],
        template="declarative",
        carrier="a finite numerical data sequence and its discrete Fourier-frequency bins",
        state="N/A",
        law="return Abs[Fourier[data]]^2",
        support="the frequency bins of the discrete Fourier transform of the supplied data",
        topology="finite sequence order mapped to discrete frequency order",
        alphabet="numeric input samples and nonnegative real spectral powers",
        input_value="a finite numerical sequence data",
        boundary="the complete supplied sequence under the Fourier convention used by Fourier",
        external="none",
        result="a discrete power spectrum, one squared Fourier magnitude per frequency bin",
        determinism="deterministic for fixed data and Fourier convention",
        witness="the returned spectrum and any fitted power-law form 1/f^alpha",
        params=[
            (
                "spectral exponent alpha",
                "The displayed output families are alpha=0, 1/2, 1, 3/2, and 2; alpha describes a spectrum and does not define a generating dynamics.",
                ["U006604", "U006605"],
            )
        ],
        images=[
            (
                "A000666",
                "DIRECT_PARTIAL_MECHANICS",
                "The five labeled examples identify analyzed spectrum families alpha=0, 1/2, 1, 3/2, and 2; they do not define a generator.",
            )
        ],
    ),
    C(
        "electronic physical-randomness generator",
        "U006609",
        ["U006609"],
        template="stochastic_partial",
        carrier="an electronic noise source and sampling circuitry",
        state="the sampled noise signal and any output-conditioning state",
        law="sample shot, thermal, or semiconductor-breakdown noise and condition it toward unbiased output",
        alphabet="sampled bits or digits",
        external="physical electronic noise",
        result="a stream of random-looking bits or digits",
        determinism="stochastic at the modeled level",
        termination="streaming",
        witness="output statistics and correlations at the selected sampling rate",
        variants=[
            ("ERNIE neon-discharge sampler", "Samples shot noise from neon discharge tubes at a few digits per second.", ["U006609"]),
            ("semiconductor breakdown sampler", "Samples breakdown noise, often from back-biased zener diodes.", ["U006609"]),
            ("thermal-noise sampler", "Samples thermal noise from an electronic component.", ["U006609"]),
        ],
        uncertainties=["The source does not specify a single conditioning algorithm for obtaining unbiased bits."],
    ),
    C(
        "quantum-event randomness generator",
        "U006610",
        ["U006610"],
        template="stochastic_partial",
        carrier="detected radioactive decays or paths of individual photons",
        state="the detector state and detected event stream",
        law="sample individual quantum events and encode their detected outcomes",
        alphabet="event times, paths, or derived bits",
        external="quantum events plus detector/environment effects",
        result="a random-looking output stream",
        determinism="quantum probability law at the modeled level",
        termination="streaming",
        witness="measured output bits and their residual correlations",
        variants=[
            ("radioactive-decay sampler", "Detect radioactive decay events at tens of bits per second.", ["U006610"]),
            ("single-photon path sampler", "Detect paths of individual photons at attempted megahertz rates.", ["U006610"]),
        ],
        uncertainties=["The detector law and output encoding are not specified, and the source reports possible 1/f contamination."],
    ),
    C(
        "computer entropy-pool seeding system",
        "U006610",
        ["U006610"],
        template="stochastic",
        carrier="a persistent computer entropy pool",
        state="the pool state, including persisted information across reboot",
        law="mix precise interrupt timings and device-delivery timings into a pool used to seed programmatic randomness",
        alphabet="machine state and output seed bits",
        seed="persisted pool information plus newly observed timing events",
        external="keyboard, mouse, disk, network, and other interrupt timings",
        frontier="each newly delivered timing event",
        schedule="event-driven accumulation",
        read="current pool state and the next timing event",
        write="update the pool and expose seed material",
        successor="one pool update per observed event",
        determinism="deterministic mixing of environmentally variable inputs; mixing formula unspecified",
        termination="streaming",
        witness="seed material or virtual-device output",
        aliases=["/dev/random-style entropy pool"],
        uncertainties=["The exact pool mixing and extraction functions are not given."],
    ),
    C(
        "biological stochastic DNA rearrangement process",
        "U006611",
        ["U006611", "U006612"],
        template="stochastic_partial",
        carrier="chromosomes or DNA blocks in reproductive and immune cells",
        state="the selected chromosome versions, crossover positions, or joined DNA blocks",
        law="randomly select chromosome versions and crossover/join positions during meiosis or antibody formation",
        alphabet="DNA sequences and chromosome/block choices",
        external="microscopic chemical and cellular fluctuations",
        result="a rearranged DNA sequence",
        determinism="stochastic at the modeled level",
        termination="on formation of the gamete or antibody-producing cell",
        witness="the resulting chromosome/block arrangement",
        variants=[
            ("meiotic chromosome selection", "Select one of two versions of each chromosome.", ["U006611"]),
            ("meiotic crossover", "Exchange DNA at a few approximately randomly positioned crossovers per chromosome.", ["U006611"]),
            ("antibody block joining", "Select and join DNA blocks at random.", ["U006612"]),
        ],
        uncertainties=["No quantitative probability law for choices or crossover locations is supplied."],
    ),
    C(
        "flagellar tumble direction-change process",
        "U006614",
        ["U006614"],
        template="physical_partial",
        carrier="a flagellated microorganism and its flagella",
        state="flagellar rotation state and organism direction",
        law="counter-rotation causes filaments to flail, producing a random change in direction",
        support="the organism in fluid",
        topology="physical space",
        alphabet="continuous directions and flagellar states",
        external="fluid and microscopic mechanical details",
        result="a changed swimming direction",
        determinism="stochastic at the modeled level",
        termination="one tumble event",
        witness="the post-tumble direction",
        uncertainties=["The source gives no distribution over new directions or event times."],
    ),
    C(
        "frictionally decelerated spinning/tossing model",
        "U006617",
        ["U006617"],
        template="continuous",
        carrier="a ball or rotating object",
        state="speed, traveled distance, and orientation as functions of time",
        law="speed v-a t, stop time v/a, distance v t-a t^2/2, and orientation represented modulo circumference",
        support="continuous time until rest",
        topology="one-dimensional path/orientation modulo 2 pi r",
        alphabet="real-valued speed, distance, and orientation",
        seed="initial speed v and radius r",
        input_value="N/A",
        boundary="orientation wraps modulo 2 pi r",
        frontier="the single moving object",
        schedule="continuous evolution in t",
        read="current time and fixed parameters v, a, r",
        write="evaluate the state functions at t",
        result="the object's state at time t",
        successor="one state for each t",
        determinism="deterministic",
        termination="at t=v/a",
        params=[
            ("initial speed v", "Initial speed in the stated formulas.", ["U006617"]),
            ("deceleration a", "Constant frictional deceleration.", ["U006617"]),
            ("radius r", "Sets the orientation modulus 2 pi r.", ["U006617"]),
        ],
    ),
    C(
        "rectangular billiard trajectory system",
        "U006618",
        ["U006618", "U006619"],
        template="continuous",
        carrier="a billiard ball on a rectangular table",
        state="ball position, direction, and side-hit sequence",
        law="straight motion with reflections at horizontal and vertical sides; the hit sequence is governed by the initial slope's continued fraction",
        topology="a bounded rectangle",
        alphabet="continuous positions/directions and horizontal/vertical side labels",
        seed="an initial position and slope",
        boundary="reflecting table sides",
        frontier="the ball",
        schedule="continuous flight punctuated by boundary collisions",
        read="current trajectory and the next intersected side",
        write="reflect the trajectory at the side",
        result="a trajectory and side-hit word",
        successor="one deterministic continuation",
        determinism="deterministic",
        termination="nonterminating in the idealized model",
        witness="the ordered sequence of horizontal and vertical side hits",
        params=[("initial slope", "The illustrated slope is 1/sqrt(2).", ["U006618"])],
        images=[("A000667", "DIRECT_PARTIAL_MECHANICS", "The five-panel row checks the reflected path after 2, 5, 10, 50, and 100 bounces.")],
    ),
    C(
        "three-body gravitational trajectory system",
        "U006621",
        ["U006621", "U006622", "U006623", "U006624"],
        template="continuous_partial",
        carrier="three mutually interacting bodies",
        state="the bodies' positions and velocities",
        law="three-body mechanical evolution conserving energy and angular momentum",
        topology="continuous physical space",
        alphabet="real-valued positions, velocities, and masses",
        seed="three initial positions and velocities",
        boundary="unbounded space",
        frontier="all three bodies",
        schedule="continuous simultaneous evolution",
        read="all positions, velocities, and masses",
        result="three trajectories, possibly with one body escaping",
        determinism="deterministic for fixed initial data",
        termination="no native termination; escape is an observed outcome",
        invariants="total mechanical energy and angular momentum",
        witness="the three trajectories and any escape event",
        images=[
            ("A000673", "CONTEXTUAL", "The five-panel row witnesses idealized repetitive planet orbits in the field of an elliptically orbiting star pair."),
            ("A000680", "CONTEXTUAL", "The six paired trajectory examples show different escape delays under nearby initial velocities."),
        ],
        uncertainties=["The explicit general force equation and mass parameters are not present in the assigned notes."],
    ),
    C(
        "Sitnikov-type idealized planet equation",
        "U006626",
        ["U006626", "U006627", "U006628", "U006629"],
        template="continuous",
        carrier="the scalar planet coordinate z(t)",
        state="z(t) and its time derivative",
        law="d2z/dt2 = -z/(z^2 + (1/2(1+e sin(2 pi t)))^2)^(3/2)",
        support="continuous time",
        topology="one-dimensional coordinate normal to the stars' orbital plane",
        alphabet="real-valued z and velocity",
        seed="initial z and velocity",
        boundary="unbounded z",
        frontier="the scalar trajectory",
        schedule="continuous differential evolution",
        read="z(t), time t, and eccentricity e",
        write="the differential relation determines acceleration",
        result="a numerical trajectory z(t)",
        successor="one local trajectory for fixed initial data",
        determinism="deterministic",
        termination="no native termination",
        witness="z(t), zero-crossing times, and sensitivity to z(0)",
        params=[
            ("eccentricity e", "The illustrated case uses e=0.1; e=0 is singled out as soluble.", ["U006628"]),
            ("working precision", "The illustrated numerical results use 40 decimal digits.", ["U006628"]),
        ],
        images=[("A000681", "CONTEXTUAL", "The surface plots show z(t) versus t and z(0), exposing sensitive dependence.")],
    ),
    C(
        "perfect riffle-shuffle permutation",
        "U006634",
        ["U006634", "U006635", "U006636", "U006637"],
        template="deterministic",
        carrier="an even-length ordered list",
        state="the current list ordering",
        law="partition the list in half, reverse the two halves' order, transpose them, and flatten, optionally omitting Reverse",
        support="a finite list",
        topology="linear list order",
        alphabet="the list's elements",
        seed="the initial list ordering",
        boundary="finite even list",
        frontier="the whole list",
        schedule="one permutation per shuffle",
        read="all list elements and the half-length partition",
        write="replace the list by the flattened interleaving",
        result="a permuted list",
        successor="one",
        determinism="deterministic",
        termination="one shuffle; iteration is external",
        invariants="list length and multiset of elements",
        witness="the ordering after each shuffle",
        variants=[
            ("with Reverse", "Use Reverse around the half-deck partition.", ["U006635"]),
            ("without Reverse", "Omit Reverse while retaining perfect alternation.", ["U006636"]),
        ],
        params=[("deck size", "The example iterates a 52-element deck for 26 shuffles.", ["U006636"])],
        images=[("A000682", "CONTEXTUAL", "The row depicts the ordering generated by repeated perfect shuffles.")],
    ),
    C(
        "linear congruential generator",
        "U006639",
        ["U006639", "U006640", "U006641", "U006642", "U006643", "U006644", "U006645", "U006646", "U006647"],
        template="deterministic",
        carrier="an integer residue n modulo m",
        state="the current residue n",
        law="replace n by Mod[a n,m], or in the affine variant by Mod[a n+b,m]",
        support="the finite residue set modulo m",
        topology="a finite functional graph",
        alphabet="integers 0 through m-1",
        seed="an initial residue n",
        boundary="arithmetic modulo m",
        frontier="the single residue state",
        schedule="one modular update per step",
        read="n and fixed parameters a,m (and b in the affine variant)",
        write="replace n by the modular result",
        result="a residue sequence",
        successor="one",
        determinism="deterministic",
        termination="nonterminating; finite-state evolution eventually repeats",
        witness="the emitted residue/digit sequence and its repetition period",
        params=[
            ("multiplier a", "Examples include 23, 65539, and 69069.", ["U006639"]),
            ("modulus m", "Examples include 10^8+1 and 2^j, often j=31.", ["U006639", "U006640"]),
            ("increment b", "The affine generalization adds b before reduction.", ["U006642"]),
        ],
        variants=[
            ("multiplicative LCG", "n -> Mod[a n,m].", ["U006639"]),
            ("affine LCG", "n -> Mod[a n+b,m].", ["U006642"]),
            ("RANDU parameters", "a=65539 with m=2^31.", ["U006639", "U006645"]),
        ],
    ),
    C(
        "linear feedback shift register",
        "U006649",
        ["U006649", "U006650", "U006651", "U006652", "U006654", "U006655", "U006657", "U006658", "U006659"],
        template="deterministic",
        carrier="a finite binary register",
        state="the ordered register bit list",
        law="drop the first bit and append the modulo-2 sum of selected tap bits",
        support="n register positions",
        topology="a finite shift register with feedback/spiral boundary",
        alphabet="{0,1}",
        seed="an n-bit register; the example uses n-1 zeros followed by one",
        boundary="feedback from selected positions to the appended end",
        frontier="the whole register shift and the appended cell",
        schedule="one shift/feedback update per step",
        read="the selected tap positions",
        write="Rest[list] followed by the parity bit",
        result="a binary register-state/output sequence",
        successor="one",
        determinism="deterministic",
        termination="nonterminating; finite-state evolution eventually repeats",
        witness="the state sequence and repetition period",
        params=[
            ("register length n", "Controls the finite state space and attainable period.", ["U006651", "U006659"]),
            ("tap positions", "Any selected list of register positions can feed the parity bit.", ["U006657", "U006658", "U006659"]),
        ],
        variants=[
            ("two-tap rule-60 form", "Append Mod[list[[1]]+list[[2]],2].", ["U006649", "U006650"]),
            ("general tap form", "Append the modulo-2 sum at arbitrary tap positions.", ["U006657", "U006658"]),
            ("polynomial state representation", "Represent the state by FromDigits[list,x] and x^t modulo {1+x+x^n,2}.", ["U006654", "U006655"]),
        ],
        images=[("A000683", "CONTEXTUAL", "The evolution row checks the finite-register pattern for n=30.")],
    ),
    C(
        "generalized Fibonacci random-number generator",
        "U006661",
        ["U006661", "U006662"],
        template="deterministic",
        carrier="a length-q list of residues modulo 2^k",
        state="the q most recent recurrence values",
        law="append Mod[f[n-p]+f[n-q],2^k] while dropping the oldest value",
        support="q recurrence positions",
        topology="finite shift register",
        alphabet="integers modulo 2^k",
        seed="q initial recurrence values",
        boundary="feedback from lags p and q",
        frontier="the appended recurrence value",
        schedule="one recurrence update per step",
        read="the values at lags p and q",
        write="shift and append their modular sum",
        result="a residue sequence",
        successor="one",
        determinism="deterministic",
        termination="nonterminating; finite-state evolution eventually repeats",
        witness="the emitted recurrence values",
        params=[
            ("lag p", "One example uses p=24.", ["U006661"]),
            ("lag q", "One example uses q=55 and a q-element state.", ["U006661", "U006662"]),
            ("word size k", "Values are reduced modulo 2^k.", ["U006661", "U006662"]),
        ],
    ),
    C(
        "stream-cipher random-number generator",
        "U006663",
        ["U006663"],
        template="deterministic_partial",
        carrier="a keyed stream-cipher state",
        state="the cipher's internal state and generated keystream position",
        law="use a repeatable stream cipher to emit its keystream as random numbers",
        alphabet="bits or grouped machine words",
        seed="a cryptographic key and cipher initialization",
        external="none after initialization",
        result="a repeatable pseudorandom bit stream",
        determinism="deterministic for fixed key and initialization",
        termination="streaming",
        witness="the emitted keystream",
        variants=[("DES-based generator", "Use the Data Encryption Standard as the practical cryptographic primitive.", ["U006663"])],
        uncertainties=["The in-scope source does not specify the cipher mode, state transition, or output grouping."],
    ),
    C(
        "middle-square generator",
        "U006664",
        ["U006664", "U006665"],
        template="deterministic",
        carrier="a fixed-width decimal integer",
        state="the current integer n",
        law="square n, pad to 20 decimal digits, take positions 5 through 15, and interpret them in base 10",
        support="fixed-width decimal digit strings",
        topology="a finite functional graph",
        alphabet="decimal integers in the retained width",
        seed="an initial integer n",
        boundary="fixed decimal width supplied to IntegerDigits",
        frontier="the single integer state",
        schedule="one square-and-extract update per step",
        read="n",
        write="replace n by the retained middle digits",
        result="an integer sequence",
        successor="one",
        determinism="deterministic",
        termination="nonterminating; the finite state eventually repeats",
        witness="the emitted integer sequence and its short period",
    ),
    C(
        "quadratic congruential generator",
        "U006666",
        ["U006666", "U006667", "U006668"],
        template="deterministic",
        carrier="an integer residue n modulo m",
        state="the current residue n",
        law="replace n by Mod[n^2,m]",
        support="the finite residue set modulo m",
        topology="a finite functional graph",
        alphabet="integers 0 through m-1",
        seed="an initial residue n",
        boundary="arithmetic modulo m",
        frontier="the single residue state",
        schedule="one modular squaring per step",
        read="n and m",
        write="replace n by n^2 modulo m",
        result="a residue or parity sequence",
        successor="one",
        determinism="deterministic",
        termination="nonterminating; finite-state evolution eventually repeats",
        witness="the residue sequence, optionally observed through Mod[n,2]",
        params=[("modulus m", "Discussed for pq, prime m, and the example m=65063.", ["U006668"])],
    ),
    C(
        "cellular-automaton random-number generator",
        "U006669",
        ["U006669"],
        template="deterministic_partial",
        carrier="a finite one-dimensional cellular-automaton row",
        state="the complete finite row",
        law="iterate elementary cellular automaton rule 30 or rule 45 and extract a random-number stream",
        support="n cells",
        topology="a finite 1D cellular automaton; boundary and extraction are not stated here",
        alphabet="{0,1}",
        seed="a finite initial row",
        boundary=None,
        frontier="all cells",
        schedule="synchronous cellular-automaton steps",
        read="the elementary local neighborhood named by the rule code",
        write="replace every cell by the rule output",
        result="an extracted bit stream",
        successor="one",
        determinism="deterministic",
        termination="nonterminating; finite systems eventually repeat",
        witness="the extracted bit sequence and finite-system repetition period",
        params=[("cell count n", "Rule 30 period is empirically about 2^(0.63 n).", ["U006669"])],
        variants=[
            ("rule 30 generator", "The primary 1985 cellular-automaton generator.", ["U006669"]),
            ("rule 45 generator", "An alternative with a longer period but slower local mixing.", ["U006669"]),
        ],
        uncertainties=["The finite boundary condition and exact output-cell extraction are not supplied in this notes unit."],
    ),
    C(
        "equal-bit to biased-bit converter",
        "U006670",
        ["U006670", "U006671", "U006672"],
        template="deterministic",
        carrier="a finite binary input sequence a and the binary digits of a target probability p",
        state="the fold accumulator and remaining paired digits",
        law="fold BitAnd or BitOr selected by each probability digit over paired reversed digits of p and a",
        support="n paired binary digits",
        topology="a finite sequence fold",
        alphabet="{0,1}",
        seed="fold accumulator 0",
        input_value="n unbiased input bits and target probability p",
        boundary="exactly n binary digits of p are used in the displayed function",
        external="the unbiased input bit sequence",
        frontier="the next paired probability/input digit",
        schedule="right-to-left Fold",
        read="the accumulator, one probability digit, and one input digit",
        write="replace the accumulator by BitAnd or BitOr",
        result="one output bit with approximate probabilities {1-p,p}",
        successor="one result for a fixed input sequence",
        determinism="deterministic transformation of random inputs",
        termination="after n fold elements",
        witness="the output bit and its induced probability",
        params=[
            ("target probability p", "Specified through n base-2 digits.", ["U006670", "U006671"]),
            ("precision/input length n", "Controls approximation precision.", ["U006670", "U006671"]),
        ],
        variants=[("streaming generalization", "Generate a sequence using on average as few as two input digits per output digit.", ["U006672"])],
    ),
    C(
        "noisy continuous cellular-automaton model",
        "U006673",
        ["U006673", "U006674", "U006675"],
        template="stochastic",
        carrier="a one-dimensional array of continuous cell values",
        state="all current real-valued cell colors",
        law="apply lambda(x)=exp(-10(x-1)^2)+exp(-10(x-3)^2) to a+c for rule 90 or a+b+c+bc for rule 30, then add signed random perturbations of size delta",
        support="a 1D cell array",
        topology="one-dimensional local lattice",
        alphabet="continuous real cell values",
        seed="an initial real-valued row",
        boundary=None,
        external="a fresh Random[] perturbation for each update",
        frontier="all cells",
        schedule="synchronous steps",
        read="left/self/right values as required by the selected variant",
        write="replace each cell by the lambda output plus perturbation",
        result="a continuous-valued cellular-automaton history",
        successor="a probability measure over next rows",
        determinism="stochastic because perturbations are freshly sampled",
        termination="nonterminating",
        witness="the full cell-value evolution and survival/destruction of structure",
        params=[("perturbation size delta", "Scales the added signed Random[] term.", ["U006675"])],
        variants=[
            ("continuous rule 90", "Update with lambda[a+c].", ["U006675"]),
            ("continuous rule 30", "Update with lambda[a+b+c+bc].", ["U006675"]),
        ],
        uncertainties=["The array boundary condition is not stated."],
    ),
    C(
        "discrete-cellular-automaton to continuous-PDE approximation relation",
        "U006676",
        ["U006676"],
        template="declarative",
        carrier="a discrete cellular automaton and a prospective continuous field model",
        state="N/A",
        law=None,
        support="continuous color over continuous space and continuous time",
        topology="a continuous space-time domain",
        alphabet="continuous field values",
        input_value="a discrete cellular automaton together with an unspecified approximation construction",
        boundary=None,
        external="none",
        result="an unspecified partial differential equation intended to approximate the cellular automaton",
        successor="one or more possible PDE approximations",
        determinism="not determined by this notes unit",
        witness="agreement between the discrete automaton and a continuous-space/time field evolution",
        uncertainties=[
            "The notes unit states only that the approach can be extended; it supplies neither the PDE nor the discrete-to-continuous mapping, and points to page 464."
        ],
        unknown_fields={
            "rule_relation_constraint_function_or_probability_law": "The in-scope source asserts that a PDE approximation can be made but supplies no PDE or mapping procedure.",
            "successor_cardinality": "The in-scope source does not determine whether fixed discrete data select one PDE approximation or multiple alternatives.",
            "determinism_branching_or_measure": "The in-scope source does not determine a discrete-to-continuous selection law.",
        },
    ),
    C(
        "Gaussian central-limit aggregation law",
        "U006680",
        ["U006680", "U006681", "U006682", "U006683", "U006684"],
        template="declarative",
        carrier="collections of independent random variables with bounded variance",
        state="N/A",
        law="averages converge to density Exp[-(x-mu)^2/(2 sigma^2)]/(sqrt(2 pi) sigma)",
        support="real-valued outcomes x",
        topology="the real line",
        alphabet="real values",
        input_value="a collection of independent random variables",
        result="a Gaussian probability density for the aggregate",
        determinism="a probability measure fixed by mu and sigma",
        witness="the limiting density and its 1/sqrt(n) standard-deviation rescaling",
        params=[
            ("mean mu", "Determined by the underlying random variables.", ["U006681", "U006682"]),
            ("standard deviation sigma", "Determined by the inputs and shrinks by 1/sqrt(n) under Gaussian averaging.", ["U006681", "U006682", "U006684"]),
        ],
        images=[("A000684", "CONTEXTUAL", "The five-panel histogram row shows convergence under larger aggregates.")],
    ),
    C(
        "lognormal product law",
        "U006685",
        ["U006685", "U006686"],
        template="declarative",
        carrier="products of many random variables",
        state="N/A",
        law="density Exp[-(Log[x]-mu)^2/(2 sigma^2)]/(sqrt(2 pi) x sigma)",
        support="positive real x",
        topology="the positive real line",
        alphabet="positive real values",
        input_value="multiplicatively combined random variables",
        result="a lognormal probability density",
        determinism="a probability measure fixed by mu and sigma",
        witness="the resulting density",
        params=[
            ("mu", "Location parameter in log space.", ["U006686"]),
            ("sigma", "Scale parameter in log space.", ["U006686"]),
        ],
    ),
    C(
        "Fisher-Tippett extreme-value law",
        "U006687",
        ["U006687", "U006688", "U006689"],
        template="declarative",
        carrier="extreme values from large collections of random variables",
        state="N/A",
        law="density Exp[(x-mu)/beta] Exp[-Exp[(x-mu)/beta]]/beta",
        support="real-valued extreme observations",
        topology="the real line",
        alphabet="real values",
        input_value="a large collection of random variables from a broad class of distributions",
        result="an extreme-value probability density",
        determinism="a probability measure fixed by mu and beta",
        witness="the limiting extreme-value density",
        params=[
            ("mu", "Location parameter.", ["U006688"]),
            ("beta", "Scale parameter.", ["U006688"]),
        ],
        aliases=["extreme-value distribution"],
    ),
    C(
        "Wigner random-matrix spectral laws",
        "U006690",
        ["U006690", "U006691", "U006692", "U006693"],
        template="declarative",
        carrier="large symmetric random matrices with entry mean 0 and bounded variance",
        state="N/A",
        law="normalized eigenvalue density tends to 2 sqrt(1-x^2) UnitStep[1-x^2]/pi; spacings tend to (pi x/2) exp(-pi x^2/4)",
        support="normalized eigenvalues and their spacings",
        topology="the real line",
        alphabet="real eigenvalues/spacings",
        input_value="a large symmetric random matrix ensemble",
        result="limiting eigenvalue and spacing probability densities",
        determinism="probability laws induced by the matrix ensemble",
        witness="the empirical normalized spectrum and spacings",
        variants=[
            ("semicircle density", "The normalized eigenvalue density on [-1,1].", ["U006690", "U006691"]),
            ("nearest-spacing density", "The displayed pi x/2 exponential spacing law.", ["U006692"]),
            ("largest-eigenvalue law", "Often expressible with Painleve functions; no formula is supplied.", ["U006693"]),
        ],
    ),
    C(
        "lattice random walk",
        "U006695",
        ["U006695", "U006696", "U006697", "U006698", "U006699", "U006700", "U006701", "U006702", "U006703", "U006705", "U006706", "U006707", "U006708", "U006709", "U006710", "U006715"],
        template="stochastic",
        carrier="a particle position on a regular lattice",
        state="the current position and optional visited history",
        law="at each step choose one allowed unit direction at random and add it to the position",
        support="one- or d-dimensional regular lattices",
        topology="the selected regular lattice",
        alphabet="lattice coordinate vectors",
        seed="the origin in the displayed implementations",
        boundary="unbounded by default; sources, absorbers, and reflectors are named variants",
        external="one fresh random direction choice per step",
        frontier="the current particle",
        schedule="one move per discrete step",
        read="the current position and sampled direction",
        write="replace position by position plus the direction vector",
        result="a position history",
        successor="a measure over allowed neighboring positions",
        determinism="stochastic",
        termination="after t requested steps",
        witness="the complete walk or its endpoint/displacement",
        params=[
            ("step count t", "Number of generated moves.", ["U006695", "U006696", "U006700"]),
            ("dimension d", "Dimension of the coordinate vector.", ["U006699", "U006700"]),
            ("direction count k", "Number of equally spaced 2D directions.", ["U006706", "U006707", "U006709"]),
        ],
        variants=[
            ("1D plus/minus walk", "Add (-1)^Random[Integer] at each step.", ["U006695", "U006696", "U006698"]),
            ("d-dimensional axial walk", "Choose a sign and random cyclic axis.", ["U006699", "U006700"]),
            ("k-direction 2D walk", "Choose uniformly from k unit vectors on a circle.", ["U006706", "U006707", "U006709"]),
            ("source/absorber/reflector walk", "Allow particle sources, absorbers, or reflectors; exact rules are not supplied.", ["U006715"]),
        ],
    ),
    C(
        "self-avoiding walk",
        "U006717",
        ["U006717", "U006718"],
        template="stochastic_partial",
        carrier="a growing lattice path",
        state="the ordered path and set of already visited sites",
        law="choose steps subject to the global constraint that no visited site may be revisited",
        support="a lattice",
        topology="the selected lattice",
        alphabet="lattice coordinate vectors",
        seed="a starting site or simple line",
        boundary="unbounded in the stated examples",
        external="random choices used by the chosen generation algorithm",
        frontier="the current endpoint or the pivoted path segment",
        schedule="append a step, combine shorter walks, or pivot a segment",
        read="the candidate step/segment and the complete visited set",
        write="accept only a path that remains self-avoiding",
        result="a self-avoiding path",
        successor="a measure over valid continuations or transformed paths",
        determinism="stochastic generation under a hard constraint",
        termination="after the requested length or when a naive growth attempt gets stuck",
        witness="the full path and absence of repeated sites",
        variants=[
            ("naive endpoint growth", "Add individual random steps until stuck.", ["U006717"]),
            ("combine-shorter-walks method", "Generate long walks by combining shorter valid walks.", ["U006717"]),
            ("pivot method", "Successively pivot pieces beginning from a line.", ["U006717"]),
        ],
        images=[("A000699", "CONTEXTUAL", "The row shows 1-, 20-, and 1000-particle/step self-avoiding examples.")],
        uncertainties=["The exact proposal and acceptance distributions for the combination and pivot algorithms are not supplied."],
    ),
    C(
        "Eden aggregation model",
        "U006719",
        ["U006719", "U006721", "U006722", "U006723", "U006724", "U006725"],
        template="stochastic",
        carrier="a finite set or grid of occupied lattice cells",
        state="the complete occupied cluster",
        law="type B selects an occupied cell and one of its four neighbors, retrying if occupied; type A selects uniformly from all cells adjacent to the cluster",
        support="a regular lattice, illustrated on the 2D square lattice",
        topology="nearest-neighbor lattice",
        alphabet="{empty,occupied}",
        seed="one occupied cell at the origin",
        boundary="unbounded in the coordinate-list form; grid boundary is implementation-specific",
        external="fresh random choices of cells/sites",
        frontier="the cluster boundary and, in type B, sampled occupied cells",
        schedule="add one new occupied cell per successful step",
        read="cluster membership and immediate neighbors",
        write="append or set one previously empty adjacent cell",
        result="a growing occupied cluster",
        successor="a measure over eligible adjacent additions",
        determinism="stochastic",
        termination="after t successful additions",
        invariants="occupied cells never become empty; the cluster remains connected",
        witness="the occupied-cell set after each addition",
        params=[("step count t", "Number of successful growth steps.", ["U006721", "U006722"])],
        variants=[
            ("type B Eden model", "Choose a cluster cell, then one of its neighbors; retry occupied choices.", ["U006721", "U006722", "U006724"]),
            ("type A Eden model", "Choose directly from all empty cells adjacent to the cluster.", ["U006724", "U006725"]),
        ],
        images=[("A000685", "CONTEXTUAL", "The cluster/plot composite documents residual lattice anisotropy at increasing scales.")],
    ),
    C(
        "generalized aggregation model",
        "U006727",
        ["U006727", "U006728", "U006729", "U006730", "U006731", "U006732", "U006733", "U006734", "U006735"],
        template="stochastic",
        carrier="an occupied lattice cluster",
        state="the complete cell configuration",
        law="randomly add a cell only at positions whose neighborhoods match an allowed template",
        support="one- or two-dimensional lattices",
        topology="a local lattice with four or eight neighbors in stated cases",
        alphabet="two or more cell colors",
        seed="a finite initial configuration",
        boundary=None,
        external="fresh random choices among proposed/eligible additions",
        frontier="positions adjacent to or otherwise eligible around the cluster",
        schedule="one accepted addition per step",
        read="the local neighborhood template at a proposed position",
        write="add/color one cell if its template is allowed",
        result="a growing cluster, possibly blocked",
        successor="a measure over allowed additions; zero successors if blocked",
        determinism="stochastic branching constrained by the selected rule",
        termination="requested step count or no eligible growth site",
        witness="the complete cluster and whether growth remains possible",
        params=[("rule code", "Rules are numbered by the stated neighborhood-offset scheme.", ["U006727", "U006728"])],
        variants=[
            ("symmetric four-neighbor family", "32 symmetric rules, 16 of which grow from any seed.", ["U006727"]),
            ("rule 2 line-growth extreme", "Only the one-black-neighbor template is allowed.", ["U006727"]),
            ("eight-neighbor totalistic constraint 242", "Allow growth except at exactly 1, 3, or 4 occupied neighbors.", ["U006729", "U006730"]),
            ("image rule 4531", "A construction-bearing panel explicitly labels rule 4531.", ["U006728"]),
            ("image rule 10779", "A construction-bearing panel explicitly labels rule 10779.", ["U006728"]),
            ("image rule 15320", "A construction-bearing panel explicitly labels rule 15320.", ["U006728"]),
            ("image rule 64881", "A construction-bearing panel explicitly labels rule 64881.", ["U006728"]),
            ("image rule 65415", "A construction-bearing panel explicitly labels rule 65415.", ["U006728"]),
            ("1D template family", "Four one-dimensional template systems are shown, including the Eden analog.", ["U006734", "U006735"]),
        ],
        images=[
            ("A000710", "DIRECT_PARTIAL_MECHANICS", "The original-resolution composite transcribes rule labels 4531, 10779, 15320, 64881, and 65415."),
            ("A000702", "CONTEXTUAL", "The six-step row shows blocking and later successful growth under totalistic constraint 242."),
            ("A000700", "CONTEXTUAL", "The five-step row shows a successful irregular cluster approaching a rough circle."),
            ("A000711", "DIRECT_PARTIAL_MECHANICS", "The four-panel row preserves the one-dimensional neighborhood templates and their growth profiles."),
        ],
        uncertainties=["The rule-number decoding scheme is only cross-referenced, and the boundary convention is not stated in this bundle."],
    ),
    C(
        "diffusion-limited aggregation",
        "U006736",
        ["U006736", "U006737", "U006738", "U006739"],
        template="stochastic",
        carrier="an occupied cluster and one incoming random walker",
        state="the cluster plus the current walk position",
        law="start a random walk far from the cluster and attach a cell where the walk first lands adjacent to the cluster",
        support="a lattice around the cluster",
        topology="global unbounded lattice probing a local cluster",
        alphabet="empty/occupied cells plus walker position",
        seed="an initial cluster",
        boundary="walker launch and outer-boundary handling are not specified",
        external="fresh random-walk direction choices",
        frontier="the incoming walker, then its first adjacent landing site",
        schedule="complete one walk and attachment before launching the next",
        read="the walk neighborhood and global cluster adjacency",
        write="add one cell at the first adjacent landing",
        result="a branching aggregate",
        successor="a measure over possible attachment sites",
        determinism="stochastic",
        termination="after the requested particle count",
        witness="the cluster after each attachment",
        aliases=["DLA"],
        images=[
            ("A000707", "CONTEXTUAL", "The referenced DLA image shows a 1000-step branching cluster."),
            ("A000721", "CONTEXTUAL", "A second referenced image shows the same construction at larger display scale."),
        ],
        uncertainties=["The walker launch radius and kill/restart policy are not supplied."],
    ),
    C(
        "aggregation cellular automaton code 746",
        "U006740",
        ["U006740", "U006741", "U006743"],
        template="deterministic_partial",
        carrier="a two-dimensional cellular-automaton configuration",
        state="the complete cell grid",
        law="iterate cellular-automaton code 746",
        support="a 2D lattice",
        topology="the neighborhood encoded by the externally cross-referenced numbering scheme",
        alphabet=None,
        seed="a finite seed; the comparison text associates the first displayed other-rule seed with 7 cells",
        boundary=None,
        external="none",
        frontier="all cells or the active growth region; not stated exactly",
        schedule="discrete cellular-automaton steps",
        read=None,
        write=None,
        result="a growing pattern with persistent small anisotropy",
        successor="one for a fixed complete rule and seed",
        determinism="deterministic",
        termination="nonterminating growth",
        witness="the complete pattern and angular-radius plots",
        params=[("rule code", "746.", ["U006740", "U006743"])],
        images=[("A000701", "DIRECT_PARTIAL_MECHANICS", "The original-resolution composite labels steps 500, 1000, 2000, and 20000 and angular anisotropy plots.")],
        uncertainties=["The local rule table, alphabet, boundary, and exact seed geometry are not present in the assigned notes."],
    ),
    C(
        "other aggregation cellular-automaton code family",
        "U006742",
        ["U006742", "U006743"],
        template="deterministic_partial",
        carrier="two-dimensional cellular-automaton configurations",
        state="the complete cell grid",
        law="iterate each of the explicitly labeled rule codes 29408, 175850, and 174826",
        support="a 2D lattice",
        topology="the neighborhood encoded by an external numbering scheme",
        alphabet=None,
        seed="rows of respectively 6, 7, and 11 cells for the three non-746 panels",
        boundary=None,
        external="none",
        frontier="all cells or the active growth region; not stated exactly",
        schedule="10,000 discrete steps in the comparison",
        read=None,
        write=None,
        result="a growing pattern with a smooth noncircular boundary; code 174826 keeps changing internally",
        successor="one for each fixed rule and seed",
        determinism="deterministic",
        termination="nonterminating growth",
        witness="the complete pattern at 10,000 steps",
        variants=[
            ("code 29408", "Second panel; starts from a row of 6 cells.", ["U006742", "U006743"]),
            ("code 175850", "Third panel; starts from a row of 7 cells.", ["U006742", "U006743"]),
            ("code 174826", "Fourth panel; starts from a row of 11 cells and its interior continues changing.", ["U006742", "U006743"]),
        ],
        images=[("A000728", "DIRECT_PARTIAL_MECHANICS", "The original-resolution row transcribes codes 746, 29408, 175850, and 174826.")],
        uncertainties=["The rule tables, alphabets, neighborhoods, and boundary conditions are absent from the assigned notes."],
    ),
    C(
        "tensor and multipole isotropy analyzer",
        "U006744",
        ["U006744", "U006745", "U006746", "U006747", "U006748", "U006749", "U006750"],
        template="declarative",
        carrier="a finite point set or a continuous-system expression whose directional symmetry is to be tested",
        state="N/A",
        law="for a point list v, sum rank-n outer products of each position, compare the result with the displayed ideal d-dimensional isotropic tensor, and optionally test rank-4 beta ratios or multipole sums; for a continuous PDE expression, require coordinates to appear only through nabla",
        support="Euclidean coordinate space in dimension d and tensor or multipole orders n",
        topology="Euclidean geometry with rotations and the symmetry group of any underlying lattice",
        alphabet="real coordinate vectors, tensor components, complex multipole values, and Boolean or numeric anisotropy results",
        input_value="point positions v with dimension d and rank/order n, or a continuous PDE expression for the stated criterion",
        boundary="the complete supplied point set or expression",
        external="none",
        result="a point-set moment tensor and isotropy comparison, a beta/multipole anisotropy test, or the stated continuous-expression criterion",
        determinism="deterministic for fixed inputs",
        witness="proportionality to the ideal isotropic tensor, beta=3 for the stated rank-4 2D ratio, vanishing nonzero-order multipoles, or coordinate occurrence only through nabla",
        params=[
            (
                "dimension d",
                "Selects the ideal target tensor and the available lattice-symmetry restrictions.",
                ["U006746", "U006747", "U006748"],
            ),
            (
                "tensor or multipole order n",
                "Selects the moment rank or order being tested.",
                ["U006744", "U006745", "U006746", "U006747", "U006748"],
            ),
            (
                "rank-4 component ratio beta",
                "For 2D rank-4 isotropy the {1,1,1,1} to {1,1,2,2} ratio must be 3.",
                ["U006748", "U006749"],
            ),
        ],
        variants=[
            (
                "point-set tensor transform",
                "Sum the rank-n outer product of every position vector.",
                ["U006744", "U006745"],
            ),
            (
                "ideal isotropic tensor comparison",
                "Compare the point-set tensor with the displayed d-dimensional target tensor.",
                ["U006746", "U006747", "U006748"],
            ),
            (
                "beta component-ratio test",
                "Use the rank-4 beta ratio, whose isotropic target is 3 in the stated 2D case.",
                ["U006748", "U006749"],
            ),
            (
                "multipole test",
                "Sum r_i Exp[i n theta_i] in 2D, or the stated higher-dimensional harmonic analogs; only order zero may remain nonzero for isotropy.",
                ["U006748"],
            ),
            (
                "continuous-PDE coordinate criterion",
                "Require coordinates to occur only through nabla in the continuous expression.",
                ["U006750"],
            ),
        ],
        uncertainties=[
            "The source supplies exact point-set tensor formulas and criteria but does not prescribe a tolerance for approximate numerical isotropy."
        ],
    ),
    C(
        "flat-domain-interface rule-150 process",
        "U006751",
        ["U006751"],
        template="deterministic_partial",
        carrier="the cell layer immediately beside a flat black/white domain interface",
        state="the colors in that one-dimensional interface layer",
        law="the layer evolves as elementary cellular automaton rule 150",
        support="an infinitely long flat interface in a 2D cellular automaton",
        topology="a one-dimensional layer embedded along the interface",
        alphabet="{black,white}",
        seed="an interface-layer pattern induced by the surrounding domains",
        boundary="infinite interface; a 90-degree corner acts as a reflecting boundary",
        external="none",
        frontier="the interface layer",
        schedule="synchronous effective rule-150 steps",
        read="the elementary three-cell neighborhood implied by rule 150",
        write="replace each interface-layer cell by the rule-150 output",
        result="the evolving interface layer and shrinking protrusions",
        successor="one",
        determinism="deterministic",
        termination="protrusions eventually leave a residual layer pattern; the process itself need not halt",
        witness="the interface-layer configuration",
        variants=[("corner-reflection variant", "A 90-degree corner supplies a reflecting boundary.", ["U006751"])],
    ),
    C(
        "two-dimensional domain cellular-automaton family",
        "U006752",
        ["U006752"],
        template="deterministic_partial",
        carrier="a two-dimensional black/white cellular-automaton grid",
        state="the complete cell configuration",
        law="iterate one of the named 4-neighbor or 8-neighbor totalistic/outer-totalistic rule codes",
        support="a 2D lattice",
        topology="four- or eight-neighbor lattice according to the variant",
        alphabet="{black,white}",
        seed="an initial black/white configuration",
        boundary=None,
        external="none",
        frontier="all cells",
        schedule="synchronous steps",
        read="the neighborhood encoded by the named totalistic rule",
        write="replace every cell by its rule output",
        result="black/white domains and their boundaries",
        successor="one",
        determinism="deterministic",
        termination="nonterminating",
        witness="the domain configuration and clarity of its boundaries",
        variants=[
            ("4-neighbor totalistic code 52", "Direct 4-neighbor analog of the illustrated domain rule.", ["U006752"]),
            ("4-neighbor outer-totalistic codes", "Codes 111, 293, 295, and 920.", ["U006752"]),
            ("8-neighbor totalistic code 976", "The rule with the clearest domain boundaries.", ["U006752"]),
        ],
        uncertainties=["Exact decoded rule tables and boundary conditions are not in the assigned notes."],
    ),
    C(
        "Cahn-Hilliard spinodal-decomposition model",
        "U006753",
        ["U006753"],
        template="continuous_partial",
        carrier="a continuous composition/order-parameter field",
        state="the field over space",
        law="the named Cahn-Hilliard equation models separation into coarsening black/white regions",
        support="continuous space",
        topology="spatial continuum",
        alphabet="continuous field values",
        seed="a mixed initial field",
        boundary=None,
        external="none stated",
        frontier="the entire field",
        schedule="continuous time",
        read=None,
        write=None,
        result="coarsening domains with average droplet radius approximately t^(1/3)",
        successor="one for fixed equation, parameters, and initial/boundary data",
        determinism="deterministic in the named PDE model",
        termination="nonterminating coarsening",
        witness="the composition field and droplet-size scaling",
        uncertainties=["The equation, parameters, and boundary conditions are not written in this notes unit."],
    ),
    C(
        "binary next-nearest-neighbor transition cellular-automaton family",
        "U006755",
        ["U006755"],
        template="deterministic_partial",
        carrier="a one-dimensional binary cellular-automaton row",
        state="the complete row",
        law="iterate one of the explicitly numbered rules depending on next-nearest neighbors",
        support="a 1D lattice",
        topology="radius-2 neighborhood",
        alphabet="{0,1}",
        seed="a random row at a selected black-cell density",
        boundary=None,
        external="none",
        frontier="all cells",
        schedule="synchronous steps",
        read="two cells on each side plus the cell itself",
        write="replace every cell by the decoded rule output",
        result="a discrete density-dependent transition between phases",
        successor="one",
        determinism="deterministic",
        termination="nonterminating",
        witness="the spacetime pattern under varying initial density",
        variants=[
            ("rule 4196304428", "Displayed first example.", ["U006755"]),
            ("rule 4262364716", "Named next-nearest-neighbor example.", ["U006755"]),
            ("rule 4268278316", "Named next-nearest-neighbor example.", ["U006755"]),
            ("rule 4266296876", "Named next-nearest-neighbor example.", ["U006755"]),
        ],
        uncertainties=["The numbering decode and boundary convention are not present in the assigned notes."],
    ),
    C(
        "Gacs-Kurdyumov-Levin seven-neighbor cellular automaton",
        "U006755",
        ["U006755", "U006756"],
        template="deterministic",
        carrier="a one-dimensional binary row",
        state="the complete row",
        law="output 1 iff the conditional sum a1+a3+a4 (when a4=1) or a4+a5+a7 (when a4=0) is at least 2",
        support="a 1D lattice",
        topology="radius-3 neighborhood",
        alphabet="{0,1}",
        seed="an initial binary row",
        boundary=None,
        external="none",
        frontier="all cells",
        schedule="synchronous steps",
        read="seven consecutive cells a1 through a7",
        write="replace the center cell by the conditional majority output",
        result="a binary cellular-automaton history with reliable phase correction/transition behavior",
        successor="one",
        determinism="deterministic",
        termination="nonterminating",
        witness="the complete spacetime history",
        uncertainties=["The boundary convention and the exact displayed initial conditions are not supplied."],
    ),
    C(
        "four-color transition cellular automaton code 294869764523995749814890097794812493824",
        "U006757",
        ["U006757", "U006758"],
        template="deterministic_partial",
        carrier="a one-dimensional four-color cellular-automaton row",
        state="the complete row",
        law="iterate rule number 294869764523995749814890097794812493824",
        support="a 1D lattice",
        topology=None,
        alphabet="four colors",
        seed="random rows at the displayed 40%, 45%, 55%, and 60% black fractions",
        boundary=None,
        external="none",
        frontier="all cells",
        schedule="synchronous steps",
        read=None,
        write=None,
        result="a sharp density-dependent transition",
        successor="one",
        determinism="deterministic",
        termination="nonterminating",
        witness="the spacetime diagrams under the four initial densities",
        images=[("A000733", "DIRECT_PARTIAL_MECHANICS", "The original-resolution four-panel row labels initial fractions 40%, 45%, 55%, and 60% black.")],
        uncertainties=["The rule-number decode, neighborhood, boundary, and mapping of all four colors are not in the assigned notes."],
    ),
    C(
        "two-dimensional transition cellular-automaton family",
        "U006759",
        ["U006759"],
        template="deterministic_partial",
        carrier="a two-dimensional binary cellular-automaton grid",
        state="the complete grid",
        law="iterate a named four-neighbor totalistic or probabilistic transition rule",
        support="a 2D lattice",
        topology="four-neighbor lattice",
        alphabet="{black,white}",
        seed="a random configuration at a selected density",
        boundary=None,
        external="none for deterministic codes; fresh choices for the probabilistic variant",
        frontier="all cells",
        schedule="synchronous steps",
        read="the cell and/or four immediate neighbors as encoded by the rule",
        write="replace each cell by the selected rule output",
        result="fixed domains or a discrete transition depending on the rule",
        successor="one for deterministic codes; a measure for the probabilistic variant",
        determinism="variant-dependent deterministic or stochastic",
        termination="nonterminating",
        witness="the complete spacetime evolution and phase selected",
        variants=[
            ("4-neighbor totalistic code 56", "A majority-style rule that yields fixed regions rather than the discrete transition.", ["U006759"]),
            ("4-neighbor totalistic code 52", "An alternative to the second transition rule.", ["U006759"]),
            ("probabilistic Toom variant", "A probabilistic version of the first rule; probabilities are not supplied.", ["U006759"]),
        ],
        uncertainties=["The main illustrated rules, their decoded tables, probabilities, and boundary conditions are outside this bundle."],
    ),
    C(
        "microcanonical fixed-energy Ising measure",
        "U006766",
        ["U006762", "U006763", "U006764", "U006765", "U006766", "U006767", "U006768", "U006769", "U006770", "U006771", "U006772", "U006773", "U006774", "U006781", "U006782", "U006784"],
        template="declarative",
        carrier="an n by n square array of spins",
        state="a complete spin configuration s",
        law="condition on a specified value of the four-neighbor Ising energy e[s] and give equal weight to all configurations at that energy",
        support="finite square grids and the n->infinity limit",
        topology="2D square lattice with cyclic boundary in the finite enumeration",
        alphabet="{+1,-1}",
        input_value="array size n and a fixed total energy or energy density",
        boundary="cyclic boundary conditions in the finite enumeration",
        invariants="the selected energy is fixed throughout the ensemble",
        result="a fixed-energy probability measure and its induced magnetization distribution",
        determinism="a probability measure, not a native time evolution",
        witness="the distribution of m[s] over all configurations at fixed e[s] and its sharp limiting branches",
        params=[
            ("array size n", "The carrier is n by n and the sharp transition is an n->infinity limit.", ["U006766", "U006767"]),
            ("fixed energy density e", "The critical value in the stated normalization is -sqrt(2).", ["U006768", "U006772"]),
        ],
        variants=[
            (
                "finite exhaustive fixed-energy measure",
                "Enumerate all cyclic n by n configurations at a specified energy and measure their magnetizations.",
                ["U006766", "U006767"],
            ),
            (
                "infinite-size limiting measure",
                "Take n to infinity, where the magnetization distribution becomes sharp.",
                ["U006766", "U006768", "U006772"],
            ),
        ],
        images=[("A000738", "CONTEXTUAL", "The finite-n and limiting energy/magnetization panels visualize the fixed-energy measure.")],
        uncertainties=[
            "The source first defines m[s] as the sum of +/-1 spins but later calls m a +1-cell density and states m=p; that observable normalization is conflicting."
        ],
        conflicting_fields=["witness_semantics"],
        conflict_sources=["U006781", "U006782", "U006784"],
    ),
    C(
        "canonical Boltzmann-weight Ising measure",
        "U006773",
        ["U006762", "U006763", "U006764", "U006765", "U006768", "U006769", "U006770", "U006771", "U006772", "U006773", "U006774", "U006781", "U006782", "U006784"],
        template="declarative",
        carrier="an n by n square array of spins",
        state="a complete spin configuration s",
        law="assign each spin configuration the canonical weight Exp[-beta e[s]], where e[s] is the four-neighbor Ising energy",
        support="finite square grids and the n->infinity limit",
        topology="a 2D four-neighbor square lattice",
        alphabet="{+1,-1}",
        input_value="array size n and inverse temperature beta",
        boundary=None,
        result="the canonical probability measure over spin configurations and its induced observables",
        determinism="a probability measure, not a native time evolution",
        witness="canonical averages that agree in the n->infinity limit with the stated fixed-energy results for most quantities",
        params=[
            ("array size n", "The thermodynamic comparison is stated in the n->infinity limit.", ["U006773"]),
            ("inverse temperature beta", "Sets the configuration weight Exp[-beta e[s]] and parametrizes the exact magnetization/energy formulas.", ["U006769", "U006771", "U006773"]),
        ],
        uncertainties=[
            "The source first defines m[s] as the sum of +/-1 spins but later calls m a +1-cell density and states m=p; that observable normalization is conflicting.",
            "The finite-grid boundary and explicit normalization of the stated Exp[-beta e[s]] weights are not supplied for this canonical measure.",
        ],
        conflicting_fields=["witness_semantics"],
        conflict_sources=["U006781", "U006782", "U006784"],
    ),
    C(
        "Ising heat-bath Monte Carlo sampler",
        "U006775",
        ["U006773", "U006774", "U006775"],
        template="stochastic_partial",
        carrier="a finite square array of Ising spins plus a random spin-flip sampler",
        state="the current complete spin configuration",
        law=None,
        support="a finite square lattice",
        topology="the four-neighbor square-lattice energy model",
        alphabet="{+1,-1}",
        seed=None,
        input_value="inverse temperature beta or the corresponding target canonical weights",
        boundary=None,
        external="random spin choices and random heat-bath decisions",
        frontier="the spin selected for the next proposal",
        schedule="repeated random spin-flip proposals; the sweep convention is not stated",
        read=None,
        write="flip the selected spin when the unspecified heat-bath procedure accepts the proposal",
        result="a stochastic trajectory of spin configurations intended to sample the canonical measure",
        successor="a probability measure over an unchanged or spin-flipped next configuration",
        determinism="stochastic",
        termination=None,
        witness="empirical configuration frequencies approaching the target canonical probabilities",
        params=[
            (
                "inverse temperature beta",
                "Determines the target canonical configuration weights Exp[-beta e[s]].",
                ["U006773"],
            )
        ],
        uncertainties=[
            "The source names random spin flipping and the heat-bath interpretation but supplies no proposal distribution, acceptance probability, sweep convention, seed, boundary, or stopping rule."
        ],
        unknown_fields={
            "rule_relation_constraint_function_or_probability_law": "The in-scope source does not supply the heat-bath spin-flip acceptance law.",
            "read_dependencies_or_neighborhood": "The in-scope source does not state which local or global quantities the heat-bath decision reads.",
        },
    ),
    C(
        "deterministic checkerboard Ising cellular automaton",
        "U006776",
        ["U006776", "U006777", "U006778", "U006779", "U006780", "U006781", "U006782", "U006783", "U006784", "U006785", "U006787"],
        template="deterministic",
        carrier="a binary 2D array plus a checkerboard mask",
        state="the spin array and the current checkerboard mask",
        law="on the active checkerboard, flip a spin exactly when its four-neighbor sum is 2 and the mask is 1; complement the mask each step",
        support="a 2D square lattice",
        topology="four-neighbor square lattice",
        alphabet="the code uses {0,1} spins plus a {0,1} mask",
        seed="an initial random spin array and Mask[list]",
        boundary="ListConvolve boundary argument 2 as written",
        external="none",
        frontier="alternating checkerboard sublattices",
        schedule="update one checkerboard synchronously, then swap masks",
        read="the current spin, four-neighbor sum, and mask bit",
        write="conditionally replace spin by 1-spin; replace mask by 1-mask",
        result="an energy-conserving spin history",
        successor="one",
        determinism="deterministic",
        termination="nonterminating",
        invariants="the stated Ising energy e[s] is conserved",
        control="the alternating checkerboard mask",
        witness="the full spin/mask evolution and long-time magnetization observable",
        params=[
            ("initial +1/black fraction p", "Used to sample different conserved energies.", ["U006781", "U006782", "U006784"]),
            ("system size", "The experiment uses a 500 by 500 array.", ["U006782"]),
            ("observation times", "Plots use 0, 10, 100, and 1000 steps.", ["U006782", "U006784"]),
        ],
        images=[
            ("A000739", "CONTEXTUAL", "The m-versus-p/e plots document finite-time approach to the transition."),
            ("A000740", "CONTEXTUAL", "The slices/configurations show outcomes at initial black fractions from 5% through 95%."),
        ],
        uncertainties=["The p/m statement conflicts with the earlier +/-1 magnetization definition: the source says m=p where normalized spin sum would be 2p-1."],
        conflicting_fields=["witness_semantics", "parameters_and_variants"],
        conflict_sources=["U006781", "U006782", "U006784"],
    ),
    C(
        "site-percolation model",
        "U006791",
        ["U006791"],
        template="stochastic_declarative",
        carrier="a regular lattice whose sites are independently black with fixed density",
        state="a complete random black/white lattice configuration",
        law="fill sites at random at density p and test whether a connected black cluster spans the lattice",
        support="an infinite-size lattice limit",
        topology="square or triangular lattice; directed connectivity in a variant",
        alphabet="{black,white}",
        seed="N/A",
        input_value="site density p and lattice/connection convention",
        boundary="spanning is defined relative to finite approximants; exact boundary convention is not stated",
        external="independent random site draws",
        frontier="N/A",
        schedule="N/A",
        read="site colors and nearest-neighbor connectivity",
        write="N/A",
        result="the probability of a spanning connected cluster",
        successor="a probability measure over configurations",
        determinism="stochastic measure with a deterministic connectivity predicate",
        termination="N/A",
        witness="existence of a spanning cluster",
        params=[("site density p", "Critical p is about 0.592746 on square and exactly 1/2 on triangular lattices.", ["U006791"])],
        variants=[
            ("square-lattice site percolation", "Critical density about 0.592746.", ["U006791"]),
            ("triangular-lattice site percolation", "Critical density exactly 1/2.", ["U006791"]),
            ("directed percolation", "Connectivity is counted only in one direction.", ["U006791"]),
        ],
    ),
    C(
        "well-mixed chemical rate-equation relation",
        "U006792",
        ["U006792"],
        template="declarative",
        carrier="species-density variables and reaction-rate expressions",
        state="N/A",
        law="reaction rates are proportional to products of reactant densities; equilibrium is the polynomial condition that opposing rates balance",
        support="well-mixed density space",
        topology="N/A",
        alphabet="nonnegative real densities",
        input_value="reaction stoichiometry, rate constants, and parameters",
        result="the set of equilibrium density solutions",
        determinism="a declarative polynomial relation",
        witness="a density vector satisfying all balance equations",
        variants=[("cellular-automaton mean-field equilibrium", "For the page-339 automaton, p == p^2(3-2p), yielding 0, 1/2, and 1.", ["U006792"])],
        uncertainties=["The source warns that spatial correlations can invalidate this well-mixed approximation."],
    ),
    C(
        "binary ring adjacency-violation cost function",
        "U006800",
        ["U006800", "U006801", "U006802", "U006805"],
        template="declarative",
        carrier="a finite binary cyclic list",
        state="N/A",
        law="Cost[list] is the sum of Abs[list-RotateLeft[list]], counting adjacent inequality violations",
        support="a finite ring of list positions",
        topology="one-dimensional cycle",
        alphabet="{0,1}",
        input_value="a binary list",
        boundary="cyclic via RotateLeft",
        result="a nonnegative integer violation count",
        determinism="deterministic function",
        witness="Cost[list], with zero accepting the equality constraint",
        params=[("list length n", "All 2^n binary lists are enumerated in the displayed distribution.", ["U006805"])],
    ),
    C(
        "greedy single-bit constraint-improvement process",
        "U006802",
        ["U006802", "U006803", "U006804", "U006807"],
        template="stochastic",
        carrier="a finite binary cyclic list",
        state="the current list",
        law="choose one random position, flip it, and retain the proposal only when its Cost is lower (or no greater in the variant)",
        support="a finite ring of list positions",
        topology="one-dimensional cycle",
        alphabet="{0,1}",
        seed="an initial binary list",
        boundary="cyclic cost function",
        external="one fresh random position per iteration",
        frontier="the sampled position",
        schedule="one proposal/acceptance decision per step",
        read="the current list, proposed flip, and both costs",
        write="commit the proposal if the selected inequality holds; otherwise retain the current list",
        result="a nonincreasing-cost trajectory",
        successor="a measure over retained or accepted next lists",
        determinism="stochastic proposal with deterministic acceptance",
        termination="FixedPoint behavior or an external step limit; exact stopping rule is not specified",
        invariants="strict variant never increases Cost; non-strict variant also never increases it",
        witness="the list/cost trajectory and any zero-cost result",
        variants=[
            ("strict improvement", "Accept only Cost[proposal] < Cost[current].", ["U006803"]),
            ("non-worsening improvement", "Replace < by <=.", ["U006804"]),
        ],
        uncertainties=["The displayed Move function is one step; a complete outer iteration/stopping wrapper is not supplied."],
    ),
    C(
        "gradient-descent iteration",
        "U006808",
        ["U006808", "U006809", "U006810"],
        template="deterministic",
        carrier="a point x in the domain of a differentiable function f",
        state="the current iterate x",
        law="x -> x-a f'(x), iterated to a FixedPoint",
        support="the function's smooth domain",
        topology="continuous state space",
        alphabet="real or compatible numeric values",
        seed="initial point x0",
        input_value="function f and step size a",
        boundary="function-domain dependent",
        external="none",
        frontier="the current iterate",
        schedule="one derivative step per iteration",
        read="x, f'(x), and a",
        write="replace x by x-a f'(x)",
        result="a fixed point, typically a local minimum",
        successor="one",
        determinism="deterministic",
        termination="when FixedPoint convergence criterion is met; criterion is implementation-defined",
        witness="the returned fixed point and its objective value",
        params=[
            ("step size a", "Controls overshoot and the reached basin.", ["U006809", "U006810"]),
            ("initial point x0", "Selects the trajectory/basin.", ["U006809", "U006810"]),
        ],
    ),
    C(
        "Newton root-finding iteration",
        "U006810",
        ["U006810", "U006811"],
        template="deterministic",
        carrier="a point x in the domain of f and f'",
        state="the current iterate x",
        law="x -> x-f(x)/f'(x), iterated to a FixedPoint",
        support="the function's differentiable domain excluding zero derivatives",
        topology="continuous state space",
        alphabet="real or compatible numeric values",
        seed="initial point x0",
        input_value="function f",
        boundary="undefined where f'(x)=0 or evaluation leaves the domain",
        external="none",
        frontier="the current iterate",
        schedule="one Newton update per iteration",
        read="x, f(x), and f'(x)",
        write="replace x by x-f(x)/f'(x)",
        result="a fixed point corresponding to a root when convergence succeeds",
        successor="one where defined",
        determinism="deterministic",
        termination="when FixedPoint convergence criterion is met or evaluation fails",
        witness="the returned iterate and whether f is zero there",
        params=[("initial point x0", "Selects the Newton trajectory.", ["U006810", "U006811"])],
    ),
    C(
        "simulated-annealing optimization process",
        "U006812",
        ["U006812"],
        template="stochastic_partial",
        carrier="a discrete candidate solution and its objective value",
        state="the current candidate plus the current acceptance/temperature setting",
        law="propose changes and sometimes accept moves away from the minimum, starting with high probability and progressively decreasing it",
        alphabet="problem-specific candidate configurations",
        seed="an initial candidate and high initial acceptance probability",
        input_value="objective function, proposal mechanism, and cooling schedule",
        boundary="problem-specific",
        external="random proposals and acceptance draws",
        frontier="the proposed local or block change",
        schedule="iterative proposals under a decreasing acceptance schedule",
        read="current/proposed objective values and current schedule value",
        write="accept or reject the proposal",
        result="a low-objective candidate",
        successor="a probability measure over accepted/rejected next states",
        determinism="stochastic",
        termination="external schedule/step limit",
        witness="the best/final objective and candidate",
        uncertainties=["No explicit acceptance-probability formula, proposal distribution, or cooling schedule is supplied."],
    ),
    C(
        "population-based genetic optimization process",
        "U006813",
        ["U006813"],
        template="stochastic_partial",
        carrier="a population of encoded candidate solutions",
        state="the current population and evaluated fitness/constraint performance",
        law="maintain a population, select better candidates, and use sex-like large-scale mixing to create new candidates",
        alphabet="problem-specific genetic encodings",
        seed="an initial population",
        input_value="fitness/constraint evaluator and reproduction operators",
        boundary="problem-specific",
        external="random selection/mixing choices",
        frontier="the selected parents and produced offspring",
        schedule="generation by generation",
        read="population encodings and evaluated performance",
        write="form the next population",
        result="a population containing improved candidates",
        successor="a probability measure over next populations",
        determinism="stochastic",
        termination="external generation or performance criterion",
        witness="the best candidate and population performance",
        aliases=["genetic algorithm"],
        uncertainties=["The source supplies no selection probabilities, encoding, mutation law, replacement policy, or stopping criterion."],
    ),
    C(
        "incremental unequal-circle packing procedure",
        "U006814",
        ["U006814", "U006815", "U006816", "U006817", "U006818", "U006819"],
        template="deterministic_partial",
        carrier="a planar collection of unequal circles and their contact network",
        state="all placed circle centers, radii, and tangencies",
        law="add each new circle so that it immediately touches two existing circles",
        support="the plane",
        topology="a growing tangency graph embedded in 2D",
        alphabet="real centers/radii and graph contacts",
        seed=None,
        input_value="a circle-size sequence or size ratio",
        boundary=None,
        external="none stated",
        frontier="the next circle and candidate gap",
        schedule="one circle placement per step",
        read="the existing packing and chosen new radius",
        write="insert a circle tangent to two existing circles",
        result="a circle packing and contact network",
        successor="not determined because gap/tie selection is unspecified",
        determinism=None,
        termination="after the supplied circles are placed",
        witness="centers, contacts, and filling fraction",
        params=[("circle-size ratio", "The panels vary the ratio and measure contact distributions.", ["U006816", "U006817"])],
        images=[
            ("A000001", "CONTEXTUAL", "The contact-network row shows packings across size ratios."),
            ("A000002", "CONTEXTUAL", "The histogram row shows contact-count distributions."),
            ("A000003", "CONTEXTUAL", "The row shows the large-scale effect of one central size change."),
        ],
        uncertainties=["The initial packing, next-circle radius sequence, gap selection, tie-breaking, and outer boundary are not supplied."],
    ),
    C(
        "Apollonian circle-packing construction",
        "U006820",
        ["U006820", "U006821", "U006822", "U006823"],
        template="deterministic",
        carrier="a planar packing of mutually tangent circles and its triangular gaps",
        state="the complete set of circles and tangencies",
        law="repeatedly inscribe in every eligible gap the circle tangent to the three surrounding circles, using the stated radius formula",
        support="the plane inside the initial bounding configuration",
        topology="a recursively refined tangency graph",
        alphabet="real circle centers and radii",
        seed="an initial mutually tangent circle configuration",
        input_value="N/A",
        boundary="the initial bounding circles/gaps",
        external="none",
        frontier="all current three-circle gaps selected for the next cycle",
        schedule="synchronous refinement cycles",
        read="the radii and positions of each touching triple",
        write="insert the unique inscribed tangent circle",
        result="a recursively refined circle packing",
        successor="one for a fixed initial configuration and all-gaps schedule",
        determinism="deterministic",
        termination="nonterminating in the limit; finite after any requested cycle",
        invariants="previous circles and tangencies are retained",
        witness="the circle/tangency set at a given cycle",
        params=[("cycle t", "Adds 3^(t-1) circles per original circle at cycle t.", ["U006820"])],
        images=[("A000004", "CONTEXTUAL", "The six-step row depicts repeated inscribed-circle refinement.")],
    ),
    C(
        "sphere-packing constraint problem",
        "U006824",
        ["U006824", "U006825", "U006826", "U006827"],
        template="constraint",
        carrier="collections of nonoverlapping equal spheres",
        state="N/A",
        law="accept arrangements with nonoverlapping sphere interiors and optimize occupied-space density",
        support="Euclidean space in the selected dimension",
        topology="dimension-dependent continuous space",
        alphabet="sphere-center coordinates",
        input_value="sphere radius/count, dimension, and container or periodicity convention",
        boundary=None,
        result="the feasible packing set or a maximum-density packing",
        determinism="many arrangements may satisfy the constraint; optimization selects maximal density",
        witness="nonoverlap plus the computed density",
        variants=[
            ("3D face-centered cubic packing", "Density pi/sqrt(18), with rhombic-dodecahedral Voronoi cells.", ["U006824"]),
            ("3D hexagonal close packing", "Same density as fcc, with shifted layers and different Voronoi cells.", ["U006824"]),
            ("random sphere packing", "Typical density around 0.64; the generation law is not specified.", ["U006825"]),
            ("higher-dimensional lattice packings", "Includes the E8 and Leech-lattice cases described by their contact counts.", ["U006827"]),
        ],
        uncertainties=["The general container/boundary convention and a constructive optimizer are not supplied."],
    ),
    C(
        "discrete toroidal circle-packing problem",
        "U006828",
        ["U006828", "U006829", "U006830", "U006831"],
        template="constraint",
        carrier="a periodic grid and centers of equal discrete circles",
        state="N/A",
        law="choose as many grid points as possible so that circles of the given diameter centered there do not overlap",
        support="a finite grid that wraps around",
        topology="two-dimensional torus",
        alphabet="{center absent,center present} at each grid point",
        input_value="grid size and diameter sqrt(m^2+n^2)",
        boundary="periodic wraparound",
        result="a maximum-cardinality nonoverlapping placement",
        determinism="a constraint/optimization problem with potentially multiple optima",
        witness="pairwise nonoverlap and maximal center count",
        params=[
            ("grid size", "The complete examples use a 7 by 7 grid.", ["U006830"]),
            ("circle diameter", "Allowed values have form sqrt(m^2+n^2).", ["U006830"]),
        ],
        images=[("A000005", "CONTEXTUAL", "The panel set shows all distinct maximal 7x7 cases for several discrete diameters.")],
    ),
    C(
        "Voronoi-diagram transform",
        "U006832",
        ["U006832", "U006833", "U006834", "U006835"],
        template="declarative",
        carrier="a set of seed points in a metric space",
        state="N/A",
        law="assign each location to the seed point to which it is closer than to any other",
        support="the ambient metric space",
        topology="metric-space geometry, illustrated in 2D and 3D",
        alphabet="seed identities labeling regions",
        input_value="seed-point coordinates and distance metric",
        boundary="ambient-domain dependent",
        result="a partition into nearest-seed regions",
        determinism="deterministic for fixed points, metric, and tie convention",
        witness="each region satisfies the nearest-seed predicate",
        aliases=["Dirichlet tessellation", "Wigner-Seitz cells for repetitive lattices"],
        images=[("A000008", "CONTEXTUAL", "The three-panel diagram shows lattice and irregular nearest-seed partitions.")],
        uncertainties=["The tie convention on equidistant boundaries and finite-domain clipping are not stated."],
    ),
    C(
        "discrete Voronoi cellular automaton",
        "U006836",
        ["U006836", "U006837", "U006838", "U006839", "U006840", "U006841"],
        template="deterministic",
        carrier="a one- or two-dimensional cellular-automaton grid",
        state="all cell values representing expanding regions and collision boundaries",
        law="in 1D apply {{0|1,n:(0|1),0|1}->n,{_,0,_}->2,{_,n_,_}->n-1}; regions grow from black seeds and stop where they meet",
        support="a regular lattice",
        topology="radius-1 1D neighborhood; a 2D analog is shown but not transcribed",
        alphabet="1D rule uses k=3 values",
        seed="initial black seed cells",
        boundary=None,
        external="none",
        frontier="expanding region boundaries",
        schedule="synchronous cellular-automaton steps",
        read="the local neighborhood",
        write="retain 0/1 interiors, create value 2 at growth sites, and decrement other n values",
        result="a discrete nearest-seed partition",
        successor="one",
        determinism="deterministic",
        termination="reaches a fixed partition for finite bounded seed arrangements",
        witness="the final regions and their collision boundaries",
        variants=[
            ("1D k=3 r=1 rule", "The fully transcribed three-clause rule.", ["U006836", "U006837", "U006838"]),
            ("2D analog", "A two-dimensional cellular automaton is shown without a rule table.", ["U006840", "U006841"]),
        ],
        images=[
            ("A000006", "CONTEXTUAL", "The 1D evolution row shows growing regions stopping on contact."),
            ("A000007", "CONTEXTUAL", "The 2D panel sequence shows the analogous discrete partition."),
        ],
        uncertainties=["The boundary convention and the native 2D rule table are not supplied."],
    ),
    C(
        "higher-order Voronoi region construction",
        "U006842",
        ["U006842"],
        template="declarative",
        carrier="a set of seed points in a metric space",
        state="N/A",
        law="partition space by which point is the k-th closest rather than the closest",
        support="the ambient metric space",
        topology="metric-space geometry",
        alphabet="seed identities and order rank k",
        input_value="seed points, metric, and positive integer k",
        boundary="ambient-domain dependent",
        result="the collection of k-th-nearest regions",
        determinism="deterministic for fixed inputs and tie convention",
        witness="the k-th-nearest predicate throughout each region",
        aliases=["higher-order Voronoi diagram", "Brillouin-zone construction"],
        params=[("order k", "Selects closest, second-closest, and higher-order regions.", ["U006842"])],
        uncertainties=["Tie handling and domain clipping are not specified."],
    ),
    C(
        "minimum-boundary deformable-object packing problem",
        "U006843",
        ["U006843"],
        template="constraint",
        carrier="space-filling deformable cells/objects",
        state="N/A",
        law="partition the available space into equal-volume cells while minimizing total interface area",
        support="2D or 3D continuous space",
        topology="planar or spatial adjacency complex",
        alphabet="cell identities and boundary surfaces",
        input_value="dimension, number/volumes of objects, and domain",
        boundary=None,
        result="a minimum-total-boundary partition",
        determinism="multiple feasible arrangements may exist; optimization selects least area",
        witness="space filling, prescribed volumes, and measured total interface area",
        variants=[
            ("2D hexagonal array", "Regular hexagons minimize total boundary for identical deformable objects.", ["U006843"]),
            ("Kelvin bcc tetradecahedra", "A repetitive 14-faced 3D proposal.", ["U006843"]),
            ("Weaire-Phelan structure", "A repetitive mix of 12- and 14-faced cells with lower total area.", ["U006843"]),
        ],
        uncertainties=["The finite/infinite-domain convention and a constructive minimization algorithm are not supplied."],
    ),
    C(
        "PDE linear-stability and dispersion analyzer",
        "U006846",
        ["U006846"],
        template="declarative",
        carrier="a partial differential equation, a basic solution, and infinitesimal perturbation modes",
        state="N/A",
        law="linearize around the basic solution, substitute perturbation modes Exp[i k x] Exp[i omega t], derive the dispersion relation omega(k), classify real, damped, and growing modes by omega, and select the wavelength whose mode has the most negative Im[omega]",
        support="the PDE's spatial domain and its wavenumber/frequency mode space",
        topology="continuous space represented by Fourier modes indexed by k",
        alphabet="symbolic or numeric PDE coefficients, wavenumbers k, and complex frequencies omega",
        input_value="a PDE and a basic solution about which small fluctuations are analyzed",
        boundary=None,
        external="none",
        result="a dispersion relation omega(k), a stability classification over k, and the dominant growing wavelength when one exists",
        determinism="deterministic within the stated linear approximation",
        witness="real omega gives constant-amplitude waves, Im[omega]>0 gives damping, Im[omega]<0 gives growth, and the most-negative imaginary part identifies the fastest-growing mode",
        params=[
            (
                "wavenumber k",
                "Indexes spatial modes and determines wavelength and omega through the dispersion relation.",
                ["U006846"],
            ),
            (
                "basic solution",
                "Fixes the state around which the PDE is linearized.",
                ["U006846"],
            ),
        ],
        variants=[
            (
                "real-frequency mode",
                "Real omega corresponds to an ordinary constant-amplitude wave.",
                ["U006846"],
            ),
            (
                "damped mode",
                "Im[omega]>0 yields exponential damping under the source's Exp[i omega t] convention.",
                ["U006846"],
            ),
            (
                "growing unstable mode",
                "Im[omega]<0 yields exponential growth; the most-negative value grows fastest.",
                ["U006846"],
            ),
        ],
        uncertainties=[
            "The notes give the analysis procedure but no particular PDE, base solution, boundary condition, or concrete dispersion relation."
        ],
    ),
    C(
        "balanced-parentheses language membership and denotation",
        "U006847",
        ["U006847", "U006848", "U006849", "U006850", "U006852", "U006853"],
        template="declarative",
        carrier="finite strings over opening and closing parentheses",
        state="N/A",
        law="accept exactly strings whose parentheses are properly paired and nested, and interpret each accepted string as the corresponding nested-list/expression-tree structure",
        support="finite strings",
        topology="linear string order with a derived parse tree",
        alphabet="{(,)}",
        input_value="a finite parenthesis string",
        boundary="the entire finite string",
        result="a membership truth value and, for an accepted string, its balanced nesting denotation",
        determinism="deterministic membership and denotation relation",
        witness="complete pair annihilation or the equivalent nested-list/expression-tree structure",
        variants=[
            ("nested-list representation", "Balanced strings correspond to nested Mathematica lists/expression trees.", ["U006849"]),
            ("annihilation representation", "Paired structures annihilate to expose the nesting depth.", ["U006847", "U006848", "U006852", "U006853"]),
        ],
        images=[
            ("A000011", "CONTEXTUAL", "The first image shows paired annihilation/nesting."),
            ("A000012", "CONTEXTUAL", "The second image shows equivalent nested structures."),
        ],
    ),
    C(
        "balanced-parentheses count analyzer",
        "U006850",
        ["U006850", "U006851"],
        template="declarative",
        carrier="nonnegative integer size and depth parameters",
        state="N/A",
        law="return Binomial[2 n,n]/(n+1) for all balanced strings with n pairs, or c[{n,n},d]-c[{n,n},d-1] using the displayed recurrence for strings of exact depth d",
        support="nonnegative integer pair counts n and depths d",
        topology="N/A",
        alphabet="nonnegative integer inputs and a nonnegative integer count",
        input_value="pair count n and either all depths or an exact depth d",
        boundary="n and d are finite nonnegative integers, with the displayed recurrence base and invalid-region cases",
        external="none",
        result="one nonnegative integer count",
        determinism="deterministic",
        witness="the Catalan formula value or the exact-depth recurrence difference",
        params=[
            (
                "pair count n",
                "Selects strings of length 2n.",
                ["U006850", "U006851"],
            ),
            (
                "depth d",
                "Selects the exact annihilation/nesting depth for the recurrence variant.",
                ["U006850", "U006851"],
            ),
        ],
        variants=[
            (
                "all-depth Catalan count",
                "For n pairs, return Binomial[2 n,n]/(n+1).",
                ["U006850"],
            ),
            (
                "exact-depth recurrence count",
                "For n pairs and exact depth d, return c[{n,n},d]-c[{n,n},d-1].",
                ["U006850", "U006851"],
            ),
        ],
    ),
    C(
        "two-dimensional sandpile stabilization cellular automaton",
        "U006854",
        ["U006854", "U006855", "U006856", "U006857"],
        template="deterministic",
        carrier="a two-dimensional integer array of relative sand heights",
        state="the complete height array s",
        law="add the 2D discrete Laplacian kernel {{0,1,0},{1,-4,1},{0,1,0}} convolved with UnitStep[s-4]",
        support="a 2D square lattice",
        topology="four-neighbor square lattice",
        alphabet="integer relative heights; stable values are below 4",
        seed="any finite initial height configuration",
        boundary="ListConvolve arguments 2,0 as written",
        external="none",
        frontier="all cells with height at least 4 and their four neighbors",
        schedule="parallel toppling steps",
        read="each height and its four-neighbor toppling contributions",
        write="subtract 4 at every unstable cell and add 1 to each of its four neighbors",
        result="a fixed stable configuration",
        successor="one",
        determinism="deterministic",
        termination="the source states every initial condition eventually reaches all values below 4",
        invariants="total height is conserved under the stated closed accounting, subject to the explicit zero boundary handling",
        witness="FixedPoint[SandStep,s] with all values below 4",
        params=[("threshold", "Topple at height 4.", ["U006855", "U006856"])],
        images=[("A000009", "CONTEXTUAL", "The referenced image shows stabilization over ten steps.")],
    ),
    C(
        "driven sandpile add-and-stabilize cycle",
        "U006858",
        ["U006858", "U006859", "U006860", "U006861", "U006862"],
        template="deterministic",
        carrier="a two-dimensional integer sandpile configuration",
        state="the stable configuration at the start of each drive cycle",
        law="add 4 to the center cell, then repeatedly apply SandStep until FixedPoint; a named variant adds at a random cell",
        support="a 2D square lattice",
        topology="four-neighbor square lattice",
        alphabet="integer heights with stable values below 4",
        seed="an initial stable sandpile",
        boundary="inherits the SandStep boundary",
        external="none for center drive; one random cell choice per cycle in the random-drive variant",
        frontier="the driven cell followed by all unstable cells during the avalanche",
        schedule="drive once, fully stabilize, then begin the next cycle",
        read="current stable array, drive location, and SandStep neighborhoods",
        write="add 4 then commit repeated topplings to a fixed point",
        result="a sequence of stable configurations and avalanche durations",
        successor="one under center drive; a measure under random drive",
        determinism="deterministic center-drive variant, stochastic random-drive variant",
        termination="each cycle ends at a fixed point; the sequence of cycles is externally bounded",
        invariants="after t center additions the stated total value is 4t",
        control="drive-cycle counter and stabilization phase",
        witness="the stable configuration and number of toppling steps per cycle",
        variants=[
            ("center-driven sandpile", "Add 4 at the center each cycle.", ["U006858"]),
            ("randomly driven sandpile", "Add at a random cell each cycle.", ["U006858"]),
        ],
        images=[
            ("A000010", "CONTEXTUAL", "The slice row shows activity at cycles 50 through 58."),
            ("A000018", "CONTEXTUAL", "The four-panel row shows fixed configurations at cycles 25, 50, 100, and 200."),
            ("A000013", "CONTEXTUAL", "The plot reports stabilization/avalanche durations through 200 cycles."),
        ],
    ),
    C(
        "d-dimensional conserved sandpile cellular-automaton family",
        "U006863",
        ["U006863", "U006867"],
        template="deterministic_partial",
        carrier="a d-dimensional integer-valued cellular-automaton configuration",
        state="the complete array s",
        law=None,
        support="a d-dimensional lattice",
        topology=None,
        alphabet="integer values with 2d final values",
        seed="an initial d-dimensional configuration",
        boundary=None,
        external="none",
        frontier=None,
        schedule="discrete cellular-automaton steps",
        read=None,
        write=None,
        result="a d-dimensional sandpile evolution and its final-value configuration",
        successor="one for a fixed complete rule and initial configuration",
        determinism="deterministic",
        termination=None,
        invariants="the total value of s is conserved",
        witness="the complete evolution, including the more complicated behavior stated for some d>1 initial conditions",
        params=[
            (
                "dimension d",
                "Sets the cellular-automaton and final-value counts.",
                ["U006863", "U006867"],
            ),
            (
                "cellular-automaton count k=4d",
                "The source identifies the d-dimensional family as k=4d.",
                ["U006863"],
            ),
            (
                "final-value count 2d",
                "The source states that the generalized family has 2d final values.",
                ["U006863"],
            ),
        ],
        uncertainties=[
            "The source states the dimensional family, k=4d, 2d final values, and conservation law, but does not write the generic d-dimensional local transition, topology, boundary, activation rule, or convergence condition."
        ],
        unknown_fields={
            "rule_relation_constraint_function_or_probability_law": "The in-scope source does not supply the generic d-dimensional sandpile transition rule.",
            "read_dependencies_or_neighborhood": "The in-scope source does not state the generic d-dimensional read neighborhood.",
            "write_replacement_assembly_or_commit": "The in-scope source does not state the generic d-dimensional replacement or commit operation.",
        },
    ),
    C(
        "one-dimensional sandpile stabilization cellular automaton",
        "U006864",
        ["U006863", "U006864", "U006865", "U006866", "U006867"],
        template="deterministic",
        carrier="a one-dimensional integer height list",
        state="the complete height list s",
        law="add ListConvolve[{1,-2,1},UnitStep[s-2],2,0] at each parallel step",
        support="a 1D lattice",
        topology="nearest-neighbor line",
        alphabet="integer heights; stable values are below 2",
        seed="an arbitrary finite initial list or repeated additions at the center",
        boundary="ListConvolve arguments 2,0 as written",
        external="none",
        frontier="all cells of height at least 2 and their neighbors",
        schedule="parallel toppling steps",
        read="each height and nearest-neighbor toppling contributions",
        write="subtract 2 from unstable cells and add 1 to each neighbor",
        result="a fixed stable configuration",
        successor="one",
        determinism="deterministic",
        termination="reaches a fixed point; time is reported to scale roughly as total initial value squared",
        invariants="total height is stated to be conserved in the d-dimensional family",
        witness="a fixed configuration with all values below 2",
        params=[
            (
                "dimension d=1",
                "The one-dimensional specialization has k=4 and 2 final values in the stated d-dimensional family.",
                ["U006863", "U006864"],
            )
        ],
        variants=[("repeated center addition", "Repeatedly add at the center before stabilization/evolution.", ["U006865", "U006866"])],
        images=[("A000014", "CONTEXTUAL", "The evolution row shows typical one-dimensional stabilization histories.")],
    ),
]


# Explicit, source-local routes only.  Same-stage page headings point back to
# Chapter 7 main text; all other page/section targets remain cross-range.
ROUTE_SPECS = [
    ("U006596", "page 299", "main discussion defining the three randomness mechanisms"),
    ("U006596", "page 552", "definition of randomness"),
    ("U006596", "page 1135", "free will and determinism"),
    ("U006596", "page 911", "random-looking mathematical digit sequences"),
    ("U006596", "page 997", "fluid turbulence"),
    ("U006597", "page 1192", "applications of randomness"),
    ("U006598", "page 969", "physical randomness sources"),
    ("U006598", "page 312", "pegboard randomness"),
    ("U006598", "page 974", "card shuffling and pseudorandom generators"),
    ("U006600", "page 301", "stochastic models"),
    ("U006600", "page 302", "random walks and electronic noise"),
    ("U006600", "page 588", "random-variable models"),
    ("U006600", "page 1192", "Monte Carlo applications"),
    ("U006600", "page 1001", "ocean surfaces"),
    ("U006600", "page 328", "random walks"),
    ("U006604", "page 918", "Weierstrass function"),
    ("U006604", "page 586", "substitution-system spectra"),
    ("U006606", "page 303", "spark chambers and physical randomness"),
    ("U006606", "page 971", "dice and roulette imperfections"),
    ("U006607", "page 999", "long-time tails"),
    ("U006610", "page 1064", "quantum randomness"),
    ("U006610", "page 317", "programmatic randomness"),
    ("U006611", "page 1013", "biological pigmentation randomness"),
    ("U006613", "page 1011", "neural randomness"),
    ("U006615", "page 1011", "biological randomness"),
    ("U006617", "page 305", "spinning and tossing"),
    ("U006618", "page 914", "continued fractions"),
    ("U006618", "page 903", "substitution systems"),
    ("U006618", "page 1022", "billiards"),
    ("U006621", "page 920", "information content of initial conditions"),
    ("U006621", "page 955", "nonrepetitive dynamics"),
    ("U006621", "page 586", "frequency recognition of chaos"),
    ("U006621", "page 1177", "weather instability"),
    ("U006621", "page 313", "three-body problem"),
    ("U006621", "page 1132", "three-body computation"),
    ("U006621", "Chapter 12", "computational irreducibility and universality"),
    ("U006626", "page 314", "Sitnikov-type simple case"),
    ("U006630", "page 314", "solar-system randomness"),
    ("U006630", "page 1021", "solar-system evolution"),
    ("U006633", "page 1067", "algorithmic randomness"),
    ("U006633", "page 316", "intrinsic generation and algorithmic randomness"),
    ("U006633", "page 317", "Mathematica cellular-automaton randomness"),
    ("U006633", "page 321", "cellular-automaton random generators"),
    ("U006633", "page 603", "finite cellular-automaton randomness deviations"),
    ("U006633", "Chapter 4", "random-looking number systems"),
    ("U006634", "page 321", "perfect card shuffling"),
    ("U006639", "page 903", "runs in number generators"),
    ("U006642", "page 962", "all starting values of modular maps"),
    ("U006648", "page 1089", "LCG cryptanalysis"),
    ("U006649", "page 951", "additive cellular automata"),
    ("U006656", "page 1094", "Cantor-set geometry of generators"),
    ("U006659", "page 1087", "tap-vector representation"),
    ("U006659", "page 963", "primitive-polynomial periods"),
    ("U006659", "page 1084", "primitive polynomials"),
    ("U006660", "page 1088", "nonlinear feedback shift registers"),
    ("U006661", "page 891", "Fibonacci recurrences"),
    ("U006663", "page 598", "stream ciphers"),
    ("U006663", "page 1085", "DES"),
    ("U006668", "page 1090", "quadratic-generator predictability"),
    ("U006669", "page 260", "finite rule-30 periods"),
    ("U006669", "page 603", "cellular-automaton generators"),
    ("U006673", "page 323", "repeatable randomness"),
    ("U006673", "page 324", "probabilistic rules"),
    ("U006673", "page 591", "probabilistic cellular automata"),
    ("U006673", "page 325", "noisy cellular automata"),
    ("U006676", "page 464", "PDE approximations to cellular automata"),
    ("U006677", "page 326", "repeatably random experiments"),
    ("U006685", "page 1003", "lognormal distributions"),
    ("U006694", "page 969", "1/f noise"),
    ("U006695", "page 328", "random walks"),
    ("U006704", "page 1082", "random-walk power spectra"),
    ("U006705", "page 330", "boundaries of random-walk particle clouds"),
    ("U006715", "page 163", "diffusion equation"),
    ("U006719", "page 331", "basic aggregation model"),
    ("U006727", "page 332", "generalized aggregation models"),
    ("U006727", "page 213", "neighborhood templates"),
    ("U006727", "page 927", "aggregation rule numbering"),
    ("U006731", "page 1036", "confluence"),
    ("U006736", "page 333", "diffusion-limited aggregation"),
    ("U006736", "page 994", "DLA details"),
    ("U006740", "page 334", "cellular-automaton code 746"),
    ("U006742", "page 177", "other growth rules"),
    ("U006742", "page 181", "other growth rules"),
    ("U006751", "page 336", "domain interfaces"),
    ("U006755", "page 339", "one-dimensional transitions"),
    ("U006759", "page 340", "two-dimensional transitions"),
    ("U006786", "page 989", "nested random patterns"),
    ("U006786", "page 1149", "nested random patterns"),
    ("U006787", "page 435", "reversible evolution"),
    ("U006788", "page 339", "finite-size exceptions near the transition"),
    ("U006790", "page 273", "nested phase competition"),
    ("U006790", "page 955", "renormalization group"),
    ("U006791", "page 325", "probabilistic cellular automata"),
    ("U006791", "page 591", "directed percolation"),
    ("U006792", "page 341", "rate equations"),
    ("U006792", "page 953", "probabilistic cellular-automaton approximations"),
    ("U006794", "page 1078", "wave superpositions"),
    ("U006800", "page 940", "rules versus constraints"),
    ("U006800", "page 1145", "NP completeness"),
    ("U006800", "page 954", "one-dimensional constraint algorithm"),
    ("U006800", "page 343", "constraint distribution"),
    ("U006800", "page 346", "constraint implementation"),
    ("U006804", "page 347", "non-strict iterative procedure"),
    ("U006806", "page 901", "Gray code"),
    ("U006807", "page 347", "iterative improvement"),
    ("U006812", "page 346", "optimization cost landscape"),
    ("U006813", "page 1105", "biological optimization"),
    ("U006813", "page 1143", "NP completeness history"),
    ("U006813", "page 349", "2D cellular automata and circle packing"),
    ("U006813", "page 927", "rule-number scheme"),
    ("U006813", "page 43", "ancient hexagonal circle packing"),
    ("U006813", "page 987", "circle packing"),
    ("U006814", "page 350", "unequal-circle packing procedure"),
    ("U006820", "page 509", "Apollonian tangency network"),
    ("U006823", "page 1007", "position-dependent circle packings"),
    ("U006824", "page 929", "Voronoi cells of close packings"),
    ("U006832", "page 929", "lattice Voronoi cells"),
    ("U006843", "page 1007", "minimal surfaces"),
    ("U006843", "page 1039", "soap-film surfaces"),
    ("U006843", "page 351", "protein folding"),
    ("U006843", "page 1003", "protein structure"),
    ("U006843", "page 1184", "protein folding"),
    ("U006845", "page 587", "uniform frequency spectra"),
    ("U006845", "page 1062", "quantum-field fluctuations"),
    ("U006846", "page 138", "rational digit repetition"),
    ("U006846", "page 144", "continued-fraction repetition"),
    ("U006846", "page 1001", "continuous instability patterns"),
    ("U006846", "page 358", "nesting in numbers"),
    ("U006846", "Chapter 4", "number systems with nested behavior"),
    ("U006850", "page 939", "context-free languages"),
    ("U006854", "page 273", "rule-184 nesting"),
    ("U006854", "page 983", "statistical-mechanics sampling"),
    ("U006854", "page 955", "rescaling and renormalization"),
    ("U006854", "page 26", "additive cellular automata"),
    ("U006868", "page 977", "random walks"),
    ("U006868", "page 969", "power-law steps"),
    ("U006869", "page 1142", "algorithm structures"),
    ("U006869", "page 1045", "topological defects"),
]


HISTORICAL = {
    "U006594",
    "U006596",
}

REPRESENTATION = {
    "U006621",
    "U006630",
    "U006679",
    "U006704",
    "U006710",
    "U006711",
    "U006712",
    "U006713",
    "U006714",
    "U006744",
    "U006745",
    "U006746",
    "U006747",
    "U006748",
    "U006749",
    "U006750",
    "U006782",
    "U006783",
    "U006784",
    "U006785",
    "U006793",
    "U006794",
    "U006795",
    "U006796",
    "U006797",
    "U006798",
    "U006806",
    "U006816",
    "U006817",
    "U006818",
    "U006819",
    "U006845",
    "U006868",
    "U006869",
}

APPLICATION = {
    "U006606",
    "U006607",
    "U006608",
    "U006611",
    "U006612",
    "U006613",
    "U006614",
    "U006615",
    "U006620",
    "U006677",
    "U006678",
    "U006716",
    "U006753",
    "U006813",
    "U006825",
    "U006826",
}

DEFECTS = {
    "U006781": (
        "CONFLICTING",
        "The source defines magnetization earlier as a sum of +/-1 spins but here states m=p for +1-cell fraction p; normalized magnetization would instead be 2p-1.",
    ),
    "U006782": (
        "CONFLICTING",
        "This unit calls m[s] a density of +1 cells although the preceding Ising definition makes m[s] a spin sum, so plotted normalization is underdetermined.",
    ),
    "U006784": (
        "CONFLICTING",
        "The p/m normalization remains inconsistent with the earlier +/-1 spin-sum definition.",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def jlist(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def field_template(spec: dict[str, Any]) -> dict[str, tuple[str, str | None, str]]:
    anchor = spec["anchor"]
    kind = spec["template"]
    temporal = kind not in {"declarative", "constraint", "stochastic_declarative"}
    stochastic = kind in {"stochastic", "stochastic_partial", "physical_partial", "stochastic_declarative"}
    partial = kind in {
        "stochastic_partial",
        "physical_partial",
        "continuous_partial",
        "deterministic_partial",
    }

    def val(
        value: str | None,
        *,
        na: bool = False,
        reason: str,
    ) -> tuple[str, str | None, str]:
        if value == "N/A" or na:
            return ("NOT_APPLICABLE", None, reason)
        if value is None:
            return ("UNKNOWN_FROM_SOURCE", None, f"The in-scope source does not determine {reason}.")
        return ("SUPPORTED", value, reason)

    if not temporal:
        native = ("NOT_APPLICABLE", None, "This object is declarative and has no native time evolution.")
        history = ("NOT_APPLICABLE", None, "A displayed derivation/history is not part of the declarative object.")
        control = ("NOT_APPLICABLE", None, "No native control state exists for this declarative object.")
        seed = ("NOT_APPLICABLE", None, "A declarative object takes inputs rather than an evolutionary seed.")
        frontier = ("NOT_APPLICABLE", None, "No active update frontier exists for a declarative object.")
        schedule = ("NOT_APPLICABLE", None, "No update schedule exists for a declarative object.")
        write = ("NOT_APPLICABLE", None, "No state commit occurs; the object denotes a relation/function/set.")
        termination = ("NOT_APPLICABLE", None, "No native iterative computation is specified.")
    else:
        native_value = "continuous evolution" if kind in {"continuous", "continuous_partial", "physical_partial"} else "discrete iterations or events"
        native = ("SUPPORTED", native_value, "The source explicitly presents successive time/step/event evolution.")
        history = ("NOT_APPLICABLE", None, "Displayed history is a witness, not part of the complete native state.")
        control = val(spec["control"], reason="the native control state")
        seed = val(spec["seed"], reason="the initial state or seed")
        frontier = val(spec["frontier"], reason="the active or writable region")
        schedule = val(spec["schedule"], reason="the update schedule")
        write = val(spec["write"], reason="the replacement/commit operation")
        termination = val(spec["termination"], reason="the completion or failure condition")

    values = {
        "object_kind": (
            "SUPPORTED",
            {
                "declarative": "declarative relation/function/probability law",
                "constraint": "constraint or optimization problem",
                "stochastic_declarative": "stochastic declarative model",
                "stochastic": "stochastic iterated process",
                "stochastic_partial": "partially specified stochastic process",
                "physical_partial": "partially specified physical stochastic process",
                "continuous": "continuous dynamical system",
                "continuous_partial": "partially specified continuous dynamical system",
                "deterministic": "deterministic iterated program",
                "deterministic_partial": "partially specified deterministic iterated program",
            }[kind],
            "The source names and delimits this formal object.",
        ),
        "native_time": native,
        "carrier": val(spec["carrier"], reason="the carrier"),
        "support": val(spec["support"], reason="the support/domain"),
        "topology": val(spec["topology"], na=spec["topology"] == "N/A", reason="the topology"),
        "structural_invariants": val(spec["invariants"], na=spec["invariants"] == "N/A", reason="the structural invariants"),
        "alphabet_or_value_schema": val(spec["alphabet"], reason="the value schema"),
        "complete_state": val(spec["state"], na=spec["state"] == "N/A", reason="the complete state"),
        "visible_history": history,
        "control_state": control,
        "seed": seed,
        "input": val(spec["input"], na=spec["input"] == "N/A", reason="the external input"),
        "boundary": val(spec["boundary"], na=spec["boundary"] == "N/A", reason="the boundary convention"),
        "external_data": val(spec["external"], na=spec["external"] == "N/A", reason="external data or randomness"),
        "frontier_or_activation": frontier,
        "schedule": schedule,
        "read_dependencies_or_neighborhood": val(
            spec["read"],
            na=(not temporal and spec["read"] is None),
            reason="the read dependencies or neighborhood",
        ),
        "law_kind": (
            "SUPPORTED",
            "probability law" if stochastic else ("constraint/relation" if not temporal else "transition/evolution law"),
            "The source establishes the law's semantic kind.",
        ),
        "rule_relation_constraint_function_or_probability_law": val(spec["law"], reason="the native law"),
        "write_replacement_assembly_or_commit": write,
        "result_kind": val(spec["result"], reason="the result kind"),
        "successor_cardinality": val(
            spec["successor"] or ("a probability measure over alternatives" if stochastic else "one denotation/result"),
            reason="the successor/result cardinality",
        ),
        "determinism_branching_or_measure": val(
            spec["determinism"] or ("stochastic measure" if stochastic else "deterministic"),
            reason="determinism, branching, or measure",
        ),
        "termination_completion_failure": termination,
        "witness_semantics": val(spec["witness"], reason="the witness/acceptance semantics"),
        "parameters_and_variants": (
            "SUPPORTED" if spec["params"] or spec["variants"] else "NOT_APPLICABLE",
            (
                "The separately recorded parameters and variants are coverage-bearing."
                if spec["params"] or spec["variants"]
                else None
            ),
            (
                "The source explicitly supplies the separately recorded parameters/variants."
                if spec["params"] or spec["variants"]
                else "No additional parameter or coverage-bearing variant is stated."
            ),
        ),
        "excluded_observers_and_representations": (
            "SUPPORTED",
            "plots, spectra, histograms, rendered histories, empirical scalings, and applications are excluded unless the candidate law explicitly consumes or returns them",
            "The source context distinguishes the native object from its displays, analyses, and applications.",
        ),
        "evidence_limit": (
            "SUPPORTED",
            "Only the assigned Chapter 7 notes units and owned images are asserted; cross-referenced mechanics remain unresolved routes.",
            "This is the exact blind evidence boundary.",
        ),
    }
    if partial:
        # A partial label never weakens fields that the source actually fixes;
        # missing entries remain explicit UNKNOWN_FROM_SOURCE above.
        pass
    for field in spec["conflicting_fields"]:
        values[field] = (
            "CONFLICTING_SOURCE",
            None,
            spec["uncertainties"][0],
        )
    for field, reason in spec["unknown_fields"].items():
        assert field in values
        values[field] = (
            "UNKNOWN_FROM_SOURCE",
            None,
            reason,
        )
    for field, (status, value, reason) in list(values.items()):
        if status == "SUPPORTED":
            values[field] = (status, value, "")
    assert set(values) == set(FIELDS)
    assert anchor in spec["sources"]
    return values


def main() -> int:
    args = parse_args()
    bundle = args.bundle.resolve()
    reading_rows = load_csv(bundle / "input" / "reading-input.csv")
    asset_rows = load_csv(bundle / "input" / "asset-input.csv")
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))

    unit_order = {row["source_unit_id"]: i + 1 for i, row in enumerate(reading_rows)}
    asset_order = {row["asset_id"]: i + 1 for i, row in enumerate(asset_rows)}
    asset_by_id = {row["asset_id"]: row for row in asset_rows}
    assert len(reading_rows) == 278
    assert len(asset_rows) == 102
    assert len(CANDIDATES) == 69

    # Candidate IDs follow first canonical source occurrence, with list order
    # breaking the intentional same-unit ties.
    indexed_specs = list(enumerate(CANDIDATES))
    indexed_specs.sort(key=lambda pair: (unit_order[pair[1]["anchor"]], pair[0]))
    candidate_specs: list[dict[str, Any]] = []
    candidate_anchor_counts: dict[str, int] = defaultdict(int)
    for index, (_, spec) in enumerate(indexed_specs, 1):
        value = dict(spec)
        value["id"] = f"W{index:04d}"
        value["group_id"] = f"WG{index:06d}"
        candidate_anchor_counts[value["anchor"]] += 1
        value["anchor_ordinal"] = candidate_anchor_counts[value["anchor"]]
        value["field_defs"] = field_template(value)
        candidate_specs.append(value)

    # Allocate one evidence group per candidate and WE identifiers in exact
    # source encounter order.  Referenced images occur at their source unit.
    evidence_refs: list[tuple[tuple[int, int, int], dict[str, Any], str, str]] = []
    for c_index, spec in enumerate(candidate_specs):
        for source in spec["sources"]:
            evidence_refs.append(((unit_order[source], 0, c_index), spec, "SOURCE_UNIT", source))
        for asset_id, _strength, _claim in spec["images"]:
            # Bundle traversal visits all assigned source units first, followed
            # by assigned assets in their frozen CSV order.
            evidence_refs.append(
                (
                    (len(reading_rows) + asset_order[asset_id], 1, c_index),
                    spec,
                    "IMAGE",
                    asset_id,
                )
            )
    evidence_refs.sort(key=lambda item: item[0])
    evidence_id_by_ref: dict[tuple[str, str], str] = {}
    evidence_ordinal_by_ref: dict[tuple[str, str], int] = {}
    evidence_anchor_counts: dict[tuple[str, str], int] = defaultdict(int)
    for index, (_order, spec, kind, ref) in enumerate(evidence_refs, 1):
        key = (spec["id"], ref)
        assert key not in evidence_id_by_ref
        evidence_id_by_ref[key] = f"WE{index:06d}"
        anchor_id = (
            ref
            if kind == "SOURCE_UNIT"
            else asset_by_id[ref]["physical_path"]
        )
        evidence_anchor_counts[(kind, anchor_id)] += 1
        evidence_ordinal_by_ref[key] = evidence_anchor_counts[(kind, anchor_id)]

    candidate_by_unit: dict[str, list[str]] = defaultdict(list)
    candidate_by_asset: dict[str, list[str]] = defaultdict(list)
    anchor_by_unit: dict[str, list[str]] = defaultdict(list)
    for spec in candidate_specs:
        for source in spec["sources"]:
            candidate_by_unit[source].append(spec["id"])
        anchor_by_unit[spec["anchor"]].append(spec["id"])
        for asset_id, _strength, _claim in spec["images"]:
            candidate_by_asset[asset_id].append(spec["id"])

    # Routes are worker-local and remain unresolved.
    route_proposals: list[dict[str, str]] = []
    route_by_unit: dict[str, list[str]] = defaultdict(list)
    seen_routes: set[tuple[str, str]] = set()
    for unit, literal, topic in ROUTE_SPECS:
        key = (unit, literal)
        assert key not in seen_routes
        seen_routes.add(key)
        route_id = f"WR{len(route_proposals) + 1:04d}"
        route_by_unit[unit].append(route_id)
        page = int(literal.split()[1]) if literal.startswith("page ") else -1
        scope = "WITHIN_STAGE" if 297 <= page <= 358 else "CROSS_RANGE"
        route_proposals.append(
            {
                "route_id": route_id,
                "source_unit_id": unit,
                "source_asset_id": "",
                "discovery_epoch": "2",
                "discovery_kind": "SOURCE_UNIT",
                "discovery_id": unit,
                "discovery_ordinal": "",
                "literal_target": literal,
                "route_kind": "PAGE" if literal.startswith("page ") else "SECTION",
                "expected_topic": topic,
                "owning_stage": "11",
                "closure_scope": scope,
                "status": "PENDING",
                "target_unit_ids": "[]",
                "target_asset_ids": "[]",
                "attempts": jlist(
                    [
                        "Blind sequential review recorded the literal target; coordinator routing is required."
                    ]
                ),
                "vocabulary_terms": jlist([topic, literal]),
                "defect_boundary": "",
            }
        )

    route_anchor_counts: dict[str, int] = defaultdict(int)
    for route in route_proposals:
        route_anchor_counts[route["source_unit_id"]] += 1
        route["discovery_ordinal"] = str(
            route_anchor_counts[route["source_unit_id"]]
        )

    # Cross-reference IDs on a candidate are only routes found in its own
    # evidence units, preserving route discovery order.
    route_rank = {row["route_id"]: i for i, row in enumerate(route_proposals)}

    candidate_proposals: list[dict[str, Any]] = []
    for spec in candidate_specs:
        anchor_eid = evidence_id_by_ref[(spec["id"], spec["anchor"])]
        strong_eids = [
            evidence_id_by_ref[(spec["id"], source)]
            for source in spec["sources"]
        ]
        law_eids = [
            evidence_id_by_ref[(spec["id"], source)]
            for source in spec["law_sources"]
        ]
        parameter_sources = {
            source
            for _name, _description, sources in spec["params"] + spec["variants"]
            for source in sources
        }
        parameter_eids = [
            evidence_id_by_ref[(spec["id"], source)]
            for source in spec["sources"]
            if source in parameter_sources
        ] or [anchor_eid]

        field_sources: dict[str, list[str]] = {}
        for field, (status, _value, _reason) in spec["field_defs"].items():
            if field == "evidence_limit":
                field_sources[field] = [anchor_eid]
            elif field == "parameters_and_variants":
                field_sources[field] = parameter_eids
            elif field in {
                "law_kind",
                "rule_relation_constraint_function_or_probability_law",
                "write_replacement_assembly_or_commit",
                "read_dependencies_or_neighborhood",
            }:
                field_sources[field] = law_eids
            elif status == "CONFLICTING_SOURCE":
                conflict_sources = spec["conflict_sources"] or spec["sources"][:2]
                field_sources[field] = [
                    evidence_id_by_ref[(spec["id"], source)]
                    for source in conflict_sources
                ]
            elif status in {"NOT_APPLICABLE", "UNKNOWN_FROM_SOURCE"}:
                field_sources[field] = [anchor_eid]
            else:
                field_sources[field] = [anchor_eid]

        for asset_id, strength, _claim in spec["images"]:
            if strength == "DIRECT_PARTIAL_MECHANICS":
                image_eid = evidence_id_by_ref[(spec["id"], asset_id)]
                for field in ("parameters_and_variants", "witness_semantics"):
                    if image_eid not in field_sources[field]:
                        field_sources[field].append(image_eid)

        fields_by_evidence: dict[str, list[str]] = defaultdict(list)
        for field in FIELDS:
            for evidence_id in field_sources[field]:
                fields_by_evidence[evidence_id].append(field)

        evidence: list[dict[str, Any]] = []
        for source in spec["sources"]:
            evidence_id = evidence_id_by_ref[(spec["id"], source)]
            strength = "DIRECT_PARTIAL_MECHANICS"
            evidence.append(
                {
                    "evidence_id": evidence_id,
                    "evidence_group_id": spec["group_id"],
                    "discovery_anchor": {
                        "epoch": 2,
                        "kind": "SOURCE_UNIT",
                        "id": source,
                        "ordinal": evidence_ordinal_by_ref[
                            (spec["id"], source)
                        ],
                    },
                    "source_unit_id": source,
                    "image_path": None,
                    "strength": strength,
                    "modality": "CODE" if next(row for row in reading_rows if row["source_unit_id"] == source)["block_kind"] == "fenced_code" else "PROSE",
                    "claim": (
                        f"{source} supplies in-bundle identity, mechanics, parameters, restrictions, "
                        f"or witness semantics for {spec['name']}."
                    ),
                    "fingerprint_fields": fields_by_evidence[evidence_id],
                }
            )
        for asset_id, strength, claim in spec["images"]:
            row = asset_by_id[asset_id]
            evidence_id = evidence_id_by_ref[(spec["id"], asset_id)]
            evidence.append(
                {
                    "evidence_id": evidence_id,
                    "evidence_group_id": spec["group_id"],
                    "discovery_anchor": {
                        "epoch": 2,
                        "kind": "IMAGE",
                        "id": row["physical_path"],
                        "ordinal": evidence_ordinal_by_ref[
                            (spec["id"], asset_id)
                        ],
                    },
                    "source_unit_id": None,
                    "image_path": row["physical_path"],
                    "strength": strength,
                    "modality": "IMAGE",
                    "claim": claim,
                    "fingerprint_fields": fields_by_evidence[evidence_id],
                }
            )
        evidence.sort(key=lambda row: int(row["evidence_id"][2:]))

        fingerprint: dict[str, dict[str, Any]] = {}
        field_support: dict[str, str] = {}
        missing: list[str] = []
        for field in FIELDS:
            status, value, reason = spec["field_defs"][field]
            field_support[field] = status
            fingerprint[field] = {
                "status": status,
                "value": value,
                "evidence_ids": field_sources[field],
                "reason": reason,
            }
            if status == "UNKNOWN_FROM_SOURCE":
                missing.append(reason)

        routes = sorted(
            {
                route
                for source in spec["sources"]
                for route in route_by_unit.get(source, [])
            },
            key=route_rank.get,
        )
        statuses = ["CLEAR"]
        if spec["conflicting_fields"]:
            statuses = ["CLEAR", "CONFLICTING"]
        strengths = []
        for row in evidence:
            if row["strength"] not in strengths:
                strengths.append(row["strength"])
        candidate_proposals.append(
            {
                "id": spec["id"],
                "record_status": "ACTIVE",
                "provisional_name": spec["name"],
                "aliases": spec["aliases"],
                "discovery_stage": 11,
                "discovery_anchor": {
                    "epoch": 2,
                    "kind": "SOURCE_UNIT",
                    "id": spec["anchor"],
                    "ordinal": spec["anchor_ordinal"],
                },
                "source_unit_ids": spec["sources"],
                "source_evidence": evidence,
                "source_status": statuses,
                "image_witnesses": [
                    asset_by_id[asset]["physical_path"]
                    for asset, _strength, _claim in spec["images"]
                ],
                "evidence_strength": strengths,
                "field_support": field_support,
                "fingerprint": fingerprint,
                "parameters": [
                    {
                        "name": name,
                        "source_description": description,
                        "evidence_ids": [evidence_id_by_ref[(spec["id"], source)] for source in sources],
                    }
                    for name, description, sources in spec["params"]
                ],
                "variants": [
                    {
                        "name": name,
                        "source_description": description,
                        "evidence_ids": [evidence_id_by_ref[(spec["id"], source)] for source in sources],
                    }
                    for name, description, sources in spec["variants"]
                ],
                "missing_mechanics": missing,
                "uncertainties": spec["uncertainties"],
                "related_candidate_ids": [],
                "cross_reference_ids": routes,
                "evidence_reassignments": [],
            }
        )

    # Every source unit receives a complete independent reading judgment.
    reading_updates: list[dict[str, str]] = []
    for row in reading_rows:
        unit = row["source_unit_id"]
        candidates = candidate_by_unit.get(unit, [])
        routes = route_by_unit.get(unit, [])
        if unit in DEFECTS:
            disposition = "SOURCE_DEFECT_OR_AMBIGUITY"
            source_status, uncertainty = DEFECTS[unit]
            roles = ["SOURCE_DEFECT", "PROPERTY_OR_RESTRICTION"]
            statement = uncertainty
        elif anchor_by_unit.get(unit):
            disposition = "CANDIDATE"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["IMPLEMENTATION_DETAIL"] if row["block_kind"] == "fenced_code" else []
            names = [
                next(spec["name"] for spec in candidate_specs if spec["id"] == cid)
                for cid in anchor_by_unit[unit]
            ]
            statement = "Introduces identity-bearing mechanics for " + "; ".join(names) + "."
        elif candidates:
            disposition = "SUPPORTS_CANDIDATE"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["REPRESENTATION"] if row["block_kind"] == "image" else ["PROPERTY_OR_RESTRICTION"]
            statement = "Supplies mechanics, parameters, restrictions, or witnesses for " + ", ".join(candidates) + "."
        elif unit in HISTORICAL:
            disposition = "HISTORICAL_ONLY"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["HISTORICAL_MENTION"]
            statement = "Historical/provenance discussion supplies no independent native law."
        elif unit in REPRESENTATION or row["block_kind"] == "image":
            disposition = "REPRESENTATION_OR_OBSERVER"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["REPRESENTATION", "OBSERVER_OR_ANALYZER"]
            statement = "Records a representation, measurement, comparison, or observer rather than a new native construction."
        elif unit in APPLICATION:
            disposition = "APPLICATION_OR_EMULATION"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["APPLICATION"]
            statement = "Applies or physically interprets a construction without defining a new reproducible native law."
        elif routes:
            disposition = "CROSS_REFERENCE"
            source_status = "CLEAR"
            uncertainty = ""
            roles = ["EXTERNAL_ONLY"]
            statement = "Construction-relevant content is limited to unresolved literal cross-reference targets."
        else:
            disposition = "NO_CONSTRUCTION"
            source_status = "CLEAR"
            uncertainty = ""
            roles = []
            statement = "Complete in-context reading found no independent construction or unresolved construction route."

        result = dict(row)
        result.update(
            {
                "review_status": "REVIEWED",
                "review_epoch": "2",
                "review_disposition": disposition,
                "source_status": source_status,
                "uncertainty": uncertainty,
                "secondary_roles": jlist(roles),
                "candidate_ids": jlist(json.loads(row["candidate_ids"]) + candidates),
                "route_ids": jlist(json.loads(row["route_ids"]) + routes),
                "evidence_statement": statement,
                "review_stage": "11",
                "reviewer": "ch07-notes",
            }
        )
        reading_updates.append({field: result[field] for field in READING_FIELDS})

    # All assets were thumbnail screened.  Every referenced or unreferenced
    # construction/text-bearing asset was also opened at its native pixels.
    observer_assets = {"A000666", "A000679", "A000684", "A000685", "A000698", "A000738", "A000739"}
    native_assets = {
        "A000006",
        "A000007",
        "A000009",
        "A000010",
        "A000014",
        "A000018",
        "A000667",
        "A000673",
        "A000680",
        "A000681",
        "A000682",
        "A000683",
        "A000699",
        "A000700",
        "A000701",
        "A000702",
        "A000707",
        "A000710",
        "A000711",
        "A000721",
        "A000728",
        "A000733",
        "A000740",
    }
    direct_image_assets = {
        asset_id
        for spec in candidate_specs
        for asset_id, strength, _claim in spec["images"]
        if strength in {"DIRECT_PARTIAL_MECHANICS", "DIRECT_COMPLETE_MECHANICS"}
    }
    asset_updates: list[dict[str, str]] = []
    for row in asset_rows:
        asset = row["asset_id"]
        referenced = row["reference_status"] == "REFERENCED"
        candidates = candidate_by_asset.get(asset, [])
        if not referenced:
            role = "RELATION"
            status = "AMBIGUOUS"
            flags = ["AMBIGUOUS", "CAPTION_INCOMPLETE", "TEXT_BEARING"]
            transcription = "CHECKED"
            uncertainty = (
                "Unreferenced physical crop has no live Markdown source unit; it was inspected only as an "
                "isolated/redundant visual and contributes no mechanics."
            )
            statement = "Thumbnail and native-pixel crop inspected; no identity or mechanics were promoted."
        else:
            role = (
                "NATIVE_EVIDENCE"
                if asset in direct_image_assets
                else ("OBSERVER" if asset in observer_assets else "RELATION")
            )
            status = "CLEAR"
            flags = ["CONSTRUCTION_BEARING"]
            if asset in native_assets or asset in observer_assets:
                flags.append("TEXT_BEARING")
                transcription = "CHECKED"
            else:
                transcription = "NOT_REQUIRED"
            uncertainty = ""
            statement = (
                "Referenced image inspected at thumbnail and original resolution; "
                + (
                    "construction labels/structure were checked against the adjacent source."
                    if transcription == "CHECKED"
                    else "the image is retained as contextual relation evidence only."
                )
            )
        result = dict(row)
        result.update(
            {
                "inspection_status": "SCREENED",
                "review_epoch": "2",
                "visual_role": role,
                "source_status": status,
                "risk_flags": jlist(flags),
                "original_resolution_status": "REVIEWED",
                "transcription_status": transcription,
                "candidate_ids": jlist(json.loads(row["candidate_ids"]) + candidates),
                "route_ids": row["route_ids"],
                "evidence_statement": statement,
                "review_stage": "11",
                "reviewer": "ch07-notes",
                "uncertainty": uncertainty,
            }
        )
        asset_updates.append({field: result[field] for field in ASSET_FIELDS})

    # Worker-level uncertainties report only concrete source limitations.
    uncertainties = [
        "The Chapter 7 notes conflict on magnetization normalization: m is first a +/-1 spin sum but later is treated as +1-cell density p.",
        "Unreferenced physical image crops were screened but not used to establish candidate identity or mechanics.",
        "All literal page targets remain pending for coordinator routing; no external target was read in this blind worker.",
    ]

    output.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": candidate_proposals,
            "asset_updates": asset_updates,
            "route_proposals": route_proposals,
            "uncertainties": uncertainties,
        }
    )

    assert len(output["reading_updates"]) == 278
    assert len(output["asset_updates"]) == 102
    assert len(output["candidate_proposals"]) == 69
    assert len({e["evidence_id"] for c in candidate_proposals for e in c["source_evidence"]}) == len(evidence_refs)
    assert len({e["evidence_group_id"] for c in candidate_proposals for e in c["source_evidence"]}) == 69
    assert all(
        c["fingerprint"]["evidence_limit"]["evidence_ids"]
        == [c["source_evidence"][0]["evidence_id"]]
        or len(c["fingerprint"]["evidence_limit"]["evidence_ids"]) == 1
        for c in candidate_proposals
    )

    payload = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.check:
        print(
            json.dumps(
                {
                    "readings": len(reading_updates),
                    "assets": len(asset_updates),
                    "candidates": len(candidate_proposals),
                    "evidence": len(evidence_refs),
                    "groups": 69,
                    "routes": len(route_proposals),
                    "bytes": len(payload.encode("utf-8")),
                },
                sort_keys=True,
            )
        )
        return 0
    temporary = output_path.with_name(f".{output_path.name}.{os.getpid()}.tmp")
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, output_path)
    print(
        f"authored {output_path}: readings=278 assets=102 candidates=69 "
        f"evidence={len(evidence_refs)} groups=69 routes={len(route_proposals)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
