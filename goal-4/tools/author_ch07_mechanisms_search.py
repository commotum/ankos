#!/usr/bin/env python3
"""Author the closed Stage 11 Chapter 7 paired-scope LOCAL search.

The frozen scope is exactly Chapter 7 main text plus its Notes.  S017 adds
only vocabulary that is mechanically new relative to the terminal Stage 10
state.  S018 repeats the same query/unit and semantic projection with no
vocabulary or semantic delta.  This helper never applies a transaction.

The implementation deliberately reuses the validated Stage 10 authoring
engine, while replacing every stage-specific constant and both sequencing
guards below.  That keeps the transaction, source-projection, candidate,
route, omission-challenge, and normalized-rerun checks identical across the
two stages.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


TOOLS = Path(__file__).resolve().parent
CORE_PATH = TOOLS / "author_ch06_randomness_search.py"
SPEC = importlib.util.spec_from_file_location(
    "_ch06_search_core_for_stage11",
    CORE_PATH,
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load validated search core: {CORE_PATH}")
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)


STAGE_PATHS = [
    "CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md",
    "BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes.md",
]
STAGE = 11
EPOCH = 2
COORDINATOR_ID = "ch07-mechanisms-local-search-e2"
ASSUMPTION = core.ASSUMPTION

# This is the mechanically deduplicated, genuinely new suffix derived from
# the 163 active Stage 11 candidates' provisional names and aliases.  Four
# already-global terms are intentionally absent:
#   elementary cellular automaton rule 184
#   elementary cellular automaton rule 254
#   elementary cellular automaton rule 128
#   two-dimensional block substitution system
PROPOSED_VOCABULARY = list(
    dict.fromkeys(
        value
        for value in """
