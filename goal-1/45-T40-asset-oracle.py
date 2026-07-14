#!/usr/bin/env python3
"""Fail-closed asset/provenance audit for T40 constant representations.

The closed T40 image universe contains fifty-three governed JPEGs and ten
explicitly excluded sibling JPEGs.  Every candidate is bound to its sole
monolith reference, optional split-Markdown reference, physical path, byte
length, JPEG dimensions, and SHA-256 digest.  The split omits exactly the
page-154 long-division link and the page-156 square-root link even though both
physical files exist.

All sixty-three candidates are HASH_BOUND.  No formula, digit, remainder,
seed, coefficient, curve sample, palette, or program is inferred from pixels.
The long-division and strict integer square-root checks below independently
replay only formulas stated in source text; their JSON interface is
deliberately separate from the raster ledgers.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import runpy
import sys
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T40 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/45-T40-source-oracle.py"

EXPECTED_BOOK_LINES = 22_498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_lines(values: set[int] | frozenset[int]) -> str:
    return sha256(",".join(map(str, sorted(values))).encode("ascii"))


def digest_records(values: set[str] | frozenset[str]) -> str:
    """Hash an unordered record set with length-delimited UTF-8 framing."""

    payload = bytearray()
    for value in sorted(values):
        encoded = value.encode("utf-8")
        payload.extend(len(encoded).to_bytes(8, "big"))
        payload.extend(encoded)
    return sha256(bytes(payload))


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
    reason: str


def parse_assets(rows: str) -> dict[int, AssetSpec]:
    assets: dict[int, AssetSpec] = {}
    for row in rows.strip().splitlines():
        fields = row.split("|", 12)
        assert len(fields) == 13, row
        line = int(fields[0])
        assert line not in assets
        assets[line] = AssetSpec(
            fields[1], fields[2], fields[3], fields[4], int(fields[5]),
            int(fields[6]), int(fields[7]), int(fields[8]), fields[9],
            fields[10], fields[11], fields[12],
        )
    return assets


GOVERNED_ROWS = r"""
998|R-neighbor-independent-substitution-source|_page_98_Figure_2.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_98_Figure_2.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md|315|96138|1082|689|3f8f959f0661ca4019b451af24fd9236b58a858486178e4fb9bfd0105e337a8c|cross-page-substitution-four|HASH_BOUND|relation observer physically on page 98 and invoked by the retained page-83 substitution-system relation; no pixel-derived rule
1008|R-substitution-tree-source|_page_99_Figure_1.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_99_Figure_1.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md|325|132555|1188|621|9faa8b2973fdf9a11f77e4b9cf169cee9d907a429e1153a1af75923f79267592|cross-page-substitution-four|HASH_BOUND|relation observer physically on page 99 and invoked by the retained page-84 substitution-tree relation; no pixel-derived branching
1014|R-substitution-branch-source|_page_99_Picture_4.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_99_Picture_4.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md|331|46147|1158|325|49727d9cd4bd099d127fb4a3e531f665fd3bdcccbdd66c9a9181c4709cbbafae|cross-page-substitution-four|HASH_BOUND|relation observer physically on page 99 and invoked by the retained page-84 substitution-branch relation; no pixel-derived tree
1449|R-nested-binary-digit-source|_page_132_Figure_10.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_132_Figure_10.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|53|56915|169|1250|396c235b7d5d7881de7a4823778065c557644da9738a61b4052de918e5d2e8b5|cross-page-substitution-four|HASH_BOUND|relation observer physically on page 132 and invoked by the retained page-117 nested-digit relation; no pixel-derived sequence
1677|N-pi-binary-walk-observer|_page_151_Figure_7.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_151_Figure_7.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|259|62314|1153|533|f70a1bf71c4afb4073ce6f895f93202bd2e4974559d7824cbeefd789544856fc|-|HASH_BOUND|native 20000-digit base-two walk view; the constant, digits, horizon, and walk rule remain source text
1711|N-rational-long-division|_page_154_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_154_Figure_2.jpeg|-|0|102867|1133|472|b607ffb9d9b5d4d90108f77d04a2ca808157a98829a4af088c31ae54117f9ecd|-|HASH_BOUND|native rational base-two long-division remainder and digit panels; split image link is explicitly absent
1744|N-square-root-generator|_page_156_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_156_Figure_1.jpeg|-|0|139449|899|892|6774d48ee79161a4abb53235c3c44eec5a877655fd7a82e5eff0ac680efefaa2|-|HASH_BOUND|native strict-integer square-root r-s generator panels; split image link is explicitly absent
1846|R-trigonometric-crossing-family|_page_161_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_161_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|305|156748|1210|909|a478c2818f9c720ae68e528849ef3cda2f904c9a837ef97a8018f151e655e328|p161-162-crossing-cf-pair|HASH_BOUND|relation observer for sine-family crossing structure; the continued-fraction connection remains source text
1854|R-continued-fraction-substitution|_page_162_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_162_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|313|206693|1050|1155|ab5e7bbab2a14b3d4fb832dad43842ceb4f206653810d7dfcd23238095741cfe|p161-162-crossing-cf-pair|HASH_BOUND|relation observer for continued-fraction-driven generalized substitution; no coefficient stream is read from pixels
6768|R-number-representation-schemas|_page_575_Figure_5.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_575_Figure_5.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|181|58746|1143|404|3f81679d8812332b34c6f907dbb4fa0cf85bf512b0b56a856d77fb5874a6cdb7|p560-561-representation-pair|HASH_BOUND|relation observer for unary, binary, self-delimiting, and Fibonacci representations; codecs remain source text
6776|R-run-length-representation-application|_page_576_Figure_4.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_576_Figure_4.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|189|82301|1191|604|af6f0c64170d7ec290ff508bed88e6e6d5c01fb0bfe3d30131d7408d63c38efa|p560-561-representation-pair|HASH_BOUND|downstream run-length application of representation e; not a native T40 positional transition
7116|R-block-frequency-composite|_page_609_Picture_2.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Images/_page_609_Picture_2.jpeg|CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md|527|7463|242|165|a701cd6cd935009250ba7bd269517ffe382f60ddb4cb364b98fb5a2c1dd2eb37|-|HASH_BOUND|page-609 block-frequency composite invoked by the retained page-594 Sturmian relation; not a digit generator
9246|C-turing-complexity-resource-boundary|_page_776_Figure_2.jpeg|CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_776_Figure_2.jpeg|CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md|629|205466|1167|1215|77a6940d63479c1d9affe067bcee9cecdb6a17c032615cdcdfe5c87e01019ee0|-|HASH_BOUND|page-776 Turing-complexity control invoked by the retained page-761 resource boundary; no T40 mechanics inferred
11252|R-ca-cantor-map-representation|_page_884_Figure_30.jpeg|CHAPTERS/12-The-Principle-of-Computational-Equivalence/Images/_page_884_Figure_30.jpeg|CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md|2633|29517|593|408|0b46d9fe0de9337a7e2d5aaca5ea73445c601ca52e2a6165adb916b040482e7e|-|HASH_BOUND|relation observer for a cellular-automaton Cantor-map representation; not native T40 evolution
12524|R-gray-code-number-order|_page_916_Figure_12.jpeg|BACK-MATTER/Index/Images/_page_916_Figure_12.jpeg|BACK-MATTER/Index/Index.md|427|16342|561|150|96edfc6a58c171c735a75ec87f9d54f90135d953af15bd814c5206fb999a9d79|p916-918-representation-three|HASH_BOUND|followed Gray-code ordering relation behind the page-928 concatenation sibling; not a T40 positional-expansion rule
12552|R-negative-base-representation|_page_917_Picture_11.jpeg|BACK-MATTER/Index/Images/_page_917_Picture_11.jpeg|BACK-MATTER/Index/Index.md|455|9004|572|48|9d98da9314261068e9616f51b2f2ade3aca8497bc346e576de4c3efeccf7d214|p916-918-representation-three|HASH_BOUND|followed negative-base representation relation; strict T40 v1 remains positive-radix and does not infer digits from pixels
12557|R-multiplicative-digit-representation|_page_918_Figure_2.jpeg|BACK-MATTER/Index/Images/_page_918_Figure_2.jpeg|BACK-MATTER/Index/Index.md|460|12033|585|75|537e2542e9042a89760407db9f1526688b62a081faa2a43487023d1c9de14ba7|p916-918-representation-three|HASH_BOUND|followed multiplicative prime-exponent digit relation; not a positional-expansion rule and no pixel-derived coefficients
12960|N-rational-digit-panels|_page_927_Figure_14.jpeg|BACK-MATTER/Index/Images/_page_927_Figure_14.jpeg|BACK-MATTER/Index/Index.md|863|68967|596|372|8b72b409f1dcf50a971e51ebf9ba6827eb28d17d7fad4aa157e39a4ea71a6a8f|-|HASH_BOUND|native base-two rational m-over-n digit panels; period facts remain source text
12992|R-concatenation-digits|_page_928_Figure_9.jpeg|BACK-MATTER/Index/Images/_page_928_Figure_9.jpeg|BACK-MATTER/Index/Index.md|895|28539|563|123|ab7f30102a14fec2439ebcf44b8d93cc8d3c015a284cc2d6ce8b1d5b26de4742|p928-concatenation-walk-trilogy|HASH_BOUND|related concatenated integer-digit sequence; not a constant-expansion transition
12996|R-concatenation-walk|_page_928_Figure_11.jpeg|BACK-MATTER/Index/Images/_page_928_Figure_11.jpeg|BACK-MATTER/Index/Index.md|899|9524|565|131|1cc65d82eb4cfead5603b65fc1154aad1339ec38057c56a3ccd1abef38faaac0|p928-concatenation-walk-trilogy|HASH_BOUND|related signed walk over concatenated digits; rendering is not evolving source state
13000|R-concatenation-walk-leading-bit-dropped|_page_928_Figure_13.jpeg|BACK-MATTER/Index/Images/_page_928_Figure_13.jpeg|BACK-MATTER/Index/Index.md|903|10809|558|131|4d4b8af0951fbdaa13c573b937a3f91e084d0abcba3fd7669a5066dff2463261|p928-concatenation-walk-trilogy|HASH_BOUND|related leading-bit-dropped concatenation walk; no pixel-derived sequence
13020|R-gray-code-concatenation|_page_928_Figure_22.jpeg|BACK-MATTER/Index/Images/_page_928_Figure_22.jpeg|BACK-MATTER/Index/Index.md|923|11104|575|120|b3c8078954ef3cfcf77d64192c8efadc33a3debc66b4341acea74445932c05f8|-|HASH_BOUND|related Gray-code concatenation sibling; representation relation only
13040|N-continued-fraction-residual-a|_page_929_Picture_11.jpeg|BACK-MATTER/Index/Images/_page_929_Picture_11.jpeg|BACK-MATTER/Index/Index.md|943|2967|86|124|0c99889c7a16af4d386f7d247e4d0c4ce5ca2d5ce99666f51111ff034779383f|p929-continued-fraction-residual-six|HASH_BOUND|native continued-fraction residual-iterate panel A; values derive from source formula
13042|N-continued-fraction-residual-b|_page_929_Picture_12.jpeg|BACK-MATTER/Index/Images/_page_929_Picture_12.jpeg|BACK-MATTER/Index/Index.md|945|3987|80|120|13c357f3159570913ad6dd4b30417b36654bade4a3e7f301484341f4a89694d9|p929-continued-fraction-residual-six|HASH_BOUND|native continued-fraction residual-iterate panel B; values derive from source formula
13044|N-continued-fraction-residual-c|_page_929_Picture_13.jpeg|BACK-MATTER/Index/Images/_page_929_Picture_13.jpeg|BACK-MATTER/Index/Index.md|947|4752|83|134|a1a0b24aed2df1092057f7841e57f568ac2016faba8b301dc9affb09db633e5a|p929-continued-fraction-residual-six|HASH_BOUND|native continued-fraction residual-iterate panel C; values derive from source formula
13046|N-continued-fraction-residual-d|_page_929_Picture_14.jpeg|BACK-MATTER/Index/Images/_page_929_Picture_14.jpeg|BACK-MATTER/Index/Index.md|949|6592|110|138|808c58449cea98ef7dea79ade9e9162c65fb22f5f9476df5d14104b2693dd6e5|p929-continued-fraction-residual-six|HASH_BOUND|native continued-fraction residual-iterate panel D; values derive from source formula
13048|N-continued-fraction-residual-e|_page_929_Picture_15.jpeg|BACK-MATTER/Index/Images/_page_929_Picture_15.jpeg|BACK-MATTER/Index/Index.md|951|5255|94|144|f2b1839afe868e8b5b2e9d780a6df14f61c07df42bd18de856b115f39f6b91c0|p929-continued-fraction-residual-six|HASH_BOUND|native continued-fraction residual-iterate panel E; values derive from source formula
13050|N-continued-fraction-residual-f|_page_929_Picture_16.jpeg|BACK-MATTER/Index/Images/_page_929_Picture_16.jpeg|BACK-MATTER/Index/Index.md|953|5278|86|143|aa1c0d4ebcaa304421297a3a05811f8b2b21b332fa6048937ac066a059941765|p929-continued-fraction-residual-six|HASH_BOUND|native continued-fraction residual-iterate panel F; values derive from source formula
13076|R-concatenation-continued-fraction-term-sizes|_page_930_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_930_Picture_4.jpeg|BACK-MATTER/Index/Index.md|979|8601|558|72|e2763e60cefa158f9c67d8d32363ed8fa2432ffe4d632e4fe70e0c5b29f7807c|-|HASH_BOUND|related term-size observer for continued fractions of concatenation numbers
13090|N-rational-approximation-quality|_page_930_Figure_10.jpeg|BACK-MATTER/Index/Images/_page_930_Figure_10.jpeg|BACK-MATTER/Index/Index.md|993|26576|583|211|508a0c6d93dfd7445f132c3146629c57715ba1224b9731d4538bfc4c8abb95cc|-|HASH_BOUND|native observer of successive continued-fraction rational-approximation quality
13094|R-euclidean-algorithm-integers|_page_930_Picture_12.jpeg|BACK-MATTER/Index/Images/_page_930_Picture_12.jpeg|BACK-MATTER/Index/Index.md|997|10158|581|111|894ff4a528fdc5b9c8e8e5646089dbf05d07c64461a4b665af153dbfce8c27b2|p930-euclid-continued-fraction-pair|HASH_BOUND|Euclidean-algorithm relation whose square counts match continued-fraction terms
13098|R-euclidean-algorithm-real|_page_930_Picture_14.jpeg|BACK-MATTER/Index/Images/_page_930_Picture_14.jpeg|BACK-MATTER/Index/Index.md|1001|7138|576|107|ab3e169d6da3c1586da8832d62d83f31d03ef7382813442968ac3dbbc0e6eab0|p930-euclid-continued-fraction-pair|HASH_BOUND|real Euclidean-algorithm relation; not coefficient-stream state
13119|R-digital-slope-a|_page_931_Figure_9.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_9.jpeg|BACK-MATTER/Index/Index.md|1022|6165|120|158|bb11803238dda52fd8f63a292f7f2d96a4d7a75cfdbfe159cb190ff64916d0ca|p931-digital-slope-five|HASH_BOUND|digital-slope representation relation A; source formula supplies segments
13121|R-digital-slope-b|_page_931_Figure_10.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_10.jpeg|BACK-MATTER/Index/Index.md|1024|6840|122|147|2282818d058f61cf1e511c3a87d944bdabdd49c95a76a82e158f5dcc9007338c|p931-digital-slope-five|HASH_BOUND|digital-slope representation relation B; source formula supplies segments
13123|R-digital-slope-c|_page_931_Figure_11.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_11.jpeg|BACK-MATTER/Index/Index.md|1026|5429|103|161|e80bdf6b9e562f086ce6efb205dce5dd6a3200d383971e3883cda4dc74eabbb2|p931-digital-slope-five|HASH_BOUND|digital-slope representation relation C; source formula supplies segments
13125|R-digital-slope-d|_page_931_Figure_12.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_12.jpeg|BACK-MATTER/Index/Index.md|1028|6192|110|155|d4cd35ac79902f539674d4114bba8bd7a12a1674ef334903028ebcd9f1a260e8|p931-digital-slope-five|HASH_BOUND|digital-slope representation relation D; source formula supplies segments
13127|R-digital-slope-e|_page_931_Figure_13.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_13.jpeg|BACK-MATTER/Index/Index.md|1030|3562|75|155|66c9d76cf184c965d21af617adbf5c87b8a6d88632494eb5be39b46386dc5b95|p931-digital-slope-five|HASH_BOUND|digital-slope representation relation E; source formula supplies segments
13134|C-operator-representation-boundary|_page_931_Figure_17.jpeg|BACK-MATTER/Index/Images/_page_931_Figure_17.jpeg|BACK-MATTER/Index/Index.md|1037|31696|576|254|50b5d23c00d10b064ed4c26b03944ba2e793bdf3dd30d367d9314b273e58ec07|-|HASH_BOUND|operator-representation complexity control; no coefficient evolution is defined by the raster
14176|R-pell-continued-fraction-size|_page_960_Figure_3.jpeg|BACK-MATTER/Index/Images/_page_960_Figure_3.jpeg|BACK-MATTER/Index/Index.md|2077|16558|574|209|4909c893d1c85a6206b6b053284838c58721ff83f61ff7e81d334859bac69121|-|HASH_BOUND|relation observer for Pell continued-fraction term sizes; no coefficients are inferred from the raster
14925|R-billiard-cf-slope-a|_page_986_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_4.jpeg|BACK-MATTER/Index/Index.md|2826|2185|118|99|dce3420f6ab4b0cda93c35df05fc0f1af1477889fcf988251894fd4c53e94a2f|p986-billiard-cf-five|HASH_BOUND|billiard continued-fraction slope relation panel A; source text supplies the relation
14927|R-billiard-cf-slope-b|_page_986_Picture_5.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_5.jpeg|BACK-MATTER/Index/Index.md|2828|2449|93|92|0cf2cee6cf4e44d42f09a4116cfd09a5e622fc9799901fcf05cc4a744a17cfe6|p986-billiard-cf-five|HASH_BOUND|billiard continued-fraction slope relation panel B; source text supplies the relation
14929|R-billiard-cf-slope-c|_page_986_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_6.jpeg|BACK-MATTER/Index/Index.md|2830|4105|99|103|91ccba8bb1c4a855376d1573507072af4ae310e06aaeb751e4a4de912f518234|p986-billiard-cf-five|HASH_BOUND|billiard continued-fraction slope relation panel C; source text supplies the relation
14931|R-billiard-cf-slope-d|_page_986_Picture_7.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_7.jpeg|BACK-MATTER/Index/Index.md|2832|5402|92|96|5d4ced55b1fed2900320f0f2d61df6dc43e63339726c33bb1bcef528e0497608|p986-billiard-cf-five|HASH_BOUND|billiard continued-fraction slope relation panel D; source text supplies the relation
14933|R-billiard-cf-slope-e|_page_986_Picture_8.jpeg|BACK-MATTER/Index/Images/_page_986_Picture_8.jpeg|BACK-MATTER/Index/Index.md|2834|6253|102|111|a1983299e03d94a78d251a7116ede9184b32a24bf8e9f9a0402cd18420749b7f|p986-billiard-cf-five|HASH_BOUND|billiard continued-fraction slope relation panel E; source text supplies the relation
17167|R-number-representation-lengths|_page_1085_Figure_16.jpeg|BACK-MATTER/Index/Images/_page_1085_Figure_16.jpeg|BACK-MATTER/Index/Index.md|5068|11809|570|114|23d4a862a4d99266f778a28c18acce5b8c10f828a3d517799542091a2ff5c9fd|p1085-number-representation-pair|HASH_BOUND|followed page-560 observer comparing unary, binary, self-delimiting, base-3-coded, and Fibonacci representation lengths
17171|R-number-representation-completeness|_page_1085_Picture_18.jpeg|BACK-MATTER/Index/Images/_page_1085_Picture_18.jpeg|BACK-MATTER/Index/Index.md|5072|12491|573|134|93b9a5e9478a8757c6c8dc5ac9f0fa5974eeaad0e8bdd14ab89a29053cbb1317|p1085-number-representation-pair|HASH_BOUND|followed page-560 completeness observer for self-delimiting representation schemas; no pixel-derived codec
17762|R-rule60-difference-table|_page_1106_Picture_4.jpeg|BACK-MATTER/Colophon/Images/_page_1106_Picture_4.jpeg|BACK-MATTER/Colophon/Colophon.md|319|19649|567|141|1b1e146be02a30f906c2bcf535f9b50d87e763c907109925bcf2b4bcbf7a4595|-|HASH_BOUND|composite rule-60 difference-table relation including pi digits; not a T40 digit generator
17876|R-base-two-power-tree|_page_1109_Picture_5.jpeg|BACK-MATTER/Colophon/Images/_page_1109_Picture_5.jpeg|BACK-MATTER/Colophon/Colophon.md|433|3747|277|52|498e773d1bfb4f6342382c109cd82563202dac362dc929d7d8b1f84d7e719789|p1109-prefix-method-pair|HASH_BOUND|whole-prefix base-two power-tree computation observer; not a one-digit transition
17878|R-base-three-conversion|_page_1109_Picture_6.jpeg|BACK-MATTER/Colophon/Images/_page_1109_Picture_6.jpeg|BACK-MATTER/Colophon/Colophon.md|435|5011|280|52|2ba5d3697687cd5b224b5e4e61c934bef48a5bc230cd7aef4d16d59ee20dcfd7|p1109-prefix-method-pair|HASH_BOUND|whole-prefix base-three conversion observer; not a one-digit transition
20588|R-minimal-ca-repetitive-context|_page_1201_Picture_6.jpeg|BACK-MATTER/Colophon/Images/_page_1201_Picture_6.jpeg|BACK-MATTER/Colophon/Colophon.md|3145|100915|567|573|1f02e8e4d9a4875aacea4400d24d42187ce222f280eb9048230ce4f11cf3c2a1|p1201-minimal-ca-four|HASH_BOUND|minimal-CA repetitive-sequence context observer; not native T40 evolution
20594|R-minimal-ca-powers-of-two|_page_1201_Picture_9.jpeg|BACK-MATTER/Colophon/Images/_page_1201_Picture_9.jpeg|BACK-MATTER/Colophon/Colophon.md|3151|5685|142|154|ca8bd4d605adf94e71306497286b3220c56645d793b2d66514004f3c2741b9f0|p1201-minimal-ca-four|HASH_BOUND|minimal-CA powers-of-two relation observer; not native T40 evolution
20596|R-minimal-ca-squares|_page_1201_Picture_10.jpeg|BACK-MATTER/Colophon/Images/_page_1201_Picture_10.jpeg|BACK-MATTER/Colophon/Colophon.md|3153|5764|117|170|d63f0244a2aa68116b98e23024b7f0a595906de277838d954401329a36f944d5|p1201-minimal-ca-four|HASH_BOUND|minimal-CA squares relation observer; not native T40 evolution
20598|R-minimal-ca-thue-morse|_page_1201_Picture_11.jpeg|BACK-MATTER/Colophon/Images/_page_1201_Picture_11.jpeg|BACK-MATTER/Colophon/Colophon.md|3155|12744|278|175|8274d856359c610851e478a5dcdf376b2b25387c693787fcb028e688a1a8aa37|p1201-minimal-ca-four|HASH_BOUND|minimal-CA Thue-Morse relation observer; not native T40 evolution
"""

EXCLUDED_ROWS = r"""
1649|X-sequence-property-sibling-a|_page_150_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_150_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|231|44033|1185|241|aba1ec87beb6d6b3308ae2bc4e6e46f58592daf0134a715fd4b8a2f2faf6572b|X-p150-sequence-property-five|HASH_BOUND|page-150 sequence-property sibling observer A lies before the T40 mathematical-constants span
1651|X-sequence-property-sibling-b|_page_150_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_150_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|233|41035|1164|245|6e3dffd17a8a0e806b25fbd3db9b350ef0e217ef9e27c7e8253abdfb1d0ba1e1|X-p150-sequence-property-five|HASH_BOUND|page-150 sequence-property sibling observer B lies before the T40 mathematical-constants span
1653|X-sequence-property-sibling-c|_page_150_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_150_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|235|45042|1175|223|4a7e843f39f9e629e8c172ee9a8791201d6657519d93e59711d2be37de2a827d|X-p150-sequence-property-five|HASH_BOUND|page-150 sequence-property sibling observer C lies before the T40 mathematical-constants span
1655|X-sequence-property-sibling-d|_page_150_Figure_4.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_150_Figure_4.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|237|36180|1183|219|18fedd7b593d7c1db04bb4a1d93d8c1fe5bda4975224ec2d5ef7cc75c7f7dee9|X-p150-sequence-property-five|HASH_BOUND|page-150 sequence-property sibling observer D lies before the T40 mathematical-constants span
1657|X-sequence-property-sibling-e|_page_150_Figure_5.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_150_Figure_5.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|239|36172|1140|228|b7e272b42566d54cdf0b04e98581e4d77783bcd5947912b0edc68f37b613bdfe|X-p150-sequence-property-five|HASH_BOUND|page-150 sequence-property sibling observer E lies before the T40 mathematical-constants span
12844|X-pre-t40-prime-section-sibling|_page_923_Figure_21.jpeg|BACK-MATTER/Index/Images/_page_923_Figure_21.jpeg|BACK-MATTER/Index/Index.md|747|9807|576|79|d5f1729767f4379de49c08cb2508f5ce08e35fee6f28028e39e82a249f6fd160|-|HASH_BOUND|page-923 prime-section sibling observer is not T40 constant-representation evidence
12917|X-aliquot-sum-sibling|_page_926_Figure_14.jpeg|BACK-MATTER/Index/Images/_page_926_Figure_14.jpeg|BACK-MATTER/Index/Index.md|820|7898|563|104|d46dfaffe665ce852110f1e98054e1c25e2d8defd9b54c0f4273c7ab25ea79fa|-|HASH_BOUND|page-926 aliquot-sum sibling observer precedes the T40 Notes section
17593|X-least-squares-model-fit-sibling|_page_1099_Figure_1.jpeg|BACK-MATTER/Colophon/Images/_page_1099_Figure_1.jpeg|BACK-MATTER/Colophon/Colophon.md|150|8888|593|97|59eb6c37e2e3b98d9c342354563b78f97dced9f2bc5d22f73aa0a58a5de80743|-|HASH_BOUND|page-1099 least-squares model-fit sibling is not the later retained Sturmian relation
17847|X-visible-lattice-point-sibling|_page_1108_Figure_13.jpeg|BACK-MATTER/Colophon/Images/_page_1108_Figure_13.jpeg|BACK-MATTER/Colophon/Colophon.md|404|14375|566|154|679821a74b328013dc9970a6ced553e01310a9871f886fb93fd7344a5e1f0ab3|-|HASH_BOUND|page-1108 visible-lattice-point observer is an adjacent unrelated sibling
20584|X-doubling-rule-sibling|_page_1201_Picture_4.jpeg|BACK-MATTER/Colophon/Images/_page_1201_Picture_4.jpeg|BACK-MATTER/Colophon/Colophon.md|3141|18451|386|261|5ce5638ca129527ea5c5fc2c7e2fe7e204c8af5fbf7349d3da60f445634292b7|-|HASH_BOUND|page-1201 doubling-rule sibling precedes the governed minimal-CA sequence assembly
"""

ASSETS = parse_assets(GOVERNED_ROWS)
EXCLUDED_ASSETS = parse_assets(EXCLUDED_ROWS)

NATIVE_IMAGE_LINES = frozenset({
    1677, 1711, 1744, 12960,
    13040, 13042, 13044, 13046, 13048, 13050,
    13090,
})
RELATION_IMAGE_LINES = frozenset({
    998, 1008, 1014, 1449, 1846, 1854, 6768, 6776, 7116, 11252,
    12524, 12552, 12557, 12992, 12996, 13000, 13020, 13076, 13094, 13098,
    13119, 13121, 13123, 13125, 13127, 14176, 14925, 14927, 14929, 14931,
    14933, 17167, 17171, 17762, 17876, 17878, 20588, 20594, 20596, 20598,
})
CONTROL_IMAGE_LINES = frozenset({9246, 13134})
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES = frozenset(EXCLUDED_ASSETS)
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()

assert GOVERNED_IMAGE_LINES == frozenset(ASSETS)
assert not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
assert not (
    NATIVE_IMAGE_LINES & RELATION_IMAGE_LINES
    or NATIVE_IMAGE_LINES & CONTROL_IMAGE_LINES
    or RELATION_IMAGE_LINES & CONTROL_IMAGE_LINES
)
assert (
    len(NATIVE_IMAGE_LINES), len(RELATION_IMAGE_LINES),
    len(CONTROL_IMAGE_LINES), len(GOVERNED_IMAGE_LINES),
) == (11, 40, 2, 53)

EXPECTED_DISPOSITION_METRICS = (11, 40, 2, 53, 10)
EXPECTED_REFERENCE_METRICS = (53, 51, 104)
EXPECTED_EXCLUDED_REFERENCE_METRICS = (10, 10, 20)
EXPECTED_PHYSICAL_METRICS = (53, 53, 1_905_596)
EXPECTED_EXCLUDED_PHYSICAL_METRICS = (10, 10, 261_881)
EXPECTED_ASSEMBLY_METRICS = (12, 40)
EXPECTED_EXCLUDED_ASSEMBLY_METRICS = (1, 5)
EXPECTED_BOUNDARY_METRICS = (63, 0, 0)

HASH_BOUND_IMAGE_LINES = CANDIDATE_IMAGE_LINES
LIMITED_TRANSCRIBED_IMAGE_LINES: frozenset[int] = frozenset()
PIXEL_REPLAYED_IMAGE_LINES: frozenset[int] = frozenset()
assert all(asset.boundary == "HASH_BOUND" for asset in ASSETS.values())
assert all(asset.boundary == "HASH_BOUND" for asset in EXCLUDED_ASSETS.values())

SPLIT_OMISSION_IMAGE_LINES = frozenset({1711, 1744})
SPLIT_REFERENCED_IMAGE_LINES = GOVERNED_IMAGE_LINES - SPLIT_OMISSION_IMAGE_LINES
assert len(SPLIT_REFERENCED_IMAGE_LINES) == 51

ASSEMBLIES = {
    "cross-page-substitution-four": frozenset({998, 1008, 1014, 1449}),
    "p161-162-crossing-cf-pair": frozenset({1846, 1854}),
    "p560-561-representation-pair": frozenset({6768, 6776}),
    "p916-918-representation-three": frozenset({12524, 12552, 12557}),
    "p928-concatenation-walk-trilogy": frozenset({12992, 12996, 13000}),
    "p929-continued-fraction-residual-six": frozenset({
        13040, 13042, 13044, 13046, 13048, 13050,
    }),
    "p930-euclid-continued-fraction-pair": frozenset({13094, 13098}),
    "p931-digital-slope-five": frozenset({
        13119, 13121, 13123, 13125, 13127,
    }),
    "p986-billiard-cf-five": frozenset({
        14925, 14927, 14929, 14931, 14933,
    }),
    "p1085-number-representation-pair": frozenset({17167, 17171}),
    "p1109-prefix-method-pair": frozenset({17876, 17878}),
    "p1201-minimal-ca-four": frozenset({20588, 20594, 20596, 20598}),
}
EXCLUDED_ASSEMBLIES = {
    "X-p150-sequence-property-five": frozenset({
        1649, 1651, 1653, 1655, 1657,
    }),
}
assert sum(map(len, ASSEMBLIES.values())) == 40
assert sum(map(len, EXCLUDED_ASSEMBLIES.values())) == 5
assert all(
    frozenset(line for line, asset in ASSETS.items() if asset.assembly == name)
    == lines
    for name, lines in ASSEMBLIES.items()
)
assert all(
    frozenset(
        line for line, asset in EXCLUDED_ASSETS.items()
        if asset.assembly == name
    ) == lines
    for name, lines in EXCLUDED_ASSEMBLIES.items()
)


SOURCE_GUARDS = frozenset({
    "1679|first 20,000 digits|curve drawn goes up every time a digit is 1",
    "1707|Digit sequences for various rational numbers|period of at most q-1 steps",
    "1709|successive steps|base 2 digit sequence|rational numbers p/q",
    "1713|column on the right|box on the left|remainder",
    "1715|standard long division|compares the values of 2r and q|If 2r is less than q|2r - q",
    "1733|\\sqrt{2} = 1.01101010000010011110011001100110111111",
    "1738|procedure for generating the base 2 digit sequence|square root",
    "1740|two numbers r and s|4(r-s-1)|2(s+2)",
    "1746|starts by setting r=n and s=0|r>s|digits of s in base 2",
    "12515|Gray code ordering|successive numbers are arranged to differ in only one digit",
    "12522|BitXor[i, Floor[i/2]]|rule 60 cellular automaton",
    "12550|Negative bases|base -2|alternating black and white blocks",
    "12555|Multiplicative digit sequences|products of powers of primes|far more than *Log[m]* digits",
    "12943|Computing  $n^{th}$  digits directly|without explicitly finding previous ones",
    "12951|finite-precision arithmetic|probability exists|incorrect results",
    "12962|Page 139|base 2 digit sequences|m/n",
    "12982|maintain the relation|keeping *r* as small as possible|rational number",
    "12990|concatenating digits of successive integers|IntegerDigits",
    "13030|Page 143|ContinuedFraction",
    "13032|Floor[NestList[1/Mod[#, 1] &, x, n-1]]",
    "13074|continued fractions|concatenation sequences|patterns of peaks",
    "13086|The pictures below show|FromContinuedFraction[ContinuedFraction[x, n]]",
    "13092|Euclid's algorithm|ContinuedFraction[a/b]",
    "13111|Digital slope representation|Floor[nh] - Floor[(n-1)h]",
    "13130|Operator representations|trees of operations|single constant",
    "17130|Page 560|Number representations|sequence of 1's and 0's",
    "17165|representations (b) through (e)|numbers 1 through 500|grow roughly linearly",
    "17169|Completeness|representations (c), (d) and (e)|valid representation",
})

ROLE_RECORDS = frozenset(
    f"{line}|{asset.role}|{asset.assembly}|{asset.reason}"
    for line, asset in ASSETS.items()
)

ASSEMBLY_RECORDS = frozenset(
    f"{name}|{','.join(map(str, sorted(lines)))}"
    for name, lines in ASSEMBLIES.items()
)

REFERENCE_RECORDS = frozenset({
    "monolith|29|one-reference-per-file",
    "split|27|one-reference-per-linked-file",
    "total-source-references|56",
    "split-omissions|1711,1744|physical-files-still-required",
    "physical-files|29|unique-names-and-paths",
    "unique-hashes|29",
    "total-bytes|636440",
    "boundary|29-HASH_BOUND|0-LIMITED_TRANSCRIBED|0-PIXEL_REPLAYED",
    "roles|N=11|R=17|C=1",
})

TEXTUAL_MECHANICS_RECORDS = frozenset({
    "long-division|base=2|digit=floor(2r/q)|next=2r-digit*q",
    "long-division-invariant|0<=r<q|2r=digit*q+next|digit-in-{0,1}",
    "sqrt-strict|seed=(n,0)|n-integer|branch=r>s",
    "sqrt-true|next=(4*(r-s-1),2*(s+2))",
    "sqrt-false|next=(4*r,2*s)",
    "sqrt-prefix|a=s/4|a_next=2*a+indicator(r>s)",
    "sqrt-invariant-zero-based|s_t^2+4r_t=4^(t+1)*n",
    "sqrt-bound-zero-based|s_t<=2^(t+1)*sqrt(n)<s_t+4",
    "sqrt-rational-source-defect|n=11/5|literal-second-r=-4/5",
    "sqrt-rational-repair|compare-r>=s+1|not-attributed-to-literal-rule",
    "pixel-boundary|all-mechanics-source-text-and-independent-arithmetic",
})

EXPECTED_MANIFEST_DIGESTS = {
    "source_guards": "b1a57a86341eeb7226da8bc2d7507022be1f7e82eb32069132e2b4fc4119fda3",
    "roles": "846fc786f8998d93eb417b60c8cd27f7e4d0ddd478f03ebd458d70cb24550d9c",
    "assemblies": "4c1672f121651214ac4cfd973f9661661f737ebc0fa2901ee90fee5c529fd239",
    "references": "522cb95db5cfe278b32af6611afce83a57990618c3afcadb28fdcb54312cdfad",
    "textual_mechanics": "92fa66e92084ad11a2f364ac70237f616f5ba326595ddb1a85efa541448f0f59",
}


TEXTUAL_REPLAY_INTERFACE = {
    "evidence": "source-text-and-independent-exact-arithmetic-not-pixels",
    "long_division": {
        "base": 2,
        "formula": "digit=floor(2*r/q); next=2*r-digit*q",
        "profiles": [
            {"p": 1, "q": 3, "digits": "01" * 24},
            {"p": 1, "q": 7, "digits": "001" * 16},
        ],
    },
    "sqrt_strict_integer": {
        "formula": (
            "if r>s: (4*(r-s-1),2*(s+2)); else: (4*r,2*s)"
        ),
        "events": 48,
        "profiles": [
            {
                "n": 2,
                "bits": "101101010000010011110011001100111111100111011110",
            },
            {
                "n": 3,
                "bits": "110111011011001111010111010000101100001001100101",
            },
        ],
        "source_extracted_sqrt2": (
            "101101010000010011110011001100110111111"
        ),
        "source_extracted_first_mismatch_zero_based": 32,
    },
    "sqrt_rational_extension_guard": {
        "n": "11/5",
        "literal_states": ["11/5,0", "24/5,4", "-4/5,12"],
        "repair": "use r>=s+1 for the claimed arbitrary-rational extension",
    },
    "split_link_omissions": [1711, 1744],
}

EXPECTED_TEXTUAL_REPLAY_JSON_SHA256 = (
    "6fd8578623171650e57a405f2d3e9740b895724609fceb38132ceb202055c1fa"
)
EXPECTED_TEXTUAL_REPLAY_METRICS = (8_255, 96, 3)

# The structural set digest uses the same length-framed record convention as
# the recent source/asset interfaces.  The auxiliary ordered digest instead
# binds the literal `sha256sum`-style path-ordered manifest requested for T40.
EXPECTED_IMAGE_ASSET_MANIFEST = (
    29,
    "1fc4c0e9d7829254d34493c43aa76ce5e91ff989dc545a764b265d4e6f405808",
)
EXPECTED_ORDERED_SHA256SUM_MANIFEST = (
    29,
    "b06ceb5e71f0e92a4d9ca33f110913669666e95beb6085f8a8164f5f5732f772",
)


def verify_semantic_manifests() -> None:
    manifests = {
        "source_guards": SOURCE_GUARDS,
        "roles": ROLE_RECORDS,
        "assemblies": ASSEMBLY_RECORDS,
        "references": REFERENCE_RECORDS,
        "textual_mechanics": TEXTUAL_MECHANICS_RECORDS,
    }
    for name, records in manifests.items():
        assert records and len(records) == len(set(records))
        actual = digest_records(records)
        expected = EXPECTED_MANIFEST_DIGESTS[name]
        assert actual == expected, (name, actual, expected)

    payload = json.dumps(
        TEXTUAL_REPLAY_INTERFACE, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    actual_json_digest = sha256(payload)
    assert actual_json_digest == EXPECTED_TEXTUAL_REPLAY_JSON_SHA256, (
        actual_json_digest, EXPECTED_TEXTUAL_REPLAY_JSON_SHA256,
    )


def verify_source_guards() -> None:
    for record in SOURCE_GUARDS:
        fields = record.split("|")
        line = int(fields[0])
        text = BOOK_LINES[line - 1]
        for needle in fields[1:]:
            assert needle in text, (line, needle)


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Read JPEG dimensions from a SOF marker without an image dependency."""

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
        segment_size = int.from_bytes(data[offset:offset + 2], "big")
        assert segment_size >= 2
        if marker in sof:
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            return width, height
        offset += segment_size
    raise AssertionError("JPEG SOF marker not found")


