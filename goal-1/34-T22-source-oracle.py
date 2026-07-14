#!/usr/bin/env python3
"""Frozen primary-source audit for T22 Moore-Neighborhood Cellular Automata.

This is an evidence oracle, not a cellular-automaton implementation.  It treats
``src/ca`` as the shared SimpleProgram algebra and tests the narrower claim the
Book actually supports: T22 reuses fixed square support, AllSites, old-snapshot
parallel commit, and finite alphabets while parameterizing the access profile
and RULE schema.  Eight surrounding offsets and Self are distinct typed roles;
``9-neighbor`` is the Book's name for their nine-position read, not evidence for
a family executor or an implicit center.

The audit closes the direct examples and codes 175850/746/174826, Notes code and
rule counts, Game of Life, seeds/realizations, observers, actual-Index aliases,
split mirrors, source-bound images, and T21/T23/T24 controls.  Every query hit
has exactly one disposition and the unresolved remainder is empty.
"""

from __future__ import annotations

import hashlib
import itertools
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T22 source oracle requires assertions; do not use -O")


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


# Q00--Q03 close the Moore/9-position direct names, named codes, Notes
# implementation, and exact rule counts. Q04--Q08 close Life and the named
# shape/anisotropy observations. Q09--Q13 are T21/T23/T24/update/history
# controls. Q14 independently closes actual-Index aliases; Q15 closes the
# positional codec; Q16 closes the Life universality relation.
QUERIES = {
    "Q00": (
        r"\bMoore neighborhood\b|\b(?:eight|8)[ -]neighbors?\b|"
        r"\b9\s*[- ]\s*(?:neighbor|cell)(?:hood)?s?\b|\bnine[- ]neighbors?\b|"
        r"\bincluding diagonals\b|\bdiagonal neighbors?\b"
    ),
    "Q01": r"\b(?:code(?: number)?\s*)?(?:175850|174826|746)\b",
    "Q02": (
        r"\b(?:9-neighbor rules introduced|FullTotal|LifeStep3?D?|LifeSten)\b|"
        r"IntegerDigits\[code, 2, 18\]|ListConvolve\[\{\{2, 2, 2\}"
    ),
    "Q03": r"2\^\{512\}|2\^\{18\}|2\^\{10\} = 1024|2\^9 = 512|262,144 9-neighbor",
    "Q04": r"\bGame of Life\b|\bConway(?:\x27s)? Life\b|\bLife 2D cellular automaton\b|\bHighLife\b",
    "Q05": (
        r"\b(?:rough surface|closely approximates? a circle|approximate circle|"
        r"stopped growing|go on growing forever|row of (?:7|eleven|11) black cells|"
        r"rows of black cells of various lengths)\b"
    ),
    "Q06": (
        r"\b(?:glider gun|spaceships? \(in Game of Life\)|persistent structures?"
        r"[^.]{0,120}\bLife\b|unbounded growth in Life|sparse computation in Game of Life|"
        r"structures in Life)\b"
    ),
    "Q07": (
        r"\b(?:8[- ]neighbor|9\s*[- ]\s*neighbor|nine[- ]neighbor)[^.]{0,160}"
        r"\b(?:outer totalistic|totalistic|growth totalistic|code)\b|"
        r"\b(?:outer totalistic|totalistic|growth totalistic|code)[^.]{0,160}"
        r"\b(?:8[- ]neighbor|9\s*[- ]\s*neighbor|nine[- ]neighbor)\b"
    ),
    "Q08": (
        r"\b(?:anisotropy|orientation dependence|limiting shapes?|surface tension|"
        r"circular growth)[^.]{0,200}\b(?:code 746|8[- ]neighbor|"
        r"9\s*[- ]\s*neighbor|Life)\b|\b(?:code 746|8[- ]neighbor|"
        r"9\s*[- ]\s*neighbor|Life)[^.]{0,200}\b(?:anisotropy|orientation dependence|"
        r"limiting shapes?|surface tension|circular growth)\b"
    ),
    "Q09": r"\b(?:five|5)[ -](?:neighbor|cell)(?:hood)?s?\b|\bfour (?:neighbors|directions)\b|\bvon Neumann neighborhood\b",
    "Q10": r"\b(?:three[- ]dimensional|3D) cellular autom(?:aton|ata)\b|\b3D CAs?\b|\b26 neighbors\b",
    "Q11": (
        r"\b(?:hexagonal|triangular) (?:grid|lattice|neighborhood)\b|"
        r"\bother geometries\b|\bPenrose tiling\b|"
        r"\bhigher[- ]dimensional cellular automata?\b"
    ),
    "Q12": (
        r"\b(?:all the cells[^.]{0,80}updated in parallel|every cell is updated in parallel|"
        r"old values of neighbors|previous step[^.]{0,80}(?:neighbor|cell)|"
        r"cyclic boundary conditions|periodic boundary conditions)\b"
    ),
    "Q13": (
        r"\b(?:Edward Moore|John Conway|William Gosper|Tommaso Toffoli|Norman Margolus)"
        r"\b[^.]{0,240}\b(?:cellular autom(?:aton|ata)|Game of Life|Life|9-cell|simulator)|"
        r"\b(?:cellular autom(?:aton|ata)|Game of Life|Life|9-cell|simulator)[^.]{0,240}"
        r"\b(?:Edward Moore|John Conway|William Gosper|Tommaso Toffoli|Norman Margolus)\b"
    ),
    "Q14": (
        r"\b(?:Moore neighborhood|9-neighbor square|9-cell neighborhood|Game of Life|"
        r"Code 175850|Code 746|Code 174826|Anisotropy in code 746|"
        r"Sparse computation in Game of Life)\b"
    ),
    "Q15": (
        r"\b(?:One can specify the neighborhood for any rule in any dimension|"
        r"offset lists are always taken to be in the order|same order as the offset list|"
        r"A single step in evolution of a general cellular automaton)\b"
    ),
    "Q16": (
        r"\b(?:Life|Game of Life)[^.]{0,200}\bunivers(?:al|ality)\b|"
        r"\bunivers(?:al|ality)[^.]{0,200}\b(?:Life|Game of Life)\b"
    ),
}