per-step random-cell recoloring process
stochastic-model randomness mechanism
random-start deterministic left-shift process
initial-condition transcription mechanism
intrinsic deterministic randomness process
intrinsic generation of randomness
microscopic-breakdown noise amplifier
friction-slowed half-colored rolling-ball process
stretch-cut-stack kneading map
kneading process
fractional-part doubling map
mirror-based kneading-map apparatus
elastic-collision pegboard process
restricted three-body scattering process
rule 30 single-black-cell evolution
rule 30 intrinsic-randomness process
rule 30 center-cell sequence observer
rule 30 center column
wrapped rule 30 random-bit generator
Random[Integer] rule 30 generator
fixed-multiplier base-2 digit process
31-bit multiplicative congruential generator
linear congruential random number generator
successive-output coordinate plot
rule 30 initial-black-cell perturbation observer
randomly perturbed continuous rule 90 process
randomly perturbed continuous rule 30 process
symmetric nearest-neighbor random walk
one-dimensional random walk
random-walk ensemble position-distribution observer
generalized one-dimensional random-walk family
Central Limit Theorem Gaussian-limit relation
Gaussian random-walk limit
two-dimensional lattice random-walk family
Eden adjacent-cell aggregation process
simple aggregation model
Eden model
one-neighbor Eden aggregation variant
one-or-four-neighbor Eden aggregation variant
outer-totalistic cellular automaton code 746
totalistic cellular automaton code 976
four-color interface-expansion cellular automaton
binary phase-selecting cellular automaton from page 339
above-right majority cellular automaton
double-well interacting-ball process
page-211 square-array constraint
case (a) square-array constraint
exhaustive constraint-satisfaction search
random constraint-pattern sampler
nonincreasing random single-cell constraint solver
exactly-two-black-neighbors square-array constraint
three-black-or-four-white-neighbors square-array constraint
cyclic right-neighbor equality constraint
strict-decrease random single-cell solver
local downhill curve minimizer
nonincrease cyclic single-cell solver
evolution-invariant-state relation
fixed-point constraint
five-neighbor cellular-automaton invariant-state family query
first uniform-invariant-state example
elementary cellular automaton rule 146
second uniform-invariant-state example
densest equal-circle packing constraint
densest equal-sphere packing constraint
greedy center-nearest circle placement process
Gray-path elementary-cellular-automaton rule sequence
homogeneous point-growth mobile automaton
rule 254 single-black-cell point-growth preset
homogeneous point-growth cellular automaton
independent rule 0 cell convergence
binary independent-element convergence
independent continuous-element convergence map
continuous independent-element convergence
elementary cellular automaton rule 160
elementary cellular automaton rule 254 class-1 preset
rule 30 spatial coarse-graining observer
three-cell gray-level averaging cellular automaton
two-neighbor uniformity constraint
deterministic finite-state eventual-periodicity relation
closed-curve recurrence criterion
finite-state recurrence criterion
elementary cellular automaton rule 50 simple-seed preset
elementary cellular automaton rule 94 simple-seed preset
elementary cellular automaton rule 54 simple-seed preset
random-start domain cellular-automaton family for rules 50, 54, and 62
random-start rule 184 domain-combination preset
random-start rule 110 domain process
binary pair substitution system
two-state recursive Y-branching preset
recursive three-child branching preset
recursive two-child orthogonal branching preset
recursive four-child triangular branching preset
additive cellular automaton rule 90
additive cellular automaton rule 150
regular two-branch creation-and-annihilation process
regular three-branch creation-and-annihilation process
equal-density random-start rule 184 nesting preset
rule 110 first-cell-per-14-by-7-block observer
three-color totalistic cellular automaton code 1893
k=3 totalistic code 1893
elementary cellular automaton rule 18 domain process
two-by-two cellular-automaton block-compression observer
mechanical toss-or-mix randomness source
stochastic model
Monte Carlo simulation-and-average method
shot-noise process
thermal (Johnson) noise process
flicker (1/f) noise process
discrete power-spectrum analyzer
electronic physical-randomness generator
quantum-event randomness generator
computer entropy-pool seeding system
/dev/random-style entropy pool
biological stochastic DNA rearrangement process
flagellar tumble direction-change process
frictionally decelerated spinning/tossing model
rectangular billiard trajectory system
three-body gravitational trajectory system
Sitnikov-type idealized planet equation
successive-new-moon interval observer
perfect riffle-shuffle permutation
linear congruential generator
linear feedback shift register
generalized Fibonacci random-number generator
stream-cipher random-number generator
middle-square generator
quadratic congruential generator
cellular-automaton random-number generator
equal-bit to biased-bit converter
noisy continuous cellular-automaton model
discrete-cellular-automaton to continuous-PDE approximation relation
Gaussian central-limit aggregation law
lognormal product law
Fisher-Tippett extreme-value law
extreme-value distribution
Wigner random-matrix spectral laws
lattice random walk
random-walk displacement probability law
random-walk extreme-position distribution analyzer
source-absorber-reflector random-walk population process
random-walk population to diffusion-equation relation
self-avoiding walk
type B Eden aggregation process
type A Eden aggregation process
generic two-dimensional template aggregation family
eight-neighbor constraint-242 aggregation process
one-dimensional template aggregation family
diffusion-limited aggregation
DLA
aggregation cellular automaton code 746
other aggregation cellular-automaton code family
tensor and multipole isotropy analyzer
continuous-PDE isotropy criterion
flat-domain-interface rule-150 process
two-dimensional domain cellular-automaton family
binary next-nearest-neighbor transition cellular-automaton family
Gacs-Kurdyumov-Levin seven-neighbor cellular automaton
four-color transition cellular automaton code 294869764523995749814890097794812493824
probabilistic Toom two-dimensional transition preset
microcanonical fixed-energy Ising measure
canonical Boltzmann-weight Ising measure
Ising heat-bath Monte Carlo sampler
deterministic checkerboard Ising cellular automaton
site-percolation model
well-mixed chemical rate-equation relation
binary ring adjacency-violation cost function
greedy single-bit constraint-improvement process
gradient-descent iteration
Newton root-finding iteration
simulated-annealing optimization process
population-based genetic optimization process
genetic algorithm
incremental unequal-circle packing procedure
Apollonian circle-packing construction
sphere-packing constraint problem
discrete toroidal circle-packing problem
Voronoi-diagram transform
Dirichlet tessellation
Wigner-Seitz cells for repetitive lattices
discrete Voronoi cellular automaton
higher-order Voronoi region construction
higher-order Voronoi diagram
Brillouin-zone construction
minimum-boundary deformable-object packing problem
PDE linear-stability and dispersion analyzer
balanced-parentheses language membership and denotation
balanced-parentheses count analyzer
two-dimensional sandpile stabilization cellular automaton
driven sandpile add-and-stabilize cycle
d-dimensional conserved sandpile cellular-automaton family
one-dimensional sandpile stabilization cellular automaton
""".splitlines()
        if value
    )
)

# F01-F10 are construction-facing and must collectively reach every Stage 11
# candidate through candidate-linked direct evidence.  F11-F15 challenge
# mechanics, representation/control boundaries, source defects, and routes.
QUERY_SPECS = [
    (
        "cellular automata, rules, codes, domains, transitions, and sandpiles",
        (
            r"\b(?:cellular autom(?:aton|ata)|rules?\s*(?:0|18|30|50|54|62|90|"
            r"94|110|128|146|150|160|184|254)\b|rule[- ]?(?:number|code)|"
            r"codes?\s*(?:746|976|1893|294869764523995749814890097794812493824)"
            r"\b|totalistic|outer[- ]totalistic|next[- ]nearest|"
            r"transition rules?|domain walls?|domains?|phase[- ]selecting|"
            r"Toom|Gacs|Kurdyumov|Levin|sandpiles?|toppl(?:e|es|ed|ing))\b"
        ),
        "REGEX",
    ),
    (
        "randomness, stochasticity, noise, probability, and entropy sources",
        (
            r"\b(?:random(?:ness|ly)?|pseudorandom|stochastic|probabilistic|"
            r"probabilit(?:y|ies)|noise|shot noise|Johnson noise|flicker|"
            r"entropy(?: pool)?|quantum|thermal|Monte Carlo|ensemble|"
            r"distribution|measure|Boltzmann|microcanonical|canonical|"
            r"percolation|Ising|biased|unbiased|independent|"
            r"microscopic fluctuations?|breakdown|"
            r"amplif(?:y|ies|ied|ication)|sparks?)\b"
        ),
        "REGEX",
    ),
    (
        "mechanical motion, trajectories, maps, collisions, and recurrence",
        (
            r"\b(?:mechanical|motion|trajector(?:y|ies)|billiards?|balls?|"
            r"rolling|spinning|toss(?:ed|ing)?|friction|collisions?|elastic|"
            r"pegboard|three[- ]body|planet|moon|gravitational|scatter(?:ing)?|"
            r"knead(?:ing)?|stretch|cut|stack|doubling map|fractional part|"
            r"left[- ]shift|shift(?:s|ed|ing)?[^.\n]{0,60}\b(?:left|right)\b|"
            r"transcription|maps?|"
            r"iterat(?:e|es|ed|ing|ion)|finite[- ]state|"
            r"periodic(?:ity)?|recurr(?:ence|ent)|closed curves?)\b"
        ),
        "REGEX",
    ),
    (
        "random walks, aggregation, growth, Eden, DLA, and phase models",
        (
            r"\b(?:random walks?|self[- ]avoiding walks?|lattice walks?|"
            r"diffusion|absorbers?|reflectors?|sources?|population|"
            r"aggregation|aggregate|Eden|DLA|diffusion[- ]limited|"
            r"templates?|point growth|interfaces?|growth|nucleation|"
            r"phases?|phase transitions?|checkerboards?)\b"
        ),
        "REGEX",
    ),
    (
        "constraints, search, optimization, packing, and Voronoi constructions",
        (
            r"\b(?:constraints?|satisf(?:y|ies|ied|action)|solutions?|"
            r"search(?:es|ed|ing)?|cost functions?|minimi[sz](?:e|es|ed|ing)|"
            r"maximi[sz](?:e|es|ed|ing)|optimization|downhill|gradient|"
            r"Newton|anneal(?:ing)?|genetic algorithms?|packing|circles?|"
            r"spheres?|pack(?:s|ed|ing)?|granular|settling|shaking|"
            r"Apollonian|Voronoi|Dirichlet|Wigner[- ]Seitz|"
            r"Brillouin|tessellations?|adjacency|nearest centers?|"
            r"fixed points?|invariants?)\b"
        ),
        "REGEX",
    ),
    (
        "equations, PDE relations, rate laws, stability, and distributions",
        (
            r"\b(?:equations?|differential equations?|partial differential|"
            r"PDE|continuum|continuous|finite differences?|rate equations?|"
            r"dispersion|linear stability|wavelengths?|Fourier|"
            r"power spectra?|spectr(?:um|a|al)|isotrop(?:y|ic)|tensors?|"
            r"multipoles?|central limit|Gaussian|lognormal|Fisher|Tippett|"
            r"extreme[- ]value|random matrices?|Wigner|chemical rates?)\b|"
            r"`[^`\n]*(?:=|->|→|Nest|NestList|Fourier|Solve|Table)[^`\n]*`|"
            r"(?:^|\n)\s*(?:\$\$|\\\[)|"
            r"(?:^|\n)\s*\$[^$\n]+\$\s*(?:\n|$)"
        ),
        "REGEX",
    ),
    (
        "substitutions, recursive branching, nesting, and creation processes",
        (
            r"\b(?:substitutions?|replac(?:e|es|ed|ing|ement)|recursive|"
            r"recursion|branch(?:es|ed|ing)?|Y[- ]branching|children|"
            r"creation|annihilation|nested|nesting|blocks?|pairs?|"
            r"parentheses|brackets?|balanced|Catalan|languages?)\b"
        ),
        "REGEX",
    ),
    (
        "random-number algorithms, shuffles, sampling, and stochastic search",
        (
            r"\b(?:random[- ]number generators?|congruential|linear feedback|"
            r"shift registers?|Fibonacci|stream ciphers?|middle[- ]square|"
            r"riffle|shuffle|permutations?|sampling|samplers?|heat[- ]bath|"
            r"Monte Carlo|simulated annealing|genetic|entropy pool|"
            r"Random\[Integer\]|multipliers?|base[- ]2 digits?)\b"
        ),
        "REGEX",
    ),
    (
        "observers, analyzers, transforms, plots, and coarse-graining",
        (
            r"\b(?:observers?|analy[sz](?:e|es|ed|ing|er|ers|is)|"
            r"plots?|coordinates?|displays?|pictures?|transform(?:s|ed|ation)?|"
            r"coarse[- ]grain(?:ing)?|averag(?:e|es|ed|ing)|compression|"
            r"sequences?|center columns?|perturbations?|position distribution|"
            r"power spectra?|isotropy|count(?:s|ed|ing)?|denotation|"
            r"membership|region construction|diagram)\b"
        ),
        "REGEX",
    ),
    (
        "broad construction and mechanism anchors",
        (
            r"\b(?:rules?|systems?|programs?|processes?|algorithms?|"
            r"procedures?|constructions?|presets?|families|models?|"
            r"relations?|constraints?|functions?|maps?|generators?|"
            r"analyzers?|observers?|transformations?|autom(?:aton|ata)|languages?|"
            r"sequences?|configurations?|patterns?|structures?|equations?|"
            r"initial conditions?|evolution|steps?|states?|inputs?|outputs?|"
            r"examples?|cases?)\b|(?:^|\n)\s*(?:#{1,6}\s+[^\n]+|"
            r"!\[[^\]]*\]\([^)]+\)|```)"
        ),
        "REGEX",
    ),
    (
        "native state, activation, schedule, neighborhood, and update mechanics",
        (
            r"\b(?:states?|configurations?|cells?|sites?|elements?|values?|"
            r"colors?|neighbou?rs?|neighbou?rhoods?|frontiers?|active|"
            r"schedules?|parallel|synchronous|asynchronous|randomly selected|"
            r"updates?|successors?|evol(?:ve|ves|ved|ving|ution)|"
            r"iterations?|transitions?|replac(?:e|es|ed|ing|ement)|"
            r"boundar(?:y|ies)|lattices?|grids?|rings?|toroidal)\b"
        ),
        "REGEX",
    ),
    (
        "representation, observer, application, and implementation boundary",
        (
            r"\b(?:represent(?:s|ed|ing|ation)?|visualiz(?:e|es|ed|ation)|"
            r"implement(?:s|ed|ing|ation)?|simulat(?:e|es|ed|ing|ion)|"
            r"render(?:s|ed|ing)?|observers?|projections?|plots?|diagrams?|"
            r"pictures?|trajector(?:y|ies)|histories|spacetime|statistics?|"
            r"measure(?:s|d|ment)?|applications?|models? of|Mathematica)\b"
        ),
        "REGEX",
    ),
    (
        "Stage 11 discovered mechanics and native aliases",
        (
            r"\b(?:left[- ]shift|intrinsic randomness|half[- ]colored|"
            r"kneading|pegboard|center[- ]cell sequence|congruential|"
            r"Eden|constraint[- ]satisfaction|invariant[- ]state|Gray[- ]path|"
            r"point[- ]growth|branching preset|creation[- ]and[- ]annihilation|"
            r"shot[- ]noise|Johnson noise|flicker noise|entropy[- ]pool|"
            r"riffle[- ]shuffle|feedback shift register|extreme[- ]value|"
            r"source[- ]absorber[- ]reflector|template aggregation|"
            r"multipole isotropy|Toom|Boltzmann[- ]weight|heat[- ]bath|"
            r"simulated[- ]annealing|Apollonian|higher[- ]order Voronoi|"
            r"dispersion analyzer|balanced[- ]parentheses|sandpile)\b"
        ),
        "REGEX",
    ),
    (
        "source-defect, uncertainty, and qualification boundary",
        (
            r"\b(?:unclear|ambiguous|defect(?:ive)?|missing|unknown|"
            r"not specified|not stated|appears?|presumably|approximately|"
            r"idealized|simplif(?:y|ies|ied)|only|rather than|except|"
            r"however|may|might|could|seems?)\b"
        ),
        "REGEX",
    ),
    (
        "typed cross-reference locator and route-anchor obligations",
        (
            r"\b(?:pages?|page|chapter)\s+"
            r"(?:\d+|[IVX]+)(?:[–-]\d+)?\b|"
            r"\b(?:the\s+)?(?:(?:top|bottom)\s+of\s+(?:the\s+)?)?"
            r"(?:facing|previous|next)(?:\s+(?:one|two|three))?"
            r"\s+pages?\b|"
            r"\b(?:previous section|next chapter|next few chapters|"
            r"later in (?:this|the) book|linear feedback shift registers?|"
            r"ultimate forms of behavior|undecidable|"
            r"non[- ]deterministic Turing machines?|tiling problems?|"
            r"halting problems?)\b"
        ),
        "REGEX",
    ),
]


# Source/query guards are filled after --calibrate-source and then immutable.
EXPECTED_QUERY_SPEC_DIGEST = (
    "9a7790adeeb39626e5234f06596b731571e0f6729ab1b3e58eee4e03f5a4502c"
)
EXPECTED_STAGE_VOCABULARY_COUNT = len(PROPOSED_VOCABULARY)
EXPECTED_STAGE_VOCABULARY_DIGEST = (
    "992dd09abae87cf800a3401591d28d3a2068a9133a39bcac33103bbc0ad74005"
)
EXPECTED_STAGE_UNIT_COUNT = 713
EXPECTED_STAGE_ASSET_COUNT = 194
EXPECTED_STAGE_UNIT_IDS_DIGEST = (
    "60046d02679da034b9579d21b8aee9bedc9a2de89251af3cfa9a6683eb14ad05"
)
EXPECTED_STAGE_UNIT_PROJECTION_DIGEST = (
    "7b04501d101772fa173b4472e6cade05244322c86d2cda3580680d62b37ab849"
)
EXPECTED_SOURCE_SHA256 = {
    STAGE_PATHS[0]: (
        "e052f275ea7519f2e8c270f1dd68eac01d123aa3b73355eff5803f02708e542d"
    ),
    STAGE_PATHS[1]: (
        "fd8696100529789964578841267bbd841411691d05248840ede6e0b4b7bd69f3"
    ),
}
EXPECTED_RESULT_PAIR_COUNT = 2478
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 704
EXPECTED_HIT_COUNTS = [
    104,
    282,
    78,
    84,
    89,
    84,
    59,
    36,
    210,
    645,
    200,
    160,
    83,
    209,
    155,
]
EXPECTED_PATH_PAIR_COUNTS = {
    STAGE_PATHS[0]: 1419,
    STAGE_PATHS[1]: 1059,
}
EXPECTED_PATH_UNIQUE_UNIT_COUNTS = {
    STAGE_PATHS[0]: 432,
    STAGE_PATHS[1]: 272,
}
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "c604632660a66ca6c815be6ecb03e6a6d0c2505b95082ee010a8154429fcb69d"
)
EXPECTED_RESULT_UNIT_IDS_DIGEST = (
    "effa31eb78c02cfc76773c2b58fe7a26de2778aefb9facb12132c9a0089a8e8b"
)

EXPECTED_CLOSED_ROUND_COUNT = 16
EXPECTED_CLOSED_ROUNDS_DIGEST = (
    "f9d4edba680a2f9c810db432bb6a79f892fbb6692f5f74f9acd93d41f0eaedbf"
)
EXPECTED_QUERY_START = {"S015": 209, "S017": 209, "S018": 224}
EXPECTED_HIT_START = {"S015": 18631, "S017": 18631, "S018": 21109}
EXPECTED_GLOBAL_VOCABULARY_COUNT = {
    "S015": 716,
    "S017": 716,
    "S018": 907,
}
EXPECTED_GLOBAL_VOCABULARY_DIGEST = {
    "S015": "c98559ab14e510f32f4f7e13852bed3d8ec016b1708dce7c94764d8120e693d6",
    "S017": "c98559ab14e510f32f4f7e13852bed3d8ec016b1708dce7c94764d8120e693d6",
    "S018": "786ca2acc4b7aba9545363c7fbc6fec49b6c95eea267153de081f2af7cf337cd",
}
EXPECTED_GLOBAL_ASSUMPTIONS_COUNT = 2
EXPECTED_GLOBAL_ASSUMPTIONS_DIGEST = (
    "671219eeacdded499c971a237e87b358ec687bfb6f085425d101d5d007a20afd"
)
EXPECTED_POST_MERGE_SEMANTICS: dict[str, Any] = {
    "stage_reading_count": 713,
    "stage_reading_digest": (
        "aefbfea99a0e698e1e30112cd703a1c732b368f474d818f03ce53218c055d4dd"
    ),
    "stage_asset_count": 194,
    "stage_asset_digest": (
        "b7b4e5ff2489d64701bb07b4d9b82688fca33d86bcbe42a80f56a633c584d864"
    ),
    "stage_candidate_count": 163,
    "stage_candidate_ids_digest": (
        "f7fdb657ab7bb6e59118c8a7367ec8d5da7a09caa6ad80ab169b66503e6a0890"
    ),
    "triage_digest": (
        "3309da9bb6b23203230d95d954ebd35cd5e1fb3af1363841296df1a5a5a6ca50"
    ),
    "candidate_coverage_digest": (
        "3496212836e9a84a6b01f393f7b8b65937f0f868d2cb594251e5e909811532b4"
    ),
    "omission_challenge_count": 489,
    "omission_challenge_digest": (
        "9ac5e8254b78d9303fc096775517b67fbe35375bebc45a0149dc7d4072a3c044"
    ),
    "route_coverage_count": 163,
    "route_coverage_digest": (
        "3f919f6a25195bb972da04af1675b7faff64bc17cfbb0bd026d51b5acff462ab"
    ),
    "disposition_counts": {
        "CONTROL_OR_RELATIONSHIP": 45,
        "CROSS_REFERENCE": 97,
        "EXCLUSION": 644,
        "GOVERNED_CANDIDATE_OR_SUPPORT": 1692,
    },
    "normalized_hit_projection_digest": (
        "0aa120c8aa645bd7846f789a7126066a9fdff14465b84ee153fbe2cefdd67946"
    ),
}
EXPECTED_ROUND_GUARDS: dict[str, dict[str, Any]] = {
    # S015 is a compatibility alias used only inside the validated Stage 10
    # analysis engine while it takes the first-round vocabulary branch.
    "S015": {
        "prior_event_sha256": (
            "8591957742594eaa43c969cab60b8b61a730854977910bdafc0c7088ac16c885"
        ),
        "base_artifact_sha256": {
            "asset-ledger.csv": (
                "717e20c259292fab63f40e3a34de76cff7770c4c288d741a8310c491e58db881"
            ),
            "candidate-ledger.jsonl": (
                "8676464e94072acec5bcfa03b98d056018dfbc77bd7915d4a647bbfc46ec1442"
            ),
            "cross-reference-ledger.csv": (
                "8f3cd4b4bbd793410f511be5b899224a5a09b06f8b1ba053929f0b0774434748"
            ),
            "reading-ledger.csv": (
                "9bb64de8b08873355191bd404febc5895f9c6e772706c291865cb6e83607232d"
            ),
            "review-history.jsonl": (
                "9452ba3327958b7e2550afc4642ee679b108f50e5ad7a8a93cdf88d18ea38680"
            ),
            "search-rounds.json": (
                "f614cce2bff0e040fca38cd1a82036432d951c2082febfcb9cf0eb86c03ae94d"
            ),
        },
        "result_digest": (
            "468f300c470f61dedbe0493a60d54e02f3eb74894ed08036570390b7749827db"
        ),
    },
    "S017": {
        "prior_event_sha256": (
            "8591957742594eaa43c969cab60b8b61a730854977910bdafc0c7088ac16c885"
        ),
        "base_artifact_sha256": {
            "asset-ledger.csv": (
                "717e20c259292fab63f40e3a34de76cff7770c4c288d741a8310c491e58db881"
            ),
            "candidate-ledger.jsonl": (
                "8676464e94072acec5bcfa03b98d056018dfbc77bd7915d4a647bbfc46ec1442"
            ),
            "cross-reference-ledger.csv": (
                "8f3cd4b4bbd793410f511be5b899224a5a09b06f8b1ba053929f0b0774434748"
            ),
            "reading-ledger.csv": (
                "9bb64de8b08873355191bd404febc5895f9c6e772706c291865cb6e83607232d"
            ),
            "review-history.jsonl": (
                "9452ba3327958b7e2550afc4642ee679b108f50e5ad7a8a93cdf88d18ea38680"
            ),
            "search-rounds.json": (
                "f614cce2bff0e040fca38cd1a82036432d951c2082febfcb9cf0eb86c03ae94d"
            ),
        },
        "result_digest": (
            "468f300c470f61dedbe0493a60d54e02f3eb74894ed08036570390b7749827db"
        ),
    },
    "S018": {
        "prior_event_sha256": (
            "7be9a15996d4a682ecd4778c22ec79a5d93ead82b1edff8ec38e14aade61ae83"
        ),
        "base_artifact_sha256": {
            "asset-ledger.csv": (
                "717e20c259292fab63f40e3a34de76cff7770c4c288d741a8310c491e58db881"
            ),
            "candidate-ledger.jsonl": (
                "8676464e94072acec5bcfa03b98d056018dfbc77bd7915d4a647bbfc46ec1442"
            ),
            "cross-reference-ledger.csv": (
                "8f3cd4b4bbd793410f511be5b899224a5a09b06f8b1ba053929f0b0774434748"
            ),
            "reading-ledger.csv": (
                "9bb64de8b08873355191bd404febc5895f9c6e772706c291865cb6e83607232d"
            ),
            "review-history.jsonl": (
                "4ca97401c6f0e9ca126e7ddbb412703ed78a710a5f77a90c1b5f4292acbbc2bd"
            ),
            "search-rounds.json": (
                "fc56b8033fee4a7a482eec7448d9b1ada6e63e9a2cf1be446ac0be394d6a01df"
            ),
        },
        "result_digest": (
            "a546b8f88ecde0d3d44ae5550b53bea022c13df4fec2e67a7caf01bf82ede434"
        ),
    },
}


def _require_closed_round_prefix(
    rounds: list[dict[str, Any]],
    *,
    enforce_frozen: bool,
) -> str:
    if len(rounds) not in {16, 17}:
        raise core.AuthoringError(
            "expected the sixteen closed S001-S016 rounds and zero/one "
            f"Stage 11 round, got {len(rounds)}"
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
        ("S011", "LOCAL", 8, 2),
        ("S012", "LOCAL", 8, 2),
        ("S013", "LOCAL", 9, 2),
        ("S014", "LOCAL", 9, 2),
        ("S015", "LOCAL", 10, 2),
        ("S016", "LOCAL", 10, 2),
    ]
    observed = [
        (
            record.get("round_id"),
            record.get("kind"),
            record.get("owning_stage"),
            record.get("epoch"),
        )
        for record in rounds[:16]
    ]
    if observed != expected_prefix:
        raise core.AuthoringError("the closed S001-S016 LOCAL prefix drifted")
    if core.digest(rounds[:16]) != EXPECTED_CLOSED_ROUNDS_DIGEST:
        raise core.AuthoringError("the exact closed S001-S016 prefix drifted")
    round_id = f"S{len(rounds) + 1:03d}"
    if round_id == "S018":
        prior = rounds[16]
        guard = EXPECTED_ROUND_GUARDS["S017"]
        if (
            prior.get("round_id") != "S017"
            or prior.get("kind") != "LOCAL"
            or prior.get("owning_stage") != STAGE
            or prior.get("epoch") != EPOCH
            or prior.get("queries")
            != core._query_objects(EXPECTED_QUERY_START["S017"])
            or prior.get("tool_assumptions") != [ASSUMPTION]
            or prior.get("new_vocabulary") != PROPOSED_VOCABULARY
            or any(
                prior.get(field) != []
                for field in (
                    "new_candidates",
                    "new_evidence_groups",
                    "new_routes",
                )
            )
            or (
                enforce_frozen
                and prior.get("result_digest") != guard["result_digest"]
            )
            or (
                enforce_frozen
                and prior.get("rerun_digest") != guard["result_digest"]
            )
        ):
            raise core.AuthoringError("the applied S017 seed round drifted")
    return round_id


def _require_history(
    history: list[dict[str, Any]],
    round_id: str,
    *,
    enforce_frozen: bool,
) -> None:
    effective_round_id = "S017" if round_id == "S015" else round_id
    expected_length = 32 if effective_round_id == "S017" else 33
    if len(history) != expected_length:
        raise core.AuthoringError(
            f"{round_id} expected {expected_length} review events, "
            f"got {len(history)}"
        )
    for number, event in enumerate(history, start=1):
        if event.get("review_id") != f"V{number:06d}":
            raise core.AuthoringError("review-history ID sequence drifted")
    prior = history[-1]
    expected_review_id = (
        "V000032" if effective_round_id == "S017" else "V000033"
    )
    expected_mode = (
        "ROUTE_RESOLUTION"
        if effective_round_id == "S017"
        else "SEARCH_APPEND"
    )
    expected_reviewer = (
        None if effective_round_id == "S017" else COORDINATOR_ID
    )
    if (
        prior.get("review_id") != expected_review_id
        or prior.get("stage") != STAGE
        or prior.get("epoch") != EPOCH
        or prior.get("mode") != expected_mode
        or (
            expected_reviewer is not None
            and prior.get("reviewer") != expected_reviewer
        )
    ):
        raise core.AuthoringError(
            f"{effective_round_id} prior terminal event drifted"
        )
    if enforce_frozen and prior.get("event_sha256") != (
        EXPECTED_ROUND_GUARDS[round_id]["prior_event_sha256"]
    ):
        raise core.AuthoringError(
            f"{effective_round_id} prior event digest drifted"
        )


def _source_rationale(
    row: dict[str, str],
    *,
    family_ordinal: int,
    outcome: str,
) -> str:
    statement = " ".join(row["evidence_statement"].split())
    if not statement:
        raise core.AuthoringError(
            f"{row['source_unit_id']} lacks an evidence statement"
        )
    lead = (
        f"Stage 11 paired-scope omission challenge F{family_ordinal:02d} "
        f"({QUERY_SPECS[family_ordinal - 1][0]}) at "
        f"{row['source_unit_id']} [{row['block_kind']}] retains {outcome}: "
    )
    if row["source_status"] in {"AMBIGUOUS", "DEFECTIVE", "CONFLICTING"}:
        uncertainty = " ".join(row["uncertainty"].split())
        return (
            f"{lead}source_status={row['source_status']}; "
            f"uncertainty={uncertainty}. {statement}"
        )
    return f"{lead}{statement}"


_CORE_ANALYZE_POST_MERGE = core._analyze_post_merge
_LAST_COMPATIBILITY_RESULT_DIGEST: str | None = None


def _analyze_post_merge(
    goal_dir: Path,
    *,
    enforce_frozen: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Adapt the validated first/second-round engine to S017/S018 IDs."""

    global _LAST_COMPATIBILITY_RESULT_DIGEST
    search = json.loads(
        (goal_dir / core.merge_worker_output.SEARCH_NAME).read_text(
            encoding="utf-8"
        )
    )
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise core.AuthoringError("global search rounds are malformed")

    if len(rounds) == 16:
        original_prefix_guard = core._require_closed_round_prefix

        def compatibility_prefix(
            records: list[dict[str, Any]],
            *,
            enforce_frozen: bool,
        ) -> str:
            _require_closed_round_prefix(
                records,
                enforce_frozen=enforce_frozen,
            )
            return "S015"

        core._require_closed_round_prefix = compatibility_prefix
        try:
            state, semantic, round_guard = _CORE_ANALYZE_POST_MERGE(
                goal_dir,
                enforce_frozen=enforce_frozen,
            )
        finally:
            core._require_closed_round_prefix = original_prefix_guard

        compatibility_digest = state["round_record"]["result_digest"]
        _LAST_COMPATIBILITY_RESULT_DIGEST = compatibility_digest
        state["round_id"] = "S017"
        state["round_record"]["round_id"] = "S017"
        result_digest = core.validate_audit.search_result_digest(
            state["round_record"]
        )
        state["round_record"]["result_digest"] = result_digest
        state["round_record"]["rerun_digest"] = result_digest
        round_guard["result_digest"] = result_digest
        if enforce_frozen and result_digest != (
            EXPECTED_ROUND_GUARDS["S017"]["result_digest"]
        ):
            raise core.AuthoringError("S017 adapted result digest drifted")
        return state, semantic, round_guard

    state, semantic, round_guard = _CORE_ANALYZE_POST_MERGE(
        goal_dir,
        enforce_frozen=enforce_frozen,
    )
    if state["round_id"] != "S018":
        raise core.AuthoringError(
            f"unsupported Stage 11 search state {state['round_id']}"
        )
    if core._normalized_hit_projection(state["round_record"]) != (
        core._normalized_hit_projection(rounds[16])
    ):
        raise core.AuthoringError(
            "S018 differs from the S017 normalized zero-delta projection"
        )
    return state, semantic, round_guard


