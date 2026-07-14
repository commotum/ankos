#!/usr/bin/env python3
"""Frozen primary-source audit for T26 two-dimensional substitution systems.

This is an evidence oracle, not a substitution-system implementation.  It
closes the Book's direct names, square-grid construction, inherited parallel
substitution mechanics, executable Notes form, backgrounds, dimensional and
shape variants, named examples, observer/encoding relations, sibling
boundaries, actual Index, split documents, Atlas, catalog, and false-positive
controls.

The evidence supports a two-dimensional ordered patch-emission form of the
existing SimpleProgram substitution construction.  It does not by itself
justify a T26 executor or top-level state class.  The strict square-grid source
uses uniformly aligned patches; orientation-sensitive off-grid geometry,
neighbor-dependent choice, adaptive subdivision, rasters, and coordinate
formulas are retained as variants, relations, controls, or observers rather
than silently promoted into the strict rule.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T26 source oracle requires assertions; do not use -O")


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


# The protocol deliberately mixes exact names with independent mechanics,
# aliases, named examples, page routes, relations, sibling controls, headings,
# actual-Index routes, and absent modern spellings.  Broad terms are always
# paired with construction-specific context so this audit does not pretend
# that every occurrence of "substitution system" concerns T26.
QUERIES = {
    "Q00": r"\btwo-dimensional substitution systems?\b|\b2D substitution systems?\b",
    "Q01": (
        r"\btwo dimensional substitution systems?\b|"
        r"\b2-dimensional substitution systems?\b|"
        r"\b2-D substitution systems?\b|"
        r"\bsubstitution systems? in two dimensions\b"
    ),
    "Q02": (
        r"\bconstruct two-dimensional substitution systems? that work in essentially the same way\b|"
        r"\beach square is replaced by four smaller squares at every step\b|"
        r"\breplace each black square with several smaller black squares\b|"
        r"\bnew black squares is then in turn replaced in exactly the\b|"
        r"\bidentical copy of the whole pattern\b"
    ),
    "Q03": r"\bSS2DEvolve\b|\bFlatten2D\b",
    "Q04": (
        r"1 \\to \\{\\{1, 0\\}, \\{1, 1\\}\\}|"
        r"\bpatterns? \(a\) through \(f\) on page 188\b|"
        r"\bexcluded pairs of digits are in exact correspondence\b"
    ),
    "Q05": (
        r"\bcolor of a cell at position \{i, j\} in a 2D substitution system\b|"
        r"\bcolor of any square in a nested pattern can be found from its coordinates\b|"
        r"\bone more digit in their coordinates\b|"
        r"\btake the rules for the substitution system that generates a particular nested pattern\b|"
        r"\bfeeding the digit sequences of its y and x coordinates\b"
    ),
    "Q06": (
        r"\b2D substitution system from a initial condition such as\b|"
        r"\bNon-white backgrounds\b|"
        r"\bwhite squares are replaced by blocks which contain black squares\b"
    ),
    "Q07": (
        r"\bHigher-dimensional generalizations\b|"
        r"\bddimensional substitution system\b|"
        r"\bnested list of depth d\b|"
        r"\bSSEvolve\b|\bFlattenArray\b|"
        r"\banalog in 3D of the 2D rule on page 187\b|"
        r"\bin d dimensions, each black cell must be replaced by at least d\+1\b"
    ),
    "Q08": (
        r"\bOther shapes\b|"
        r"\bbased on subdividing squares into smaller squares\b|"
        r"\bbased on subdividing other geometrical figures\b|"
        r"\blabelling each shape and orientation with a different color\b|"
        r"\breproduced with equal-sized squares using the rule\b"
    ),
    "Q09": (
        r"\bPage 187 . Sierpi.ski pattern\b|"
        r"\bexample on page 187 by Wac.aw Sierpi.ski\b|"
        r"\bexamples \(a\) and \(c\) on page 188 by Karl Menger\b|"
        r"\bSierpi.ski[^.]{0,120}\b2D substitution system\b|"
        r"\b2D substitution system[^.]{0,120}\bSierpi.ski\b"
    ),
    "Q10": (
        r"\btwo-dimensional recursive subdivision\b|"
        r"\bgeneralization of a two-dimensional substitution system\b|"
        r"\bquadtree representation\b|"
        r"\bRecursive subdivision[^.]{0,100}\bsubstitution systems?, 187\b|"
        r"\bSubdivision systems \(substitution systems\), 82 2D, 187\b"
    ),
    "Q11": (
        r"\bas in a two-dimensional substitution system each black cell should repeatedly be replaced\b|"
        r"\bgenerated from the two-dimensional substitution systems shown\b|"
        r"\bExamples of nested patterns created by following the two-dimensional substitution rules shown\b|"
        r"\btwo-dimensional pointer-based encoding scheme[^.]{0,120}\bnested structure\b"
    ),
    "Q12": (
        r"\b4 billion or so possible such systems with 2.2 blocks and up to four colors\b|"
        r"\bOne starts from the substitution system with rules\b|"
        r"\b51 of the 65,536 possible 2.2 blocks of cells with 16 colors\b"
    ),
    "Q13": (
        r"\bevolution of a 2D substitution system, or equivalently from a Kronecker product\b|"
        r"Nest\[Flatten2D\[Map\[# \{\{1, 1\}, \{1, -1\}\}"
    ),
    "Q14": r"\bpattern can be generated by a 2D substitution system with rule\b",
    "Q15": (
        r"\bnothing about this basic process that depends on the squares being arranged\b|"
        r"\bsimple geometrical rule to replace each black square by two smaller black squares\b|"
        r"\bmust take account of the orientation of that square\b|"
        r"\bgeometrical rule that is used to replace each black square\b|"
        r"\breplacing one black square by two or more smaller black squares\b"
    ),
    "Q16": (
        r"\breplacement for a particular element at a given step can depend\b|"
        r"\bsets up elements on a grid it is straightforward to allow the replacements\b|"
        r"\bNeighbor-dependent substitution systems\b|"
        r"\bFlatten2D\[Partition\[list, \{2, 2\}, 1, -1\] /\. rule\]\b|"
        r"\barbitrarily large set of different possible neighborhood configurations\b"
    ),
    "Q17": (
        r"\bhow can this be generalized to higher dimensions\b|"
        r"\bno immediate way to generalize sequential substitution systems to two or more dimensions\b|"
        r"\belements are scanned in order.but whatever order is used\b"
    ),
    "Q18": r"^#### \*\*Substitution Systems and Fractals\*\*$",
    "Q19": (
        r"\bat each step each one of these elements is replaced by a new block of elements\b|"
        r"\beach element of a particular color should be replaced by a fixed block\b|"
        r"\bat every step each kind of element is replaced by a fixed block\b|"
        r"\bsubdividing each element into several that are drawn smaller\b"
    ),
    "Q20": (
        r"\b2D geometrical substitution systems?\b|"
        r"\bgeometrical substitution systems?\b|"
        r"\bAffine transformations\b|"
        r"\bPenrose tilings\b"
    ),
    "Q21": (
        r"\bpage 187\b|\bpage 188\b|\bpages 187 and 188\b|"
        r"\b187[–-]192\b|\b187[–-]189\b"
    ),
    "Q22": (
        r"\bD0L systems\b|\b0L systems\b|\bL systems, 82.87 2D, 187.189\b|"
        r"\bSubdivision systems \(substitution systems\)\b"
    ),
    "Q23": (
        r"\bAffine transformations and 2D substitution systems, 933\b|"
        r"\bC curve from 1D substitution system, 892 from 2D substitution system, 190\b|"
        r"\bDeterminism in 2D substitution systems, 188\b|"
        r"\bDigit sequences[^.]{0,100}\band 2D substitution systems, 931\b|"
        r"\bFractals[^.]{0,100}\band 2D substitution systems, 187\b|"
        r"\bGoldenRatio[^.]{0,100}\band 2D substitution systems, 932\b|"
        r"\bMatrices and 2D substitution systems, 933\b"
    ),
    "Q24": (
        r"\bin 2D substitution systems, 187\b|"
        r"\bSierpi.ski[^.]{0,160}\band 2D substitution system, 188\b|"
        r"\bSierpi.ski pattern[^.]{0,160}\band 2D substitution system, 187\b|"
        r"\bTop[^.]{0,120}\bin 2D substitution systems, 188\b"
    ),
    "Q25": (
        r"\bSubstitution systems, 82.87 2D. 187.192\b|"
        r"\bd.-dimensional, 932, 1091\b|"
        r"\bgeometrical, 189.192\b|"
        r"\bneighbor-dependent 2D, 192, 935\b|"
        r"\bneighbor-independent 2D, 187\b"
    ),
    "Q26": (
        r"\bTwo-dimensional cellular automata[^.]{0,180}\bsubstitution systems, 187.192\b|"
        r"\bL systems, 82.87 2D, 187.189\b|"
        r"\bRecursive subdivision and data compression, 568[^.]{0,160}\band substitution systems, 187\b"
    ),
    "Q27": (
        r"\bpatterns shown here ultimately have a simple nested structure\b|"
        r"\ball the patterns shown here ultimately have a simple nested structure\b|"
        r"\bpurely nested patterns\b"
    ),
    "Q28": (
        r"\btile substitution systems?\b|\bblock substitution systems?\b|"
        r"\barray substitution systems?\b|\bpicture grammars?\b|"
        r"\borientation policy\b|"
        r"\bscale factor\b.{0,120}\bsubstitution systems?\b|"
        r"\bsubstitution systems?\b.{0,120}\bscale factor\b"
    ),
    "Q29": (
        r"\b2D representations\b|"
        r"\bsequences from 1D substitution systems can be displayed in 2D\b|"
        r"\barranged in two dimensions\b"
    ),
}


def line_set(spec: str) -> frozenset[int]:
    """Parse comma-separated physical line numbers and inclusive ranges."""
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Each tuple is (all physical lines, pre-Index lines, actual-Index lines,
# digest of the complete ascending line set).
EXPECTED_QUERY = {
    "Q00": (23, 13, 10, "b946fac1940f142a257a962e200195c404c5992d222216104af1f9aebfec9035"),
    "Q01": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q02": (4, 4, 0, "e0c53973b4fc9b688a4e37b9990e91a8f898d8362b514d5c54a1926eead892f3"),
    "Q03": (8, 8, 0, "6684f97186f9ce4d45248d6924d477076acc46aa821e811023db27b838ce7e5a"),
    "Q04": (2, 2, 0, "1578f5b9695b2efde6fd45016b585c8741c4a4d6fed25d37ba6be4090668f791"),
    "Q05": (3, 3, 0, "6e513346594b4e56c490da6dbd055b35919e1d1ed9acc5d48ca4abe09d9d285f"),
    "Q06": (2, 2, 0, "3394bdd090329c118c048c47e6fe70d1ea3ce8a14ab7a81824503d1eb003e3f1"),
    "Q07": (7, 7, 0, "56a635e4c63f4c8197688129619823ef36cea74e21a5133faf2c15230f3a33a5"),
    "Q08": (3, 3, 0, "7a46b8658011548e02b0c86105b0f0ce46f5db40d1e8771555bae8cee827fd3d"),
    "Q09": (3, 2, 1, "ec66702a6b6d3c7f9fb6100cb93f0c3b7ed8c8deb95d0bdba09c114c939af8b0"),
    "Q10": (3, 1, 2, "c37c74fe9fd8cbd51e034126d852e3649b8ae1c3e845a505c0f5ba908e6dc86d"),
    "Q11": (3, 3, 0, "76f9746fb0dd86aca77e0060e725dbff718cce0b1f48c8636f6364ee44589a28"),
    "Q12": (2, 2, 0, "92cea8bd8be3e0026a24243a9e244fceab0c32ce0bcc3dd39364c1afb425e752"),
    "Q13": (2, 2, 0, "7baa6019a6880a355060dbaec114bab55edfedc48d0db14735c27b37dd7f40eb"),
    "Q14": (1, 1, 0, "3a6a06a207e19079b77324fa89227865e95bb9df85001afb3bbb55e2df9ff7d6"),
    "Q15": (4, 4, 0, "084e864d193a546acb6ede637138da7f3e7fac7bfc459bd1bb2ebdca3f67520d"),
    "Q16": (9, 8, 1, "5203dee1563534a3aef6fa6b8014a4bcdfa7f674964eeb82a104d4baa0d2025d"),
    "Q17": (2, 2, 0, "2b38c0a5431171f2d39496c0bec159ed30c56fed81014b631db34fc5614547c1"),
    "Q18": (2, 2, 0, "b78f09ad0d3f50882d52ceec4efc71eaf8f3c0296ed6336d968341974df7f691"),
    "Q19": (4, 4, 0, "5155fe66a6f6d67fcf7954994aab4f599f09ad2f87eaa9fe64becc6d69d2b092"),
    "Q20": (16, 4, 12, "f625f246f75454b4a100e770d00e7dc77cd83be22ac1ea4d7d88eee14c50fd7b"),
    "Q21": (10, 7, 3, "e4e817d6e72348e1d4c1827a2581260d7418ac667de0fbe87fa504697963a2b4"),
    "Q22": (4, 1, 3, "b85b8ad19fd19241a9b895a002b6062993dde6d207c3c10753e003a022bf04e3"),
    "Q23": (6, 0, 6, "2e06cb69e173d658fbcea2334bdfcc2be25df8024f97d6961802eb0554033955"),
    "Q24": (3, 0, 3, "d2de5a968e7e861c3fdb324379b860fdd4552e039dc81595b4d09ccea5d213da"),
    "Q25": (1, 0, 1, "51493d0e1042577adde32e82b51d1ce32eee5d1903b81fe72f4cb791c11ac6b2"),
    "Q26": (3, 0, 3, "28de60283e32b0cded087a9564a4a8924c16ea7298a1bd6aa60d37574b1b6aab"),
    "Q27": (2, 2, 0, "8001eee54b360ef1cfc6836c07224b7029c41cbf853cd4cd58e9f1bd5af51ba6"),
    "Q28": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q29": (2, 2, 0, "f71a7f01c25f66bd178930ec98105495294ac57becb109bae1baf192054cdb14"),
}


# Every pre-Index query hit is assigned exactly once.  Native evidence is the
# strict rank-two construction or its inherited parallel-substitution rule.
# Relation evidence covers lossless/equivalent generators, analyzers, named
# examples, dimensional generalization, shape encodings, and downstream uses.
# Controls preserve the T27 geometric, T28 contextual, and sequential sibling
# boundaries without treating those constructions as strict T26 mechanics.
NATIVE_MATCHED = line_set(
    "984,986,992,994,"
    "2308,2312,2316,2318,2320,2324,"
    "13681,13683,13686-13688,13692,13699,13722"
)
RELATION_MATCHED = line_set(
    "6676,6842,6978,6984,7312,7322,12249,12259,"
    "13701,13726,13729-13731,13736,13738,13740,13744,13746,13754,"
    "13775,13786,14099,14109,17297,17299,17301,19197"
)
CONTROL_MATCHED = line_set(
    "2326,2332,2334,2348,2350,2356,2364,2366,13806,13808,13810"
)

NATIVE_CONTINUATIONS = line_set(
    "982,2310,2314,2322,13689,13695,13696,13724"
)
RELATION_CONTINUATIONS = line_set(
    "6668,6840,6982,7306,7316,7318,7320,"
    "13710,13712,13714-13720,13732,13733,13742,13748,13750,13752,"
    "13756,14102-14106,14111,17303,17305,17307,17309,17311"
)
CONTROL_CONTINUATIONS = line_set(
    "2328,2330,2340,2342,2344,2346,2352,2354,"
    "13758,13760,13762,13770,13772"
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
    "one_dimensional_sequences_displayed_in_2d": line_set("7118,12230"),
    "one_dimensional_contextual_or_lsystem_routes": line_set(
        "8024,8028,12251,18788"
    ),
    "unrelated_generic_heading_collisions": line_set("13272,13617"),
    "unrelated_flatten2d_uses": line_set("17352,17442"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("2314,2322,13724")
RELATION_IMAGE_LINES = line_set(
    "6668,6840,6982,7306,7320,13742,13748,14111,"
    "17303,17305,17307,17309,17311"
)
CONTROL_IMAGE_LINES = line_set("2328,2330,2340,2344,2354,13772")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)


# Actual Index rows are dense physical lines, so exact occurrence guards below
# prevent unrelated material on the same row from satisfying a route.
INDEX_CLASS = {
    "grid_construction_routes": line_set("21080,21088,21681,22144,22380"),
    "named_and_representation_routes": line_set(
        "20850,20944,21195,21223,21513,22114,22352"
    ),
    "alias_and_subdivision_routes": line_set("21422,21923,22138"),
    "geometric_and_contextual_sibling_routes": line_set("21213,21652"),
    "one_dimensional_alias_controls": line_set("20828,21068"),
    "generic_penrose_collisions": line_set(
        "20836,20862,21187,21193,21763,21819,21845,22306"
    ),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())

INDEX_ENTRY_GUARDS = {
    "grid_construction_routes": {
        21080: ("determinism in 2d substitution systems, 188",),
        21088: ("digit sequences", "and 2d substitution systems, 931"),
        21681: ("in 2d substitution systems, 187",),
        22144: (
            "substitution systems, 82-87 2d. 187-192",
            "neighbor-independent 2d, 187",
        ),
        22380: (
            "two-dimensional cellular automata",
            "substitution systems, 187–192",
        ),
    },
    "named_and_representation_routes": {
        20850: ("affine transformations and 2d substitution systems, 933",),
        20944: (
            "c curve from 1d substitution system, 892 from 2d substitution system, 190",
        ),
        21195: ("fractals and 1d substitution systems, 83", "and 2d substitution systems, 187"),
        21223: ("goldenratio", "and 2d substitution systems, 932"),
        21513: ("matrices and 2d substitution systems, 933",),
        22114: ("and 2d substitution system, 188", "and 2d substitution system, 187"),
        22352: ("top (spinning)", "in 2d substitution systems, 188"),
    },
    "alias_and_subdivision_routes": {
        21422: ("l systems, 82–87 2d, 187–189",),
        21923: ("recursive subdivision", "and substitution systems, 187"),
        22138: ("subdivision systems (substitution systems), 82 2d, 187",),
    },
    "geometric_and_contextual_sibling_routes": {
        21213: ("geometrical substitution systems", "189-192"),
        21652: ("neighbor-dependent substitution systems, 85–87",),
    },
    "one_dimensional_alias_controls": {
        20828: ("0l systems, 82-85, 893",),
        21068: ("d0l systems, 82-85", "d1l systems, 85–87"),
    },
    "generic_penrose_collisions": {
        20836: ("5d hypercubes and penrose tilings, 932",),
        20862: ("and penrose tilings, 932",),
        21187: ("fibonacci substitution system", "and penrose tilings, 932"),
        21193: ("folding map", "and penrose tilings, 932, 943"),
        21763: ("penrose tilings, 932",),
        21819: ("projection method", "for penrose tilings, 932"),
        21845: ("quadratic irrationals", "and penrose tilings, 932"),
        22306: ("penrose, 932", "see also penrose tilings"),
    },
}


EXPECTED_SET = {
    "union": (93, "9d6d6ff88a8d9e71dfc416e5946c60d786b9c0bd901a3326a0d65a38593d3fa8"),
    "pre_index_union": (66, "441ea2cf41ce38a9e868e3a56bf6f8446a5e3ffc71bd29c690ce02ba64ffe713"),
    "index": (27, "45f49612482d7bd4b8e168d19aa59674bfc7760b0d844be1966a8006dadd864c"),
    "matched_retained": (56, "5f543b779cbaa44df53149d856dbad95d96c6c43eb770f27365c8023bc65138f"),
    "governed_continuations": (55, "a73fc1767b97ae801fe3761d12a88a5c950b68c60866c86e1618ee6cc678540f"),
    "retained": (111, "30d5a9f4883150e22b30871e8d819c5c5617e1aaf0edbe00ca8deda6370cbc5c"),
    "excluded": (10, "6491ec40a274c829a77d3d6575dfbf1fe4964199506fba6e84c125c3d209b2c8"),
    "native": (26, "6e1fe6cad7bba3a647abfb578fb1069e1428c0681a53a35aeab368b207486e20"),
    "relation": (61, "d0ac2838289bd0ca4601092e8aa49715f02b920632b64c199d473c8d25060ccb"),
    "control": (24, "229b2d34e579a83e9a7ffeb4ef69354601fc766a200381734d112fe70e3a2348"),
    "governed_images": (22, "abb638e415af1ae4c09e8348d72c1df81c5cc599cd4e1846ea992160fe1fbebf"),
}
EXPECTED_EXCLUDED_CLASS = {
    "one_dimensional_sequences_displayed_in_2d": (
        2, "f71a7f01c25f66bd178930ec98105495294ac57becb109bae1baf192054cdb14"
    ),
    "one_dimensional_contextual_or_lsystem_routes": (
        4, "006550027143fe8557c458468a38d2d7cad67465513dd3ad9b00f7cc72e305e4"
    ),
    "unrelated_generic_heading_collisions": (
        2, "38a1f1197069a9b982bc7a237f953943a40d95b3a7c2e303ed99fb2b90dc3eae"
    ),
    "unrelated_flatten2d_uses": (
        2, "6ae34b4177b609a31a4c972474915f4775c00b36bfa8c3ad2a7534735dbf142c"
    ),
}
EXPECTED_INDEX_CLASS = {
    "grid_construction_routes": (
        5, "1a5c212f9bd426c05ea8ff45a0c7a3e52343a0fed0744cd33de1a732f59a2aa3"
    ),
    "named_and_representation_routes": (
        7, "a88a45f79087efacbb72095e12a5b93994a850e918b188a743374dd00ab896ad"
    ),
    "alias_and_subdivision_routes": (
        3, "9053b4b740afb58086f7c9778eb01fa1a42d518e82bcb9e1afcc4e9f63c4d660"
    ),
    "geometric_and_contextual_sibling_routes": (
        2, "8a49323bd44d5d72feea4c102b575e1fa19d0bb91f9c1f00f09ce0053c07ab62"
    ),
    "one_dimensional_alias_controls": (
        2, "154cff02563829d70fa5bbf0637554554a894d903e16e5af8ce0b32c97ff570c"
    ),
    "generic_penrose_collisions": (
        8, "bd1283aaf22bbeb6136e2a2696fc4c517b360756cf38b8350302cc9f79e76882"
    ),
}
EXPECTED_INDEX_ENTRY_GUARDS = (
    27, "c2ffa647e16540e11653146ba67e5193955704ac1e5222a04610041f763a3071"
)
EXPECTED_IMAGE_PARTITION = {
    "native": (3, "88c77dedfd94731adae1c3913a93edfea3ad631c7afc976b012c7024d169e83a"),
    "relation": (13, "477608a48338c626512a9ce01b6fa3c65e93700a4c8c67e6c21a769218ce3c91"),
    "control": (6, "c01d2da1809b7371770766da477a0290ee261809969d8668fb238cee19f2f775"),
}


# The split-source corpus is immutable in this repository snapshot.  Query and
# retained-line reverse-join expectations are filled from the complete final
# protocol below; every nonexact match must clear an explicit similarity gate.
EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"


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


def expand_uniform_grid(
    grid: tuple[tuple[int, ...], ...],
    rule: dict[int, tuple[tuple[int, ...], ...]],
) -> tuple[tuple[int, ...], ...]:
    """Derived reading of the Notes' rule replacement plus Flatten2D."""
    assert grid and all(grid) and len({len(row) for row in grid}) == 1
    patches = [rule[value] for row in grid for value in row]
    patch_heights = {len(patch) for patch in patches}
    patch_widths = {len(row) for patch in patches for row in patch}
    assert len(patch_heights) == len(patch_widths) == 1
    patch_height = next(iter(patch_heights))
    patch_width = next(iter(patch_widths))
    assert patch_height > 0 and patch_width > 0
    assert all(
        len(patch) == patch_height
        and all(len(row) == patch_width for row in patch)
        for patch in patches
    )
    return tuple(
        tuple(
            rule[grid[source_y][source_x]][local_y][local_x]
            for source_x in range(len(grid[0]))
            for local_x in range(patch_width)
        )
        for source_y in range(len(grid))
        for local_y in range(patch_height)
    )


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 38-T26-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
    )
    print("source", "OK" if source_ok else "MISMATCH")
    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        found = {n for n, line in enumerate(lines, 1) if re.search(pattern, line, re.I)}
        hits[name] = found
        print(
            name,
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
            ",".join(map(str, sorted(found))),
        )
    union = set().union(*hits.values())
    pre = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre
    print("union", len(union), digest(union), ",".join(map(str, sorted(union))))
    print("pre", len(pre), digest(pre), ",".join(map(str, sorted(pre))))
    print("index", len(index), digest(index), ",".join(map(str, sorted(index))))
    return 0 if source_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
