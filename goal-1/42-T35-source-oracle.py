#!/usr/bin/env python3
"""Fail-closed primary-source audit for T35 piecewise integer maps.

The oracle freezes redundant searches over the canonical monolithic Book,
classifies every returned line plus governed continuations, routes the actual
Index, and reverse-joins the split corpus.  It audits evidence rather than
executing damaged Wolfram Language fragments or decoding raster pixels.

The source-faithful core is a singleton exact-integer configuration whose
current residue selects one closed arithmetic branch.  The residue dispatch,
not a new executor, is the construction-defining addition to T34's unary
scalar rule.  Digit rows, parity words, sizes, cycles, stopping times, and
emulation diagrams are observers or relations.  Conway's ordered-fraction
system is a partial ordered-divisibility sibling, not an untyped callback.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T35 source oracle requires assertions; do not use -O")


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


# Direct, mechanics, aliases, observers, relations, source-defect, image,
# actual-Index, and modern-taxonomy guard lanes.  Broad lanes are deliberate:
# all pre-Index false positives are explicitly classified below.
QUERIES = {
    "Q00": r"Piecewise Integer Maps?|Arithmetic Iteration Systems?",
    "Q01": (
        r"if the number at a particular step is even[^.]{0,260}multiply[^.]{0,80}3/2|"
        r"if the number is odd[^.]{0,180}add 1[^.]{0,120}3/2|"
        r"if the number obtained at a particular step is even[^.]{0,180}5/2"
    ),
    "Q02": (
        r"If\[EvenQ\[n\], 3\s*\\?,?\s*n/2, 3\s*\\?\(n\+1\)/2\]|"
        r"NestList\[If\[EvenQ\[#\], 3#/2, 3\(# \+ 1\)/2\]"
    ),
    "Q03": (
        r"If\[EvenQ\[n\], 5 n/2, \(n\+1\)/2\]|"
        r"multiply this number by 5/2|"
        r"rule[^.]{0,80}5 n/2[^.]{0,80}\(n\+1\)/2"
    ),
    "Q04": r"1, 3, 6, 9, 15, 24, 36, 54, 81, 123|48,554 \(base 10\) digits",
    "Q05": (
        r"rightmost digits obtained at each step|"
        r"sequence of which numbers are even and which are odd|"
        r"successive values of n are randomly even and odd"
    ),
    "Q06": (
        r"purely repetitive behavior[^.]{0,180}more complicated|"
        r"repeats if n ever reaches 2, 4 or 40|"
        r"no sign of repetition or of any other significant regularity"
    ),
    "Q07": r"_page_137_Picture_7\.jpeg|_page_138_Figure_6\.jpeg|_page_139_Figure_1\.jpeg",
    "Q08": r"3n\+1 problem|3 n \+ 1 problem|3\*n\*\+1",
    "Q09": (
        r"Collatz problem|Syracuse problem|Thwaites conjecture|"
        r"Ulam.?s problem \(3 n \+ 1 problem\)|"
        r"Hailstone numbers \(3 n \+ 1|Hasse.?s algorithm \(3 n \+ 1"
    ),
    "Q10": (
        r"FixedPoint\[\(3#/2\^IntegerExponent\[#|"
        r"IntegerExponent and 3n \+ 1 problem|"
        r"IntegerQ \(integer test\) and fraction systems"
    ),
    "Q11": (
        r"3n\+1 problem can then be viewed as a question|"
        r"3.?n.?\+1 problem as cellular automaton|"
        r"cellular automaton with 7 possible colors"
    ),
    "Q12": (
        r"Reconstructing initial conditions|"
        r"rightmost t digits in the starting value|"
        r"A reversible system|"
        r"Round\[3n/4\]|Round\[4n/3\]"
    ),
    "Q13": (
        r"generalization of the arithmetic systems discussed on page 122|"
        r"remainder after dividing by a constant|"
        r"based on the value of this remainder[^.]{0,180}arithmetic operation"
    ),
    "Q14": (
        r"computes Mod\[n, 30\]|"
        r"depending on the result applies to n one of the arithmetic operations|"
        r"simple arithmetic system can emulate a register machine"
    ),
    "Q15": (
        r"arithmetic system which emulates it can be obtained|"
        r"arithmetic system can emulate a register machine|"
        r"register machines-or arithmetic systems from page 673"
    ),
    "Q16": r"RMToAS\[|ASEvolveList\[|Mod\[#, n\]/\. rules",
    "Q17": (
        r"Conway considered fraction systems based on rules|"
        r"FSEvolveList\[|NestList\[First\[Select\[fracs #"
    ),
    "Q18": (
        r"fracs = \{17/91|Rest\[Log\[2, Select\[list|"
        r"_page_1130_Figure_11\.jpeg|Fractran \(universal fraction system\)"
    ),
    "Q19": (
        r"universal system using essentially just the operations of ordinary arithmetic|"
        r"universality of arithmetic systems|Universality[^.]{0,180}of arithmetic systems"
    ),
    "Q20": (
        r"discrete system[^.]{0,140}If\[EvenQ\[x\], 3x/2|"
        r"continuous iterated[^.]{0,160}3 \+ 6x - 3\\?cos|"
        r"universal arithmetic system on page 673"
    ),
    "Q21": (
        r"Turing machine 600720[^.]{0,180}number theory systems|"
        r"Nest\[If\[EvenQ\[#\], 5#/2, # \+ 21\]|"
        r"connection with the number theory systems of page 122"
    ),
    "Q22": (
        r"nthat it obtains|successive stens|"
        r"n \+ Table\[Prime\[i\]\^reg\[\[i\]\]|"
        r"ASEvolveList\[\{n \. rules \}\. init \. t|"
        r"\(13 \+ \(6 \\# \+ 8\)\(5/2\)\^\{4\}\)"
    ),
    "Q23": (
        r"fractional parts of successive powers of 3/2|"
        r"independent of what base is used to represent the numbers|"
        r"example just given involves numbers with fractional parts"
    ),
    "Q24": (
        r"write its base 2 digits in reverse order|"
        r"Reversal-addition systems|"
        r"same rule as on the previous page, but now starting with the number 512"
    ),
    "Q25": (
        r"#### \*\*Recursive Sequences\*\*|"
        r"definite rule for getting the next number in the sequence from previous ones|"
        r"f\[n\] depends only on the number immediately before"
    ),
    "Q26": (
        r"_page_115_Figure_1\.jpeg|_page_919_Figure_10\.jpeg|"
        r"_page_920_Figure_8\.jpeg|_page_688_(?:Figure_4|Picture_5)\.jpeg|"
        r"_page_1159_Figure_21\.jpeg"
    ),
    "Q27": (
        r"3n \+ 1 problem, 904|3 n \+ 1 problem, 904|"
        r"for 3n\+1 problem, 904|Reversible 3 n \+ 1 problem, 905"
    ),
    "Q28": (
        r"Arithmetic systems, 122-124|"
        r"emulated by arithmetic systems, 673|"
        r"of arithmetic systems, 673|"
        r"arithmetic recurrences, 123 and register machines"
    ),
    "Q29": (
        r"Fraction systems, 1115|Fraction system\)\. 1115|"
        r"from fraction system, 1115|Primes and arithmetic systems, 1115"
    ),
    "Q30": (
        r"Backtracking in 3 n \+ 1 problem|"
        r"Markov processes[^.]{0,120}3n \+ 1 problem|"
        r"Random walks and 3n\+1 problem"
    ),
    "Q31": (
        r"systems based on numbers are typically reversible|"
        r"Page 905 gives another example of a reversible system based on numbers|"
        r"Reversibility[^.]{0,300}in systems based on numbers"
    ),
    "Q32": (
        r"values can in fact be obtained by a simple arithmetic rule|"
        r"next value is 3n/2 if n is even|"
        r"After the first step these systems give the same sequence"
    ),
    "Q33": (
        r"systems that involve only whole numbers|"
        r"succession of whole numbers|overall sizes of whole numbers|"
        r"branching arithmetic program"
    ),
    "Q34": (
        r"number of steps are needed to reach value 1|"
        r"overall sizes of the numbers obtained for the first thousand steps|"
        r"digit is 0 when the number is even and 1 when it is odd"
    ),
    "Q35": (
        r"divisible by 2[^.]{0,180}whole number as the result|"
        r"always guaranteed to give a whole number|"
        r"finds the remainder after dividing by a constant"
    ),
    "Q36": (
        r"1930s: The 3n\+1 problem|"
        r"correspondence between arithmetic systems and register machines was established|"
        r"Additional work was done by John Conway"
    ),
    "Q37": r"If\[EvenQ\[",
    "Q38": r"arithmetic systems?",
}