EXPECTED_QUERY = {
    "Q00": (23, 20, 3, "68b470a75c894f61e67ec2d829eefb9d8ccf32d96e86f235c733b79a15e71d21"),
    "Q01": (18, 9, 9, "59354c97a35024a8fa86ecea2629d835320663a218efaf7a193269f842bc3ca2"),
    "Q02": (8, 8, 0, "00f32135d9635b43bda8866bde414c2ecb3fec1926f908622b4c00d948be4a95"),
    "Q03": (5, 5, 0, "6a75d9b6e8bfc181551922dfa52e51398855b07e70e0456477f4f76525709756"),
    "Q04": (37, 13, 24, "7c142c7e96642aa57798f18029c93df98d5878d594e6f70228502b0c8742fa25"),
    "Q05": (7, 7, 0, "bc7f508509a4e317c3c4ee078af1ef25f59b0f9549dfac66a501b57e7962f330"),
    "Q06": (8, 4, 4, "e1924605dc2a926038347cd10c2e034f8a69527d1291a5441dc0881ce4b26290"),
    "Q07": (8, 8, 0, "e08af49926ddb266660ec5703102edca229424ed24f59db2fa3326cf951baa3e"),
    "Q08": (2, 0, 2, "3e200fd8303cdc59ce9b56ce0306889707b2251f5afeff4a7c399488531b0f1f"),
    "Q09": (34, 32, 2, "9a9ccf6e5fd6baa3a8946a13c162a7e7c4700f53bb61ca92caa1cb2a580f5c22"),
    "Q10": (11, 6, 5, "ea81ae9d5afd56675ad42902fd9b05258aff2783e4777fbf1fa41a3e3c0f25ad"),
    "Q11": (17, 15, 2, "f97ce16acfbb76156a5c328ffb8922dbed33105abb1efcdeb85d73d650d0c537"),
    "Q12": (14, 13, 1, "6a6b4f62f4ce36963f37f1ef4a5444b4e5563060f36f40e422bebbc271f07eaf"),
    "Q13": (6, 6, 0, "dd393449755fe7eb639f02bbbbac0c8860bccfeec1d2637e8d7915e30b4af4bb"),
    "Q14": (48, 19, 29, "e1da40a2b74fc4c3a44084399d88f3ae5da7b29ea64e359b8a76ccbac86cf19d"),
    "Q15": (2, 2, 0, "4cde4076dbc89c3533e8674e944a8f27a341850407e22e6348fbb8ad979c4889"),
    "Q16": (15, 2, 13, "5b3d9f6ccd123791b5f4a170635d13a77d38b66b380f57d43ec67415626f7c7e"),
}