def verify_asset_bytes(book_line: int, asset: AssetSpec, data: bytes) -> str:
    assert len(data) == asset.byte_length, (book_line, len(data), asset.byte_length)
    assert jpeg_size(data) == (asset.width, asset.height), book_line
    digest = sha256(data)
    assert digest == asset.digest, (book_line, digest, asset.digest)
    return digest


def verify_source_interface() -> None:
    """Bind the independently frozen source audit's image interface."""

    assert SOURCE_ORACLE_PATH.is_file(), "T40 source oracle is not frozen"
    source = runpy.run_path(
        str(SOURCE_ORACLE_PATH), run_name="t40_source_for_asset_interface"
    )
    expected_sets = {
        "NATIVE_IMAGE_LINES": NATIVE_IMAGE_LINES,
        "RELATION_IMAGE_LINES": RELATION_IMAGE_LINES,
        "CONTROL_IMAGE_LINES": CONTROL_IMAGE_LINES,
        "GOVERNED_IMAGE_LINES": GOVERNED_IMAGE_LINES,
        "EXCLUDED_IMAGE_LINES": EXCLUDED_IMAGE_LINES,
        "CANDIDATE_IMAGE_LINES": CANDIDATE_IMAGE_LINES,
        "UNRESOLVED_IMAGE_LINES": UNRESOLVED_IMAGE_LINES,
    }
    for name, expected in expected_sets.items():
        actual = frozenset(source[name])
        assert actual == expected, (name, sorted(actual), sorted(expected))

    expected_partition = {
        "native": (len(NATIVE_IMAGE_LINES), digest_lines(NATIVE_IMAGE_LINES)),
        "relation": (
            len(RELATION_IMAGE_LINES), digest_lines(RELATION_IMAGE_LINES)
        ),
        "control": (len(CONTROL_IMAGE_LINES), digest_lines(CONTROL_IMAGE_LINES)),
    }
    assert source["EXPECTED_IMAGE_ROLE_PARTITION"] == expected_partition

    expected_ledger = {
        "candidate_images": (
            len(CANDIDATE_IMAGE_LINES), digest_lines(CANDIDATE_IMAGE_LINES)
        ),
        "governed_images": (
            len(GOVERNED_IMAGE_LINES), digest_lines(GOVERNED_IMAGE_LINES)
        ),
        "excluded_images": (
            len(EXCLUDED_IMAGE_LINES), digest_lines(EXCLUDED_IMAGE_LINES)
        ),
    }
    assert source["EXPECTED_IMAGE_LEDGER"] == expected_ledger
    assert tuple(source["EXPECTED_IMAGE_ASSET_MANIFEST"]) == (
        EXPECTED_IMAGE_ASSET_MANIFEST
    )


