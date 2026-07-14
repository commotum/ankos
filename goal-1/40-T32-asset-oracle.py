#!/usr/bin/env python3
"""Fail-closed raster/provenance audit for T32 template constraints.

The native T32 visual record consists of the printed-page-213 two-example
plate, the printed-page-214/215 two-file catalog of 171 periodic witnesses,
and the printed-page-941 Notes plate that displays the 32 possible oriented
five-cell templates.  Relation assets cover the 1D allowed-block predecessor,
a 2D-substitution source, CA fixed-point/spacetime encodings, local-block
forcing, tiling/network relatives, and observer/application views.  Controls
cover T31/T33, solver landscapes, evolution-versus-invariance, exact-template
feature extraction, stochastic aggregation conditioned on templates, and a
CA feature extractor.  None is promoted to T32 native evidence.

Every governed JPEG is bound to one unique physical file, its exact monolith
and split-Markdown references, byte length, dimensions, SHA-256, assembly,
and evidence boundary.  No pixels are used to reconstruct a template table,
seed, configuration, trace, palette, or solver result.  The exact five-cell
template order is independently source-derived at BOOK:13513-13520; it is not
a transcription of the page-941 raster.  Thus all 42 assets are HASH_BOUND,
LIMITED_TRANSCRIBED is empty, and none is PIXEL_REPLAYED.  The source prose
also owns such facts as the two printed constraint numbers, the total of 32
possible templates, and the 171-pattern catalog count.

The image-line sets below were independently enumerated and are stable.  The
verifier also binds the frozen source oracle's final image partition, while
all physical-file and split-reference evidence remains independently checked.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T32 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/40-T32-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_lines(values: set[int] | frozenset[int]) -> str:
    return sha256(",".join(map(str, sorted(values))).encode("ascii"))


book_bytes = BOOK.read_bytes()
assert len(book_bytes.decode("utf-8").splitlines()) == EXPECTED_BOOK_LINES
assert sha256(book_bytes) == EXPECTED_BOOK_SHA256
BOOK_LINES = book_bytes.decode("utf-8").splitlines()
IMAGE_RE = re.compile(r"^!\[[^]]*\]\(([^)]*?\.jpeg)\)$")
BOOK_IMAGES = {
    line_number: match.group(1)
    for line_number, line in enumerate(BOOK_LINES, 1)
    if (match := IMAGE_RE.fullmatch(line))
}


class AssetSpec(NamedTuple):
    role: str
    name: str
    physical: str
    split_markdown: str
    split_line: int
    byte_length: int
    width: int
    height: int
    digest: str
    assembly: str
    boundary: str


CHAPTER5 = "CHAPTERS/5-Two-Dimensions-and-Beyond"
CHAPTER7 = "CHAPTERS/7-Mechanisms-in-Programs-and-Nature"
CHAPTER9 = "CHAPTERS/9-Fundamental-Physics"
CHAPTER10 = "CHAPTERS/10-Processes-of-Perception-and-Analysis"
INDEX = "BACK-MATTER/Index"
COLOPHON = "BACK-MATTER/Colophon"

ASSETS = {
    2322: AssetSpec(
        "R-T26-NESTED-SOURCE", "_page_203_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_203_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 179,
        295_361, 1141, 1349,
        "e898fd8f8039ae055dbcbfba6d7128e91e7b1f857f6bd0e994a67d0f454dd2ff",
        "-", "2D-substitution gallery cited as a source of nested patterns; not a constraint model",
    ),
    2576: AssetSpec(
        "C-T31-1D-UNIQUE", "_page_225_Picture_5.jpeg",
        f"{CHAPTER5}/Images/_page_225_Picture_5.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 405,
        6_337, 881, 34,
        "f17d16990ae3b165d316d52bf3412e28ff3645f56fd5472bbdac36486871df3a",
        "-", "T31 one-dimensional neighbor-count constraint; orientation is not represented",
    ),
    2584: AssetSpec(
        "C-T31-1D-PERMISSIVE", "_page_226_Picture_2.jpeg",
        f"{CHAPTER5}/Images/_page_226_Picture_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 413,
        18_960, 885, 132,
        "d40d24b2ee67bbb22698755054ab438bdb04809f8ed7332b29765b8709d9eea0",
        "-", "T31 one-dimensional count/profile control; not an oriented template set",
    ),
    2598: AssetSpec(
        "C-T31-2D-COUNT-WITNESS", "_page_226_Picture_9.jpeg",
        f"{CHAPTER5}/Images/_page_226_Picture_9.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 427,
        37_372, 480, 342,
        "6d25b292bb7a1d01eb7a745fde1eafd36416133e23e7852773abc205a246717b",
        "-", "T31 center-conditioned neighbor-count witness; not exact oriented matching",
    ),
    2606: AssetSpec(
        "C-T31-COUNT-GALLERY", "_page_227_Figure_3.jpeg",
        f"{CHAPTER5}/Images/_page_227_Figure_3.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 435,
        306_964, 1143, 1089,
        "36beded6e40b45e1007ef8d8b631ed24d492bd8f411ae069eeca2614ced3d682",
        "-", "T31 count-profile gallery immediately preceding the T32 orientation boundary",
    ),
    2616: AssetSpec(
        "N-T32-TWO-CONSTRAINT-EXAMPLES", "_page_228_Figure_5.jpeg",
        f"{CHAPTER5}/Images/_page_228_Figure_5.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 445,
        118_339, 887, 387,
        "85384087ad022c63c28840a67dd25d6afca2dcdf2fc02aaec7d64ebbfd66c21e",
        "-", "native T32 examples; exact glyph tables and cell arrays remain unrecovered",
    ),
    2626: AssetSpec(
        "N-T32-171-CATALOG-A", "_page_229_Picture_1.jpeg",
        f"{CHAPTER5}/Images/_page_229_Picture_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 451,
        528_780, 1239, 1462,
        "e9e718444e44af1d3a41a229e44927d65d3691aaf098c8d964f0d88e7e01dc79",
        "catalog_171", "first physical half of the native catalog; entries are not pixel-decoded",
    ),
    2628: AssetSpec(
        "N-T32-171-CATALOG-B", "_page_230_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_230_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 453,
        470_834, 1165, 1226,
        "2af86815dd48d0c17257587b822add600b9a1736d18f17b20c2dbfcaae7a043b",
        "catalog_171", "second physical half of the native catalog; entries are not pixel-decoded",
    ),
    2638: AssetSpec(
        "C-T33-REQUIRED-OCCURRENCE-GALLERY", "_page_231_Picture_4.jpeg",
        f"{CHAPTER5}/Images/_page_231_Picture_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 463,
        193_577, 1180, 497,
        "938db44090a9b4ba5ea13349757d126e7b0c694796bd981227f92c53f9771586",
        "-", "T33 begins by requiring a template occurrence; not native unseeded T32",
    ),
    2662: AssetSpec(
        "C-T33-SEARCH-STAGES", "_page_233_Figure_1.jpeg",
        f"{CHAPTER5}/Images/_page_233_Figure_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 487,
        138_025, 918, 708,
        "5a1e25b7b903562a6acd946933aa43541e34cc8d07b0b2d4c154e18621f1844c",
        "-", "T33 anchored solver/search trace; gray search state is not configuration alphabet",
    ),
    2670: AssetSpec(
        "C-T33-NONPERIODIC-SEEDED", "_page_234_Figure_2.jpeg",
        f"{CHAPTER5}/Images/_page_234_Figure_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 495,
        314_108, 1197, 1185,
        "24e34e823066f1884d8a682d8ad04d13fdc59a0289cd97cb16139b2a33095dba",
        "-", "T33 required-template nonperiodic example; existential condition is essential",
    ),
    2682: AssetSpec(
        "C-T33-RULE60-PART-A", "_page_235_Picture_4.jpeg",
        f"{CHAPTER5}/Images/_page_235_Picture_4.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 505,
        20_869, 533, 152,
        "5a9b08141b7d1e281be90b375ca59dc637058350a560d86b3bb585608ce87a29",
        "t33_rule60", "T33 3x3/rule-60 construction part; requires first-template occurrence",
    ),
    2686: AssetSpec(
        "C-T33-RULE60-PART-B", "_page_235_Picture_6.jpeg",
        f"{CHAPTER5}/Images/_page_235_Picture_6.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 509,
        133_681, 576, 572,
        "717a2b642c45c185720ab26ae877f8396b487c7dd344960736a43607146f4cd0",
        "t33_rule60", "T33 3x3/rule-60 construction companion; no native T32 table claim",
    ),
    2690: AssetSpec(
        "C-T33-RULE30-PART-A", "_page_236_Picture_1.jpeg",
        f"{CHAPTER5}/Images/_page_236_Picture_1.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 513,
        193_879, 1192, 635,
        "8657ab025bb0e8aaccecf078f0ea5949d177c2eb49dcef65e39febdac7201c3c",
        "t33_rule30", "T33 3x3/rule-30 forced-complexity construction part",
    ),
    2692: AssetSpec(
        "C-T33-RULE30-PART-B", "_page_236_Picture_2.jpeg",
        f"{CHAPTER5}/Images/_page_236_Picture_2.jpeg",
        f"{CHAPTER5}/Two-Dimensions-and-Beyond.md", 515,
        31_242, 576, 178,
        "9010ea53f9ecf7f45ff84a106e6959f1d30d73045e7de4c3e199acdb7a98acb1",
        "t33_rule30", "T33 3x3/rule-30 construction companion; required occurrence is distinct",
    ),
    4040: AssetSpec(
        "C-SOLVER-LANDSCAPE-A", "_page_361_Figure_7.jpeg",
        f"{CHAPTER7}/Images/_page_361_Figure_7.jpeg",
        f"{CHAPTER7}/Mechanisms-in-Programs-and-Nature.md", 611,
        5_370, 277, 172,
        "0202c6b41b0c506de64b3f9c71c7177114d8fc681ff56720a37fc443663f9efa",
        "solver_landscape", "optimization analogy part A; external search is not T32 semantics",
    ),
    4042: AssetSpec(
        "C-SOLVER-LANDSCAPE-B", "_page_361_Figure_8.jpeg",
        f"{CHAPTER7}/Images/_page_361_Figure_8.jpeg",
        f"{CHAPTER7}/Mechanisms-in-Programs-and-Nature.md", 613,
        6_202, 272, 187,
        "e329e90008163ba261920c5ee4f486e6647b661d12b8a2cd4bc980f337d84587",
        "solver_landscape", "optimization analogy part B; local minima are solver behavior",
    ),
    4044: AssetSpec(
        "C-SOLVER-LANDSCAPE-C", "_page_361_Figure_9.jpeg",
        f"{CHAPTER7}/Images/_page_361_Figure_9.jpeg",
        f"{CHAPTER7}/Mechanisms-in-Programs-and-Nature.md", 615,
        5_736, 284, 177,
        "fe01dc70f470ff7724d641f2dc7faaca8fe95c0a3153952196d94d944fca9303",
        "solver_landscape", "discrete constraint-landscape analogy; not a model or proof",
    ),
    4074: AssetSpec(
        "C-ELEMENTARY-INVARIANT-CA-A", "_page_363_Picture_7.jpeg",
        f"{CHAPTER7}/Images/_page_363_Picture_7.jpeg",
        f"{CHAPTER7}/Mechanisms-in-Programs-and-Nature.md", 645,
        6_991, 220, 142,
        "4b7812c66ba736164526457f476a999582bc8ffb37aa5cb9b3a1699eff29b31c",
        "elementary_invariant_pair", "CA evolution that reaches an invariant state; control only",
    ),
    4076: AssetSpec(
        "C-ELEMENTARY-INVARIANT-CA-B", "_page_363_Picture_9.jpeg",
        f"{CHAPTER7}/Images/_page_363_Picture_9.jpeg",
        f"{CHAPTER7}/Mechanisms-in-Programs-and-Nature.md", 647,
        15_637, 228, 159,
        "d87280d6d085c7284ee5f6b8870c39a6f96f35a53e2798801d59dd306a639d33",
        "elementary_invariant_pair", "CA with uniform invariants that does not settle; control only",
    ),
    4080: AssetSpec(
        "R-2D-CA-FIXED-POINT", "_page_364_Figure_2.jpeg",
        f"{CHAPTER7}/Images/_page_364_Figure_2.jpeg",
        f"{CHAPTER7}/Mechanisms-in-Programs-and-Nature.md", 651,
        116_597, 989, 397,
        "81bf29a27913353b89e4e32d4b9ccf8a8af86c863077527b912a773c58c968d2",
        "-", "2D CA trajectories with a T32 invariant relation; evolution is not a solver",
    ),
    5786: AssetSpec(
        "R-NETWORK-CONSTRAINT-ANALOG", "_page_498_Picture_1.jpeg",
        f"{CHAPTER9}/Images/_page_498_Picture_1.jpeg",
        f"{CHAPTER9}/Fundamental-Physics.md", 621,
        151_593, 1200, 1134,
        "093b64cd96ee2dc310aac0ed471e881f4bf63705b4d0f2ddf53ac849c6b5ad30",
        "-", "network-template analog on a graph carrier; not the T32 square-lattice profile",
    ),
    6940: AssetSpec(
        "C-FEATURE-MATCHING-A", "_page_594_Picture_5.jpeg",
        f"{CHAPTER10}/Images/_page_594_Picture_5.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md", 353,
        28_460, 263, 247,
        "a45e5167bdcb769d5c8fac3d2598515f45c88a7f8f9873bb0d8e7bae12a84e14",
        "feature_matching", "exact-template feature detector part A; observer, not model-set semantics",
    ),
    6942: AssetSpec(
        "C-FEATURE-MATCHING-B", "_page_594_Picture_6.jpeg",
        f"{CHAPTER10}/Images/_page_594_Picture_6.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md", 355,
        27_326, 269, 259,
        "42d56967b498077397ef788fd3919d4b1b448cd44cffffd0366270ee5db25af0",
        "feature_matching", "exact-template feature detector part B; output is not satisfaction",
    ),
    6944: AssetSpec(
        "C-FEATURE-MATCHING-C", "_page_594_Picture_7.jpeg",
        f"{CHAPTER10}/Images/_page_594_Picture_7.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md", 357,
        28_041, 272, 261,
        "af08e1c6ec6f8a1192dc68ffa9a0aee9fed1c0400b2a514e8b845db0773930d1",
        "feature_matching", "second feature-matching example part A; not T32 configuration data",
    ),
    6946: AssetSpec(
        "C-FEATURE-MATCHING-D", "_page_594_Picture_8.jpeg",
        f"{CHAPTER10}/Images/_page_594_Picture_8.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md", 359,
        26_618, 261, 264,
        "8bfc57a4dcab2c648754f7dfc014777bd7b3dc830b2535ffe3c2701164d407c9",
        "feature_matching", "second feature-matching example part B; observer control only",
    ),
    6974: AssetSpec(
        "R-REPETITIVE-BLOCK-OBSERVER", "_page_597_Picture_4.jpeg",
        f"{CHAPTER10}/Images/_page_597_Picture_4.jpeg",
        f"{CHAPTER10}/Processes-of-Perception-and-Analysis.md", 387,
        117_732, 1176, 288,
        "af141871d07013cbc96cc7668acf1f54d903ae3f2f1f87f2933435b165780cc6",
        "-", "observer gallery cross-referencing page 215; not a template constraint table",
    ),
    14042: AssetSpec(
        "R-1D-ALLOWED-BLOCK-DEBRUIJN", "_page_956_Picture_2.jpeg",
        f"{INDEX}/Images/_page_956_Picture_2.jpeg",
        f"{INDEX}/Index.md", 1943,
        31_826, 575, 293,
        "f593e5c3b7438d4bf47428ed3474451c436c5e1572d009c4ad201b4687961ad6",
        "-", "one-dimensional allowed-block/de Bruijn relation; carrier is not T32 2D",
    ),
    14052: AssetSpec(
        "N-T32-ORDERED-32-TEMPLATE-KEY", "_page_956_Picture_8.jpeg",
        f"{INDEX}/Images/_page_956_Picture_8.jpeg",
        f"{INDEX}/Index.md", 1953,
        16_014, 573, 80,
        "c869c2839aee8d0f4319646140de881e57eef5165df901ca0de079b9e4510e4e",
        "-", "native Notes key; raster untranscribed, while tuple order is source-derived at 13513-20",
    ),
    14111: AssetSpec(
        "R-16-COLOR-LOCAL-BLOCK-FORCING", "_page_957_Picture_14.jpeg",
        f"{INDEX}/Images/_page_957_Picture_14.jpeg",
        f"{INDEX}/Index.md", 2012,
        11_244, 560, 84,
        "957c224462a36129efb03f2413788e4bc4a4f0606372f27dc67ca1df05b87b35",
        "-", "16-color 2x2 allowed-block forcing relation; exact 51 blocks unrecovered",
    ),
    14117: AssetSpec(
        "R-CA-SPACETIME-TEMPLATE", "_page_958_Picture_4.jpeg",
        f"{INDEX}/Images/_page_958_Picture_4.jpeg",
        f"{INDEX}/Index.md", 2018,
        6_294, 561, 36,
        "245be117b883ed09e8f5fa56750351c77686dbebe6acf67943249afe7d47f009",
        "-", "rule-30 spacetime allowed-template relation; not CA evolution or native T32 data",
    ),
    14136: AssetSpec(
        "R-POLYOMINO-SET-A", "_page_958_Picture_14.jpeg",
        f"{INDEX}/Images/_page_958_Picture_14.jpeg",
        f"{INDEX}/Index.md", 2037,
        6_209, 235, 113,
        "6e2b1cf80ec33ace8df4fa467421ac5a125d8ddf75152868c73f50d21068ec10",
        "polyomino_tiling", "polyomino tiling relation part A; distinct carrier/matching semantics",
    ),
    14138: AssetSpec(
        "R-POLYOMINO-SET-B", "_page_958_Picture_15.jpeg",
        f"{INDEX}/Images/_page_958_Picture_15.jpeg",
        f"{INDEX}/Index.md", 2039,
        6_339, 326, 109,
        "a7f419934ce41465427c5daa4a8536234bb95f4d5a83ed30909378301e78cd77",
        "polyomino_tiling", "polyomino tiling relation part B; shapes are not T32 cell labels",
    ),
    14142: AssetSpec(
        "R-POLYOMINO-CONSTRUCTION", "_page_958_Picture_17.jpeg",
        f"{INDEX}/Images/_page_958_Picture_17.jpeg",
        f"{INDEX}/Index.md", 2043,
        71_912, 595, 356,
        "1b61b17be3fc38d6494849ed1a67be69d9658afd61d0be3549743f8a3357fc64",
        "polyomino_tiling", "polyomino construction companion; not a T32 model witness",
    ),
    15211: AssetSpec(
        "C-AGGREGATION-TEMPLATE-DYNAMIC-A", "_page_994_Picture_3.jpeg",
        f"{INDEX}/Images/_page_994_Picture_3.jpeg",
        f"{INDEX}/Index.md", 3112,
        3_818, 119, 109,
        "bbae1064a5c23d5e9638c8587d33c804de3eb0f7cd907b7d5065d89693831c4d",
        "aggregation_template_gallery", "template-conditioned stochastic growth A; dynamic control",
    ),
    15213: AssetSpec(
        "C-AGGREGATION-TEMPLATE-DYNAMIC-B", "_page_994_Picture_4.jpeg",
        f"{INDEX}/Images/_page_994_Picture_4.jpeg",
        f"{INDEX}/Index.md", 3114,
        3_789, 107, 112,
        "b1430c29bed143b063fbc07a34f1b5232d87fc479d90b2beca1afd87df5abd6f",
        "aggregation_template_gallery", "template-conditioned stochastic growth B; dynamic control",
    ),
    15215: AssetSpec(
        "C-AGGREGATION-TEMPLATE-DYNAMIC-C", "_page_994_Picture_5.jpeg",
        f"{INDEX}/Images/_page_994_Picture_5.jpeg",
        f"{INDEX}/Index.md", 3116,
        3_379, 110, 119,
        "7d47e459b95d2f9765ab732968f40db589be265d0691f06b267b75aa487962a9",
        "aggregation_template_gallery", "template-conditioned stochastic growth C; dynamic control",
    ),
    15217: AssetSpec(
        "C-AGGREGATION-TEMPLATE-DYNAMIC-D", "_page_994_Picture_6.jpeg",
        f"{INDEX}/Images/_page_994_Picture_6.jpeg",
        f"{INDEX}/Index.md", 3118,
        2_430, 107, 115,
        "c7214b5edb00142fdf7b117089a2fa8fe763aafbeac051c0575e9d1a1eb76d5a",
        "aggregation_template_gallery", "template-conditioned stochastic growth D; dynamic control",
    ),
    15219: AssetSpec(
        "C-AGGREGATION-TEMPLATE-DYNAMIC-E", "_page_994_Picture_7.jpeg",
        f"{INDEX}/Images/_page_994_Picture_7.jpeg",
        f"{INDEX}/Index.md", 3120,
        2_528, 100, 136,
        "301f9a8a252bfc39f65c0fe450c17ca5a9cd6a961bb020b590f40d4e40c08e31",
        "aggregation_template_gallery", "template-conditioned stochastic growth E; dynamic control",
    ),
    16375: AssetSpec(
        "R-SYMMETRIC-GRAPH-TEMPLATE", "_page_1047_Picture_11.jpeg",
        f"{INDEX}/Images/_page_1047_Picture_11.jpeg",
        f"{INDEX}/Index.md", 4276,
        24_424, 532, 168,
        "6741bdbfbc784f0428517083d681feec8b0abbee46151676b051584211d91c73",
        "-", "whole-network symmetric-template relation; graph carrier remains distinct",
    ),
    17433: AssetSpec(
        "C-CA-FEATURE-EXTRACTION", "_page_1092_Picture_6.jpeg",
        f"{INDEX}/Images/_page_1092_Picture_6.jpeg",
        f"{INDEX}/Index.md", 5336,
        21_682, 583, 141,
        "b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6",
        "-", "single-step CA feature extraction; observer control, not T32 satisfaction",
    ),
    17465: AssetSpec(
        "R-TEXTURE-MINIMAL-PATTERNS", "_page_1093_Picture_6.jpeg",
        f"{COLOPHON}/Images/_page_1093_Picture_6.jpeg",
        f"{COLOPHON}/Colophon.md", 22,
        14_942, 555, 98,
        "b1b2a6ab123cc672995f0c53bf9207a5606a7d8043d3135756c6b173b83e1a79",
        "-", "texture-generation relation for 2x2 local patterns; raster rules unrecovered",
    ),
}


NATIVE_IMAGE_LINES = frozenset({2616, 2626, 2628, 14052})
RELATION_IMAGE_LINES = frozenset(
    {2322, 4080, 5786, 6974, 14042, 14111, 14117, 14136, 14138, 14142,
     16375, 17465}
)
CONTROL_IMAGE_LINES = frozenset(
    {2576, 2584, 2598, 2606, 2638, 2662, 2670, 2682, 2686, 2690, 2692,
     4040, 4042, 4044, 4074, 4076, 6940, 6942, 6944, 6946,
     15211, 15213, 15215, 15217, 15219, 17433}
)
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
assert GOVERNED_IMAGE_LINES == frozenset(ASSETS)
assert not (
    NATIVE_IMAGE_LINES & RELATION_IMAGE_LINES
    or NATIVE_IMAGE_LINES & CONTROL_IMAGE_LINES
    or RELATION_IMAGE_LINES & CONTROL_IMAGE_LINES
)
assert (
    len(NATIVE_IMAGE_LINES),
    len(RELATION_IMAGE_LINES),
    len(CONTROL_IMAGE_LINES),
    len(GOVERNED_IMAGE_LINES),
) == (4, 12, 26, 42)
assert digest_lines(NATIVE_IMAGE_LINES) == (
    "116eddcbd978b9193b877cb54568c69f3a139585f90caf4445c1f81dcd91c322"
)
assert digest_lines(RELATION_IMAGE_LINES) == (
    "f950133f7c777867e778109e1e636054a5ce806579e43ea3cd2ee52bea48a806"
)
assert digest_lines(CONTROL_IMAGE_LINES) == (
    "6ae50cda27274b79ac14af3f95ca5c23b7b7dd9a8b953679760c64180dc34861"
)
assert digest_lines(GOVERNED_IMAGE_LINES) == (
    "1c06663f8fd6c6d760ed5cbb6e004e65544c40e1acf72080e06fb6ba6f7902df"
)


ASSEMBLIES = {
    assembly: frozenset(
        line for line, asset in ASSETS.items() if asset.assembly == assembly
    )
    for assembly in {asset.assembly for asset in ASSETS.values()} - {"-"}
}
assert ASSEMBLIES == {
    "catalog_171": frozenset({2626, 2628}),
    "t33_rule60": frozenset({2682, 2686}),
    "t33_rule30": frozenset({2690, 2692}),
    "solver_landscape": frozenset({4040, 4042, 4044}),
    "elementary_invariant_pair": frozenset({4074, 4076}),
    "feature_matching": frozenset({6940, 6942, 6944, 6946}),
    "polyomino_tiling": frozenset({14136, 14138, 14142}),
    "aggregation_template_gallery": frozenset(
        {15211, 15213, 15215, 15217, 15219}
    ),
}
assert sum(map(len, ASSEMBLIES.values())) == 23


# These are source-routed candidates that are not owned by a retained T32
# caption, a "pictures below" passage, or a facing-page continuation.  The
# exclusions prevent mere proximity from importing another family/passage.
ADJACENCY_EXCLUSIONS = {
    2314: ("_page_202_Picture_4.jpeg", "T26 page-187 example, not the cited page-188 gallery"),
    2328: ("_page_204_Picture_4.jpeg", "T27 geometric-substitution result companion"),
    2330: ("_page_204_Picture_5.jpeg", "T27 geometric-substitution rule companion"),
    2564: ("_page_224_Picture_6.jpeg", "multiway network immediately before constraint section"),
    5804: ("_page_500_Figure_3.jpeg", "explicit reversible-CA evolution after network constraints"),
    6926: ("_page_593_Picture_1.jpeg", "source texture mosaic, not a constraint template set"),
    6952: ("_page_595_Picture_1.jpeg", "perception filter bank, not declarative constraints"),
    6954: ("_page_595_Picture_2.jpeg", "perception filter bank companion"),
    6964: ("_page_596_Figure_2.jpeg", "feature-density observer, not T32 satisfaction"),
    6982: ("_page_598_Figure_2.jpeg", "T26 nested-substitution observer after relation"),
    14273: ("_page_964_Picture_11.jpeg", "3D CA moving structure owned by the preceding passage"),
    17113: ("_page_1083_Figure_4.jpeg", "Ramsey run figure; 17115 is only a comparison route"),
    17457: ("_page_1093_Picture_2.jpeg", "dithering predecessor"),
    17461: ("_page_1093_Picture_4.jpeg", "nested-pattern gray observer"),
    17469: ("_page_1093_Picture_8.jpeg", "CA-generated texture successor"),
    17475: ("_page_1093_Picture_11.jpeg", "Moire-pattern successor"),
    17479: ("_page_1093_Picture_13.jpeg", "Moire-pattern continuation"),
    17483: ("_page_1093_Picture_15.jpeg", "Moire proximity-join continuation"),
}
EXCLUDED_IMAGE_LINES = frozenset(ADJACENCY_EXCLUSIONS)
assert GOVERNED_IMAGE_LINES.isdisjoint(EXCLUDED_IMAGE_LINES)
for excluded_line, (excluded_name, _reason) in ADJACENCY_EXCLUSIONS.items():
    assert BOOK_LINES[excluded_line - 1] == f"![]({excluded_name})"


# Candidate scope is an explicit source-derived closure, grouped by the
# passage that owns or excludes each raster.  It is intentionally not formed
# by an arbitrary numeric radius around a query hit.
SOURCE_DERIVED_CANDIDATE_GROUPS = {
    "T26_link_and_T27_boundary": frozenset({2314, 2322, 2328, 2330}),
    "main_constraint_section": frozenset(
        {2564, 2576, 2584, 2598, 2606, 2616, 2626, 2628, 2638, 2662,
         2670, 2682, 2686, 2690, 2692}
    ),
    "solver_landscape": frozenset({4040, 4042, 4044}),
    "invariant_relation": frozenset({4074, 4076, 4080}),
    "network_analogy": frozenset({5786, 5804}),
    "observer_caption_chain": frozenset(
        {6926, 6940, 6942, 6944, 6946, 6952, 6954, 6964, 6974, 6982}
    ),
    "notes_template_chain": frozenset(
        {14042, 14052, 14111, 14117, 14136, 14138, 14142}
    ),
    "no_initial_conditions_adjacency": frozenset({14273}),
    "aggregation_template_dynamics": frozenset(
        {15211, 15213, 15215, 15217, 15219}
    ),
    "network_notes": frozenset({16375}),
    "pattern_avoidance_cross_reference": frozenset({17113}),
    "feature_extraction_and_texture": frozenset(
        {17433, 17457, 17461, 17465, 17469, 17475, 17479, 17483}
    ),
}
CANDIDATE_IMAGE_LINES = frozenset().union(
    *SOURCE_DERIVED_CANDIDATE_GROUPS.values()
)
assert sum(map(len, SOURCE_DERIVED_CANDIDATE_GROUPS.values())) == len(
    CANDIDATE_IMAGE_LINES
)
assert all(line in BOOK_IMAGES for line in CANDIDATE_IMAGE_LINES)
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()
assert CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
assert len(CANDIDATE_IMAGE_LINES) == 60
assert digest_lines(EXCLUDED_IMAGE_LINES) == (
    "c50b84ca950cd076ddc8a53ea0528e1aad2ecbc83bedeee51d70054115756edc"
)
assert digest_lines(CANDIDATE_IMAGE_LINES) == (
    "5035af79590acbc957ba6d9d49aac97b29bd39ad5a7505968f4c5b09d0d95321"
)

CLASSIFICATION = {
    **{line: "N" for line in NATIVE_IMAGE_LINES},
    **{line: "R" for line in RELATION_IMAGE_LINES},
    **{line: "C" for line in CONTROL_IMAGE_LINES},
    **{line: "X" for line in EXCLUDED_IMAGE_LINES},
}
assert frozenset(CLASSIFICATION) == CANDIDATE_IMAGE_LINES
assert tuple(CLASSIFICATION.values()).count("N") == 4
assert tuple(CLASSIFICATION.values()).count("R") == 12
assert tuple(CLASSIFICATION.values()).count("C") == 26
assert tuple(CLASSIFICATION.values()).count("X") == 18


HASH_BOUND = GOVERNED_IMAGE_LINES
LIMITED_TRANSCRIBED: frozenset[int] = frozenset()
PIXEL_REPLAYED: frozenset[int] = frozenset()
assert LIMITED_TRANSCRIBED <= HASH_BOUND
assert PIXEL_REPLAYED <= LIMITED_TRANSCRIBED
assert (len(HASH_BOUND), len(LIMITED_TRANSCRIBED), len(PIXEL_REPLAYED)) == (42, 0, 0)

UNRECOVERED_RASTER_SEMANTICS = frozenset(
    {
        "native example cell arrays and exact fundamental-domain encodings",
        "all 171 catalog tiles and their printed numeric labels",
        "catalog minimality, uniqueness, or exhaustive-sufficiency proof",
        "exact 51-block 16-color relation table",
        "T33 required template tables, anchors, seeds, and traces",
        "network, polyomino, CA-spacetime, and texture raster rule details",
        "palette-to-symbol mapping for every governed plate",
        "any solver/search transition inferred from displayed intermediate pictures",
    }
)
assert len(UNRECOVERED_RASTER_SEMANTICS) == 8

# These semantics are exact, but their evidence is text/code rather than a
# pixel transcription.  BOOK:13513 fixes the offset order, BOOK:13515-13520
# constructs all neighborhood tuples in order, and BOOK:14050 maps rule-number
# bit positions to that list.  The two numbered main examples are consequently
# decodable without reading their rendered glyphs.
SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED = frozenset(
    {
        "ordered 32 five-cell neighborhood tuples from BOOK:13513-13520",
        "constraint 1384774 allowed-template set from BOOK:2618/14050",
        "constraint 328778790 allowed-template set from BOOK:2618/14050",
    }
)
assert len(SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED) == 3


# These are prose-owned facts, not raster transcriptions.  They make explicit
# what can safely be said while the pixel content above remains unrecovered.
SOURCE_GUARDS = {
    2318: "next page gives some more examples of two-dimensional substitution systems",
    2326: "nothing about this basic process that depends on the squares being arranged",
    2332: "take account of the orientation of that square",
    2572: "instead of having explicit rules for evolution",
    2596: "every black cell should have exactly one black neighbor",
    2608: "constraints which specify that every black cell and every white cell",
    2614: "match a fixed set of possible templates",
    2618: "templates of neighboring cells overlapping",
    2620: "There are a total of 4,294,967,296 possible sets",
    2630: "complete collection of all 171 patterns",
    2634: "a particular template from this set must appear at least somewhere",
    2640: "a certain template from this set must occur at least once",
    2664: "Gray is used to indicate cells whose colors have not yet been determined",
    2674: "at least somewhere in the pattern a template containing",
    2684: "requirement that the first template must appear at least somewhere",
    2694: "with the first template appearing at least once",
    4046: "basic phenomenon which makes it difficult to find patterns that satisfy constraints",
    4078: "Two of the 28 elementary cellular automata whose only invariant states",
    4082: "leave only the pattern on the right invariant",
    5788: "network constraint systems shown here are analogs",
    6948: "cells sensitive to the 2 x 2 template shown on the left",
    6976: "Page 215 shows patterns obtained in systems based on constraints",
    13513: "offset lists are always taken to be in the order given by *Sort*",
    13520: "shown on page 53 for elementary rules and page 941 for 5-neighbor rules",
    14040: "only some of the  $k^n$  possible blocks of cells",
    14048: "removing any of the allowed templates prevents the constraint",
    14050: "Position[IntegerDigits[n, 2, 32], 1]",
    14055: "A set of allowed templates can be specified",
    14099: "generate a large class of nested patterns",
    14109: "only 51 of the 65,536 possible 2×2 blocks",
    14115: "represented in terms of a set of allowed templates",
    14124: "constraints discussed here are similar to those encountered in covering the plane",
    14134: "close to the grid-based constraint systems discussed in the main text",
    14271: "successive steps in the evolution of a moving structure",
    14275: "Systems based on constraints do not have initial conditions",
    15207: "positions whose neighborhoods match specific templates",
    16373: "template being the whole network",
    17111: "every single possible sequence contains at least one run of length 3",
    17115: "Compare pattern-avoiding sequences on page 944",
    17431: "single step of the 16 even-numbered totalistic 5-neighbor rules",
    17459: "best impression of uniform gray",
    17463: "match some definite set of templates",
}
for source_line, fragment in SOURCE_GUARDS.items():
    assert fragment in BOOK_LINES[source_line - 1], (source_line, fragment)


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read a JPEG SOF marker without depending on an image library."""

    assert data[:2] == b"\xff\xd8"
    sof = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    offset = 2
    while offset < len(data):
        while offset < len(data) and data[offset] != 0xFF:
            offset += 1
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        assert offset < len(data)
        marker = data[offset]
        offset += 1
        if marker in {0x00, 0x01} or 0xD0 <= marker <= 0xD9:
            continue
        segment_size = int.from_bytes(data[offset : offset + 2], "big")
        if marker in sof:
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            return width, height
        offset += segment_size
    raise AssertionError("JPEG SOF marker not found")


