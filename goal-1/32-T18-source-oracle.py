#!/usr/bin/env python3
"""Frozen source-evidence audit for T18 Cyclic Tag Systems.

This is a line-oriented source oracle, not a semantic implementation.  It
freezes the direct name, neighboring aliases, definition, queue mechanics,
cyclic schedule, implementation symbols, generalizations, properties,
history, randomness, initial-condition limits, emulations, universality,
actual Index, and split-source routes used by the T18 audit.

The disposition deliberately follows the SimpleProgram axes.  A cyclic tag
configuration is an ordered word plus visible cyclic rule position; ordinary
tag, substitution, Turing/CA, and rule-110 passages are controls or explicit
relations, not evidence for a separate executor and not native T18 mechanics.
Every query candidate is assigned to a frozen disposition and the unresolved
remainder is required to be empty.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("T18 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = (
    "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
)
EXPECTED_ATLAS_SHA256 = (
    "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
)
EXPECTED_CATALOG_SHA256 = (
    "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
)
EXPECTED_TAXONOMY_SHA256 = (
    "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"
)


# Q00/Q01 saturate the direct and broad tag-family vocabulary.  Q02 follows
# the ordinary/Post/Wang/uniform/multiway boundary names.  Q03--Q05 recover
# the native definition, front/tail geometry, and cyclic rule schedule even
# where a line does not repeat the family name.  Q06 follows every observed
# implementation/compiler symbol.  Q07--Q13 independently close the requested
# generalization, property, history, randomness, initial-condition, emulation,
# and universality routes.  Q14 and Q15 are intentionally broad substitution
# and rule-110 controls; their large residuals are dispositioned below.  Q16
# closes focused Turing/CA tag emulation routes.  Q17 distinguishes the Notes'
# empty-word clause from the physical trough's capacity failure.  Q18 freezes
# an important terminology limitation: ``program counter``, ``trigger
# symbol``, ``deletion number``, and ``appendant`` are not native cyclic-tag
# wording in the Book.  Its only hits are register/practical-computer or Index
# controls.
QUERIES = {
    "Q00": r"\bcyclic[ -]tag systems?\b",
    "Q01": r"\btag(?:[ -])systems?\b",
    "Q02": (
        r"\b(?:ordinary|Post(?:'s)?|uniform|multiway|"
        r"one[- ]element[- ]dependence|first[- ]element"
        r"(?:[- ]dependence)?) tag systems?\b|\blag systems?\b"
    ),
    "Q03": (
        r"\b(?:two possible blocks|rule simply alternates on successive steps|"
        r"cases are used on alternate steps|block can be added at each step|"
        r"blocks? to be used in each case|choice of what block[^.]{0,160}"
        r"does not depend[^.]{0,80}form of the sequence)\b"
    ),
    "Q04": (
        r"\b(?:single element is removed from the beginning|"
        r"first element from the sequence|leftmost ball in the trough is released|"
        r"new block (?:is|of balls to be) added at the (?:right-hand )?end|"
        r"first element[^.]{0,100}is black|element removed is black)\b"
    ),
    "Q05": (
        r"\b(?:alternates? on successive steps|used on alternate steps|"
        r"cycle through a list|complete cycle|rotary element[^.]{0,100}"
        r"which case of the rule|stripe[^.]{0,100}block that can be added "
        r"at that step|blocks? that can be added at successive steps)\b"
    ),
    "Q06": (
        r"\b(?:CTEvolveList|CTStep|CTListStep|CTList|TS1ToCT|CTToR110|"
        r"CTTOR110)\b|RotateLeft\[rules,\s*Length\[list\]\]"
    ),
    "Q07": (
        r"\b(?:more than two blocks|with just one block|"
        r"allow any value for each element|blocks?[^.]{0,100}"
        r"lengths? divisible by n|multiple of six elements long|"
        r"at least one block is added[^.]{0,80}complete cycle)\b"
    ),
    "Q08": (
        r"Count\[Flatten\[rules\],\s*1\]/n-1|\b(?:growth at an average rate|"
        r"grow by an average|growth is by an average|sequences? of limited length|"
        r"first elements on alternate steps|encoded versions grow like fractional powers|"
        r"contains no more than two identical consecutive blocks|overall behavior "
        r"obtained must correspond to a neighbor-independent substitution system)\b"
    ),
    "Q09": (
        r"\b(?:Matthew Cook|William Kolakoski|Emil Post|Hao Wang)\b|"
        r"Map\[Length,\s*Split\[list\]\]"
    ),
    "Q10": (
        r"\b(?:fluctuations? in (?:this )?growth|fluctuations? are shown with "
        r"respect to growth|first elements produced on successive steps|"
        r"elements (?:are|occur in an) (?:again )?(?:un)?correlated|"
        r"frequency of 1.s among the first elements|highly random behavior)\b"
    ),
    "Q11": (
        r"\b(?:initial condition consists of a single black element|"
        r"cannot meaningfully be given infinite random initial conditions|"
        r"cannot readily be given infinite random initial conditions|"
        r"initial condition for the tag system can be converted|"
        r"initial conditions[^.]{0,160}cyclic tag system|"
        r"rules for a cyclic tag system[^.]{0,160}initial conditions)\b"
    ),
    "Q12": (
        r"\bcyclic tag systems?[^.]{0,240}\bemulat(?:e|es|ed|ing|ion)\b|"
        r"\bemulat(?:e|es|ed|ing|ion)\b[^.]{0,240}\bcyclic tag systems?\b|"
        r"\b(?:TS1ToCT|CTToR110|CTTOR110)\b"
    ),
    "Q13": (
        r"\b(?:universal cyclic tag systems?|cyclic tag systems?[^.]{0,180}"
        r"universal|universality of rule 110|proof of the universality of rule 110)\b"
    ),
    "Q14": (
        r"\b(?:neighbor-independent substitution systems?|"
        r"Thue-Morse substitution system|Fibonacci substitution system)\b"
    ),
    "Q15": r"\brule 110\b",
    "Q16": (
        r"\b(?:Turing machines?|cellular automata|cellular automaton)\b"
        r".{0,220}\b(?:cyclic tag|tag system)\b|\b(?:cyclic tag|tag system)\b"
        r".{0,220}\b(?:Turing machines?|cellular automata|cellular automaton)\b"
    ),
    "Q17": (
        r"CTStep.*\\\{\\\}|"
        r"\bsystem will inevitably fail if the trough overflows\b"
    ),
    "Q18": (
        r"\b(?:program counter|trigger symbol|deletion number|appendant|"
        r"append blocks?|cyclic tag machines?|rotating tag systems?|"
        r"periodic tag systems?)\b"
    ),
}

DIRECT_NAME_STREAM_RX = re.compile(
    r"\bcyclic(?:[\s-]+)tag(?:[\s-]+)systems?\b", re.IGNORECASE
)


# Expected tuple: total lines, pre-Index lines, actual-Index lines, line digest.
EXPECTED_QUERY = {
    "Q00": (60, 44, 16, "19bfa01d30875e74f8a1f1e5d952603ce1a014614064b8933db4b41d9fbf349a"),
    "Q01": (111, 81, 30, "6487e6800a0a4deae848669dd04c35233777fa2f6d546ea1f2adfe039a4f3c4c"),
    "Q02": (17, 11, 6, "cd6c7d23750c173db7db79ec5791ff7859bdc62f280ad6e0dbfcf74e3d6a29ad"),
    "Q03": (5, 5, 0, "b2a822628cc858aea84f4540f9355e333257663f2d5e12096cd5d236b6b90588"),
    "Q04": (6, 6, 0, "86a8107947853e8bb7e58db1ec09b5f1f449125b0ba6194cab40d9f4c13d0175"),
    "Q05": (13, 13, 0, "78eb8f69a4787c8929991bb2b5ae17b6647bf8e6134ad81e0f56fc2d2181365a"),
    "Q06": (17, 17, 0, "24cd7db1e5388d578f164b8c992fdf2e219d999785554049c2f4e9a37f218a59"),
    "Q07": (5, 5, 0, "4df7f82bac146ccc7aa94c3bd408cd9f2c26946ea6eae991bf0fcbd9f4f653f2"),
    "Q08": (7, 7, 0, "3c34faef8ed53bf6e6c4d9bbbb9776f04636ff61115606e720e8e6e3c75238a9"),
    "Q09": (21, 20, 1, "809cf0e665230a810576c123c87f7a80baeadb3667436edebc59dffb0e805b72"),
    "Q10": (7, 7, 0, "8c4a64d30689bf6eefd1ab77466559a91fce37e4cb42cce09986f26f6fb15589"),
    "Q11": (8, 8, 0, "98dc70dc51e3dbdca6cc0a86b082252078b781b9ba6286fef57c32bf91880037"),
    "Q12": (24, 21, 3, "fe1d0c639967fd62009d79faf4d25ac34f00d09727dc67917b4559a50fd0eb30"),
    "Q13": (13, 12, 1, "2b6544c26807e6122b39de101f73c99edef914ca1f498c9f1442f4f2779374d4"),
    "Q14": (33, 30, 3, "8c9b2f17e51dcca0aeab19122d2094c92f44dbebe5aa7ca4a4ad517cf1a3a67c"),
    "Q15": (138, 121, 17, "15fc2a5f32e94399f4a6e3bce25d570632835b48e495cb3b5bd374b977af1714"),
    "Q16": (21, 16, 5, "99f037fae4a564b0a16aa45c518e36db3858c5977cae7c5a7cfd36af2e5aa6e8"),
    "Q17": (2, 2, 0, "f43d968fad5842828fda21acb7a21bc2a5366ad6fa19f25af074a3c4fb69cbe9"),
    "Q18": (3, 2, 1, "b1375eef94a690b328ed1283c9d6fcd7e962f39148f023259a2bf4202324b091"),
}


# Native T18 evidence: complete Chapter 3 presentation (including its five
# source-bound images), native Notes implementation, generalized symbol
# multiplicity, mechanical realization, properties, history, and observers.
NATIVE_EVIDENCE = frozenset(range(1134, 1160, 2)) | frozenset(
    {
        12315, 12317, 12320, 12321, 12322, 12323, 12324, 12327,
        12330, 12331, 12332, 12333, 12334, 12337, 12340, 12341,
        12344, 12346, 12348, 12350, 12352, 12354, 12356, 12358,
        12361, 12364,
    }
)

# Explicit relations and derived properties.  The full rule-110 mechanism
# prose and source-bound pictures are retained as an emulation witness, never
# as the native T18 UPDATE.  CTToR110/TS1ToCT are compilers, not callbacks in a
# cyclic-tag runner.
RELATION_EVIDENCE = (
    frozenset(
        {
            8056, 8058, 8062, 8064, 8066, 8068, 8070, 8072, 8074,
            8076, 8078, 8080,
        }
    )
    | frozenset(range(8172, 8273, 2))
    | frozenset(
        {
            13265, 14275, 17236,
            18514, 18517, 18518, 18519, 18520, 18523, 18526, 18527,
            18528, 18530,
            18672, 18674, 18677, 18678, 18679,
            18736, 18738, 18740,
        }
    )
)

# Neighboring constructions retained only to police boundaries: ordinary/Post
# tags, uniform tags as substitution aliases, multiway tags, CA/Turing and
# recursive emulations, and the register/practical-computer uses of "program
# counter".  None becomes native T18 state/update by being retained here.
CONTROL_EVIDENCE = frozenset(
    {
        1108, 1110, 1112, 1114, 1124, 1126, 1132,
        7952, 8032, 8046, 8498, 8500, 11540,
        12249, 12294, 12298, 12311, 12313, 12368, 14016,
        17684, 18215, 18488, 18498,
        18556, 18562, 18568,
        18794, 18804, 18806, 18877,
        18910, 18916, 19294, 19305, 19314, 19324,
    }
)

RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE

EXPECTED_SET = {
    "union": (305, "db3643b42768e2079aa28e248b05aeeb77bcaae4c6e0e610fd080d63ca4ab15c"),
    "pre_index_union": (259, "ec4955e232ed49260218ca482044cd632cadc5bf726366f2cceba763370fc78a"),
    "index": (46, "34dc4b774ced6937c57f069923339c584525ebae542cd59d83678ecb317afaf6"),
    "matched_native": (30, "681a60e12e4d19716fb98aed9cd8489242627374922d385cf728654745735158"),
    "matched_relation": (43, "8303f7eb4e2cc056878823b7fd8071b501fd5d4ef1910e7def32f26fc3705562"),
    "matched_control": (36, "b493dba7189149d3720055fea0548060181cbe44f0cefb76da810ed586f3c589"),
    "governed_continuations": (51, "737ca402165a067d7f14fecba6b8ea0a8dcfd1ed1ff15f538615ef3438ebd57f"),
    "retained": (160, "698fb02434bd7d28565f4dd5c6e8597c079f41d94339374638e9d2a925e7630c"),
    "excluded": (150, "d0a2a1652b2ca5aaf5e897cf236f1d70e790ba28ca009606fa346ce518e64f0b"),
}

# Sequential residual classification.  This is an exhaustive partition of all
# 150 pre-Index candidates not retained above; no generic "unreviewed" bucket
# exists.  Broad rule-110/substitution saturation is useful search control but
# does not make unrelated occurrences T18 evidence.
EXPECTED_EXCLUDED_CLASS = {
    "rule110_background": (102, "e9752c182aea06b2437be7d4c486e3023105f687f426e8e1f67d2c554c5e6e3d"),
    "substitution_background": (23, "2ce84e11735fc1c52ba2f3b96f0ce0b0ef57f9ac391e98937119d5f3118089b9"),
    "tag_family_background": (1, "2f81a3ea330ff8335a8cbd0bf221054d278b0f19b0964b3ac136191f95bef676"),
    "history_background": (15, "a7fe4577c1ca2f96366af523f411dc6167dceecf5b69cf03a0fe1e9d99030f26"),
    "context_false_positive": (9, "b31ac5eb17732a22d556b1fe3d1b327333aa99ecdeda8567ce72508d8d616850"),
}


INDEX_T18_ROUTES = frozenset(
    {
        20908, 20957, 21050, 21068, 21187, 21233, 21420, 21515,
        21683, 21893, 22134, 22136, 22144, 22150, 22279, 22390,
    }
)
EXPECTED_INDEX_CLASS = {
    "t18_routes": (16, "f28ca632f946d2ccbfd28b2110ee1a0f87cb458308de89e3bfe19f04868f1a45"),
    "tag_controls": (16, "68ad52ebc863632820cf12b14e357ddc86f9395754fdca12f0fbe390581bbcdb"),
    "substitution_controls": (2, "bf0a59374ef9f20be3901c02e3cb74309bb47c6f8c0cc93070899e995e84fee4"),
    "rule110_background": (11, "67a2d59d98634b16a8544188f7758f1711236718c2c9cc8ae5d549685d27789a"),
    "history_background": (1, "01bacc5e93c75bfe8d649a5cd4d5f921d04b12d505ed1895d481a68d9136afbe"),
    "other_background": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}


EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = (
    "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
)
EXPECTED_SPLIT_MANIFEST_DIGEST = (
    "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
)
EXPECTED_SPLIT_QUERY_RECORDS = (
    302,
    "eefde3b65b5fb97ca3a4c52a3d6addd9d8df2f36b4c1e382d18e1cede5acfa96",
)
EXPECTED_SPLIT_EXACT_QUERY_RECORDS = (
    269,
    "7ded0f714fdf9f2d971d0e9cb57f4638e47c85d4c43971ea2f10cdf249202b35",
)

# Every query-bearing split line that is not byte-for-byte equal to a queried
# monolith line is reverse-joined here.  Multi-target tuples denote split lines
# that merge prose separated by a monolith image or line break.
SPLIT_NONEXACT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:1894": (19337,),
    "BACK-MATTER/Colophon/Colophon.md:5049": (22494,),
    "BACK-MATTER/Index/Index.md:11": (12099,),
    "BACK-MATTER/Index/Index.md:48": (12136,),
    "BACK-MATTER/Index/Index.md:154": (12249,),
    "BACK-MATTER/Index/Index.md:203": (12298,),
    "BACK-MATTER/Index/Index.md:259": (12356,),
    "CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md:689": (7278,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:251": (7952,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:321": (8022,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:361": (8066, 8080),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:371": (8076,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:437": (8148,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:441": (8152,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:443": (8154,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:493": (8204, 8210),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:551": (8266,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:587": (8302,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:601": (8318,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:609": (8326,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:613": (8330,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:665": (8384,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:687": (8406,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:731": (8452,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:779": (8504,),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:823": (8556,),
    "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md:99": (8710,),
    "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md:263": (8880,),
    "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md:87": (498,),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:425": (1108, 12294),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:315": (1856,),
    "CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md:275": (2978,),
    "FRONT-MATTER/Preface/Preface.md:52": (136,),
}
EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST = (
    "d1c7c63f615bd2e4d728c79540ea2532ac1f899d1a019d7c3ffde229c4e7d0b2"
)
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = (
    "8965e742cbf76876a00bff50696c9395f779e158bacd3288fc1b716cce642e0f"
)

EXPECTED_SPLIT_DIRECT_NAME_PATHS = frozenset(
    {
        "BACK-MATTER/Colophon/Colophon.md",
        "BACK-MATTER/Index/Index.md",
        "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md",
        "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md",
    }
)
EXPECTED_SPLIT_DIRECT_NAME_PATHS_DIGEST = (
    "cf4388b9033b27000c135eee151600cb542b018a9af015265174d3355e6a1eaa"
)
EXPECTED_SPLIT_DIRECT_COUNTS_DIGEST = (
    "72ef4c18f58ded4667dab34b39f976ae81c53b13bebd1267b59dedeb61b2776a"
)

EXPECTED_EXACT_RETAINED_MIRRORS = (
    125,
    "8ade7cf4df5c5491de27d983dfaa907dd99624a2f58af979b59cf322d7c2218d",
)
SPLIT_NONEXACT_RETAINED = frozenset(
    {
        1140, 1142, 1146, 1152, 1156, 7952,
        8062, 8066, 8068, 8070, 8074, 8076, 8080,
        8180, 8182, 8184, 8186, 8190,
        8204, 8206, 8210, 8226, 8228, 8232, 8236, 8240, 8242,
        8260, 8266,
        12249, 12298, 12313, 12348, 12356, 18738,
    }
)
EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST = (
    "1b7149da9d6de280e7b14d17313405087629b367885e39d53843a4fee72d1d40"
)
MONOLITH_ONLY_RETAINED = frozenset({12348})
SPLIT_NONEXACT_RETAINED_WITNESSES = {
    1140: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:457",
    1142: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:459",
    1146: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:463",
    1152: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:469",
    1156: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:473",
    7952: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:251",
    8062: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:357",
    8066: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:361",
    8068: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:363",
    8070: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:365",
    8074: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:369",
    8076: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:371",
    8080: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:361",
    8180: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:469",
    8182: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:471",
    8184: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:473",
    8186: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:475",
    8190: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:479",
    8204: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:493",
    8206: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:495",
    8210: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:493",
    8226: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:513",
    8228: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:515",
    8232: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:519",
    8236: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:523",
    8240: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:527",
    8242: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:513",
    8260: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:545",
    8266: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:551",
    12249: "BACK-MATTER/Index/Index.md:154",
    12298: "BACK-MATTER/Index/Index.md:203",
    12313: "BACK-MATTER/Index/Index.md:218",
    12356: "BACK-MATTER/Index/Index.md:259",
    18738: "BACK-MATTER/Colophon/Colophon.md:1295",
}
EXPECTED_SPLIT_RETAINED_WITNESS_RECORDS_DIGEST = (
    "66e675a0d5b4111866852360551dfcc6db126112f1cd4c46ce100e2fc936391e"
)
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = (
    "8aaf51d301ea5625023a4fc3665afcf5faf700a27f43c38a89395f9254234953"
)


EXPECTED_ATLAS_LINES = 542
EXPECTED_ATLAS_QUERY_LINES = frozenset({7, 97, 99, 101, 231, 465, 467, 469, 471})
EXPECTED_ATLAS_QUERY_DIGEST = (
    "36518fd6786946eb6c197e37c5515d9dad546d629805b4a202b84b4ae9595400"
)


def digest(lines: set[int] | frozenset[int]) -> str:
    payload = ",".join(map(str, sorted(lines))).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    payload = "\n".join(sorted(records)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def classify_residual(
    candidates: set[int], hits: dict[str, set[int]]
) -> dict[str, set[int]]:
    """Assign every non-retained pre-Index candidate exactly once."""

    remaining = set(candidates)
    classes: dict[str, set[int]] = {}
    routes = (
        ("rule110_background", hits["Q15"]),
        ("substitution_background", hits["Q14"]),
        ("tag_family_background", hits["Q01"] | hits["Q02"] | hits["Q16"]),
        ("history_background", hits["Q09"]),
    )
    for name, route in routes:
        classes[name] = remaining & route
        remaining -= classes[name]
    classes["context_false_positive"] = remaining
    return classes


def classify_index(index: set[int], hits: dict[str, set[int]]) -> dict[str, set[int]]:
    """Assign every actual-Index candidate exactly once."""

    remaining = set(index)
    classes: dict[str, set[int]] = {}
    routes = (
        ("t18_routes", hits["Q00"]),
        ("tag_controls", hits["Q01"] | hits["Q02"] | hits["Q16"] | hits["Q18"]),
        ("substitution_controls", hits["Q14"]),
        ("rule110_background", hits["Q15"]),
        ("history_background", hits["Q09"]),
    )
    for name, route in routes:
        classes[name] = remaining & route
        remaining -= classes[name]
    classes["other_background"] = remaining
    return classes


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 32-T18-source-oracle.py [BOOK]")
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
        and len(DIRECT_NAME_STREAM_RX.findall(text)) == 81
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        found = {n for n, line in enumerate(lines, 1) if rx.search(line)}
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
    matched_native = pre_index_union & NATIVE_EVIDENCE
    matched_relation = pre_index_union & RELATION_EVIDENCE
    matched_control = pre_index_union & CONTROL_EVIDENCE
    matched_retained = matched_native | matched_relation | matched_control
    governed_continuations = set(RETAINED) - union
    excluded = pre_index_union - RETAINED
    sets = {
        "union": union,
        "pre_index_union": pre_index_union,
        "index": index,
        "matched_native": matched_native,
        "matched_relation": matched_relation,
        "matched_control": matched_control,
        "governed_continuations": governed_continuations,
        "retained": set(RETAINED),
        "excluded": excluded,
    }
    for name, values in sets.items():
        expected_count, expected_digest = EXPECTED_SET[name]
        good = len(values) == expected_count and digest(values) == expected_digest
        ok &= good
        print(name, "OK" if good else "MISMATCH", len(values), digest(values))

    excluded_classes = classify_residual(excluded, hits)
    excluded_ok = (
        set().union(*excluded_classes.values()) == excluded
        and sum(map(len, excluded_classes.values())) == len(excluded)
    )
    for name, values in excluded_classes.items():
        expected_count, expected_digest = EXPECTED_EXCLUDED_CLASS[name]
        good = len(values) == expected_count and digest(values) == expected_digest
        excluded_ok &= good
        print(
            f"excluded_{name}",
            "OK" if good else "MISMATCH",
            len(values),
            digest(values),
        )
    ok &= excluded_ok
    print("unresolved_pre_index", "OK" if excluded_ok else "MISMATCH", 0)

    index_classes = classify_index(index, hits)
    index_ok = (
        set().union(*index_classes.values()) == index
        and sum(map(len, index_classes.values())) == len(index)
        and index_classes["t18_routes"] == INDEX_T18_ROUTES
    )
    for name, values in index_classes.items():
        expected_count, expected_digest = EXPECTED_INDEX_CLASS[name]
        good = len(values) == expected_count and digest(values) == expected_digest
        index_ok &= good
        print(
            f"index_{name}",
            "OK" if good else "MISMATCH",
            len(values),
            digest(values),
        )
    ok &= index_ok
    print("unresolved_index", "OK" if index_ok else "MISMATCH", 0)

    # The Book directly establishes visible cyclic control and queue geometry.
    # CTEvolveList carries {rules, word}; both nonempty CTStep clauses rotate
    # the rule list, while the current front symbol controls emission.  This is
    # a state factor and one coupled transition, not hidden executor memory.
    # The black-branch transcription at BOOK:12323 is damaged and has no ':=';
    # its exact output is therefore recovered from prose/assets, not invented
    # from this OCR fragment.  BOOK:12324 directly records the Notes' empty-word
    # self-loop/reference totalization.
    native_semantics_ok = (
        at(1134) == "#### Cyclic Tag Systems"
        and "ordinary tag system" in at(1136)
        and "underlying rule already specify exactly what block can be added at each step" in at(1136)
        and "two possible blocks" in at(1138)
        and "rule simply alternates on successive steps" in at(1138)
        and "adding a block at a particular step when the first element" in at(1138)
        and "single element is removed from the beginning" in at(1144)
        and "new block is added at the end whenever the element removed is black" in at(1144)
        and "same nested form as the third neighbor-independent substitution system" in at(1148)
        and "fluctuations in this growth" in at(1150)
        and "initial condition consists of a single black element" in at(1154)
        and "average rate of half an element per step" in at(1158)
        and at(12315) == "#### Cyclic Tag Systems"
        and "rules for the cyclic tag system on page 95 given as {{1, 1}, {1, 0}}" in at(12317)
        and at(12320) == "CTEvolveList[rules_, init_, t_] :="
        and "NestList[CTStep, {rules, init}, t]" in at(12321)
        and at(12322) == "CTStep[{{r_, s___}, {0, a___}}] := {{s, r}, {a}}"
        and at(12323).startswith("CTStep[\\{\\{r_")
        and ":=" not in at(12323)
        and at(12324) == "CTStep[\\{u_{-}, \\{\\}\\}] := \\{u, \\{\\}\\}\\}"
        and "RotateLeft[rules, Length[list]]" in at(12333)
        and "Position[list, 1]" in at(12334)
        and "list of more than two blocks" in at(12337)
        and "With just one block the behavior is always repetitive" in at(12337)
        and "allow any value for each element" in at(12337)
        and at(12340).startswith("CTStep[{{r_, s___}, {n_, a___}}]")
        and "Table[r, {n}]" in at(12341)
        and "rotary element that determines which case of the rule" in at(12346)
        and "system will inevitably fail if the trough overflows" in at(12346)
        and "Count[Flatten[rules], 1]/n-1" in at(12350)
        and "all blocks in a cyclic tag system with n blocks have lengths divisible by n" in at(12352)
        and "rules for the relevant substitution system may however depend on the initial conditions" in at(12352)
        and "Thue-Morse substitution system" in at(12354)
        and "growth is by an average" in at(12356)
        and "frequency of 1's" in at(12356)
        and "Matthew Cook in 1994" in at(12358)
        and "Map[Length, Split[list]]" in at(12358)
        and "does not repeat" in at(12364)
        and hits["Q17"] == {12324, 12346}
    )
    ok &= native_semantics_ok
    print("native_semantics", "OK" if native_semantics_ok else "MISMATCH")

    # Relations remain typed relations.  Restricted CT/substitution agreement,
    # CT->ordinary-tag->Turing->CA chains, and rule-110 compilation do not
    # replace the native axes or add a family executor.  The multiple-of-six
    # condition belongs to one rule-110 encoding and is explicitly repaired by
    # a CT-to-CT compiler that can represent any cyclic tag system.
    relation_boundary_ok = (
        "cyclic tag system to emulate an ordinary tag system" in at(8058)
        and "rules depend only on the very first element" in at(8058)
        and "cyclic tag system can successfully emulate any cellular automaton" in at(8080)
        and "removing the first element" in at(8192)
        and "adding a new block of elements to the end" in at(8192)
        and "choice of what block" in at(8192)
        and "does not depend in any way on the form of the sequence" in at(8192)
        and "complete emulation of a cyclic tag system using rule 110" in at(8220)
        and "multiple of six elements long" in at(8270)
        and "emulates any other cyclic tag system" in at(8272)
        and "cannot meaningfully be given infinite random initial conditions" in at(13265)
        and "ordinary and cyclic tag systems" in at(14275)
        and "encoded versions grow like fractional powers" in at(17236)
        and "slight analogy with cyclic tag systems" in at(17684)
        and "constructs a cyclic tag system emulating it" in at(18514)
        and at(18517).startswith("TS1ToCT[")
        and "proof of the universality of rule 110" in at(18530)
        and "rules for a cyclic tag system" in at(18674)
        and "initial conditions in rule 110 which will emulate it" in at(18674)
        and at(18677).startswith("CTToR110[")
        and "definition of TS1ToCT" in at(18740)
        and "emulate any one-element-dependence tag system" in at(18740)
        and "tagged onto the end" in at(1112)
        and "uniform tag systems" in at(12249)
        and "neighbor-independent substitution systems" in at(12249)
        and "Multiway tag systems" in at(19324)
        and "list of strings at each step" in at(19324)
    )
    ok &= relation_boundary_ok
    print("relation_boundaries", "OK" if relation_boundary_ok else "MISMATCH")

    # Taxonomy language is useful as a typed role description but is not a
    # quote from the Book.  The Book exposes the role structurally by rotating
    # `rules` inside the complete state.  It never uses the queried API jargon
    # natively for cyclic tags.
    terminology_ok = (
        hits["Q18"] == {12368, 18215, 21819}
        and "register machine" in at(12368)
        and "program counter" in at(12368)
        and "practical computers" in at(18215)
        and "Program counter 678-689, 1116" in at(21819)
        and not re.search(QUERIES["Q18"], "\n".join(at(n) for n in NATIVE_EVIDENCE), re.I)
    )
    ok &= terminology_ok
    print("terminology", "OK" if terminology_ok else "MISMATCH")

    index_text_ok = (
        "Cyclic tag systems, 95" in at(21068)
        and "emulated by rule 110, 678" in at(21068)
        and "emulating cellular automata, 668" in at(21068)
        and "emulating tag systems, 669, 1116" in at(21068)
        and "generalizations of, 895" in at(21068)
        and "implementation of, 895" in at(21068)
        and "mechanical version of, 895" in at(21068)
        and "random initial conditions in, 949" in at(21068)
        and "Tag systems, 93–94 cyclic, 95" in at(22150)
        and "see also Cyclic tag systems" in at(22150)
        and "in cyclic tag systems, 669" in at(22390)
    )
    ok &= index_text_ok
    print("actual_index_text", "OK" if index_text_ok else "MISMATCH")

    structural = (
        not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and matched_retained == pre_index_union & RETAINED
        and governed_continuations == set(RETAINED) - union
        and pre_index_union == matched_retained | excluded
        and not matched_retained & excluded
        and not RETAINED & index
        and {n for n in hits["Q00"] if n < INDEX_FIRST_LINE} <= RETAINED
        and len(union | governed_continuations) == 356
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    split_paths = sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() not in {DEFAULT_BOOK.resolve(), ATLAS.resolve()}
    )
    relative_paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in split_paths]
    split_manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    path_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(split_manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    ok &= path_manifest_ok
    print(
        "split_manifest",
        "OK" if path_manifest_ok else "MISMATCH",
        len(split_paths),
        digest_records(relative_paths),
        digest_records(split_manifest),
    )

    compiled = {
        name: re.compile(pattern, re.IGNORECASE) for name, pattern in QUERIES.items()
    }
    monolith_query_text = {at(n) for n in union}
    split_records: set[str] = set()
    split_exact_records: set[str] = set()
    split_nonexact_records: set[str] = set()
    split_texts: set[str] = set()
    split_direct_counts: dict[str, int] = {}
    all_split_records: set[str] = set()
    for path, relative in zip(split_paths, relative_paths, strict=True):
        split_document = path.read_text(encoding="utf-8")
        direct_count = len(DIRECT_NAME_STREAM_RX.findall(split_document))
        if direct_count:
            split_direct_counts[relative] = direct_count
        for line_no, line in enumerate(split_document.splitlines(), 1):
            record = f"{relative}:{line_no}"
            all_split_records.add(record)
            split_texts.add(line)
            if not any(rx.search(line) for rx in compiled.values()):
                continue
            split_records.add(record)
            if line in monolith_query_text:
                split_exact_records.add(record)
            else:
                split_nonexact_records.add(record)

    query_mapping_records = {
        f"{record}->{','.join(map(str, targets))}"
        for record, targets in SPLIT_NONEXACT_QUERY_WITNESSES.items()
    }
    direct_count_records = {
        f"{path}:{count}" for path, count in split_direct_counts.items()
    }
    split_query_ok = (
        (len(split_records), digest_records(split_records))
        == EXPECTED_SPLIT_QUERY_RECORDS
        and (len(split_exact_records), digest_records(split_exact_records))
        == EXPECTED_SPLIT_EXACT_QUERY_RECORDS
        and split_nonexact_records == set(SPLIT_NONEXACT_QUERY_WITNESSES)
        and digest_records(split_nonexact_records)
        == EXPECTED_SPLIT_NONEXACT_QUERY_RECORDS_DIGEST
        and digest_records(query_mapping_records)
        == EXPECTED_SPLIT_QUERY_MAPPING_DIGEST
        and set(split_direct_counts) == EXPECTED_SPLIT_DIRECT_NAME_PATHS
        and digest_records(set(split_direct_counts))
        == EXPECTED_SPLIT_DIRECT_NAME_PATHS_DIGEST
        and sum(split_direct_counts.values()) == 81
        and digest_records(direct_count_records)
        == EXPECTED_SPLIT_DIRECT_COUNTS_DIGEST
        and all(
            canonical in union
            for targets in SPLIT_NONEXACT_QUERY_WITNESSES.values()
            for canonical in targets
        )
    )
    ok &= split_query_ok
    print(
        "split_query",
        "OK" if split_query_ok else "MISMATCH",
        len(split_records),
        len(split_exact_records),
        len(split_nonexact_records),
        digest_records(split_records),
        digest_records(split_exact_records),
        digest_records(split_nonexact_records),
    )
    if not split_query_ok:
        print("split_nonexact_records", sorted(split_nonexact_records))
        print("split_direct_counts", sorted(split_direct_counts.items()))

    exact_retained_mirror = {n for n in RETAINED if at(n) in split_texts}
    split_nonexact_retained = set(RETAINED) - exact_retained_mirror
    retained_witness_records = set(SPLIT_NONEXACT_RETAINED_WITNESSES.values())
    retained_mapping_records = {
        f"{line}->{record}"
        for line, record in SPLIT_NONEXACT_RETAINED_WITNESSES.items()
    }
    retained_split_ok = (
        (len(exact_retained_mirror), digest(exact_retained_mirror))
        == EXPECTED_EXACT_RETAINED_MIRRORS
        and split_nonexact_retained == SPLIT_NONEXACT_RETAINED
        and digest(split_nonexact_retained)
        == EXPECTED_SPLIT_NONEXACT_RETAINED_DIGEST
        and set(SPLIT_NONEXACT_RETAINED_WITNESSES) | MONOLITH_ONLY_RETAINED
        == split_nonexact_retained
        and not set(SPLIT_NONEXACT_RETAINED_WITNESSES) & MONOLITH_ONLY_RETAINED
        and retained_witness_records <= all_split_records
        and digest_records(retained_witness_records)
        == EXPECTED_SPLIT_RETAINED_WITNESS_RECORDS_DIGEST
        and digest_records(retained_mapping_records)
        == EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST
        and at(12348) not in split_texts
    )
    ok &= retained_split_ok
    print(
        "split_retained",
        "OK" if retained_split_ok else "MISMATCH",
        len(exact_retained_mirror),
        len(split_nonexact_retained),
        digest(exact_retained_mirror),
        digest(split_nonexact_retained),
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n
        for n, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in compiled.values())
    }
    atlas_text = "\n".join(atlas_lines)
    atlas_ok = (
        len(atlas_lines) == EXPECTED_ATLAS_LINES
        and atlas_hits == EXPECTED_ATLAS_QUERY_LINES
        and digest(atlas_hits) == EXPECTED_ATLAS_QUERY_DIGEST
        and len(DIRECT_NAME_STREAM_RX.findall(atlas_text)) == 1
        and atlas_lines[100] == "### Cyclic Tag Systems"
        and "cycling through a fixed list of append operations" in atlas_lines[102]
        and "complexity persists" in atlas_lines[102]
    )
    ok &= atlas_ok
    print(
        "atlas",
        "OK" if atlas_ok else "MISMATCH",
        len(atlas_lines),
        len(atlas_hits),
        digest(atlas_hits),
        sorted(atlas_hits),
    )

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[18] == "Cyclic Tag Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 18. Cyclic Tag Systems" in taxonomy_text
        and "A cyclic list of append blocks acts like a program counter." in taxonomy_text
        and "advance to the next append block in the cycle" in taxonomy_text
        and "append the current block only if the removed symbol satisfies the trigger condition" in taxonomy_text
        and "The deleted symbol controls whether the scheduled block is appended" in taxonomy_text
        and "`program_counter`: current position in the cyclic list." in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