def _install_stage_constants() -> None:
    replacements = {
        "STAGE_PATHS": STAGE_PATHS,
        "STAGE": STAGE,
        "EPOCH": EPOCH,
        "COORDINATOR_ID": COORDINATOR_ID,
        "ASSUMPTION": ASSUMPTION,
        "PROPOSED_VOCABULARY": PROPOSED_VOCABULARY,
        "QUERY_SPECS": QUERY_SPECS,
        "EXPECTED_QUERY_SPEC_DIGEST": EXPECTED_QUERY_SPEC_DIGEST,
        "EXPECTED_STAGE_VOCABULARY_COUNT": EXPECTED_STAGE_VOCABULARY_COUNT,
        "EXPECTED_STAGE_VOCABULARY_DIGEST": EXPECTED_STAGE_VOCABULARY_DIGEST,
        "EXPECTED_STAGE_UNIT_COUNT": EXPECTED_STAGE_UNIT_COUNT,
        "EXPECTED_STAGE_ASSET_COUNT": EXPECTED_STAGE_ASSET_COUNT,
        "EXPECTED_STAGE_UNIT_IDS_DIGEST": EXPECTED_STAGE_UNIT_IDS_DIGEST,
        "EXPECTED_STAGE_UNIT_PROJECTION_DIGEST": (
            EXPECTED_STAGE_UNIT_PROJECTION_DIGEST
        ),
        "EXPECTED_SOURCE_SHA256": EXPECTED_SOURCE_SHA256,
        "EXPECTED_RESULT_PAIR_COUNT": EXPECTED_RESULT_PAIR_COUNT,
        "EXPECTED_UNIQUE_RESULT_UNIT_COUNT": EXPECTED_UNIQUE_RESULT_UNIT_COUNT,
        "EXPECTED_HIT_COUNTS": EXPECTED_HIT_COUNTS,
        "EXPECTED_PATH_PAIR_COUNTS": EXPECTED_PATH_PAIR_COUNTS,
        "EXPECTED_PATH_UNIQUE_UNIT_COUNTS": (
            EXPECTED_PATH_UNIQUE_UNIT_COUNTS
        ),
        "EXPECTED_NORMALIZED_RESULT_DIGEST": (
            EXPECTED_NORMALIZED_RESULT_DIGEST
        ),
        "EXPECTED_RESULT_UNIT_IDS_DIGEST": EXPECTED_RESULT_UNIT_IDS_DIGEST,
        "EXPECTED_CLOSED_ROUND_COUNT": EXPECTED_CLOSED_ROUND_COUNT,
        "EXPECTED_CLOSED_ROUNDS_DIGEST": EXPECTED_CLOSED_ROUNDS_DIGEST,
        "EXPECTED_QUERY_START": EXPECTED_QUERY_START,
        "EXPECTED_HIT_START": EXPECTED_HIT_START,
        "EXPECTED_GLOBAL_VOCABULARY_COUNT": (
            EXPECTED_GLOBAL_VOCABULARY_COUNT
        ),
        "EXPECTED_GLOBAL_VOCABULARY_DIGEST": (
            EXPECTED_GLOBAL_VOCABULARY_DIGEST
        ),
        "EXPECTED_GLOBAL_ASSUMPTIONS_COUNT": (
            EXPECTED_GLOBAL_ASSUMPTIONS_COUNT
        ),
        "EXPECTED_GLOBAL_ASSUMPTIONS_DIGEST": (
            EXPECTED_GLOBAL_ASSUMPTIONS_DIGEST
        ),
        "EXPECTED_POST_MERGE_SEMANTICS": EXPECTED_POST_MERGE_SEMANTICS,
        "EXPECTED_ROUND_GUARDS": EXPECTED_ROUND_GUARDS,
        "_require_closed_round_prefix": _require_closed_round_prefix,
        "_require_history": _require_history,
        "_source_rationale": _source_rationale,
        "_analyze_post_merge": _analyze_post_merge,
    }
    for name, value in replacements.items():
        setattr(core, name, value)


