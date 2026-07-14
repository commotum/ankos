#!/usr/bin/env python3
"""Frozen primary-source audit for T24 higher-dimensional lattice CAs.

This is an evidence oracle, not a cellular-automaton implementation.  It
separates the Book's arbitrary-dimensional and fixed-incidence cellular-
automaton mechanics from geometric representations, observers, cross-reference
routes, and structurally evolving network systems.  The architectural result
is intentionally narrower than the source collection: dimension, fixed
topology/incidence, ordered finite access, and closed rule data--including a
visible site-indexed rule bank sampled during setup--are candidate parameters
of the shared SimpleProgram event; this oracle does not manufacture a T24
executor from the catalog name.
"""

from __future__ import annotations

import hashlib
import itertools
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T24 source oracle requires assertions; do not use -O")


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


# Q00--Q04 close the direct name, arbitrary-dimensional implementation,
# formula, ordered-offset, and chapter-introduction vocabulary.  Q05--Q09
# close alternative lattice, tiling, Penrose, and fixed-network incidence.
# Q10--Q12 close update/realization and rule-restriction controls. Q13--Q14
# establish the structural-network and schedule seams. Q15 independently
# freezes actual-Index routes. Q16 follows geometry/isotropy references, Q17
# closes the built-in function/time-dependent-rule control, and Q18--Q19
# follow the lossless hexagonal-array implementation to both printed rules.
# Q20 deliberately broadens the hexagonal/triangular vocabulary and exposes
# block-CA, Turing-machine, random-walk, percolation, and biological false
# positives; it is not a claim that every possible alias has been saturated.
# Q21 closes the historical CA names and their actual-Index redirects. Q22--Q24
# expose broad tessellation/honeycomb, slice, and embedding vocabulary so views
# and lexical collisions remain visible. Q25 follows the fixed-network Cayley
# cross-reference, and Q26 closes the random-Boolean-network variant/history
# and its dense actual-Index routes.  Its randomness selects per-node tables at
# setup; a sampled visible bank is still closed fixed-incidence rule data. Q27
# independently guards the Bravais and Brillouin-zone actual-Index route used
# by the basis-coordinate handoff. Q28 gives every dense mixed line an
# independent T24 occurrence, and Q29 closes the Graphs/Networks index entries
# for fixed-incidence cellular automata.
QUERIES = {
    "Q00": r"\bhigher[- ]dimensional cellular automata\b",
    "Q01": (
        r"\bIn d dimensions with k colors\b|"
        r"d\\text\{-dimensional rule with|"
        r"\bvalues in d dimensions with d-dimensional padding\b|"
        r"\bIn any number of dimensions, aspec\b|"
        r"\bneighborhood for any rule in any dimension\b|"
        r"\brange r rules in d dimensions\b"
    ),
    "Q02": (
        r"\b(?:AxesTotal|FullTotal)\b|IdentityMatrix\[d\]|"
        r"Table\[3, \{d\}\]|"
        r"k \(2 d \(k - 1\) \+ 1\)|"
        r"\(3<sup>d</sup> - 1\) \(k - 1\) \+ 1|"
        r"9-neighbor rules generalize to 3<sup>d</sup> -neighbor rules"
    ),
    "Q03": (
        r"\boffset lists are always taken to be in the order\b|"
        r"\bpossible neighborhood configurations are\b|"
        r"\bIntegerDigits\[i - 1\b|FromDigits\[Reverse\[u\], k\]|"
        r"IntegerDigits\[num, k, k\^Length\[os\]\]|"
        r"\bListCorrelate\b|\brule with neighbors at specified offsets\b"
    ),
    "Q04": (
        r"\bExamples of simple arrangements of elements in one, two and three dimensions\b|"
        r"\btriangular and hexagonal grids are also possible\b|"
        r"\bvarious other lattices, analogous to those for regular crystals\b|"
        r"\bOther lattices\. See page 929\b|\bOther geometries\b"
    ),
    "Q05": (
        r"\bSystems like cellular automata can readily be set up on any geometrical structure\b|"
        r"\binteger multiples of some set of basis vectors\b|"
        r"\bfor the purpose of nearest-neighbor cellular automaton rules\b|"
        r"\bVoronoi region \(see page 987\) for each point in the lattice\b|"
        r"\bIn 4D, 8, 16 and 24 nearest neighbors are possible\b|"
        r"\bhigher dimensions possibilities have been investigated in connection with sphere packing\b"
    ),
    "Q06": (
        r"\bhexagonal prism\b|\brhombic dodecahedr(?:on|a)\b|"
        r"\brhombo-hexagonal\b|\belongated dodecahedron\b|"
        r"\btruncated octahedr(?:on|a)\b|\btetradecahedr(?:on|a)\b|"
        r"\bface-centered cubic\b|\bbody-centered cubic\b|"
        r"\b(?:fcc|bcc) lattice\b"
    ),
    "Q07": (
        r"\bno need for individual cells in a cellular automaton to have the same orientation\b|"
        r"\bany tiling of congruent figures can readily be used to make a cellular automaton\b|"
        r"\bpentagonal example\b|\bcode 4094\b|"
        r"\bcellular automaton on a nested Penrose tiling\b|"
        r"\bboth are treated the same by the cellular automaton rule\b|\bcode 254\b"
    ),
    "Q08": (
        r"\bPenrose tilings can be obtained by looking at how a 2D plane\b|"
        r"\bgeneralized cellular automaton constructed say on a Penrose tiling\b|"
        r"\b5D hypercubes and Penrose tilings\b|"
        r"\bPenrose tilings, 932 cellular automata on\b|"
        r"\b5-fold symmetry CA patterns with\b"
    ),
    "Q09": (
        r"\bCellular automata can be set up so that each cell corresponds to a node in a network\b|"
        r"\baround each node the network must have the same structure\b|"
        r"\bFor nearest-neighbor rules, it suffices that each node has the same number of connections\b|"
        r"\bCayley graphs of groups always have the necessary homogeneity\b|"
        r"\bconnections at each node are not labelled, then only totalistic cellular automaton rules\b|"
        r"\bCellular automata on networks\b|\bnodes in arbitrary networks\b|"
        r"\bNetCAStep\b"
    ),
    "Q10": (
        r"\bupdated in parallel at every step\b|\bold values of neighbors\b|"
        r"\bfinite array of cells\b|\bcyclic array\b|"
        r"\bautomatically gets cyclic boundary conditions\b"
    ),
    "Q11": (
        r"\bInitial conditions are constructed from init\b|"
        r"\bpositive direction in each coordinate\b|"
        r"\bevolution list of length t\+1\b|"
        r"\ball cells that can be affected by the specified\b|"
        r"\btrim off background from the sides\b"
    ),
    "Q12": (
        r"\bRules are considered rotationally symmetric\b|"
        r"\bTotalistic rules depend only on the total number\b|"
        r"\bouter totalistic rules\b|\bGrowth totalistic rules\b|"
        r"\bouter totalistic code(?: number)?\b"
    ),
    "Q13": (
        r"\bfixed underlying geometrical structure which remains unchanged\b|"
        r"\brules that specify how the connections coming out of each node should be rerouted\b|"
        r"\bdifferent operations are performed at different nodes, depending on the local structure\b|"
        r"\bnew node should be inserted in the above connection\b|"
        r"\bSequential network systems\b|\bevery node is updated in parallel at each step\b"
    ),
    "Q14": (
        r"\bprobabilistic cellular automata\b|\bNoisy cellular automata\b|"
        r"\bcontinuous cellular automata\b|"
        r"\bupdated sequentially rather than in parallel\b"
    ),
    "Q15": (
        r"\bCrystal lattices[^.]{0,80}\bsystems on, 169, 929\b|"
        r"\bCubic lattices cellular automata on, 182\b|"
        r"\bcellular automata on networks, 930, 936\b|"
        r"\bPenrose tilings, 932 cellular automata on, 930, 1028\b|"
        r"\bTriangular lattice[^.]{0,100}\bcellular automata on, 930\b|"
        r"\bTruncated octahedron[^.]{0,80}\band 3D lattices, 930\b|"
        r"\bVoronoi region and CA lattices, 929\b|"
        r"\bWigner-Seitz cells[^.]{0,50}\band CA lattices, 929\b|"
        r"\bWulff shapes[^.]{0,80}\band CA lattices, 929\b|"
        r"\bRhombic dodecahedron, 929, 987\b|"
        r"\bRhombo-hexagonal dodecahedron, 930\b|"
        r"\bSphere packing, 986[^.]{0,130}\band lattices, 930\b|"
        r"\bTetradecahedron, 930, 987, 988\b|"
        r"\b24 dimensions isotropy of lattices in, 980\b|"
        r"\b8 dimensions isotropy of lattices in, 980\b"
    ),
    "Q16": (
        r"\bVoronoi diagram for a set of points shows the region\b|"
        r"\bsimple cubic lattice the regions are cubes with 6 faces\b|"
        r"\bfcc lattice they are rhombic dodecahedra with 12 faces\b|"
        r"\bbcc lattice they are truncated octahedra\b|"
        r"\bIn 3D no regular lattice forces isotropy beyond n = 2\b|"
        r"\bSO\(8\) lattice works up to n = 4\b|"
        r"\bLeech lattice up to n = 10\b"
    ),
    "Q17": (
        r"\brule in which neighbor i is assigned weight\b|"
        r"\bapplies the function fun to each list of\b|"
        r"\bneighbors, with a second argument of the step\b|"
        r"\bsecond argument passed to fun is the step number\b|"
        r"\bwhen a general function is used\b"
    ),
    "Q18": (
        r"\bregular arrays of atoms laid out much like the cells in a cellular automaton\b|"
        r"\badjacent to a black cell will itself become black on the next step\b|"
        r"\breflects directly the structure of the underlying lattice of cells\b|"
        r"\ball the molecules in a snowflake ultimately lie on a simple hexagonal grid\b|"
        r"\bcells become black if they have exactly one black neighbor\b|"
        r"\beach cell on a hexagonal grid becomes black whenever exactly one\b"
    ),
    "Q19": (
        r"\bOne can treat hexagonal lattices as distorted square lattices\b|"
        r"\bcode 16382\b|\bcode 10926\b|"
        r"\bcenters of an array of regular hexagons\b"
    ),
    "Q20": (
        r"\bhexagonal (?:grid|lattice|lattices)\b|"
        r"\btriangular lattice\b|\bpentagonal (?:example|cell|tiling)\b"
    ),
    "Q21": (
        r"\btessellation automata\b|\bcellular spaces\b|"
        r"\biterative automata\b|\bhomogeneous structures\b|"
        r"\buniversal spaces\b"
    ),
    "Q22": r"\bhoneycomb\b|\btessellations?\b",
    "Q23": r"\bslices?\b",
    "Q24": r"\bembedded\b|\bembeddings?\b",
    "Q25": (
        r"\bGiven a particular representation of a group or semigroup in terms of rules for a multiway system\b|"
        r"\bsimilar Cayley graphs\b|"
        r"\bdifferent choices of generators can yield Cayley graphs with different local subgraphs\b"
    ),
    "Q26": r"\bBoolean networks?\b",
    "Q27": (
        r"\bBravais lattices, 929\b|"
        r"\bBrillouin zones, 987 and CA lattices, 929\b"
    ),
    "Q28": (
        r"\bBody-centered cubic \(bcc\), 930\b|"
        r"\bCayley graphs, 938\b|"
        r"\bmultidimensional CAs, 927\b|"
        r"\bSO\(8\) lattice, isotropy of, 980\b|"
        r"\bSpace groups, 929\b|"
        r"\bTetradecahedron, 930, 987, 988\b|"
        r"\bWigner-Seitz cells\b"
    ),
    "Q29": r"\bcellular automata on, 930, 936\b",
}

