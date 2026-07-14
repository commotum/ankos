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