def load_source_oracle():
    """Load the frozen source audit without depending on the caller's cwd."""

    assert SOURCE_ORACLE_PATH.is_file(), "T32 source oracle is not frozen"
    spec = importlib.util.spec_from_file_location("t32_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_source_interface() -> None:
    """Bind the source audit's final source-owned image partition."""

    source = load_source_oracle()
    required = {
        "NATIVE_IMAGE_LINES": NATIVE_IMAGE_LINES,
        "RELATION_IMAGE_LINES": RELATION_IMAGE_LINES,
        "CONTROL_IMAGE_LINES": CONTROL_IMAGE_LINES,
        "GOVERNED_IMAGE_LINES": GOVERNED_IMAGE_LINES,
        "EXCLUDED_IMAGE_LINES": EXCLUDED_IMAGE_LINES,
        "CANDIDATE_IMAGE_LINES": CANDIDATE_IMAGE_LINES,
    }
    for attribute, expected in required.items():
        actual = frozenset(getattr(source, attribute))
        assert actual == expected, (attribute, sorted(actual), sorted(expected))

    catalog = tuple(source.source_template_catalog())
    assert len(catalog) == len(set(catalog)) == 32
    assert all(len(template) == 5 and set(template) <= {0, 1} for template in catalog)
    example_numbers = (1_384_774, 328_778_790)
    example_allowed = tuple(
        frozenset(source.allowed_from_constraint_number(number))
        for number in example_numbers
    )
    assert tuple(map(len, example_allowed)) == (8, 12)
    assert tuple(
        source.constraint_number_from_allowed(allowed)
        for allowed in example_allowed
    ) == example_numbers


def ledger() -> tuple[str, int, int, int, int]:
    """Verify every asset and return the canonical provenance ledger."""

    split_markdown = sorted(
        path
        for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(split_markdown) == 17

    monolith_by_name: dict[str, list[int]] = {}
    for line_number, reference in BOOK_IMAGES.items():
        monolith_by_name.setdefault(Path(reference).name, []).append(line_number)

    split_by_name: dict[str, list[tuple[Path, int]]] = {}
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    for markdown in split_markdown:
        for line_number, line in enumerate(
            markdown.read_text(encoding="utf-8").splitlines(), 1
        ):
            if match := split_re.fullmatch(line):
                split_by_name.setdefault(match.group(1), []).append(
                    (markdown, line_number)
                )

    physical_by_name: dict[str, list[Path]] = {}
    for path in SOURCE_ROOT.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)

    rows: list[str] = []
    hashes: set[str] = set()
    total_bytes = 0
    monolith_references = 0
    split_references = 0
    for book_line, asset in sorted(ASSETS.items()):
        kind = (
            "N" if book_line in NATIVE_IMAGE_LINES
            else "R" if book_line in RELATION_IMAGE_LINES
            else "C"
        )
        assert BOOK_LINES[book_line - 1] == f"![]({asset.name})"
        assert monolith_by_name.get(asset.name) == [book_line]

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(expected_split, asset.split_line)], (book_line, split_hits)

        expected_physical = SOURCE_ROOT / asset.physical
        physical_hits = physical_by_name.get(asset.name, [])
        assert physical_hits == [expected_physical], (book_line, physical_hits)

        data = expected_physical.read_bytes()
        digest = sha256(data)
        assert len(data) == asset.byte_length, (book_line, len(data), asset.byte_length)
        assert jpeg_size(data) == (asset.width, asset.height)
        assert digest == asset.digest, (book_line, digest, asset.digest)
        assert digest not in hashes, (book_line, digest)

        hashes.add(digest)
        total_bytes += len(data)
        monolith_references += 1
        split_references += 1
        rows.append(
            "|".join(
                (
                    str(book_line), kind, asset.role, asset.physical,
                    str(asset.byte_length), str(asset.width), str(asset.height),
                    asset.digest, asset.split_markdown, str(asset.split_line),
                    asset.assembly, asset.boundary,
                )
            )
        )

    payload = "\n".join(rows) + "\n"
    return payload, monolith_references, split_references, len(hashes), total_bytes


EXPECTED_LEDGER_SHA256 = "a8c3becaa4ebf8926130421eee5b43fe2c3756e74121e59ae5d291b18bd11ba0"


def main() -> None:
    verify_source_interface()
    payload, monolith_refs, split_refs, hashes, total_bytes = ledger()
    ledger_digest = sha256(payload.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger", ledger_digest, EXPECTED_LEDGER_SHA256,
    )
    assert (monolith_refs, split_refs, hashes, total_bytes) == (
        42, 42, 42, 3_571_461,
    )
    print(
        "T32 asset oracle: PASS governed=42; classes N/R/C=4/12/26; "
        "candidates=60; excluded=18; refs=84(monolith=42,split=42); "
        "unique_hashes=42; bytes=3571461; assemblies=8/23_files; "
        "boundary=42_HASH_BOUND/0_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        "template_order=source-derived_not-pixel-transcribed; "
        "raster_tables/seeds/traces=unrecovered; "
        "unresolved_image_dispositions=0"
    )


if __name__ == "__main__":
    main()
