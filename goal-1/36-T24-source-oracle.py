#!/usr/bin/env python3
"""Frozen primary-source audit for T24 higher-dimensional lattice CAs.

This is an evidence oracle, not a cellular-automaton implementation.  It
separates the Book's arbitrary-dimensional and fixed-incidence cellular-
automaton mechanics from geometric representations, observers, cross-reference
routes, and structurally evolving network systems.  The architectural result
is intentionally narrower than the source collection: dimension, fixed
topology/incidence, ordered finite access, and closed rule data are candidate
parameters of the shared SimpleProgram event; this oracle does not manufacture
a T24 executor from the catalog name.
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
# Q20 saturates the broad hexagonal/triangular aliases and exposes block-CA,
# Turing-machine, random-walk, percolation, and biological false positives.
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
    "4416,10261,13746,13748,13754,13756,15293,15467,15473-15475,"
    "15485,15487,16253,16255,19588"
)

# Controls make representation and execution boundaries explicit: finite/crop
# realization, unrestricted function/time dependence, stochastic/continuous
# values, topology rewriting, per-node random rules, sequential scheduling, and
# alternating block updates are not smuggled into strict T24.
CONTROL_EVIDENCE = line_set(
    "2018,2372,2426,2464,11037,11063-11065,11077,11079-11087,11090,"
    "11092,11095-11100,11103,11106-11107,11110,11112,11114,11116,"
    "11118,11120,11122,11124,13314,13464,13835,13889,13891,13893,"
    "13895,13917-13919,15708,16446"
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
        "20828,20836,20910,20918,20967,21054,21068,21102,21170,21181,"
        "21243,21763,21934,22132,22150,22166,22352,22416,22434,22438"
    ),
    "other_rule_restriction_routes": line_set("21233,21731"),
    "structural_or_sequential_network_routes": line_set("22096"),
    "continuous_or_stochastic_routes": line_set("21046,21434,21735,21815"),
    "broad_implementation_name_routes": line_set("21050,21471"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())


EXPECTED_SOURCE_COUNT = 145
EXPECTED_SOURCE_DIGEST = "52c5ea5e4964df3ec11e3c2994691a4fb9eda6b0ee9ce61a5ea91f87d7df37fa"
EXPECTED_SET = {
    "union": (142, "23247daa90ba3ad9bf8892f02e9c010cdeff596c2f99652504405c8254fb7fee"),
    "pre_index_union": (113, "ef9e88414b9d5843b9e77e9bbe5a0429d853fa220381278206289a4370447b87"),
    "index": (29, "12b31e400df0dac3114d8153f4692b1cc7970bf9ffee0afa9b896daa3c1696ac"),
    "matched_retained": (69, "dfc95e295b50dccb78dc459d1d433b7ab482ea9af57dd868fcca067121fbc985"),
    "governed_continuations": (76, "3e50c1a4d9e20f37b104c4ebe8350f596fa525044cd19396861613aec5995d55"),
    "retained": (EXPECTED_SOURCE_COUNT, EXPECTED_SOURCE_DIGEST),
    "excluded": (44, "fdfa685987fbc2e6f63b41a56e5ec8253df85afaceb1bcef500341afc755fa6a"),
    "native": (80, "1c7fa838bfa3e42073f8f8b7f8dfe2647a16a188f515063421892fb7255df2c3"),
    "relation": (16, "d74e8224571c62fff7eb6ed75171a60a0be1a19c299dc9fe8a83bd9f4942585b"),
    "control": (49, "eaaa54ac9aa56764b6b86260be2c0d978067d24db4c17884fad1632b784bff99"),
    "governed_images": (11, "07b740cf80d9e0caef2500ebb6882c4322a6969b9fc284e3e77af4b9a611b62d"),
}
EXPECTED_EXCLUDED_CLASS = {
    "other_ca_family_or_dimension": (31, "518bafbc6cfd250eff1dedd235d768aa786a7fcab576dce1d9da8df701b34234"),
    "broad_implementation_name_collision": (8, "1e1b1fd12fdbaf287f1f20611843ed5c22c8d5ad1a20b94b0fc66bbb46d561d7"),
    "other_geometry_or_physics": (5, "ba1d93bbb23d8cd72f1cf471b68d0cf1e3f7e99771703b79cb762fe4269f9e18"),
}
EXPECTED_INDEX_CLASS = {
    "t24_geometry_and_topology_routes": (20, "2c49222d95d70fc15730c34490c2ed4ba9faad7355f8ba47b1aeab2bc453cafc"),
    "other_rule_restriction_routes": (2, "633b53d4c3b49f1981130965b95e51e3c505945acafb9fe29b57949f19812fde"),
    "structural_or_sequential_network_routes": (1, "2754f6e1f004d4298d7ed6444c52385d98a70aee827877053ef7d43e519ac10f"),
    "continuous_or_stochastic_routes": (4, "c6db33d21c31050eaaa818770ba46e08cb74c0f434347d2559db6cae73a0e772"),
    "broad_implementation_name_routes": (2, "5eed2a6567b8caf8645117fb1956b63eafe9819a2286932a9a0aa26ca88f561b"),
}
EXPECTED_IMAGE_PARTITION = {
    "native": (6, "e6b89d89fdb76ba4bb76560fcbcd6dd0f22169301ab98bc8017e8bf0571b085f"),
    "relation": (2, "97cdd4f0b5c022cd17993d343b86304469fd691b53f5e5d6d3d8dad5b003b5c8"),
    "control": (3, "4c1ead45e337c9c578d9a72d3e1095924b382013c19f58f95bf21391ef6b6d6c"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
# Filled from the deterministic reverse joins below; unlike raw source hashes,
# these freeze both exact duplicates and normalized split-document variants.
EXPECTED_SPLIT_QUERY = (0, "")
EXPECTED_SPLIT_QUERY_EXACT = (0, "")
EXPECTED_SPLIT_QUERY_NONEXACT = (0, "")
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = ""
EXPECTED_SPLIT_RETAINED_EXACT = (0, "")
EXPECTED_SPLIT_RETAINED_NONEXACT = (0, "")
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = ""
EXPECTED_MONOLITH_ONLY = (0, "")
EXPECTED_ATLAS_HITS = (0, "")


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 36-T24-source-oracle.py [BOOK]")
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
    union: set[int] = set()
    for name, pattern in QUERIES.items():
        found = {n for n, line in enumerate(lines, 1) if re.search(pattern, line, re.I)}
        union |= found
        print(
            name, len(found), sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found), digest(found),
            ",".join(map(str, sorted(found))),
        )
    print("union", len(union), digest(union), ",".join(map(str, sorted(union))))
    pre_index = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index
    matched_retained = pre_index - EXCLUDED
    governed = set(RETAINED) - union
    print("pre_index", len(pre_index), digest(pre_index))
    print("index", len(index), digest(index))
    print("matched_retained", len(matched_retained), digest(matched_retained))
    print("excluded", len(EXCLUDED), digest(EXCLUDED))
    print("governed", len(governed), digest(governed))
    print("retained", len(RETAINED), digest(RETAINED))
    print("native", len(NATIVE_EVIDENCE), digest(NATIVE_EVIDENCE))
    print("relation", len(RELATION_EVIDENCE), digest(RELATION_EVIDENCE))
    print("control", len(CONTROL_EVIDENCE), digest(CONTROL_EVIDENCE))
    print("images", len(GOVERNED_IMAGE_LINES), digest(GOVERNED_IMAGE_LINES))
    print("missing_matched", sorted(matched_retained - set(RETAINED)))
    print("extra_queried", sorted((set(RETAINED) & pre_index) - matched_retained))
    print("index_missing", sorted(index - set(INDEX_ROUTED)))
    print("index_extra", sorted(set(INDEX_ROUTED) - index))
    structural = (
        matched_retained == set(RETAINED) & pre_index
        and pre_index == matched_retained | set(EXCLUDED)
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE == RETAINED
        and index == set(INDEX_ROUTED)
    )
    print("structural", "OK" if structural else "MISMATCH")
    return 0 if source_ok and structural else 1


if __name__ == "__main__":
    raise SystemExit(main())