def long_division_step(r: int, q: int) -> tuple[int, int]:
    """Replay the source's strict base-two long-division event."""

    assert type(r) is int and type(q) is int
    assert q > 0 and 0 <= r < q
    doubled = 2 * r
    if doubled < q:
        digit, successor = 0, doubled
    else:
        digit, successor = 1, doubled - q
    assert digit in {0, 1}
    assert 0 <= successor < q
    assert doubled == digit * q + successor
    return digit, successor


def long_division_digits(p: int, q: int, count: int) -> str:
    assert type(count) is int and count >= 0
    assert type(p) is int and type(q) is int and 0 <= p < q
    remainder = p
    digits: list[str] = []
    for _ in range(count):
        digit, remainder = long_division_step(remainder, q)
        digits.append(str(digit))
    return "".join(digits)


def sqrt_integer_step(r: int, s: int) -> tuple[int, int, int]:
    """Replay one literal strict-integer square-root event from BOOK:1746."""

    assert type(r) is int and type(s) is int
    assert r >= 0 and s >= 0 and s % 4 == 0
    bit = int(r > s)
    if bit:
        next_r, next_s = 4 * (r - s - 1), 2 * (s + 2)
    else:
        next_r, next_s = 4 * r, 2 * s
    assert next_r >= 0 and next_s >= 0 and next_s % 4 == 0
    assert next_s // 4 == 2 * (s // 4) + bit
    return bit, next_r, next_s


