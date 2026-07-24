#!/usr/bin/env python3
"""Author the closed Stage 10 Chapter 6 paired-scope LOCAL search.

The frozen search scope is exactly the Chapter 6 main text and its notes.
The first invocation, after the blind merge and route-resolution transactions,
authors S015.  Once S015 is applied, the second invocation authors S016 and
requires an identical normalized hit projection with no semantic delta.

The source-side family can be checked before V000028 with
``--self-check-source``.  The V000028/V000029 ledger projections cannot be
known until the final main-text worker output is merged and route IDs are
allocated.  ``--calibrate-post-merge`` prints those read-only projections;
proposal authoring remains fail-closed until they are copied into the frozen
guard dictionaries below.  This helper never applies a transaction.

Design provenance: the notes vocabulary was read from the exact worker output
with SHA-256 41b827fd531ec5d3b7f1902fd3ad5725386a7dfaf7f64411c90243af1513e81f.
The main-text vocabulary remains provisional until its final hostile-audit
hash is accepted.
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
import merge_worker_output  # noqa: E402
import validate_audit  # noqa: E402
from audit_contract import (  # noqa: E402
    GOAL_DIR,
    REPO_ROOT,
    canonical_json_bytes,
)


STAGE_PATHS = [
    "CHAPTERS/06-Starting-from-Randomness.md",
    "BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes.md",
]
STAGE = 10
EPOCH = 2
COORDINATOR_ID = "ch06-randomness-local-search-e2"

ASSUMPTION = (
    "Python Unicode regular expressions over decoded UTF-8 canonical "
    "source-unit byte ranges, with IGNORECASE and MULTILINE semantics and "
    "query-major then canonical source-unit result order."
)

# This is the mechanically deduplicated Chapter 6 vocabulary learned from the
# exact final notes output and the current provisional main-text output.  It
# must be re-projected once the main-text hostile audit accepts an exact hash.
PROPOSED_VOCABULARY = list(
    dict.fromkeys(
        value
        for value in """
