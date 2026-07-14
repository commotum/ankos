#!/usr/bin/env python3
"""Fail-closed raster/provenance audit for T35 piecewise integer maps.

T35 has one exact integer state and selects a closed arithmetic arm from the
old state by an explicit predicate.  Its native visual record consists of the
printed-page-122 parity example, the printed-page-123 seed gallery, the
printed-page-124 long seed-six run, and the two Notes plates for 3n+1-style
halting-time and reversible variants.

This audit also retains source-routed relations to the page-100 register
machine, continuous iterated maps, universal arithmetic encodings of register
machines, and Conway's fraction system.  T34 fixed arithmetic and T36 digit
reversal plates are explicit controls.  The preceding tag/Turing plate and
the first T37 recursive-sequence plate are provenance-bound exclusions rather
than silently ignored neighbors.

Every governed JPEG is bound to one physical file, one monolith reference,
one split-Markdown reference, exact bytes, dimensions, SHA-256, evidence
role, and assembly.  No pixel is used to invent a predicate, formula, residue
class, arm order, seed, trace value, palette, crop rule, halting result, or
encoding.  All governed assets are therefore HASH_BOUND, with no
LIMITED_TRANSCRIBED or PIXEL_REPLAYED asset.
"""

from __future__ import annotations

import hashlib
import re
import runpy
from pathlib import Path
from typing import NamedTuple


