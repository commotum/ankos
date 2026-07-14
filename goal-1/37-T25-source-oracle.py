#!/usr/bin/env python3
"""Frozen primary-source audit for T25 two-dimensional Turing machines.

This is an evidence oracle, not a Turing-machine implementation.  It closes
the Book's direct name, captions, Notes implementation, aliases, turning-rule
variant, historical routes, actual Index, split documents, Atlas, catalog, and
false-positive controls.  It preserves the Book's distinction between the
generic square-grid rule (head state need not be heading), restricted systems
whose state records heading, and the separate 2D-mobile-automaton construction.

The architectural conclusion is deliberately no stronger than the evidence:
T25 reuses the T12 finite-state/symbol head event while parameterizing its
fixed support and displacement set to two dimensions.  A transparent tagged
cell representation is lossless, but arbitrary CA rules, hidden interpreters,
random transition choice, path-only state, or a T25 executor are not inferred.
"""

from __future__ import annotations

import hashlib
import itertools
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T25 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"


# Q00--Q04 close direct names, dimensional generalization, captions, the
# executable Notes form, and fixed-versus-relative movement. Q05--Q09 close
# every named alias, person route, Langton-ant formula, worm/hex variant, and
# visualization/path vocabulary. Q10 guards the adjacent but distinct 2D
# mobile-automaton construction. Q11--Q15 independently recover inherited
# Turing semantics: unique stateful head, self-only read, complete atomic
# transition, blank/default support, rule cardinality, and lossless tagged-cell
# representation. Q16--Q20 deliberately broaden worm, turtle, turning, hex-grid,
# and two-dimensional-grid vocabulary to expose false positives. Q21--Q24
# close dense actual-Index entry routes, aliases, Logo/robotics history, and the
# TMs redirect. Q25 closes all Turing section headings; Q26 closes experiment
# randomness and repeated-position language without treating either as a
# stochastic rule. Q27 independently closes the fixed-grid fact inherited from
# the Chapter 3 construction. Q28 freezes absent spelling variants. Q29 closes
# the remaining ant, lattice, and randomness routes found by a page-route sweep
# of the actual Index rather than by name-only lookup.
QUERIES = {
    "Q00": r"\btwo-dimensional Turing machines?\b|\b2D Turing machines?\b",
    "Q01": (
        r"\bgeneralize Turing machines to two dimensions\b|"
        r"\bgeneralizes Turing machines to move in two dimensions\b|"
        r"\bhead of the Turing machine to move around on a two-dimensional grid\b|"
        r"\bbackwards and forwards on a one-dimensional tape\b"
    ),
    "Q02": (
        r"\bfour possible directions the head should move\b|"
        r"\borientation of the arrow representing the state of the head has no direct relationship\b|"
        r"\bhead often visits the same position on the grid\b"
    ),
    "Q03": (
        r"\bTM2DStep\b|"
        r"\{dx, dy\}|"
        r"r : \{x\_, y\_\}|"
        r"tape\[\[x, y\]\]"
    ),
    "Q04": (
        r"\bRules based on turning\b|"
        r"\bfixed directions in the underlying grid\b|"
        r"\bturns to make at each step in the motion of the head\b|"
        r"\bturtles in the Logo computer language are set up\b"
    ),
    "Q05": (
        r"\bprehistoric worm\b|\bpossible worms\b|\bPaterson worms?\b|"
        r"\bvants?\b|\bturmites?\b|\bturning machines?\b|"
        r"\bLangton's ant\b|\bmobile turtles?\b"
    ),
    "Q06": (
        r"\bMichael Paterson (?:and John Conway|considers a class of simple 2D Turing machines)\b|"
        r"\bMichael Beeler[^.]{0,100}\b1296 possible worms\b|"
        r"\bChristopher Langton[^.]{0,100}\bvants\b|"
        r"\bRudy Rucker[^.]{0,100}\bturmites\b|"
        r"\bAllen Brady[^.]{0,100}\bturning machines\b"
    ),
    "Q07": (
        r"sp = s \(2c - 1\)i|"
        r"\{sp, 1 - c, \{Re\[sp\], Im\[sp\]\}\}|"
        r"\bspecific 4-state rule\b"
    ),
    "Q08": (
        r"\b1296 possible worms\b|"
        r"\bstate of the head records the direction of the motion taken at each step\b|"
        r"\bworms with rules of the simplest type on a hexagonal grid\b"
    ),
    "Q09": (
        r"\b2D position of the head at 500 successive steps\b|"
        r"\bpath traced out by the head of the two-dimensional Turing machine\b|"
        r"\bseemingly random fluctuations in this path\b"
    ),
    "Q10": (
        r"\b2D mobile automata\b|"
        r"\bMobile automata can be generalized just like Turing machines\b|"
        r"\$\(4k\)\^k\$ possible rules|"
        r"nearly\s+\$10\^\{29\}\$\s+even for k = 2"
    ),
    "Q11": (
        r"\bline of cells, known as the \"tape\"\b|"
        r"\bsingle active cell, known as the \"head\"\b|"
        r"\brule for a Turing machine can depend on the state of the head\b|"
        r"\bnot on the colors of any neighboring cells\b"
    ),
    "Q12": (
        r"\bstate of a Turing machine at a particular step can be represented by the triple\b|"
        r"\bleft-hand side in each case gives the state of the head\b|"
        r"\bnew state of the head, the new value of the cell under the head and the displacement\b|"
        r"\bTMStep\b|\bTMEvolveList\b"
    ),
    "Q13": (
        r"\bresult of \*t\* steps of evolution from a blank tape\b|"
        r"s = 1; a\[_\] = 0; n = 0|"
        r"\bactive cell must start at a definite location\b|"
        r"\ball cells are initially white\b"
    ),
    "Q14": (
        r"\blighter colors in the cellular automaton represent ordinary cells in the Turing machine\b|"
        r"\bdarker colors represent the cell under the head\b|"
        r"\bcellular automaton which emulates it can be constructed\b|"
        r"\bcellular automaton has k\(s\+1\) colors\b|"
        r"\bemulate each step in the evolution of a mobile automaton or a Turing machine with a single step\b"
    ),
    "Q15": (
        r"\bWith k possible colors for each cell and s possible states\b|"
        r"\$\(2sk\)\^\{sk\}\$|"
        r"\btotal of 4096 rules of this kind\b"
    ),
    "Q16": r"\bworms?\b",
    "Q17": r"\bturtles?\b",
    "Q18": r"\bturning\b",
    "Q19": r"\bhexagonal grid\b",
    "Q20": r"\btwo-dimensional grid\b",
    "Q21": (
        r"\bBeeler, Michael.*?and 2D Turing machines, 930\b|"
        r"\bBrady, Allen.*?and 2D Turing machines, 930\b|"
        r"\bConway, John.*?and 2D Turing machines, 930\b|"
        r"\bLangton, Christopher.*?and 2D Turing machines, 930\b|"
        r"\bPaterson, Michael.*?and 2D Turing machines, 880, 930\b|"
        r"\bRucker, Rudy.*?and 2D Turing machines, 930\b"
    ),
    "Q22": (
        r"\bTuring machines, 78-81 2D 184-186\b|"
        r"\bhistory of 2D, 930\b|\bimplementation of 2D, 930\b|"
        r"\bpaths in 3D from 2D, 931\b|"
        r"\bTurmites \(2D Turing machines\), 930\b|"
        r"\bTurning machines \(2D Turing machines\), 930\b|"
        r"\bTurtles \(artificial\) and 2D Turing machines, 930\b|"
        r"\bVants \(2D Turing machines\), 930\b|"
        r"\bTwo-dimensional cellular automata[^.]{0,240}\bTuring machines, 184.186\b"
    ),
    "Q23": (
        r"\bLogo \(computer language\) and 2D TMs, 930, 931\b|"
        r"\bRobotics[^.]{0,100}\bmobile turtles 930\b|"
        r"\bMIT[^.]{0,140}\bPaterson worms, 930\b|"
        r"\bWorm[^.]{0,100}\bPaterson's, 930\b"
    ),
    "Q24": r"\bTMs, see Turing machines\b",
    "Q25": r"^#### \*\*Turing Machines\*\*$",
    "Q26": (
        r"\bmillion randomly chosen rules\b|"
        r"\belements of randomness at some steps\b|"
        r"\bhead often visits the same position on the grid many times\b"
    ),
    "Q27": (
        r"\bcellular automata, mobile automata and Turing machines all have in common\b|"
        r"\bunderlying number and organization of cells always stays the same\b"
    ),
    "Q28": (
        r"\btwo dimensional Turing machines?\b|"
        r"\b2-dimensional Turing machines?\b|"
        r"\b2-D Turing machines?\b|"
        r"\bTuring machines? in two dimensions\b"
    ),
    "Q29": (
        r"\bAnts, artificial, 931\b|"
        r"\bTuring machines on, 930\b|"
        r"\bin Turing machines in 2D, 184\b|"
        r"\bTMs on, 184\b"
    ),
}