def _unresolved_source_guards() -> bool:
    frozen = {
        "query": EXPECTED_QUERY_SPEC_DIGEST,
        "vocabulary": EXPECTED_STAGE_VOCABULARY_DIGEST,
        "unit_ids": EXPECTED_STAGE_UNIT_IDS_DIGEST,
        "unit_projection": EXPECTED_STAGE_UNIT_PROJECTION_DIGEST,
        "normalized_results": EXPECTED_NORMALIZED_RESULT_DIGEST,
        "result_unit_ids": EXPECTED_RESULT_UNIT_IDS_DIGEST,
    }
    return (
        "__FILL_" in json.dumps(frozen)
        or EXPECTED_RESULT_PAIR_COUNT < 0
        or EXPECTED_UNIQUE_RESULT_UNIT_COUNT < 0
        or not EXPECTED_HIT_COUNTS
        or not EXPECTED_PATH_PAIR_COUNTS
        or not EXPECTED_PATH_UNIQUE_UNIT_COUNTS
    )


def _target_goal_dir() -> Path:
    value = os.environ.get("GOAL4_STAGE11_SEARCH_GOAL_DIR")
    if value is None:
        return core.GOAL_DIR
    target = Path(value).resolve()
    if target != core.GOAL_DIR.resolve() and not target.is_relative_to(
        Path("/tmp").resolve()
    ):
        raise core.AuthoringError(
            "simulation goal directory must be canonical Goal 4 or under /tmp"
        )
    core.GOAL_DIR = target
    return target


