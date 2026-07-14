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
from difflib import SequenceMatcher
from fractions import Fraction
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
    "Q39": r"5/2, multiplication system, 123",
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


# Every pre-Index query hit is classified exactly once.  Native contains the
# two strict parity presets and the residue-dispatch generalization.  Relation
# contains register/CA/continuous/Turing encodings and Conway's sibling.
# Control retains neighboring T34/T36/T37 boundaries.  Exclusions are lexical
# collisions returned by deliberately broad EvenQ/reversibility lanes.
NATIVE_MATCHED = line_set(
    "1497,1499,1503,1505,1507,1509,1513,1517,1519,1523,1525,1527,1529,"
    "8086,8102,12598,12599,12601,12603,12605,12609,12611,12619,12621,"
    "12625,12627,12629,12633"
)
RELATION_MATCHED = line_set(
    "1196,1198,8092,8094,8098,8100,11544,12613,12615,12617,16072,"
    "18626,18629,18632,18635,18636,18639,18648,18651,18652,18656,"
    "18660,18662,19102,19441,19456,19460,19933"
)
CONTROL_MATCHED = line_set("1495,1545,1555,1559,1561,12635,12688")

EXCLUDED_CLASS = {
    "generic_reversibility_not_T35": line_set("5304,16061"),
    "unrelated_EvenQ_programs": line_set("12122,14172,16432,19548"),
    "later_T36_caption": line_set("1549"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# Governed continuations close complete formulas, captions, table rows, and
# the immediate construction boundaries without pretending every line was a
# regex hit.  Blank lines are intentionally absent.
NATIVE_CONTINUATIONS = line_set(
    "1501,1511,1515,1521,1531,1533,1535,1537,1539,"
    "8104,8106-8110,12607,12623,12631"
)
RELATION_CONTINUATIONS = line_set(
    "1200,1202,1204,8096,"
    "18628,18630,18634,18637,18641-18644,18646,"
    "18650,18653,18655,18657-18658,18664,"
    "19439,19443-19444,19446-19448,19450-19451,19453,19455,19457-19458,"
    "19462-19465,19468"
)
CONTROL_CONTINUATIONS = line_set(
    "1491,1493,1541,1543,1557,12637,12639,12641,12643,12645,12690"
)

NATIVE_EVIDENCE = NATIVE_MATCHED | NATIVE_CONTINUATIONS
RELATION_EVIDENCE = RELATION_MATCHED | RELATION_CONTINUATIONS
CONTROL_EVIDENCE = CONTROL_MATCHED | CONTROL_CONTINUATIONS
MATCHED_RETAINED = NATIVE_MATCHED | RELATION_MATCHED | CONTROL_MATCHED
GOVERNED_CONTINUATIONS = (
    NATIVE_CONTINUATIONS | RELATION_CONTINUATIONS | CONTROL_CONTINUATIONS
)
RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("1505,1517,1523,12611,12633")
RELATION_IMAGE_LINES = line_set("1196,8098,8100,18662,19441")
CONTROL_IMAGE_LINES = line_set("1493,1543,12641")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_CLASS = {
    "register_machine_neighbors": line_set("1190"),
    "T34_predecessors": line_set("1481,1487"),
    "T36_T37_successors": line_set("1547,1551,1565"),
    "universal_emulation_predecessors": line_set("8084,8088"),
    "later_T36_notes": line_set("12654,12656,12658"),
}
EXCLUDED_IMAGE_LINES = frozenset().union(*EXCLUDED_IMAGE_CLASS.values())
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
# These Chapter-4 plates belong wholly to T43.  Their caption merely compares
# the appearance of iterated maps with page 122, so they are frozen as an
# explicit outside-candidate relation rather than silently added to T35 assets.
OUT_OF_SCOPE_RELATED_IMAGE_LINES = line_set("1884,1888")


INDEX_CLASS = {
    "core_alias_and_observer_routes": line_set(
        "20828,20836,20908,20957,20980,21090,21233,21329,21471,21497,21893,"
        "21933,22150,22287,22382"
    ),
    "arithmetic_and_emulation_routes": line_set(
        "20882,20894,21173,21223,21923,22390"
    ),
    "ordered_fraction_routes": line_set("21195,21805,21807"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_ENTRY_GUARDS = {
    "core_alias_and_observer_routes": {
        20828: ("3n + 1 problem, 904", "see also Arithmetic systems"),
        20836: ("5/2, multiplication system, 123",),
        20908: ("Backtracking in 3 n + 1 problem, 904",),
        20957: ("for 3n+1 problem, 904",),
        20980: ("Collatz problem, 904",),
        21090: ("Directional entropies and 3n + 1 problem, 904",),
        21233: ("Hasse's algorithm (3 n + 1 problem)",),
        21329: ("IntegerExponent and 3n + 1 problem, 904",),
        21471: ("Localized structures and 3n + 1 problem, 904",),
        21497: ("Markov processes, 1084 and 3n + 1 problem, 904",),
        21893: ("Random walks and 3n+1 problem, 904",),
        21933: ("Reversible 3 n + 1 problem, 905",),
        22150: ("Syracuse problem (3 n+1 problem)",),
        22287: ("Thwaites conjecture (3 n + 1 problem), 904",),
        22382: ("Ulam's problem (3 n + 1 problem)",),
    },
    "arithmetic_and_emulation_routes": {
        20882: ("Arithmetic systems, 122-124", "and Turing machine 600720, 1145"),
        20894: ("in systems based on numbers, 961",),
        21173: ("FactorInteger (integer factorization) and arithmetic system encoding, 1115",),
        21223: ("Gödel's Theorem, 1158 and arithmetic systems, 673",),
        21923: ("Register machines, 97–102", "emulated by arithmetic systems, 673. 1114"),
        22390: ("of arithmetic systems, 673",),
    },
    "ordered_fraction_routes": {
        21195: ("Fraction systems, 1115", "Fractran (universal fraction system). 1115"),
        21805: ("Primes and arithmetic systems, 1115",),
        21807: ("from fraction system, 1115",),
    },
}


VISUAL_ONLY_BOUNDARY = (
    "strict-parity-digit-rows-and-right-edge-trace",
    "strict-5-over-2-seed-gallery-and-log-size-trace",
    "3n-plus-1-stopping-time-and-reversible-size-observers",
    "register-machine-stroboscopic-and-residue-compiler-relations",
    "Conway-ordered-fraction-prime-observer",
    "Turing-600720-halting-time-relation",
    "T34-T36-neighbor-plates-remain-controls-or-exclusions",
    "T43-page165-page166-plates-are-explicitly-outside-the-T35-candidate-interface",
)


SOURCE_MODEL_RECORDS = (
    "category:deterministic discrete singleton t+0D transition system",
    "state:one exact integer; strict main presets preserve positive integers",
    "seed:one for the 3-over-2 preset; one and six are canonical 5-over-2 examples",
    "frontier:reuse UniqueScalar rather than a family-specific control object",
    "neighborhood:complete current integer read at the unique scalar locus",
    "rule:closed residue dispatch to arithmetic branch data",
    "strict-A:mod2 residue0 maps n to 3n/2 and residue1 maps n to 3(n+1)/2",
    "strict-B:mod2 residue0 maps n to 5n/2 and residue1 maps n to (n+1)/2",
    "integrality:each closed branch must prove integer output on its selected residue",
    "update:generic same-locus typed assignment and atomic commit",
    "successor:one deterministic successor for every strict positive-integer state",
    "termination:no strict cycle fixed-point or growth observation halts evolution",
    "generalization:modulus m provides one closed branch for each residue 0 through m-1",
    "branching:residue dispatch is data and validation, not executor family dispatch",
    "T34-boundary:fixed add or multiply is a one-operation restriction without predicates",
    "T36-boundary:digit reversal makes base representation feed the rule",
    "T37-boundary:recursive sequences read prior history rather than only the current scalar",
    "T43-boundary:continuous interval maps use real carriers and invariance contracts",
    "observer:digit rows parity words and logarithmic sizes never feed back",
    "locality:complete scalar read versus digit stencils is an alphabet-access distinction not a runner distinction",
    "observer:cycles stopping times directional entropy and random-walk approximations do not halt",
    "relation:register-machine trace equality is stroboscopic or encoded, not state identity",
    "relation:3n-plus-1 CA lowering adds digit cells and end markers",
    "relation:continuous cosine map emulation is not the discrete integer carrier",
    "image-boundary:page165-page166 iterated-map plates belong to T43 despite a page122 comparison",
    "Conway-sibling:ordered first applicable exact fraction is semantically order-sensitive",
    "Conway-sibling:reduced denominator divisibility lowers to ordered integer predicates",
    "Conway-sibling:no applicable fraction is source-undefined partial evolution; the evaluator uses the common zero-successor Error without inventing source-native halt or identity",
    "source-defect:line1501 extraction is not the chronological parity prefix",
    "source-defect:line8102 loses multiplication and contains nthat and stens OCR damage",
    "source-defect:line12623 reconstruction code has missing punctuation and stays opaque",
    "source-defect:line18632 says Table where a scalar prime-power Product is required",
    "source-defect:lines18635-18636 lose the ASEvolveList pattern punctuation",
    "source-defect:lines19456-19465 are not executable Turing-600720 formulas",
    "codec:no finite alphabet or fixed-width integer representation is inferred",
    "architecture:no callback new state class update law executor or runner branch",
)


EXPECTED_QUERY = {
    "Q00": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q01": (3, 3, 0, "e2f6dbf35de2eb7e14263a60a454600910f4295e128e47d4b00084a1cec4b2fa"),
    "Q02": (1, 1, 0, "74f43b441dde988eec37530a47aea2b433324d3311c4c6d6e870809a221bc39c"),
    "Q03": (3, 3, 0, "39150fd2acc8ec02aa747df1231f74b9418491245b308467254dde735a4c2744"),
    "Q04": (2, 2, 0, "70173ee5582cecf7e4e135456d0f071554de0dc0294e2d976f23ba5e56c6e5b6"),
    "Q05": (3, 3, 0, "3784070314b3a9a8c916736e0c4445488b08b3109214616854cef4d818665586"),
    "Q06": (2, 2, 0, "6800a0a1538d1ed9399188f6cd46c0872c554ae0bd7410e483abb02e8a7b7cfa"),
    "Q07": (3, 3, 0, "144ab6f7256b46c6b867c4aad5e908ce0bce1a25177145738f7b9f3ba10905dc"),
    "Q08": (14, 6, 8, "d23f89ad9297104d3a42612817c22e7efb537fca1303f6174aa5c16c11738875"),
    "Q09": (5, 0, 5, "1a12b12f3785a14ed687a5892baf6cfb81bc3266e0a12ff6d56e462e04a5f205"),
    "Q10": (2, 1, 1, "41bdbcf0310026ca7d7e265f9c1a9637dd7dbb499da3257bbdf43e040ae6f55d"),
    "Q11": (2, 2, 0, "b0c612cfa192ae4203923c16d16dd5aaa82b4ea2f624dc46d5fadfa992917c83"),
    "Q12": (8, 8, 0, "672e9049dfaf3bb847725f75419028011198b1b6872e13619564848ee40e996e"),
    "Q13": (1, 1, 0, "824bd8704dd8ed22c38ff1d7f04d4c60464bc559a59e661961afd9db42c53239"),
    "Q14": (1, 1, 0, "e209f7b7bfe0f9ccd9c6b5d8aa497b55b76812f56ff0cddd6fc9f703f17192b3"),
    "Q15": (3, 3, 0, "c35b61ba454eb4e3fc88f6cafd954e17780d112c0981025af0715e6b6f21adc8"),
    "Q16": (3, 3, 0, "f5f3af6dd8736e68ec11f8317fabcce7d4cd6f22b0b7dfd081c9a527a063b654"),
    "Q17": (3, 3, 0, "35e19ec0e37cd8540050361435a83b5fac8a08aa0183c1fa1174d6b7db042d0e"),
    "Q18": (4, 3, 1, "1bca3a62c5804921d9edef7c01f860113ceb52791d1f8cdf7287f2c1cc08b17b"),
    "Q19": (2, 1, 1, "7cf07a51b106addd27a36829dbe993b86a2ea0547f911b5250b9bba77acaf5ea"),
    "Q20": (1, 1, 0, "1d16a2735c7e1355d5dee5fe662d1ba09a6998ffcd7ce69b01eb4ff2b328d02f"),
    "Q21": (1, 1, 0, "d5dd8dc829d1c9d2d5ee39ddaf234b2ee822348d4122ab3b01b58b815fa0acca"),
    "Q22": (4, 4, 0, "7dccbb85f369ce924920d23e73dc4d55af06e1c815fd585a099bf183e9bc4a69"),
    "Q23": (2, 2, 0, "c0681fd6a58fb60951baed501f6466ee09dc57661c49b778a2981c4d6ad07e4e"),
    "Q24": (4, 3, 1, "224757ea6e50ec2d793d17dfe67298a5be4f4c7a3c7ea46b75b659db1f139133"),
    "Q25": (4, 4, 0, "164807a4778e78e9cfaa0c7b9609bd839c615856334a54032d75f4c1757753b6"),
    "Q26": (6, 6, 0, "d3eec325869682fc9d9cb387776c86bbf228c847e9cbdd5c4c807c50c6839703"),
    "Q27": (8, 0, 8, "21a489c63caa8145366e3b4d0529e0eca0a2dcb62124d7f8756d95ab03d5812d"),
    "Q28": (3, 0, 3, "51908fe4e4a72b4b385085dab985ee97052092201a3372385673d9dc136f6e01"),
    "Q29": (4, 0, 4, "990172075052e73e91f8e638350112bf57b30c49d29baf92fe165dcfd0bc1d1f"),
    "Q30": (3, 0, 3, "6dd203db24f4888836758a57cea13870fce67c5be123bf821763dc747c493d5b"),
    "Q31": (2, 1, 1, "9a44d47a4c74dd1d98a772b8623089fdebaf493c83d06f7620a11f6f6bfb1f0c"),
    "Q32": (2, 2, 0, "e3754d84c871cfe8335763909deabb9b39da3f1f203b3cebada7d768952c55f5"),
    "Q33": (3, 3, 0, "1af8d6ce03de1f26b43e2cc481e5f070bf739f4708894a4c033825ca92ed5b3b"),
    "Q34": (2, 2, 0, "81f23dacefd9f76e25be25df9f2f6bfd81796916f78ed3fa89a154826e7db69a"),
    "Q35": (3, 3, 0, "9122e9c513fcdd21f5d6f371f82fcb4423a73685334bde345c2a3602de9cf93c"),
    "Q36": (2, 2, 0, "5597aaeb5815f2bbf49f31584f274c471410a8537812109777126b5a1ac446f2"),
    "Q37": (13, 13, 0, "eb0599b3481bb207128d491751677db7d74176d607eeb10500a1d8b50984c696"),
    "Q38": (16, 9, 7, "4c2295155eb814d20b2cb239b3c05f7bbd529dabc47eeefd8cf996d3234a1849"),
    "Q39": (1, 0, 1, "TO_BE_FROZEN"),
}

EXPECTED_SET = {
    "union": (93, "edeed322c433ae5aa6a5aa496a1bf60dd4b1a4cba06454a65589a3757e1b93c5"),
    "pre_index_union": (70, "a5ca5ad032a64d7d35bc6c3b84dee4c220b4c26e7a685884dea22381fd5ed6a7"),
    "index": (23, "382ea160348f5429a8e0c999d0d74a0179c75f536903f6583e716c8f55b7948e"),
    "matched_retained": (63, "abe81df93c1a1006c8e97df9cf4d2c707696b6cf6b4849435062e7e694d8e1cc"),
    "governed_continuations": (65, "d71d4c46f610feae93defe56b9abb3ac81dfebc2d3428f42fdc9e20a54882f54"),
    "retained": (128, "014989b13a238d181d8039684eb508e3840df2d7d41cbbca0cff7e2d5b7f252b"),
    "excluded": (7, "d217cebdd1081002deb8a75cd08fd46ab4842822d96a9dc81f04fbf75cb8be61"),
    "native": (46, "90e59083b9fed98bcf868e74b70b721bf25025dd832cc54ac62478b8ab1b8c89"),
    "relation": (64, "ba05d4cac4e856b8b42ded72b132b3ac9449a25a7f7af5a94ba64b6eec88e044"),
    "control": (18, "46d2af20cd2dd9e4b9bbab77c5bcfa7083617b55cf9d4ebc820b4e3e8ff105e9"),
    "candidate_images": (24, "310fe3a307edd50f320ff21fde967fe8f403e211b297406ec4118b5f252f8703"),
    "governed_images": (13, "b8f65bdb30c81add390024e294cee779846e8f0ab6efe0492ea27662cd6a0e41"),
    "excluded_images": (11, "ab89873ac299a642221006015964a71145b35dc68cc52423724ec4d07b20e0fb"),
}
EXPECTED_EXCLUDED_CLASS = {
    "generic_reversibility_not_T35": (2, "18974dcafbc47a3a616bad13af26907786be5e353fc37bfdf0605760306201ef"),
    "unrelated_EvenQ_programs": (4, "470fbcb147f6b4789cc3da37b3f8c1712b06ea8866898c475a7dca8ab60f6ee9"),
    "later_T36_caption": (1, "75abf1771c0d9038e45203aa603758410f2418fd29b3fe0c25534009c579bb8e"),
}
EXPECTED_INDEX_CLASS = {
    "core_alias_and_observer_routes": (14, "15c37fcfbfadb59500416e15e3bdc8f49b734e264bda1e6c78a98c63016ed8c1"),
    "arithmetic_and_emulation_routes": (6, "2150118212314c3de41c2c6b6811b35879d4651d01999735891fc1283dfcf6e7"),
    "ordered_fraction_routes": (3, "9a44ad617d7439ee0c7608b0a917e31d962759bb52c235d99cd10f89fffa3322"),
}
EXPECTED_INDEX_GUARDS = (
    23,
    "bf020508d3063deb0782398e75606fe0eede3e1c856ba86ff5aaef5dd070e376",
)
EXPECTED_IMAGE_PARTITION = {
    "native": (5, "0c03146ee327f67d29869863e7180f135426d5a0d76003d5276678feb1c826b8"),
    "relation": (5, "24dbbd9b5294a09803addca6e12765187f465d74144f1bcde1fddb7f82b4f89a"),
    "control": (3, "cd97b97e7f85a1476197e80888d1b4115465c5902247f38741e7880a5f615482"),
}
EXPECTED_EXCLUDED_IMAGE_CLASS = {
    "register_machine_neighbors": (1, "58eb0dd988df36c54ae88fcf58afcd0a69944c335d82dfbe68094063f54f4363"),
    "T34_predecessors": (2, "87b23105b616d204fb7c46497bbea8b4749c57fca070e907bed05faf90813f4a"),
    "T36_T37_successors": (3, "f4064d394c624d178a611b8ec9a374b888f97b897cfc7d17caac24234cc2effe"),
    "universal_emulation_predecessors": (2, "f8526bf0d9ed0b78b7baa779232ec675f51079a32bbec7cfce2fdd8ce1e20245"),
    "later_T36_notes": (3, "a988c242ab8946f7a30e9aafdb304b4557702ad8c1193bd6222f07ee5b19f734"),
}
EXPECTED_OUT_OF_SCOPE_RELATED_IMAGES = (
    2,
    "1a0bb7e2ee9e24af615d6a2b4163e2f3c3150628047a06462becf0969bad8de9",
)
EXPECTED_VISUAL_ONLY_BOUNDARY = (
    8,
    "8c6eb95cb11cfd589c2183d0c1239e2c5b7172e50bafe0035ede5e794b1123b9",
)
EXPECTED_SOURCE_MODEL = (
    36,
    "a9c6a61dbcaf1a959dbaf75ca512414879840ac091bc30d3bbfc7fa640bd1247",
)


# Explicit content crosswalks replace unconstrained lexical nearest-neighbor
# matching.  The monolith and split corpus are independently hash-bound above;
# these records identify the intended split source location, while the replay
# below requires strong symmetric-token and ordered-text agreement.  Thus a
# tiny unrelated line cannot become a provenance witness merely by containing
# every one of its own few tokens.
SPLIT_QUERY_WITNESSES = {
    "BACK-MATTER/Colophon/Colophon.md:1219": 18662,
    "BACK-MATTER/Colophon/Colophon.md:1998": 19441,
    "BACK-MATTER/Colophon/Colophon.md:4939": 22382,
    "BACK-MATTER/Index/Index.md:514": 12611,
    "BACK-MATTER/Index/Index.md:536": 12633,
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:379": 8086,
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:391": 8098,
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:393": 8100,
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:395": 8102,
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:513": 1196,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:103": 1499,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:107": 1503,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:109": 1505,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:121": 1517,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:123": 1519,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:127": 1523,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:129": 1525,
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:163": 1559,
}

SPLIT_RETAINED_WITNESSES = {
    1196: "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:513",
    1493: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:97",
    1499: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:103",
    1501: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:105",
    1503: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:107",
    1505: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:109",
    1517: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:121",
    1519: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:123",
    1523: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:127",
    1525: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:129",
    1543: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:147",
    1559: "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:163",
    8086: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:379",
    8098: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:391",
    8100: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:393",
    8102: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:395",
    8104: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:397",
    8106: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:399",
    8107: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:400",
    8108: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:401",
    8109: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:402",
    8110: "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md:403",
    12611: "BACK-MATTER/Index/Index.md:514",
    12633: "BACK-MATTER/Index/Index.md:536",
    12637: "BACK-MATTER/Index/Index.md:540",
    12641: "BACK-MATTER/Index/Index.md:544",
    18662: "BACK-MATTER/Colophon/Colophon.md:1219",
    19441: "BACK-MATTER/Colophon/Colophon.md:1998",
}


# Split-corpus values are frozen after the reverse provenance pass below.
EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY = (
    92,
    "2bef8550a09a2c32b7cf59aa025b828094efb4d7be024e160b0c214e405b3114",
)
EXPECTED_SPLIT_QUERY_EXACT = (
    74,
    "940f357b5f6ee2419babbb044ce44f126ec971a5feeba15ba73e75419d01d272",
)
EXPECTED_SPLIT_QUERY_NONEXACT = (
    18,
    "ea572f9cfd2e25b6190f7e9ee0c194e1caa3f3f3e89d6d85fe7fc3520d2628dd",
)
EXPECTED_SPLIT_QUERY_MAPPING = (
    18,
    "3bfc618322bcfd96e7ed7f200452d6e238cc566f3d2aa5858988023cdfcc4f15",
)
EXPECTED_SPLIT_RETAINED_EXACT = (
    100,
    "934cd8c249df0dd47fab8079a9574832ecd8d464b2e6a3f54bbe74c10a8ed008",
)
EXPECTED_SPLIT_RETAINED_NONEXACT = (
    28,
    "0de29e75eebf9f4b859952171c6bc48a2105f9006067ce5a26173e319dd52ee4",
)
EXPECTED_SPLIT_RETAINED_MAPPING = (
    28,
    "1477e98ae2b38ecf0603f3e55595e99d8bed3d0ca2c9463101bf123364d36000",
)
EXPECTED_MONOLITH_ONLY = (
    0,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
)
EXPECTED_ATLAS_HITS = (
    5,
    "bc2d3922561b25c21574253966619ebf550e76c0c42a04c6f4074133ad845c32",
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


def witness_similarity(canonical: str, candidate: str) -> tuple[float, float]:
    """Return symmetric token and ordered-text agreement for one declared pair."""

    left = normalized_line(canonical)
    right = normalized_line(candidate)
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    denominator = len(left_tokens) + len(right_tokens)
    dice = (
        2 * len(left_tokens & right_tokens) / denominator
        if denominator
        else 0.0
    )
    ordered = SequenceMatcher(None, left, right).ratio()
    return dice, ordered


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 42-T35-source-oracle.py [BOOK]")
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
        found = {
            line_no
            for line_no, line in enumerate(lines, 1)
            if re.search(pattern, line, re.IGNORECASE)
        }
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

    exclusion_ok = set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS[name]
        exclusion_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    classification_delta = matched_retained ^ set(MATCHED_RETAINED)
    classification_ok = (
        exclusion_ok
        and not classification_delta
        and MATCHED_RETAINED == RETAINED & pre_index_union
        and GOVERNED_CONTINUATIONS == RETAINED - union
        and not EXCLUDED & RETAINED
    )
    ok &= classification_ok
    print(
        "unresolved_pre_index",
        "OK" if classification_ok else "MISMATCH",
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
            all(needle in at(line_no) for needle in needles)
            for entries in INDEX_ENTRY_GUARDS.values()
            for line_no, needles in entries.items()
        )
        and (len(guard_records), digest_records(guard_records))
        == EXPECTED_INDEX_GUARDS
    )
    index_ok &= guards_ok
    ok &= index_ok
    print(
        "index_entry_occurrence_guards",
        "OK" if guards_ok else "MISMATCH",
        len(guard_records),
        digest_records(guard_records),
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
    for line_no in CANDIDATE_IMAGE_LINES | OUT_OF_SCOPE_RELATED_IMAGE_LINES:
        match = IMAGE_RE.fullmatch(at(line_no))
        image_paths_ok &= match is not None
        if match is not None:
            basename = Path(match.group(1)).name
            image_paths_ok &= len(list(SOURCE_ROOT.rglob(basename))) == 1
    images_ok = (
        derived_images == set(GOVERNED_IMAGE_LINES)
        and sum(map(len, image_sets.values())) == len(GOVERNED_IMAGE_LINES)
        and set().union(*EXCLUDED_IMAGE_CLASS.values())
        == set(EXCLUDED_IMAGE_LINES)
        and sum(map(len, EXCLUDED_IMAGE_CLASS.values()))
        == len(EXCLUDED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and not EXCLUDED_IMAGE_LINES & RETAINED
        and not OUT_OF_SCOPE_RELATED_IMAGE_LINES & CANDIDATE_IMAGE_LINES
        and image_paths_ok
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION[name]
        images_ok &= good
        print(f"images_{name}", "OK" if good else "MISMATCH", *actual)
    for name, values in EXCLUDED_IMAGE_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_IMAGE_CLASS[name]
        images_ok &= good
        print(f"excluded_images_{name}", "OK" if good else "MISMATCH", *actual)
    outside_actual = (
        len(OUT_OF_SCOPE_RELATED_IMAGE_LINES),
        digest(OUT_OF_SCOPE_RELATED_IMAGE_LINES),
    )
    outside_ok = (
        outside_actual == EXPECTED_OUT_OF_SCOPE_RELATED_IMAGES
        and "Examples of iterated maps" in at(1886)
        and "compare page 122" in at(1886)
        and "number x between 0 and 1" in at(1886)
    )
    images_ok &= outside_ok
    image_ownership_ok = (
        images_ok
        and "succession of whole numbers" in at(1503)
        and "applying the rule" in at(1519)
        and "logarithmic scale" in at(1525)
        and "register machine" in at(1198)
        and "simple arithmetic system can emulate a register machine" in at(8102)
        and "exactly the primes" in at(18660)
        and "Longest halting times" in at(19439)
        and "number theory systems of page 122" in at(19460)
        and "fractional parts of successive powers of 3/2" in at(1495)
        and "write its base 2 digits in reverse order" in at(1545)
        and "Page 125 · Reversal-addition systems" in at(12635)
        and "nested rather than strictly repetitive" in at(1192)
        and "register machine set up to emulate a Turing machine" in at(8090)
        and "Examples of some simple recursive sequences" in at(1567)
        and "Digit reversal" in at(12646)
    )
    images_ok &= image_ownership_ok
    visual_actual = (len(VISUAL_ONLY_BOUNDARY), digest_records(VISUAL_ONLY_BOUNDARY))
    visual_ok = (
        visual_actual == EXPECTED_VISUAL_ONLY_BOUNDARY
        and not any("transcribed" in record for record in VISUAL_ONLY_BOUNDARY)
        and images_ok
    )
    ok &= visual_ok
    print(
        "governed_image_interface_asset_hash_routed_no_pixel_replay",
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
    print(
        "out_of_candidate_T43_page165_page166_relation",
        "OK" if outside_ok else "MISMATCH",
        *outside_actual,
    )
    print(
        "image_exact_caption_facing_and_sibling_ownership",
        "OK" if image_ownership_ok else "MISMATCH",
        len(EXCLUDED_IMAGE_CLASS),
    )

    # Strict source presets and exact main-text anchors.
    def step_a(n: int) -> int:
        return 3 * n // 2 if n % 2 == 0 else 3 * (n + 1) // 2

    def step_b(n: int) -> int:
        return 5 * n // 2 if n % 2 == 0 else (n + 1) // 2

    expected_a = [
        1, 3, 6, 9, 15, 24, 36, 54, 81, 123, 186, 279, 420, 630,
        945, 1419, 2130, 3195, 4794,
    ]
    trace_a = [1]
    for _ in range(len(expected_a) - 1):
        trace_a.append(step_a(trace_a[-1]))
    trace_b6 = [6]
    for _ in range(100):
        trace_b6.append(step_b(trace_b6[-1]))
    strict_ok = (
        "if the number at a particular step is even" in at(1499)
        and "multiply that number by 3/2" in at(1499)
        and "if the number is odd" in at(1499)
        and "first add 1" in at(1499)
        and "otherwise, add 1, then multiply by 3/2" in at(1503)
        and "always guaranteed to give a whole number" in at(1507)
        and all(step_a(n) > 0 and isinstance(step_a(n), int) for n in range(1, 1001))
        and all(step_b(n) > 0 and isinstance(step_b(n), int) for n in range(1, 1001))
        and trace_a == expected_a
        and ", ".join(map(str, expected_a)) in at(1507)
        and "multiply this number by 5/2" in at(1513)
        and "multiply the result by 1/2" in at(1513)
        and step_b(1) == 1
        and trace_b6[:6] == [6, 15, 8, 20, 50, 125]
    )
    ok &= strict_ok
    print(
        "source_two_strict_parity_presets_exact_positive_integer_branches",
        "OK" if strict_ok else "MISMATCH",
        len(trace_a),
        trace_a[-1],
        trace_b6[:6],
    )

    extracted_bits = at(1501).strip()
    n = 1
    parity_values: list[str] = []
    for _ in range(len(extracted_bits)):
        parity_values.append(str(n % 2))
        n = step_a(n)
    parity_prefix = "".join(parity_values)
    parity_observer_ok = (
        extracted_bits == "1011010001101001101010101010101010100000"
        and len(extracted_bits) == 40
        and parity_prefix != extracted_bits
        and parity_prefix[::-1] != extracted_bits
        and "rightmost digits obtained at each step are shown above" in at(1503)
        and "digit is 0 when the number is even and 1 when it is odd" in at(1503)
        and "seems to be completely random" in at(1509)
    )
    ok &= parity_observer_ok
    print(
        "source_line1501_opaque_display_not_chronological_parity_oracle",
        "OK" if parity_observer_ok else "MISMATCH",
        len(extracted_bits),
        hashlib.sha256(extracted_bits.encode("ascii")).hexdigest(),
        hashlib.sha256(parity_prefix.encode("ascii")).hexdigest(),
    )

    observer_ok = (
        "generally increasing trend" in at(1521)
        and "first thousand steps" in at(1525)
        and "logarithmic scale" in at(1525)
        and "48,554 (base 10) digits" in at(1527)
        and "system eventually evolves to 1" in at(12599)
        and "no general proof" in at(12599)
        and "sequence produced repeats if n ever reaches 2, 4 or 40" in at(12603)
        and "randomly even and odd with equal probability" in at(12605)
        and "no fundamental basis for the randomness approximation" in at(12607)
        and "how many steps are needed to reach value 1" in at(12609)
    )
    ok &= observer_ok
    print(
        "source_parity_size_cycle_stopping_and_random_walk_are_observers",
        "OK" if observer_ok else "MISMATCH",
    )

    # Residue-dispatch generalization and its complete 30-row source table.
    residue_rows = [8106, 8108, 8110]
    residues = [int(token) for line_no in residue_rows for token in re.findall(r"\d+", at(line_no))]
    formula_rows = [8104, 8107, 8109]
    formula_cells = [
        cell.strip()
        for line_no in formula_rows
        for cell in at(line_no).strip().strip("|").split("|")
    ]
    residue_ok = (
        "remainder after dividing by a constant" in at(8086)
        and "based on the value of this remainder" in at(8086)
        and "specified arithmetic operation" in at(8086)
        and "computes Mod[n, 30]" in at(8102)
        and "depending on the result applies to n one of" in at(8102)
        and residues == list(range(30))
        and len(formula_cells) == 30
        and all(formula_cells)
    )
    ok &= residue_ok
    print(
        "source_complete_residue_dispatch_generalization",
        "OK" if residue_ok else "MISMATCH",
        len(residues),
        len(formula_cells),
    )

    locality_ok = (
        "digit sequences" in at(1531)
        and "cellular automata are always local" in at(1533)
        and "systems based on numbers there is usually no such locality" in at(1533)
        and "carry" in at(1535)
        and "digits that were originally far away" in at(1535)
        and "fundamental differences" in at(1537)
        and "details of underlying rules" in at(1539)
    )
    ok &= locality_ok
    print(
        "source_digit_locality_contrast_is_alphabet_access_not_runner_split",
        "OK" if locality_ok else "MISMATCH",
    )

    notes_ok = (
        "NestList[If[EvenQ[#], 3#/2, 3(# + 1)/2] &, 1, t]" in at(12598)
        and "If[EvenQ[n], n/2, (3n+1)/2]" in at(12599)
        and "FixedPoint" in at(12601)
        and "If[EvenQ[n], 3n/2, Round[3n/4]]" in at(12627)
        and "If[Mod[n, 3] == 0, 2n/3, Round[4n/3]]" in at(12629)
        and "always possible to go backwards" in at(12629)
    )
    ok &= notes_ok
    print(
        "source_3n_plus_1_and_reversible_piecewise_siblings",
        "OK" if notes_ok else "MISMATCH",
    )

    reconstruction_ok = (
        "Reconstructing initial conditions" in at(12619)
        and "list of 0's and 1's" in at(12619)
        and "rightmost t digits" in at(12621)
        and "IntegerDigits[First[Fold" in at(12623)
        and "Last[#1]] 2 Last[#1]" in at(12623)
        and "Last[#1]], 2 Last[#1]" not in at(12623)
    )
    ok &= reconstruction_ok
    print(
        "source_reconstruction_formula_hash_bound_opaque_missing_punctuation",
        "OK" if reconstruction_ok else "MISMATCH",
    )

    ca_relation_ok = (
        "3*n*+1 **problem as cellular automaton" in at(12613)
        and "7 possible colors" in at(12613)
        and "color 6 works as an end marker" in at(12613)
        and "existence of persistent structure" in at(12617)
        and "register machine" in at(1198)
        and "compressed form" in at(1198)
        and "3n/2 if n is even" in at(1198)
        and "(3n+1)/2 if n is odd" in at(1198)
    )
    ok &= ca_relation_ok
    print(
        "source_CA_and_register_relations_add_representation_or_stroboscopic_state",
        "OK" if ca_relation_ok else "MISMATCH",
    )

    compiler_ok = (
        "RMToAS[prog_, nr_]" in at(18629)
        and "system from page 122 becomes" in at(18632)
        and "{2, \\{0 \\mapsto" in at(18632)
        and "ASEvolveList" in at(18635)
        and "NestList[(Mod[#, n]/. rules)[#] &, init, t]" in at(18636)
        and "state of the register machine" in at(18639)
        and "FactorInteger" in at(18642)
        and "only multiplication, with no addition" in at(18646)
    )
    ok &= compiler_ok
    print(
        "source_residue_program_representation_and_register_compiler_relation",
        "OK" if compiler_ok else "MISMATCH",
    )

    source_defects_ok = (
        at(8102).count("nthat") == 1
        and at(8102).count("stens") == 1
        and "i + 5,  $2^a$ ,  $3^b$" in at(8102)
        and "i + 5 2^a 3^b" not in at(8102)
        and "n + Table[Prime[i]^reg[[i]]" in at(18632)
        and "Product[Prime[i]^reg[[i]]" not in at(18632)
        and "Product[Prime[i]" in at(18643)
        and "ASEvolveList[{n . rules }. init . t ]" in at(18635)
        and "ASEvolveList[{n_, rules_}, init_, t_]" not in at(18635)
        and reconstruction_ok
        and "u = Nest[(13 + (6 \\# + 8)(5/2)^{4})]" in at(19456)
        and "\\{13/6 + 13/6\\}" in at(19463)
        and "16321 - 7860 i" in at(19465)
    )
    ok &= source_defects_ok
    print(
        "source_OCR_defects_guarded_no_executable_repair_invented",
        "OK" if source_defects_ok else "MISMATCH",
        6,
    )

    # Conway's exact ordered-fraction sibling: source order is observable.
    fractions = (
        Fraction(17, 91), Fraction(78, 85), Fraction(19, 51),
        Fraction(23, 38), Fraction(29, 33), Fraction(77, 29),
        Fraction(95, 23), Fraction(77, 19), Fraction(1, 17),
        Fraction(11, 13), Fraction(13, 11), Fraction(15, 14),
        Fraction(15, 2), Fraction(55, 1),
    )

    def fraction_successors(n: int) -> list[int]:
        products = [fraction * n for fraction in fractions]
        return [int(value) for value in products if value.denominator == 1]

    fraction_trace = [2]
    for _ in range(30):
        applicable = fraction_successors(fraction_trace[-1])
        if not applicable:
            break
        fraction_trace.append(applicable[0])
    conway_ok = (
        "Conway considered fraction systems" in at(18648)
        and "NestList[First[Select[fracs #, IntegerQ, 1]] &, init, t]" in at(18652)
        and "17/91" in at(18656)
        and "55/1" in at(18657)
        and len(fractions) == 14
        and fraction_successors(2) == [15, 110]
        and fraction_trace[:6] == [2, 15, 825, 725, 1925, 2275]
        and "exactly the primes" in at(18660)
    )
    ok &= conway_ok
    print(
        "source_Conway_ordered_first_applicable_fraction_sibling",
        "OK" if conway_ok else "MISMATCH",
        len(fractions),
        fraction_successors(2),
        len(fraction_trace),
    )

    turing_relation_ok = (
        "Longest halting times" in at(19439)
        and "Machine 600720" in at(19444)
        and "Nest[If[EvenQ[#], 5#/2, # + 21] &, 14, m]" in at(19460)
        and "number theory systems of page 122" in at(19460)
        and "halting time" in at(19460)
        and source_defects_ok
    )
    ok &= turing_relation_ok
    print(
        "source_Turing600720_connection_relation_opaque_not_native_rule",
        "OK" if turing_relation_ok else "MISMATCH",
    )

    boundaries_ok = (
        "fractional parts of successive powers of 3/2" in at(1495)
        and "independent of what base" in at(1495)
        and "write its base 2 digits in reverse order" in at(1545)
        and "Recursive Sequences" in at(1555)
        and "next number in the sequence from previous ones" in at(1559)
        and "f[n] depends" in at(1561)
        and "Page 125 · Reversal-addition systems" in at(12635)
        and "continuous iterated" in at(19102)
        and "3 + 6x - 3\\cos" in at(19102)
        and outside_ok
    )
    ok &= boundaries_ok
    print(
        "source_T34_T36_T37_T43_boundaries_explicit",
        "OK" if boundaries_ok else "MISMATCH",
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

    query_mapping: set[str] = set()
    query_mapping_ok = set(SPLIT_QUERY_WITNESSES) == split_nonexact
    for record in sorted(split_nonexact):
        witness = SPLIT_QUERY_WITNESSES.get(record)
        if witness is None:
            query_mapping_ok = False
            continue
        dice, ordered = witness_similarity(split_record_text[record], at(witness))
        query_mapping.add(f"{record}->{witness}")
        query_mapping_ok &= (
            witness in union
            and dice >= 0.60
            and ordered >= 0.80
        )
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
    retained_mapping_ok = (
        set(SPLIT_RETAINED_WITNESSES) == nonexact_retained
        and len(set(SPLIT_RETAINED_WITNESSES.values()))
        == len(SPLIT_RETAINED_WITNESSES)
    )
    for line_no in sorted(nonexact_retained):
        witness = SPLIT_RETAINED_WITNESSES.get(line_no)
        if witness is None or witness not in split_record_text:
            retained_mapping_ok = False
            monolith_only.add(line_no)
            continue
        dice, ordered = witness_similarity(at(line_no), split_record_text[witness])
        if dice < 0.60 or ordered < 0.80:
            retained_mapping_ok = False
            monolith_only.add(line_no)
            continue
        retained_mapping.add(f"{line_no}->{witness}")
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
        and retained_mapping_ok
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
        re.compile(r"^## 4\. Systems Based on Numbers$", re.I),
        re.compile(r"number-based systems", re.I),
        re.compile(r"^### Elementary Arithmetic$", re.I),
        re.compile(r"Simple operations like repeated addition or multiplication", re.I),
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
        and "Systems Based on Numbers" in atlas_lines[122]
        and "Elementary Arithmetic" in atlas_lines[128]
    )
    ok &= atlas_ok
    print("atlas_summary_only", "OK" if atlas_ok else "MISMATCH", *atlas_actual)

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[34] == "Arithmetic Iteration Systems,"
        and catalog_lines[35] == "Piecewise Integer Maps,"
        and catalog_lines[36] == "Digit-Reversal Arithmetic Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 35. Piecewise Integer Maps" in taxonomy_text
        and "predicate may be parity, divisibility, residue class" in taxonomy_text
        and "branching arithmetic program over one integer" in taxonomy_text
        and "`branches`: ordered predicate/update cases" in taxonomy_text
        and not hits["Q00"]
    )
    ok &= catalog_ok
    print(
        "catalog_taxonomy_piecewise_vocabulary_only_absent_from_primary_Book",
        "OK" if catalog_ok else "MISMATCH",
    )

    model_actual = (len(SOURCE_MODEL_RECORDS), digest_records(SOURCE_MODEL_RECORDS))
    architecture_ok = (
        model_actual == EXPECTED_SOURCE_MODEL
        and strict_ok
        and parity_observer_ok
        and observer_ok
        and residue_ok
        and locality_ok
        and notes_ok
        and reconstruction_ok
        and ca_relation_ok
        and compiler_ok
        and source_defects_ok
        and conway_ok
        and turing_relation_ok
        and boundaries_ok
    )
    ok &= architecture_ok
    print(
        "source_fit_T34_scalar_reuse_plus_closed_residue_dispatch_no_new_executor",
        "OK" if architecture_ok else "MISMATCH",
        *model_actual,
    )
    print(
        "unrecovered_raster_and_corrupt_formula_execution_semantics_fail_closed",
        "OK" if visual_ok and source_defects_ok else "MISMATCH",
        len(VISUAL_ONLY_BOUNDARY),
        4,
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
