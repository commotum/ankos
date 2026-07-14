#!/usr/bin/env python3
"""Frozen primary-source audit for T23 Three-Dimensional Cellular Automata.

This is an evidence oracle, not a 3D cellular-automaton implementation and not
an argument for a construction-named executor.  It audits the Book's cubic
configuration, six-face and full 26-position access profiles, compact and
positional RULE representations, seeds/finite realizations, snapshot-parallel
UPDATE, named 3D presets, and observer-only views.  It treats T21, T22, T24,
T44, stochastic systems, history, complexity, and the actual Index as typed
relations or controls rather than silently widening T23.

The architectural inference tested here is deliberately narrower than the
source facts: rank three, declared offsets/case maps, and named restrictions
parameterize the same branch-free fixed-lattice SimpleProgram event.  Display
reversal, projections, seeds, run observations, and catalog vocabulary do not
define configuration coordinates, transition state, or an executor family.
Every frozen query hit has exactly one disposition and the unresolved remainder
is empty.
"""

from __future__ import annotations

import hashlib
import itertools
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T23 source oracle requires assertions; do not use -O")


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


# Q00--Q07 close direct names, cubic access, d-dimensional implementations,
# positional rules, views, class-4 presets, and the majority preset. Q08--Q12
# deliberately search stochastic, realization/update, T24, and T44 seams.
# Q13 closes T22/higher-dimensional aliases; Q14 symmetry/isotropy; Q15 the
# actual-Index vocabulary independently; Q16 seeds; Q17 rule restrictions;
# Q18 freezes the hostile-review discovery under Localized structures.
QUERIES = {
    "Q00": (
        r"\b(?:three[- ]dimensional|3D) cellular autom(?:aton|ata)\b|"
        r"\b3D CAs?\b"
    ),
    "Q01": (
        r"\bcubic lattices?\b|\b(?:six|6) neighbors?[^.]{0,120}\bface\b|"
        r"\ball 26 neighbors\b|\b26 neighbors\b|"
        r"\bshare either a face or a corner\b"
    ),
    "Q02": (
        r"\b(?:AxesTotal|FullTotal)\b|\b5-neighbor rules generalize\b|"
        r"\b9-neighbor rules generalize\b"
    ),
    "Q03": (
        r"\bk \(2 d \(k - 1\) \+ 1\)|"
        r"\bk \(\(3<sup>d</sup> - 1\) \(k - 1\) \+ 1\)|"
        r"\bCAStep\[\{rule_, d_\}"
    ),
    "Q04": (
        r"\bOne can specify the neighborhood for any rule in any dimension\b|"
        r"\boffset lists are always taken to be in the order\b|"
        r"\bA single step in evolution of a general cellular automaton\b"
    ),
    "Q05": (
        r"\bProjections from 3D\b|Graphics3D\[Map\[Cuboid|"
        r"\bDisplays? of 3D cellular automata\b|"
        r"\bGraphics3D and 3D cellular automata\b|"
        r"\bCuboid and 3D cellular automata\b"
    ),
    "Q06": (
        r"\b3D class 4 rules\b|\bLifeStep3D\b|\bCarter Bays\b|"
        r"\bclass 4 rules on\b[^.]{0,80}\bcubic\b"
    ),
    "Q07": r"\b3D majority cellular automaton\b|\bMajority cellular automaton\b",
    "Q08": (
        r"\b(?:stochastic|probabilistic|noisy) cellular automata\b|"
        r"\brandom initial conditions in\b"
    ),
    "Q09": (
        r"\b(?:cyclic|periodic|fixed|zero) boundary conditions?\b|"
        r"\bfinite array\b|\binitial condition contains?\b|"
        r"\binitial block of black cells\b"
    ),
    "Q10": (
        r"\b(?:all the cells[^.]{0,100}updated in parallel|"
        r"every cell is updated in parallel|old values of neighbors|"
        r"previous step[^.]{0,100}(?:neighbor|cell))\b"
    ),
    "Q11": (
        r"\bOther geometries\b|\bhexagonal prism\b|"
        r"\brhombic dodecahedron\b|\btruncated octahedron\b|"
        r"\bface-centered cubic\b|\bbody-centered cubic\b"
    ),
    "Q12": r"\bcontinuous cellular automata\b|\bcontinuous CAs\b",
    "Q13": (
        r"\bhigher[- ]dimensional cellular automata\b|"
        r"\b5-neighbor rules introduced\b|\b9-neighbor rules introduced\b|"
        r"\bMoore neighborhood\b|\bvon Neumann neighborhood\b|"
        r"\b(?:eight|8) neighbors\b|\bcode (?:number )?174826\b"
    ),
    "Q14": (
        r"\b(?:isotropy|symmetr(?:y|ies))\b[^.]{0,180}"
        r"\b(?:3D|three dimensions?|cubic lattice|cellular automata)\b|"
        r"\b(?:3D|three dimensions?|cubic lattice|cellular automata)"
        r"[^.]{0,180}\b(?:isotropy|symmetr(?:y|ies))\b"
    ),
    "Q15": (
        r"\b(?:Three-dimensional cellular automata|3D cellular automata|"
        r"3D CAs|Cubic lattices|Cuboid and 3D cellular automata|"
        r"Displays of 3D cellular automata|Graphics3D and 3D cellular automata|"
        r"3D class 4|Majority cellular automaton)\b"
    ),
    "Q16": (
        r"\bInitial conditions are constructed from init\b|"
        r"\bexplicit list of values in two dimensions\b|"
        r"\bpositive direction in each coordinate\b|"
        r"\bevolution list of length t\+1\b|\bIn any number of dimensions\b|"
        r"\bAutomatic can be used to trim off background\b"
    ),
    "Q17": (
        r"\bNumbers of possible rules\b|\bRules are considered rotationally\b|"
        r"\bTotalistic rules depend only on the total number\b|"
        r"\bGrowth totalistic rules make any cell\b"
    ),
    "Q18": r"\bin three dimensions 949\b",
}