EXPECTED_QUERY = {
    "Q00": (1, 1, 0, "690c4db056e43ca1024e4878a222d0851fd0784206d10f5107ac6553e434066f"),
    "Q01": (5, 5, 0, "df1b395debca55f9676069f65c41dec29f0535edc45726c67f32455ec4620da4"),
    "Q02": (11, 11, 0, "f70bf9e3e81120144d25bfa54322d58252b2401f5240e630a1e478bcbe730756"),
    "Q03": (13, 11, 2, "83fa2727e4fa717149a36b228cbf46c92829c6b71ecceaf2076f92a1265d2967"),
    "Q04": (3, 3, 0, "033e5a900cf397c304cbb8988666503159eaf538b9cc18924504c9c783e154b0"),
    "Q05": (3, 3, 0, "426d1e9ae1d4e062b42e11f273eccf13dc54b8ab62e22499ba6857407975b41f"),
    "Q06": (15, 5, 10, "8472ca1c543b44bb7bf6679942f3c3adcd72b7502a6bed493eb164f8d1c844c2"),
    "Q07": (2, 2, 0, "91db60877c50db77528fcb86829c44a573344ffa314e5f0f83dad0fe06202961"),
    "Q08": (4, 2, 2, "cedd849cf095fe3ad6fc5468aea38522a4dbb3b3340328c4c9e40daf8df77242"),
    "Q09": (7, 6, 1, "ebfc6ada0b89ac0f5a4d72b84704c261c606c289f378124005ac0117c496ee07"),
    "Q10": (4, 4, 0, "09f0ced54248f816de461539fe9f4703b92b7a353b413328816e1f3a94e4346b"),
    "Q11": (5, 5, 0, "e938101e6472fb355452b7a93951bf5575b11a430a084f6e0ed79d710b4072d2"),
    "Q12": (12, 10, 2, "42db202eee8b0a3e6d45e03d2a5bc3ff3ad88094d8ca4f9ee027e8e3c67711e7"),
    "Q13": (6, 5, 1, "76e6c49ffdd32e1f99c554baaa05920cf809171d2e80225399e43fe67153ded9"),
    "Q14": (31, 27, 4, "f7ba64517fae4ad6c993b7d319fa9b9bb665e5aabdc6f719e2f4a9aced76beab"),
    "Q15": (13, 0, 13, "ec47e680e4e6cd26af3cd5eb8e846a4086ad55576060ca31f43e036cf4b944a8"),
    "Q16": (2, 2, 0, "c51ecba43eadb73dfdeeca54f8b691b91c5d6b27f91310d2abc3aae9a5a3d7f4"),
    "Q17": (4, 4, 0, "a42512c7dafb47a47226f2b2452bdee8a1c210e7404bbe41f12b6a2faaa59d71"),
    "Q18": (7, 7, 0, "0bffb17916facc44a53a086f117ef6db099957744f44e03f822f3746b99b5851"),
    "Q19": (2, 2, 0, "748b344c47308275c85e78147e066c7cdd86c39ae1a53cb5f10b7cee58fcfc10"),
    "Q20": (14, 12, 2, "26c82e76aab7eb8587dd01a3114a8c4196e0079aa2c7c17d650b0385d01fe0b6"),
    "Q21": (6, 1, 5, "ac1f1acdbb0da3e0ea9b78e135a4e5704b65668fcfe9450191ff53a81a81caba"),
    "Q22": (8, 6, 2, "27b8e41c5c3d636894a4997ddeba5fea82b9b64a32f80758fae705ec6dc8ddcd"),
    "Q23": (40, 36, 4, "77823e5de2675ce66a760965dfbf8cdb0f82bf5f2dec0034d419be00fbd7bd81"),
    "Q24": (10, 8, 2, "b203d92c67310e4e6fb75d9d19447a01518100285758a908fdd922f894c69761"),
    "Q25": (3, 3, 0, "6c5b017ba141cb4fbe65c6f8ae39abd8faefe68e8da18a60a4660b4843737b4c"),
    "Q26": (13, 3, 10, "2ab226cf54f54d1911a100c3e80f22d8912587e541ad5e723d6d28b1cb68b0e5"),
    "Q27": (1, 0, 1, "f2472c5ec828ce28052b6ac9b556c251a00e2722dec5c411cb75b47ba44a55f0"),
    "Q28": (7, 0, 7, "6c326b0f0c9c42b8a98f86336f7c8b0a5cbd9cc7fbd47d314839ee6b429b3fc7"),
    "Q29": (2, 0, 2, "717073c9f930df73ba41e6a72a55f8905fe0013ecdf6b5ff9700af5a62ba87e9"),
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


# Broad-query collisions are retained here, rather than silently disappearing.
# The structural-network and alternate-schedule seams remain control evidence
# below because they directly bound the native fixed-incidence construction.
EXCLUDED_CLASS = {
    "other_ca_family_or_dimension": line_set(
        "1948,1986,2008,2014,2102,2878,2880,2884,2890,2904,3784,3804,"
        "3902,7084,7092,13281,13296,13601,13613,13666,14234,14237,14241,"
        "15074,15075,15359,15392,15959,17002,17588,19072"
    ),
    "broad_implementation_name_collision": line_set(
        "11289,14358,14490,14573,14617,16755,17429,17722"
    ),
    "other_geometry_or_physics": line_set("3856,3862,4440,15507,15865"),
    "other_program_or_schedule_vocabulary": line_set(
        "2600,2618,6190,6194,6196,6198,6200,6214,6240,6266,6268,"
        "6270,6272,6280,6282,6286,6386,6388,6392,6456,6458,13347,"
        "15378,15550,16556,16672"
    ),
    "unrelated_slice_embedding_or_honeycomb": line_set(
        "3124,15881,15887,15944,15996,17109,18262"
    ),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# Strict native mechanics preserve the Book's own decomposition: finite label
# values on fixed support, old-snapshot local reads, same-site label writes,
# and parallel update.  This includes arbitrary integer-offset lattices,
# distorted-array coordinates for a hexagonal lattice, congruent/nonrepetitive
# tilings, and fixed networks whose connections are read but not rewritten.
NATIVE_EVIDENCE = line_set(
    "850,2154,2156,4408,4410,4412,4414,4422,4424,4428,4430,"
    "10984,10986,10992,11050-11056,11060-11062,"
    "13483,13485-13486,13488,13490,13492,13494-13495,13497,13499,"
    "13501,13503,13505,13507,13513,13515-13518,13520,13522-13525,"
    "13528,13530-13531,13534,13536,13538,13540,13542-13549,"
    "13642,13644,13646,13648,13650,13652,13654,"
    "13656,13658,13909-13910,13913-13915,15608,15610,15612"
)

# Relations provide examples, topology/geometry derivations, symmetry facts,
# and observer-level outcomes.  They do not silently define native coordinates,
# rule identity, or an execution family.
RELATION_EVIDENCE = line_set(
    "4416,10261,11503,13746,13748,13754,13756,13994,13996,14000,"
    "15293,15467,15473-15475,15485,15487,16253,16255,16808,19588"
)

# Controls make representation and execution boundaries explicit: finite/crop
# realization, unrestricted function/time dependence, stochastic/continuous
# values, topology rewriting, random rule-bank generation/ensemble provenance,
# sequential scheduling, and alternating block updates are not smuggled into
# strict T24.  Once sampled into visible finite per-node tables, however, a
# Boolean rule bank uses the same fixed-incidence snapshot event.
CONTROL_EVIDENCE = line_set(
    "2018,2202,2204,2206,2372,2426,2464,2910,2912,2918,2930,5334,"
    "6376,11037,11063-11065,11077,11079-11087,11090,"
    "11092,11095-11100,11103,11106-11107,11110,11112,11114,11116,"
    "11118,11120,11122,11124,11563,13314,13464,13575,13835,13889,"
    "13891,13893,13895,13917-13919,14063,15708,16446,16717,16875,"
    "18778,20118"
)

RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE

# Stable public interface for the independent asset audit.  Native images show
# the dimensional/lattice setup and strict fixed-incidence CA examples;
# relation images show the Penrose/Voronoi source routes; control images show
# the explicitly excluded single-active-node network schedule.
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("2154,4412,4428,13648,13652,13656")
RELATION_IMAGE_LINES = line_set("13748,15487")
CONTROL_IMAGE_LINES = line_set("13891,13893,13895")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)


# The actual Index supplies search routes, not construction semantics.
INDEX_CLASS = {
    "t24_geometry_and_topology_routes": line_set(
        "20828,20836,20910,20940,20967,21054,21068,21102,21170,21181,"
        "21231,21243,21683,21763,21934,22132,22166,22352,22416,22438"
    ),
    "historical_ca_alias_routes": line_set("20970,21253,21362,22390"),
    "boolean_network_variant_routes": line_set(
        "21213,21283,21416,21495,21687,21689,21771,22134,22426"
    ),
    "observer_or_embedding_routes": line_set("20980,21132"),
    "mixed_t24_alias_variant_or_observer_routes": line_set(
        "20918,20946,21471,22114,22120,22150,22434"
    ),
    "t24_rule_restriction_routes": line_set("21233,21731"),
    "structural_or_sequential_network_routes": line_set("22096"),
    "continuous_or_stochastic_routes": line_set("21046,21434,21735,21815"),
    "broad_implementation_name_routes": line_set("21050"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())

# Dense Index rows interleave columns. Every routed physical line therefore
# freezes the exact entry (or entries) that justify its line-exclusive class;
# an unrelated match elsewhere on the same row cannot stand in for T24.
INDEX_ENTRY_GUARDS = {
    "t24_geometry_and_topology_routes": {
        20828: ("24 dimensions isotropy of lattices in, 980",),
        20836: ("5-fold symmetry ca patterns with", "8 dimensions isotropy of lattices in, 980"),
        20910: ("bcc (body-centered cubic), 930",),
        20940: ("bravais lattices, 929", "brillouin zones, 987 and ca lattices, 929"),
        20967: ("cellular automata on networks, 930, 936",),
        21054: ("crystal lattices", "systems on, 169, 929"),
        21068: ("cubic lattices cellular automata on, 182",),
        21102: ("rhombo-hexagonal, 930",),
        21170: ("face-centered cubic (fcc) lattice, 930",),
        21181: ("fcc (face-centered cubic) lattice, 930",),
        21231: ("graphs", "cellular automata on, 930, 936", "see also networks"),
        21243: ("hexagonal cellular automata", "implementation of cas on 992", "hexagonal prism, 929"),
        21683: ("networks", "cayley graphs, 1032", "cellular automata on, 930, 936"),
        21763: ("penrose tilings, 932 cellular automata on, 930, 1028",),
        21934: ("rhombic dodecahedron, 929, 987", "rhombo-hexagonal dodecahedron, 930"),
        22132: ("sphere packing, 986", "isotropy of lattices, 980", "and lattices, 930"),
        22166: ("see tetradecahedron",),
        22352: ("triangular lattice", "cellular automata on, 930", "truncated octahedron", "3d lattices, 930"),
        22416: ("voronoi region and ca lattices, 929",),
        22438: ("wulff shapes in ca growth, 929", "ca lattices, 929"),
    },
    "historical_ca_alias_routes": {
        20970: ("cellular spaces see cellular automata",),
        21253: ("homogeneous structures see cellular automata",),
        21362: ("iterative automata", "see cellular automata"),
        22390: ("universal spaces see cellular automata",),
    },
    "boolean_network_variant_routes": {
        21213: ("boolean networks",), 21283: ("boolean networks",),
        21416: ("boolean networks",), 21495: ("boolean networks",),
        21687: ("boolean networks",), 21689: ("boolean networks",),
        21771: ("boolean networks",), 22134: ("boolean networks",),
        22426: ("boolean networks",),
    },
    "observer_or_embedding_routes": {
        20980: ("communications systems slices through, 928",),
        21132: ("embeddings of networks, 193, 476, 1031",),
    },
    "mixed_t24_alias_variant_or_observer_routes": {
        20918: ("body-centered cubic (bcc), 930", "boolean networks, 936"),
        20946: ("cayley graphs, 938", "cellular automata on 930"),
        21471: ("listconvolve", "multidimensional cas, 927", "listcorrelate"),
        22114: ("so(8) lattice, isotropy of, 980", "spacelike slices"),
        22120: ("space groups, 929", "spacelike slices, 1041"),
        22150: ("tessellation automata", "tetradecahedron, 930, 987, 988"),
        22434: ("wigner-seitz cells", "ca lattices, 929", "whitney embedding theorem"),
    },
    "t24_rule_restriction_routes": {
        21233: ("growth totalistic rules, 928",),
        21731: ("outer totalistic rules",),
    },
    "structural_or_sequential_network_routes": {
        22096: ("sequential network systems, 936",),
    },
    "continuous_or_stochastic_routes": {
        21046: ("continuous cellular automata",),
        21434: ("continuous cellular automata",),
        21735: ("noisy cellular automata",),
        21815: ("probabilistic cellular automata",),
    },
    "broad_implementation_name_routes": {
        21050: ("listcorrelate",),
    },
}
EXPECTED_INDEX_ENTRY_GUARDS = (
    50, "21864ccce511d0563103361b1784eff377fe16bc686c0910760330bca47c9c58"
)


EXPECTED_SOURCE_COUNT = 166
EXPECTED_SOURCE_DIGEST = "6df18eafb55416cb2cdfb0972da8bcaf958e1605df5e8e64785187212ff137f5"
EXPECTED_SET = {
    "union": (218, "962900aed133abc4c2df18dccc4c85f3729388b2e9f589c5dbc8fefcb1e474c9"),
    "pre_index_union": (168, "b08f6b6fb0e7ef05e9ad9b52f35e6d29fd7fc5c5e371943fe34dd59707293f5d"),
    "index": (50, "da2b55cc285ac5a347972772610fe0b017c3d0752bf244b9903202432b4d8ff6"),
    "matched_retained": (91, "1f6edc49c8836e6b06631fbf8c4b05850b39230fd21d4a3fe8a05b48d4c7ef89"),
    "governed_continuations": (75, "b595c685406b8df5bf1e5defeeed1baea4ad59822ef8a816020bd579fe3696a1"),
    "retained": (EXPECTED_SOURCE_COUNT, EXPECTED_SOURCE_DIGEST),
    "excluded": (77, "8a2d25876bd2e8f9997d8c7e7963ffc99d26904396af055ad8bcd600e546ae5f"),
    "native": (80, "1c7fa838bfa3e42073f8f8b7f8dfe2647a16a188f515063421892fb7255df2c3"),
    "relation": (21, "765f57ae96e7b9c673423056032c498f84be315d95d40821a1259e801753ca45"),
    "control": (65, "b65f6092999ffd35c43394980ce559c35612378cb5efe26801c5e085b86a4ece"),
    "governed_images": (11, "07b740cf80d9e0caef2500ebb6882c4322a6969b9fc284e3e77af4b9a611b62d"),
}
EXPECTED_EXCLUDED_CLASS = {
    "other_ca_family_or_dimension": (31, "518bafbc6cfd250eff1dedd235d768aa786a7fcab576dce1d9da8df701b34234"),
    "broad_implementation_name_collision": (8, "1e1b1fd12fdbaf287f1f20611843ed5c22c8d5ad1a20b94b0fc66bbb46d561d7"),
    "other_geometry_or_physics": (5, "ba1d93bbb23d8cd72f1cf471b68d0cf1e3f7e99771703b79cb762fe4269f9e18"),
    "other_program_or_schedule_vocabulary": (26, "d99b45eb1dd8f6f3fbe3fd1828da15a12a490c7cc6de90564138b5d558b47e2b"),
    "unrelated_slice_embedding_or_honeycomb": (7, "eb213f4e64c2d1ee8aa82e6bd2a6c4dc7d2284e433d14b42f944942d763cb711"),
}
EXPECTED_INDEX_CLASS = {
    "t24_geometry_and_topology_routes": (20, "33cb39114836c9d79b84f777c0e52a59a4d05fe9cf50585e0c01b6d9017c3a24"),
    "historical_ca_alias_routes": (4, "2049afd38c1c49e2c5b1f0d87a3187a9cf023ebfb8748fc950cc259d7cb94172"),
    "boolean_network_variant_routes": (9, "a4217032d8bb25cdc44d7df67553f654f2837a87313d0ab5b2f02294f8e0e8b8"),
    "observer_or_embedding_routes": (2, "41142e6d10049d6279a02badfde7fd780eb3befdade8d370d06cc466607371f1"),
    "mixed_t24_alias_variant_or_observer_routes": (7, "6c326b0f0c9c42b8a98f86336f7c8b0a5cbd9cc7fbd47d314839ee6b429b3fc7"),
    "t24_rule_restriction_routes": (2, "633b53d4c3b49f1981130965b95e51e3c505945acafb9fe29b57949f19812fde"),
    "structural_or_sequential_network_routes": (1, "2754f6e1f004d4298d7ed6444c52385d98a70aee827877053ef7d43e519ac10f"),
    "continuous_or_stochastic_routes": (4, "c6db33d21c31050eaaa818770ba46e08cb74c0f434347d2559db6cae73a0e772"),
    "broad_implementation_name_routes": (1, "9c8f3bc73a25f8227f7d939c8134e388e68a5d50f5629d9b62023cc699fa1e0f"),
}
EXPECTED_IMAGE_PARTITION = {
    "native": (6, "e6b89d89fdb76ba4bb76560fcbcd6dd0f22169301ab98bc8017e8bf0571b085f"),
    "relation": (2, "97cdd4f0b5c022cd17993d343b86304469fd691b53f5e5d6d3d8dad5b003b5c8"),
    "control": (3, "5748688fa018e741a32f21c25a0b5935985b6c17f924575daf80fcfe2ce258c1"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
# Filled from the deterministic reverse joins below; unlike raw source hashes,
# these freeze both exact duplicates and normalized split-document variants.
EXPECTED_SPLIT_QUERY = (218, "a8a19d0bc6317edc4ad4986da865bd2726eec003eabbcc4b7438c5e5fad5cdd7")
EXPECTED_SPLIT_QUERY_EXACT = (208, "4fa8013fc5109242e3b74f9634fb5c53db88c9b09c9a06ada542b331ad9627e3")
EXPECTED_SPLIT_QUERY_NONEXACT = (10, "101d91b24328ba3ade771d965c618f065ca35a6c38ea0f3a49426e056260a891")
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = "049eaeabdd9c88c46f4d1e225aea230dcee97e1b9ccfa2cc07aefb5e00406357"
EXPECTED_SPLIT_RETAINED_EXACT = (150, "c6e1e03966eb6c7e191879895bf9a72f36aeaa165d29ad8ba7246e84c3e387be")
EXPECTED_SPLIT_RETAINED_NONEXACT = (16, "ebe344dc2bebbbf661fc80f91ff5cafd1d760b496198da5d6955748e84e7d0cc")
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = "ace92ae9d4caebb974d026d1115ca8e0c3d7bfd8b95fd0e4135337aa949c465e"
EXPECTED_MONOLITH_ONLY = (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
EXPECTED_ATLAS_HITS = (1, "620c9c332101a5bae955c66ae72268fbcd3972766179522c8deede6a249addb7")


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
    """Return the deterministic highest-overlap witness for a source line."""
    canonical_tokens = set(normalized_line(canonical).split())
    scored: list[tuple[float, str]] = []
    for record, normalized in candidates:
        candidate_tokens = set(normalized.split())
        denominator = min(len(canonical_tokens), len(candidate_tokens))
        score = len(canonical_tokens & candidate_tokens) / denominator if denominator else 0.0
        scored.append((score, record))
    score, record = max(scored, key=lambda item: (item[0], item[1]))
    return record, score


def axis_offsets(dimension: int) -> tuple[tuple[int, ...], ...]:
    """The derived 2d face/axis shell, excluding Self."""
    return tuple(
        sorted(
            tuple(sign if coordinate == axis else 0 for coordinate in range(dimension))
            for axis in range(dimension)
            for sign in (-1, 1)
        )
    )


def full_offsets(dimension: int) -> tuple[tuple[int, ...], ...]:
    """The derived {-1,0,1}^d shell, excluding Self."""
    zero = (0,) * dimension
    return tuple(
        offset
        for offset in itertools.product((-1, 0, 1), repeat=dimension)
        if offset != zero
    )


def aggregate_rule(code: int, aggregate: int) -> int:
    """Decode the Book's binary aggregate-table convention at one input."""
    return (code >> aggregate) & 1


def sampled_site_rule_step(
    state: tuple[int, ...],
    incidence: tuple[tuple[int, ...], ...],
    rule_bank: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Apply visible per-site Boolean tables from one old snapshot."""

    assert state and len(state) == len(incidence) == len(rule_bank)
    assert all(value in (0, 1) for value in state)
    assert all(
        sources
        and all(0 <= source < len(state) for source in sources)
        and len(table) == 2 ** len(sources)
        and all(value in (0, 1) for value in table)
        for sources, table in zip(incidence, rule_bank)
    )
    return tuple(
        table[sum(state[source] << bit for bit, source in enumerate(sources))]
        for sources, table in zip(incidence, rule_bank)
    )


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 36-T24-source-oracle.py [BOOK]")
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
        good = actual == EXPECTED_QUERY[name]
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index_union = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index_union
    matched_retained = pre_index_union - EXCLUDED
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
        set().union(*EXCLUDED_CLASS.values()) == EXCLUDED
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    excluded_ok &= (
        pre_index_union == matched_retained | set(EXCLUDED)
        and matched_retained == set(RETAINED) & pre_index_union
    )
    ok &= excluded_ok
    print("unresolved_pre_index", "OK" if excluded_ok else "MISMATCH", 0)

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
    print("unresolved_index", "OK" if index_ok else "MISMATCH", 0)

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

    # Direct source facts. The checks deliberately preserve the Book's exact
    # wording; arithmetic and representation conclusions are tested separately.
    source_facts_ok = (
        "updated in parallel at every step" in at(850)
        and "old values of neighbors" in at(10984)
        and "two copies of the array" in at(10984)
        and "finite array" in at(10986)
        and "cyclic array" in at(10986)
        and "automatically gets cyclic boundary conditions" in at(10992)
        and "In d dimensions with k colors" in at(13483)
        and "a + k AxesTotal[a, d]" in at(13488)
        and "IdentityMatrix[d]" in at(13492)
        and "k (2 d (k - 1) + 1)" in at(13494)
        and "3<sup>d</sup> -neighbor rules" in at(13497)
        and "a + k FullTotal[a, d]" in at(13501)
        and "Table[3, {d}]" in at(13505)
        and "(3<sup>d</sup> - 1) (k - 1) + 1" in at(13507)
        and "any rule in any dimension" in at(13513)
        and "offset lists are always taken to be in the order given by *Sort*" in at(13513)
        and "same order as the offset list" in at(13513)
        and "IntegerDigits[i - 1" in at(13516)
        and "FromDigits[Reverse[u], k]" in at(13520)
        and "IntegerDigits[num, k, k^Length[os]]" in at(13523)
        and "ListCorrelate" in at(13531)
    )
    ok &= source_facts_ok
    print("source_facts_dimension_offsets_update", "OK" if source_facts_ok else "MISMATCH")

    dimensions = range(1, 7)
    colors = range(2, 5)
    dimension_formula_ok = all(
        len(axis_offsets(d)) == 2 * d
        and len(set(axis_offsets(d))) == 2 * d
        and all(tuple(-x for x in offset) in axis_offsets(d) for offset in axis_offsets(d))
        and len(full_offsets(d)) == 3**d - 1
        and len(set(full_offsets(d))) == 3**d - 1
        and all(tuple(-x for x in offset) in full_offsets(d) for offset in full_offsets(d))
        and all(
            k * (2 * d * (k - 1) + 1) == k * ((len(axis_offsets(d))) * (k - 1) + 1)
            and k * (((3**d - 1) * (k - 1)) + 1)
            == k * (len(full_offsets(d)) * (k - 1) + 1)
            for k in colors
        )
        for d in dimensions
    )
    ok &= dimension_formula_ok
    print(
        "derived_arbitrary_dimension_shells_and_case_counts",
        "OK" if dimension_formula_ok else "MISMATCH", 1, 6,
    )

    def from_digits(digits: tuple[int, ...], base: int) -> int:
        value = 0
        for digit in digits:
            value = value * base + digit
        return value

    positional_ok = True
    sample_offsets = tuple(sorted({(-2, 1), (0, 0), (1, -1), (3, 0)}))
    for k in (2, 3):
        context_count = k ** len(sample_offsets)
        table = tuple((i * i + 2 * i + 1) % k for i in range(context_count))
        code = from_digits(tuple(reversed(table)), k)
        decoded = tuple((code // (k**i)) % k for i in range(context_count))
        positional_ok &= decoded == table
        configurations = tuple(
            itertools.product(range(k), repeat=len(sample_offsets))
        )
        positional_ok &= all(
            from_digits(configuration, k) == index
            for index, configuration in enumerate(configurations)
        )
        positional_ok &= tuple(reversed(configurations))[0] == (k - 1,) * len(sample_offsets)
    ok &= positional_ok
    print("derived_positional_codec_round_trip", "OK" if positional_ok else "MISMATCH")

    # The hexagonal column is direct T24 evidence, not a schedule control. The
    # orbit counts below independently recover the printed 28 and 26 exponents.
    hex_contexts = tuple(itertools.product((0, 1), repeat=7))

    def rotate_hex(context: tuple[int, ...], amount: int) -> tuple[int, ...]:
        center, ring = context[0], context[1:]
        return (center,) + ring[amount:] + ring[:amount]

    def reflect_hex(context: tuple[int, ...]) -> tuple[int, ...]:
        return (context[0],) + tuple(reversed(context[1:]))

    rotation_orbits = {
        min(rotate_hex(context, amount) for amount in range(6))
        for context in hex_contexts
    }
    dihedral_orbits = {
        min(
            *(rotate_hex(context, amount) for amount in range(6)),
            *(rotate_hex(reflect_hex(context), amount) for amount in range(6)),
        )
        for context in hex_contexts
    }
    hex_rule_space_ok = (
        "total number of 2D rules" in at(13534)
        and "Totalistic rules depend only" in at(13536)
        and "outer totalistic rules" in at(13536)
        and "Growth totalistic rules" in at(13536)
        and "hexagonal" in at(13542)
        and "$2^{128}" in at(13544)
        and "$2^{28}" in at(13545)
        and "$2^{26}" in at(13546)
        and "$2^{14} = 16384" in at(13547)
        and "$2^8 = 256" in at(13548)
        and "$2^7 = 128" in at(13549)
        and len(hex_contexts) == 128
        and len(rotation_orbits) == 28
        and len(dihedral_orbits) == 26
        and 2 * (6 + 1) == 14
        and 6 + 2 == 8
        and 6 + 1 == 7
    )
    ok &= hex_rule_space_ok
    print(
        "native_hexagonal_rule_spaces",
        "OK" if hex_rule_space_ok else "MISMATCH", 128, 28, 26, 14, 8, 7,
    )

    geometry_source_ok = (
        "any geometrical structure" in at(13642)
        and "limited number of types of cells" in at(13642)
        and "merely what cells are adjacent" in at(13644)
        and "integer multiples of some set of basis vectors" in at(13644)
        and "Voronoi region" in at(13644)
        and "In 4D, 8, 16 and 24 nearest neighbors are possible" in at(13646)
        and "higher dimensions possibilities have been investigated in connection with sphere packing" in at(13646)
        and "any tiling of congruent figures" in at(13650)
        and "any of its five neighbors are black and has code 4094" in at(13650)
        and "no need for the tiling to be repetitive" in at(13654)
        and "both are treated the same" in at(13654)
        and "code 254" in at(13654)
        and "any of its three neighbors are black" in at(13654)
    )
    code_derivations_ok = (
        tuple(aggregate_rule(4094, value) for value in range(12))
        == (0,) + (1,) * 11
        and tuple(aggregate_rule(254, value) for value in range(8))
        == (0,) + (1,) * 7
    )
    ok &= geometry_source_ok and code_derivations_ok
    print(
        "source_geometry_and_exact_code_wording",
        "OK" if geometry_source_ok else "MISMATCH", 4094, 254,
    )
    print(
        "derived_outer_totalistic_code_tables",
        "OK" if code_derivations_ok else "MISMATCH", 12, 8,
    )

    hex_kernel = ((1, 1, 0), (1, 0, 1), (0, 1, 1))
    hex_source_ok = (
        "regular arrays of atoms" in at(4408)
        and "any cell which is adjacent to a black cell" in at(4410)
        and "structure of the underlying lattice" in at(4414)
        and "simple hexagonal grid" in at(4422)
        and "exactly one black neighbor" in at(4424)
        and "step before" in at(4430)
        and "treat hexagonal lattices as distorted square lattices" in at(15608)
        and "rule[[14-#]]" in at(15610)
        and "ListConvolve" in at(15612)
        and "IntegerDigits[code, 2, 14]" in at(15612)
        and "code 16382" in at(15612)
        and "code 10926" in at(15612)
        and "centers of an array of regular hexagons" in at(15612)
    )
    displayed_centers = {
        (i, j)
        for i in range(1, 8)
        for j in range(i % 2, 12, 2)
    }
    hex_representation_ok = (
        sum(map(sum, hex_kernel)) == 6
        and len(displayed_centers) == sum(
            len(range(i % 2, 12, 2)) for i in range(1, 8)
        )
        and tuple(aggregate_rule(16382, value) for value in range(14))
        == (0,) + (1,) * 13
        and all(
            aggregate_rule(10926, 2 * neighbors) == int(neighbors == 1)
            and aggregate_rule(10926, 2 * neighbors + 1) == 1
            for neighbors in range(7)
        )
    )
    ok &= hex_source_ok and hex_representation_ok
    print("source_lossless_hex_array_route", "OK" if hex_source_ok else "MISMATCH", 15608, 15612)
    print(
        "derived_hex_kernel_and_printed_rule_semantics",
        "OK" if hex_representation_ok else "MISMATCH", 6, 16382, 10926,
    )

    fixed_network_source_ok = (
        "each cell corresponds to a node in a network" in at(13658)
        and "same structure (or at least a limited number of possible structures)" in at(13658)
        and "only totalistic cellular automaton rules" in at(13658)
        and "assign a color to each node" in at(13909)
        and "update this color at each step" in at(13909)
        and "element i is  $\\{a, i, b\\}$" in at(13910)
        and "NetCAStep" in at(13913)
        and "list[[net]]" in at(13914)
        and "Totalistic rules depend only on the total number of black cells in a neighborhood" in at(13536)
        and "outer totalistic rules" in at(13536)
        and "also depend on the color of the center cell" in at(13536)
    )
    structural_network_control_ok = (
        "fixed underlying geometrical structure which remains unchanged" in at(2372)
        and "connections coming out of each node should be rerouted" in at(2426)
        and "different operations are performed at different nodes" in at(2464)
        and "connections from node *i* should be rerouted" in at(13835)
        and "new node should be inserted" in at(13835)
        and "only a single active node" in at(13889)
    )
    boolean_setup_control_ok = (
        "like cellular automata on networks" in at(13917)
        and "when they are set up each node has a rule" in at(13917)
        and "randomly chosen from all" in at(13917)
        and "$2^{2^s}$" in at(13917)
        and "possible ones with s inputs" in at(13917)
        and "averages are in effect taken over possible configurations" in at(13919)
        and {11563, 13917, 13918, 13919} <= CONTROL_EVIDENCE
    )
    # The executable Notes row is explicitly {above, Self, below}; it does not
    # support a neighbor-only/no-Self interpretation of the main-text word
    # "totalistic". This closed exact-one totalistic witness includes explicit
    # Self in every read tuple.
    fixed_net = ((1, 0, 2), (2, 1, 3), (3, 2, 0), (0, 3, 1))
    old_colors = (1, 0, 1, 0)
    read_colors = tuple(
        tuple(old_colors[node] for node in incidence)
        for incidence in fixed_net
    )
    new_colors = tuple(
        int(sum(reads) == 1)
        for reads in read_colors
    )
    fixed_network_derivation_ok = (
        all(incidence[1] == site for site, incidence in enumerate(fixed_net))
        and read_colors == ((0, 1, 1), (1, 0, 0), (0, 1, 1), (1, 0, 0))
        and new_colors == (0, 1, 0, 1)
    )
    sampled_boolean_incidence = ((1, 2), (0, 2), (0, 1))
    sampled_boolean_rule_bank = (
        (0, 1, 1, 0),  # XOR
        (0, 0, 0, 1),  # AND
        (1, 0, 0, 1),  # equality
    )
    sampled_boolean_old = (1, 0, 1)
    sampled_boolean_new = sampled_site_rule_step(
        sampled_boolean_old,
        sampled_boolean_incidence,
        sampled_boolean_rule_bank,
    )
    sampled_boolean_derivation_ok = sampled_boolean_new == (1, 1, 0)
    ok &= (
        fixed_network_source_ok
        and structural_network_control_ok
        and boolean_setup_control_ok
        and fixed_network_derivation_ok
        and sampled_boolean_derivation_ok
    )
    print(
        "fixed_network_ca_vs_structural_t29_boundary",
        "OK" if fixed_network_source_ok and structural_network_control_ok else "MISMATCH",
    )
    print(
        "random_boolean_setup_provenance_control",
        "OK" if boolean_setup_control_ok else "MISMATCH",
    )
    print(
        "derived_notes_fixed_incidence_snapshot_event_includes_self",
        "OK" if fixed_network_derivation_ok else "MISMATCH", *new_colors,
    )
    print(
        "derived_sampled_boolean_rule_bank_fixed_incidence_snapshot_event",
        "OK" if sampled_boolean_derivation_ok else "MISMATCH", *sampled_boolean_new,
    )

    historical_aliases = (
        "tessellation automata",
        "cellular spaces",
        "iterative automata",
        "homogeneous structures",
        "universal spaces",
    )
    alias_index_lines = {20970, 21253, 21362, 22150, 22390}
    boolean_index_lines = {
        20918, 21213, 21283, 21416, 21495,
        21687, 21689, 21771, 22134, 22426,
    }
    alias_variant_route_guards_ok = (
        all(alias in at(11503).lower() for alias in historical_aliases)
        and "cellular spaces see cellular automata" in at(20970).lower()
        and "homogeneous structures see cellular automata" in at(21253).lower()
        and "iterative automata" in at(21362).lower()
        and "see cellular automata" in at(21362).lower()
        and "tessellation automata" in at(22150).lower()
        and "see cellular automata" in at(22150).lower()
        and "universal spaces see cellular automata" in at(22390).lower()
        and "given a particular representation of a group or semigroup" in at(13994).lower()
        and "cayley graph is a 2d grid" in at(13994).lower()
        and "similar cayley graphs" in at(13996).lower()
        and "different choices of generators can yield cayley graphs" in at(14000).lower()
        and "simulations of random boolean networks" in at(11563).lower()
        and "each node has a rule that is randomly chosen" in at(13917).lower()
        and "averages are in effect taken over possible configurations" in at(13919).lower()
        and all("boolean networks" in at(line_no).lower() for line_no in boolean_index_lines)
        and 11503 in RELATION_EVIDENCE
        and {13994, 13996, 14000} <= RELATION_EVIDENCE
        and {11563, 13917, 13919} <= CONTROL_EVIDENCE
        and alias_index_lines == (
            set(INDEX_CLASS["historical_ca_alias_routes"]) | {22150}
        )
        and boolean_index_lines == (
            set(INDEX_CLASS["boolean_network_variant_routes"]) | {20918}
        )
    )
    ok &= alias_variant_route_guards_ok
    print(
        "historical_alias_cayley_boolean_route_guards",
        "OK" if alias_variant_route_guards_ok else "MISMATCH",
        len(historical_aliases), len(alias_index_lines), len(boolean_index_lines),
    )

    ca_slice_controls = {
        2202, 2204, 2206, 2910, 2912, 2918, 2930, 5334, 13575, 18778,
    }
    embedding_controls = {6376, 16717, 16875, 20118}
    boundary_vocabulary_guards_ok = (
        "one-dimensional slices through some of the two-dimensional cellular automata" in at(2202).lower()
        and "looking at such slices cannot reveal much" in at(2206).lower()
        and "code 942 slices" in at(13575).lower()
        and "represented as tessellations of rectangles" in at(14063).lower()
        and "any network can be laid out in 3d space" in at(16717).lower()
        and "whitney embedding theorem" in at(16717).lower()
        and "embeddings of networks" in at(21132).lower()
        and "bravais lattices, 929" in at(20940).lower()
        and "brillouin zones, 987 and ca lattices, 929" in at(20940).lower()
        and 20940 in INDEX_CLASS["t24_geometry_and_topology_routes"]
        and "honeycomb moray" in at(15944).lower()
        and ca_slice_controls <= CONTROL_EVIDENCE
        and embedding_controls <= CONTROL_EVIDENCE
        and {2600, 2618} <= EXCLUDED_CLASS["other_program_or_schedule_vocabulary"]
        and {15944} <= EXCLUDED_CLASS["unrelated_slice_embedding_or_honeycomb"]
        and {20980, 21132} == set(INDEX_CLASS["observer_or_embedding_routes"])
        and {20918, 20946, 21471, 22114, 22120, 22150, 22434}
        == set(INDEX_CLASS["mixed_t24_alias_variant_or_observer_routes"])
    )
    ok &= boundary_vocabulary_guards_ok
    print(
        "slice_embedding_tessellation_honeycomb_guards",
        "OK" if boundary_vocabulary_guards_ok else "MISMATCH",
        len(ca_slice_controls), len(embedding_controls),
    )

    controls_ok = (
        "general function is used" in at(11077)
        and "step number" in at(11077)
        and "continuous range of gray levels" in at(2018)
        and "introduce probabilities" in at(13314)
        and "updated sequentially rather than in parallel" in at(16446)
        and "only a single active node" in at(13889)
        and "when they are set up each node has a rule that is randomly chosen" in at(13917)
        and "alternating steps" in at(15708)
    )
    ok &= controls_ok
    print(
        "function_time_stochastic_setup_schedule_controls",
        "OK" if controls_ok else "MISMATCH",
    )

    structural = (
        len(RETAINED) == EXPECTED_SOURCE_COUNT
        and digest(RETAINED) == EXPECTED_SOURCE_DIGEST
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE == RETAINED
        and not RETAINED & index
        and matched_retained == set(RETAINED) & pre_index_union
        and governed == set(RETAINED) - union
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    # Close all split markdown copies with immutable manifests, complete query
    # enumeration, and deterministic reverse joins back to the monolith.
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
        len(split_records), digest_records(split_records), len(split_exact),
        digest_records(split_exact), len(split_nonexact), digest_records(split_nonexact),
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
        len(exact_retained), digest(exact_retained), len(nonexact_retained),
        digest(nonexact_retained), len(retained_mapping), digest_records(retained_mapping),
        len(monolith_only), digest(monolith_only),
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n for n, line in enumerate(atlas_lines, 1) if any(rx.search(line) for rx in compiled)
    }
    atlas_ok = (
        len(atlas_lines) == 542
        and (len(atlas_hits), digest(atlas_hits)) == EXPECTED_ATLAS_HITS
        and atlas_hits == {153}
        and atlas_lines[152] == "### Continuous Cellular Automata"
        and "higher-dimensional geometry enriches form" in atlas_lines[174]
        and "same core behavior classes persist" in atlas_lines[174]
    )
    ok &= atlas_ok
    print("atlas_summary_only", "OK" if atlas_ok else "MISMATCH", len(atlas_hits), digest(atlas_hits))

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[24] == "Higher-Dimensional Lattice Cellular Automata,"
        and len(set(catalog_lines[1:])) == 45
        and "## 24. Higher-Dimensional Lattice Cellular Automata" in taxonomy_text
        and "Fixed lattice in dimension `d`." in taxonomy_text
        and "finite alphabet" in taxonomy_text
        and "finite neighborhood is defined by offsets" in taxonomy_text
        and "All sites update in parallel." in taxonomy_text
        and "`neighborhood_offsets`" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only", "OK" if catalog_ok else "MISMATCH")

    architecture_inference_ok = (
        source_facts_ok
        and dimension_formula_ok
        and positional_ok
        and hex_rule_space_ok
        and geometry_source_ok
        and hex_source_ok
        and hex_representation_ok
        and fixed_network_source_ok
        and structural_network_control_ok
        and boolean_setup_control_ok
        and fixed_network_derivation_ok
        and sampled_boolean_derivation_ok
        and alias_variant_route_guards_ok
        and boundary_vocabulary_guards_ok
        and controls_ok
    )
    ok &= architecture_inference_ok
    print(
        "architecture_inference_parameterizes_shared_simple_program_event_with_sampled_rule_bank",
        "OK" if architecture_inference_ok else "MISMATCH",
    )

    unresolved_total = (
        len(pre_index_union - matched_retained - set(EXCLUDED))
        + len(index - set(INDEX_ROUTED))
        + len(monolith_only)
    )
    unresolved_ok = unresolved_total == 0
    ok &= unresolved_ok
    print("unresolved_total", "OK" if unresolved_ok else "MISMATCH", unresolved_total)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
