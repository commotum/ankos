#!/usr/bin/env python3
"""Frozen primary-source audit for T28 contextual two-dimensional substitution.

This is an evidence oracle, not a substitution-system implementation.  It
freezes a deliberately redundant vocabulary over the canonical monolithic
Book, dispositions every candidate returned by that vocabulary, follows
governed continuations and source-linked images, checks actual-Index routes,
and reverse-joins the split corpus.

The source supports a grid-aligned, snapshot-parallel contextual patch
replacement: a 2 x 2 neighborhood selects a replacement patch and the patches
are assembled with ``Flatten2D``.  The displayed native preset exists only as
a raster; the Notes give an example row and the step expression, but no
machine-readable complete rule table or seed.  This oracle therefore freezes
the construction while refusing to invent an executable preset from pixels.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T28 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"
NATIVE_RASTER = (
    SOURCE_ROOT
    / "CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_207_Figure_1.jpeg"
)

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"
EXPECTED_NATIVE_RASTER_SHA256 = "e7f0112ebc4a6b4276bffeaccc043855335527d38e638c2ed37c428451d57b1c"


# Each lane has a distinct purpose.  Direct names and mechanics find the
# construction; aliases and absent modern spellings guard vocabulary drift;
# executable symbols and Notes phrases bind the only textual rule schema;
# sibling lanes preserve the T14/T26/T27/T29/T31 boundaries; page and Index
# lanes follow the Book's own routes.  Broad words occur only with local
# construction context, so this is a closed audit of this frozen vocabulary,
# not a claim to have searched every imaginable paraphrase.
QUERIES = {
    "Q00": r"\bneighbor(?:[\s-]*)dependent(?:[\s-]+)substitution systems?\b",
    "Q01": (
        r"\btwo[- ]dimensional neighbor[- ]dependent substitution systems?\b|"
        r"\bneighbor[- ]dependent two[- ]dimensional substitution systems?\b|"
        r"\b2D neighbor[- ]dependent substitution systems?\b|"
        r"\bneighbor[- ]dependent 2D\b"
    ),
    "Q02": (
        r"\binteraction between different elements\b|"
        r"\breplacement for a particular element[^.]{0,220}\bneighboring elements\b|"
        r"\bsets up elements on a grid[^.]{0,220}\breplacements?[^.]{0,120}\bdepend on its neighbors\b|"
        r"\breplacements? for a given element[^.]{0,160}\bdepend on its neighbors\b"
    ),
    "Q03": (
        r"Flatten2D\[Partition\[list, \{2, 2\}, 1, -1\] /\. rule\]|"
        r"\\\{\\\{-, 1\\\}, \\\{0, 1\\\}\\\} \\rightarrow \\\{\\\{1, 0\\\}, \\\{1, 1\\\}\\\}|"
        r"\barbitrarily large set of different possible neighborhood configurations\b"
    ),
    "Q04": (
        r"\bwrap around in both (?:of )?its dimensions\b|"
        r"\bneighbor[- ]dependent substitution systems?[^.]{0,180}\b(?:wrap|cyclic boundary)\b|"
        r"\b(?:wrap|cyclic boundary)[^.]{0,180}\bneighbor[- ]dependent substitution systems?\b"
    ),
    "Q05": r"\bPage 192\b|\bpage 935\b|\b187[–-]192\b",
    "Q06": (
        r"\bimmediately to its right\b|"
        r"\brightmost element is always dropped\b|"
        r"\bSS2EvolveList\b|"
        r"Partition\[#, 2, 1\] /\. rule"
    ),
    "Q07": (
        r"\btwo-dimensional substitution systems?\b|"
        r"\b2D substitution systems?\b|"
        r"\bsubstitution systems? in two dimensions\b"
    ),
    "Q08": (
        r"\bgeometrical replacement rules?\b|"
        r"\bdifficult to define an obvious notion of neighbors\b|"
        r"\bsquares produced to overlap\b"
    ),
    "Q09": (
        r"\bnetwork systems?[^.]{0,200}\b(?:local structure|underlying grid)\b|"
        r"\b(?:local structure|underlying grid)[^.]{0,200}\bnetwork systems?\b"
    ),
    "Q10": (
        r"^#### \*\*Systems Based on Constraints\*\*$|"
        r"\bform is defined by the constraint that every cell should have at least one neighbor\b|"
        r"\btwo-dimensional systems based on constraints\b"
    ),
    "Q11": (
        r"\bgeneralizes? to neighbor[- ]dependent substitution systems?[^.]{0,160}\bemulate cellular automata\b|"
        r"\bneighbor[- ]dependent substitution systems? that emulate cellular automata\b|"
        r"\bhighly uniform rules always yielding just one cell\b"
    ),
    "Q12": (
        r"\bcontext(?:ual|[- ](?:dependent|sensitive)) two[- ]dimensional substitution systems?\b|"
        r"\btwo[- ]dimensional context(?:ual|[- ](?:dependent|sensitive)) substitution systems?\b|"
        r"\b(?:tile|block|array) substitution systems?\b|"
        r"\bpicture grammars?\b"
    ),
    "Q13": (
        r"\bcontext[^.]{0,120}\bsubstitution systems?\b|"
        r"\bsubstitution systems?[^.]{0,120}\bcontext\b"
    ),
    "Q14": (
        r"\bno immediate way to generalize sequential substitution systems to two or more dimensions\b|"
        r"\bon a two-dimensional grid[^.]{0,220}\bscan all the elements\b"
    ),
    "Q15": (
        r"\bSubstitution systems, 82[–-]87 2D[.,] 187[–-]192\b|"
        r"\bTwo-dimensional cellular automata[^.]{0,180}\bsubstitution systems, 187[–-]192\b|"
        r"\bneighbor-dependent 2D, 192, 935\b"
    ),
    "Q16": r"_page_20[67]_(?:Picture_1|Figure_1)\.jpeg",
    "Q17": r"\bPage 192 · Neighbor-dependent substitution systems\b",
    "Q18": r"\b1L systems, 85[–-]88\b|\bD1L systems, 85[–-]87\b",
    "Q19": (
        r"\b(?:padding|padded with (?:a )?blank|special boundary symbol)\b[^.]{0,180}\bsubstitution systems?\b|"
        r"\bsubstitution systems?\b[^.]{0,180}\b(?:padding|padded with (?:a )?blank|special boundary symbol)\b"
    ),
    "Q20": (
        r"\bfixed underlying geometrical structure which remains unchanged\b|"
        r"\bnetwork system is fundamentally just a collection of nodes\b|"
        r"\brules that specify how these connections should change from one step to the next\b"
    ),
    "Q21": (
        r"\bexplicit rules that specify how the system evolves from step to step\b|"
        r"\binstead of having explicit rules for evolution[^.]{0,180}\bconstraints to satisfy\b|"
        r"\bknowing only this constraint gives no explicit procedure\b"
    ),
    "Q22": (
        r"\bwhat about two dimensions\? The proof for one dimension breaks down\b|"
        r"\bas a first example of a two-dimensional system, consider an array\b|"
        r"\ba system consisting of a grid of black and white cells defined by the constraint\b"
    ),
    "Q23": (
        r"\bA two-dimensional neighbor-dependent substitution system\b|"
        r"\bgrid of cells is assumed to wrap around in both its dimensions\b|"
        r"\bPatterns generated by 8 steps of evolution in various two-dimensional neighbor-dependent substitution systems\b"
    ),
    "Q24": (
        r"\bPage 187 · Two-dimensional substitution systems\b|"
        r"\bPage 192 · Space-filling curves\b|"
        r"\bSubstitution Systems and Fractals\b"
    ),
}


EXPECTED_QUERY = {
    "Q00": (7, 6, 1, "f37901fb3b77c8a4c4f80bf0456322ee203ce5dc42ca86523323a23d0bc13f8b"),
    "Q01": (1, 0, 1, "51493d0e1042577adde32e82b51d1ce32eee5d1903b81fe72f4cb791c11ac6b2"),
    "Q02": (2, 2, 0, "99cc0441a49e6cb1bf773c82cc27a06e0923e447dadef1a8453805ff6f8ac19c"),
    "Q03": (3, 3, 0, "97ad5a256e556b9ac4e431f1dd8a9d2b233c76352ba9fbd01bedd4baebc44701"),
    "Q04": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q05": (4, 2, 2, "67ac7d563f560e9f2d22f30b5bb27ab7d20819025435385e22d2e373ae8ddf2c"),
    "Q06": (5, 5, 0, "24169a59e11dd2bdec245a477d181c83e8624b486250f595c8364fe17acc0954"),
    "Q07": (23, 13, 10, "b946fac1940f142a257a962e200195c404c5992d222216104af1f9aebfec9035"),
    "Q08": (3, 3, 0, "0fd8f2dce4a000702d7fd1b8969d8ee6dd412a5c5ef4cf43b8d2430b86d1910d"),
    "Q09": (2, 2, 0, "f81e470d92b3fbd2fbdcd0fdf76a13de4fb423dde7c3b25fb437665c921e79f1"),
    "Q10": (4, 4, 0, "e09ce51fdd294991012e28f7a4de6cea1b6c5d66d374fbca07bdfbe82ed0ef45"),
    "Q11": (2, 2, 0, "8f29f394e6d0403d3c3e0ba58cdfc2f49a14d831cc43244c1f1e7e1a2f558f6a"),
    "Q12": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q13": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q14": (2, 2, 0, "2b38c0a5431171f2d39496c0bec159ed30c56fed81014b631db34fc5614547c1"),
    "Q15": (2, 0, 2, "d036a1ece9a499652236e864811f066808f46b6755a3c0aca2ed09c7369468a3"),
    "Q16": (2, 2, 0, "1c3f52bf3553a603d9408f3ba60f4f01df9d044b5cd5738cfbfde32af92bdd0f"),
    "Q17": (1, 1, 0, "337f683f86185141f92ef0a68c76b2cc254dcdfcca9f6ab1e513c14e9248e0e7"),
    "Q18": (2, 0, 2, "154cff02563829d70fa5bbf0637554554a894d903e16e5af8ce0b32c97ff570c"),
    "Q19": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q20": (2, 2, 0, "df0811e5f702c0ba50307e135c77ae6dc031128fd9f47223e57be5dd4f69c212"),
    "Q21": (3, 3, 0, "aca5f673c27b0ffa5674a95ea2bc09f392492aec71a182270788a10582cfee57"),
    "Q22": (3, 3, 0, "de7a93a3ec621266b299d66d258294215044970ec0d17d9b9a8023ecfa88cd78"),
    "Q23": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q24": (3, 3, 0, "dd130125682c7f05623ebc777bf2e79002de980b669334726af560a93bceb7b7"),
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


# Every pre-Index query hit is classified exactly once.  Native is restricted
# to the T28 grid/context construction and Notes.  Relations are the exact T14
# analog and its singleton-output CA degeneration.  Controls establish the
# independent T26 base, free-geometric T27 nonfit, ordered T16 boundary, graph
# T29 boundary, and non-evolutionary T31 boundary.
NATIVE_MATCHED = line_set("2350,2356,2362,13806,13808,13810")
RELATION_MATCHED = line_set("1018,1022,1050,8024,8028,12109,12113")
CONTROL_MATCHED = line_set(
    "12251,"
    "2308,2312,2316,2318,2334,2352,2354,"
    "2364,2366,2370,2372,2376,2464,2496,"
    "2568,2570,2572,2574,2586,2594,2596,2600,5788,"
    "13681,13683,13812,14027"
)

NATIVE_CONTINUATIONS = frozenset()
RELATION_CONTINUATIONS = line_set("1020,1024,8022,8026,12111,12115")
CONTROL_CONTINUATIONS = line_set(
    "2310,2314,2320,2322,2324,"
    "2326,2328,2330,2332,2340,2342,2344,2348,"
    "2368,2374,2646,13685-13690,14029,14055"
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
    "ordinary_T26_downstream_only": line_set(
        "6676,6842,6978,7312,12249,13692,14099,17297,19197"
    ),
    "unrelated_CA_cryptanalysis": line_set("7204"),
    "generic_encoding_function": line_set("18788"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("2362")
RELATION_IMAGE_LINES = line_set("1020,8026")
CONTROL_IMAGE_LINES = line_set("2314,2322,2328,2330,2340,2344,2354")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_CLASS = {
    "adjacent_T25_or_post_relation_families": line_set("2302,8018,8036,8038"),
    "notes_page_Mandelbrot_noise": line_set("13800,13802,13804"),
}
EXCLUDED_IMAGE_LINES = frozenset().union(*EXCLUDED_IMAGE_CLASS.values())
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES = frozenset()


INDEX_CLASS = {
    "native_T28_routes": line_set("22144,22380"),
    "T14_alias_controls": line_set("20828,21068,21652"),
    "T26_sibling_routes": line_set(
        "20850,20944,21080,21088,21195,21223,21513,21681,22114,22352"
    ),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_ENTRY_GUARDS = {
    "native_T28_routes": {
        22144: ("neighbor-dependent 2d, 192, 935",),
        22380: ("two-dimensional cellular automata", "substitution systems, 187–192"),
    },
    "T14_alias_controls": {
        20828: ("1l systems, 85–88, 893",),
        21068: ("d1l systems, 85–87",),
        21652: ("neighbor-dependent substitution systems, 85–87",),
    },
    "T26_sibling_routes": {
        20850: ("affine transformations and 2d substitution systems, 933",),
        20944: ("from 2d substitution system, 190",),
        21080: ("determinism in 2d substitution systems, 188",),
        21088: ("and 2d substitution systems, 931",),
        21195: ("and 2d substitution systems, 187",),
        21223: ("and 2d substitution systems, 932",),
        21513: ("matrices and 2d substitution systems, 933",),
        21681: ("in 2d substitution systems, 187",),
        22114: ("and 2d substitution system, 187",),
        22352: ("in 2d substitution systems, 188",),
    },
}


# The raster is hash-bound and these are deliberately limited manual
# transcriptions.  No glyph content, complete table, seed, or trace is claimed.
NATIVE_RASTER_TRANSCRIPTION = (
    "caption:two-dimensional neighbor-dependent substitution system",
    "boundary:grid wraps in both dimensions",
    "top-trajectory:steps 1 through 7",
    "displayed-rule-glyph-panels:5",
    "example-galleries:a through h (8)",
    "gallery-caption:generated by 8 steps",
)

RAW_EXAMPLE_ROW = (
    r"\{\{-, 1\}, \{0, 1\}\} \rightarrow \{\{1, 0\}, \{1, 1\}\}"
)
REPAIRED_EXAMPLE_ROW = (
    r"\{\{_, 1\}, \{0, 1\}\} \rightarrow \{\{1, 0\}, \{1, 1\}\}"
)
OFFICIAL_NOTE_URL = (
    "https://www.wolframscience.com/nks/"
    "notes-5-4--neighbor-dependent-2d-substitution-systems/"
)


# Frozen after every discovery hit and governed continuation was inspected.
EXPECTED_SET = {
    "union": (67, "11bb91d9a96cd9b82089c1f45a8bb8473c91eb6ebec3ba04f78404fe0a5f9e2c"),
    "pre_index_union": (52, "9d6995eaf237deca9959ba2d18547896fcfcf9e14cea07f1fd8e307714616a63"),
    "index": (15, "525d824e26d2830c26e171aeed650e5830a812ae3a251693d0cbd01aa5da85e7"),
    "matched_retained": (41, "38211f87eb2055900e25d896dbd0ab014f00ecfbc873e30a7b141a71cb8c28c7"),
    "governed_continuations": (30, "df8df7d8c1934fb069d5048e6ee8f8fefef3c0b5a246f2c5616e55fc39759856"),
    "retained": (71, "985faff919920a422eecde0ef283c86d49c4cea73be8bf33e86d29e96be99c18"),
    "excluded": (11, "0d5619d01232a9f8e9fabb87027b847549465b9a4cb916944d4d2f497426c0ed"),
    "native": (6, "8fbba0be6bdf720fd223be421b5b0fdf4e547c8832230b08eb42aca320e9045e"),
    "relation": (13, "83fa916fb2b060dbe8896af54a58950776e900217bdf0da673b88c174c353150"),
    "control": (52, "be292a32930d092e5bb886849f2cc0f1cc119e2fdf474bdecea8d8ad62f81182"),
    "governed_images": (10, "06e50ad4cf8480aed23443fd40147ac0fb35e0776e1883d025467943c4889411"),
    "excluded_images": (7, "8b6cbf265e37d7759d88fad5b1fa99c9814dc40293ea8a350f3a40b21bbd26f7"),
}
EXPECTED_EXCLUDED_CLASS = {
    "ordinary_T26_downstream_only": (9, "3e1e2dec1734f75bf57c79911bc12d66e4e6d91ebf26cab9f50ac0a3f0b0de10"),
    "unrelated_CA_cryptanalysis": (1, "ed12f17149c7e7b586c76a949fed6e85c2f1bf57e820427eac00c1eeb3926f3d"),
    "generic_encoding_function": (1, "77a8197f477be9bace08ae8afa8959a2ca59bfbe351d767d7ba9ea60008383d4"),
}
EXPECTED_INDEX_CLASS = {
    "native_T28_routes": (2, "d036a1ece9a499652236e864811f066808f46b6755a3c0aca2ed09c7369468a3"),
    "T14_alias_controls": (3, "6ece6fe889c2a32a9152d22aa19342a55b799c56a2e5ab8fecb48f56924f1c65"),
    "T26_sibling_routes": (10, "89f71cc6c580d01bd25fe1c5e94b3dbfafa0aa5353a922f43194024d26f27222"),
}
EXPECTED_IMAGE_PARTITION = {
    "native": (1, "9bf42f4b66fe462d800a8b659ec866dca7f23597393f9cb25456d41f5458b590"),
    "relation": (2, "ac31f08d2eaed3c8cfd457f9d4922b7fab79508739676c57158d156356528eb2"),
    "control": (7, "6159ae09901c63d9c720102232de4bbc096433209203024d3750c10068f2f0e9"),
}
EXPECTED_EXCLUDED_IMAGE_CLASS = {
    "adjacent_T25_or_post_relation_families": (4, "7aa56d7cb437421ee86b85981746d758cd8adc86c8057f4cb918128bc994b84c"),
    "notes_page_Mandelbrot_noise": (3, "fe656793d838867fcb52027854d8ffb11168eef2d923f4194b4e1cb0f5661446"),
}
EXPECTED_INDEX_GUARDS = (15, "dfcc4b6eff8a0df684f9938f42aee8695628bc2dfe604011228b6f0f10c9259c")
EXPECTED_RASTER_TRANSCRIPTION = (6, "6a4016f19a5bb71a3dcd20f3973e4b109a54dfe5dfe73e5d89fe1b167d8f0a9b")

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY = (66, "72049c6d60dda71ba13b6bce1b76d2ea5afeb9bf6cf3f02dc9d27076ba716d14")
EXPECTED_SPLIT_QUERY_EXACT = (53, "82102d417dcf8f0d73a18bdb4e797ad1d99218c485dc190319ad550f19da20ff")
EXPECTED_SPLIT_QUERY_NONEXACT = (13, "d6bc73fd224b5466f28277cab27128a40c35037603b7c10ed4e1fe2ccfdd1ac9")
EXPECTED_SPLIT_QUERY_MAPPING = (13, "53abbb27d237e52e94deb76a0fe5c949b4d7b55d3ff55593f3c031a7636f5d04")
EXPECTED_SPLIT_RETAINED_EXACT = (48, "4ef4dbfec95bd1bb4d0b4f8606c29a61115e3dc8987d964f46cc131df16bd453")
EXPECTED_SPLIT_RETAINED_NONEXACT = (23, "e45d05c69921a8c9d47372b0d380ec9d216855744400a19a887e10d1d6f6a20e")
EXPECTED_SPLIT_RETAINED_MAPPING = (23, "bf1528da95d3a92fa509f09e1062aed566f89ccf15ded67713baed7a5b279748")
EXPECTED_MONOLITH_ONLY = (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
EXPECTED_ATLAS_HITS = (2, "d6ef54ffa4ed4062c4cce2ec86050f137de9e2b75fdeea0b6e2cf6a9de0ae307")


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def digest_records(records: set[str] | list[str] | tuple[str, ...]) -> str:
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


def periodic_windows_2x2(
    grid: tuple[tuple[int, ...], ...],
) -> tuple[tuple[tuple[tuple[int, int], tuple[int, int]], ...], ...]:
    """Derived reading of ``Partition[..., {2,2}, 1, -1]``.

    Each locus is the southeast/self cell of ``((NW, N), (W, self))``;
    indices wrap in both dimensions, as the hash-bound page-207 caption says.
    """

    assert grid and all(grid) and len({len(row) for row in grid}) == 1
    height, width = len(grid), len(grid[0])
    return tuple(
        tuple(
            (
                (grid[(y - 1) % height][(x - 1) % width], grid[(y - 1) % height][x]),
                (grid[y][(x - 1) % width], grid[y][x]),
            )
            for x in range(width)
        )
        for y in range(height)
    )


def flatten2d_uniform(
    patches: tuple[tuple[tuple[tuple[int, ...], ...], ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Derived rank-two assembly for a rectangular grid of uniform patches."""

    assert patches and all(patches) and len({len(row) for row in patches}) == 1
    blocks = [patch for row in patches for patch in row]
    assert blocks and all(block and all(block_row for block_row in block) for block in blocks)
    heights = {len(block) for block in blocks}
    widths = {len(block_row) for block in blocks for block_row in block}
    assert len(heights) == len(widths) == 1
    block_height, block_width = next(iter(heights)), next(iter(widths))
    assert all(
        len(block) == block_height
        and all(len(block_row) == block_width for block_row in block)
        for block in blocks
    )
    return tuple(
        tuple(
            patches[source_y][source_x][local_y][local_x]
            for source_x in range(len(patches[0]))
            for local_x in range(block_width)
        )
        for source_y in range(len(patches))
        for local_y in range(block_height)
    )


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 39-T28-source-oracle.py [BOOK]")
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
        and sha256(NATIVE_RASTER) == EXPECTED_NATIVE_RASTER_SHA256
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
            sum(line_no < INDEX_FIRST_LINE for line_no in found),
            sum(line_no >= INDEX_FIRST_LINE for line_no in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY[name]
        ok &= good
        print(
            name,
            "OK" if good else "MISMATCH",
            *actual,
        )

    union = set().union(*hits.values())
    pre_index_union = {line_no for line_no in union if line_no < INDEX_FIRST_LINE}
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
        "governed_images": set(GOVERNED_IMAGE_LINES),
        "excluded_images": set(EXCLUDED_IMAGE_LINES),
    }
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    excluded_ok = (
        set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    classification_delta = matched_retained ^ set(MATCHED_RETAINED)
    excluded_ok &= not classification_delta
    ok &= excluded_ok
    print(
        "unresolved_pre_index", "OK" if excluded_ok else "MISMATCH",
        len(classification_delta), *sorted(classification_delta),
    )

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
    guards_ok = (
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
        and (len(guard_records), digest_records(guard_records)) == EXPECTED_INDEX_GUARDS
    )
    index_ok &= guards_ok
    ok &= index_ok
    print(
        "index_entry_occurrence_guards", "OK" if guards_ok else "MISMATCH",
        len(guard_records), digest_records(guard_records),
    )
    print(
        "unresolved_index", "OK" if index_ok else "MISMATCH",
        len(index ^ set(INDEX_ROUTED)),
    )

    derived_images = {line_no for line_no in RETAINED if IMAGE_RE.fullmatch(at(line_no))}
    image_sets = {
        "native": NATIVE_IMAGE_LINES,
        "relation": RELATION_IMAGE_LINES,
        "control": CONTROL_IMAGE_LINES,
    }
    images_ok = (
        derived_images == set(GOVERNED_IMAGE_LINES)
        and sum(map(len, image_sets.values())) == len(GOVERNED_IMAGE_LINES)
        and all(IMAGE_RE.fullmatch(at(line_no)) for line_no in GOVERNED_IMAGE_LINES)
        and not set(EXCLUDED_IMAGE_LINES) & set(RETAINED)
        and all(IMAGE_RE.fullmatch(at(line_no)) for line_no in EXCLUDED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and len(CANDIDATE_IMAGE_LINES) == 17
        and not UNRESOLVED_IMAGE_LINES
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION.get(name)
        images_ok &= good
        print(f"images_{name}", "OK" if good else "MISMATCH", *actual)
    for name, values in EXCLUDED_IMAGE_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_IMAGE_CLASS.get(name)
        images_ok &= good
        print(f"excluded_images_{name}", "OK" if good else "MISMATCH", *actual)
    ok &= images_ok
    print(
        "governed_image_interface", "OK" if images_ok else "MISMATCH",
        len(derived_images), digest(derived_images),
        "excluded", len(EXCLUDED_IMAGE_LINES), digest(EXCLUDED_IMAGE_LINES),
    )

    raster_transcription_actual = (
        len(NATIVE_RASTER_TRANSCRIPTION),
        digest_records(NATIVE_RASTER_TRANSCRIPTION),
    )
    raster_ok = (
        raster_transcription_actual == EXPECTED_RASTER_TRANSCRIPTION
        and at(2362) == "![](_page_207_Figure_1.jpeg)"
        and 2362 in NATIVE_IMAGE_LINES
        and not hits["Q04"]
        and not hits["Q23"]
    )
    ok &= raster_ok
    print(
        "native_raster_hash_bound_limited_transcription_no_pixel_replay",
        "OK" if raster_ok else "MISMATCH", *raster_transcription_actual,
    )

    repaired_line = at(13806).replace(RAW_EXAMPLE_ROW, REPAIRED_EXAMPLE_ROW, 1)
    repair_ok = (
        at(13806).count(RAW_EXAMPLE_ROW) == 1
        and RAW_EXAMPLE_ROW.count("-") == 1
        and "_" not in RAW_EXAMPLE_ROW
        and RAW_EXAMPLE_ROW.replace("-", "_") == REPAIRED_EXAMPLE_ROW
        and repaired_line.count(REPAIRED_EXAMPLE_ROW) == 1
        and RAW_EXAMPLE_ROW not in repaired_line
        and OFFICIAL_NOTE_URL.endswith(
            "notes-5-4--neighbor-dependent-2d-substitution-systems/"
        )
        and "Mathematica pattern of the form" in at(14055)
        and at(14055).count("-") >= 4
        and 14055 in CONTROL_EVIDENCE
    )
    ok &= repair_ok
    print(
        "source_official_exact_blank_OCR_repair_one_example_row_only",
        "OK" if repair_ok else "MISMATCH",
    )

    main_construction_ok = (
        "interaction between different elements" in at(2350)
        and "replacement for a particular element" in at(2350)
        and "other neighboring elements" in at(2350)
        and "difficult to define an obvious notion of neighbors" in at(2352)
        and "sets up elements on a grid" in at(2356)
        and "replacements for a given element to depend on its neighbors" in at(2356)
        and "not just purely nested" in at(2356)
        and 2352 in CONTROL_EVIDENCE
        and 2356 in NATIVE_EVIDENCE
    )
    ok &= main_construction_ok
    print("source_grid_context_construction", "OK" if main_construction_ok else "MISMATCH")

    notes_block = "\n".join(at(line_no) for line_no in range(13806, 13811))
    notes_ok = (
        repair_ok
        and "Page 192 · Neighbor-dependent substitution systems" in at(13806)
        and "such as" in at(13806)
        and "Flatten2D[Partition[list, {2, 2}, 1, -1] /. rule]" == at(13808)
        and "some replacements lead to subdivision" in at(13810)
        and "arbitrarily large set of different possible neighborhood configurations" in at(13810)
        and notes_block.count("\\rightarrow") == 1
        and "initial condition" not in notes_block.lower()
    )
    ok &= notes_ok
    print(
        "source_notes_one_row_periodic_2x2_context_flatten2d",
        "OK" if notes_ok else "MISMATCH",
    )

    adaptive_extension_ok = (
        "some replacements lead to subdivision of elements but others do not" in at(13810)
        and "unlike for the 1D case" in at(13810)
        and "arbitrarily large set of different possible neighborhood configurations" in at(13810)
        and 13810 in NATIVE_EVIDENCE
    )
    ok &= adaptive_extension_ok
    print(
        "source_adaptive_mixed_subdivision_is_dynamic_context_caveat",
        "OK" if adaptive_extension_ok else "MISMATCH",
    )

    windows = periodic_windows_2x2(((0, 1, 2), (3, 4, 5)))
    example_window = ((9, 1), (0, 1))
    periodic_model_ok = (
        windows[0][0] == ((5, 3), (2, 0))
        and windows[1][2] == ((1, 2), (4, 5))
        and example_window[0][1] == 1
        and example_window[1] == (0, 1)
        and REPAIRED_EXAMPLE_ROW.endswith(
            r"\rightarrow \{\{1, 0\}, \{1, 1\}\}"
        )
    )
    ok &= periodic_model_ok
    print(
        "derived_periodic_NW_N_W_self_window_example_ignores_NW",
        "OK" if periodic_model_ok else "MISMATCH",
    )

    synthetic_patches = tuple(
        tuple(
            ((10 * y + x, 10 * y + x), (10 * y + x, 10 * y + x))
            for x in range(3)
        )
        for y in range(2)
    )
    assembled = flatten2d_uniform(synthetic_patches)
    assembly_ok = (
        len(assembled) == 4
        and {len(row) for row in assembled} == {6}
        and assembled[0] == (0, 0, 1, 1, 2, 2)
        and assembled[2] == (10, 10, 11, 11, 12, 12)
    )
    ok &= assembly_ok
    print(
        "derived_uniform_2x2_patch_grid_assembly_2H_by_2W",
        "OK" if assembly_ok else "MISMATCH", len(assembled), len(assembled[0]),
    )

    analog_and_boundary_ok = (
        "rules depend not only on the color of a single element" in at(1018)
        and "element immediately to its right" in at(1018)
        and "rightmost element is always dropped" in at(1022)
        and "SS2EvolveList" in at(12113)
        and "Partition[#, 2, 1]" in at(12113)
        and "highly uniform rules always yielding just one cell" in at(8028)
        and "squares produced to overlap" in at(2334)
        and "difficult to define an obvious notion of neighbors" in at(2352)
        and "no immediate way to generalize sequential substitution systems" in at(2366)
        and "fixed underlying geometrical structure" in at(2372)
        and "network system is fundamentally just a collection of nodes" in at(2376)
        and "explicit rules that specify how the system evolves" in at(2570)
        and "instead of having explicit rules for evolution" in at(2572)
        and "no explicit procedure" in at(2574)
        and "proof for one dimension breaks down in two dimensions" in at(2594)
        and "grid of black and white cells defined by the constraint" in at(2600)
    )
    ok &= analog_and_boundary_ok
    print(
        "source_T14_T26_T27_T29_T31_boundaries",
        "OK" if analog_and_boundary_ok else "MISMATCH",
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

    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in QUERIES.values()]
    monolith_query_text = {at(line_no) for line_no in union}
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

    monolith_witnesses = [
        (str(line_no), normalized_line(at(line_no))) for line_no in sorted(union)
    ]
    query_mapping: set[str] = set()
    query_mapping_ok = True
    for record in sorted(split_nonexact):
        witness, score = best_witness(split_record_text[record], monolith_witnesses)
        query_mapping.add(f"{record}->{witness}:{score:.6f}")
        query_mapping_ok &= score >= 0.50 and int(witness) in union
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
        "split_query_reverse_join", "OK" if split_query_ok else "MISMATCH",
        *split_query_actual, *split_exact_actual, *split_nonexact_actual,
        *query_mapping_actual,
    )

    exact_retained = {line_no for line_no in RETAINED if at(line_no) in split_texts}
    nonexact_retained = set(RETAINED) - exact_retained
    retained_mapping: set[str] = set()
    monolith_only: set[int] = set()
    for line_no in sorted(nonexact_retained):
        witness, score = best_witness(at(line_no), split_lines)
        if score >= 0.50:
            retained_mapping.add(f"{line_no}->{witness}:{score:.6f}")
        else:
            monolith_only.add(line_no)
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
    )
    ok &= split_retained_ok
    print(
        "split_retained_reverse_join", "OK" if split_retained_ok else "MISMATCH",
        *exact_retained_actual, *nonexact_retained_actual,
        *retained_mapping_actual, *monolith_only_actual,
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_patterns = (
        re.compile(r"^### Substitution Systems and Fractals$", re.I),
        re.compile(r"more intricate behavior requires interaction among elements", re.I),
    )
    atlas_hits = {
        line_no for line_no, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in atlas_patterns)
    }
    atlas_actual = (len(atlas_hits), digest(atlas_hits))
    atlas_ok = (
        len(atlas_lines) == 542
        and atlas_actual == EXPECTED_ATLAS_HITS
        and "Substitution Systems and Fractals" in atlas_lines[180]
        and "interaction among elements" in atlas_lines[182]
    )
    ok &= atlas_ok
    print("atlas_summary_only", "OK" if atlas_ok else "MISMATCH", *atlas_actual)

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[28] == "Neighbor-Dependent Two-Dimensional Substitution Systems,"
        and len(set(catalog_lines[1:])) == 45
        and "## 28. Neighbor-Dependent Two-Dimensional Substitution Systems" in taxonomy_text
        and "replacement for a tile can depend on neighboring tiles" in taxonomy_text
        and "Chapter 5 presents this as the two-dimensional analog" in taxonomy_text
        and "`context`: neighborhood offsets" in taxonomy_text
        and "`boundary_policy`" in taxonomy_text
        and "`update`: parallel contextual replacement" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only", "OK" if catalog_ok else "MISMATCH")

    architecture_inference_ok = (
        raster_ok
        and repair_ok
        and main_construction_ok
        and notes_ok
        and adaptive_extension_ok
        and periodic_model_ok
        and assembly_ok
        and analog_and_boundary_ok
    )
    ok &= architecture_inference_ok
    print(
        "source_fit_periodic_context_selector_plus_T26_patch_assembly_not_executor",
        "OK" if architecture_inference_ok else "MISMATCH",
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