random cellular-automaton initial-field generator family
completely random initial conditions
elementary cellular automaton rule 254
uniform-attractor elementary cellular-automaton preset panel
fixed-or-periodic-structure elementary cellular-automaton preset panel
elementary cellular automaton rule 126
rule 126
elementary cellular automaton rule 22
elementary cellular automaton rule 30
elementary cellular automaton rule 150
elementary cellular automaton rule 182
rule 182
elementary cellular automaton rule 90
elementary cellular automaton rule 105
elementary cellular automaton rule 110
four-class cellular-automaton behavior classification
four classes of behavior
classes 1, 2, 3, and 4
symmetric quiescent-white binary nearest-neighbor cellular-automaton family
binary next-nearest-neighbor totalistic cellular-automaton family
three-color nearest-neighbor totalistic cellular-automaton family
three-color nearest-neighbor totalistic cellular automaton code 1815
code 1815
three-color nearest-neighbor totalistic cellular automaton code 2007
code 2007
three-color nearest-neighbor totalistic cellular automaton code 1659
code 1659
three-color nearest-neighbor totalistic cellular automaton code 2043
code 2043
four-color nearest-neighbor totalistic cellular-automaton sequence
fractional-average continuous cellular automaton
neighbor-difference gray-field display transformation
neighbor-difference display
stripe-removing gray display
neighbor-weighted fractional-average continuous cellular automaton
one-dimensional slice-through-time and spatial-depth-fog observer
one-dimensional slice observer
slice-history projection
spatial-depth fog display
Game of Life cellular automaton
outer totalistic 9-neighbor code 224
binary two-dimensional von-Neumann-totalistic cellular-automaton family
prior-time gray-trail rendering observer
temporal fog
prior-step gray trail
single-cell initial-perturbation difference observer
sensitivity to initial conditions experiment
finite-system repetition-period and maximum-period observer
finite repetition-period query
period-versus-size observer
finite cyclic translation of a single dot
single-dot wraparound system
finite cyclic doubling map
finite cyclic binary cellular automaton
limited-size cellular automaton
periodic-boundary cellular automaton
elementary cellular automaton rule 45 on a finite cycle
additive cellular-automaton superposition relation
cellular-automaton additivity
pattern superposition
periodic-block cellular-automaton initial-condition generator
fixed block repeated forever
rule-126 random two-block initial-condition ensemble
rule-126 to rule-90 pair-block emulation
rule 126 emulates rule 90
rule-90 pair-block self-emulation
rule 90 emulates itself
rule-150 block self-emulation
rule 150 emulates itself
elementary cellular automaton rule 184
rule 184
rule-184 three-cell-block self-emulation
rule 184 emulates itself
nested substitution initial condition for rule 184
next-nearest cellular automaton rule 4067213884
rule 4067213884
full binary configuration language
all possible black-and-white sequences
elementary cellular automaton rule 255
rule 255
rule-255 all-black attractor
elementary cellular automaton rule 4
rule 4
rule-4 isolated-black attractor-set constraint
rule-4 many-to-one basin-of-attraction relation
allowed-sequence path-network observer
network of possible sequences
elementary cellular automaton rule 128
rule 128
surjective binary cellular-automaton mapping family
onto cellular automata
surjective cellular automata
conflicted adjacent-black constrained initial-condition language
two-color next-nearest-neighbor cellular automaton code 20
code 20 cellular automaton
persistent-structure exhaustive search query
persistent structure search
three-color nearest-neighbor cellular automaton code 357
code 357 cellular automaton
three-color nearest-neighbor cellular automaton code 1329
code 1329 cellular automaton
localized finite-seed integer codec family
initial-condition integer codec
systematic fixed-period persistent-structure constraint solver
complete fixed-period structure search
fair random cellular-automaton initial-condition ensemble
random initial condition
long-run cellular-automaton density and pattern-statistics survey
cellular automaton with continual center-cell randomness injection
elementary-rule bit-pattern selector
three-color one-dimensional totalistic class-4 preset family
1D totalistic class-4 rules
one-dimensional totalistic rule-class frequency survey
class-1 no-surviving-pattern decision query
continuously parameterized cellular automaton family
continuous cellular automata
larger-range cellular-automaton rule embedding transform
edge-local cellular-automaton rule-nearness relation
nine-neighbor outer-totalistic two-dimensional class-4 preset family
2D class 4 outer-totalistic rules
Life
code 224
three-dimensional Life-like cellular automaton family
random infinite-sequence initial-condition generator
cellular-automaton difference-pattern observer
two-k-color cellular-automaton difference-emulation lift
cellular-automaton perturbation-growth Lyapunov analyzer
cyclic addition dot system
cyclic multiplication dot system
primitive spatial-period state-count function
finite cyclic rule-60 polynomial cellular automaton
rule 60 with cyclic boundary conditions
finite cyclic rule-60 repetition-period bound function
finite cyclic rule-90 polynomial cellular automaton
rule 90 with cyclic boundary conditions
finite cyclic rule-90 repetition-period bound function
finite-ring cellular-automaton repetition-period comparison survey
finite cellular-automaton boundary implementation codec
rule-22 randomness-producing seed family
elementary cellular automaton rule 225
elementary cellular automaton rule 94
rule 94
elementary cellular automaton rule 218
rule 218
weighted additive cellular automaton family
generalized-additive monoid cellular automaton family
integer- or real-valued linear cellular automaton family
Cauchy-additive function constraint
irrational-modulus additive cellular automaton
local linear differential-operator function evolution
independent-cell mean-field density map for cellular automata
mean field theory
mean field theories
rule-90 density evolution function
cellular-automaton density-response raster analyzer
rule-73 fair-random initial-condition ensemble
rule-73 no-even-black-block initial-condition filter
rule-73 period-3 density-oscillation analyzer
exact-period-p repeating-configuration constraint for one-dimensional cellular automata
rule-90 repeating-block seed preset survey for periods 1 through 10
period-dividing cellular-automaton configuration count function
two-dimensional repeating-configuration constraint
modular multiplication circle map
Anosov torus map family
continued-fraction map
polynomial iterated-map family
p-return point query for an iterated map
Sarkovskii period-implication relation
renormalization-group blocking transformation
prime-modulus additive-CA scale self-emulation transform
additive-cellular-automaton fractal-dimension analyzer
associative-operation cellular automaton family
rule-45 nested-background seed preset
elementary-rule pattern-uniqueness analyzer
three-state cellular-automaton square roots of rule 30
nested-sequence initial-condition family for rule 90
finite-automaton path recognizer
finite automaton
finite state machine
nondeterministic finite automaton
NDFA
sequential machine
sequential machines
cellular-automaton image-set network transform
NetCAStep
NDFA image-network transform
deterministic finite-automaton minimizer
MinNet
DFA minimizer
trimmed sequence-network transformer
TrimNet
regular language
sofic system
sofic systems
regular-expression sequence denotation
regular expression
rational generating-function representation of a regular language
cellular-automaton image-network growth and maximum-size analyzer
finite-complement language
subshift of finite type
spatial topological-entropy analyzer
limiting spatial-entropy bound decision query
dynamical zeta function of network cycles
hard-square no-adjacent-black constraint model
hard-hexagon lattice-gas model
square-grid domino-covering constraint
dimer problem
measure-entropy analyzer
entropy
information
information dimension
set/topological entropy from block-support growth
set entropy
topological entropy
capacity
fractal dimension
generalized q-entropy analyzer
generalized dimensions
sequence-set to Cantor-set encoding
finite sequence-network to substitution-system transform
cellular-automaton surjectivity decision query
surjective
onto
cellular-automaton injectivity, bijectivity, and reversibility decision relation
injective
one-to-one
bijective
automorphism
reversible
full temporal-sequence language for additive cellular automata
rule-18 no-adjacent-black temporal-sequence language
temporal-sequence entropy analyzer
topological spacetime-entropy analyzer
invariant entropy
measure spacetime-entropy analyzer
full left-shift symbolic dynamical system
full shift
finite global-state transition graph
left-shift cellular automaton rule 170
shift rule
shift-rule necklace-cycle count function
shift-rule exact-cycle-length count function
random functional-digraph ensemble
random functional-network statistics analyzer
code-20 initial-condition survival-time analyzer
rule-110 periodic background field
rule-110 background function
rule-110 persistent-structure seed preset survey
rule-110 period/displacement semigroup constraint
rule-110 collision-based structure extension transform
rule-110 extended b/c structure seed generator
rule-110 glider-gun initial condition
rule-110 collision width-conservation modulo-14 relation
Game of Life block still life
Game of Life beehive still life
Game of Life blinker oscillator
Game of Life glider
Game of Life spaceship
Game of Life still-life catalogue below eight live cells
bounded Game of Life exact-period oscillator example survey
bounded Game of Life velocity-class example survey
Gosper Game of Life glider gun
Game of Life switch engine
Game of Life pulsar puffer
Game of Life spaceship gun
infinite-line Game of Life seed
Game of Life spacefiller
Game of Life puffer train
""".splitlines()
        if value
    )
)

QUERY_SPECS = [
    (
        "named cellular automata, rules, codes, and Life constructions",
        (
            r"\b(?:cellular automata?|rules?\s*(?:4|18|20|22|30|45|60|"
            r"73|90|94|105|110|126|128|150|170|182|184|218|225|250|"
            r"254|255)\b|rule[- ]?(?:number|code)|codes?\s*(?:20|224|"
            r"357|1329|1659|1815|2007|2043|4067213884)\b|Game of Life|"
            r"Life[- ]like|outer[- ]totalistic|totalistic|"
            r"nearest[- ]neighbor|next[- ]nearest[- ]neighbor|"
            r"von Neumann)\b"
        ),
        "REGEX",
    ),
    (
        "randomness, probability, density, seed, and initial-condition generation",
        (
            r"\b(?:random(?:ness|ly)?|pseudorandom|stochastic|"
            r"probabilit(?:y|ies)|probability law|Bernoulli|mean[- ]field|"
            r"statistical|density|densities|initial conditions?|"
            r"initial configurations?|initial fields?|seeds?|"
            r"starting configurations?|starting from|"
            r"generate(?:s|d|r|rs|tion)?|ensemble|independent(?:ly)?|"
            r"distribution|measure)\b"
        ),
        "REGEX",
    ),
    (
        "native state, rule, neighborhood, update, and evolution mechanics",
        (
            r"\b(?:states?|configurations?|cells?|values?|colors?|"
            r"neighbou?rs?|neighbou?rhoods?|ranges?|rules?|codes?|steps?|"
            r"updates?|successors?|evol(?:ve|ves|ved|ving|ution)|"
            r"iterations?|maps?|transitions?|apply|applied|"
            r"replac(?:e|es|ed|ing|ement)|parallel|synchronous|"
            r"cyclic boundar(?:y|ies)|wrap(?:s|ped)? around|finite sizes?|"
            r"limited sizes?|lattices?|grids?)\b"
        ),
        "REGEX",
    ),
    (
        "behavior classes, order, chaos, and pattern production",
        (
            r"\b(?:class(?:es)?\s*(?:1|2|3|4|one|two|three|four)?|"
            r"four classes|behavior|behaviour|order(?:ed)?|chaos|chaotic|"
            r"complex(?:ity)?|pattern(?:s|ed)?|uniform|stable|localized|"
            r"nested|irregular|regular|symmetr(?:y|ies|ic)|growth|"
            r"dies out|surviv(?:e|es|ed|ing|al))\b"
        ),
        "REGEX",
    ),
    (
        "attractors, basins, periods, repetition, cycles, and recurrence",
        (
            r"\b(?:attractors?|basins?(?: of attraction)?|preimages?|"
            r"fixed points?|period(?:s|ic|icity)?|repetition|"
            r"repeat(?:s|ed|ing)?|cycles?|cyclic|recurr(?:ence|ent)|"
            r"return(?:s|ed|ing)?|oscillat(?:e|es|ed|ing|ion|ions|or|ors)|"
            r"transients?|long[- ]run|asymptotic|limit(?:ing)?|"
            r"maximum period|eventually)\b"
        ),
        "REGEX",
    ),
    (
        "persistent structures, particles, collisions, and Life forms",
        (
            r"\b(?:persistent structures?|structures?|particles?|"
            r"localized structures?|backgrounds?|domains?|defects?|"
            r"collisions?|gliders?|glider guns?|still lifes?|blinkers?|"
            r"spaceships?|spacefillers?|puffers?|puffer trains?|"
            r"switch engines?|pulsars?|beehives?|blocks?|Gosper|"
            r"propagat(?:e|es|ed|ing)|displacements?|velocit(?:y|ies)|"
            r"width conservation)\b"
        ),
        "REGEX",
    ),
    (
        "constraints, languages, automata, and decision relations",
        (
            r"\b(?:constraints?|relations?|queries?|"
            r"decid(?:e|es|ed|ing|able|ability)|"
            r"accept(?:s|ed|ing|ance)?|allowed|forbidden|languages?|"
            r"regular expressions?|finite automata?|finite state machines?|"
            r"nondeterministic finite automata?|NDFA|DFA|MinNet|TrimNet|"
            r"sofic|subshifts?|surjectiv(?:e|ity)|injectiv(?:e|ity)|"
            r"bijectiv(?:e|ity)|reversib(?:le|ility)|automorphisms?|"
            r"one[- ]to[- ]one|onto|satisf(?:y|ies|ied|action)|solutions?|"
            r"models?|all possible sequences?|no adjacent)\b"
        ),
        "REGEX",
    ),
    (
        "generators, analyzers, transforms, observers, inputs, and outputs",
        (
            r"\b(?:generators?|generate(?:s|d|ing|tion)?|"
            r"analy[sz](?:e|es|ed|ing|er|ers|is)|observers?|surveys?|"
            r"experiments?|transform(?:s|ed|ing|ation)?|"
            r"encod(?:e|es|ed|ing|er|ers)|decod(?:e|es|ed|ing|er|ers)|"
            r"represent(?:s|ed|ing|ation)?|emulat(?:e|es|ed|ing|ion)|"
            r"simulat(?:e|es|ed|ing|ion)|inputs?|outputs?|results?|"
            r"functions?|statistics?|counts?|"
            r"classif(?:y|ies|ied|ication)|search(?:es|ed|ing)?|"
            r"enumerat(?:e|es|ed|ing|ion)|render(?:s|ed|ing)?|"
            r"display(?:s|ed|ing)?|plots?|pictures?)\b"
        ),
        "REGEX",
    ),
    (
        "maps, functions, formulas, equations, entropy, and quantitative laws",
        (
            r"\b(?:maps?|functions?|formulas?|equations?|polynomials?|"
            r"eigenvalues?|matrices?|coefficients?|modulo|modular|addition|"
            r"multiplication|fractional|continued fractions?|logistic|"
            r"Anosov|Sarkovskii|Lyapunov|renormalization|entropy|entropies|"
            r"information|dimensions?|zeta|generating functions?|Perron|"
            r"Myhill|Nerode|semigroups?|monoids?|associative|"
            r"differential operators?|mean field)\b|"
            r"`[^`\n]*(?:->|→|==|:=|:>|Nest|NestList|Map|Table|Replace|"
            r"Rule|Step|Evolve|LinearSolve)[^`\n]*`"
        ),
        "REGEX",
    ),
    (
        "broad construction and mechanism anchors",
        (
            r"\b(?:rules?|systems?|programs?|processes?|algorithms?|"
            r"procedures?|constructions?|presets?|families|models?|"
            r"relations?|constraints?|functions?|maps?|generators?|"
            r"analyzers?|observers?|transformations?|automata?|networks?|"
            r"sequences?|configurations?|patterns?|structures?|"
            r"initial conditions?|evolution|steps?|states?|results?|"
            r"inputs?|outputs?|examples?|cases?)\b|"
            r"(?:^|\n)\s*(?:!\[[^\]]*\]\([^)]+\)|```)"
        ),
        "REGEX",
    ),
    (
        "headings, captions, image, and code anchors",
        (
            r"(?:^|\n)\s*(?:#{1,6}\s+[^\n]+|"
            r"!\[[^\]]*\]\([^)]+\)|```)|"
            r"\b(?:figure|picture|diagram|table|caption|shown|displayed|"
            r"illustrated|above|below|left|right|top|bottom)\b"
        ),
        "REGEX",
    ),
    (
        "observer, representation, and implementation boundary",
        (
            r"\b(?:pictures?|plots?|displays?|"
            r"visualiz(?:e|es|ed|ing|ation)|"
            r"represent(?:s|ed|ing|ation)?|"
            r"implement(?:s|ed|ing|ation)?|"
            r"simulat(?:e|es|ed|ing|ion)|render(?:s|ed|ing)?|"
            r"projections?|slices?|histories|history|trajector(?:y|ies)|"
            r"spacetime|space[- ]time|difference patterns?|gray trails?|"
            r"fog|networks?|graphs?|statistics?|"
            r"measure(?:s|d|ment)?|Mathematica)\b"
        ),
        "REGEX",
    ),
    (
        "probability, generator, constraint, and sampling aliases",
        (
            r"\b(?:probability laws?|initial[- ]state generators?|"
            r"initial[- ]condition generators?|configuration constraints?|"
            r"sampling|sample(?:s|d)?|random fields?|random sequences?|"
            r"random networks?|random mappings?|functional digraphs?|"
            r"fair random|bias(?:ed)?|black[- ]cell density|survival time|"
            r"periodic backgrounds?|repeating blocks?|nested sequences?)\b"
        ),
        "REGEX",
    ),
    (
        "Stage 10 discovered construction vocabulary",
        (
            r"\b(?:neighbor[- ]difference|fractional[- ]average|prior[- ]time|"
            r"gray[- ]trail|single[- ]cell perturbation|superposition|"
            r"block self[- ]emulation|pair[- ]block emulation|"
            r"period[- ]dividing|return points?|blocking transformation|"
            r"fractal dimension|Cauchy[- ]additive|irrational modulus|"
            r"image[- ]set network|topological entropy|spacetime entropy|"
            r"dynamical zeta|hard square|hard hexagon|domino covering|"
            r"Cantor[- ]set encoding|global[- ]state transition graph|"
            r"necklace cycles?|functional[- ]network|period/displacement|"
            r"collision[- ]based|exact[- ]period|velocity[- ]class)\b"
        ),
        "REGEX",
    ),
    (
        "typed cross-reference and locator obligations",
        (
            r"\b(?:pages?|page|chapter)\s+"
            r"(?:\d+|[IVX]+)(?:[–-]\d+)?\b|"
            r"\b(?:the\s+)?(?:(?:top|bottom)\s+of\s+(?:the\s+)?)?"
            r"(?:facing|previous|next)(?:\s+(?:one|two|three))?"
            r"\s+pages?\b|"
            r"\b(?:previous section|next chapter|next few chapters|"
            r"later in (?:this|the) book)\b"
        ),
        "REGEX",
    ),
]

# Source-only constants can be established before V000028.  They are filled
# after running --self-check-source during authoring.
EXPECTED_QUERY_SPEC_DIGEST = (
    "40ea5944b0ff1d77a6d48b234474ae697cd6762ea3891dc4c5b75b1161262bf0"
)
EXPECTED_STAGE_VOCABULARY_COUNT = 268
EXPECTED_STAGE_VOCABULARY_DIGEST = (
    "573440bb29785c50ccac67500a9e3b9ffcd7574823606e383e488a0b389fc5e3"
)
EXPECTED_STAGE_UNIT_COUNT = 607
EXPECTED_STAGE_ASSET_COUNT = 177
EXPECTED_STAGE_UNIT_IDS_DIGEST = (
    "cb188d1f8a550b87de696869aad8e19f6b96933fc8b52e95f47ba42e3959b3d6"
)
EXPECTED_STAGE_UNIT_PROJECTION_DIGEST = (
    "60c2b06f0b6b4a06541d8ddc470bcb7b5a9ef18215e92643aa9ebfe90e506ab1"
)
EXPECTED_SOURCE_SHA256 = {
    STAGE_PATHS[0]: (
        "0eb4ebc5400c3e3ed39fb2dd8fd9c38a2977eaef1ffefb528fd4c2708a42dca5"
    ),
    STAGE_PATHS[1]: (
        "23b589b5e711b93d2e4eb85f78c36e6c39f5b418f73a72bd79697fe6575f5a93"
    ),
}
EXPECTED_RESULT_PAIR_COUNT = 2665
EXPECTED_UNIQUE_RESULT_UNIT_COUNT = 591
EXPECTED_HIT_COUNTS = [
    213,
    180,
    322,
    228,
    106,
    128,
    39,
    158,
    83,
    559,
    350,
    135,
    7,
    12,
    145,
]
EXPECTED_PATH_PAIR_COUNTS = {
    STAGE_PATHS[0]: 1546,
    STAGE_PATHS[1]: 1119,
}
EXPECTED_PATH_UNIQUE_UNIT_COUNTS = {
    STAGE_PATHS[0]: 350,
    STAGE_PATHS[1]: 241,
}
EXPECTED_NORMALIZED_RESULT_DIGEST = (
    "69c987503995ba8624d58a1b6df87ca251f9838c71a9b1788a48b7b4582016c9"
)
EXPECTED_RESULT_UNIT_IDS_DIGEST = (
    "d99900888698352eacad691e91b957f1c61d4d391db593c112113b7d31e30ab8"
)

# These values are fixed by the closed S001-S014 prefix and do not depend on
# Stage 10 candidate or route allocation.
EXPECTED_CLOSED_ROUND_COUNT = 14
EXPECTED_CLOSED_ROUNDS_DIGEST = (
    "0e6d5001c789c5c30965a986033265ae036dff2b26354b29676f73732c1e3a0b"
)
EXPECTED_QUERY_START = {"S015": 179, "S016": 194}
EXPECTED_HIT_START = {"S015": 13301, "S016": 15966}
EXPECTED_GLOBAL_VOCABULARY_COUNT: dict[str, int] = {
    "S015": 448,
    "S016": 716,
}
EXPECTED_GLOBAL_VOCABULARY_DIGEST = {
    "S015": (
        "bb73796d6c3d42d7e80efb1d3fc3e9652508c8b9ca850a3fcd5936c53302b5c9"
    ),
    "S016": (
        "c98559ab14e510f32f4f7e13852bed3d8ec016b1708dce7c94764d8120e693d6"
    ),
}
EXPECTED_GLOBAL_ASSUMPTIONS_COUNT = 2
EXPECTED_GLOBAL_ASSUMPTIONS_DIGEST = (
    "671219eeacdded499c971a237e87b358ec687bfb6f085425d101d5d007a20afd"
)

# Do not guess these.  The shared semantic projection is available only after
# the accepted main output and exact notes output are merged and the V000028
# route IDs exist.  S016's base/event/result guards become available only
# after the exact S015 proposal is applied as V000029.
EXPECTED_POST_MERGE_SEMANTICS: dict[str, Any] = {
    "stage_reading_count": 607,
    "stage_reading_digest": (
        "7a3a51940f6d65be4e0f5ee8fd1684edcf320bf01e94705459c17c3455f59354"
    ),
    "stage_asset_count": 177,
    "stage_asset_digest": (
        "92ab2772906b38448b204971bc67c9ead196fd983284662efb816d9613af2c6f"
    ),
    "stage_candidate_count": 181,
    "stage_candidate_ids_digest": (
        "cf6d770bdacbffbcd05dd6681699e3f8b7407b1b46de65bf64460dbf9a2ba963"
    ),
    "triage_digest": (
        "f232e4154fad7d8253c08ead7ad100a942a8c76d7446bacb57dbfe188d85010f"
    ),
    "candidate_coverage_digest": (
        "c3d89c71298eace34c3108fab4acca2544c1bdc0067278a10f1b46222008a013"
    ),
    "omission_challenge_count": 331,
    "omission_challenge_digest": (
        "840b6a6269eaea0c2ebd70cc068981626e50febb6e40b9103bc5fb4c570ea996"
    ),
    "route_coverage_count": 179,
    "route_coverage_digest": (
        "153e9b26af249c920f4ff90cf6af0ce554c00a6e5c7845213e3a917a863ea97b"
    ),
    "disposition_counts": {
        "CONTROL_OR_RELATIONSHIP": 12,
        "CROSS_REFERENCE": 57,
        "EXCLUSION": 378,
        "GOVERNED_CANDIDATE_OR_SUPPORT": 2218,
    },
    "normalized_hit_projection_digest": (
        "08c4877cf250c1215cb6b7a90a551960a32c121ae4d610b24ca7a6a4e5c47c61"
    ),
}
EXPECTED_ROUND_GUARDS: dict[str, dict[str, Any]] = {
    "S015": {
        "prior_event_sha256": (
            "5c5f09889b0a0ce8ed245d650edfd2c4854e1d5ff6fe157f045edebaa3ba3f7d"
        ),
        "base_artifact_sha256": {
            "asset-ledger.csv": (
                "b57d00e4d9bc1cde61d79acf869b3968e5b2e5e871d9938de099d0bb035d8f4e"
            ),
            "candidate-ledger.jsonl": (
                "8ba1ffba5061a2e115063c6b552b10369e53a3fd3bf4fcb08d3bfcaf7c8bf1c7"
            ),
            "cross-reference-ledger.csv": (
                "fda975932dade9ffd2b78380d87f27347ef45d32736f53418318b719d117a6fc"
            ),
            "reading-ledger.csv": (
                "e6fcdf7ca4ab1dbaf0f51aa29d4451eef98e15762f9fe22803d2c2121271303d"
            ),
            "review-history.jsonl": (
                "b74fc6f17bb6e4f162afb8158c1c7ce0b4ae944a6cefbae3503a89afa18870fe"
            ),
            "search-rounds.json": (
                "925eb472bf560e859fa6b28106edc913d827f816f2618fb31c000ddbe8c8cfd6"
            ),
        },
        "result_digest": (
            "f39684dcfdd2e95001082c664ffeddafbf7bb1278e4bef89c9085c022d5fe303"
        ),
    },
    "S016": {
        "prior_event_sha256": None,
        "base_artifact_sha256": None,
        "result_digest": None,
    },
}

DIRECT_STRENGTHS = {
    "DIRECT_IDENTITY",
    "DIRECT_PARTIAL_MECHANICS",
    "DIRECT_COMPLETE_MECHANICS",
    "DEFECT_LIMITED",
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


def _query_objects(query_start: int) -> list[dict[str, Any]]:
    return [
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
    ordinal_by_query_id = {
        query["query_id"]: ordinal
        for ordinal, query in enumerate(round_record["queries"], start=1)
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


def _source_projection(goal_dir: Path) -> dict[str, Any]:
    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    stage_units = [unit for unit in units if unit["path"] in STAGE_PATHS]
    stage_unit_ids = [unit["id"] for unit in stage_units]
    query_start = EXPECTED_QUERY_START["S015"]
    queries = _query_objects(query_start)
    result_pairs, query_errors = validate_audit.execute_frozen_queries(
        queries,
        units,
        REPO_ROOT / "ref" / "A-New-Kind-of-Science",
    )
    if query_errors:
        raise AuthoringError("; ".join(query_errors))
    normalized_pairs = _normalized_result_pairs(result_pairs, query_start)
    result_unit_ids = sorted({unit_id for _, unit_id in result_pairs})
    unit_by_id = {unit["id"]: unit for unit in units}
    return {
        "query_spec_digest": digest(QUERY_SPECS),
        "stage_vocabulary_count": len(PROPOSED_VOCABULARY),
        "stage_vocabulary_digest": digest(PROPOSED_VOCABULARY),
        "stage_unit_count": len(stage_units),
        "stage_unit_ids_digest": digest(stage_unit_ids),
        "stage_unit_projection_digest": digest(stage_units),
        "source_sha256": {
            path: hashlib.sha256(
                (
                    REPO_ROOT / "ref" / "A-New-Kind-of-Science" / path
                ).read_bytes()
            ).hexdigest()
            for path in STAGE_PATHS
        },
        "result_pair_count": len(result_pairs),
        "unique_result_unit_count": len(result_unit_ids),
        "hit_counts": [
            sum(query_id == query["query_id"] for query_id, _ in result_pairs)
            for query in queries
        ],
        "path_pair_counts": {
            path: sum(
                unit_by_id[unit_id]["path"] == path
                for _, unit_id in result_pairs
            )
            for path in STAGE_PATHS
        },
        "path_unique_unit_counts": {
            path: sum(
                unit_by_id[unit_id]["path"] == path
                for unit_id in result_unit_ids
            )
            for path in STAGE_PATHS
        },
        "normalized_result_digest": digest(normalized_pairs),
        "result_unit_ids_digest": digest(result_unit_ids),
    }


def _assert_source_projection(projection: dict[str, Any]) -> None:
    expected = {
        "query_spec_digest": EXPECTED_QUERY_SPEC_DIGEST,
        "stage_vocabulary_count": EXPECTED_STAGE_VOCABULARY_COUNT,
        "stage_vocabulary_digest": EXPECTED_STAGE_VOCABULARY_DIGEST,
        "stage_unit_count": EXPECTED_STAGE_UNIT_COUNT,
        "stage_unit_ids_digest": EXPECTED_STAGE_UNIT_IDS_DIGEST,
        "stage_unit_projection_digest": EXPECTED_STAGE_UNIT_PROJECTION_DIGEST,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "result_pair_count": EXPECTED_RESULT_PAIR_COUNT,
        "unique_result_unit_count": EXPECTED_UNIQUE_RESULT_UNIT_COUNT,
        "hit_counts": EXPECTED_HIT_COUNTS,
        "path_pair_counts": EXPECTED_PATH_PAIR_COUNTS,
        "path_unique_unit_counts": EXPECTED_PATH_UNIQUE_UNIT_COUNTS,
        "normalized_result_digest": EXPECTED_NORMALIZED_RESULT_DIGEST,
        "result_unit_ids_digest": EXPECTED_RESULT_UNIT_IDS_DIGEST,
    }
    if projection != expected:
        raise AuthoringError(
            "the frozen Stage 10 source/query projection drifted: "
            f"{json.dumps(projection, sort_keys=True)}"
        )


def _require_closed_round_prefix(
    rounds: list[dict[str, Any]],
    *,
    enforce_frozen: bool,
) -> str:
    if len(rounds) not in {14, 15}:
        raise AuthoringError(
            "expected the fourteen closed S001-S014 rounds and zero/one "
            f"Stage 10 round, got {len(rounds)}"
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
    ]
    observed = [
        (
            record.get("round_id"),
            record.get("kind"),
            record.get("owning_stage"),
            record.get("epoch"),
        )
        for record in rounds[:14]
    ]
    if observed != expected_prefix:
        raise AuthoringError("the closed S001-S014 LOCAL prefix drifted")
    if digest(rounds[:14]) != EXPECTED_CLOSED_ROUNDS_DIGEST:
        raise AuthoringError("the exact closed S001-S014 round prefix drifted")
    round_id = f"S{len(rounds) + 1:03d}"
    if round_id == "S016":
        prior = rounds[14]
        guard = EXPECTED_ROUND_GUARDS["S015"]
        if (
            prior.get("round_id") != "S015"
            or prior.get("kind") != "LOCAL"
            or prior.get("owning_stage") != STAGE
            or prior.get("epoch") != EPOCH
            or prior.get("queries")
            != _query_objects(EXPECTED_QUERY_START["S015"])
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
            raise AuthoringError("the applied S015 seed round drifted")
    return round_id


def _require_history(
    history: list[dict[str, Any]],
    round_id: str,
    *,
    enforce_frozen: bool,
) -> None:
    expected_length = 28 if round_id == "S015" else 29
    if len(history) != expected_length:
        raise AuthoringError(
            f"{round_id} expected {expected_length} review events, "
            f"got {len(history)}"
        )
    for number, event in enumerate(history, start=1):
        if event.get("review_id") != f"V{number:06d}":
            raise AuthoringError("review-history ID sequence drifted")
    prior = history[-1]
    expected_review_id = "V000028" if round_id == "S015" else "V000029"
    expected_mode = "ROUTE_RESOLUTION" if round_id == "S015" else "SEARCH_APPEND"
    expected_reviewer = None if round_id == "S015" else COORDINATOR_ID
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
        raise AuthoringError(f"{round_id} prior terminal review event drifted")
    if enforce_frozen and prior.get("event_sha256") != (
        EXPECTED_ROUND_GUARDS[round_id]["prior_event_sha256"]
    ):
        raise AuthoringError(f"{round_id} prior event digest drifted")


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
        f"Paired-scope omission challenge F{family_ordinal:02d} "
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


def _candidate_coverage_projection(
    *,
    expected_candidates: set[str],
    candidates_by_id: dict[str, dict[str, Any]],
    reading_by_id: dict[str, dict[str, str]],
    normalized_pairs: list[tuple[int, str]],
    stage_unit_ids: set[str],
) -> list[dict[str, Any]]:
    pair_set = set(normalized_pairs)
    coverage: list[dict[str, Any]] = []
    for candidate_id in sorted(expected_candidates):
        candidate = candidates_by_id[candidate_id]
        candidate_units = set(candidate["source_unit_ids"])
        candidate_units.update(
            item["source_unit_id"]
            for item in candidate["source_evidence"]
            if isinstance(item, dict)
            and isinstance(item.get("source_unit_id"), str)
        )
        witnesses = sorted(
            (ordinal, unit_id)
            for ordinal, unit_id in pair_set
            if ordinal <= 10
            and unit_id in candidate_units
            and candidate_id
            in parse_links(
                reading_by_id[unit_id]["candidate_ids"],
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
            if isinstance(item, dict)
            and item.get("source_unit_id") in stage_unit_ids
            and item.get("strength") in DIRECT_STRENGTHS
        }
        if direct_units and not any(
            unit_id in direct_units for _, unit_id in witnesses
        ):
            raise AuthoringError(
                f"{candidate_id} lacks a direct-evidence search witness"
            )
        coverage.append(
            {
                "candidate_id": candidate_id,
                "witnesses": [
                    [ordinal, unit_id] for ordinal, unit_id in witnesses
                ],
                "direct_units": sorted(direct_units),
            }
        )
    return coverage


def _analyze_post_merge(
    goal_dir: Path,
    *,
    enforce_frozen: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    units = read_jsonl(goal_dir / merge_worker_output.UNITS_NAME)
    reading = read_csv(goal_dir / merge_worker_output.READING_NAME)
    assets = read_csv(goal_dir / merge_worker_output.ASSET_NAME)
    candidates = read_jsonl(goal_dir / merge_worker_output.CANDIDATE_NAME)
    routes = read_csv(goal_dir / merge_worker_output.ROUTE_NAME)
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(
            encoding="utf-8"
        )
    )
    history = read_jsonl(goal_dir / merge_worker_output.REVIEW_HISTORY_NAME)

    if search.get("fixed_point") is not None:
        raise AuthoringError("Stage 10 LOCAL closure cannot follow a fixed point")
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise AuthoringError("global search rounds are malformed")
    round_id = _require_closed_round_prefix(
        rounds,
        enforce_frozen=enforce_frozen,
    )
    _require_history(history, round_id, enforce_frozen=enforce_frozen)

    base_digests = artifact_digests(goal_dir)
    if enforce_frozen and base_digests != (
        EXPECTED_ROUND_GUARDS[round_id]["base_artifact_sha256"]
    ):
        raise AuthoringError(f"{round_id} base-artifact snapshot drifted")

    vocabulary = search.get("vocabulary")
    assumptions = search.get("tool_assumptions")
    if (
        not isinstance(vocabulary, list)
        or len(vocabulary) != EXPECTED_GLOBAL_VOCABULARY_COUNT[round_id]
        or len(vocabulary) != len(set(vocabulary))
        or digest(vocabulary)
        != EXPECTED_GLOBAL_VOCABULARY_DIGEST[round_id]
    ):
        raise AuthoringError(f"{round_id} global vocabulary drifted")
    if (
        not isinstance(assumptions, list)
        or len(assumptions) != EXPECTED_GLOBAL_ASSUMPTIONS_COUNT
        or len(assumptions) != len(set(assumptions))
        or digest(assumptions) != EXPECTED_GLOBAL_ASSUMPTIONS_DIGEST
        or ASSUMPTION not in assumptions
    ):
        raise AuthoringError("global search assumptions drifted")
    mechanically_new = [
        value for value in PROPOSED_VOCABULARY if value not in vocabulary
    ]
    if round_id == "S015":
        if mechanically_new != PROPOSED_VOCABULARY:
            raise AuthoringError(
                "Stage 10 vocabulary is not a fully new frozen suffix"
            )
        new_vocabulary = mechanically_new
    else:
        if mechanically_new:
            raise AuthoringError("the applied S015 vocabulary is incomplete")
        if vocabulary[-len(PROPOSED_VOCABULARY) :] != PROPOSED_VOCABULARY:
            raise AuthoringError("the applied S015 vocabulary suffix drifted")
        new_vocabulary = []

    unit_by_id = {unit["id"]: unit for unit in units}
    reading_by_id = {row["source_unit_id"]: row for row in reading}
    candidates_by_id = {candidate["id"]: candidate for candidate in candidates}
    routes_by_id = {route["route_id"]: route for route in routes}
    assets_by_id = {asset["asset_id"]: asset for asset in assets}
    if (
        len(unit_by_id) != len(units)
        or len(reading_by_id) != len(reading)
        or len(candidates_by_id) != len(candidates)
        or len(routes_by_id) != len(routes)
        or len(assets_by_id) != len(assets)
    ):
        raise AuthoringError("canonical ledgers contain duplicate IDs")

    stage_units = [unit for unit in units if unit["path"] in STAGE_PATHS]
    stage_unit_ids = {unit["id"] for unit in stage_units}
    stage_reading = [
        row for row in reading if row["source_unit_id"] in stage_unit_ids
    ]
    stage_assets = [
        row for row in assets if row["assignment_path"] in STAGE_PATHS
    ]
    if (
        len(stage_units) != EXPECTED_STAGE_UNIT_COUNT
        or len(stage_unit_ids) != EXPECTED_STAGE_UNIT_COUNT
    ):
        raise AuthoringError("Stage 10 source-unit scope drifted")
    if (
        len(stage_reading) != EXPECTED_STAGE_UNIT_COUNT
        or any(
            row["path"] not in STAGE_PATHS
            or row["review_status"] != "REVIEWED"
            or row["review_epoch"] != str(EPOCH)
            or row["review_stage"] != str(STAGE)
            for row in stage_reading
        )
        or (
            enforce_frozen
            and (
                len(stage_reading)
                != EXPECTED_POST_MERGE_SEMANTICS["stage_reading_count"]
                or digest(stage_reading)
                != EXPECTED_POST_MERGE_SEMANTICS["stage_reading_digest"]
            )
        )
    ):
        raise AuthoringError("Stage 10 reading projection drifted")
    if (
        len(stage_assets) != EXPECTED_STAGE_ASSET_COUNT
        or any(
            row["inspection_status"] != "SCREENED"
            or row["review_epoch"] != str(EPOCH)
            or row["review_stage"] != str(STAGE)
            for row in stage_assets
        )
        or (
            enforce_frozen
            and (
                len(stage_assets)
                != EXPECTED_POST_MERGE_SEMANTICS["stage_asset_count"]
                or digest(stage_assets)
                != EXPECTED_POST_MERGE_SEMANTICS["stage_asset_digest"]
            )
        )
    ):
        raise AuthoringError("Stage 10 asset projection drifted")

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
            isinstance(evidence, dict)
            and evidence.get("source_unit_id") in stage_unit_ids
            for evidence in candidate["source_evidence"]
        )
    }
    expected_candidates = (
        linked_from_reading | linked_from_assets | evidenced_in_stage
    )
    if enforce_frozen and (
        len(expected_candidates)
        != EXPECTED_POST_MERGE_SEMANTICS["stage_candidate_count"]
        or digest(sorted(expected_candidates))
        != EXPECTED_POST_MERGE_SEMANTICS["stage_candidate_ids_digest"]
    ):
        raise AuthoringError("Stage 10 candidate target drifted")
    unknown_or_inactive = {
        candidate_id
        for candidate_id in expected_candidates
        if candidate_id not in candidates_by_id
        or candidates_by_id[candidate_id].get("record_status") != "ACTIVE"
    }
    if unknown_or_inactive:
        raise AuthoringError(
            "Stage 10 reaches unknown or inactive candidates: "
            f"{sorted(unknown_or_inactive)}"
        )
    for row in stage_reading:
        unknown_routes = set(
            parse_links(row["route_ids"], f"{row['source_unit_id']}.route_ids")
        ) - routes_by_id.keys()
        if unknown_routes:
            raise AuthoringError(
                f"{row['source_unit_id']} reaches unknown routes: "
                f"{sorted(unknown_routes)}"
            )

    query_start = sum(len(record.get("queries", [])) for record in rounds) + 1
    hit_start = sum(len(record.get("hits", [])) for record in rounds) + 1
    if (
        query_start != EXPECTED_QUERY_START[round_id]
        or hit_start != EXPECTED_HIT_START[round_id]
    ):
        raise AuthoringError(
            f"{round_id} query/hit start drifted: "
            f"Q{query_start:04d}/H{hit_start:06d}"
        )
    queries = _query_objects(query_start)
    result_pairs, query_errors = validate_audit.execute_frozen_queries(
        queries,
        units,
        REPO_ROOT / "ref" / "A-New-Kind-of-Science",
    )
    if query_errors:
        raise AuthoringError("; ".join(query_errors))
    normalized_pairs = _normalized_result_pairs(result_pairs, query_start)
    if (
        len(result_pairs) != EXPECTED_RESULT_PAIR_COUNT
        or digest(normalized_pairs) != EXPECTED_NORMALIZED_RESULT_DIGEST
    ):
        raise AuthoringError("Stage 10 query result projection drifted")
    if any(
        unit_by_id[unit_id]["path"] not in STAGE_PATHS
        for _, unit_id in result_pairs
    ):
        raise AuthoringError("a query result escaped the paired Stage 10 scope")
    hit_counts = [
        sum(query_id == query["query_id"] for query_id, _ in result_pairs)
        for query in queries
    ]
    if hit_counts != EXPECTED_HIT_COUNTS:
        raise AuthoringError("Stage 10 query hit counts drifted")
    result_unit_ids = sorted({unit_id for _, unit_id in result_pairs})

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
    triage_digest = digest(triage_projection)
    if (
        enforce_frozen
        and triage_digest
        != EXPECTED_POST_MERGE_SEMANTICS["triage_digest"]
    ):
        raise AuthoringError("Stage 10 search triage projection drifted")

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
            "candidate-facing Stage 10 search differs from its target: "
            f"missing={sorted(expected_candidates - reached_candidates)} "
            f"unexpected={sorted(reached_candidates - expected_candidates)}"
        )
    candidate_coverage = _candidate_coverage_projection(
        expected_candidates=expected_candidates,
        candidates_by_id=candidates_by_id,
        reading_by_id=reading_by_id,
        normalized_pairs=normalized_pairs,
        stage_unit_ids=stage_unit_ids,
    )
    candidate_coverage_digest = digest(candidate_coverage)
    if (
        enforce_frozen
        and candidate_coverage_digest
        != EXPECTED_POST_MERGE_SEMANTICS["candidate_coverage_digest"]
    ):
        raise AuthoringError("Stage 10 candidate witness coverage drifted")

    omission_projection: list[tuple[Any, ...]] = []
    for ordinal, unit_id in normalized_pairs:
        if ordinal > 10:
            continue
        row = reading_by_id[unit_id]
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
    omission_digest = digest(omission_projection)
    if enforce_frozen and (
        len(omission_projection)
        != EXPECTED_POST_MERGE_SEMANTICS["omission_challenge_count"]
        or omission_digest
        != EXPECTED_POST_MERGE_SEMANTICS["omission_challenge_digest"]
    ):
        raise AuthoringError("Stage 10 F01-F10 omission challenge drifted")

    result_set = set(result_unit_ids)
    active_route_ids = {
        route_id
        for row in stage_reading
        for route_id in parse_links(
            row["route_ids"], f"{row['source_unit_id']}.route_ids"
        )
    }
    for candidate_id in expected_candidates:
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
        if route["owning_stage"] == str(STAGE) or target_units & stage_unit_ids:
            active_route_ids.add(route["route_id"])

    locator_result_units = {
        unit_id
        for ordinal, unit_id in normalized_pairs
        if ordinal == len(QUERY_SPECS)
    }
    stage_route_source_units = {
        routes_by_id[route_id]["source_unit_id"]
        for route_id in active_route_ids
        if routes_by_id[route_id]["source_unit_id"] in stage_unit_ids
    }
    missing_locator_sources = stage_route_source_units - locator_result_units
    if missing_locator_sources:
        raise AuthoringError(
            "F15 misses Stage 10 typed-route source units: "
            f"{sorted(missing_locator_sources)}"
        )

    candidate_route_witnesses: dict[str, set[str]] = {}
    for candidate_id in expected_candidates:
        witnesses = {
            unit_id
            for unit_id in result_set & stage_unit_ids
            if candidate_id
            in parse_links(
                reading_by_id[unit_id]["candidate_ids"],
                f"{unit_id}.candidate_ids",
            )
        }
        for route_id in candidates_by_id[candidate_id]["cross_reference_ids"]:
            candidate_route_witnesses.setdefault(route_id, set()).update(
                witnesses
            )
    route_coverage: list[tuple[str, list[str]]] = []
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
        witnesses.update(candidate_route_witnesses.get(route_id, set()))
        witnesses &= result_set
        if not witnesses:
            raise AuthoringError(
                f"{route_id} lacks an in-scope frozen-query witness"
            )
        route_coverage.append((route_id, sorted(witnesses)))
    route_coverage_digest = digest(route_coverage)
    if enforce_frozen and (
        len(route_coverage)
        != EXPECTED_POST_MERGE_SEMANTICS["route_coverage_count"]
        or route_coverage_digest
        != EXPECTED_POST_MERGE_SEMANTICS["route_coverage_digest"]
    ):
        raise AuthoringError("Stage 10 route witness coverage drifted")

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
            outcome = "governed candidate/support"
        elif row_route_ids:
            disposition = "CROSS_REFERENCE"
            outcome = "typed cross-reference"
        elif row["review_disposition"] in {
            "REPRESENTATION_OR_OBSERVER",
            "APPLICATION_OR_EMULATION",
            "SOURCE_DEFECT_OR_AMBIGUITY",
        }:
            disposition = "CONTROL_OR_RELATIONSHIP"
            outcome = "control/relationship"
        elif row["review_disposition"] in {
            "NO_CONSTRUCTION",
            "HISTORICAL_ONLY",
        }:
            disposition = "EXCLUSION"
            outcome = "exclusion"
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
                "rationale": _source_rationale(
                    row,
                    family_ordinal=family_ordinal,
                    outcome=outcome,
                ),
            }
        )
    disposition_counts: dict[str, int] = {}
    for hit in hits:
        disposition = hit["disposition"]
        disposition_counts[disposition] = (
            disposition_counts.get(disposition, 0) + 1
        )
    if (
        enforce_frozen
        and disposition_counts
        != EXPECTED_POST_MERGE_SEMANTICS["disposition_counts"]
    ):
        raise AuthoringError("Stage 10 hit dispositions drifted")

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
        "new_vocabulary": new_vocabulary,
        "new_candidates": [],
        "new_evidence_groups": [],
        "new_routes": [],
        "rerun_digest": "",
    }
    result_digest = validate_audit.search_result_digest(round_record)
    round_record["result_digest"] = result_digest
    round_record["rerun_digest"] = result_digest
    normalized_hit_projection = _normalized_hit_projection(round_record)
    normalized_hit_projection_digest = digest(normalized_hit_projection)
    if enforce_frozen and (
        normalized_hit_projection_digest
        != EXPECTED_POST_MERGE_SEMANTICS[
            "normalized_hit_projection_digest"
        ]
        or result_digest
        != EXPECTED_ROUND_GUARDS[round_id]["result_digest"]
    ):
        raise AuthoringError(f"{round_id} hit/result digest drifted")
    if round_id == "S016" and normalized_hit_projection != (
        _normalized_hit_projection(rounds[14])
    ):
        raise AuthoringError("S016 differs from the S015 zero-delta projection")

    semantic_projection = {
        "stage_reading_count": len(stage_reading),
        "stage_reading_digest": digest(stage_reading),
        "stage_asset_count": len(stage_assets),
        "stage_asset_digest": digest(stage_assets),
        "stage_candidate_count": len(expected_candidates),
        "stage_candidate_ids_digest": digest(sorted(expected_candidates)),
        "triage_digest": triage_digest,
        "candidate_coverage_digest": candidate_coverage_digest,
        "omission_challenge_count": len(omission_projection),
        "omission_challenge_digest": omission_digest,
        "route_coverage_count": len(route_coverage),
        "route_coverage_digest": route_coverage_digest,
        "disposition_counts": disposition_counts,
        "normalized_hit_projection_digest": normalized_hit_projection_digest,
    }
    round_guard = {
        "prior_event_sha256": history[-1]["event_sha256"],
        "base_artifact_sha256": base_digests,
        "result_digest": result_digest,
    }
    return (
        {
            "round_id": round_id,
            "search": search,
            "round_record": round_record,
            "base_digests": base_digests,
        },
        semantic_projection,
        round_guard,
    )


def _require_frozen_post_merge_guards(round_id: str) -> None:
    unresolved_semantics = [
        key
        for key, value in EXPECTED_POST_MERGE_SEMANTICS.items()
        if value is None
    ]
    unresolved_round = [
        key
        for key, value in EXPECTED_ROUND_GUARDS[round_id].items()
        if value is None
    ]
    if unresolved_semantics or unresolved_round:
        raise AuthoringError(
            "post-merge guards are intentionally unresolved; run "
            "--calibrate-post-merge after the required terminal transaction: "
            f"semantic={unresolved_semantics}, {round_id}={unresolved_round}"
        )


def build_proposal(goal_dir: Path) -> dict[str, Any]:
    goal_dir = goal_dir.resolve()
    if goal_dir != GOAL_DIR.resolve():
        raise AuthoringError("this reproducer is bound to canonical Goal 4")
    _assert_source_projection(_source_projection(goal_dir))
    search = json.loads(
        (goal_dir / merge_worker_output.SEARCH_NAME).read_text(
            encoding="utf-8"
        )
    )
    rounds = search.get("rounds")
    if not isinstance(rounds, list):
        raise AuthoringError("global search rounds are malformed")
    round_id = f"S{len(rounds) + 1:03d}"
    if round_id not in EXPECTED_ROUND_GUARDS:
        raise AuthoringError(f"unsupported Stage 10 round state {round_id}")
    _require_frozen_post_merge_guards(round_id)
    state, _, _ = _analyze_post_merge(goal_dir, enforce_frozen=True)
    proposed_search = deepcopy(state["search"])
    proposed_search["vocabulary"].extend(
        state["round_record"]["new_vocabulary"]
    )
    proposed_search["rounds"].append(state["round_record"])
    if (
        proposed_search["tool_assumptions"]
        != state["search"]["tool_assumptions"]
        or proposed_search.get("fixed_point") is not None
    ):
        raise AuthoringError("proposal changed global search semantics")
    return {
        "schema_version": 1,
        "proposal_kind": "SEARCH_APPEND",
        "coordinator_id": COORDINATOR_ID,
        "epoch": EPOCH,
        "source_paths": [],
        "base_artifact_sha256": state["base_digests"],
        "reading_updates": [],
        "asset_updates": [],
        "candidate_updates": [],
        "route_appends": [],
        "proposed_search": proposed_search,
    }


def main() -> int:
    if sys.argv[1:] == ["--self-check-source"]:
        try:
            projection = _source_projection(GOAL_DIR)
            if "__FILL_" not in json.dumps(
                {
                    "query": EXPECTED_QUERY_SPEC_DIGEST,
                    "vocabulary": EXPECTED_STAGE_VOCABULARY_DIGEST,
                    "units": EXPECTED_STAGE_UNIT_IDS_DIGEST,
                }
            ):
                _assert_source_projection(projection)
        except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
            print(f"Chapter 6 source self-check failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(projection, indent=2, sort_keys=True))
        return 0
    if sys.argv[1:] == ["--calibrate-post-merge"]:
        try:
            _assert_source_projection(_source_projection(GOAL_DIR))
            with audit_transaction.read_guard(GOAL_DIR):
                state, semantic, round_guard = _analyze_post_merge(
                    GOAL_DIR,
                    enforce_frozen=False,
                )
        except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
            print(
                f"Chapter 6 post-merge calibration failed: {exc}",
                file=sys.stderr,
            )
            return 1
        print(
            json.dumps(
                {
                    "round_id": state["round_id"],
                    "semantic": semantic,
                    "round_guard": round_guard,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if len(sys.argv) != 2:
        print(
            f"usage: {Path(sys.argv[0]).name} "
            "[--self-check-source|--calibrate-post-merge|OUTPUT_JSON]",
            file=sys.stderr,
        )
        return 2
    output_path = Path(sys.argv[1])
    try:
        with audit_transaction.read_guard(GOAL_DIR):
            proposal = build_proposal(GOAL_DIR)
            atomic_create(output_path, canonical_json_bytes(proposal))
    except (OSError, json.JSONDecodeError, AuthoringError, ValueError) as exc:
        print(f"Chapter 6 search authoring failed: {exc}", file=sys.stderr)
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
