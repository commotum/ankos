#!/usr/bin/env python3
"""Fail-closed raster/provenance audit for T33 seeded constraints.

T33 is the static constraint construction obtained by conjoining an exact
allowed-local-pattern relation with a global requirement that a designated
allowed pattern occur at least once.  Its native visual record is the
printed-page-216 gallery, the printed-page-218 search plate, the page-219
forced nonperiodic example, and the paired page-220/page-221 rule-60/rule-30
constructions.  The displayed search stages are evidence about the examples,
not a transition trace of the declarative system.

This audit also keeps the T31/T32/T34 sibling plates as explicit controls and
retains the source-routed substitution, CA, tiling, graph, observer, and
pattern-forcing relations.  Candidate scope follows captions, facing-page
assemblies, Notes/Index routes, and named sibling boundaries; it is not an
arbitrary line-radius search.

Every governed JPEG is bound to one physical file, one monolith reference,
one split-Markdown reference, exact bytes, dimensions, SHA-256, evidence
role, and assembly.  No pixel is used to invent a required pattern, allowed
table, anchor, field, search decision, proof, palette, or transition.  All
governed assets are therefore HASH_BOUND, with no LIMITED_TRANSCRIBED or
PIXEL_REPLAYED asset.
"""

from __future__ import annotations

import hashlib
import re
import runpy
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T33 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/41-T33-source-oracle.py"

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