def sqrt_integer_bits(n: int, count: int) -> str:
    assert type(n) is int and 1 <= n < 4
    assert type(count) is int and count >= 0
    r, s = n, 0
    bits: list[str] = []
    for event in range(count):
        assert s * s + 4 * r == 4 ** (event + 1) * n
        assert s * s <= 4 ** (event + 1) * n < (s + 4) ** 2
        bit, r, s = sqrt_integer_step(r, s)
        bits.append(str(bit))
        prefix = s // 4
        assert prefix == math.isqrt(n * 4 ** event)
    return "".join(bits)


def verify_textual_replays() -> tuple[int, int, int]:
    """Replay source formulas independently; never inspect raster pixels."""

    long_division_checks = 0
    for q in range(2, 129):
        for remainder in range(q):
            long_division_step(remainder, q)
            long_division_checks += 1

    long_profiles = TEXTUAL_REPLAY_INTERFACE["long_division"]["profiles"]
    for profile in long_profiles:
        expected = profile["digits"]
        assert long_division_digits(
            profile["p"], profile["q"], len(expected)
        ) == expected

    # Bind the source's strict comparison at the only integer boundary where
    # `>` and `>=` differ, plus the immediately adjacent true branch.
    assert sqrt_integer_step(4, 4) == (0, 16, 8)
    assert sqrt_integer_step(5, 4) == (1, 0, 12)

    sqrt_profiles = TEXTUAL_REPLAY_INTERFACE["sqrt_strict_integer"]["profiles"]
    sqrt_events = TEXTUAL_REPLAY_INTERFACE["sqrt_strict_integer"]["events"]
    for profile in sqrt_profiles:
        assert sqrt_integer_bits(profile["n"], sqrt_events) == profile["bits"]

    source_bits = TEXTUAL_REPLAY_INTERFACE["sqrt_strict_integer"][
        "source_extracted_sqrt2"
    ]
    generated = sqrt_integer_bits(2, len(source_bits))
    mismatches = [
        index for index, pair in enumerate(zip(source_bits, generated))
        if pair[0] != pair[1]
    ]
    expected_first = TEXTUAL_REPLAY_INTERFACE["sqrt_strict_integer"][
        "source_extracted_first_mismatch_zero_based"
    ]
    assert mismatches and mismatches[0] == expected_first == 32
    assert source_bits[:expected_first] == generated[:expected_first]

    # BOOK:12982's arbitrary-rational extension is false under the literal
    # integer predicate r>s.  Preserve the exact counterexample rather than
    # silently attributing the repaired threshold to BOOK:1746.
    r0, s0 = Fraction(11, 5), Fraction(0)
    r1, s1 = 4 * (r0 - s0 - 1), 2 * (s0 + 2)
    assert (r1, s1) == (Fraction(24, 5), Fraction(4))
    assert r1 > s1
    r2, s2 = 4 * (r1 - s1 - 1), 2 * (s1 + 2)
    assert (r2, s2) == (Fraction(-4, 5), Fraction(12))
    corrected_r2, corrected_s2 = 4 * r1, 2 * s1
    assert not (r1 >= s1 + 1)
    assert (corrected_r2, corrected_s2) == (Fraction(96, 5), Fraction(8))

    return long_division_checks, len(sqrt_profiles) * sqrt_events, len(mismatches)