def line_set(spec: str) -> frozenset[int]:
    """Parse comma-separated line numbers and inclusive ranges."""
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Each tuple is (all physical lines, pre-Index lines, actual-Index lines,
# line-set digest). These values freeze the complete reproducible protocol.
EXPECTED_QUERY = {
    "Q00": (15, 7, 8, "85928fb476231db85e8fae575c8759d0d839b9870e887775c5552fce717e6d22"),
    "Q01": (1, 1, 0, "e5481aa7df58a36f4d0a1fb99cb56e3cf20e1ea96329e414c81d0ce7ad2c1bfc"),
    "Q02": (2, 2, 0, "6873df9115fb08f76e58897cf04b396f0fab326a50e2307826bccbb1a959c03f"),
    "Q03": (1, 1, 0, "b0d590b1856a5932562a182ddba086ba705a26a6813eaac67a8529cd1994ed1d"),
    "Q04": (1, 1, 0, "91b8107ca1d9412220d158442772f7ab53d3a648edf5368642363de43b9896d4"),
    "Q05": (8, 2, 6, "94b29e0f5e4e8e7b443cf506b95a8d2c3b23003006439cd6ee29faa2876da64b"),
    "Q06": (2, 2, 0, "73666a72eee27b6d8fa8a63c0f7670ca0d2501d65ec554b245560dcad826b9b5"),
    "Q07": (2, 2, 0, "9f207cb008ead43ffbfd042820751b865446daf1986f08712aeed1c1179368f9"),
    "Q08": (1, 1, 0, "dce1a79f6d2e8530d871495b38cb219277141dd8685661e25254c28f2b02f6f5"),
    "Q09": (2, 2, 0, "1b47323493327539c8c6cb63c4f2fc33953304153d9b6ea28cba98e76331050a"),
    "Q10": (2, 2, 0, "dcba1568e6e6fd926e94c7954d3832b4ba9110373f1c574002286be3f56af129"),
    "Q11": (1, 1, 0, "68e1e435db6ab43fd38ae5df6c6a03b50a5c9c6290f4691e1b670a786c0ebe12"),
    "Q12": (5, 5, 0, "665ba2fa608c32fa95f4916ad41b0e1ba5269a973dbaeaa73ea2bf259dd15dfa"),
    "Q13": (4, 4, 0, "2c9466e2d348ff8b82821ba208b3e31f7eceda10da9a3b7855126c086f965b71"),
    "Q14": (5, 5, 0, "f4c88c3f01bf0d06dee6cf3f7581803c8cf46a94421e36fc300cfff554939b91"),
    "Q15": (2, 2, 0, "a71b8a7138378f80a86d813fbf25198ae17e2192db54495f726a856ab2f5688d"),
    "Q16": (7, 4, 3, "9edd32a308bad5ff4e025ef3f0b7f28f887de8311bae7e654a7b76f03bd1bd07"),
    "Q17": (4, 2, 2, "a3953178f88d931f2f5386b4394324ab4c3d6e3507ac44783b6bfc2f1f29e799"),
    "Q18": (8, 5, 3, "26a4019877d27744b764b9e4222baa97e2cc0d4090f6ce7414b12a7edf2ee79b"),
    "Q19": (6, 6, 0, "3fa0afa370940f10ed94b10577eec4a046ecbf317ee579a46a0017f2b2e4aeb4"),
    "Q20": (4, 4, 0, "e55847563ab52d066668140948e6f5edba1d05e4b0e7f6d98ac4b7930ce58669"),
    "Q21": (6, 0, 6, "22432869124663b0ff4c53130dd4c6d803e5580dd3e147ef32d4835066ecf967"),
    "Q22": (4, 0, 4, "931f35533dd2e7db782551c3d06378920bbef8c50790a6457dc0cd4e4762d5bf"),
    "Q23": (4, 0, 4, "bfd2983a29cd872a59598d73a88dddd616a8fc8eae3dc0cd23a78e2774879841"),
    "Q24": (1, 0, 1, "e7c46013c81f7709dcba473bd51901ba3f2f54eac6810b7295f77f626bc41b6f"),
    "Q25": (4, 4, 0, "11eac1eed640d74e413e32a1a8eda74deae28a4258a14a161d4c303efaed730c"),
    "Q26": (3, 3, 0, "dc3e443df30429a659ad0bc09a71b1c3151aaca0632872ff81824ca2f560d892"),
    "Q27": (1, 1, 0, "dff17949eb4f9ecd9361bb97c38a9404f3d034565e5d4395f073c0c367b5ea0b"),
    "Q28": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q29": (4, 0, 4, "08760b879c5806754dfc4f5ac4319803327d7365b840a677012d2966e611341e"),
}


# Every broad-query collision stays visible.  No line is silently discarded.
EXCLUDED_CLASS = {
    "unrelated_worms": line_set("4966,20480"),
    "unrelated_turning": line_set("5036,15324,17045"),
    "other_hexagonal_grid_systems": line_set("4422,4430,4440,15708,15865"),
    "other_two_dimensional_grid_systems": line_set("2364,5634"),
    "other_emulation_construction": line_set("18352"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# Native evidence is the construction itself or an inherited Turing primitive:
# one stateful head, self-only table input, typed write/state/displacement
# result, fixed support, blank/default realization, and the explicit square-
# grid/turning/hex variants.  Images are included only when they are direct
# construction/rule/evolution evidence for the dependent asset audit.
NATIVE_EVIDENCE = line_set(
    "940,942,948,982,"
    "12014,12016,12018,12020,12023,12026,12034,12037,12039,12042,"
    "14275,"
    "2266,2268,2270,2280,2284,2286,2290,2292,2294,"
    "13662,13664,13666,13668,13670,13678"
)

# Relations are historical routes, observers, behavior summaries, generic
# dimensional context, equivalent transparent representations, and path views.
RELATION_EVIDENCE = line_set(
    "936,956,2152,2156,2264,2272,2274,2276,2306,"
    "2298,2302,"
    "7938,7942,7944,7946,7948,11566,12012,12028,12031,"
    "13660,13672,13674,"
    "18363,18366-18369,18372"
)

# Controls prevent nearby language from becoming invented semantics: random
# rule sampling and observed randomness are not stochastic UPDATE; a missing
# printed 3-state formula is not reconstructed; the malformed 2D-mobile
# exponent is repaired only from its five-cell input and same-line magnitude;
# 2D mobile automata are a different read rule; and CA emulation is not the
# native compact program.
CONTROL_EVIDENCE = line_set(
    "2278,13676,13679,16400"
)

RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("2268,2280,2284,2286,2290,2292")
RELATION_IMAGE_LINES = line_set("2298,2302,7942,7944,7946,13674")
CONTROL_IMAGE_LINES = line_set("")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)


# Actual Index supplies routes, never construction mechanics. Dense physical
# rows are classified by the exact T25 entry guarded below.
INDEX_CLASS = {
    "ant_lattice_behavior_routes": line_set("20868,21243,21899,22136"),
    "named_people_routes": line_set("20910,20940,21050,21432,21761,21990"),
    "logo_robotics_worm_routes": line_set("21475,21521,21970,22434"),
    "turing_entry_and_alias_routes": line_set("22346,22362,22378,22380,22394"),
    "broad_turning_collision_routes": line_set("20946,22352"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())

INDEX_ENTRY_GUARDS = {
    "ant_lattice_behavior_routes": {
        20868: ("ants, artificial, 931",),
        21243: ("hexagonal lattice", "turing machines on, 930"),
        21899: ("randomness", "in turing machines in 2d, 184"),
        22136: ("square lattices", "tms on, 184"),
    },
    "named_people_routes": {
        20910: ("beeler, michael", "and 2d turing machines, 930"),
        20940: ("brady, allen", "and 2d turing machines, 930"),
        21050: ("conway, john", "and 2d turing machines, 930"),
        21432: ("langton, christopher", "langton's ant (2d turing machine), 931"),
        21761: ("paterson, michael", "and 2d turing machines, 880, 930"),
        21990: ("rucker, rudy", "and 2d turing machines, 930"),
    },
    "logo_robotics_worm_routes": {
        21475: ("logo (computer language) and 2d tms, 930, 931",),
        21521: ("mit", "and paterson worms, 930"),
        21970: ("robotics", "and mobile turtles 930"),
        22434: ("worm", "paterson's, 930"),
    },
    "turing_entry_and_alias_routes": {
        22346: ("tms, see turing machines",),
        22362: ("turing machines, 78-81 2d 184-186",),
        22378: (
            "history of 2d, 930", "implementation of 2d, 930",
            "paths in 3d from 2d, 931", "turmites (2d turing machines), 930",
            "turning machines (2d turing machines), 930",
            "turtles (artificial) and 2d turing machines, 930",
        ),
        22380: ("two-dimensional cellular automata", "turing machines, 184–186"),
        22394: ("vants (2d turing machines), 930",),
    },
    "broad_turning_collision_routes": {
        20946: ("turning tracks of",),
        22352: ("tracks made by turning vehicles",),
    },
}


EXPECTED_SET = {
    "union": (71, "99d8130e0bdc5676ab50b37967752a2502f8d24ffcb692921fa8a0ba217272db"),
    "pre_index_union": (50, "f1e2fc20a63767458eb989b20bd3d63ee92b8e5b3e59cac69d4eea2285e3f09e"),
    "index": (21, "bf42af3b8e92eea8299221bec0005318851f85b5364f3e7f1848e6cc042dc6ac"),
    "matched_retained": (37, "134fd3b39d4bc29efbcc40d67529e252610e4cc29d7de29b13c0a62804b8ecc5"),
    "governed_continuations": (26, "c460bf9f54da12cfa085b564509d6413296177395327094c6d0f61057c5b9963"),
    "retained": (63, "d65c11e7f57b120a83e9c37cd0d789ee591312f9a1316b41fae7c9ee194010b4"),
    "excluded": (13, "2653a26f21f1f90e6106650d78acfbb7d64416acdae85795b41862ca15224971"),
    "native": (30, "c7f09f0a15878ddf9078e96baface0169302db3ada59bc76e8f723a2ca86a848"),
    "relation": (29, "8339d80f08310f0c2b3dd75cf415730ab80e55d6735510a0438deec8852f04fe"),
    "control": (4, "8015743896a86aef3b04d12c93279f51c5f8eae5baf9fc7ed93545f6a16f268b"),
    "governed_images": (12, "259a790e9c6451ab832d1a2e4296ed587311377fdd9e5b9f7737dff6d2de8836"),
}
EXPECTED_EXCLUDED_CLASS = {
    "unrelated_worms": (2, "c7263fd0d9d6f37673504814865ee8754faa349ac193057849cca0d0c740cac4"),
    "unrelated_turning": (3, "65def06fa09ec4e0abb9ac607a04496b255195a321e99eaa4de6875b3cb47bd6"),
    "other_hexagonal_grid_systems": (5, "7cb22225cca27f8fc9c313133cceae5c2c220adcdd80548e33cf25491e20c919"),
    "other_two_dimensional_grid_systems": (2, "3ca52e85fd5c25b2d989821ec79d9a5c5684b93d6ec93e5a396e0321f4e69278"),
    "other_emulation_construction": (1, "c4af1ccb5cb4559b05dea6639f91383a49c9d833c8caf3efae462c460818807e"),
}
EXPECTED_INDEX_CLASS = {
    "ant_lattice_behavior_routes": (4, "08760b879c5806754dfc4f5ac4319803327d7365b840a677012d2966e611341e"),
    "named_people_routes": (6, "22432869124663b0ff4c53130dd4c6d803e5580dd3e147ef32d4835066ecf967"),
    "logo_robotics_worm_routes": (4, "bfd2983a29cd872a59598d73a88dddd616a8fc8eae3dc0cd23a78e2774879841"),
    "turing_entry_and_alias_routes": (5, "c40215af304020f024f40f59cb22c6f5e5cb3c11af4343287380d08e08d19613"),
    "broad_turning_collision_routes": (2, "f46ced44e475e9f1681169c6860a9dc704067b49c3f2ba0c8ec4bdee0b252cdb"),
}
EXPECTED_INDEX_ENTRY_GUARDS = (
    21, "138764607b770b97b5c563ad4ecbe66eee19eb7b797ddd3964693e2d826f86ec"
)
EXPECTED_IMAGE_PARTITION = {
    "native": (6, "6cb059a1eaf065c9f6fdceff4dd39db0adab35db77584c819004ad49cfd99617"),
    "relation": (6, "143311c5f560e6b63d56cc7a3074518658e161c471db549f93a9a3fd4b7881d0"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY = (70, "3a83b3a73fd044a815eb6c4ac8ae6e51e8c7e5ac8811c628564458c900f7224c")
EXPECTED_SPLIT_QUERY_EXACT = (63, "479099e9e653bc0fdcd78fbed4cb02b032f121f455870480dd20e20603544802")
EXPECTED_SPLIT_QUERY_NONEXACT = (7, "1b13fcf4341f6d2dce59b5b8835d9116bf064e26994c69d834ccd819ad479fa3")
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = "48d46002d3bcdcf0bc560b0c4bfa24d0b4aada1fc74f5987e3e56c5d9e088b71"
EXPECTED_SPLIT_RETAINED_EXACT = (47, "95141e5dce2c995de51a95f4d6060c61afeb486a2c6ddc95e617e3dd7c772e42")
EXPECTED_SPLIT_RETAINED_NONEXACT = (16, "f7d6e79fa049bdae71529b5062f0ce82cf3400386f1903c4d111aa906c313d8a")
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = "b61d0ee6bc8c7ef2a24fab5227cb1adab81befb2b8ec89a01d2e2f7a4de2e87e"
EXPECTED_MONOLITH_ONLY = (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
EXPECTED_ATLAS_HITS = (1, "3068430da9e4b7a674184035643d9e19af3dc7483e31cc03b35f75268401df77")


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def best_witness(canonical: str, candidates: list[tuple[str, str]]) -> tuple[str, float]:
    canonical_tokens = set(normalized_line(canonical).split())
    scored: list[tuple[float, str]] = []
    for record, normalized in candidates:
        candidate_tokens = set(normalized.split())
        denominator = min(len(canonical_tokens), len(candidate_tokens))
        score = len(canonical_tokens & candidate_tokens) / denominator if denominator else 0.0
        scored.append((score, record))
    score, record = max(scored, key=lambda item: (item[0], item[1]))
    return record, score


STRICT_MOVE_PORTS = ("move0", "move1", "move2", "move3")


def declared_cardinal_realization() -> tuple[tuple[int, int], ...]:
    """A conventional coordinate witness, not a source-recovered port map."""
    return ((-1, 0), (0, -1), (0, 1), (1, 0))


def langton_unit_moves() -> tuple[tuple[int, int], ...]:
    """The exact four displacements generated by the Notes' complex formula."""
    return ((-1, 0), (0, -1), (0, 1), (1, 0))


def tagged_step(
    cells: dict[tuple[int, int], tuple[str, int, int] | tuple[str, int]],
    table: dict[tuple[int, int], tuple[int, int, tuple[int, int]]],
    blank: int = 0,
) -> dict[tuple[int, int], tuple[str, int, int] | tuple[str, int]]:
    """Transparent lowering under the declared cardinal coordinate witness."""
    heads = [
        (position, value) for position, value in cells.items()
        if value[0] == "head"
    ]
    assert len(heads) == 1
    source, (_, state, symbol) = heads[0]
    next_state, write, move = table[(state, symbol)]
    assert move in declared_cardinal_realization()
    destination = (source[0] + move[0], source[1] + move[1])
    destination_old = cells.get(destination, ("plain", blank))
    assert destination_old[0] == "plain"
    result = dict(cells)
    result[source] = ("plain", write)
    result[destination] = ("head", next_state, destination_old[1])
    return result


def langton_transition(state: complex, color: int) -> tuple[complex, int, tuple[int, int]]:
    """Exact Notes formula, evaluated over the four unit complex headings."""
    assert state in (1, 1j, -1, -1j) and color in (0, 1)
    next_state = state * (2 * color - 1) * 1j
    move = (int(next_state.real), int(next_state.imag))
    return next_state, 1 - color, move


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 37-T25-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda line_no: lines[line_no - 1]

    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        found = {n for n, line in enumerate(lines, 1) if re.search(pattern, line, re.I)}
        hits[name] = found
        actual = (
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index_union = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index_union
    matched_retained = pre_index_union - set(EXCLUDED)
    governed = set(RETAINED) - union
    sets = {
        "union": union,
        "pre_index_union": pre_index_union,
        "index": index,
        "matched_retained": matched_retained,
        "governed_continuations": governed,
        "retained": set(RETAINED),
        "excluded": set(EXCLUDED),
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
        "governed_images": set(GOVERNED_IMAGE_LINES),
    }
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    excluded_ok = (
        set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    classification_delta = matched_retained ^ (set(RETAINED) & pre_index_union)
    excluded_ok &= not classification_delta
    ok &= excluded_ok
    print(
        "unresolved_pre_index", "OK" if excluded_ok else "MISMATCH",
        len(classification_delta), *sorted(classification_delta),
    )

    index_ok = (
        set().union(*INDEX_CLASS.values()) == index
        and sum(map(len, INDEX_CLASS.values())) == len(index)
    )
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        print(f"index_{name}", "OK" if good else "MISMATCH", *actual)
    guard_records = {
        f"{class_name}:{line_no}:{'|'.join(needles)}"
        for class_name, entries in INDEX_ENTRY_GUARDS.items()
        for line_no, needles in entries.items()
    }
    index_entry_guards_ok = (
        set(INDEX_ENTRY_GUARDS) == set(INDEX_CLASS)
        and all(
            set(INDEX_ENTRY_GUARDS[class_name]) == set(INDEX_CLASS[class_name])
            for class_name in INDEX_CLASS
        )
        and all(
            all(needle in at(line_no).lower() for needle in needles)
            for entries in INDEX_ENTRY_GUARDS.values()
            for line_no, needles in entries.items()
        )
        and (len(guard_records), digest_records(guard_records))
        == EXPECTED_INDEX_ENTRY_GUARDS
    )
    index_ok &= index_entry_guards_ok
    print(
        "index_entry_occurrence_guards",
        "OK" if index_entry_guards_ok else "MISMATCH",
        len(guard_records), digest_records(guard_records),
    )
    ok &= index_ok
    print("unresolved_index", "OK" if index_ok else "MISMATCH", len(index ^ set(INDEX_ROUTED)))

    derived_images = {n for n in RETAINED if IMAGE_RE.fullmatch(at(n))}
    image_sets = {
        "native": NATIVE_IMAGE_LINES,
        "relation": RELATION_IMAGE_LINES,
        "control": CONTROL_IMAGE_LINES,
    }
    images_ok = (
        derived_images == set(GOVERNED_IMAGE_LINES)
        and sum(map(len, image_sets.values())) == len(GOVERNED_IMAGE_LINES)
        and NATIVE_IMAGE_LINES <= NATIVE_EVIDENCE
        and RELATION_IMAGE_LINES <= RELATION_EVIDENCE
        and CONTROL_IMAGE_LINES <= CONTROL_EVIDENCE
        and all(IMAGE_RE.fullmatch(at(n)) for n in GOVERNED_IMAGE_LINES)
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION.get(name)
        images_ok &= good
        print(f"images_{name}", "OK" if good else "MISMATCH", *actual)
    ok &= images_ok
    print(
        "governed_image_interface", "OK" if images_ok else "MISMATCH",
        len(derived_images), digest(derived_images),
    )

    # Exact source wording and executable shape. No textbook-default boundary,
    # direction/state coupling, random rule choice, or missing formula is added.
    source_facts_ok = (
        "line of cells, known as the \"tape\"" in at(940)
        and "single active cell, known as the \"head\"" in at(940)
        and "state of the head" in at(942)
        and "color of the cell at the position of the head" in at(942)
        and "not on the colors of any neighboring cells" in at(942)
        and "fixed array of cells" in at(982)
        and "underlying number and organization of cells always stays the same" in at(982)
        and "generalize Turing machines to two dimensions" in at(2266)
        and "move around on a two-dimensional grid" in at(2266)
        and "four possible directions" in at(2270)
        and "no direct relationship to directions on the grid" in at(2270)
        and "all cells are initially white" in at(2294)
        and "head often visits the same position" in at(2294)
        and "\\{s, a\\} \\rightarrow \\{sp, ap, \\{dx, dy\\}\\}" in at(13662)
        and "TM2DStep" in at(13664)
        and "ReplacePart[tape, #2, {r}]" in at(13664)
        and "{s, tape[[x, y]]}/. rule" in at(13664)
    )
    ok &= source_facts_ok
    print("source_core_t25_mechanics", "OK" if source_facts_ok else "MISMATCH")

    inherited_turing_ok = (
        "state of a Turing machine at a particular step" in at(12014)
        and "state of the head" in at(12018)
        and "value of the cell under the head" in at(12018)
        and "new state of the head" in at(12018)
        and "new value of the cell under the head" in at(12018)
        and "displacement of the head" in at(12018)
        and "TMStep" in at(12023)
        and "ReplacePart" in at(12023)
        and "TMEvolveList" in at(12026)
        and "blank tape" in at(12034)
        and "a[_] = 0" in at(12037)
        and "n += d" in at(12039)
        and "$(2sk)^{sk}$" in at(12042)
        and "active cell must start at a definite location" in at(14275)
    )
    ok &= inherited_turing_ok
    print("source_inherited_t12_state_read_write_move", "OK" if inherited_turing_ok else "MISMATCH")

    tagged_representation_ok = (
        "lighter colors" in at(7938)
        and "ordinary cells in the Turing machine" in at(7938)
        and "darker colors represent the cell under the head" in at(7938)
        and "specific darker color corresponding to each possible state of the head" in at(7938)
        and "each step in the evolution of a mobile automaton or a Turing machine"
        in at(7948)
        and "with a single step of cellular automaton evolution" in at(7948)
        and "cellular automaton which emulates it" in at(18363)
        and "k(s+1) colors" in at(18372)
        and "single cell of color k" in at(18372)
        and "blank tape" in at(18372)
    )
    ok &= tagged_representation_ok
    print("source_lossless_tagged_cell_route", "OK" if tagged_representation_ok else "MISMATCH")

    variants_ok = (
        "state of the head records the direction" in at(13666)
        and "1296 possible worms" in at(13666)
        and "hexagonal grid" in at(13666)
        and "vants" in at(13666)
        and "turmites" in at(13666)
        and "turning machines" in at(13666)
        and "sp = s (2c - 1)i" in at(13668)
        and "sp, 1 - c" in at(13668)
        and "Re[sp], Im[sp]" in at(13668)
        and "Langton's ant" in at(13670)
        and "fixed directions in the underlying grid" in at(13678)
        and "turns to make at each step" in at(13678)
    )
    ok &= variants_ok
    print("source_alias_turning_hex_variants", "OK" if variants_ok else "MISMATCH")

    # The corpus gives the count and qualitative restriction, but no worm
    # transition schema from which 1296 could honestly be reverse-engineered.
    # The subsequent printed formula is explicitly the separate Langton rule.
    hex_worm_source_limit_ok = (
        "1296 possible worms with rules of the simplest type on a hexagonal grid"
        in at(13666)
        and at(13667) == ""
        and "sp = s (2c - 1)i" in at(13668)
        and "Langton's ant" in at(13670)
    )
    ok &= hex_worm_source_limit_ok
    print(
        "hex_worm_count_retained_without_invented_schema",
        "OK" if hex_worm_source_limit_ok else "MISMATCH", 1296,
    )

    mobile_2d_binary_count = (4 * 2) ** (2**5)
    experiment_controls_ok = (
        "million randomly chosen rules" in at(2278)
        and "one of the rules" in at(2294)
        and "elements of randomness at some steps" in at(13676)
        and at(13677) == ""
        and at(13678).startswith("- Rules based on turning.")
        and "2D mobile automata" in at(13679)
        and "$(4k)^k$" in at(13679)
        and "$10^{29}$" in at(13679)
        and mobile_2d_binary_count == 8**32
        and 10**28 < mobile_2d_binary_count < 10**29
    )
    ok &= experiment_controls_ok
    print(
        "random_ensemble_and_mobile_ocr_control",
        "OK" if experiment_controls_ok else "MISMATCH", mobile_2d_binary_count,
    )

    # Conditional rule-space count: inherited Q x Sigma input and typed output
    # gain the four source-stated movement choices.  Arity, not the conventional
    # coordinate realization used by the lowering witness, drives this count.
    square_rule_count_ok = all(
        (4 * states * colors) ** (states * colors) > 0
        and len(STRICT_MOVE_PORTS) == 4
        for states in range(1, 6)
        for colors in range(1, 5)
    )
    square_4_state_binary_count = (4 * 4 * 2) ** (4 * 2)
    square_rule_count_ok &= square_4_state_binary_count == 32**8
    ok &= square_rule_count_ok
    print(
        "derived_square_grid_total_table_count",
        "OK" if square_rule_count_ok else "MISMATCH",
        square_4_state_binary_count,
    )

    langton_rows = {
        (state, color): langton_transition(state, color)
        for state, color in itertools.product((1, 1j, -1, -1j), (0, 1))
    }
    langton_ok = (
        len(langton_rows) == 8
        and all(row[0] in (1, 1j, -1, -1j) for row in langton_rows.values())
        and all(row[1] == 1 - color for (_, color), row in langton_rows.items())
        and {row[2] for row in langton_rows.values()} == set(langton_unit_moves())
        and all(
            row[2] == (int(row[0].real), int(row[0].imag))
            for row in langton_rows.values()
        )
    )
    ok &= langton_ok
    print("derived_langton_closed_absolute_table", "OK" if langton_ok else "MISMATCH", len(langton_rows))

    sample_table = {
        (0, 0): (1, 1, (1, 0)),
        (0, 1): (0, 0, (0, 1)),
        (1, 0): (0, 1, (-1, 0)),
        (1, 1): (1, 0, (0, -1)),
    }
    initial = {
        (0, 0): ("head", 0, 0),
        (1, 0): ("plain", 1),
    }
    next_cells = tagged_step(initial, sample_table)
    atomic_lowering_ok = (
        next_cells[(0, 0)] == ("plain", 1)
        and next_cells[(1, 0)] == ("head", 1, 1)
        and sum(value[0] == "head" for value in next_cells.values()) == 1
    )
    ok &= atomic_lowering_ok
    print("derived_transparent_atomic_head_move", "OK" if atomic_lowering_ok else "MISMATCH")

    structural = (
        not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE == RETAINED
        and not RETAINED & index
        and matched_retained == set(RETAINED) & pre_index_union
        and governed == set(RETAINED) - union
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    # Close all split Markdown copies with immutable manifests, complete query
    # enumeration, and deterministic reverse joins to the canonical monolith.
    split_paths = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() not in {DEFAULT_BOOK.resolve(), ATLAS.resolve()}
    )
    relative_paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in split_paths]
    manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    split_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    ok &= split_manifest_ok
    print(
        "split_manifest", "OK" if split_manifest_ok else "MISMATCH",
        len(split_paths), digest_records(relative_paths), digest_records(manifest),
    )

    compiled = [re.compile(pattern, re.I) for pattern in QUERIES.values()]
    monolith_query_text = {at(n) for n in union}
    split_records: set[str] = set()
    split_exact: set[str] = set()
    split_nonexact: set[str] = set()
    split_lines: list[tuple[str, str]] = []
    split_texts: set[str] = set()
    split_record_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            record = f"{relative}:{line_no}"
            split_lines.append((record, normalized_line(line)))
            split_texts.add(line)
            split_record_text[record] = line
            if not any(rx.search(line) for rx in compiled):
                continue
            split_records.add(record)
            (split_exact if line in monolith_query_text else split_nonexact).add(record)

    query_mapping: set[str] = set()
    query_mapping_ok = True
    monolith_witnesses = [
        (str(line_no), normalized_line(at(line_no))) for line_no in sorted(union)
    ]
    for record in sorted(split_nonexact):
        witness, score = best_witness(split_record_text[record], monolith_witnesses)
        query_mapping.add(f"{record}->{witness}:{score:.6f}")
        query_mapping_ok &= score >= 0.50 and int(witness) in union
    split_query_ok = (
        (len(split_records), digest_records(split_records)) == EXPECTED_SPLIT_QUERY
        and (len(split_exact), digest_records(split_exact)) == EXPECTED_SPLIT_QUERY_EXACT
        and (len(split_nonexact), digest_records(split_nonexact)) == EXPECTED_SPLIT_QUERY_NONEXACT
        and digest_records(query_mapping) == EXPECTED_SPLIT_QUERY_MAPPING_DIGEST
        and query_mapping_ok
    )
    ok &= split_query_ok
    print(
        "split_query_reverse_join", "OK" if split_query_ok else "MISMATCH",
        len(split_records), digest_records(split_records),
        len(split_exact), digest_records(split_exact),
        len(split_nonexact), digest_records(split_nonexact),
        digest_records(query_mapping),
    )

    exact_retained = {n for n in RETAINED if at(n) in split_texts}
    nonexact_retained = set(RETAINED) - exact_retained
    retained_mapping: set[str] = set()
    monolith_only: set[int] = set()
    for line_no in sorted(nonexact_retained):
        witness, score = best_witness(at(line_no), split_lines)
        if score >= 0.50:
            retained_mapping.add(f"{line_no}->{witness}:{score:.6f}")
        else:
            monolith_only.add(line_no)
    split_retained_ok = (
        (len(exact_retained), digest(exact_retained)) == EXPECTED_SPLIT_RETAINED_EXACT
        and (len(nonexact_retained), digest(nonexact_retained)) == EXPECTED_SPLIT_RETAINED_NONEXACT
        and digest_records(retained_mapping) == EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST
        and (len(monolith_only), digest(monolith_only)) == EXPECTED_MONOLITH_ONLY
        and len(retained_mapping) + len(monolith_only) == len(nonexact_retained)
    )
    ok &= split_retained_ok
    print(
        "split_retained_reverse_join", "OK" if split_retained_ok else "MISMATCH",
        len(exact_retained), digest(exact_retained),
        len(nonexact_retained), digest(nonexact_retained),
        len(retained_mapping), digest_records(retained_mapping),
        len(monolith_only), digest(monolith_only),
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n for n, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in compiled)
    }
    atlas_ok = (
        len(atlas_lines) == 542
        and (len(atlas_hits), digest(atlas_hits)) == EXPECTED_ATLAS_HITS
        and "Turing Machines" in atlas_lines[176]
        and "move in two dimensions" in atlas_lines[178]
    )
    ok &= atlas_ok
    print("atlas_summary_only", "OK" if atlas_ok else "MISMATCH", len(atlas_hits), digest(atlas_hits))

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[25] == "Two-Dimensional Turing Machines,"
        and len(set(catalog_lines[1:])) == 45
        and "## 25. Two-Dimensional Turing Machines" in taxonomy_text
        and "Two-dimensional grid of tape cells." in taxonomy_text
        and "single active head occupies one grid location" in taxonomy_text
        and "four possible movement directions on the square grid" in taxonomy_text
        and "`movement_set`" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only", "OK" if catalog_ok else "MISMATCH")

    architecture_inference_ok = (
        source_facts_ok
        and inherited_turing_ok
        and tagged_representation_ok
        and variants_ok
        and hex_worm_source_limit_ok
        and experiment_controls_ok
        and square_rule_count_ok
        and langton_ok
        and atomic_lowering_ok
    )
    ok &= architecture_inference_ok
    print(
        "architecture_inference_parameterizes_t12_event_over_2d_support_and_moves",
        "OK" if architecture_inference_ok else "MISMATCH",
    )

    unresolved_total = (
        len(classification_delta)
        + len(index - set(INDEX_ROUTED))
        + len(set(INDEX_ROUTED) - index)
        + len(monolith_only)
    )
    unresolved_ok = unresolved_total == 0
    ok &= unresolved_ok
    print("unresolved_total", "OK" if unresolved_ok else "MISMATCH", unresolved_total)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