# Compact, frozen manifest.  Each row is independently checked below against
# the monolith, all split Markdown files, and all physical JPEGs.
ASSET_ROWS = r"""
1449|C-T34-ADD-ONE|_page_132_Figure_10.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_132_Figure_10.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|53|56915|169|1250|396c235b7d5d7881de7a4823778065c557644da9738a61b4052de918e5d2e8b5|-|T34 exact scalar addition rendered as digits; transition control, not a model-set relation
1455|C-T34-ADD-CONSTANTS|_page_133_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_133_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|59|118982|887|697|c58ad8ce64d656841e1f7ab6f6692179b5d662da59a8285c401865fff3ff438c|-|T34 add-constant gallery; digit rows are views of evolving scalar state
1463|C-T34-MULTIPLY-TWO|_page_134_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_134_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|67|46524|448|453|c011a897557eaac9fba56c0c470c74763c3812c0f6bdcb253e1b4ad3a3969dba|t34_multiplication_pair|first half of the T34 fixed-multiplication sibling plate
1465|C-T34-MULTIPLY-THREE|_page_134_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_134_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|69|62569|645|420|eaacf39d1a4f8af165ae9ba01756514b205aec56a4729496c0d38adde9b5d109|t34_multiplication_pair|second half of the T34 fixed-multiplication sibling plate
1481|C-T34-POWERS-THREE|_page_135_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_135_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|85|384807|1187|1342|d76cde1ce58580d77777613fc8c4abf3fa05d114c0fedade7152bb660d4d7945|-|T34 powers-of-three digit view; no global existential constraint
1487|C-T34-RATIONAL-MULTIPLY|_page_136_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_136_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|91|183701|1171|756|d4859c1d1e6f3efcfbe910e4bd6d734ebe4aea19b2189c079851d5dc12fa8e7e|-|T34 exact rational multiplication; transition sibling control
1493|C-T34-FRACTIONAL-OBSERVER|_page_137_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_137_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|97|34574|1175|186|31f00bec35b2895c74fea00cb6026073d6075d5d33006f988994edc95c5389c6|-|T34 fractional-part observer; not a T33 solution field
2322|R-T26-NESTED-SOURCE|_page_203_Figure_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_203_Figure_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|179|295361|1141|1349|e898fd8f8039ae055dbcbfba6d7128e91e7b1f857f6bd0e994a67d0f454dd2ff|-|2D-substitution gallery cited as a source of candidate nested patterns
2576|C-T31-1D-UNIQUE|_page_225_Picture_5.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_225_Picture_5.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|405|6337|881|34|f17d16990ae3b165d316d52bf3412e28ff3645f56fd5472bbdac36486871df3a|-|T31 neighbor-count constraint; no required exact pattern
2584|C-T31-1D-PERMISSIVE|_page_226_Picture_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_226_Picture_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|413|18960|885|132|d40d24b2ee67bbb22698755054ab438bdb04809f8ed7332b29765b8709d9eea0|-|T31 count/profile control; not an occurrence relation
2598|C-T31-2D-COUNT-WITNESS|_page_226_Picture_9.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_226_Picture_9.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|427|37372|480|342|6d25b292bb7a1d01eb7a745fde1eafd36416133e23e7852773abc205a246717b|-|T31 center-conditioned count witness; not exact-oriented or existential
2606|C-T31-COUNT-GALLERY|_page_227_Figure_3.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_227_Figure_3.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|435|306964|1143|1089|36beded6e40b45e1007ef8d8b631ed24d492bd8f411ae069eeca2614ced3d682|-|T31 count-profile gallery before the T32/T33 boundary
2616|C-T32-TWO-CONSTRAINT-EXAMPLES|_page_228_Figure_5.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_228_Figure_5.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|445|118339|887|387|85384087ad022c63c28840a67dd25d6afca2dcdf2fc02aaec7d64ebbfd66c21e|-|T32 allowed-template examples without a required occurrence
2626|C-T32-171-CATALOG-A|_page_229_Picture_1.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_229_Picture_1.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|451|528780|1239|1462|e9e718444e44af1d3a41a229e44927d65d3691aaf098c8d964f0d88e7e01dc79|catalog_171|first half of T32 periodic catalog; entries remain untranscribed
2628|C-T32-171-CATALOG-B|_page_230_Figure_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_230_Figure_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|453|470834|1165|1226|2af86815dd48d0c17257587b822add600b9a1736d18f17b20c2dbfcaae7a043b|catalog_171|second half of T32 periodic catalog; no required template
2638|N-T33-REQUIRED-OCCURRENCE-GALLERY|_page_231_Picture_4.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_231_Picture_4.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|463|193577|1180|497|938db44090a9b4ba5ea13349757d126e7b0c694796bd981227f92c53f9771586|-|native T33 gallery; exact displayed required patterns and fields remain unrecovered
2662|N-T33-SEARCH-STAGES|_page_233_Figure_1.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_233_Figure_1.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|487|138025|918|708|5a1e25b7b903562a6acd946933aa43541e34cc8d07b0b2d4c154e18621f1844c|-|native source example plate; gray/backtracking stages are external search evidence
2670|N-T33-NONPERIODIC-SEEDED|_page_234_Figure_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_234_Figure_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|495|314108|1197|1185|24e34e823066f1884d8a682d8ad04d13fdc59a0289cd97cb16139b2a33095dba|-|native required-template nonperiodic model; pixels do not supply a proof
2682|N-T33-RULE60-PART-A|_page_235_Picture_4.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_235_Picture_4.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|505|20869|533|152|5a9b08141b7d1e281be90b375ca59dc637058350a560d86b3bb585608ce87a29|t33_rule60|native 33-template/rule-60 construction part; table untranscribed
2686|N-T33-RULE60-PART-B|_page_235_Picture_6.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_235_Picture_6.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|509|133681|576|572|717a2b642c45c185720ab26ae877f8396b487c7dd344960736a43607146f4cd0|t33_rule60|native rule-60 construction companion; field pixels untranscribed
2690|N-T33-RULE30-PART-A|_page_236_Picture_1.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_236_Picture_1.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|513|193879|1192|635|8657ab025bb0e8aaccecf078f0ea5949d177c2eb49dcef65e39febdac7201c3c|t33_rule30|native 56-template/rule-30 construction part; table untranscribed
2692|N-T33-RULE30-PART-B|_page_236_Picture_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_236_Picture_2.jpeg|CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md|515|31242|576|178|9010ea53f9ecf7f45ff84a106e6959f1d30d73045e7de4c3e199acdb7a98acb1|t33_rule30|native rule-30 construction companion; pixels untranscribed
4040|C-SOLVER-LANDSCAPE-A|_page_361_Figure_7.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_361_Figure_7.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md|611|5370|277|172|0202c6b41b0c506de64b3f9c71c7177114d8fc681ff56720a37fc443663f9efa|solver_landscape|optimization analogy A; search is outside T33 denotation
4042|C-SOLVER-LANDSCAPE-B|_page_361_Figure_8.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_361_Figure_8.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md|613|6202|272|187|e329e90008163ba261920c5ee4f486e6647b661d12b8a2cd4bc980f337d84587|solver_landscape|optimization analogy B; local minima are solver behavior
4044|C-SOLVER-LANDSCAPE-C|_page_361_Figure_9.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_361_Figure_9.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md|615|5736|284|177|fe01dc70f470ff7724d641f2dc7faaca8fe95c0a3153952196d94d944fca9303|solver_landscape|optimization analogy C; not model data or a proof
4074|C-ELEMENTARY-INVARIANT-CA-A|_page_363_Picture_7.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_363_Picture_7.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md|645|6991|220|142|4b7812c66ba736164526457f476a999582bc8ffb37aa5cb9b3a1699eff29b31c|elementary_invariant_pair|CA evolution/invariant control; no required occurrence
4076|C-ELEMENTARY-INVARIANT-CA-B|_page_363_Picture_9.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_363_Picture_9.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md|647|15637|228|159|d87280d6d085c7284ee5f6b8870c39a6f96f35a53e2798801d59dd306a639d33|elementary_invariant_pair|CA evolution/invariant control; not T33 satisfaction
4080|R-2D-CA-FIXED-POINT|_page_364_Figure_2.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Images/_page_364_Figure_2.jpeg|CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md|651|116597|989|397|81bf29a27913353b89e4e32d4b9ccf8a8af86c863077527b912a773c58c968d2|-|CA trajectories whose invariant fields obey local constraints; relation only
5786|R-NETWORK-CONSTRAINT-ANALOG|_page_498_Picture_1.jpeg|CHAPTERS/9-Fundamental-Physics/Images/_page_498_Picture_1.jpeg|CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md|621|151593|1200|1134|093b64cd96ee2dc310aac0ed471e881f4bf63705b4d0f2ddf53ac849c6b5ad30|-|network-template analog on a graph carrier; distinct occurrence geometry
6940|C-FEATURE-MATCHING-A|_page_594_Picture_5.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_594_Picture_5.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|353|28460|263|247|a45e5167bdcb769d5c8fac3d2598515f45c88a7f8f9873bb0d8e7bae12a84e14|feature_matching|template detector A; observation is not existential satisfaction
6942|C-FEATURE-MATCHING-B|_page_594_Picture_6.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_594_Picture_6.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|355|27326|269|259|42d56967b498077397ef788fd3919d4b1b448cd44cffffd0366270ee5db25af0|feature_matching|template detector output; not a T33 model
6944|C-FEATURE-MATCHING-C|_page_594_Picture_7.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_594_Picture_7.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|357|28041|272|261|af08e1c6ec6f8a1192dc68ffa9a0aee9fed1c0400b2a514e8b845db0773930d1|feature_matching|second feature detector A; observer control
6946|C-FEATURE-MATCHING-D|_page_594_Picture_8.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_594_Picture_8.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|359|26618|261|264|8bfc57a4dcab2c648754f7dfc014777bd7b3dc830b2535ffe3c2701164d407c9|feature_matching|second feature detector B; observer control
6974|R-REPETITIVE-BLOCK-OBSERVER|_page_597_Picture_4.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_597_Picture_4.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|387|117732|1176|288|af141871d07013cbc96cc7668acf1f54d903ae3f2f1f87f2933435b165780cc6|-|observer gallery cross-referencing T32 periodic models
14042|R-1D-ALLOWED-BLOCK-DEBRUIJN|_page_956_Picture_2.jpeg|BACK-MATTER/Index/Images/_page_956_Picture_2.jpeg|BACK-MATTER/Index/Index.md|1943|31826|575|293|f593e5c3b7438d4bf47428ed3474451c436c5e1572d009c4ad201b4687961ad6|-|1D allowed-block relation; different carrier and occurrence scope
14052|C-T32-ORDERED-32-TEMPLATE-KEY|_page_956_Picture_8.jpeg|BACK-MATTER/Index/Images/_page_956_Picture_8.jpeg|BACK-MATTER/Index/Index.md|1953|16014|573|80|c869c2839aee8d0f4319646140de881e57eef5165df901ca0de079b9e4510e4e|-|T32 Notes key; raster order remains untranscribed here
14111|R-16-COLOR-LOCAL-BLOCK-FORCING|_page_957_Picture_14.jpeg|BACK-MATTER/Index/Images/_page_957_Picture_14.jpeg|BACK-MATTER/Index/Index.md|2012|11244|560|84|957c224462a36129efb03f2413788e4bc4a4f0606372f27dc67ca1df05b87b35|-|16-color local blocks force nesting without supplying T33 native data
14117|R-CA-SPACETIME-TEMPLATE|_page_958_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_958_Picture_4.jpeg|BACK-MATTER/Index/Index.md|2018|6294|561|36|245be117b883ed09e8f5fa56750351c77686dbebe6acf67943249afe7d47f009|-|rule-30 spacetime allowed-template relation; encoding, not evolution here
14136|R-POLYOMINO-SET-A|_page_958_Picture_14.jpeg|BACK-MATTER/Index/Images/_page_958_Picture_14.jpeg|BACK-MATTER/Index/Index.md|2037|6209|235|113|6e2b1cf80ec33ace8df4fa467421ac5a125d8ddf75152868c73f50d21068ec10|polyomino_tiling|nonperiodic tiling relation A; distinct matching carrier
14138|R-POLYOMINO-SET-B|_page_958_Picture_15.jpeg|BACK-MATTER/Index/Images/_page_958_Picture_15.jpeg|BACK-MATTER/Index/Index.md|2039|6339|326|109|a7f419934ce41465427c5daa4a8536234bb95f4d5a83ed30909378301e78cd77|polyomino_tiling|nonperiodic tiling relation B; distinct matching carrier
14142|R-POLYOMINO-CONSTRUCTION|_page_958_Picture_17.jpeg|BACK-MATTER/Index/Images/_page_958_Picture_17.jpeg|BACK-MATTER/Index/Index.md|2043|71912|595|356|1b61b17be3fc38d6494849ed1a67be69d9658afd61d0be3549743f8a3357fc64|polyomino_tiling|polyomino construction companion; not a T33 field witness
15211|C-AGGREGATION-TEMPLATE-DYNAMIC-A|_page_994_Picture_3.jpeg|BACK-MATTER/Index/Images/_page_994_Picture_3.jpeg|BACK-MATTER/Index/Index.md|3112|3818|119|109|bbae1064a5c23d5e9638c8587d33c804de3eb0f7cd907b7d5065d89693831c4d|aggregation_template_gallery|template-conditioned stochastic growth A; dynamic control
15213|C-AGGREGATION-TEMPLATE-DYNAMIC-B|_page_994_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_994_Picture_4.jpeg|BACK-MATTER/Index/Index.md|3114|3789|107|112|b1430c29bed143b063fbc07a34f1b5232d87fc479d90b2beca1afd87df5abd6f|aggregation_template_gallery|template-conditioned stochastic growth B; dynamic control
15215|C-AGGREGATION-TEMPLATE-DYNAMIC-C|_page_994_Picture_5.jpeg|BACK-MATTER/Index/Images/_page_994_Picture_5.jpeg|BACK-MATTER/Index/Index.md|3116|3379|110|119|7d47e459b95d2f9765ab732968f40db589be265d0691f06b267b75aa487962a9|aggregation_template_gallery|template-conditioned stochastic growth C; dynamic control
15217|C-AGGREGATION-TEMPLATE-DYNAMIC-D|_page_994_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_994_Picture_6.jpeg|BACK-MATTER/Index/Index.md|3118|2430|107|115|c7214b5edb00142fdf7b117089a2fa8fe763aafbeac051c0575e9d1a1eb76d5a|aggregation_template_gallery|template-conditioned stochastic growth D; dynamic control
15219|C-AGGREGATION-TEMPLATE-DYNAMIC-E|_page_994_Picture_7.jpeg|BACK-MATTER/Index/Images/_page_994_Picture_7.jpeg|BACK-MATTER/Index/Index.md|3120|2528|100|136|301f9a8a252bfc39f65c0fe450c17ca5a9cd6a961bb020b590f40d4e40c08e31|aggregation_template_gallery|template-conditioned stochastic growth E; dynamic control
16375|R-SYMMETRIC-GRAPH-TEMPLATE|_page_1047_Picture_11.jpeg|BACK-MATTER/Index/Images/_page_1047_Picture_11.jpeg|BACK-MATTER/Index/Index.md|4276|24424|532|168|6741bdbfbc784f0428517083d681feec8b0abbee46151676b051584211d91c73|-|whole-graph template relation; distinct global object semantics
17433|C-CA-FEATURE-EXTRACTION|_page_1092_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_1092_Picture_6.jpeg|BACK-MATTER/Index/Index.md|5336|21682|583|141|b13e50f8bb2f7e905b8580ea94d93c7295e5967125aa8042defe76936bdb1dd6|-|single-step CA feature extraction; observer/update control
17465|R-TEXTURE-MINIMAL-PATTERNS|_page_1093_Picture_6.jpeg|BACK-MATTER/Colophon/Images/_page_1093_Picture_6.jpeg|BACK-MATTER/Colophon/Colophon.md|22|14942|555|98|b1b2a6ab123cc672995f0c53bf9207a5606a7d8043d3135756c6b173b83e1a79|-|texture generated from minimal local patterns; relation raster untranscribed
""".strip()


