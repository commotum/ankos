#!/usr/bin/env python3
"""Frozen primary-source audit for T32 oriented template constraints.

This is an evidence oracle, not a constraint solver.  It freezes redundant
query lanes over the canonical monolithic Book, classifies every returned
line and governed continuation, routes the actual Index, and reverse-joins
the split corpus.  It also binds the official Wolfram Science repair for four
Blank characters corrupted in the local extraction.

The smallest strict construction recovered here is a declarative model set:
every site of a binary two-dimensional total field exposes the exact ordered
five-site cardinal cross, and that assignment must be a member of a finite
allowed set.  Reads at neighboring sites overlap because they refer to one
field.  There is no seed, time step, write, update, successor, or solver in
the construction.  Finite checking, periodic presentations, search, and
symmetry reduction remain separately typed operations or observations.
"""

from __future__ import annotations

import hashlib
import itertools
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T32 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"
OFFICIAL_NOTE_SNAPSHOT = (
    ROOT / "goal-1/40-T32-official-checking-note-snapshot.txt"
)
LANGUAGE_SEMANTICS_SNAPSHOT = (
    ROOT / "goal-1/39-T28-wolfram-language-semantics-snapshot.txt"
)

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"
EXPECTED_OFFICIAL_NOTE_SNAPSHOT_SHA256 = (
    "15e06813de186756952e5ec1d465ed4cec7931fc388b68e08437af1cd0c6678f"
)
EXPECTED_OFFICIAL_NOTE_DOCUMENT_SHA256 = (
    "9d11a2fa1f1bce6b40a7cf896303749c7fe562b4b68244b860226e91b0348bfb"
)
EXPECTED_LANGUAGE_SEMANTICS_SNAPSHOT_SHA256 = (
    "89dc720f5f905d41821c4284457cf75d08de2cae66af501789f26746682c6589"
)

OFFICIAL_NOTE_URL = (
    "https://www.wolframscience.com/nks/"
    "notes-5-7--checking-tilings-with-constraints/"
)
OFFICIAL_RAW_ALLOWED_PATTERN_HTML = (
    '<span class="inlinecode clipboard-inline" '
    'data-copy="\\!\\(\\*SubscriptBox[\\(t\\),\\(1\\)]\\)|'
    '\\!\\(\\*SubscriptBox[\\(t\\),\\(2\\)]\\)|'
    '\\!\\(\\*SubscriptBox[\\(t\\),\\(3\\)]\\)">'
    "t<sub>1</sub> | t<sub>2</sub> | t<sub>3</sub></span>"
)
OFFICIAL_RAW_TEMPLATE_HTML = (
    '<span class="inlinecode clipboard-inline">'
    "{{_, 1, _}, {0, 0, 1}, {_, 0, _}}</span>"
)
OFFICIAL_RAW_CHECKER_HTML = (
    '<span class="clipboard-block">SatisfiedQ[list_, allowed_] := '
    '<span class="spacer-2"></span>Apply[And, Map[MatchQ[#, allowed] &amp;, '
    '<span class="spacer-5"></span> Partition[list, {3, 3}, {1, 1}], {2}], '
    "{0, 1}]</span>"
)
OFFICIAL_DECODED_TEMPLATE = "{{_, 1, _}, {0, 0, 1}, {_, 0, _}}"
OFFICIAL_DECODED_ALLOWED_PATTERN = "t1 | t2 | t3"
OFFICIAL_DECODED_CHECKER = (
    "SatisfiedQ[list_, allowed_] := Apply[And, Map[MatchQ[#, allowed] &, "
    "Partition[list, {3, 3}, {1, 1}], {2}], {0, 1}]"
)