EXPECTED_QUERY = {
    "Q00": (10, 5, 5, "f2013b2b3a19f3381967f98a5c5b2a084348b65cba40cf9fec5ee68ec779d650"),
    "Q01": (8, 7, 1, "50ee4d43e147a912b15fea54d8d474f6bed9d884bf4249df4e0286b60b04ad93"),
    "Q02": (7, 7, 0, "8679769f357f1667662c30b0f6fd0c571c2e8f7899e641222b962cefbaeb9f90"),
    "Q03": (3, 3, 0, "6052a6725ca11d892c5a258ff40351fe337a922b9e52634dede858d068209d14"),
    "Q04": (2, 2, 0, "4cde4076dbc89c3533e8674e944a8f27a341850407e22e6348fbb8ad979c4889"),
    "Q05": (4, 2, 2, "2b1857a8f464a87b3ae667f9e991812938dffc6022f2e2ec3e9e01afca4e7f31"),
    "Q06": (3, 3, 0, "89be316c9b9cccfbca456f04767c4408ace0e06753547f3084de6a7a4be14cc9"),
    "Q07": (2, 1, 1, "beea42b843208fd79b3be34e3389f60d9e1eff8c1c5760bc7c0e075f080c4fb1"),
    "Q08": (22, 11, 11, "76907c6f1e9d54297c8e48e02638e8fb0e92337fd0b5aea137ff4e349af76641"),
    "Q09": (16, 15, 1, "5e948fe0d2e312c29c5b3819793dd43d95328e35bc74eee48108afc450115701"),
    "Q10": (4, 4, 0, "05bbb098fd4acc1a9aaeeeccd5e9975f2bd13a80822f23d62a3a9a73195fbbc1"),
    "Q11": (11, 4, 7, "06c1b525a15db8fca6a4a8769fee9cccaf48d000adced8c9cb8fcd62497ef9c9"),
    "Q12": (40, 22, 18, "1c7b086269352983af41f016a399b69b820e90041739cd0745a07452c35e820c"),
    "Q13": (13, 10, 3, "6af56dcad3d8b7fc3a3fdf7d8143066da6b779281b93c2f6afdf4b6a547c803e"),
    "Q14": (12, 3, 9, "3495d304aa4fc25b770455197ca185f95fda6c394bf6ff024a67ebdaf7493430"),
    "Q15": (14, 7, 7, "fdb8988f94a0be1c42c9b7101c42875162ba9d5897822b9f1f4f039f6c5cd682"),
    "Q16": (13, 13, 0, "739f4a67d856c2eda9317c087ea730a01a26afde7a15aa23eea374df628df6a0"),
    "Q17": (3, 3, 0, "3b69fa045d438628a80e2c906aea86cc5193774b0451ba0b1b6e3514d2cf7013"),
    "Q18": (1, 0, 1, "70ed69b6f26f98cea25f99d53163821dc2d5535704c071950dcad20d7436040e"),
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


# 72 of 104 pre-Index query hits are retained. The other 32 are frozen broad
# query collisions below. The 66 governed lines close multiline code, tables,
# source-bound images, seed schemas, and observer/control continuations.
MATCHED_RETAINED = line_set(
    "850,1948,1986,2008,2014,2018,2102,2156,2212,2226,2234,2236,2238,"
    "2256,2262,2878,2880,2884,2890,2904,3784,3804,7084,7092,10984,10986,"
    "10992,11037,11077,11090,11092,11103,11124,11192,13281,13296,13314,"
    "13471,13475,13483,13486,13488,13490,13494,13497,13501,13503,13507,"
    "13511,13513,13520,13534,13536,13622,13632,13642,13644,13646,14234,"
    "14237,14263,14266,14271,14336,15074,15075,15293,15485,16446,17002,"
    "19072,19588"
)

GOVERNED_CONTINUATIONS = line_set(
    "2252,2254,2258,2260,11079-11087,11095-11100,11106-11107,11110,11112,"
    "11114,11116,11118,11120,11122,13485,13492,13495,13499,13505,13509,"
    "13515-13518,13522-13526,13528,13530-13531,13538,13540,13542-13549,"
    "13634,13636,13638,13640,13648,14265,14267-14269,14273"
)

RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS

# Stable public interface consumed by the T23 asset oracle. The first four are
# direct plates, the next four projection observers, 13648 a T24 topology
# control, and 14273 the source-listed (4,5,5) moving-structure observer.
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
GOVERNED_IMAGE_LINES = line_set(
    "2252,2254,2258,2260,13634,13636,13638,13640,13648,14273"
)

# Native evidence contains the smallest same-runner construction and exact
# named presets. View/run plates remain relations. T22/T24/T44 and stochastic
# material is control evidence even when its text is physically adjacent.
NATIVE_EVIDENCE = line_set(
    "850,2156,2256,2262,10984,10986,10992,11077,11079-11087,11090,11092,"
    "11095-11100,11103,11106-11107,11110,11112,11114,11116,11118,11120,"
    "11122,11124,13483,13485-13486,13488,13490,13492,13494-13495,13497,"
    "13499,13501,13503,13505,13507,13513,13515-13518,13520,13522-13526,"
    "13528,13530-13531,13534,13536,13538,13540,14263,14265-14269,14271,"
    "19588"
)
RELATION_EVIDENCE = line_set(
    "2236,2238,2252,2254,2258,2260,11192,13509,13511,13632,13634,13636,"
    "13638,13640,14273,15293"
)
CONTROL_EVIDENCE = line_set(
    "1948,1986,2008,2014,2018,2102,2212,2226,2234,2878,2880,2884,2890,"
    "2904,3784,3804,7084,7092,11037,13281,13296,13314,13471,13475,"
    "13542-13549,13622,13642,13644,13646,13648,14234,14237,14336,15074,"
    "15075,15485,16446,17002,19072"
)

EXCLUDED_CLASS = {
    "other_simple_program_or_dimension": line_set(
        "2366,10261,13756,14014,16161,16900,17770"
    ),
    "other_ca_family_or_observer": line_set(
        "466,3370,3902,4304,5806,11256,11953,13619,14301,14313,15221,"
        "16460,18755"
    ),
    "random_or_statistical_model": line_set(
        "3250,3258,14275,15338,15388,15392,17588"
    ),
    "other_geometry_or_physics": line_set("13332,15141,15149,15467"),
    "broad_rule_phrase": line_set("5576"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())

# The actual Index is routing vocabulary, never primary semantic evidence.
INDEX_CLASS = {
    "t23_routes": line_set("20910,20972,21068,21090,21231,21473,21495,22262"),
    "t22_t24_routes": line_set(
        "20918,21004,21170,21181,21243,21525,21934,22416"
    ),
    "t44_routes": line_set(
        "21046,21086,21189,21195,21223,21405,21434,21471,21475,21497,"
        "21711,21735,21771,21805,21815,21990,22352"
    ),
    "stochastic_routes": line_set(
        "21207,21550,21683,22096,22144,22150,22378"
    ),
    "symmetry_routes": line_set(
        "21114,21193,21513,21658,21927,22016,22136"
    ),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())


EXPECTED_SOURCE_COUNT = 138
EXPECTED_SOURCE_DIGEST = "92ce01dbf10875f7549f3eedb180a9001c72c588494247ec13d6b9f5d7160c07"
EXPECTED_SET = {
    "union": (151, "03268aed2534b66f807af417c006cf1a9209d195bc5d7f36d36b7a17134ae875"),
    "pre_index_union": (104, "6cc99039ed61f7e5c2566ebf71e9b0bc400637f5e1488452ee32d803f671afc5"),
    "index": (47, "739d429e33df93489ed54bfe36cbe013b498e7a11c53c27fd83a473d7478d22e"),
    "matched_retained": (72, "60b0151a40c057b0d457014835f118a2b3544ad982aa5c3a6492e304beceff13"),
    "governed_continuations": (66, "a34d522a306d42e688cfa8d10d41e790174db2e55bdf4feb607066c8d1ca8ab2"),
    "retained": (138, EXPECTED_SOURCE_DIGEST),
    "excluded": (32, "78e3f6a33102ab61399d5913a88f0ac7b0aed533a8b1e8bd1fe6383d1139dff9"),
    "native": (76, "f0ff42e8c0bd188cf78cbf809306d3543d0fce156c18ac17e88273bb823a3886"),
    "relation": (16, "17c8d2e0c7e6d0152f970d4f72a2d829a92143c4351747306175742da8458e02"),
    "control": (46, "83b1cbbc1f944a8ed1e7d05bfb125e662684d72d5528f652d22b7ca8ec56b889"),
    "governed_images": (10, "321e19bd6ddda35985b08d095c182b529076ce4eea99854230c5b512b6f115ef"),
}
EXPECTED_EXCLUDED_CLASS = {
    "other_simple_program_or_dimension": (7, "8e61eacd4f3bbc36702135dbf888362a48ba146cd77c0bf1ca808b4f0b756972"),
    "other_ca_family_or_observer": (13, "7e0bec9f13202b9640b0808e3b551acdf166589971715fd830fc0348562e1755"),
    "random_or_statistical_model": (7, "390cc07d1283f191614de9260887d4037bfbf081bfe7ed5f8bd5b9ae0023b1d0"),
    "other_geometry_or_physics": (4, "0144624cdc7db211717f0ea525aeba840708f8f9f87162cfed4e8e88cb057791"),
    "broad_rule_phrase": (1, "a398152fa8e559b07ad69683d6f51a0e9cefad1d0e0c495642fe10b2e1170417"),
}
EXPECTED_INDEX_CLASS = {
    "t23_routes": (8, "0ac2b1e75d049571dbb00db4429524b6b2438c552f04a8fc5606b5c976799aa4"),
    "t22_t24_routes": (8, "cecc07d8175bcf5e02d59ce2708037b6a2300388ba047c5604a51961ab7381af"),
    "t44_routes": (17, "7228e9b0a3064f40151340dd5fb4fdde8cdcf21ec2688d88dac23ef2cc2289b1"),
    "stochastic_routes": (7, "9230116c0996408425cc17c1f92c7cad18e1a3da0f5b67f764714cb5a5886149"),
    "symmetry_routes": (7, "ba062503b0797b305078805ded535690d027f2f14c7240b8aa5a3737f8de86c5"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY = (151, "c594bf08b9c675fc4693ce51dfe00513da4528b048c182e21fd4947e67b25413")
EXPECTED_SPLIT_QUERY_EXACT = (142, "6de73915b6d70b5fdde2565e102706b6cb50896bf3d67d9d62a2495573558ba0")
EXPECTED_SPLIT_QUERY_NONEXACT = (9, "2fe74b7de0c2013d050dee23c1b1da8a6c4441f1471ac1b5aea0110811fe4300")
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = "941b3d82e0d98afe43c0140ce29adf798d0249f73b7be6220c002465b5b38256"
EXPECTED_SPLIT_RETAINED_EXACT = (123, "ecb52f0ad759547f90ba7489c1a3e37ecd00ae8bc46f500f2a159eabfd8e989e")
EXPECTED_SPLIT_RETAINED_NONEXACT = (15, "e12bcb3afdc3877683c9712a253e00f6380072318e4c1821781146bd1aaca3c7")
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = "f0cf3bc772b722907d69fdc91cbd9f07a49cc59e5e20f5e42c172ec3af119a12"
EXPECTED_MONOLITH_ONLY = (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
EXPECTED_ATLAS_HITS = (2, "3222ed71a3afde66b68d8e493f55c4854b897b9cb71748893a433513ff1eba1a")


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def best_witness(canonical: str, split_lines: list[tuple[str, str]]) -> tuple[str, float]:
    """Return a deterministic high-overlap split witness for a monolith line."""
    canonical_tokens = set(normalized_line(canonical).split())
    scored: list[tuple[float, str]] = []
    for record, normalized in split_lines:
        split_tokens = set(normalized.split())
        denominator = min(len(canonical_tokens), len(split_tokens))
        score = len(canonical_tokens & split_tokens) / denominator if denominator else 0.0
        scored.append((score, record))
    score, record = max(scored, key=lambda item: (item[0], item[1]))
    return record, score


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def periodic_step(
    state: tuple[tuple[tuple[int, ...], ...], ...],
    offsets: tuple[tuple[int, int, int], ...],
    rule: object,
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Independent finite-quotient witness for one old-snapshot local event."""
    nx, ny, nz = len(state), len(state[0]), len(state[0][0])
    output: list[list[list[int]]] = [
        [[0 for _ in range(nz)] for _ in range(ny)] for _ in range(nx)
    ]
    for x, y, z in itertools.product(range(nx), range(ny), range(nz)):
        reads = tuple(
            state[(x + dx) % nx][(y + dy) % ny][(z + dz) % nz]
            for dx, dy, dz in offsets
        )
        output[x][y][z] = rule(state[x][y][z], reads)  # type: ignore[operator]
    return tuple(tuple(tuple(row) for row in plane) for plane in output)


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 35-T23-source-oracle.py [BOOK]")
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

    excluded_ok = set().union(*EXCLUDED_CLASS.values()) == EXCLUDED
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    excluded_ok &= pre_index_union == set(MATCHED_RETAINED) | set(EXCLUDED)
    ok &= excluded_ok
    print("unresolved_pre_index", "OK" if excluded_ok else "MISMATCH", 0)

    index_ok = set().union(*INDEX_CLASS.values()) == index
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        print(f"index_{name}", "OK" if good else "MISMATCH", *actual)
    ok &= index_ok
    print("unresolved_index", "OK" if index_ok else "MISMATCH", 0)

    localized_route_ok = (
        hits["Q18"] == {21473}
        and 21473 in INDEX_CLASS["t23_routes"]
        and "same in different 2D rules, 949" in at(21473)
        and "in three dimensions 949" in at(21473)
    )
    ok &= localized_route_ok
    print(
        "localized_structures_3d_index_route",
        "OK" if localized_route_ok else "MISMATCH", 21473,
    )

    derived_images = {n for n in RETAINED if IMAGE_RE.fullmatch(at(n))}
    images_ok = derived_images == set(GOVERNED_IMAGE_LINES)
    ok &= images_ok
    print(
        "governed_image_interface", "OK" if images_ok else "MISMATCH",
        len(derived_images), digest(derived_images),
    )

    # Source facts: do not silently repair the Book's wording. Line 2262 says
    # face or corner, not edge; the 6/12/8 decomposition below is a separately
    # labelled geometric derivation from all 26 {-1,0,1}^3 positions.
    source_facts_ok = (
        "shown is a cubic lattice" in at(2156)
        and "any of the six neighbors with which it shares a face" in at(2256)
        and "exactly one of its six neighbors" in at(2256)
        and "initial condition contains a single black cell" in at(2256)
        and "all 26 neighbors that share either a face or a corner" in at(2262)
        and "exactly two of its 26 neighbors" in at(2262)
        and "line of three black cells" in at(2262)
        and "edge" not in at(2262).lower()
        and "In d dimensions with k colors" in at(13483)
        and "a + k AxesTotal[a, d]" in at(13488)
        and "IdentityMatrix[d]" in at(13492)
        and "k (2 d (k - 1) + 1)" in at(13494)
        and "3<sup>d</sup> -neighbor rules" in at(13497)
        and "a + k FullTotal[a, d]" in at(13501)
        and "Table[3, {d}]" in at(13505)
        and "(3<sup>d</sup> - 1) (k - 1) + 1" in at(13507)
    )
    ok &= source_facts_ok
    print("source_facts_cubic_access_and_formulas", "OK" if source_facts_ok else "MISMATCH")

    face_offsets = tuple(
        sorted(
            tuple(sign if coordinate == axis else 0 for coordinate in range(3))
            for axis in range(3)
            for sign in (-1, 1)
        )
    )
    full_with_self = tuple(sorted(itertools.product((-1, 0, 1), repeat=3)))
    full_offsets = tuple(offset for offset in full_with_self if offset != (0, 0, 0))
    faces = {offset for offset in full_offsets if sum(map(abs, offset)) == 1}
    edges = {offset for offset in full_offsets if sum(map(abs, offset)) == 2}
    corners = {offset for offset in full_offsets if sum(map(abs, offset)) == 3}

    signed_permutations = {
        (permutation, signs)
        for permutation in itertools.permutations(range(3))
        for signs in itertools.product((-1, 1), repeat=3)
    }
    proper_rotations = {
        (permutation, signs)
        for permutation, signs in signed_permutations
        if permutation_sign(permutation) * signs[0] * signs[1] * signs[2] == 1
    }

    def transform(
        offset: tuple[int, int, int],
        transform_spec: tuple[tuple[int, ...], tuple[int, ...]],
    ) -> tuple[int, int, int]:
        permutation, signs = transform_spec
        return tuple(signs[i] * offset[permutation[i]] for i in range(3))  # type: ignore[return-value]

    cubic_geometry_ok = (
        len(face_offsets) == 6
        and len(full_with_self) == 27
        and full_with_self[13] == (0, 0, 0)
        and len(full_offsets) == 26
        and (len(faces), len(edges), len(corners)) == (6, 12, 8)
        and faces | edges | corners == set(full_offsets)
        and not (faces & edges or faces & corners or edges & corners)
        and len(signed_permutations) == 48
        and len(proper_rotations) == 24
        and all(
            {transform(offset, symmetry) for offset in face_offsets} == set(face_offsets)
            and {transform(offset, symmetry) for offset in full_offsets} == set(full_offsets)
            for symmetry in signed_permutations
        )
    )
    ok &= cubic_geometry_ok
    print(
        "derived_cubic_geometry_and_symmetry",
        "OK" if cubic_geometry_ok else "MISMATCH", 6, 12, 8, 24, 48,
    )

    # These counts are arithmetic consequences of the source formulas, not
    # counts printed for T23. The printed table at 13534--13549 is explicitly
    # 2D and is retained only to source the restriction vocabulary.
    k = 2
    face_product_cases = k * (2 * 3 * (k - 1) + 1)
    full_product_cases = k * (((3**3 - 1) * (k - 1)) + 1)
    face_positional_contexts = k ** (len(face_offsets) + 1)
    full_positional_contexts = k ** (len(full_offsets) + 1)
    counts_ok = (
        (face_product_cases, full_product_cases) == (14, 54)
        and (face_positional_contexts, full_positional_contexts) == (128, 134217728)
        and (2 ** (len(face_offsets) + 1), 2 ** (len(full_offsets) + 1)) == (128, 134217728)
        and "total number of 2D rules" in at(13534)
        and "rotational symmetry" in at(13536)
        and "Totalistic rules depend only" in at(13536)
        and "outer totalistic rules" in at(13536)
        and "Growth totalistic rules" in at(13536)
        and "$2^{512}" in at(13544)
        and "$2^{18}" in at(13547)
        and "$2^{10} = 1024" in at(13548)
        and "$2^9 = 512" in at(13549)
    )
    ok &= counts_ok
    print(
        "derived_3d_case_and_rule_exponents",
        "OK" if counts_ok else "MISMATCH",
        face_product_cases, full_product_cases,
        face_positional_contexts, full_positional_contexts,
    )

    positional_ok = (
        "offset lists are always taken to be in the order given by *Sort*" in at(13513)
        and "same order as the offset list" in at(13513)
        and "IntegerDigits[i - 1" in at(13516)
        and "k, Length[os]" in at(13517)
        and "FromDigits[Reverse[u], k]" in at(13520)
        and "IntegerDigits[num, k, k^Length[os]]" in at(13523)
        and "ListCorrelate" in at(13531)
        and full_with_self == tuple(itertools.product((-1, 0, 1), repeat=3))
    )
    ok &= positional_ok
    print("source_positional_order_and_codec", "OK" if positional_ok else "MISMATCH")

    # Exhaust all aggregate input cases, including Self, for the four direct
    # examples and the three Carter Bays presets. This proves they are typed
    # table restrictions, not reasons for a distinct UPDATE or executor.
    direct_rules = {
        "face_any": (6, lambda center, count: int(count >= 1)),
        "face_exactly_1": (6, lambda center, count: int(count == 1)),
        "full_exactly_1": (26, lambda center, count: int(count == 1)),
        "full_exactly_2": (26, lambda center, count: int(count == 2)),
    }
    direct_tables = {
        name: tuple(rule(center, count) for count in range(size + 1) for center in range(2))
        for name, (size, rule) in direct_rules.items()
    }
    direct_rules_ok = (
        all(
            table[2 * count] == table[2 * count + 1]
            for name, table in direct_tables.items()
            for count in range(direct_rules[name][0] + 1)
        )
        and tuple(map(len, direct_tables.values())) == (14, 14, 54, 54)
    )

    named_presets = ((5, 7, 6), (4, 5, 5), (5, 6, 5))

    def life3d(preset: tuple[int, int, int], center: int, count: int) -> int:
        p, q, birth = preset
        return int((center == 1 and p <= count <= q) or count == birth)

    class4_ok = (
        "3D class 4 rules" in at(14263)
        and "With a cubic lattice" in at(14263)
        and "LifeStep3D" in at(14266)
        and "#1 == 1" in at(14267)
        and "p \\le #2 \\le q" in at(14267)
        and "#2 == r" in at(14267)
        and "{i, -1, 1}" in at(14268)
        and "-a" in at(14268)
        and "{5, 7, 6}, {4, 5, 5}, and {5, 6, 5}" in at(14271)
        and all(
            len(tuple(life3d(preset, center, count) for count in range(27) for center in range(2))) == 54
            for preset in named_presets
        )
        and all(life3d((4, 5, 5), 0, count) == int(count == 5) for count in range(27))
        and all(life3d((4, 5, 5), 1, count) == int(count in {4, 5}) for count in range(27))
    )
    ok &= direct_rules_ok and class4_ok
    print("direct_and_named_presets_all_cases", "OK" if direct_rules_ok and class4_ok else "MISMATCH")

    majority_table = tuple(
        int(center + count >= 4) for count in range(7) for center in range(2)
    )
    majority_ok = (
        "3D majority cellular automaton" in at(19588)
        and "UnitStep[a+AxesTotal[a, 3]-4]" in at(19588)
        and len(majority_table) == 14
        and all(
            majority_table[2 * count + center] == int(center + count >= 4)
            for count in range(7) for center in range(2)
        )
    )
    ok &= majority_ok
    print("majority_named_preset_all_cases", "OK" if majority_ok else "MISMATCH")

    # One native event through one old snapshot. Shape (1,2,3) deliberately
    # aliases several offsets to the same physical quotient cell; every declared
    # slot is still read, so multiplicity is not silently deduplicated.
    state = tuple(
        tuple(
            tuple((7 * x + 3 * y + z) % 2 for z in range(3))
            for y in range(2)
        )
        for x in range(1)
    )
    face_any = periodic_step(state, face_offsets, lambda center, reads: int(sum(reads) >= 1))
    face_exact = periodic_step(state, face_offsets, lambda center, reads: int(sum(reads) == 1))
    full_exact = periodic_step(state, full_offsets, lambda center, reads: int(sum(reads) == 2))
    class4_second = periodic_step(
        state, full_offsets, lambda center, reads: life3d((4, 5, 5), center, sum(reads))
    )
    snapshot_ok = (
        "updated in parallel at every step" in at(850)
        and "old values of neighbors" in at(10984)
        and "two copies of the array" in at(10984)
        and "finite array" in at(10986)
        and "cyclic array" in at(10986)
        and "automatically gets cyclic boundary conditions" in at(10992)
        and all(value in {0, 1} for result in (face_any, face_exact, full_exact, class4_second)
                for plane in result for row in plane for value in row)
        and len(face_any) == len(state)
        and len(face_any[0]) == len(state[0])
        and len(face_any[0][0]) == len(state[0][0])
    )
    ok &= snapshot_ok
    print("one_event_snapshot_parallel_with_alias_multiplicity", "OK" if snapshot_ok else "MISMATCH")

    seeds_views_ok = (
        "Initial conditions are constructed from init" in at(11077)
        and "explicit list of values in two dimensions" in at(11090)
        and "positive direction in each coordinate" in at(11092)
        and "evolution list of length t+1" in at(11103)
        and "In any number of dimensions" in at(11124)
        and "always the same size" in at(11124)
        and "Automatic can be used to trim off background" in at(11124)
        and "positions of black cells can conveniently be displayed" in at(13509)
        and "Cuboid[-Reverse[#]]" in at(13511)
        and "Looking from above, with closer cells shown darker" in at(13632)
        and "after 30 steps" in at(13632)
        and "$3\\times3\\times1$" in at(13632)
        and "$3\\times1\\times1$" in at(13632)
    )
    ok &= seeds_views_ok
    print("seed_realizations_and_observer_only_views", "OK" if seeds_views_ok else "MISMATCH")

    controls_ok = (
        "9-neighbor rules introduced" in at(13475)
        and "Other geometries" in at(13642)
        and "cube (6)" in at(13644)
        and "hexagonal prism (8)" in at(13644)
        and "truncated octahedron" in at(13646)
        and "probabilistic cellular automata" in at(7084)
        and "introduce probabilities" in at(13314)
        and "Noisy cellular automata" in at(15075)
        and "Continuous Cellular Automata" in at(1948)
        and "continuous range of gray levels" in at(2018)
        and "updated sequentially rather than in parallel" in at(16446)
        and not NATIVE_EVIDENCE & line_set("7084,7092,13314,14234,15075")
    )
    ok &= controls_ok
    print("t22_t24_t44_stochastic_and_schedule_controls", "OK" if controls_ok else "MISMATCH")

    structural = (
        len(RETAINED) == EXPECTED_SOURCE_COUNT
        and digest(RETAINED) == EXPECTED_SOURCE_DIGEST
        and MATCHED_RETAINED == matched_retained
        and GOVERNED_CONTINUATIONS == governed
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE == RETAINED
        and not RETAINED & index
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    # Close every split markdown copy with immutable file hashes, complete query
    # enumeration, and deterministic reverse joins to the monolith.
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
        and atlas_hits == {153, 175}
    )
    ok &= atlas_ok
    print("atlas", "OK" if atlas_ok else "MISMATCH", len(atlas_hits), digest(atlas_hits))

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[23] == "Three-Dimensional Cellular Automata,"
        and len(set(catalog_lines[1:])) == 45
        and "## 23. Three-Dimensional Cellular Automata" in taxonomy_text
        and "Six face-sharing neighbors." in taxonomy_text
        and "Twenty-six neighbors sharing either a face, edge, or corner." in taxonomy_text
        and "All cells update in parallel." in taxonomy_text
        and "`dimension`: `3`." in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only", "OK" if catalog_ok else "MISMATCH")

    # Explicit source/inference boundary: the source establishes mechanics and
    # views above; this classification is the governed architectural conclusion.
    architecture_inference_ok = (
        cubic_geometry_ok
        and counts_ok
        and direct_rules_ok
        and class4_ok
        and snapshot_ok
        and controls_ok
        and len(GOVERNED_IMAGE_LINES) == 10
    )
    ok &= architecture_inference_ok
    print(
        "architecture_inference_parameterizes_shared_simple_program_event",
        "OK" if architecture_inference_ok else "MISMATCH",
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