def split_and_physical_indices() -> tuple[
    dict[str, list[tuple[Path, int, str]]], dict[str, list[Path]]
]:
    split_markdown = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(split_markdown) == 17
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    split_by_name: dict[str, list[tuple[Path, int, str]]] = {}
    for markdown in split_markdown:
        for line_number, text in enumerate(
            markdown.read_text(encoding="utf-8").splitlines(), 1
        ):
            if match := split_re.fullmatch(text):
                split_by_name.setdefault(match.group(1), []).append(
                    (markdown, line_number, text)
                )

    physical_by_name: dict[str, list[Path]] = {}
    for path in SOURCE_ROOT.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)
    return split_by_name, physical_by_name


def ledger() -> tuple[str, tuple[int, int, int, int], str, str]:
    """Verify the closed universe and return ledger/manifest payloads."""

    scoped_main = {
        line for line in BOOK_IMAGES if 1665 < line < 1834
    }
    scoped_notes = {
        line for line in BOOK_IMAGES if 12921 < line < 13146
    }
    scoped_followed_relations = {12524, 12552, 12557, 17167, 17171}
    assert frozenset(
        scoped_main | scoped_notes | scoped_followed_relations
    ) == GOVERNED_IMAGE_LINES
    assert (
        len(scoped_main), len(scoped_notes), len(scoped_followed_relations)
    ) == (3, 21, 5)

    split_by_name, physical_by_name = split_and_physical_indices()
    rows: list[str] = []
    structural_records: set[str] = set()
    ordered_sha256sum_rows: list[str] = []
    hashes: set[str] = set()
    names: set[str] = set()
    physical_paths: set[Path] = set()
    total_bytes = 0
    monolith_references = 0
    split_references = 0

    for book_line, asset in sorted(ASSETS.items()):
        role = asset.role[0]
        assert role in {"N", "R", "C"} and asset.role[1] == "-"
        assert book_line in {
            "N": NATIVE_IMAGE_LINES,
            "R": RELATION_IMAGE_LINES,
            "C": CONTROL_IMAGE_LINES,
        }[role]

        assert BOOK_IMAGES[book_line] == asset.name
        assert [
            line for line, reference in BOOK_IMAGES.items()
            if Path(reference).name == asset.name
        ] == [book_line]
        monolith_references += 1

        split_hits = split_by_name.get(asset.name, [])
        if book_line in SPLIT_OMISSION_IMAGE_LINES:
            assert asset.split_markdown == "-" and asset.split_line == 0
            assert split_hits == [], (book_line, split_hits)
        else:
            expected_split = SOURCE_ROOT / asset.split_markdown
            assert split_hits == [(
                expected_split, asset.split_line,
                f"![](Images/{asset.name})",
            )], (book_line, split_hits)
            split_references += 1

        physical_path = SOURCE_ROOT / asset.physical
        assert physical_by_name.get(asset.name) == [physical_path]
        data = physical_path.read_bytes()
        digest = verify_asset_bytes(book_line, asset, data)
        assert asset.name not in names
        assert physical_path not in physical_paths
        assert digest not in hashes
        names.add(asset.name)
        physical_paths.add(physical_path)
        hashes.add(digest)
        total_bytes += len(data)

        rows.append("|".join((str(book_line),) + tuple(map(str, asset))))
        structural_records.add(
            f"{book_line}->{asset.physical}\0{asset.byte_length}\0{digest}"
        )
        root_relative = physical_path.relative_to(ROOT).as_posix()
        ordered_sha256sum_rows.append(f"{digest}  {root_relative}\n")

    assert len(names) == len(physical_paths) == len(hashes) == 29
    assert (monolith_references, split_references) == (29, 27)
    payload = "\n".join(rows) + "\n"
    ordered_payload = "".join(ordered_sha256sum_rows)
    return (
        payload,
        (monolith_references, split_references, len(hashes), total_bytes),
        digest_records(structural_records),
        sha256(ordered_payload.encode("utf-8")),
    )