# Frozen, deliberately redundant discovery lanes.  Exact construction lanes
# are joined by shape, overlap, representation, search-boundary, sibling, and
# actual-Index lanes.  Modern taxonomy labels are included as negative guards.
QUERIES = {
    "Q00": r"\bfixed set of possible templates\b",
    "Q01": (
        r"\btemplates apply to every cell\b|"
        r"\btemplates of neighboring cells overlapping\b|"
        r"\beach neighborhood match one of a fixed set of templates\b"
    ),
    "Q02": (
        r"4,294,967,296 possible sets of such templates|"
        r"766,979,044 lead to constraints|3,527,988,252 that remain"
    ),
    "Q03": (
        r"\b171 (?:repetitive )?patterns\b|"
        r"\bminimal constraint which requires the given pattern\b"
    ),
    "Q04": (
        r"\bPage 215 · 2D constraints\b|"
        r"\bNumbering scheme\.\*\* The constraint numbered\b|"
        r"IntegerDigits\[n, 2, 32\]"
    ),
    "Q05": (
        r"\bChecking constraints\b|SatisfiedQ\[list_, allowed_\]|"
        r"MatchQ\[#, allowed\]|Partition\[list, \{3, 3\}, \{1, 1\}\]"
    ),
    "Q06": r"\ballowed templates\b|\ballowed local templates\b",
    "Q07": (
        r"\bcompatible with itself or with at least one other\b|"
        r"\beight immediately adjacent positions\b"
    ),
    "Q08": (
        r"\bcomplete\s+\$?3 ?\\?times ?3\$?\s+blocks of cells\b|"
        r"\b3×3 templates\b|\b3\\times3\$?\s+templates\b|"
        r"\b3 by 3 templates\b"
    ),
    "Q09": (
        r"\bincrease the size of the templates\b|"
        r"\bincrease the number of possible colors for each cell\b"
    ),
    "Q10": (
        r"\bparticular template from this set must appear at least somewhere\b|"
        r"\bcertain template from this set must occur at least once\b|"
        r"\bfirst template must appear at least somewhere\b|"
        r"\bevery template in the set, must occur somewhere\b"
    ),
    "Q11": (
        r"\bfixed number of black and white neighbors\b|"
        r"\bvarious numbers of black and white neighbors\b|"
        r"\bexactly one black neighbor\b[^.]{0,180}\bexactly two white neighbors\b"
    ),
    "Q12": (
        r"\bno such direct procedure\b|\balways go outside of the system\b|"
        r"\bbuild up patterns iteratively\b|\bbacktracking if the constraint\b|"
        r"\bextend patterns along a square spiral\b"
    ),
    "Q13": (
        r"\btessellation of 5 x 10 blocks\b|\btessellation of 24 x 24 blocks\b|"
        r"\bRepresenting repetitive patterns\b|"
        r"\btessellations of rectangles whose corners overlap\b"
    ),
    "Q14": (
        r"\bgeneral problem of whether an infinite pattern exists\b|"
        r"\bno upper bound on the size of region\b|"
        r"\bfinite region is NPcomplete\b|"
        r"\bno pattern that satisfies the constraint in a limited region\b"
    ),
    "Q15": (
        r"\bconstraints which differ only by overall rotation, reflection\b|"
        r"\bpatterns differing by overall reflection, rotation or interchange\b|"
        r"\brotations and reflections\b"
    ),
    "Q16": (
        r"\bonly some of the\s+\$k\^n\$\s+possible blocks\b|"
        r"\bonly certain length n blocks are allowed\b|"
        r"\bsubshifts of finite type\b|\bfinite complement languages\b"
    ),
    "Q17": (
        r"\bRelation to 2D cellular automata\b|"
        r"\bconstraint can then be represented in terms of a set of allowed templates\b|"
        r"\bconfigurations that remain unchanged in the evolution of a 2D cellular automaton\b"
    ),
    "Q18": (
        r"\bconstraints discussed here are similar to those encountered in covering the plane\b|"
        r"\btiling problem[^.]{0,180}grid-based constraint systems\b|"
        r"\bTessellations defined by constraints\b"
    ),
    "Q19": (
        r"\bnetwork is determined by the constraint[^.]{0,180}template\b|"
        r"\bnetwork constraint systems shown here are analogs\b|"
        r"\bconstraints in a network constraint system[^.]{0,180}template\b"
    ),
    "Q20": (
        r"_page_22[89]_(?:Figure_5|Picture_1)\.jpeg|"
        r"_page_230_Figure_2\.jpeg|_page_956_Picture_8\.jpeg"
    ),
    "Q21": r"\btemplate numbering, 941\b|\bfor 2D constraints, 941\b",
    "Q22": (
        r"\btemplate constraint systems?\b|"
        r"\bseeded template constraint systems?\b"
    ),
    "Q23": r"\bconstraints?[^.]{0,240}\btemplates?\b|\btemplates?[^.]{0,240}\bconstraints?\b",
    "Q24": (
        r"\bspecific templates\b|\bparticular templates to be matched\b|"
        r"\btemplate matching\b"
    ),
    "Q25": (
        r"\b32 possible (?:ones|templates|5-cell neighborhoods)\b|"
        r"\b512 possible (?:ones|templates)\b"
    ),
    "Q26": (
        r"\bmust match (?:some|one of|the) [^.]{0,80}templates?\b|"
        r"\bmust correspond to the template shown\b"
    ),
    "Q27": (
        r"\bset of allowed templates\b|\bsets of templates that are supersets\b|"
        r"\bany of a set of templates\b"
    ),
    "Q28": (
        r"\bTwo-dimensional cellular automata[^.]{0,200}\btemplate numbering, 941\b|"
        r"\bTemplates[^.]{0,200}\bfor 2D constraints, 941\b|"
        r"\bTessellations[^.]{0,160}\bdefined by constraints, 213\b"
    ),
    "Q29": r"\bsystems? based on constraints\b",
    "Q30": r"\bsystems based on constraints do not have initial conditions\b",
    "Q31": r"\bpage 213\b|\bpage 215\b|\bpage 941\b",
    "Q32": (
        r"\\\{\\\{-, 1, -\\\}, \\\{0, 0, 1\\\}, \\\{-, 0, -\\\}\\\}"
    ),
    "Q33": (
        r"\bConstraints in 1D systems, 940\b|"
        r"\bsystems based on, 210[–-]221\b|"
        r"\bSatisfying constraints, 210[–-]221\b"
    ),
    "Q34": (
        r"\bCorner-overlapping patterns, 941\b|"
        r"\bTemplates and history of CAs[^.]{0,220}\bfor 2D constraints, 941\b|"
        r"\bTilings, 211[–-]221\b"
    ),
    "Q35": (
        r"\bBacktracking[^.]{0,220}\bin satisfying constraints, 941\b|"
        r"\bSearching[^.]{0,700}\bto satisfy constraints, 343, 941\b"
    ),
    "Q36": (
        r"\bfor 2D 5-neighbor rules it is\b|"
        r"\bpossible neighborhood configurations are\b|"
        r"\bshown on page 53 for elementary rules and page 941 for 5-neighbor rules\b"
    ),
    "Q37": (
        r"\bnotion of constraints is often introduced[^.]{0,180}\bevolution rules\b|"
        r"\btwo-dimensional patterns that arise from the constraints[^.]{0,220}\binvariant states\b|"
        r"\bTypical behavior of two-dimensional cellular automata[^.]{0,160}\binvariant\b"
    ),
    "Q38": (
        r"\bPattern-avoiding sequences\b|"
        r"\bno pair of identical blocks ever appear together\b|"
        r"\bno triple of identical blocks appear together\b|"
        r"\bpatterns of blocks can be avoided\b"
    ),
}


def line_set(spec: str) -> frozenset[int]:
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Every pre-Index query hit is assigned once.  Native is the strict binary
# oriented-cross relation plus its source-backed larger-template/color
# extension.  Relations retain exact encodings, periodic presentations, CA,
# tiling, graph, and observer bridges.  Controls preserve T31/T33 and external
# search boundaries.  Two bare page-941 references are lexical false hits.
NATIVE_MATCHED = line_set(
    "2614,2616,2618,2620,2626,2628,2630,"
    "14048,14050,14052,14054,14055,14058-14060,14097"
)
RELATION_MATCHED = line_set(
    "4068,4072,4082,5776,5788,6976,13513,13520,13551,"
    "14040,14044,14047,14063,14099,"
    "14113,14115,14124,14134,"
    "16022,16367,16369,16373"
)
CONTROL_MATCHED = line_set(
    "2568,2590,2596,2600,2608,2610,"
    "2634,2640,2646,2650,2654,2672,2680,2684,2688,2696,"
    "4046,4244,4324,6948,14027,14080,14082,14083,"
    "14145,14146,14147,14151,14155,14275,15207,15930,17431,19816,20769"
)

NATIVE_CONTINUATIONS = line_set("14057,14061")
RELATION_CONTINUATIONS = line_set(
    "2322,4080,4084,5778,5780,5786,6974,"
    "13515-13518,14042,14046,"
    "14065-14067,14069,14071-14078,"
    "14109,14111,14117,14119,14121,14123,"
    "14126,14128,14130,14132,14136,14138,14140,14142,"
    "16371,17463,17465"
)
CONTROL_CONTINUATIONS = line_set(
    "2576,2584,2598,2606,2632,2636,2638,4074,4076,4078,"
    "2642,2644,2648,2652,2656,2658,2660,2662,2664,2666,2668,"
    "2670,2674,2676,2678,2682,2686,2690,2692,2694,2698,"
    "14084,14144,14149,14153"
)

NATIVE_EVIDENCE = NATIVE_MATCHED | NATIVE_CONTINUATIONS
RELATION_EVIDENCE = RELATION_MATCHED | RELATION_CONTINUATIONS
CONTROL_EVIDENCE = CONTROL_MATCHED | CONTROL_CONTINUATIONS
MATCHED_RETAINED = NATIVE_MATCHED | RELATION_MATCHED | CONTROL_MATCHED
GOVERNED_CONTINUATIONS = (
    NATIVE_CONTINUATIONS | RELATION_CONTINUATIONS | CONTROL_CONTINUATIONS
)
RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE

EXCLUDED_CLASS = {
    "bare_page_941_debruijn_relations": line_set("16159,17698"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("2616,2626,2628,14052")
RELATION_IMAGE_LINES = line_set(
    "2322,4080,5786,6974,14042,14111,14117,14136,14138,14142,17465"
)
CONTROL_IMAGE_LINES = line_set(
    "2576,2584,2598,2606,2638,2662,2670,2682,2686,2690,2692,4074,4076"
)
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES = line_set(
    "2314,2328,2564,5804,6926,6940,6942,6944,6946,"
    "6952,6954,6964,6982,17457,17461,17469,17475,17479,17483"
)
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES


INDEX_CLASS = {
    "solver_and_constraint_routes": line_set("20908,21042,21044,22080"),
    "one_dimensional_language_routes": line_set("21189,22144"),
    "T32_template_tiling_routes": line_set("21050,22150,22291,22380"),
    "sibling_spin_and_substitution_routes": line_set("22134,22146"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_ENTRY_GUARDS = {
    "solver_and_constraint_routes": {
        20908: ("backtracking", "in satisfying constraints, 941"),
        21042: ("constraints in 1d systems, 940",),
        21044: ("systems based on, 210-221", "undecidability of satisfying"),
        22080: ("satisfying constraints, 210–221", "to satisfy constraints, 343, 941"),
    },
    "one_dimensional_language_routes": {
        21189: ("finite complement languages, 941", "2d generalizations, 959"),
        22144: ("subshifts of finite type", "2d generalizations of, 959"),
    },
    "T32_template_tiling_routes": {
        21050: ("corner-overlapping patterns, 941",),
        22150: ("templates", "for 2d constraints, 941", "in tilings, 213"),
        22291: ("tilings, 211–221",),
        22380: ("two-dimensional cellular automata", "template numbering, 941"),
    },
    "sibling_spin_and_substitution_routes": {
        22134: ("spin systems", "as systems based on constraints, 944"),
        22146: ("substitution systems", "systems based on constraints, 942"),
    },
}
INDEX_CONTINUATIONS = line_set(
    "22293-22302,22304,22306,22308,22310"
)


# The visual plates are hash-routed to the independent asset audit only.  No
# glyph, bitmap color, pattern, rule row, 171-catalog entry, or template-key
# ordering is transcribed here.  Text/code independently supplies the strict
# shape and numeric codec.
VISUAL_ONLY_BOUNDARY = (
    "native-example-template-glyphs",
    "native-example-solution-pixels",
    "complete-171-pattern-catalog",
    "notes-rendered-32-template-key",
    "T31-and-T33-sibling-plates",
    "relation-and-observer-plates",
)


LOCAL_CORRUPT_ALLOWED_PATTERN = r"$t_1/t_2/t_3$"
LOCAL_CORRUPT_TEMPLATE = (
    r"\{\{-, 1, -\}, \{0, 0, 1\}, \{-, 0, -\}\}"
)
BOOK_CARDINAL_OFFSETS = ((-1, 0), (0, -1), (0, 0), (0, 1), (1, 0))
EXPECTED_ENU_OFFSETS = ((0, 1), (-1, 0), (0, 0), (1, 0), (0, -1))
EXPECTED_ENU_NAMES = ("N", "W", "C", "E", "S")


EXPECTED_QUERY = {
    "Q00": (2, 2, 0, "5cf212572c40500ba656d1c14b6b82e81c0cf6ab8e414ce39f75fc0559ffa474"),
    "Q01": (2, 2, 0, "b7b6c1a1e150abf46e3c24faf2c502f3102b791630b80de35360d99a549c713e"),
    "Q02": (1, 1, 0, "1483c82372b98e6864d52a9e4a66c92ac7b568d7f2ffca7f405ea0853af10e89"),
    "Q03": (3, 3, 0, "f2caf630dc36b99412a7125672bbfde23f143cc1514b9e5d08af098e56c97a5f"),
    "Q04": (2, 2, 0, "6228103e94133d4564f55d3c2e99afe332cc83d92cbbea8ed2cccb757a4ab7a3"),
    "Q05": (4, 4, 0, "d7726dbcbf2c48583f00e46e5debcefeeb56c53852e12df02ff91d3835d23c03"),
    "Q06": (4, 4, 0, "95204445677f456dc9ecb1108b3875ebe6c79ba050dd0fcd4e8a50e14013c9c3"),
    "Q07": (1, 1, 0, "37a88294d68fdcad0a8292bee384e96616f4f66d4ff7cd25668d017bf1c7fd1d"),
    "Q08": (3, 3, 0, "073913f6e855aabe72651166f01b145f56b71b5f3cd60748823d77e3976d47d0"),
    "Q09": (1, 1, 0, "0d89b2b31f97c14550cbb4dce99493abcd983962abddc28ee00e42b5b19556d7"),
    "Q10": (4, 4, 0, "74c28d10187266370dd3315ce688d82abf3b4b887569322c1985ca50e4a1b7d9"),
    "Q11": (4, 4, 0, "2576deac9b63e588d97580909309dd906bc1edade9a1105004fded141771c74e"),
    "Q12": (3, 3, 0, "95e3201d510661f8e12ea8ff778cce1956c142ef1af1852390502c2287615a41"),
    "Q13": (2, 2, 0, "b6487eeadc023158d63e2f3f5f87d8217eb78cd22b4c26d118a39e7bdd85234f"),
    "Q14": (3, 3, 0, "e78350c758070ad49c59516edaebfe2f45bf1496833bce4c3de12f907297fce2"),
    "Q15": (4, 4, 0, "734f8c92823fc29b0a45fb959e72e33d48c8e8608b08cee0b3a1f8ada9935294"),
    "Q16": (5, 3, 2, "04ec3566d8a2f16485346198aa70237e35af95c27ff79b151b89763f783e7047"),
    "Q17": (2, 2, 0, "89db2eba8239f1abe2f23bc1992cdccff4a765e987dbe8f533285f913e99d43d"),
    "Q18": (2, 2, 0, "8e4b00d5329cd732d94e3223af87bd9f839983f7b8d1356d2e93393068930474"),
    "Q19": (3, 3, 0, "e908d52e75e3c47d252cf206b3c3306f5006e6cccb5315500f044f66ee46e8be"),
    "Q20": (4, 4, 0, "116eddcbd978b9193b877cb54568c69f3a139585f90caf4445c1f81dcd91c322"),
    "Q21": (2, 0, 2, "4f7f2f63cd5ab998832114ddd71342282c0a62c002f3d804ffed7c3096a9eb0a"),
    "Q22": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q23": (17, 16, 1, "1bcbe693d218b40cf78515ea2b869275b8878c4e2b9221d6cd3bece14bba9613"),
    "Q24": (3, 3, 0, "1ad16efbcc4d45b5ec64d3521f682c0e8fe97aa2f487b5794a491964fc1ee867"),
    "Q25": (2, 2, 0, "36caf6dd934b8a3fbfb06912efb5c582a858d528bc15c6adbcc08720a0104b10"),
    "Q26": (3, 3, 0, "a6dff00e911234e0530769ca7d28178ce9211be0594bd876ce2cf1ad9b6ae510"),
    "Q27": (4, 4, 0, "21b3a6a66711c2b333c63dc2883d4b693f4b0aee3f44d411a82fce307533dd14"),
    "Q28": (2, 0, 2, "4f7f2f63cd5ab998832114ddd71342282c0a62c002f3d804ffed7c3096a9eb0a"),
    "Q29": (17, 15, 2, "e20f31a102695f2d3dae11df65b55d215b9d7721f6e3fc321e80facb1a4f8fb0"),
    "Q30": (1, 1, 0, "5175c49e0f8899350452c178dc36b5d617354e67def675d9be70ac870e30edc9"),
    "Q31": (11, 11, 0, "c505c11bb682207b6285e73020b8e8f9d7543566e59fe76d43c05ef01c7f44e7"),
    "Q32": (1, 1, 0, "484bd41058fa7d44453b24cea344cc9bb864f7cd4a210ba1349a42f6bb67700e"),
    "Q33": (3, 0, 3, "a38e54e96c4488d31540f2ba1c728174a26c8990fe421acb639e8dcd7f8fb11c"),
    "Q34": (2, 0, 2, "47665fb901a7490b55545bc8a22c216c83b5476bf01cd63e03bbad689d2156b2"),
    "Q35": (1, 0, 1, "6260c5396105f84a82abe20a2dc8e5d4621e94d4d2f4c9e084cc2d58006a0901"),
    "Q36": (2, 2, 0, "4cde4076dbc89c3533e8674e944a8f27a341850407e22e6348fbb8ad979c4889"),
}

EXPECTED_SET = {
    "union": (81, "ef727403fc33960d3c5d157d13d38e2164305db8379448ccd0eb3d0a42f2d37c"),
    "pre_index_union": (69, "2e2215ea2a34075fd617ddac4086f7636b9141da6fd152f207748dc32efacea3"),
    "index": (12, "ec6480c4f94ddff516e90bdea8f03616ab88c04172b91c3f171e6941aff40865"),
    "matched_retained": (67, "009ead3e814474d4fb5a3b8b0a6d2986d8e7a1d36203cdeff162fdd132bdd4ce"),
    "governed_continuations": (72, "8d05a92368b89ef22ae35d8bb68bc4e22d67ed91d81513c6eaaa503ad72d90c0"),
    "retained": (139, "7da00714ad1cfe85053a88c355d0bd57122fb349473e21774cdf0c145d7fc920"),
    "excluded": (2, "0b8c44fbe9cc6024183a91950d93293221a00ae51b16e139156854a4228c0a77"),
    "native": (18, "7594896d68d77de7b8f37f988848a98790dc98c247aff9ab3f493805c1c33858"),
    "relation": (59, "9ed35b1ebf068735c52af6be3a8248b97eb8dfd3e19cf3513c5fbdb6e074efd2"),
    "control": (62, "bbf6518c64905b5bb18d297d896b392b6ddedcfb0b5b470eb087cd49753cf618"),
    "candidate_images": (44, "1b8c95f829ccff1bf5d5695a063d3961e5cf408748fc3a7bf3913179e5bc2991"),
    "governed_images": (25, "743d34a350e9769ac23e71deb35b8bdb6540c9489e72e614f9ebed2fc38be137"),
    "excluded_images": (19, "644fa7352dc6ce543692370a8e8381d1aa6cbbc6d29482bbdc685f75b869ef8b"),
}

EXPECTED_EXCLUDED_CLASS = {
    "bare_page_941_debruijn_relations": (
        2,
        "0b8c44fbe9cc6024183a91950d93293221a00ae51b16e139156854a4228c0a77",
    ),
}
EXPECTED_INDEX_CLASS = {
    "solver_and_constraint_routes": (
        4,
        "e7955e6aaaa02893e0808c25a1976ed85f049ed48d22bfba10ba69fef0563c27",
    ),
    "one_dimensional_language_routes": (
        2,
        "e9477cb01ebf8fd4bc6ff36d9a69e0d81af14f21ab1f935be220d2882da15c8f",
    ),
    "T32_template_tiling_routes": (
        4,
        "98fe93e69afbd322d5aa6982e735d1ee196ae02fc2a23f39119502522e784045",
    ),
    "sibling_spin_and_substitution_routes": (
        2,
        "652197ba4bfd4fa73c7ef5895aa82ceb1223c7f6df5571458699602ace14ff71",
    ),
}
EXPECTED_INDEX_GUARDS = (
    12,
    "7d34b8d5bd4408e99bbc91f5331a6f0e86346cce55c36db521a639ddda340000",
)
EXPECTED_INDEX_CONTINUATIONS = (
    14,
    "e51f10f5a7a066fac014e2205812a5db899745ecfdf4a16ba63890274a3a7df8",
)
EXPECTED_IMAGE_PARTITION = {
    "native": (
        4,
        "116eddcbd978b9193b877cb54568c69f3a139585f90caf4445c1f81dcd91c322",
    ),
    "relation": (
        10,
        "cdbd2bf11dc7e9213616c88d549f75c1292c4ec8d8f09a8017a72a3833ce8794",
    ),
    "control": (
        11,
        "5c7facca1e5a926412a17acea675e58032a5680629a9008e094e56237b3b0c8e",
    ),
}
EXPECTED_VISUAL_ONLY_BOUNDARY = (
    6,
    "52933c22ebc7b4868e41797734eab33d2a324372ba3b40848164d9ced7267547",
)

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = (
    "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
)
EXPECTED_SPLIT_MANIFEST_DIGEST = (
    "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
)

# Filled from the independently recomputed reverse joins below.  These values
# bind both exact duplication and normalized one-to-one provenance witnesses.
EXPECTED_SPLIT_QUERY = (
    81,
    "c2f4dbcfef108d45b5713ce6295b45b3e7adfabc64c57d8e74a13fc837bbb145",
)
EXPECTED_SPLIT_QUERY_EXACT = (
    72,
    "7e940e324929ebddac50095dddfc1d9bc9efdac8746d5d1aecc35779a83fd580",
)
EXPECTED_SPLIT_QUERY_NONEXACT = (
    9,
    "bec8940b39c59c8891c7f9ab9bbda6df120ced4a5885fd6eebb2dbb9ebed1c32",
)
EXPECTED_SPLIT_QUERY_MAPPING = (
    9,
    "74462d069019f277540e2695bff55714c5ebe95667e75a971f21327db856cf2a",
)
EXPECTED_SPLIT_RETAINED_EXACT = (
    107,
    "9f54eba108226aa196fcab88ab5625e40157611efc962e0736a152284b994fd8",
)
EXPECTED_SPLIT_RETAINED_NONEXACT = (
    32,
    "855c4ddc2779f4e79f9e62e365a28748cee630356da9b8f90cdde0f2ebe5fd7f",
)
EXPECTED_SPLIT_RETAINED_MAPPING = (
    32,
    "166dcd0f2f2b3d55d2161f901a1620e78168aa50c6494b91809faee8622c7ae1",
)
EXPECTED_MONOLITH_ONLY = (
    0,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
)
EXPECTED_ATLAS_HITS = (
    2,
    "dd39606da577b951d544e3e059f492e5932d034f4cd462fcb22e29b1a77f93ed",
)

SOURCE_MODEL_RECORDS = (
    "category:declarative model-set relation, not transition evolution",
    "strict-domain:static discrete 2D total field with no time axis",
    "strict-alphabet:binary ordered symbols 0,1",
    "strict-footprint:raw sorted Book row,column cross plus explicit ENU basis codec",
    "strict-clause:exact oriented five-symbol assignment",
    "strict-allowed:finite set drawn from all 32 assignments",
    "satisfaction:every translated footprint assignment is allowed",
    "overlap:translated reads share one underlying field",
    "symmetry:rotation/reflection/color exchange are catalog quotients only",
    "code:source-derived 32-bit mask over descending binary assignments",
    "models:possibly empty and not restricted to periodic witnesses",
    "periodic:presentation/witness property, not finite boundary policy",
    "checker:external finite MatchQ verification over overlapping 3x3 windows",
    "search:external square-spiral/backtracking/query algorithm",
    "compatibility-screen:eight-position test is enumeration pruning, not model data",
    "T31-boundary:center-conditioned neighbor counts lose orientation",
    "T33-boundary:global required occurrence is an additional relation",
    "extension:larger complete templates and more finite colors are source-backed",
    "execution:no seed/frontier/write/update/successor/runner branch",
)
EXPECTED_SOURCE_MODEL = (
    18,
    "23a617037c8f508dc2e16b21eb4d12dd0c5cdda10bb9d26e32709bacccd964a1",
)


def digest(values: set[int] | frozenset[int]) -> str:
    payload = ",".join(map(str, sorted(values))).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def digest_records(records: set[str] | list[str] | tuple[str, ...]) -> str:
    payload = "\n".join(sorted(records)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def fixed_binary_digits(number: int, width: int) -> tuple[int, ...]:
    if number < 0 or number >= 1 << width:
        raise ValueError("number does not fit declared width")
    return tuple((number >> shift) & 1 for shift in range(width - 1, -1, -1))


def proof_template_universe() -> frozenset[tuple[int, ...]]:
    """All strict assignments, independent of the unrecovered raster order."""

    return frozenset(itertools.product((0, 1), repeat=len(BOOK_CARDINAL_OFFSETS)))


def source_template_catalog() -> tuple[tuple[int, ...], ...]:
    """BOOK:13513-20 order, independently cross-referenced to page 941."""

    ascending = tuple(itertools.product((0, 1), repeat=len(BOOK_CARDINAL_OFFSETS)))
    return tuple(reversed(ascending))


def allowed_catalog_positions(number: int) -> frozenset[int]:
    """One-based positions selected by the source mask, not template values."""

    digits = fixed_binary_digits(number, 32)
    return frozenset(index for index, digit in enumerate(digits, 1) if digit)


def constraint_number_from_positions(positions: frozenset[int]) -> int:
    if not positions <= frozenset(range(1, 33)):
        raise ValueError("catalog position is outside 1 through 32")
    digits = tuple(int(index in positions) for index in range(1, 33))
    return sum(digit << (31 - index) for index, digit in enumerate(digits))


def allowed_from_constraint_number(number: int) -> frozenset[tuple[int, ...]]:
    catalog = source_template_catalog()
    return frozenset(catalog[index - 1] for index in allowed_catalog_positions(number))


def constraint_number_from_allowed(allowed: frozenset[tuple[int, ...]]) -> int:
    catalog = source_template_catalog()
    universe = frozenset(catalog)
    if not allowed <= universe:
        raise ValueError("allowed set contains a non-cross assignment")
    positions = frozenset(
        index for index, template in enumerate(catalog, 1) if template in allowed
    )
    return constraint_number_from_positions(positions)


def book_row_column_to_enu(offset: tuple[int, int]) -> tuple[int, int]:
    """Explicit basis map: Book array (row,column) to ENU (x,y)."""

    row, column = offset
    return column, -row


def periodic_cross_read(
    fundamental: tuple[tuple[int, ...], ...], row: int, column: int
) -> tuple[int, ...]:
    """Read the exact infinite periodic field represented by a rectangle."""

    if not fundamental or not all(fundamental):
        raise ValueError("fundamental rectangle must be nonempty")
    widths = {len(values) for values in fundamental}
    if len(widths) != 1:
        raise ValueError("fundamental rectangle must be rectangular")
    height, width = len(fundamental), len(fundamental[0])
    return tuple(
        fundamental[(row + drow) % height][(column + dcolumn) % width]
        for drow, dcolumn in BOOK_CARDINAL_OFFSETS
    )


def periodic_cross_handles(
    shape: tuple[int, int], row: int, column: int
) -> tuple[tuple[int, int], ...]:
    height, width = shape
    if height <= 0 or width <= 0:
        raise ValueError("periods must be positive")
    return tuple(
        ((row + drow) % height, (column + dcolumn) % width)
        for drow, dcolumn in BOOK_CARDINAL_OFFSETS
    )


def periodic_model_satisfies(
    fundamental: tuple[tuple[int, ...], ...],
    allowed: frozenset[tuple[int, ...]],
) -> bool:
    height, width = len(fundamental), len(fundamental[0])
    return all(
        periodic_cross_read(fundamental, row, column) in allowed
        for row in range(height)
        for column in range(width)
    )


def project_cross_from_3x3(
    template: tuple[tuple[object, object, object], ...],
) -> tuple[object, ...]:
    if len(template) != 3 or any(len(row) != 3 for row in template):
        raise ValueError("adapter requires a 3 by 3 source pattern")
    return (
        template[0][1],
        template[1][0],
        template[1][1],
        template[1][2],
        template[2][1],
    )


def neighbor_count_signature(template: tuple[int, ...]) -> tuple[int, int]:
    north, west, center, east, south = template
    return center, north + west + east + south


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 40-T32-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda line_no: lines[line_no - 1]

    official_raw = OFFICIAL_NOTE_SNAPSHOT.read_bytes()
    official_text = official_raw.decode("utf-8")
    decoded_template_matches = re.findall(
        r"(?m)^Decoded-Template:\n([^\n]+)$", official_text
    )
    decoded_allowed_matches = re.findall(
        r"(?m)^Decoded-Allowed-Pattern:\n([^\n]+)$", official_text
    )
    decoded_checker_matches = re.findall(
        r"(?m)^Decoded-Checker:\n([^\n]+)$", official_text
    )
    official_template = (
        decoded_template_matches[0] if len(decoded_template_matches) == 1 else ""
    )
    official_allowed_pattern = (
        decoded_allowed_matches[0] if len(decoded_allowed_matches) == 1 else ""
    )
    official_checker = (
        decoded_checker_matches[0] if len(decoded_checker_matches) == 1 else ""
    )
    official_ok = (
        hashlib.sha256(official_raw).hexdigest()
        == EXPECTED_OFFICIAL_NOTE_SNAPSHOT_SHA256
        and official_text.count(f"Canonical-URL: {OFFICIAL_NOTE_URL}") == 1
        and official_text.count(
            f"Fetched-Document-SHA256: {EXPECTED_OFFICIAL_NOTE_DOCUMENT_SHA256}"
        )
        == 1
        and official_text.count(OFFICIAL_RAW_ALLOWED_PATTERN_HTML) == 1
        and official_text.count(OFFICIAL_RAW_TEMPLATE_HTML) == 1
        and official_text.count(OFFICIAL_RAW_CHECKER_HTML) == 1
        and official_template == OFFICIAL_DECODED_TEMPLATE
        and official_allowed_pattern == OFFICIAL_DECODED_ALLOWED_PATTERN
        and official_checker == OFFICIAL_DECODED_CHECKER
        and official_text.count("The alternative bars and four Mathematica Blank underscores are copied exactly.")
        == 1
    )

    language_raw = LANGUAGE_SEMANTICS_SNAPSHOT.read_bytes()
    language_text = language_raw.decode("utf-8")
    language_ok = (
        hashlib.sha256(language_raw).hexdigest()
        == EXPECTED_LANGUAGE_SEMANTICS_SNAPSHOT_SHA256
        and language_text.count(
            "Blank-Meta-Description: _ or Blank[] is a pattern object that can stand for any Wolfram Language expression."
        )
        == 1
    )
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
        and official_ok
        and language_ok
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        found = {
            line_no
            for line_no, line in enumerate(lines, 1)
            if re.search(pattern, line, re.IGNORECASE)
        }
        hits[name] = found
        actual = (
            len(found),
            sum(line_no < INDEX_FIRST_LINE for line_no in found),
            sum(line_no >= INDEX_FIRST_LINE for line_no in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY[name]
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index_union = {line_no for line_no in union if line_no < INDEX_FIRST_LINE}
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
        "candidate_images": set(CANDIDATE_IMAGE_LINES),
        "governed_images": set(GOVERNED_IMAGE_LINES),
        "excluded_images": set(EXCLUDED_IMAGE_LINES),
    }
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET[name]
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    excluded_ok = (
        set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS[name]
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    classification_delta = matched_retained ^ set(MATCHED_RETAINED)
    excluded_ok &= not classification_delta
    ok &= excluded_ok
    print(
        "unresolved_pre_index",
        "OK" if excluded_ok else "MISMATCH",
        len(classification_delta),
        *sorted(classification_delta),
    )

    index_ok = (
        set().union(*INDEX_CLASS.values()) == index
        and sum(map(len, INDEX_CLASS.values())) == len(index)
    )
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS[name]
        index_ok &= good
        print(f"index_{name}", "OK" if good else "MISMATCH", *actual)
    guard_records = {
        f"{class_name}:{line_no}:{'|'.join(needles)}"
        for class_name, entries in INDEX_ENTRY_GUARDS.items()
        for line_no, needles in entries.items()
    }
    guards_ok = (
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
        == EXPECTED_INDEX_GUARDS
    )
    continuation_actual = (len(INDEX_CONTINUATIONS), digest(INDEX_CONTINUATIONS))
    continuation_ok = (
        continuation_actual == EXPECTED_INDEX_CONTINUATIONS
        and all(at(line_no).strip() for line_no in INDEX_CONTINUATIONS)
        and "from 2×2 squares, 1078" in at(22293)
        and "undecidability" in at(22310)
    )
    index_ok &= guards_ok and continuation_ok
    ok &= index_ok
    print(
        "index_entry_occurrence_guards",
        "OK" if guards_ok else "MISMATCH",
        len(guard_records),
        digest_records(guard_records),
    )
    print(
        "index_tiling_continuations",
        "OK" if continuation_ok else "MISMATCH",
        *continuation_actual,
    )
    print(
        "unresolved_index",
        "OK" if index_ok else "MISMATCH",
        len(index ^ set(INDEX_ROUTED)),
    )

    derived_images = {
        line_no for line_no in RETAINED if IMAGE_RE.fullmatch(at(line_no))
    }
    image_sets = {
        "native": NATIVE_IMAGE_LINES,
        "relation": RELATION_IMAGE_LINES,
        "control": CONTROL_IMAGE_LINES,
    }
    image_paths_ok = True
    for line_no in CANDIDATE_IMAGE_LINES:
        match = IMAGE_RE.fullmatch(at(line_no))
        image_paths_ok &= match is not None
        if match is not None:
            basename = Path(match.group(1)).name
            image_paths_ok &= len(list(SOURCE_ROOT.rglob(basename))) == 1
    images_ok = (
        derived_images == set(GOVERNED_IMAGE_LINES)
        and sum(map(len, image_sets.values())) == len(GOVERNED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and image_paths_ok
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION[name]
        images_ok &= good
        print(f"images_{name}", "OK" if good else "MISMATCH", *actual)
    visual_actual = (len(VISUAL_ONLY_BOUNDARY), digest_records(VISUAL_ONLY_BOUNDARY))
    visual_ok = (
        visual_actual == EXPECTED_VISUAL_ONLY_BOUNDARY
        and not any("transcription" in record for record in VISUAL_ONLY_BOUNDARY)
        and images_ok
    )
    ok &= visual_ok
    print(
        "governed_image_interface_hash_bound_no_transcription_no_replay",
        "OK" if visual_ok else "MISMATCH",
        len(derived_images),
        digest(derived_images),
        "candidates",
        len(CANDIDATE_IMAGE_LINES),
        digest(CANDIDATE_IMAGE_LINES),
        "excluded",
        len(EXCLUDED_IMAGE_LINES),
        digest(EXCLUDED_IMAGE_LINES),
    )

    local_line = at(14055)
    official_local_template = (
        official_template.replace("{", r"\{").replace("}", r"\}")
    )
    official_local_allowed = "$t_1 | t_2 | t_3$"
    repaired_line = local_line.replace(
        LOCAL_CORRUPT_ALLOWED_PATTERN, official_local_allowed, 1
    ).replace(LOCAL_CORRUPT_TEMPLATE, official_local_template, 1)
    local_checker = " ".join(
        " ".join(at(line_no) for line_no in (14058, 14059, 14060)).split()
    )
    repair_ok = (
        official_ok
        and language_ok
        and local_line.count(LOCAL_CORRUPT_ALLOWED_PATTERN) == 1
        and local_line.count(LOCAL_CORRUPT_TEMPLATE) == 1
        and LOCAL_CORRUPT_ALLOWED_PATTERN.count("/") == 2
        and LOCAL_CORRUPT_TEMPLATE.count("-") == 4
        and "_" not in LOCAL_CORRUPT_TEMPLATE
        and official_template.count("_") == 4
        and official_allowed_pattern.count("|") == 2
        and repaired_line.count(official_local_allowed) == 1
        and repaired_line.count(official_local_template) == 1
        and LOCAL_CORRUPT_ALLOWED_PATTERN not in repaired_line
        and LOCAL_CORRUPT_TEMPLATE not in repaired_line
        and local_checker == official_checker
    )
    ok &= repair_ok
    print(
        "source_hash_bound_official_Blank_alternative_checker_repair",
        "OK" if repair_ok else "MISMATCH",
        EXPECTED_OFFICIAL_NOTE_SNAPSHOT_SHA256,
        EXPECTED_OFFICIAL_NOTE_DOCUMENT_SHA256,
    )

    main_ok = (
        "local arrangement of colors around every cell" in at(2614)
        and "fixed set of possible templates" in at(2614)
        and "templates apply to every cell" in at(2618)
        and "templates of neighboring cells overlapping" in at(2618)
        and "1384774 and 328778790" in at(2618)
        and "4,294,967,296 possible sets" in at(2620)
        and "766,979,044" in at(2620)
        and "3,527,988,252" in at(2620)
        and "set of 171 repetitive patterns" in at(2620)
        and "complete collection of all 171 patterns" in at(2630)
        and "minimal constraint" in at(2630)
        and "Patterns differing by overall reflection, rotation" in at(2630)
    )
    ok &= main_ok
    print("source_strict_oriented_template_model_set", "OK" if main_ok else "MISMATCH")

    notes_ok = (
        "Page 215 · 2D constraints" in at(14048)
        and "removing any of the allowed templates" in at(14048)
        and "differ only by overall rotation, reflection" in at(14048)
        and "total of 32 possible" in at(14048)
        and "Position[IntegerDigits[n, 2, 32], 1]" in at(14050)
        and "compatible with itself or with at least one other" in at(14054)
        and "eight immediately adjacent positions" in at(14054)
        and repair_ok
        and local_checker == OFFICIAL_DECODED_CHECKER
        and "Partition[list, {3, 3}, {1, 1}]" in local_checker
        and "cyclic" not in local_checker.lower()
        and "wrap" not in local_checker.lower()
    )
    ok &= notes_ok
    print(
        "source_notes_allowed_set_overlap_checker_no_periodic_argument",
        "OK" if notes_ok else "MISMATCH",
    )

    offsets_ok = (
        "for 2D 5-neighbor rules" in at(13513)
        and r"\{(-1, 0), \{0, -1\}, \{0, 0\}, \{0, 1\}, \{1, 0\}\}" in at(13513)
        and "offset lists are always taken to be in the order given by *Sort*" in at(13513)
        and "possible neighborhood configurations are" in at(13513)
        and "Reverse[Table[IntegerDigits[i - 1," in at(13516)
        and "k, Length[os]], {i, k^Length[os]}]]" in at(13517)
        and "page 941 for 5-neighbor rules" in at(13520)
        and tuple(map(book_row_column_to_enu, BOOK_CARDINAL_OFFSETS))
        == EXPECTED_ENU_OFFSETS
        and tuple(
            {
                (0, 1): "N",
                (-1, 0): "W",
                (0, 0): "C",
                (1, 0): "E",
                (0, -1): "S",
            }[offset]
            for offset in EXPECTED_ENU_OFFSETS
        )
        == EXPECTED_ENU_NAMES
    )
    ok &= offsets_ok
    print(
        "source_raw_sorted_row_column_offsets_explicit_ENU_codec_page941_order",
        "OK" if offsets_ok else "MISMATCH",
    )

    templates = source_template_catalog()
    codec_ok = (
        offsets_ok
        and len(templates) == len(set(templates)) == 32
        and frozenset(templates) == proof_template_universe()
        and templates[0] == (1, 1, 1, 1, 1)
        and templates[-1] == (0, 0, 0, 0, 0)
        and allowed_catalog_positions(0) == frozenset()
        and allowed_catalog_positions(1) == frozenset({32})
        and allowed_catalog_positions(1 << 31) == frozenset({1})
        and allowed_from_constraint_number(0) == frozenset()
        and allowed_from_constraint_number(1) == frozenset({templates[-1]})
        and allowed_from_constraint_number(1 << 31) == frozenset({templates[0]})
        and constraint_number_from_allowed(frozenset(templates)) == (1 << 32) - 1
        and all(
            constraint_number_from_allowed(allowed_from_constraint_number(number))
            == number
            for number in (0, 1, 2, 3, 1384774, 328778790, (1 << 32) - 1)
        )
        and all(
            constraint_number_from_positions(allowed_catalog_positions(number))
            == number
            for number in (0, 1, 2, 3, 1384774, 328778790, (1 << 32) - 1)
        )
        and len(allowed_from_constraint_number(1384774)) == 8
        and len(allowed_from_constraint_number(328778790)) == 12
        and 1 << len(templates) == 4_294_967_296
    )
    ok &= codec_ok
    print(
        "derived_exact_source_ordered_32_template_mask_codec_no_raster_read",
        "OK" if codec_ok else "MISMATCH",
        len(templates),
        1 << len(templates),
    )

    source_pattern = (
        ("_", 1, "_"),
        (0, 0, 1),
        ("_", 0, "_"),
    )
    projected = project_cross_from_3x3(source_pattern)
    adapter_ok = (
        repair_ok
        and projected == (1, 0, 0, 1, 0)
        and tuple(source_pattern[row][column] for row, column in ((0, 0), (0, 2), (2, 0), (2, 2)))
        == ("_", "_", "_", "_")
        and all(value != "_" for value in projected)
        and len(BOOK_CARDINAL_OFFSETS) == 5
    )
    ok &= adapter_ok
    print(
        "derived_3x3_MatchQ_adapter_projects_four_Blank_corners",
        "OK" if adapter_ok else "MISMATCH",
        projected,
    )

    fundamental = (
        (0, 1, 0, 1),
        (1, 0, 1, 0),
        (0, 1, 0, 1),
        (1, 0, 1, 0),
    )
    periodic_allowed = frozenset(
        periodic_cross_read(fundamental, row, column)
        for row in range(len(fundamental))
        for column in range(len(fundamental[0]))
    )
    handles_here = periodic_cross_handles((4, 4), 0, 0)
    handles_east = periodic_cross_handles((4, 4), 0, 1)
    overlap_ok = (
        periodic_model_satisfies(fundamental, periodic_allowed)
        and len(periodic_allowed) == 2
        and set(handles_here) & set(handles_east)
        and handles_here[3] == handles_east[2]
        and periodic_cross_read(fundamental, 0, 0)[3]
        == periodic_cross_read(fundamental, 0, 1)[2]
    )
    ok &= overlap_ok
    print(
        "derived_one_field_overlapping_translated_reads_periodic_witness",
        "OK" if overlap_ok else "MISMATCH",
        len(periodic_allowed),
        len(set(handles_here) & set(handles_east)),
    )

    north_black = (1, 0, 0, 0, 0)
    west_black = (0, 1, 0, 0, 0)
    count_loss_ok = (
        north_black != west_black
        and neighbor_count_signature(north_black)
        == neighbor_count_signature(west_black)
        == (0, 1)
        and "various numbers of black and white neighbors" in at(2610)
        and "local arrangement of colors" in at(2614)
    )
    ok &= count_loss_ok
    print(
        "derived_T31_histogram_loss_T32_orientation_witness",
        "OK" if count_loss_ok else "MISMATCH",
    )

    all_white = (0, 0, 0, 0, 0)
    all_black = (1, 1, 1, 1, 1)
    local_allowed = frozenset({all_white, all_black})
    white_model = ((0,),)
    required_loss_ok = (
        periodic_model_satisfies(white_model, local_allowed)
        and all_black not in {
            periodic_cross_read(white_model, 0, 0)
        }
        and "particular template from this set must appear at least somewhere" in at(2634)
        and "certain template from this set must occur at least once" in at(2640)
    )
    ok &= required_loss_ok
    print(
        "derived_T33_global_occurrence_strictly_strengthens_T32",
        "OK" if required_loss_ok else "MISMATCH",
    )

    periodic_and_search_ok = (
        "tessellation of 5 x 10 blocks" in at(2618)
        and "tessellation of 24 x 24 blocks" in at(2618)
        and "one of the set of 171 repetitive patterns" in at(2620)
        and "Representing repetitive patterns" in at(14063)
        and "tessellations of rectangles whose corners overlap" in at(14063)
        and "no such direct procedure" in at(2646)
        and "go outside of the system" in at(2646)
        and "build up patterns iteratively" in at(2650)
        and "backtracking" in at(2650)
        and "extend patterns along a square spiral" in at(14080)
        and "formally undecidable" in at(14082)
        and "finite region is NPcomplete" in at(14083)
        and "Systems based on constraints do not have initial conditions" in at(14275)
    )
    ok &= periodic_and_search_ok
    print(
        "source_periodic_presentations_external_search_no_initial_state",
        "OK" if periodic_and_search_ok else "MISMATCH",
    )

    extension_ok = (
        "increase the size of the templates" in at(14097)
        and "increase the number of possible colors for each cell" in at(14097)
        and "3×3 templates with two colors" in at(14097)
        and "complete  $3 \\times 3$  blocks" in at(2680)
        and "only the 33 templates" in at(2684)
        and "out of the 512 possible ones" in at(2684)
        and "only 2×2 arrangements of colors" in at(14109)
        and "51 blocks" in at(14109)
    )
    ok &= extension_ok
    print(
        "source_backed_larger_complete_templates_and_more_colors",
        "OK" if extension_ok else "MISMATCH",
    )

    source_defects_ok = (
        repair_ok
        and " $56.3 \\times 3$  templates" in at(2694)
        and "56 allowed templates" in at(2688)
        and len(at(14105)) == 4254
        and 14105 not in RETAINED
        and 2694 in CONTROL_EVIDENCE
    )
    ok &= source_defects_ok
    print(
        "source_defects_scoped_blank_alternative_T33_typesetting_corrupt_relation",
        "OK" if source_defects_ok else "MISMATCH",
    )

    structural = (
        not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE == RETAINED
        and MATCHED_RETAINED == RETAINED & pre_index_union
        and GOVERNED_CONTINUATIONS == RETAINED - union
        and not RETAINED & index
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    split_paths = sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
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
        "split_manifest",
        "OK" if split_manifest_ok else "MISMATCH",
        len(split_paths),
        digest_records(relative_paths),
        digest_records(manifest),
    )

    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in QUERIES.values()]
    monolith_query_text = {at(line_no) for line_no in union}
    split_records: set[str] = set()
    split_exact: set[str] = set()
    split_nonexact: set[str] = set()
    split_lines: list[tuple[str, str]] = []
    split_texts: set[str] = set()
    split_record_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        split_file_lines = path.read_text(encoding="utf-8").splitlines()
        for line_no, line in enumerate(split_file_lines, 1):
            record = f"{relative}:{line_no}"
            split_lines.append((record, normalized_line(line)))
            split_texts.add(line)
            split_record_text[record] = line
            if not any(rx.search(line) for rx in compiled):
                continue
            split_records.add(record)
            (split_exact if line in monolith_query_text else split_nonexact).add(record)

    monolith_witnesses = [
        (str(line_no), normalized_line(at(line_no))) for line_no in sorted(union)
    ]
    query_mapping: set[str] = set()
    query_mapping_ok = True
    for record in sorted(split_nonexact):
        witness, score = best_witness(split_record_text[record], monolith_witnesses)
        query_mapping.add(f"{record}->{witness}:{score:.6f}")
        query_mapping_ok &= score >= 0.50 and int(witness) in union
    split_query_actual = (len(split_records), digest_records(split_records))
    split_exact_actual = (len(split_exact), digest_records(split_exact))
    split_nonexact_actual = (len(split_nonexact), digest_records(split_nonexact))
    query_mapping_actual = (len(query_mapping), digest_records(query_mapping))
    split_query_ok = (
        split_query_actual == EXPECTED_SPLIT_QUERY
        and split_exact_actual == EXPECTED_SPLIT_QUERY_EXACT
        and split_nonexact_actual == EXPECTED_SPLIT_QUERY_NONEXACT
        and query_mapping_actual == EXPECTED_SPLIT_QUERY_MAPPING
        and query_mapping_ok
    )
    ok &= split_query_ok
    print(
        "split_query_reverse_join",
        "OK" if split_query_ok else "MISMATCH",
        *split_query_actual,
        *split_exact_actual,
        *split_nonexact_actual,
        *query_mapping_actual,
    )

    exact_retained = {line_no for line_no in RETAINED if at(line_no) in split_texts}
    nonexact_retained = set(RETAINED) - exact_retained
    retained_mapping: set[str] = set()
    monolith_only: set[int] = set()
    for line_no in sorted(nonexact_retained):
        witness, score = best_witness(at(line_no), split_lines)
        if score >= 0.50:
            retained_mapping.add(f"{line_no}->{witness}:{score:.6f}")
        else:
            monolith_only.add(line_no)
    exact_retained_actual = (len(exact_retained), digest(exact_retained))
    nonexact_retained_actual = (len(nonexact_retained), digest(nonexact_retained))
    retained_mapping_actual = (len(retained_mapping), digest_records(retained_mapping))
    monolith_only_actual = (len(monolith_only), digest(monolith_only))
    split_retained_ok = (
        exact_retained_actual == EXPECTED_SPLIT_RETAINED_EXACT
        and nonexact_retained_actual == EXPECTED_SPLIT_RETAINED_NONEXACT
        and retained_mapping_actual == EXPECTED_SPLIT_RETAINED_MAPPING
        and monolith_only_actual == EXPECTED_MONOLITH_ONLY
        and len(retained_mapping) + len(monolith_only) == len(nonexact_retained)
    )
    ok &= split_retained_ok
    print(
        "split_retained_reverse_join",
        "OK" if split_retained_ok else "MISMATCH",
        *exact_retained_actual,
        *nonexact_retained_actual,
        *retained_mapping_actual,
        *monolith_only_actual,
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_patterns = (
        re.compile(r"^### Systems Based on Constraints$", re.I),
        re.compile(r"defined by what configurations are allowed", re.I),
    )
    atlas_hits = {
        line_no
        for line_no, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in atlas_patterns)
    }
    atlas_actual = (len(atlas_hits), digest(atlas_hits))
    atlas_ok = (
        len(atlas_lines) == 542
        and atlas_actual == EXPECTED_ATLAS_HITS
        and "Systems Based on Constraints" in atlas_lines[192]
        and "defined by what configurations are allowed" in atlas_lines[194]
    )
    ok &= atlas_ok
    print("atlas_summary_only", "OK" if atlas_ok else "MISMATCH", *atlas_actual)

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[32] == "Template Constraint Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 32. Template Constraint Systems" in taxonomy_text
        and "Each local neighborhood in the final pattern must match one of the allowed templates." in taxonomy_text
        and "Neighbor-count constraints specify totals." in taxonomy_text
        and "Template constraints specify exact allowed local arrangements." in taxonomy_text
        and "required global occurrence" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only", "OK" if catalog_ok else "MISMATCH")

    model_actual = (len(SOURCE_MODEL_RECORDS), digest_records(SOURCE_MODEL_RECORDS))
    architecture_ok = (
        model_actual == EXPECTED_SOURCE_MODEL
        and main_ok
        and notes_ok
        and offsets_ok
        and codec_ok
        and adapter_ok
        and overlap_ok
        and count_loss_ok
        and required_loss_ok
        and periodic_and_search_ok
        and extension_ok
        and source_defects_ok
        and "evolution" not in "\n".join(at(n) for n in range(2614, 2631)).lower()
    )
    ok &= architecture_ok
    print(
        "source_fit_declarative_oriented_template_relation_not_runner",
        "OK" if architecture_ok else "MISMATCH",
        *model_actual,
    )

    unresolved_total = (
        len(classification_delta)
        + len(index ^ set(INDEX_ROUTED))
        + len(monolith_only)
    )
    unresolved_ok = unresolved_total == 0
    ok &= unresolved_ok
    print("unresolved_total", "OK" if unresolved_ok else "MISMATCH", unresolved_total)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
