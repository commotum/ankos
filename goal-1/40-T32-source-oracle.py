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
    "5776,5788,6976,13513,13520,13551,"
    "14040,14044,14047,14063,14099,"
    "14113,14115,14124,14134,"
    "16022,16367,16369,16373"
)
CONTROL_MATCHED = line_set(
    "2568,2590,2596,2600,2608,2610,"
    "2634,2640,2646,2650,2654,2672,2680,2684,2688,2696,"
    "4046,4244,4324,6948,14027,14080,14082,14083,"
    "14145,14146,14275,15207,15930,17431,19816,20769"
)

NATIVE_CONTINUATIONS = line_set("14057,14061")
RELATION_CONTINUATIONS = line_set(
    "2322,5778,5780,5786,6974,"
    "13515-13518,14042,14046,"
    "14065-14067,14069,14071-14078,"
    "14109,14111,14117,14119,14121,14123,"
    "14126,14128,14130,14132,14136,14138,14140,14142,"
    "16371,17463,17465"
)
CONTROL_CONTINUATIONS = line_set(
    "2576,2584,2598,2606,2632,2636,2638,"
    "2642,2644,2648,2652,2656,2658,2660,2662,2664,2666,2668,"
    "2670,2674,2676,2678,2682,2686,2690,2692,2694,2698,"
    "14084,14144"
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
    "2322,5786,6974,14042,14111,14117,14136,14138,14142,17465"
)
CONTROL_IMAGE_LINES = line_set(
    "2576,2584,2598,2606,2638,2662,2670,2682,2686,2690,2692"
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
CARDINAL_OFFSETS = ((-1, 0), (0, -1), (0, 0), (0, 1), (1, 0))


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