def line_set(spec: str) -> frozenset[int]:
    """Parse a comma-separated set of line numbers and inclusive ranges."""
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# 93 of the 117 pre-Index query candidates are relevant; the remaining 24 are
# frozen broad-query collisions below. Governed continuations retain multiline
# code, captions, source-bound images, seeds, observers, and close controls.
MATCHED_RETAINED = line_set(
    "670,672,850,2168,2170,2174,2212,2214,2216,2226,2230,2234,2236,2238,"
    "2250,2256,2262,2600,2680,2918,2922,3902,4072,4422,4430,4440,4452,"
    "5638,8322,8324,10984,10992,11037,11068,11070,11072,11074,11136,11178,"
    "11192,11507,11565,11569,11581,13471,13475,13479,13481,13483,13497,"
    "13501,13503,13513,13520,13542,13544,13547,13548,13549,13551,13559,"
    "13563,13579,13619,13620,13621,13622,13632,13642,13650,13654,14113,"
    "14239,14241,14243,14246,14254,14266,14787,14811,14815,14835,15221,"
    "15267,15301,15359,15959,16255,16446,16460,17431,18749,18755"
)

SEED_REALIZATION_CONTINUATIONS = (
    line_set("11077,11079-11087,11090,11092,11095-11100,11103,11106,11107")
    | line_set("11110,11112,11114,11116,11118,11120,11122,11124")
)

GOVERNED_CONTINUATIONS = (
    line_set(
        "2208,2210,2218,2220,2222,2224,2228,2232,2240,2242,2244,2246,2248,"
        "2252,2254,2258,2260,2682,2684,2920,3900,3904,3906,3908,3910,3912,"
        "3914,4428,4450,5634,5636,5640,5642,10986,11180,11182,11184,11186,"
        "11188,11190,11509,13469,13477,13499,13505,13507,13509,13511,13515-"
        "13518,13522-13526,13528,13530,13531,13534,13536,13538,13540,13543,"
        "13545,13546,13617,13624,13626,13628,13630,13634,13636,13638,13640,"
        "13644,13646,13648,13652,13656,13658,14245,14247-14249,14251,14253,"
        "14255-14259,14261,14263,14265,14267-14269,14271,14273,14789,14791,"
        "14793,14795,14797,14799,14801,14803,14805,14807,14809,14813,14817,"
        "14819,14821,14823,14825,14827,14829,14831,14833,14837,14839,14841,"
        "14843,15223,15225,15227,15229,15231,15269,15271,15273,15275,15277,"
        "15279,15281,18751,18753,18757,18759"
    )
    | SEED_REALIZATION_CONTINUATIONS
)

RETAINED = MATCHED_RETAINED | GOVERNED_CONTINUATIONS