EXPECTED_LEDGER_SHA256 = (
    "c5c030aa35a158fe7797fbee2060200dc9e3f89fdac4066c73c978711943780f"
)


def main() -> None:
    if len(sys.argv) != 1:
        raise SystemExit("usage: 45-T40-asset-oracle.py")

    verify_semantic_manifests()
    verify_source_guards()
    verify_source_interface()
    long_checks, sqrt_events, sqrt_source_mismatches = verify_textual_replays()
    payload, metrics, structural_digest, ordered_digest = ledger()
    ledger_digest = sha256(payload.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger", ledger_digest, EXPECTED_LEDGER_SHA256,
    )
    assert (29, structural_digest) == EXPECTED_IMAGE_ASSET_MANIFEST
    assert (29, ordered_digest) == EXPECTED_ORDERED_SHA256SUM_MANIFEST
    assert (
        metrics[0], metrics[1], metrics[0] + metrics[1]
    ) == EXPECTED_REFERENCE_METRICS
    assert (metrics[2], metrics[2], metrics[3]) == EXPECTED_PHYSICAL_METRICS
    assert (
        long_checks, sqrt_events, sqrt_source_mismatches
    ) == EXPECTED_TEXTUAL_REPLAY_METRICS
    assert (
        len(NATIVE_IMAGE_LINES), len(RELATION_IMAGE_LINES),
        len(CONTROL_IMAGE_LINES), len(GOVERNED_IMAGE_LINES),
        len(EXCLUDED_IMAGE_LINES),
    ) == EXPECTED_DISPOSITION_METRICS
    assert (len(ASSEMBLIES), sum(map(len, ASSEMBLIES.values()))) == (
        EXPECTED_ASSEMBLY_METRICS
    )
    assert (
        len(HASH_BOUND_IMAGE_LINES), len(LIMITED_TRANSCRIBED_IMAGE_LINES),
        len(PIXEL_REPLAYED_IMAGE_LINES),
    ) == EXPECTED_BOUNDARY_METRICS
    assert len(ROLE_RECORDS) == 29 and len(SOURCE_GUARDS) == 28

    print(
        "T40 asset oracle: PASS governed=29; classes N/R/C=11/17/1; "
        "candidates=29; excluded=0; refs=56(monolith=29,split=27); "
        "split_link_omissions=2(page154,page156); unique_hashes=29; "
        "physical_files=29; bytes=636440; assemblies=5/18_files; "
        "boundary=29_HASH_BOUND/0_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        f"textual_replay=long_division_{long_checks}_states/"
        f"sqrt_{sqrt_events}_events; "
        f"sqrt2_extracted_bit_defect=guarded_{sqrt_source_mismatches}_mismatches; "
        "rational_sqrt_extension_counterexample=11/5_guarded; "
        "ordered_manifest=b06ceb5e71f0e92a4d9ca33f110913669666e95beb6085f8a8164f5f5732f772; "
        "pixel_inference=0; unresolved_image_dispositions=0"
    )


if __name__ == "__main__":
    main()
