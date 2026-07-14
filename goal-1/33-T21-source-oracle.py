#!/usr/bin/env python3
"""Frozen source-evidence audit for T21 Two-Dimensional Cellular Automata.

This oracle audits source identity and architecture evidence; it is not a CA
implementation.  It freezes the complete direct-name surface, the square-grid
four-neighbor construction, all three five-site rule forms, synchronous update
semantics, seeds and realization boundaries, lattice variants, close T22/T23/
T24 controls, Game of Life relations, history, properties, and observers.

T21's DOMAIN is discrete t+2D.  The fixed support/topology and its realization
boundary belong to the configuration.  A square/von-Neumann neighborhood is a
typed offset preset; it does not justify a family executor or a CA-only runner.
Every query candidate has one frozen disposition and the remainder is empty.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T21 source oracle requires assertions; do not use -O")


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


# The queries deliberately overlap.  Q00 saturates both singular and plural
# direct names. Q01--Q06 recover the cardinal square profile, implementation,
# rule quotients/codecs, and alternate lattices. Q07--Q10 are close-family
# controls. Q11--Q16 close observers, support/boundary, update semantics,
# history, and relations. Q17 closes actual-Index aliases; Q18 independently
# freezes the 10/6/32-case split and catches misleading 2^32 collisions.
QUERIES = {
    "Q00": r"\b(?:two[- ]dimensional|2D) cellular autom(?:aton|ata)\b|\b2D CAs?\b",
    "Q01": (
        r"\b(?:neighbors? in all four directions|(?:four|4)[ -](?:immediate |nearest |orthogonal )?"
        r"neighbors?|(?:five|5)[ -](?:neighbor|cell)(?:hood)?s?|von Neumann neighborhood)\b"
    ),
    "Q02": r"\b(?:square (?:grid|lattice)|grid of (?:black and white )?cells|whole grid of cells)\b",
    "Q03": (
        r"\b(?:AxesTotal|FullTotal|CAStep\[\{rule_, d_\}|PadLeft\[\{\{1\}\}, \{n, n\}|"
        r"ListConvolve\[\{\{0, 2, 0\}|offset list os)\b"
    ),
    "Q04": r"\b(?:outer totalistic|growth totalistic|5-neighbor square|9-neighbor square)\b",
    "Q05": (
        r"\b(?:code(?: number)?s? (?:1022|942|175850|746|174826|3702|468|312|204|686|12|52)|"
        r"outer totalistic codes? (?:111|293|295|920)|4,294,967,296 possible five-neighbor)\b"
    ),
    "Q06": (
        r"\b(?:hexagonal (?:grid|lattice|neighborhood)|triangular (?:grid|lattice)|"
        r"pentagonal example|Penrose tiling|other geometries|Voronoi region|"
        r"square \(4 neighbors\) and hexagon \(6\))\b"
    ),
    "Q07": (
        r"\b(?:eight|8)[ -]neighbors?\b|\b9[- ](?:neighbor|cell)(?:hood)?s?\b|"
        r"\bMoore neighborhood\b|\bincluding diagonals\b"
    ),
    "Q08": r"\b(?:three[- ]dimensional|3D) cellular autom(?:aton|ata)\b|\b3D CAs?\b",
    "Q09": (
        r"\b(?:higher[- ]dimensional cellular automata?|\(2d\+1\)-neighbor|"
        r"3<sup>d</sup> -neighbor|in d dimensions with k colors|in any dimension)\b"
    ),
    "Q10": r"\bGame of Life\b|\bConway(?:'s)? Life\b",
    "Q11": (
        r"\b(?:one-dimensional slices? through (?:some of )?the two-dimensional|limiting shapes|"
        r"orientation dependence[^.]{0,120}two-dimensional|2D cellular autom(?:aton|ata)"
        r"[^.]{0,160}(?:history|image processing|simulator|visual|slic|invariant|reversib|"
        r"undecid|persistent|univers|self-reproduction)|(?:invariant|repeating) "
        r"(?:states|configurations)[^.]{0,160}2D cellular autom(?:aton|ata))\b"
    ),
    "Q12": (
        r"\b(?:starting (?:with|from) a single black (?:cell|square)|initial condition"
        r"[^.]{0,100}row of (?:7|11) black cells|periodic boundary conditions|"
        r"cyclic boundary conditions|effectively wrapped around|wrap around at each edge|"
        r"initial condition[^.]{0,100}continue cyclically|tricky point in cellular automaton "
        r"programs concerns boundary conditions|single black cell on a white background|"
        r"infinite sequence of randomly chosen cells)\b|PadLeft\[\{\{1\}\}, \{n, n\}"
    ),
    "Q13": (
        r"\b(?:all the cells[^.]{0,80}updated in parallel|all their elements[^.]{0,80}"
        r"updated in parallel|every cell is updated in parallel|intrinsically operate in parallel|"
        r"color of each cell being updated according to a rule)\b"
    ),
    "Q14": (
        r"\b(?:5-cell neighborhood on page 170|9-cell one on page 177|general 2D rules|"
        r"rule numbers are specified as on page 927|numbers of possible rules|"
        r"Symmetric 5-neighbor rules|Page 171 · Code 942 slices|Cellular automaton art)\b"
    ),
    "Q15": (
        r"\b(?:John von Neumann|Edward Moore|Tommaso Toffoli|Norman Margolus|"
        r"Stanislaw Ulam|Marcel Golay)\b[^.]{0,240}\b(?:2D|cellular autom(?:aton|ata)|"
        r"neighborhood|simulator)|\b(?:2D|cellular autom(?:aton|ata)|neighborhood|simulator)"
        r"[^.]{0,240}\b(?:John von Neumann|Edward Moore|Tommaso Toffoli|Norman Margolus|"
        r"Stanislaw Ulam|Marcel Golay)\b"
    ),
    "Q16": (
        r"\b(?:rugs|wallpaper|image processing|self-reproduction|constraints?|feature extraction)"
        r"\b[^.]{0,180}\b(?:2D|two-dimensional|5-neighbor)\b|\b(?:2D|two-dimensional|"
        r"5-neighbor)[^.]{0,180}\b(?:rugs|wallpaper|image processing|self-reproduction|"
        r"constraints?|feature extraction)\b"
    ),
    "Q17": (
        r"\b(?:Square lattices|von Neumann neighborhood|Moore neighborhood|"
        r"Higher-dimensional cellular automata|Three-dimensional cellular automata)\b"
    ),
    "Q18": (
        r"IntegerDigits\[code, 2, 10\]|2\^\{32\}|2\^6 = 64|"
        r"32 (?:possible )?5-cell neighborhoods|last digit specifies what color the center cell|"
        r"second-to-last digit specifies what happens"
    ),
}

DIRECT_NAME_STREAM_RX = re.compile(
    r"\b(?:two[- ]dimensional|2D) cellular autom(?:aton|ata)\b|\b2D CAs?\b",
    re.IGNORECASE,
)

EXPECTED_QUERY = {
    "Q00": (112, 78, 34, "f65001a09ea0aabab38615d348ac3ffb1d1721e2627da8960b84eab87edea087"),
    "Q01": (40, 38, 2, "d26016e800b2c07b0fb630ed9edac435ebd958ce31e98d509f8fafac6ea15151"),
    "Q02": (18, 18, 0, "0d5d4d04e50acba024d55fe043c5d3a51c6e5b6c14f019606fd1fbea210cd23d"),
    "Q03": (6, 6, 0, "c70886cb207819db85a255b80ebf66d72b4d3e484fe17f334e619a18d8e8ec4f"),
    "Q04": (21, 18, 3, "9252bbb7dac14f4b738f1bf3d460a72c71d5fd2d616436b6c07800a55d5d7020"),
    "Q05": (25, 19, 6, "96547c52ef296a21925dbea4e81d1e719f8b34e3d78e105b523ba6220a25fd44"),
    "Q06": (18, 15, 3, "d6582468faaf182f73dd0d884e4d56014733ab67a55ccddf0d6fea4060da9447"),
    "Q07": (20, 18, 2, "7131cde2499d7365b781a4c282957e89d8240d7e95fd3cf859dcb1ad247ffeb5"),
    "Q08": (10, 5, 5, "f2013b2b3a19f3381967f98a5c5b2a084348b65cba40cf9fec5ee68ec779d650"),
    "Q09": (4, 4, 0, "be34d4b3e5b67c6e8815cff1e0148f9ce2d136e476dfe3f043cef77694fc5185"),
    "Q10": (36, 13, 23, "ab6b262ac2b5a45961e444904c8545324eb49cd1c9246384ec5b8cbbe967dc5f"),
    "Q11": (12, 8, 4, "131f791f95a02d446689bcb58cec6f54b549bc662b4abf57e4c3b086049ad031"),
    "Q12": (45, 44, 1, "f05be26f2ace5032d336287d6254f990b1793f2c1ab700fbfda0086acabc801a"),
    "Q13": (5, 5, 0, "2634ac63a4539e11d83086298cf2c7eca047df1a93c470d82be34809d87c10d7"),
    "Q14": (8, 8, 0, "19882907007efd13565e280e8ba699b2963a9b146b4aeda91667dcd354fec708"),
    "Q15": (10, 10, 0, "c344186cc0322a9cb86e4c6e69603d7d2c3845b2f3d33d88eb1a24ee8f44cbe5"),
    "Q16": (27, 16, 11, "c74bff6def66449b996ac455e5e9d815743995c254ed0f05e282e48fec1fb28d"),
    "Q17": (10, 6, 4, "b4c3deeee4a8096d212e29cb44ccd9378f631628f4d2617342cbdb2b297c31b5"),
    "Q18": (11, 11, 0, "c026bcf3affa32135845f977747b28f4cb02e7eac37273ff6c97635db85270f4"),
}


def line_set(spec: str) -> frozenset[int]:
    return frozenset(map(int, spec.split(","))) if spec else frozenset()


# 180 queried lines are retained after review; 42 broad-query collisions are
# excluded.  The other 132 retained lines are governed continuations, source-
# bound images, multiline implementations, and typed close-family controls.
MATCHED_RETAINED = line_set(
    "142,670,672,850,1254,2156,2168,2170,2174,2178,2180,2184,2190,2194,"
    "2198,2202,2206,2208,2212,2218,2226,2230,2234,2236,2238,2250,2256,2262,"
    "2410,2596,2600,2654,2908,2910,2918,2922,2926,2930,3034,3892,3894,"
    "3902,3914,3956,4072,4082,4422,4430,4440,4452,5082,5088,5316,5324,"
    "5638,5788,5816,6636,6644,6684,6848,7862,7896,8322,8324,10261,10882,"
    "10986,10992,11037,11067,11068,11070,11072,11074,11136,11178,11192,"
    "11495,11497,11505,11507,11511,11521,11548,11552,11558,11565,11567,"
    "11569,11581,11603,12840,13265,13469,13471,13473,13475,13483,13488,"
    "13490,13497,13501,13503,13513,13520,13534,13536,13538,13544,13547,"
    "13548,13549,13551,13559,13563,13575,13579,13601,13613,13617,13619,"
    "13620,13621,13622,13642,13644,13650,13654,13666,13679,14048,14113,"
    "14115,14144,14239,14241,14243,14301,14336,14464,14660,14695,14787,"
    "14845,15221,15259,15267,15293,15295,15301,15321,15359,15412,15444,"
    "15499,15539,15608,15708,15713,15791,15942,15955,15959,15972,16022,"
    "16215,16255,16446,17384,17394,17431,18249,18749,18755,19256,19266,"
    "19274,19588,20480"
)

GOVERNED_CONTINUATIONS = line_set(
    "2172,2176,2182,2186,2188,2192,2196,2200,2204,2210,2214,2216,2220,"
    "2222,2224,2228,2232,2240,2242,2244,2246,2248,2252,2254,2258,2260,"
    "2912,2914,2916,2920,2924,2928,3900,3912,4080,5086,5636,6642,10259,"
    "11069,11071,11073,11075,11077,11079,11080,13467,13477,13479,13481,"
    "13485,13486,13487,13489,13491,13492,13493,13494,13495,13499,13505,"
    "13507,13509,13511,13515,13516,13517,13518,13522,13523,13524,13525,"
    "13526,13528,13530,13531,13540,13542,13543,13545,13546,13553,13554,"
    "13555,13556,13557,13558,13561,13565,13567,13569,13571,13573,13577,"
    "13580,13582,13583,13584,13585,13586,13587,13588,13589,13590,13591,"
    "13592,13593,13594,13595,13596,13597,13599,13603,13605,13607,13609,"
    "13611,13615,13624,13626,13628,13630,13632,13634,13636,13638,13640,"
    "13646,13648,13652,13656,13658"
)

RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS
EXPECTED_SOURCE_COUNT = 312
EXPECTED_SOURCE_DIGEST = "50caf57ebaa912d54ca50df2ec22ebcd418d2b898fbe03414de0af282e9fa60d"

# Native T21 mechanics are only the square/cardinal construction, the shared
# old-snapshot update, its three explicit rule representations, seeds, and
# boundary realizations. Everything else retained is a relation or control.
NATIVE_EVIDENCE = (
    frozenset({850, 1254, 2156, 10986, 10992, 11136, 13265, 16446, 18249})
    | frozenset(range(2168, 2211, 2))
    | (frozenset(range(2908, 2931, 2)) - {2918})
    | line_set(
        "11067,11069,11070,11071,11072,11073,11074,11075,11077,11079,11080,"
        "13467,13469,13471,13473,13513,13515,13516,13517,13518,13520,13522,"
        "13523,13524,13525,13526,13528,13530,13531,13534,13536,13538,13540,"
        "13542,13543,13544,13545,13546,13547,13548,13549,13551,13553,13554,"
        "13555,13556,13557,13558,13559,13561,13563,13565,13567,13569,13571,"
        "13573,13575,13577,13617,13619,14301,14336"
    )
)

T22_CONTROL = line_set(
    "670,672,2212,2214,2216,2218,2220,2222,2224,2226,2228,2230,2232,2234,"
    "2918,3900,3902,3912,3914,4452,5638,8322,10261,11068,11178,11507,"
    "11565,13475,13477,13479,13481,13497,13499,13501,13503,13505,13507,"
    "13579,14239,14241,14243,14787,15301,15359,15959,18755"
)
T23_CONTROL = line_set(
    "2236,2238,2240,2242,2244,2246,2248,2250,2252,2254,2256,2258,2260,2262,"
    "11192,13509,13511,13632,13634,13636,13638,13640"
)
T24_CONTROL = line_set(
    "11037,13483,13485,13486,13487,13488,13489,13490,13491,13492,13493,"
    "13494,13495,13642,13644,13646,13648,13650,13652,13654,13656,13658"
)
OTHER_CONTROL = line_set(
    "2410,2596,2600,2654,5788,13580,13582,13583,13584,13585,13586,13587,"
    "13588,13589,13590,13591,13592,13593,13594,13595,13596,13597,13599,"
    "13601,13603,13605,13607,13609,13611,13613,13615,13666,13679,14048,"
    "14113,14115,14144,15221,15412,15608,16255,19274,19588"
)
CONTROL_EVIDENCE = T22_CONTROL | T23_CONTROL | T24_CONTROL | OTHER_CONTROL
RELATION_EVIDENCE = RETAINED - NATIVE_EVIDENCE - CONTROL_EVIDENCE

EXPECTED_SET = {
    "union": (283, "8011234be88f7701d989637b17fb0c4d29c6a2f581349135df7d6e53da267062"),
    "pre_index_union": (222, "6dd224ef51b5d767b3f1aa15264680584323dcd41f0cecb5cbc3178eb6ac2710"),
    "index": (61, "0d24061a7997946b106a2afe88529d9af0ecdf285b46b3c1d96ca729414d2684"),
    "matched_retained": (180, "5998b9deafc9b19404c07de328dc188771b80b8fcaece58e46f403eecb269584"),
    "governed_continuations": (132, "1f693900e93176cd68716b4f8a9edc7c2673d9216c6a295e0fe2d6b24aed1b92"),
    "retained": (312, EXPECTED_SOURCE_DIGEST),
    "excluded": (42, "c09e0fd7840d9479290be19d0c6f32fc632a2900ad03154839ec019055c770ba"),
    "native": (104, "dadb04aef72a78f676cd06ef87109faf2581b6dde190fddc813fbe873220a640"),
    "relation": (75, "e8de98fc89586c37b194a028f97211f38a109433bea50f34ed60c8cee3abb10f"),
    "control": (133, "374a2a8a05ea9a10db23aace923856cfd116394b2e64c3fba9c18a43abe72224"),
}

EXPECTED_EXCLUDED_CLASS = {
    "one_dimensional_seed_background": (26, "76768e71026360c2bca9f3da8fedc35c746f2a844c6410754f7c5c1e736025dc"),
    "square_lattice_background": (6, "23fb05a97ff9523ac06e4f19bcfe2f59dbd144b4787299cdc427d52a9cb885e7"),
    "code_count_collision": (4, "89d8813bc251c3f86843eccb05837c2033dd90a8446ee0d218b1b261165be2ac"),
    "neighbor_word_collision": (5, "d8913fa9de98611fafcf3fe27709a231e8acb91b789446760da2718db80853a9"),
    "other_background": (1, "a398152fa8e559b07ad69683d6f51a0e9cefad1d0e0c495642fe10b2e1170417"),
}
EXPECTED_INDEX_CLASS = {
    "t21_routes": (34, "48da7ba8bef0b671806cba2d338a2b0257d26b358818d2f0d3b586d67c72fca1"),
    "t22_life_routes": (18, "d1f0d2f458f7002c2b2404a527b27c5f244e7a689a6641b5e98b10de577c6114"),
    "t23_routes": (3, "c1ec6cd7f7b24f92309bddc1a0312769e81c52ba53d95246ca3d1118b8c281f8"),
    "t24_lattice_routes": (2, "d77f2bc1978314d7a59a68a89c699aadb77fd6cbde0a455d6864c8a871a2ef5a"),
    "rule_code_routes": (3, "8f45cb02b25fd9213d9d6150baddd02733afa2b73b75792f44a460c445fbe2f2"),
    "other_index_background": (1, "5ff11842e79ccdab708d273fd345efd5f8fdedc3976b17574a9d0f9f643cb257"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY_RECORDS = (281, "587d86a9f003c5d981bc09fa8492c23af93d0d2ae6e8d07030c6f94f75ac12ed")
EXPECTED_SPLIT_EXACT_QUERY_RECORDS = (266, "9d25633c7d1cddbfbd02c302d78f1f9567ab590b247307e68e21c911a56b045f")
EXPECTED_SPLIT_NONEXACT_QUERY_DIGEST = "c5f9c056ef956f51db8d0495cfb54e4d1b5adba4c965900aeea19a255962aaf7"
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = "f578cda27b1cc5b4374693d4c5b262ea486598445f68cf6b303dbd6f21abd19a"

SPLIT_NONEXACT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:4909": (22352,),
    "BACK-MATTER/Index/Index.md:2214": (14313,),
    "BACK-MATTER/Index/Index.md:3194": (15293,),
    "BACK-MATTER/Index/Index.md:5287": (17384,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:163": (7862,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:605": (8322,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:743": (8464,),
    "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md:2902": (11521,),
    "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md:45": (450,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:13": (2156,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:47": (2190,),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:69": (2212,),
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md:491": (3914,),
    "CHAPTERS/8-Implications-for-Everyday-Systems/Implications-for-Everyday-Systems.md:109": (4452,),
    "FRONT-MATTER/Preface/Preface.md:56": (142,),
}

EXPECTED_SPLIT_DIRECT_COUNTS = {
    "BACK-MATTER/Colophon/Colophon.md": 50,
    "BACK-MATTER/Index/Index.md": 27,
    "CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md": 3,
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md": 2,
    "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md": 18,
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md": 14,
    "CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md": 7,
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md": 6,
    "CHAPTERS/8-Implications-for-Everyday-Systems/Implications-for-Everyday-Systems.md": 2,
    "CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md": 3,
    "FRONT-MATTER/Preface/Preface.md": 1,
}
EXPECTED_SPLIT_DIRECT_COUNTS_DIGEST = "ab544ec1361afc04d4f33a8db64d488ec91cc9797fb719b60fde70ca5274f224"

EXPECTED_EXACT_RETAINED_MIRRORS = (244, "0f6aad633c172e9089bb0f5ab7fa6ef7cdbd99363461040567c543597f6df895")
EXPECTED_SPLIT_NONEXACT_RETAINED = (68, "dec93299051fddeddfde24bdc9365789d7224fc005958ac153a2fe9cecd3ff29")
MONOLITH_ONLY_RETAINED = frozenset({670, 672})
EXPECTED_MONOLITH_ONLY_DIGEST = "e92cb1a2eccf4c40fee9c336e8d42bd0e32a46aeda886ad95524aa9a318b622e"
MANUAL_RETAINED_WITNESSES = {
    142: "FRONT-MATTER/Preface/Preface.md:56",
    7862: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:163",
    11521: "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md:2902",
    17384: "BACK-MATTER/Index/Index.md:5287",
}
EXPECTED_RETAINED_MAPPING_COUNT = 66
EXPECTED_RETAINED_MAPPING_DIGEST = "5c757acfb0a537ea2538bcad0ab6ddb36f309b57929d1e36e8aab1977f78e0d9"
EXPECTED_RETAINED_WITNESS_DIGEST = "dae36d70a1c812eeb498dabc7ab396dfa775847cb8858806b27a5a6827ef330b"


def digest(lines: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(lines))).encode("ascii")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def classify_excluded(excluded: set[int], hits: dict[str, set[int]]) -> dict[str, set[int]]:
    remaining = set(excluded)
    classes: dict[str, set[int]] = {}
    routes = (
        ("one_dimensional_seed_background", hits["Q12"]),
        ("square_lattice_background", hits["Q02"] | hits["Q06"]),
        ("code_count_collision", hits["Q18"]),
        ("neighbor_word_collision", hits["Q01"] | hits["Q07"]),
    )
    for name, route in routes:
        classes[name] = remaining & route
        remaining -= classes[name]
    classes["other_background"] = remaining
    return classes


def classify_index(index: set[int], hits: dict[str, set[int]]) -> dict[str, set[int]]:
    remaining = set(index)
    classes: dict[str, set[int]] = {}
    routes = (
        ("t21_routes", hits["Q00"]),
        ("t22_life_routes", hits["Q07"] | hits["Q10"]),
        ("t23_routes", hits["Q08"]),
        ("t24_lattice_routes", hits["Q06"] | hits["Q09"] | hits["Q17"]),
        ("rule_code_routes", hits["Q04"] | hits["Q05"] | hits["Q18"]),
    )
    for name, route in routes:
        classes[name] = remaining & route
        remaining -= classes[name]
    classes["other_index_background"] = remaining
    return classes


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 33-T21-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
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
        good = actual == EXPECTED_QUERY[name]
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index_union = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index_union
    matched_retained = pre_index_union & RETAINED
    governed_continuations = set(RETAINED) - union
    excluded = pre_index_union - RETAINED
    sets = {
        "union": union,
        "pre_index_union": pre_index_union,
        "index": index,
        "matched_retained": matched_retained,
        "governed_continuations": governed_continuations,
        "retained": set(RETAINED),
        "excluded": excluded,
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
    }
    for name, values in sets.items():
        expected_count, expected_digest = EXPECTED_SET[name]
        good = len(values) == expected_count and digest(values) == expected_digest
        ok &= good
        print(name, "OK" if good else "MISMATCH", len(values), digest(values))

    excluded_classes = classify_excluded(excluded, hits)
    excluded_ok = set().union(*excluded_classes.values()) == excluded
    for name, values in excluded_classes.items():
        expected = EXPECTED_EXCLUDED_CLASS.get(name)
        good = expected == (len(values), digest(values))
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", len(values), digest(values))
    ok &= excluded_ok
    print("unresolved_pre_index", "OK" if excluded_ok else "MISMATCH", 0)

    index_classes = classify_index(index, hits)
    index_ok = set().union(*index_classes.values()) == index
    for name, values in index_classes.items():
        expected = EXPECTED_INDEX_CLASS.get(name)
        good = expected == (len(values), digest(values))
        index_ok &= good
        print(f"index_{name}", "OK" if good else "MISMATCH", len(values), digest(values))
    ok &= index_ok
    print("unresolved_index", "OK" if index_ok else "MISMATCH", 0)

    # Three source rule forms share the same 5-site offset profile but not the
    # same RULE quotient. Main-text page 170 and its direct Notes code are a
    # center-conditioned cardinal count (10 cases); page 262 is equal sum over
    # all five sites (6 cases); General rules is the full 32-context table.
    strict_rule_forms_ok = (
        "neighbors in all four directions" in at(2168)
        and "four neighbors" in at(2170)
        and "as well as on its own previous color" in at(2170)
        and "last digit specifies what color the center cell should be" in at(2194)
        and "second-to-last digit specifies what happens" in at(2194)
        and "progressively more neighbors are black" in at(2194)
        and "ListConvolve[{{0, 2, 0}, {2, 1, 2}, {0, 2, 0}}" in at(13473)
        and "IntegerDigits[code, 2, 10]" in at(13473)
        and "four immediate neighbors" in at(2922)
        and "total of the cell and its four neighbors runs from 5 down to 0" in at(2922)
        and "$2^{32}" in at(13544)
        and "$2^{10} = 1024$" in at(13547)
        and "$2^6 = 64$" in at(13548)
    )
    ok &= strict_rule_forms_ok
    print("strict_rule_forms_10_6_32", "OK" if strict_rule_forms_ok else "MISMATCH")

    # Preserve raw tuples. No N/W labels are inferred from Book row/column
    # coordinates; an orientation adapter must be explicit at an API boundary.
    raw_offsets = r"\{(-1, 0), \{0, -1\}, \{0, 0\}, \{0, 1\}, \{1, 0\}\}"
    general_table_ok = (
        raw_offsets in at(13513)
        and "offset lists are always taken to be in the order given by *Sort*" in at(13513)
        and "same order as the offset list" in at(13513)
        and "IntegerDigits[i, k, Length[os]]" in at(13520)
        and "FromDigits[Reverse[u], k]" in at(13520)
        and "ListCorrelate" in at(13531)
    )
    ok &= general_table_ok
    print("raw_sorted_offsets_no_implicit_orientation", "OK" if general_table_ok else "MISMATCH")

    update_domain_ok = (
        "updated in parallel at every step" in at(850)
        and "based on the colors of neighboring cells on the previous step" in at(16446)
        and "array of white squares with a single black square in the middle" in at(13469)
        and "practical computer one can use only a finite array" in at(10986)
        and "effectively use a cyclic array" in at(10986)
        and "assumed cyclic" in at(11080)
        and "periodic boundary conditions" in at(13619)
        and "centers of the cells form a lattice" in at(13644)
        and "what matters is not detailed geometry, but merely what cells are adjacent" in at(13644)
    )
    ok &= update_domain_ok
    print("discrete_t_plus_2d_configuration_topology", "OK" if update_domain_ok else "MISMATCH")

    controls_ok = (
        "eight neighbors—including diagonals" in at(2212)
        and "9-neighbor rules introduced on page 177" in at(13475)
        and "three-dimensional cellular automata" in at(2236)
        and "In d dimensions with k colors" in at(13483)
        and "Game of Life" in at(14243)
        and "Life 2D cellular automaton" in at(14243)
        and "Other geometries" in at(13642)
        and "triangular lattice" in at(13650)
        and "nested Penrose tiling" in at(13654)
    )
    ok &= controls_ok
    print("t22_t23_t24_and_life_controls", "OK" if controls_ok else "MISMATCH")

    structural = (
        len(RETAINED) == EXPECTED_SOURCE_COUNT
        and digest(RETAINED) == EXPECTED_SOURCE_DIGEST
        and MATCHED_RETAINED == matched_retained
        and GOVERNED_CONTINUATIONS == set(RETAINED) - union
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not CONTROL_EVIDENCE & RELATION_EVIDENCE
        and NATIVE_EVIDENCE | CONTROL_EVIDENCE | RELATION_EVIDENCE == RETAINED
        and pre_index_union == matched_retained | excluded
        and not matched_retained & excluded
        and not RETAINED & index
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    # Split-copy closure. Query and retained reverse-join constants are filled
    # below after their exact records are frozen.
    split_paths = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() not in {DEFAULT_BOOK.resolve(), ATLAS.resolve()}
    )
    relative_paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in split_paths]
    manifest = [
        f"{rel}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, rel in zip(split_paths, relative_paths, strict=True)
    ]
    split_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    ok &= split_manifest_ok
    print("split_manifest", "OK" if split_manifest_ok else "MISMATCH",
          len(split_paths), digest_records(relative_paths), digest_records(manifest))

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    compiled = [re.compile(pattern, re.I) for pattern in QUERIES.values()]
    atlas_hits = {
        n for n, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in compiled)
    }
    atlas_retained = atlas_hits | {13}
    atlas_ok = (
        len(atlas_lines) == 542
        and atlas_hits == {175}
        and atlas_retained == {13, 175}
        and "higher dimensions change the story" in atlas_lines[12]
        and "Two- and three-dimensional cellular automata" in atlas_lines[174]
        and "same core behavior classes persist" in atlas_lines[174]
    )
    ok &= atlas_ok
    print("atlas", "OK" if atlas_ok else "MISMATCH", len(atlas_retained), digest(atlas_retained))

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[21] == "Two-Dimensional Cellular Automata,"
        and len(set(catalog_lines[1:])) == 45
        and "## 21. Two-Dimensional Cellular Automata" in taxonomy_text
        and "Fixed two-dimensional grid of cells." in taxonomy_text
        and "All cells update in parallel." in taxonomy_text
        and "four orthogonal neighbors" in taxonomy_text
        and '`dimension`: `2`.' in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