# Stable public interface for the source-bound asset audit.
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
GOVERNED_IMAGE_LINES = line_set(
    "2220,2224,2228,2232,2240,2242,2244,2246,2248,2252,2254,2258,2260,"
    "2682,2920,3900,3908,3912,4428,4450,5636,11182,11184,11186,11188,11190,"
    "13626,13628,13630,13634,13636,13638,13640,13648,13652,13656,14273,"
    "14789,14793,14797,14801,14805,14809,14813,14817,14819,14821,14823,"
    "14829,14831,14833,14837,14839,14841,14843,15223,15225,15227,15229,"
    "15231,15269,15271,15275,15277,15279,15281,18753,18759"
)

# Native is the smallest same-runner construction: declared Self plus the
# eight offsets, typed tables, shared seeds/realizations, and snapshot commit.
# Life's code-224/B3-S23 mechanics are a named outer-totalistic preset over
# that same construction; its history, structures, and universality stay in
# RELATION_EVIDENCE.
LIFE_PRESET_EVIDENCE = line_set(
    "14239,14241,14243,14245-14249,14251,14253-14259,14261"
)
NATIVE_EVIDENCE = (
    line_set(
        "850,2212,2226,2230,2234,10984,10986,10992,11068,11136,11178,11180,"
        "13469,13475,13477,13479,13481,13513,13515-13518,13520,13522-13526,"
        "13528,13530,13531,13534,13536,13538,13540,13542-13549,16446"
    )
    | SEED_REALIZATION_CONTINUATIONS
    | LIFE_PRESET_EVIDENCE
)

T21_CONTROL = line_set(
    "2168,2170,2174,2600,2922,4072,11070,11072,11074,11569,13471,13551,"
    "13559,13563,14113,17431"
)
T23_CONTROL = line_set(
    "2236,2238,2240,2242,2244,2246,2248,2250,2252,2254,2256,2258,2260,"
    "2262,11192,13483,13497,13499,13501,13503,13505,13507,13509,13511,"
    "13632,13634,13636,13638,13640,14263,14265,14266,14267,14268,14269,"
    "14271,14273"
)
T24_CONTROL = line_set(
    "4422,4428,4430,4440,11037,13642,13644,13646,13648,13650,13652,13654,"
    "13656,13658,16255"
)
OTHER_CONTROL = line_set("2680,2682,2684,16460")
CONTROL_EVIDENCE = T21_CONTROL | T23_CONTROL | T24_CONTROL | OTHER_CONTROL
RELATION_EVIDENCE = RETAINED - NATIVE_EVIDENCE - CONTROL_EVIDENCE