def parse_assets(rows: str) -> dict[int, AssetSpec]:
    assets: dict[int, AssetSpec] = {}
    for row in rows.splitlines():
        fields = row.split("|", 11)
        assert len(fields) == 12, row
        line = int(fields[0])
        assert line not in assets
        assets[line] = AssetSpec(
            fields[1], fields[2], fields[3], fields[4], int(fields[5]),
            int(fields[6]), int(fields[7]), int(fields[8]), fields[9],
            fields[10], fields[11],
        )
    return assets


ASSETS = parse_assets(ASSET_ROWS)

NATIVE_IMAGE_LINES = frozenset({2638, 2662, 2670, 2682, 2686, 2690, 2692})
RELATION_IMAGE_LINES = frozenset(
    {2322, 4080, 5786, 6974, 14042, 14111, 14117, 14136, 14138, 14142,
     16375, 17465}
)
CONTROL_IMAGE_LINES = frozenset(ASSETS) - NATIVE_IMAGE_LINES - RELATION_IMAGE_LINES
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
    len(NATIVE_IMAGE_LINES), len(RELATION_IMAGE_LINES),
    len(CONTROL_IMAGE_LINES), len(GOVERNED_IMAGE_LINES),
) == (7, 12, 30, 49)


ASSEMBLIES = {
    assembly: frozenset(
        line for line, asset in ASSETS.items() if asset.assembly == assembly
    )
    for assembly in {asset.assembly for asset in ASSETS.values()} - {"-"}
}
assert ASSEMBLIES == {
    "t34_multiplication_pair": frozenset({1463, 1465}),
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
assert sum(map(len, ASSEMBLIES.values())) == 25


# Every nearby/source-routed raster that is not governed is named and
# dispositioned.  In particular, line 1505 is the first predicate-branched
# T35 picture, while the seven preceding strict T34 pictures are controls.
ADJACENCY_EXCLUSIONS = {
    1505: ("_page_137_Picture_7.jpeg", "T35 parity-selected arithmetic begins here"),
    2314: ("_page_202_Picture_4.jpeg", "T26 page-187 example, not cited page-188 gallery"),
    2328: ("_page_204_Picture_4.jpeg", "T27 geometric-substitution result companion"),
    2330: ("_page_204_Picture_5.jpeg", "T27 geometric-substitution rule companion"),
    2564: ("_page_224_Picture_6.jpeg", "multiway network before the constraint section"),
    5804: ("_page_500_Figure_3.jpeg", "reversible-CA evolution after network constraints"),
    6926: ("_page_593_Picture_1.jpeg", "source texture mosaic, not constraint data"),
    6952: ("_page_595_Picture_1.jpeg", "perception filter bank"),
    6954: ("_page_595_Picture_2.jpeg", "perception filter-bank companion"),
    6964: ("_page_596_Figure_2.jpeg", "feature-density observer"),
    6982: ("_page_598_Figure_2.jpeg", "T26 nested-substitution observer"),
    14273: ("_page_964_Picture_11.jpeg", "3D CA motion owned by preceding passage"),
    17113: ("_page_1083_Figure_4.jpeg", "Ramsey run figure; comparison route only"),
    17457: ("_page_1093_Picture_2.jpeg", "dithering predecessor"),
    17461: ("_page_1093_Picture_4.jpeg", "nested-pattern gray observer"),
    17469: ("_page_1093_Picture_8.jpeg", "CA-generated texture successor"),
    17475: ("_page_1093_Picture_11.jpeg", "Moire-pattern successor"),
    17479: ("_page_1093_Picture_13.jpeg", "Moire continuation"),
    17483: ("_page_1093_Picture_15.jpeg", "Moire proximity-join continuation"),
}
EXCLUDED_IMAGE_LINES = frozenset(ADJACENCY_EXCLUSIONS)
assert GOVERNED_IMAGE_LINES.isdisjoint(EXCLUDED_IMAGE_LINES)
for excluded_line, (excluded_name, _reason) in ADJACENCY_EXCLUSIONS.items():
    assert BOOK_LINES[excluded_line - 1] == f"![]({excluded_name})"


SOURCE_DERIVED_CANDIDATE_GROUPS = {
    "T34_controls_and_T35_boundary": frozenset(
        {1449, 1455, 1463, 1465, 1481, 1487, 1493, 1505}
    ),
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
CANDIDATE_IMAGE_LINES = frozenset().union(*SOURCE_DERIVED_CANDIDATE_GROUPS.values())
assert sum(map(len, SOURCE_DERIVED_CANDIDATE_GROUPS.values())) == len(
    CANDIDATE_IMAGE_LINES
)
assert all(line in BOOK_IMAGES for line in CANDIDATE_IMAGE_LINES)
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()
assert CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
assert len(CANDIDATE_IMAGE_LINES) == 68


CLASSIFICATION = {
    **{line: "N" for line in NATIVE_IMAGE_LINES},
    **{line: "R" for line in RELATION_IMAGE_LINES},
    **{line: "C" for line in CONTROL_IMAGE_LINES},
    **{line: "X" for line in EXCLUDED_IMAGE_LINES},
}
assert frozenset(CLASSIFICATION) == CANDIDATE_IMAGE_LINES
assert tuple(CLASSIFICATION.values()).count("N") == 7
assert tuple(CLASSIFICATION.values()).count("R") == 12
assert tuple(CLASSIFICATION.values()).count("C") == 30
assert tuple(CLASSIFICATION.values()).count("X") == 19


HASH_BOUND = GOVERNED_IMAGE_LINES
LIMITED_TRANSCRIBED: frozenset[int] = frozenset()
PIXEL_REPLAYED: frozenset[int] = frozenset()
assert LIMITED_TRANSCRIBED <= HASH_BOUND
assert PIXEL_REPLAYED <= LIMITED_TRANSCRIBED
assert (len(HASH_BOUND), len(LIMITED_TRANSCRIBED), len(PIXEL_REPLAYED)) == (
    49, 0, 0,
)


UNRECOVERED_RASTER_SEMANTICS = frozenset(
    {
        "required cross-template glyphs displayed at centers of the page-216 gallery",
        "complete allowed-template sets and exact field arrays for all native examples",
        "the page-218 gray search states, choice order, deductions, and backtracking trace",
        "a raster-derived proof of existence, uniqueness, periodicity, or nonperiodicity",
        "the complete 33-entry rule-60 and 56-entry rule-30 3x3 template tables",
        "exact first required 3x3 templates and their occurrence coordinates",
        "palette-to-symbol maps, crop rules, and fundamental domains for governed plates",
        "any solver, transition, UPDATE, or initial-state semantics inferred from pictures",
    }
)
assert len(UNRECOVERED_RASTER_SEMANTICS) == 8


SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED = frozenset(
    {
        "required-occurrence prose at BOOK:2634-2640",
        "constraint numbers and repetition dimensions explicitly printed in captions",
        "page-219 coordinate formula at BOOK:14085-14095",
        "33-of-512 and 56-of-512 3x3 counts stated in prose",
        "rule-60 and rule-30 correspondence stated in prose",
    }
)
assert len(SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED) == 5


SOURCE_GUARDS = {
    1439: "the very simplest possible type of arithmetic rule",
    1497: "different operations depending on whether the number obtained at each step",
    2318: "next page gives some more examples of two-dimensional substitution systems",
    2634: "particular template from this set must appear at least somewhere",
    2640: "certain template from this set must occur at least once",
    2664: "Gray is used to indicate cells whose colors have not yet been determined",
    2674: "at least somewhere in the pattern a template containing",
    2684: "requirement that the first template must appear at least somewhere",
    2688: "56 allowed templates",
    2694: "with the first template appearing at least once",
    4046: "difficult to find patterns that satisfy constraints",
    14080: "extend patterns along a square spiral",
    14085: "Page 219 · Non-periodic pattern",
    14097: "every template in the set, must occur somewhere in the pattern",
    14099: "Forcing nested patterns",
    14115: "represented in terms of a set of allowed templates",
    14134: "force non-periodic patterns",
    14275: "Systems based on constraints do not have initial conditions",
    20769: "force, say, cellular automaton patterns to be generated, as on page 221",
}
for source_line, fragment in SOURCE_GUARDS.items():
    assert fragment in BOOK_LINES[source_line - 1], (source_line, fragment)


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read a JPEG SOF marker without an image-library dependency."""

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


def load_source_oracle() -> dict[str, object]:
    """Load the independent source audit without depending on caller cwd."""

    assert SOURCE_ORACLE_PATH.is_file(), "T33 source oracle is not frozen"
    return runpy.run_path(
        str(SOURCE_ORACLE_PATH), run_name="t33_source_oracle_asset_interface"
    )


def verify_source_interface() -> None:
    """Bind the source audit's final source-owned image partition exactly."""

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
        actual = frozenset(source[attribute])
        assert actual == expected, (attribute, sorted(actual), sorted(expected))


def ledger() -> tuple[str, int, int, int, int]:
    """Verify every governed asset and return the canonical provenance ledger."""

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
        kind = CLASSIFICATION[book_line]
        assert kind in {"N", "R", "C"}
        assert BOOK_LINES[book_line - 1] == f"![]({asset.name})"
        assert monolith_by_name.get(asset.name) == [book_line]

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(expected_split, asset.split_line)], (
            book_line, split_hits,
        )

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


# Frozen after independent reconciliation; deliberately impossible until the
# first full verifier run reports the recomputed value.
EXPECTED_LEDGER_SHA256 = "TO_BE_FROZEN"


def main() -> None:
    verify_source_interface()
    payload, monolith_refs, split_refs, hashes, total_bytes = ledger()
    ledger_digest = sha256(payload.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger", ledger_digest, EXPECTED_LEDGER_SHA256,
    )
    assert (monolith_refs, split_refs, hashes, total_bytes) == (
        49, 49, 49, 4_579_533,
    )
    print(
        "T33 asset oracle: PASS governed=49; classes N/R/C=7/12/30; "
        "candidates=68; excluded=19; refs=98(monolith=49,split=49); "
        "unique_hashes=49; bytes=4579533; assemblies=9/25_files; "
        "boundary=49_HASH_BOUND/0_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        "required_patterns/tables/search_trace=unrecovered; "
        "unresolved_image_dispositions=0"
    )


if __name__ == "__main__":
    main()