if not __debug__:
    raise RuntimeError("T35 asset verification requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/42-T35-source-oracle.py"

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


# Frozen manifest.  Each row is independently checked below against the
# monolith, every split Markdown file, and every physical JPEG.
ASSET_ROWS = r"""
1190|C-T19-NESTED-REGISTER|_page_114_Picture_5.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_114_Picture_5.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md|507|90854|597|810|6ee0109e4946151386ee806f1b52768d2be823063d697b683c7006f6ab962c63|register_behavior_pair|register-machine sibling before the exact page-100 arithmetic relation
1196|R-T19-PIECEWISE-REGISTER|_page_115_Figure_1.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_115_Figure_1.jpeg|CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md|513|236706|1182|990|937e1c6f6882a107f3d55a85f1c1131f4481170faf0b5b5a8c79c208417597c0|register_behavior_pair|page-100 compressed register values obey a stated T35-style map; raster does not define the map
1449|C-T34-ADD-ONE|_page_132_Figure_10.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_132_Figure_10.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|53|56915|169|1250|396c235b7d5d7881de7a4823778065c557644da9738a61b4052de918e5d2e8b5|-|fixed addition has no predicate-selected arm
1455|C-T34-ADD-CONSTANTS|_page_133_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_133_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|59|118982|887|697|c58ad8ce64d656841e1f7ab6f6692179b5d662da59a8285c401865fff3ff438c|-|fixed-addition gallery is a T34 control
1463|C-T34-MULTIPLY-TWO|_page_134_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_134_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|67|46524|448|453|c011a897557eaac9fba56c0c470c74763c3812c0f6bdcb253e1b4ad3a3969dba|t34_multiplication_pair|first fixed-multiplication control
1465|C-T34-MULTIPLY-THREE|_page_134_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_134_Figure_3.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|69|62569|645|420|eaacf39d1a4f8af165ae9ba01756514b205aec56a4729496c0d38adde9b5d109|t34_multiplication_pair|second fixed-multiplication control
1481|C-T34-POWERS-THREE|_page_135_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_135_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|85|384807|1187|1342|d76cde1ce58580d77777613fc8c4abf3fa05d114c0fedade7152bb660d4d7945|-|fixed multiply-by-three trace is a digit-view control
1487|C-T34-RATIONAL-MULTIPLY|_page_136_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_136_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|91|183701|1171|756|d4859c1d1e6f3efcfbe910e4bd6d734ebe4aea19b2189c079851d5dc12fa8e7e|-|fixed rational multiplication is the immediate T34 predecessor
1493|C-T34-FRACTIONAL-OBSERVER|_page_137_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_137_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|97|34574|1175|186|31f00bec35b2895c74fea00cb6026073d6075d5d33006f988994edc95c5389c6|-|printed-page-122 fractional observer immediately precedes T35
1505|N-T35-PARITY-MAP|_page_137_Picture_7.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_137_Picture_7.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|109|94903|445|735|959a39064c320d7b1b67d38394446622a11faba14b767526cdaa6c52b767c4e7|-|native printed-page-122 even/odd selected arithmetic example; raster trace untranscribed
1517|N-T35-SEED-GALLERY|_page_138_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_138_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|121|73976|904|398|abae36c2d750cbab48c5bea86d0afe80d5d16ffc4f7fc31d225406fcfcef2b60|t35_growth_pair|native printed-page-123 multi-seed behavior gallery
1523|N-T35-SEED-SIX-LONG-RUN|_page_139_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_139_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|127|50875|1065|561|994a1ab97bc3de5aee725d3a7ad222e9c970e8b8f7c454b89b46805159795f2c|t35_growth_pair|native printed-page-124 seed-six digit and logarithmic views
1543|C-T36-REVERSAL-SEED-16|_page_140_Picture_5.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_140_Picture_5.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|147|140714|607|922|4adb983dd8fa5ec5a8904cca51dec2d6fef50b3f28924784ee832e4f2d8b5d6c|t36_reversal_main|first T36 digit-reversal plate; digit representation is rule-visible
1547|C-T36-REVERSAL-SEED-512|_page_141_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_141_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|151|359405|950|1461|2523481bae71468864a41f08ae0e0dcc1a823bfd49c5efdcc788625b00cd0fba|t36_reversal_main|second T36 digit-reversal plate
1551|C-T36-REVERSAL-MILLIONTH|_page_142_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_142_Picture_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|155|516673|962|1476|d304e0089d5be1c9662e1645812b78f2d900f009e7805978a142b4f1b741700e|t36_reversal_main|third T36 continuation plate; crop is not numeric state
1884|R-T43-ITERATED-MAPS-A|_page_165_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_165_Figure_1.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|343|283207|1196|1147|4581f6e83f6de80cecf11d98d79239e00248ff77e015f27ed641ca5c848f88bf|iterated_map_pair|continuous self-map comparison explicitly routed back to page 122
1888|R-T43-ITERATED-MAPS-B|_page_166_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_166_Figure_2.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|347|64825|1199|203|93dabe2074ed063e0f601509d30bbb1c7f79223ba29c9f997b361f84c10f0ddc|iterated_map_pair|paired continuous-map plate; distinct carrier and closure invariants
8088|C-T19-REGISTER-EMULATES-TM|_page_687_Figure_1.jpeg|CHAPTERS/11-The-Notion-of-Computation/Images/_page_687_Figure_1.jpeg|CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md|381|231175|970|1344|c68f2e12fbff35606cfa79279f4def45585431c7a8c5c9ed899a3bc354b445b9|-|register-machine universality context before arithmetic lowering
8098|R-T35-UNIVERSAL-ARITHMETIC-TRACE|_page_688_Figure_4.jpeg|CHAPTERS/11-The-Notion-of-Computation/Images/_page_688_Figure_4.jpeg|CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md|391|115324|773|743|68fade069ee73569e798de272d65f52b585002fef79a286e89d68f058206ec68|universal_arithmetic_pair|residue-selected arithmetic system emulating a register machine
8100|R-T35-UNIVERSAL-ARITHMETIC-RULE|_page_688_Picture_5.jpeg|CHAPTERS/11-The-Notion-of-Computation/Images/_page_688_Picture_5.jpeg|CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md|393|4133|177|110|666d4850858d260b59bbcf972761c5dc08dcd1abeb4575adb8cd8dae816476f3|universal_arithmetic_pair|rule companion; raster formulas are not transcribed
12548|C-T34-DIGIT-COUNT|_page_917_Figure_9.jpeg|BACK-MATTER/Index/Images/_page_917_Figure_9.jpeg|BACK-MATTER/Index/Index.md|451|13761|583|109|5bee4ad516f029c69379729146666151c5215f790386350c104e6e35d9a691ad|-|T34 observer control in the shared Elementary Arithmetic Notes
12552|C-T34-NEGATIVE-BASE|_page_917_Picture_11.jpeg|BACK-MATTER/Index/Images/_page_917_Picture_11.jpeg|BACK-MATTER/Index/Index.md|455|9004|572|48|9d98da9314261068e9616f51b2f2ade3aca8497bc346e576de4c3efeccf7d214|-|T34 representation control; base does not choose a T35 arm
12557|C-T34-MULTIPLICATIVE-DIGITS|_page_918_Figure_2.jpeg|BACK-MATTER/Index/Images/_page_918_Figure_2.jpeg|BACK-MATTER/Index/Index.md|460|12033|585|75|537e2542e9042a89760407db9f1526688b62a081faa2a43487023d1c9de14ba7|-|T34 factorization-view control
12561|C-T34-POWER-DIGIT-FREQUENCY|_page_918_Figure_4.jpeg|BACK-MATTER/Index/Images/_page_918_Figure_4.jpeg|BACK-MATTER/Index/Index.md|464|14303|547|159|1e3c487aad78076111c6dedaa943af6e3b1bc2858bd2c3b45e3adccbd90682e9|-|T34 powers-of-three observer control
12583|C-T34-IRRATIONAL-MULTIPLES|_page_918_Figure_16.jpeg|BACK-MATTER/Index/Images/_page_918_Figure_16.jpeg|BACK-MATTER/Index/Index.md|486|29780|565|165|063be8f26ae1d13f7c97292b30d845cc67552027aef4964c99f4e44d9254fae6|-|last T34 Notes plate before T35 implementation
12611|N-T35-THREE-N-PLUS-ONE|_page_919_Figure_10.jpeg|BACK-MATTER/Index/Images/_page_919_Figure_10.jpeg|BACK-MATTER/Index/Index.md|514|37752|546|413|54a3e611eebc4f35590c6265304589ea84fe3e8e04bb935379bf530df6760e4c|-|native Notes comparison of halting times for three residue-selected maps
12633|N-T35-REVERSIBLE-VARIANT|_page_920_Figure_8.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_8.jpeg|BACK-MATTER/Index/Index.md|536|8897|593|100|99b72bc69f8a8badf8665097268dc8e021fbb53f8ae9c94de7eaeb4071179e71|-|native Notes forward/backward length view for a stated reversible map
12641|C-T36-REGULAR-REGION-LENGTHS|_page_920_Figure_12.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_12.jpeg|BACK-MATTER/Index/Index.md|544|13166|559|107|806545c68cad4830840650728e14b07bbab6a6de84eca6c95e83e1422f0d768a|-|first T36 Notes plate after the T35 reversible variant
12654|C-T36-DIGIT-REVERSAL-A|_page_920_Picture_20.jpeg|BACK-MATTER/Index/Images/_page_920_Picture_20.jpeg|BACK-MATTER/Index/Index.md|557|6689|184|155|2029134c9db04ce2aff0d1659a3c8a349080c727e32232e8d678111a62de4de9|t36_digit_reversal_notes|digit-reversal sequence control A
12656|C-T36-DIGIT-REVERSAL-B|_page_920_Picture_21.jpeg|BACK-MATTER/Index/Images/_page_920_Picture_21.jpeg|BACK-MATTER/Index/Index.md|559|13053|181|153|f13f46847832eb97ca2665867c4dda09101f8f7f7448348961d702fe7fe14305|t36_digit_reversal_notes|digit-reversal sequence control B
12658|C-T36-DIGIT-REVERSAL-C|_page_920_Picture_22.jpeg|BACK-MATTER/Index/Images/_page_920_Picture_22.jpeg|BACK-MATTER/Index/Index.md|561|12353|184|153|5d85f1c33422576a95048a3e57e4ed1d97fb5466cd174916921fbb0b153164b1|t36_digit_reversal_notes|digit-reversal sequence control C
12674|C-T36-DIGIT-COUNT-SEQUENCE|_page_920_Figure_30.jpeg|BACK-MATTER/Index/Images/_page_920_Figure_30.jpeg|BACK-MATTER/Index/Index.md|577|10024|575|98|8e8c22a2c52e54c3d5ab4ae00b12f84e862a1264a532e2f35266b29b5a6d3ba0|-|representation-visible sequence tangent; not T35 state
12678|C-T36-BITWISE-A|_page_921_Picture_3.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_3.jpeg|BACK-MATTER/Index/Index.md|581|2657|96|83|985e5d74ae6c0bbf6f3beb1554345c0af51c848889f0305de416ef093bd70481|t36_bitwise_notes|bitwise/arithmetic digit-sequence control A
12680|C-T36-BITWISE-B|_page_921_Picture_4.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_4.jpeg|BACK-MATTER/Index/Index.md|583|2980|81|83|d9da05f6d43e78e6cb16a0ea451d8204e2f4320aaccdfe6ef2b9b157daa6749e|t36_bitwise_notes|bitwise/arithmetic digit-sequence control B
12682|C-T36-BITWISE-C|_page_921_Picture_5.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_5.jpeg|BACK-MATTER/Index/Index.md|585|3791|133|93|5e308a461a3d1852a69750c906d5a46a0b94e264696fff6209ca414e43c58068|t36_bitwise_notes|bitwise/arithmetic digit-sequence control C
12684|C-T36-BITWISE-D|_page_921_Picture_6.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_6.jpeg|BACK-MATTER/Index/Index.md|587|3249|114|89|b0eca5ac7ce927db9edb42807573b5a63ee9c9420a733782609612234cc565eb|t36_bitwise_notes|bitwise/arithmetic digit-sequence control D
12686|C-T36-BITWISE-E|_page_921_Picture_7.jpeg|BACK-MATTER/Index/Images/_page_921_Picture_7.jpeg|BACK-MATTER/Index/Index.md|589|2324|92|93|5ed00f75d880eb9a2d3aa47132e1d560a5f2997f7f7292d309b7146532adca15|t36_bitwise_notes|bitwise/arithmetic digit-sequence control E
18662|R-CONWAY-FRACTION-SYSTEM|_page_1130_Figure_11.jpeg|BACK-MATTER/Colophon/Images/_page_1130_Figure_11.jpeg|BACK-MATTER/Colophon/Colophon.md|1219|11011|557|123|68930b0c9134e18b02d6a41f1eb23fe258918d551a109da169ff5d8da5ec1335|-|Conway fraction-system relation; ordered applicable fractions are prose/code evidence
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

NATIVE_IMAGE_LINES = frozenset({1505, 1517, 1523, 12611, 12633})
RELATION_IMAGE_LINES = frozenset({1196, 1884, 1888, 8098, 8100, 18662})
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
) == (5, 6, 27, 38)


ASSEMBLIES = {
    assembly: frozenset(
        line for line, asset in ASSETS.items() if asset.assembly == assembly
    )
    for assembly in {asset.assembly for asset in ASSETS.values()} - {"-"}
}
assert ASSEMBLIES == {
    "register_behavior_pair": frozenset({1190, 1196}),
    "t34_multiplication_pair": frozenset({1463, 1465}),
    "t35_growth_pair": frozenset({1517, 1523}),
    "t36_reversal_main": frozenset({1543, 1547, 1551}),
    "iterated_map_pair": frozenset({1884, 1888}),
    "universal_arithmetic_pair": frozenset({8098, 8100}),
    "t36_digit_reversal_notes": frozenset({12654, 12656, 12658}),
    "t36_bitwise_notes": frozenset({12678, 12680, 12682, 12684, 12686}),
}
assert sum(map(len, ASSEMBLIES.values())) == 21


# Exact source-routed adjacency exclusions.  They are physically verified
# below but do not contribute to governed evidence counts or byte totals.
ADJACENCY_EXCLUSIONS = {
    1565: ("_page_143_Figure_6.jpeg", "first T37 recursive-sequence plate"),
    8084: ("_page_686_Picture_3.jpeg", "preceding tag/Turing emulation plate"),
}
EXCLUDED_IMAGE_LINES = frozenset(ADJACENCY_EXCLUSIONS)
assert GOVERNED_IMAGE_LINES.isdisjoint(EXCLUDED_IMAGE_LINES)
for excluded_line, (excluded_name, _reason) in ADJACENCY_EXCLUSIONS.items():
    assert BOOK_LINES[excluded_line - 1] == f"![]({excluded_name})"

EXCLUDED_ASSET_ROWS = r"""
1565|X-T37-RECURSIVE-BOUNDARY|_page_143_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Images/_page_143_Figure_6.jpeg|CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md|169|86025|1231|382|731de2a621d5b227026c1b1ac4ed488ce96afc26be0fd5fcb0495297f5ed650b|-|first recursive-sequence plate after the T36 section
8084|X-TAG-TURING-EMULATION|_page_686_Picture_3.jpeg|CHAPTERS/11-The-Notion-of-Computation/Images/_page_686_Picture_3.jpeg|CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md|377|109620|833|699|702dbbb8c4c58e9ff4b146f85ed93a05b1d642f288316682902071b3c1c2f227|-|preceding tag/Turing relation before register and arithmetic emulation
""".strip()
EXCLUDED_ASSETS = parse_assets(EXCLUDED_ASSET_ROWS)
assert frozenset(EXCLUDED_ASSETS) == EXCLUDED_IMAGE_LINES
for line, asset in EXCLUDED_ASSETS.items():
    assert asset.name == ADJACENCY_EXCLUSIONS[line][0]


SOURCE_DERIVED_CANDIDATE_GROUPS = {
    "register_machine_relation": frozenset({1190, 1196}),
    "T34_main_controls_and_T35_main": frozenset(
        {1449, 1455, 1463, 1465, 1481, 1487, 1493, 1505, 1517, 1523}
    ),
    "T36_main_controls_and_T37_boundary": frozenset(
        {1543, 1547, 1551, 1565}
    ),
    "iterated_map_relation": frozenset({1884, 1888}),
    "universal_arithmetic_relation": frozenset({8084, 8088, 8098, 8100}),
    "T34_notes_controls": frozenset(
        {12548, 12552, 12557, 12561, 12583}
    ),
    "T35_notes_and_T36_controls": frozenset(
        {12611, 12633, 12641, 12654, 12656, 12658, 12674,
         12678, 12680, 12682, 12684, 12686}
    ),
    "Conway_fraction_relation": frozenset({18662}),
}
CANDIDATE_IMAGE_LINES = frozenset().union(*SOURCE_DERIVED_CANDIDATE_GROUPS.values())
assert sum(map(len, SOURCE_DERIVED_CANDIDATE_GROUPS.values())) == len(
    CANDIDATE_IMAGE_LINES
)
assert all(line in BOOK_IMAGES for line in CANDIDATE_IMAGE_LINES)
UNRESOLVED_IMAGE_LINES: frozenset[int] = frozenset()
assert CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
assert len(CANDIDATE_IMAGE_LINES) == 40


CLASSIFICATION = {
    **{line: "N" for line in NATIVE_IMAGE_LINES},
    **{line: "R" for line in RELATION_IMAGE_LINES},
    **{line: "C" for line in CONTROL_IMAGE_LINES},
    **{line: "X" for line in EXCLUDED_IMAGE_LINES},
}
assert frozenset(CLASSIFICATION) == CANDIDATE_IMAGE_LINES
assert tuple(CLASSIFICATION.values()).count("N") == 5
assert tuple(CLASSIFICATION.values()).count("R") == 6
assert tuple(CLASSIFICATION.values()).count("C") == 27
assert tuple(CLASSIFICATION.values()).count("X") == 2


HASH_BOUND = GOVERNED_IMAGE_LINES
LIMITED_TRANSCRIBED: frozenset[int] = frozenset()
PIXEL_REPLAYED: frozenset[int] = frozenset()
assert LIMITED_TRANSCRIBED <= HASH_BOUND
assert PIXEL_REPLAYED <= LIMITED_TRANSCRIBED
assert (len(HASH_BOUND), len(LIMITED_TRANSCRIBED), len(PIXEL_REPLAYED)) == (
    38, 0, 0,
)


UNRECOVERED_RASTER_SEMANTICS = frozenset(
    {
        "predicate definitions, residue moduli, branch priority, and fallthrough policy",
        "complete native integer traces and exact seed-gallery row identities",
        "formula constants, division exactness, signed-domain policy, and invalid arms",
        "binary and decimal palette maps, alignment, padding, crop, and width rules",
        "halting-time values, cycle proofs, reversibility proofs, and growth claims",
        "register/arithmetic encoders, decoder states, scheduling, and stutter steps",
        "Conway fraction order, selected fractions, prime filter, and generated values",
        "any callback, hidden interpreter, family dispatch, or executor inferred from pixels",
    }
)
assert len(UNRECOVERED_RASTER_SEMANTICS) == 8


SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED = frozenset(
    {
        "page-122 and page-123 formulas stated in captions and prose",
        "the source-printed first sequence values and million-step digit count",
        "3n+1, reversible-map, and cellular-automaton formulas in Notes text",
        "register-machine correspondence and residue-selected arithmetic encoding",
        "Conway fraction list and prime-producing claim in executable text/prose",
    }
)
assert len(SOURCE_DERIVED_NOT_PIXEL_TRANSCRIBED) == 5


SOURCE_GUARDS = {
    1198: "next value is 3n/2 if n is even",
    1495: "fractional parts of successive powers of 3/2",
    1499: "if the number at a particular step is even",
    1503: "If[EvenQ[n], 3\\,n/2, 3\\,(n+1)/2]",
    1513: "if the number obtained at a particular step is even",
    1519: "If[EvenQ[n], 5 n/2, (n+1)/2]",
    1525: "starting from the value 6",
    1545: "write its base 2 digits in reverse order",
    1886: "compare page 122",
    8086: "generalization of the arithmetic systems discussed on page 122",
    8102: "simple arithmetic system can emulate a register machine",
    12598: "NestList[If[EvenQ[#], 3#/2, 3(# + 1)/2] &, 1, t]",
    12599: "so-called 3n+1 problem",
    12625: "A reversible system",
    12635: "Reversal-addition systems",
    18632: "system from page 122 becomes for example",
    18648: "Additional work was done by John Conway",
    18660: "gives exactly the primes",
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

    assert SOURCE_ORACLE_PATH.is_file(), "T35 source oracle is not frozen"
    return runpy.run_path(
        str(SOURCE_ORACLE_PATH), run_name="t35_source_oracle_asset_interface"
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

    expected_partition = {
        "native": (len(NATIVE_IMAGE_LINES), digest_lines(NATIVE_IMAGE_LINES)),
        "relation": (len(RELATION_IMAGE_LINES), digest_lines(RELATION_IMAGE_LINES)),
        "control": (len(CONTROL_IMAGE_LINES), digest_lines(CONTROL_IMAGE_LINES)),
    }
    assert source["EXPECTED_IMAGE_PARTITION"] == expected_partition
    expected_set = source["EXPECTED_SET"]
    assert expected_set["candidate_images"] == (
        len(CANDIDATE_IMAGE_LINES), digest_lines(CANDIDATE_IMAGE_LINES),
    )
    assert expected_set["governed_images"] == (
        len(GOVERNED_IMAGE_LINES), digest_lines(GOVERNED_IMAGE_LINES),
    )
    assert expected_set["excluded_images"] == (
        len(EXCLUDED_IMAGE_LINES), digest_lines(EXCLUDED_IMAGE_LINES),
    )


def ledger() -> tuple[str, str, int, int, int, int, int, int, int, int]:
    """Verify governed and excluded assets; return canonical ledgers."""

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
        assert asset.role.startswith(f"{kind}-")
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

    excluded_rows: list[str] = []
    excluded_hashes: set[str] = set()
    excluded_bytes = 0
    excluded_monolith_references = 0
    excluded_split_references = 0
    for book_line, asset in sorted(EXCLUDED_ASSETS.items()):
        assert CLASSIFICATION[book_line] == "X"
        assert asset.role.startswith("X-")
        assert BOOK_LINES[book_line - 1] == f"![]({asset.name})"
        assert monolith_by_name.get(asset.name) == [book_line]

        expected_split = SOURCE_ROOT / asset.split_markdown
        split_hits = split_by_name.get(asset.name, [])
        assert split_hits == [(expected_split, asset.split_line)]
        expected_physical = SOURCE_ROOT / asset.physical
        physical_hits = physical_by_name.get(asset.name, [])
        assert physical_hits == [expected_physical]

        data = expected_physical.read_bytes()
        digest = sha256(data)
        assert len(data) == asset.byte_length
        assert jpeg_size(data) == (asset.width, asset.height)
        assert digest == asset.digest
        assert digest not in hashes and digest not in excluded_hashes
        excluded_hashes.add(digest)
        excluded_bytes += len(data)
        excluded_monolith_references += 1
        excluded_split_references += 1
        excluded_rows.append(
            "|".join(
                (
                    str(book_line), "X", asset.role, asset.physical,
                    str(asset.byte_length), str(asset.width), str(asset.height),
                    asset.digest, asset.split_markdown, str(asset.split_line),
                    asset.assembly, asset.boundary,
                )
            )
        )

    excluded_payload = "\n".join(excluded_rows) + "\n"
    return (
        payload, excluded_payload,
        monolith_references, split_references, len(hashes), total_bytes,
        excluded_monolith_references, excluded_split_references,
        len(excluded_hashes), excluded_bytes,
    )


EXPECTED_LEDGER_SHA256 = "TO_BE_FROZEN"
EXPECTED_EXCLUDED_LEDGER_SHA256 = "TO_BE_FROZEN"


def main() -> None:
    verify_source_interface()
    (
        payload, excluded_payload,
        monolith_refs, split_refs, hashes, total_bytes,
        excluded_monolith_refs, excluded_split_refs,
        excluded_hashes, excluded_bytes,
    ) = ledger()
    ledger_digest = sha256(payload.encode("utf-8"))
    excluded_ledger_digest = sha256(excluded_payload.encode("utf-8"))
    assert ledger_digest == EXPECTED_LEDGER_SHA256, (
        "ledger", ledger_digest, EXPECTED_LEDGER_SHA256,
    )
    assert excluded_ledger_digest == EXPECTED_EXCLUDED_LEDGER_SHA256, (
        "excluded ledger", excluded_ledger_digest,
        EXPECTED_EXCLUDED_LEDGER_SHA256,
    )
    assert (monolith_refs, split_refs, hashes, total_bytes) == (
        38, 38, 38, 0,
    )
    assert (
        excluded_monolith_refs, excluded_split_refs,
        excluded_hashes, excluded_bytes,
    ) == (2, 2, 2, 195_645)
    print(
        "T35 asset oracle: PASS governed=38; classes N/R/C=5/6/27; "
        "candidates=40; excluded=2; refs=76(monolith=38,split=38); "
        "unique_hashes=38; bytes=TO_BE_FROZEN; assemblies=8/21_files; "
        "excluded_bound=2/4_refs/2_hashes/195645_bytes/0_assemblies; "
        "boundary=38_HASH_BOUND/0_LIMITED_TRANSCRIBED/0_PIXEL_REPLAYED; "
        "predicates/formulas/palettes/traces=unrecovered; "
        "unresolved_image_dispositions=0"
    )


if __name__ == "__main__":
    main()