def main() -> int:
    _install_stage_constants()
    try:
        goal_dir = _target_goal_dir()
    except (OSError, core.AuthoringError, ValueError) as exc:
        print(f"Chapter 7 search setup failed: {exc}", file=sys.stderr)
        return 1

    if sys.argv[1:] == ["--calibrate-source"]:
        try:
            projection = core._source_projection(goal_dir)
        except (OSError, json.JSONDecodeError, core.AuthoringError, ValueError) as exc:
            print(f"Chapter 7 source calibration failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(projection, indent=2, sort_keys=True))
        return 0

    if sys.argv[1:] == ["--self-check-source"]:
        if _unresolved_source_guards():
            print("Chapter 7 source guards are unresolved", file=sys.stderr)
            return 1
        try:
            core._assert_source_projection(core._source_projection(goal_dir))
        except (OSError, json.JSONDecodeError, core.AuthoringError, ValueError) as exc:
            print(f"Chapter 7 source self-check failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(core._source_projection(goal_dir), indent=2, sort_keys=True))
        return 0

    if sys.argv[1:] == ["--calibrate-post-merge"]:
        if _unresolved_source_guards():
            print("Chapter 7 source guards are unresolved", file=sys.stderr)
            return 1
        try:
            core._assert_source_projection(core._source_projection(goal_dir))
            with core.audit_transaction.read_guard(goal_dir):
                state, semantic, round_guard = core._analyze_post_merge(
                    goal_dir,
                    enforce_frozen=False,
                )
        except (OSError, json.JSONDecodeError, core.AuthoringError, ValueError) as exc:
            print(
                f"Chapter 7 post-merge calibration failed: {exc}",
                file=sys.stderr,
            )
            return 1
        print(
            json.dumps(
                {
                    "round_id": state["round_id"],
                    "semantic": semantic,
                    "round_guard": round_guard,
                    "compatibility_result_digest": (
                        _LAST_COMPATIBILITY_RESULT_DIGEST
                    ),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if len(sys.argv) != 2:
        print(
            f"usage: {Path(sys.argv[0]).name} "
            "[--calibrate-source|--self-check-source|"
            "--calibrate-post-merge|OUTPUT_JSON]",
            file=sys.stderr,
        )
        return 2
    if _unresolved_source_guards():
        print("Chapter 7 source guards are unresolved", file=sys.stderr)
        return 1

    output_path = Path(sys.argv[1])
    try:
        with core.audit_transaction.read_guard(goal_dir):
            proposal = core.build_proposal(goal_dir)
            core.atomic_create(
                output_path,
                core.canonical_json_bytes(proposal),
            )
    except (OSError, json.JSONDecodeError, core.AuthoringError, ValueError) as exc:
        print(f"Chapter 7 search authoring failed: {exc}", file=sys.stderr)
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
        "new_candidates=0 new_evidence_groups=0 new_routes=0 "
        f"dispositions={json.dumps(counts, sort_keys=True)} "
        f"digest={round_record['result_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