# Frozen broad-query false positives, classified rather than silently dropped.
EXCLUDED_CLASS = {
    "generic_1d_code_or_update": line_set(
        "466,3034,7862,7896,8464,11256,14301,14313,14336,14417,14785,17669"
    ),
    "physical_or_aggregation_background": line_set(
        "3550,3878,13332,15338,15392,15708,15865"
    ),
    "other_construction": line_set("13666,13679,15293,17394,17573"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())

# The actual Index is routing vocabulary, never primary semantic evidence.
INDEX_CLASS = {
    "t22_geometry_or_code_routes": line_set(
        "20868,20957,20980,21004,21338,21432,21513,21525,21689"
    ),
    "life_routes": line_set(
        "20910,20916,21050,21193,21207,21213,21223,21229,21251,21335,21460,"
        "21461,21475,21683,21731,21819,21839,21915,21923,21992,22080,22114,"
        "22120,22136,22148,22352,22386,22392"
    ),
    "t23_routes": line_set("20972,21068,21090,21231,22262"),
    "t24_routes": line_set("21243,22416"),
    "numeric_false_collisions": line_set("21014,21024,21032"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())


EXPECTED_SOURCE_COUNT = 264
EXPECTED_SOURCE_DIGEST = "e54447c5ecdd87f896d65e5f05bbcd809de6908a357f35762a44aedb194c39e6"
EXPECTED_SET = {
    "union": (164, "20e6b1ba2eeca71d654f5cc4f8c15a7a410a45045140c037815f0ab0648b3072"),
    "pre_index_union": (117, "7e54e0a1c1bd79e10090aa640619f2dcc2911ed67e5f2ad090c5a9af6f661739"),
    "index": (47, "30e156e15372f04159ea4c4ec5c06e81cf3cd595b96da51e693082b3afa987e8"),
    "matched_retained": (93, "d8d3f2bb41cea07e16a1824c18f1fee5e1728d5dcf12136e0446e537a237a6d5"),
    "governed_continuations": (171, "a5bda2c9e2da262d1f675e89de37b6efbde081913bd3425fc95392228e0ffaa8"),
    "retained": (264, EXPECTED_SOURCE_DIGEST),
    "excluded": (24, "f324bb0607cb6830546d8cad257d011cd3bba4d0f037c176bed4472c119dc713"),
    "native": (90, "1395e5a2c4fb042ab82c57369b6747d12aa40002fd6752fe6f8479692cd968b0"),
    "relation": (102, "2bff19ad53338f3008a9f7f146ef8ac64c12d15c77e8ddba25025c6a6517aaa0"),
    "control": (72, "ca31ecfb0fac60ca36471c851e4dbedf7204f653f818c624131469429b264849"),
    "governed_images": (68, "d596854fe15fafe293038296ec2e5872612edda3033c08d6d2d314134ac3dd43"),
}
EXPECTED_EXCLUDED_CLASS = {
    "generic_1d_code_or_update": (12, "c70c62fe3bff5696801676142209e7f1be6ab3b3ccaf878fa8f6e5746fa445c8"),
    "physical_or_aggregation_background": (7, "d591a3b85f765abd34ad6eda75ee762459cb3d634af4547e3ef2c4d216be998c"),
    "other_construction": (5, "f734f7b1bfb2b9436e3451a4fc2f0ebb57424fe3d4c2ebc6a3cff68bdf2437d2"),
}
EXPECTED_INDEX_CLASS = {
    "t22_geometry_or_code_routes": (9, "1f001746e854c4b960108f8f390adfde73e7b6a44e5e956e33803b2bbc255104"),
    "life_routes": (28, "4a4f9aa94c1121378644effb63d582b9f142c7a71b2167a451787950713f72b7"),
    "t23_routes": (5, "c7459881d3a8ae47c919831c02f9f70640a07bcf0b7bdf36e1ffba29fdb83e07"),
    "t24_routes": (2, "dd78d1964dd243324fcedd5127e8a401b08add223aafabb2ff61c9d471a7ec24"),
    "numeric_false_collisions": (3, "9ab74ca0280d52af89368b30d9d812dd8146b7f91f369c798585a1cc8b908119"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY = (162, "0f93d0f9a3a53e08cc35db13176eadbfe21b76a62df22a439a04fd5e27e6d933")
EXPECTED_SPLIT_QUERY_EXACT = (151, "157e46e9e28cca11fdd7c6952a43d179b1957937b4f6423244dfdaab91e89605")
EXPECTED_SPLIT_QUERY_NONEXACT = (11, "6c816598a74c83605d417915d240d9af73bbe28722d4709700cd954bdc93697e")
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = "8c18b6feb0084967234cf8f37714a83908732debf202e6d0bc04227b6b1327e3"
EXPECTED_SPLIT_RETAINED_EXACT = (186, "3f9f01d2d069d2e5411f6dc0ea6c41be4bd1f4f32ae9328979a8312fc0fb6401")
EXPECTED_SPLIT_RETAINED_NONEXACT = (78, "35976a4a7f6d596fbc2ec6d109a520f62f6674ce1042c013e76ab07233029632")
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = "22b622d6b596da0671e5573db8ded54067041367ce0f9ef516f1bc7ae0554979"
EXPECTED_MONOLITH_ONLY = (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
EXPECTED_ATLAS_HITS = (1, "dac53c17c250fd4d4d81eaf6d88435676dac1f3f3896441e277af839bf50ed8a")


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


def encoded_code(predicate: object) -> int:
    pred = predicate  # keep the quantified construction readable below
    return sum(
        1 << (2 * count + center)
        for count in range(9)
        for center in range(2)
        if pred(center, count)  # type: ignore[operator]
    )


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 34-T22-source-oracle.py [BOOK]")
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
        expected = EXPECTED_SET.get(name)
        good = actual == expected
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

    # The source-bound image interface is derived independently from the
    # retained source lines so the asset oracle cannot inherit a hand typo.
    derived_images = {n for n in RETAINED if IMAGE_RE.fullmatch(at(n))}
    images_ok = derived_images == set(GOVERNED_IMAGE_LINES)
    ok &= images_ok
    print("governed_image_interface", "OK" if images_ok else "MISMATCH",
          len(derived_images), digest(derived_images))

    # Book convention: j = 2*surrounding_count + old_center.  Reconstruct all
    # 18 outputs rather than testing only the illustrated seeds.
    code_175850 = encoded_code(lambda center, count: count in {3, 5} or center == 1)
    code_174826 = encoded_code(lambda center, count: count == 3 or center == 1)
    code_746 = encoded_code(
        lambda center, count: count == 3 or (count in {0, 1, 2, 4} and center == 1)
    )
    named_codes_ok = (
        (code_175850, code_746, code_174826) == (175850, 746, 174826)
        and "exactly three of its eight neighbors—including diagonals" in at(2212)
        and "either 3 or 5 of its 8 neighbors" in at(2226)
        and "code number 175850" in at(2226)
        and "code number 746" in at(2230)
        and "code number 174826" in at(2234)
        and all(((746 >> (2 * n + s)) & 1) == (1 if n == 3 else (s if n < 5 else 0))
                for n in range(9) for s in range(2))
    )
    ok &= named_codes_ok
    print("named_codes_all_18_cases", "OK" if named_codes_ok else "MISMATCH",
          code_175850, code_746, code_174826)

    expected_raw_offsets = tuple(
        (-1 + i, -1 + j) for i in range(3) for j in range(3)
    )
    derived_raw_offsets = tuple(sorted(itertools.product((-1, 0, 1), repeat=2)))
    rule_schemas_ok = (
        expected_raw_offsets == derived_raw_offsets
        and len(derived_raw_offsets) == 9
        and derived_raw_offsets.count((0, 0)) == 1
        and "9-neighbor rules introduced on page 177" in at(13475)
        and "ListConvolve[{{2, 2, 2}, {2, 1, 2}, {2, 2, 2}}" in at(13479)
        and "IntegerDigits[code, 2, 18]" in at(13481)
        and "offset lists are always taken to be in the order given by *Sort*" in at(13513)
        and "same order as the offset list" in at(13513)
        and "IntegerDigits[i, k, Length[os]]" in at(13520)
        and "FromDigits[Reverse[u], k]" in at(13520)
        and "ListCorrelate" in at(13531)
        and "$2^{512}" in at(13544)
        and "$2^{18}" in at(13547)
        and "$2^{10} = 1024$" in at(13548)
        and "$2^9 = 512$" in at(13549)
        and 2 * ((3**2 - 1) * (2 - 1) + 1) == 18
        and 2**9 == 512
        and 9 + 1 == 10
    )
    ok &= rule_schemas_ok
    print("declared_self_plus_eight_and_512_18_10_9_schemas",
          "OK" if rule_schemas_ok else "MISMATCH")

    update_seed_ok = (
        "updated in parallel at every step" in at(850)
        and "old values of neighbors" in at(10984)
        and "two copies of the array" in at(10984)
        and "practical computer one can use only a finite array" in at(10986)
        and "effectively use a cyclic array" in at(10986)
        and "explicit list of values in two dimensions" in at(11090)
        and "positive direction in each coordinate relative to the origin" in at(11092)
        and "evolution list of length t+1" in at(11103)
        and "always the same size" in at(11124)
        and "Automatic can be used to trim off background" in at(11124)
        and "previous step" in at(16446)
        and "updated sequentially rather than in parallel" in at(16446)
    )
    ok &= update_seed_ok
    print("shared_snapshot_update_seed_and_realization", "OK" if update_seed_ok else "MISMATCH")

    relations_controls_ok = (
        "Game of Life" in at(670)
        and "Life 2D cellular automaton" in at(14243)
        and "LifeStep[a_List]" in at(14246)
        and "unbounded growth in Life" in at(14811)
        and "Game of Life" in at(18749)
        and "three-dimensional cellular automata" in at(2236)
        and "all 26 neighbors" in at(2262)
        and "9-neighbor rules generalize" in at(13497)
        and "Other geometries" in at(13642)
        and "triangular lattice" in at(13650)
        and "nested Penrose tiling" in at(13654)
        and "constraint involving" in at(2684)
        and "only the 33 templates" in at(2684)
        and "stopped growing" in at(2234)
    )
    ok &= relations_controls_ok
    print("life_observers_and_t21_t23_t24_controls",
          "OK" if relations_controls_ok else "MISMATCH")

    structural = (
        len(RETAINED) == EXPECTED_SOURCE_COUNT
        and digest(RETAINED) == EXPECTED_SOURCE_DIGEST
        and MATCHED_RETAINED == matched_retained
        and GOVERNED_CONTINUATIONS == governed
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not CONTROL_EVIDENCE & RELATION_EVIDENCE
        and NATIVE_EVIDENCE | CONTROL_EVIDENCE | RELATION_EVIDENCE == RETAINED
        and not RETAINED & index
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    # Close every split markdown copy with immutable file hashes, query-record
    # enumeration, and a deterministic reverse join to the monolith.
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
    print("split_manifest", "OK" if split_manifest_ok else "MISMATCH",
          len(split_paths), digest_records(relative_paths), digest_records(manifest))

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
    for record in sorted(split_nonexact):
        witness, score = best_witness(split_record_text[record], [
            (str(line_no), normalized_line(at(line_no))) for line_no in sorted(union)
        ])
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
    print("split_query_reverse_join", "OK" if split_query_ok else "MISMATCH",
          len(split_records), digest_records(split_records), len(split_exact),
          digest_records(split_exact), len(split_nonexact), digest_records(split_nonexact),
          digest_records(query_mapping))

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
    print("split_retained_reverse_join", "OK" if split_retained_ok else "MISMATCH",
          len(exact_retained), digest(exact_retained), len(nonexact_retained),
          digest(nonexact_retained), len(retained_mapping), digest_records(retained_mapping),
          len(monolith_only), digest(monolith_only))

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n for n, line in enumerate(atlas_lines, 1) if any(rx.search(line) for rx in compiled)
    }
    atlas_ok = (
        len(atlas_lines) == 542
        and (len(atlas_hits), digest(atlas_hits)) == EXPECTED_ATLAS_HITS
    )
    ok &= atlas_ok
    print("atlas", "OK" if atlas_ok else "MISMATCH", len(atlas_hits), digest(atlas_hits))

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[22] == "Moore-Neighborhood Cellular Automata,"
        and len(set(catalog_lines[1:])) == 45
        and "## 22. Moore-Neighborhood Cellular Automata" in taxonomy_text
        and "all eight surrounding cells, including diagonals" in taxonomy_text
        and "center cell may also be included in the rule logic" in taxonomy_text
        and "`dimension`: `2`." in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog", "OK" if catalog_ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
