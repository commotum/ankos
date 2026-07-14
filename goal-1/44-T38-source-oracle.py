#!/usr/bin/env python3
"""Fail-closed primary-source audit for T38 variable-index recurrences.

T38 is a closed-RULE specialization of the shared SimplePrograms construction,
not a request for a family executor.  The native state is the complete
consecutive prefix; the reused NEIGHBORHOOD exposes that old snapshot, a closed
recurrence computes addresses into it, and a successful event appends one term.  Main-text plates are
opaque here: their pixels belong to the asset oracle, while this oracle freezes
their identities, roles, exclusions, and monolith/split provenance.

The Book does not use the catalog name.  Redundant query lanes therefore bind
the semantic boundary, Notes, relations, actual flattened Index, controls, and
false positives.  Every result is dispositioned and every governed record has
a unique split-corpus owner.  Known extraction/source defects are guarded
instead of silently repaired.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


if not __debug__:
    raise RuntimeError("T38 source oracle requires assertions; do not use -O")


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = SCRIPT_ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"


def line_set(spec: str) -> frozenset[int]:
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Exactly seventeen redundant lanes.  Q00 proves that the catalog label is
# external vocabulary.  Q12/Q13 close the complete 15-image interface.
QUERIES = {
    "Q00": r"Variable-Index Recursive Sequences?",
    "Q01": r"Recursive Sequences?|Recurrence Relations?",
    "Q02": (
        r"not (?:just )?a fixed distance|"
        r"f\[n\s*-\s*f\[n\s*-\s*1\]\]|"
        r"meaningless quantities|necessarily be a positive number"
    ),
    "Q03": (
        r"Computation of sequences|store all the values of f\[n\]|"
        r"recomputing them|memoization|memoized"
    ),
    "Q04": (
        r"recursive definitions yield meaningful|leftmost innermost|"
        r"Evaluation schemes"
    ),
    "Q05": (
        r"Properties of sequences|f\[p\[n\]\]|f\[q\[n\]\]|"
        r"evaluation tree|distinct nodes reached|depth of the evaluation tree"
    ),
    "Q06": r"f\[n\s*-\s*f\[n\s*-\s*[12]\]\]|f\[f\[n\s*-\s*1\]\]",
    "Q07": (
        r"Conway.{0,100}recursive sequences|"
        r"Hofstadter.{0,100}recursive sequences|"
        r"sequence \(c\).{0,120}Conway|"
        r"sequence \(e\).{0,120}Hofstadter"
    ),
    "Q08": (
        r"positive and negative fluctuations|"
        r"fluctuations.{0,160}base 2 digit|"
        r"number of 1.s.{0,120}base 2|"
        r"recursive sequences on page 130"
    ),
    "Q09": (
        r"IntegerExponent.{0,200}recursive sequence|2m\+1-DigitCount|"
        r"first\s+\$2\^m\$\s+elements in the sequence can also be generated|"
        r"largest n for which f\[n\] = m"
    ),
    "Q10": (
        r"Networks?.{0,80}recursive sequences|"
        r"Randomness.{0,80}recursive sequences|"
        r"Discontinuities.{0,100}recursive sequences|"
        r"Forts.{0,80}recursive sequences|in recursive evaluation"
    ),
    "Q11": (
        r"Integer sequences, 123, 128.?131|"
        r"Recurrence relations, 128.?131|"
        r"Recursive sequences, 128.?131|"
        r"Leftmost innermost evaluation, 906"
    ),
    "Q12": r"_page_(?:144_Figure_3|145_Figure_1|920_Figure_30|922_Figure_2)\.jpeg",
    "Q13": (
        r"_page_(?:143_Figure_6|147_Figure_4|921_Picture_[3-7]|"
        r"923_Figure_(?:10|12|17|21))\.jpeg|The Sequence of Primes"
    ),
    "Q14": (
        r"f\[(?:0|-1|-2|k)\]|meaningful sequences|"
        r"details of how the rules are applied"
    ),
    "Q15": (
        r"recursive sequences.{0,120}sounds|"
        r"sounds.{0,120}recursive sequences|page 130 yield sounds"
    ),
    "Q16": (
        r"Integer sequences|Nested sequences|Recursion relations|"
        r"Douglas Hofstadter|John Conway"
    ),
}


# Full governed evidence includes structural continuations not directly found
# by a query.  These semantic partitions are deliberately independent of the
# image governed/excluded partition below.
NATIVE_EVIDENCE = line_set(
    "1569,1571,1573,1575,1599,1601,1603,1605,1607,1609,1611,1613,1615,1617,"
    "12720,12722,12724,12726,12761,12763"
)
RELATION_EVIDENCE = line_set(
    "11570,12668,12670,12672,12674,"
    "12728,12730,12731,12734,12736,12738,12740,12742,12744,12746,12747,"
    "12748,12751,12753,12754,12755,12756,12759,12765,12767,"
    "12822,12824,12826,12828,12830,12832,12834,12836,12838,14021,17518"
)
CONTROL_EVIDENCE = line_set(
    "1555,1559,1561,1563,1565,1567,"
    "1619,1623,1625,1627,1629,1633,1637,1641,"
    "12138,12167,12187,12190,12192,"
    "12688,12690,12692,12694,12696,12698,12700,12702,12704,12706,12708,"
    "12710,12712,12714,12716,12718,"
    "12840,12842,12844,12846,15049,15051,15053,17533,17585"
)
RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE

QUERY_NATIVE = line_set(
    "1569,1571,1573,1575,1599,1601,1607,1611,1613,"
    "12720,12722,12726,12761,12763"
)
QUERY_RELATION = line_set(
    "11570,12674,12728,12742,12751,12759,12765,12767,"
    "12822,12826,12836,14021,17518"
)
QUERY_CONTROL = line_set(
    "1555,1565,1567,1619,1625,1629,1633,1637,1641,"
    "12138,12167,12187,12190,12192,12688,12690,12692,12698,12700,"
    "12844,12846,15051,17533,17585"
)

EXCLUDED_CLASS = {
    "unrelated_name_and_history": line_set(
        "144,7022,7024,7028,7032,7040,7124,10475,11507,11565,13666,"
        "14128,14147,14243,14542,17321,17519,17599,17806,18648,18749"
    ),
    "unrelated_recursive_or_observer": line_set(
        "2476,2484,12609,12664,13827,16325"
    ),
    "bitwise_neighbor_assets": line_set("12678,12680,12682,12684,12686"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


INDEX_CLASS = {
    "native": line_set("21114,21162,21450"),
    "relation": line_set(
        "21050,21074,21090,21193,21253,21329,21683,21899,22352"
    ),
    "control": line_set("21172,21185,21275,21360,21915,21923"),
}
INDEX_EXCLUDED_CLASS = {"nested_sequence_collision": line_set("21677")}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())
INDEX_EXCLUDED = frozenset().union(*INDEX_EXCLUDED_CLASS.values())

INDEX_ENTRY_GUARDS = {
    21050: ("and recursive sequences, 907",),
    21074: ("Delete and Boolean minimization, 1095", "and recursive sequence, 906"),
    21090: ("Discontinuities", "and recursive sequences, 131, 906"),
    21114: ("Dynamic programming", "and recursive sequences, 906"),
    21162: ("Evaluation schemes", "and recursive sequences, 906"),
    21172: ("as recursive sequence, 906",),
    21185: ("FFT (fast Fourier transform)", "as recursive sequence, 128"),
    21193: ("Forts, nested architecture", "in recursive evaluation, 906"),
    21253: ("Hofstadter, Douglas R.", "and recursive sequences, 880, 907"),
    21275: ("and recursive sequences, 907 in reduced arithmetic",),
    21329: ("Integer sequences, 123, 128–131", "and a recursive sequence, 906"),
    21360: ("and recurrence relations, 906",),
    21450: ("Leftmost innermost evaluation, 906",),
    21683: ("Network systems", "in recursive sequences, 130"),
    21899: ("in primitive recursive functions", "in recursive sequences, 130"),
    21915: ("Recurrence relations, 128–131",),
    21923: ("Recursive sequences, 128–131", "sounds from, 1080"),
    22352: ("in recursive evaluation, 907",),
}
INDEX_EXCLUDED_GUARDS = {
    21677: ("Nested sequences", "pointer-based encoding of, 1071"),
}
INDEX_FLATTENING_SENTINELS = {
    21050: ("Corollaries",),
    21193: ("Fisher-Tippett distribution",),
    21275: ("and history of 2D CAs",),
    21329: ("Instantons, in path integrals",),
    22352: ("Toffoli, Tommaso",),
}


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("1573,1599,12763")
RELATION_IMAGE_LINES = line_set("12674")
CONTROL_IMAGE_LINES = frozenset()
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)
EXCLUDED_IMAGE_LINES = line_set(
    "1565,1625,12678,12680,12682,12684,12686,12822,12826,12836,12844"
)
CANDIDATE_IMAGE_LINES = GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
UNRESOLVED_IMAGE_LINES = frozenset()

# Exported for the asset oracle.  "Excluded" means excluded from T38 raster
# semantics, not necessarily excluded from textual relation/control evidence.
IMAGE_ROLE_RECORDS = (
    "1573:native:main:page144 strict formula seed and finite term plate",
    "1599:native:main:page145 c-h fluctuation observer plate",
    "12674:relation:notes:page920 digit-count comparison only",
    "12763:native:notes:page922 p-q address plots for the displayed recurrences",
)
IMAGE_EXCLUSION_REASONS = {
    1565: "T37 fixed-distance recurrence plate at the immediate left boundary",
    1625: "T39 prime-sieve plate at the immediate right boundary",
    12678: "iterated-bitwise Notes sibling, picture 3",
    12680: "iterated-bitwise Notes sibling, picture 4",
    12682: "iterated-bitwise Notes sibling, picture 5",
    12684: "iterated-bitwise Notes sibling, picture 6",
    12686: "iterated-bitwise Notes sibling, picture 7",
    12822: "general primitive-recursive-function relation, not a T38 native plate",
    12826: "general primitive-recursive-function relation, not a T38 native plate",
    12836: "general primitive-recursive-function relation, not a T38 native plate",
    12844: "Ulam-sequence T39 control, not a T38 native plate",
}
IMAGE_ASSEMBLY_BOUNDARIES = (
    "main:1573:page144 contains eight formula-seed-term rows; lower e-h small plots are cropped",
    "main:1599:page145 contains c-h fluctuation plots; plotted observations do not feed RULE",
    "notes:12674:page920 is a digit-count relation assembled outside Recursive Sequences Notes",
    "notes:12763:page922 belongs to the p-q sentence at BOOK12761 and evaluation-tree prose at BOOK12765",
    "path:monolith image references omit Images/ while split references include it",
)


# Semantic guards bind exact claims without treating raster pixels as text.
SOURCE_SEMANTIC_GUARDS = (
    (
        "strict_dynamic_access",
        1569,
        ("not just a fixed distance back", "f[n - f[n - 1]]"),
        (),
    ),
    (
        "strict_invalid_boundary",
        1571,
        ("necessarily be a positive number", "f[0], f[-1] and f[-2]"),
        (),
    ),
    (
        "strict_plate_scope",
        1575,
        ("Most such rules", "particular rules shown here all avoid this problem"),
        (),
    ),
    (
        "strict_observer",
        1601,
        ("cases (c) and (d)", "base 2 digit sequence", "f[1] = f[2] = 1"),
        (),
    ),
    (
        "strict_qualification",
        1607,
        ("seem instead in many respects random", "even after a million steps"),
        (),
    ),
    (
        "strict_digit_relation",
        1613,
        ("number of 1's", "all numbers less than n"),
        (),
    ),
    (
        "strict_conclusion",
        1617,
        ("only addition and subtraction", "behavior of great complexity"),
        (),
    ),
    (
        "notes_storage",
        12720,
        ("store all the values of f[n]", "rather than recomputing them"),
        (),
    ),
    (
        "notes_case_e",
        12722,
        ("f[n-f[n-1]] + f[n-f[n-2]]",),
        (),
    ),
    ("notes_case_e_seed", 12724, ("f[1] = f[2] = 1",), ()),
    (
        "notes_evaluation_profile",
        12726,
        ("leftmost innermost scheme", "f[-1]-f[-1]", "SMP system"),
        (),
    ),
    (
        "notes_dependency_form",
        12761,
        ("f[p[n]] + f[q[n]]", "p[n] and q[n]"),
        (),
    ),
    (
        "notes_evaluation_tree",
        12765,
        ("yielding a tree", "{{12}, {3, 7}, {1, 2, 4}, {1, 2}, {1}}"),
        (),
    ),
    (
        "notes_history",
        12767,
        ("John Conway around 1988", "Douglas Hofstadter in 1979"),
        (),
    ),
    (
        "case_d_source_defect",
        12738,
        ("Flatten[Table[n, {IntegerExponent[n, 2] + 1}], {n, m}]]",),
        ("Flatten[Join[{1}",),
    ),
    (
        "case_d_corroboration",
        12742,
        ("2m+1-DigitCount", "h[1] = 2"),
        (),
    ),
    (
        "primitive_recursive_relation",
        12830,
        ("if they never sample values below *f*[0]", "all primitive recursive"),
        (),
    ),
    (
        "primitive_recursive_domain",
        12832,
        ("must be given integers that are non-negative",),
        (),
    ),
    ("left_boundary", 1567, ("simple recursive sequences", "Fibonacci sequence"), ()),
    ("right_boundary", 1619, ("The Sequence of Primes",), ()),
    ("notes_left_boundary", 12688, ("Recursive Sequences",), ()),
    ("notes_right_boundary", 12846, ("The Sequence of Primes",), ()),
    (
        "history_relation",
        11570,
        ("Douglas Hofstadter studies a recursive sequence",),
        (),
    ),
    (
        "multiway_relation",
        14021,
        ("recursive sequences are discussed on page 907",),
        (),
    ),
    (
        "sound_relation",
        17518,
        ("recursive sequences on page 130 yield sounds",),
        (),
    ),
)

# Stable normalized interface for consumers such as the asset oracle.  The
# digest is SHA-256 over the lexicographically sorted records joined by LF.
SOURCE_SEMANTIC_GUARD_RECORDS = frozenset(
    f"{kind}:{line_no}:{'|'.join(positive)}!{'|'.join(negative)}"
    for kind, line_no, positive, negative in SOURCE_SEMANTIC_GUARDS
)
EXPECTED_SOURCE_SEMANTIC_GUARDS = (
    25,
    "e3fe7d2455039acbf875899046d67d96b0cd862724532b58407fabc5a071fa53",
)

AUXILIARY_SEMANTIC_GUARDS = (
    ("catalog", 39, ("Variable-Index Recursive Sequences,",), ()),
    ("taxonomy", 1050, ("## 38. Variable-Index Recursive Sequences",), ()),
    ("taxonomy", 1054, ("Same growing sequence structure",), ()),
    ("taxonomy", 1062, ("zero, negative, or beyond the generated prefix",), ()),
    ("taxonomy", 1069, ("invalid_index_policy",), ()),
)

SOURCE_DEFECT_RECORDS = (
    "BOOK12738:case-d multiplicity list omits the extra initial one",
    "BOOK12742:h-one-equals-two independently contradicts the omitted-leading-seed list",
    "page144:asset ends midway through lower e-h small-plot row; no missing axes or samples may be inferred",
    "image-paths:monolith omits Images directory while split corpus includes it",
    "split-routing:nominal BACK-MATTER/Index file contains Notes material",
    "split-routing:actual flattened Index rows are stored in BACK-MATTER/Colophon",
    "BOOK12726:all-standard-languages evaluation statement is a Book profile not a universal external fact",
)
SOURCE_DEFECT_GUARD_RECORDS = frozenset(SOURCE_DEFECT_RECORDS)
EXPECTED_SOURCE_DEFECT_GUARDS = (
    7,
    "277d5e921297670115036eee89ebb073678fedc0574593e7a12148b6f18ea5e6",
)

SOURCE_MODEL_RECORDS = (
    "category:deterministic discrete singleton-successor simple program",
    "domain:discrete t+1D growing consecutive indexed support",
    "state:complete exact integer prefix rather than newest scalar or hidden memo cache",
    "seed:origin-one finite consecutive values",
    "frontier:reuse T37 unique endpoint selector",
    "neighborhood:reuse complete explicit old-prefix context",
    "access-validity:one through n-minus-one in the immutable old prefix",
    "access-order:source profile is leftmost innermost and retains demanded occurrences",
    "rule:closed integer expression evaluates dependent TermAt reads and emits the endpoint write",
    "write:one exact term at the unique endpoint",
    "update:reuse T37-to-T16 atomic single-splice append",
    "failure:demanded absent address gives common zero-successor no-commit error",
    "failure:not wrap clamp padding Python negative indexing or invented default",
    "memoization:direct implementation of visible complete-prefix state",
    "observer:digit formula fluctuations p-q plots evaluation trees and sounds do not feed back",
    "relation:primitive-recursive classification does not replace append-event provenance",
    "architecture:no T38 state class update law executor runner branch or family dispatch",
    "architecture:closed dependent TermAt syntax is the only class-two axis delta established by source",
    "source-epistemic:catalog taxonomy supplies vocabulary but not primary mechanics",
    "source-epistemic:raster-only formula seed and row claims belong to asset verification",
    "source-epistemic:meaningless reference does not itself name a halt or policy menu",
    "domain-vocabulary:DOMAIN means t plus dimensional support not CA lattice family",
)

SPLIT_BOUNDARY_WITNESSES = (
    "pre-debris:BOOK1575->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:179",
    "post-debris:BOOK1599->CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md:181",
    "notes-owner:BOOK12720->BACK-MATTER/Index/Index.md:623",
    "defect-duplicated:BOOK12738->BACK-MATTER/Index/Index.md:641",
    "actual-index-owner:BOOK21114->BACK-MATTER/Colophon/Colophon.md:3671",
)


EXPECTED_QUERY = {
    "Q00": (0, 0, 0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "Q01": (33, 17, 16, "a1f0c6eba942a5173875a5dba58dd4a75f2989d3567aeb9a2bca233ef632fccd"),
    "Q02": (4, 4, 0, "10fc01c721ef2458b1491592a656be9ede96e0e002324883104e2313edde7f30"),
    "Q03": (1, 1, 0, "1173b00bed000d7a9dbc26078fc3c8c11f80343dd9b4726d356d1fc0d72715e6"),
    "Q04": (3, 1, 2, "be3dcdd95b95a7aa36e2104529fa3c1fb4c01cfd33fe8ea7384f48da8d760be1"),
    "Q05": (6, 6, 0, "96f0a3242181fa207eb8c71eaa2a5f0e156d3e8dcbf2b0bf6ad846abd7dd15d9"),
    "Q06": (2, 2, 0, "881b5e0c7fa02e0675fe60a36b837029b74b5755be3803d5928e14a707352e43"),
    "Q07": (2, 1, 1, "0bcb93fe40cb4af225cb13cb5346c4383db5fca5f4169fbd76cdf7a062c2cd11"),
    "Q08": (8, 8, 0, "b91175a8e599617978c5b9649b0edc438bfd2b34f203994e135e176ea97708e1"),
    "Q09": (3, 2, 1, "712292994e41aaee2f30f731f1dd7e5ec0a96fcabce815d1fdc201cf6aa91292"),
    "Q10": (3, 0, 3, "eb421cef97c4d4855d968500a3377c255ce304e482ad6adde3ef22e962929bd4"),
    "Q11": (4, 0, 4, "54ca5f46bc143f2423c5554d303380539111d19d3bbeaf20e8c02ac43a67b713"),
    "Q12": (4, 4, 0, "b144e6374dc135b619f728e1d40b131814bf043865836bf3a92a92c78275c99a"),
    "Q13": (18, 18, 0, "8897c011c5846a5d9c38dace5496e985372e7c6437cfcbd8bd17c029cc4753d7"),
    "Q14": (8, 8, 0, "39098edd0532067c6740ea311330d9e9b3de31014640d7a610e68258238819d7"),
    "Q15": (2, 1, 1, "91adfd6158754d59e16fd9de6b2e772a0aecbdba7ab359ea7ce209a8d85cde66"),
    "Q16": (28, 23, 5, "fcba3bb9cd40477d197647c0a8949facb9ac9004e1f0c20fd62d5db1f73251cf"),
}
EXPECTED_QUERY_PATTERNS = (
    17,
    "50c1a7d9b3609fb6cb415a7cee44e8f49c9b30085de0249e552a347d54d90be1",
)
EXPECTED_SET = {
    "union": (102, "887ad4b5850c24ec79a5c2fdeeb4c032298e4f25365d102e10647f2ee7a6c459"),
    "pre_index": (83, "739302076793b4613803db470b7e6a5a6468db9aba45e059a35245caf87d68f9"),
    "index_candidates": (19, "bb2f5d4505cc3fca15b6243af5f440b61ece7e864f329166e3f5ffc3368a8651"),
    "query_native": (14, "5fb058e7940e16031d7a2daa5f3d25aa1dd036853bbaf77dd2be35ea75693f83"),
    "query_relation": (13, "85c240df5ca4c834b27ecfa920f3aadd5b3119877d422eabfbc4407fc49a5d16"),
    "query_control": (24, "e80b0d935bac4d96961836a1032c37dd87005997c23e41aad748f520e6dfda07"),
    "excluded": (32, "f8523cf96ec29be4c1e754d5a7a23d81304417d06b9b97edc4f2d588f91ed9b6"),
    "native": (20, "e612b750f0aa4905f5c9c14c115b4a43a87dc9c9a4914658d18e55b51cc32a01"),
    "relation": (36, "4bd6fff54e8e5435f6925c459ddef8fff58f9bcd1610b0128ffabc9eec6eb961"),
    "control": (44, "ccc2dfec013fcd437b28ddc24d74fbb9303f29cb066d116e8bf43a1cacc0fdb1"),
    "retained": (100, "b7d58b713ec63471c837b0c47e25180101edc0072850cce987778183fb77f379"),
    "retained_query": (51, "bd8f15a2891534a931f220fc004993016ca572220b83eac01b113fa54a133660"),
    "continuations": (49, "8c0da8e8a2951ff05cd7f903f3d30943ef4e8db0dce8292d2256c8c0ff2e7443"),
}
EXPECTED_EXCLUDED_CLASS = {
    "unrelated_name_and_history": (21, "8663cd346c6affdb0bee867556d262d8b51ad4e3445a897f76e5303306716c8a"),
    "unrelated_recursive_or_observer": (6, "d344dda08a6dc15b24b6407e86ca1a69bd46e326e1da2d156cb12c3b6ad594d7"),
    "bitwise_neighbor_assets": (5, "7b9bcbe5785a8d90dad6e15d7ac3a1838d8d6ca9fde1ea0e688efc596ab1153f"),
}
EXPECTED_INDEX_CLASS = {
    "native": (3, "9abcdcff889a9eecc2dfe62b2a23655ccb78390a914dbb23d8a1c17066d18349"),
    "relation": (9, "0d956d905c1d2ab8ea62e38ccd362e975a13cb5c5e6638bb76707fd29ef057bb"),
    "control": (6, "3fa42cf9e766f85b2d7a341eb2408ac4f2aa1de47866fccea3b15876f69c0fb5"),
}
EXPECTED_INDEX_EXCLUDED_CLASS = {
    "nested_sequence_collision": (1, "cc5295912db23d5e6b9ecc12f1bb01f7fa5ed69ba82140db7e51a44034691195"),
}
EXPECTED_IMAGE_PARTITION = {
    "native": (3, "74b2a8fe45b8b92a70a8a5c1640229346056f4ab0b97880daf3f66e2d25095fc"),
    "relation": (1, "abc9f91be5b16b673b527fc797b4ce1504f81ea000d907d867c16655e2a507c7"),
    "control": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "governed": (4, "b144e6374dc135b619f728e1d40b131814bf043865836bf3a92a92c78275c99a"),
    "excluded": (11, "9c7e291e8073dfea27ce3bef2a34999731cac67869e60b3a3d88cabe05e8d4b8"),
    "candidate": (15, "8417713424e88f9c2f1a3a471abe2c7795cc0912d196969a85dcbf529c7b9a80"),
}
IMAGE_PARTITION = {
    "native": NATIVE_IMAGE_LINES,
    "relation": RELATION_IMAGE_LINES,
    "control": CONTROL_IMAGE_LINES,
}
IMAGE_LEDGER = {
    "candidate_images": CANDIDATE_IMAGE_LINES,
    "governed_images": GOVERNED_IMAGE_LINES,
    "excluded_images": EXCLUDED_IMAGE_LINES,
}
EXPECTED_IMAGE_ROLE_PARTITION = {
    name: EXPECTED_IMAGE_PARTITION[name] for name in IMAGE_PARTITION
}
EXPECTED_IMAGE_LEDGER = {
    "candidate_images": EXPECTED_IMAGE_PARTITION["candidate"],
    "governed_images": EXPECTED_IMAGE_PARTITION["governed"],
    "excluded_images": EXPECTED_IMAGE_PARTITION["excluded"],
}
EXPECTED_CANDIDATE_IMAGE_LINES = EXPECTED_IMAGE_PARTITION["candidate"]
EXPECTED_GOVERNED_IMAGE_LINES = EXPECTED_IMAGE_PARTITION["governed"]
EXPECTED_EXCLUDED_IMAGE_LINES = EXPECTED_IMAGE_PARTITION["excluded"]
EXPECTED_UNRESOLVED_IMAGE_LINES = (
    0,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
)
EXPECTED_IMAGE_ASSET_MANIFEST = (
    15,
    "1d0157b9499dd616b64252c33aa0421e5dfcdb8ac09c67b634bcfd6f7db6d77c",
)

# Record contracts are filled after their independently readable records above.
# They intentionally fail closed if any needle, rationale, or model assertion is
# weakened even when its line set happens not to change.
EXPECTED_RECORDS = {
    "excluded_line_hashes": (32, "6d9fdcdc0edc299f617237393bac0edbd9c253ec22453e41948ec279d8b7d565"),
    "index_guards": (18, "90362ad1c14bf2d16997130aa55ec7ba17189f9af547505b25547ede8dc33a45"),
    "index_excluded_guards": (1, "2ab26251570dd7b355ef2b789ace5332568deda06b22f8ab5cfbed3e43844d09"),
    "index_sentinels": (5, "d25296b081e2abf05e33d14a135b5a3a843eeaa8a38673a53b5d5e7c66703236"),
    "semantic_guards": EXPECTED_SOURCE_SEMANTIC_GUARDS,
    "auxiliary_guards": (5, "b85864acc356516285636c63040d648c2528e9c11bc0e6bd10a75f9694c1ffcd"),
    "source_defects": EXPECTED_SOURCE_DEFECT_GUARDS,
    "source_model": (22, "94bf8172b7ec622cabe52b0762f2715ac6803850c3ed1daee63f4769c88e031a"),
    "image_roles": (4, "694eda0f0bf637f6d27cf861b3c7b4212f68113a15ab45d138fcaaabb74a5fae"),
    "image_exclusion_reasons": (11, "cc68366a0b17271866ac99c1bdaf7ea4ba1411af697a04cdef3520bd08a84430"),
    "image_assembly_boundaries": (5, "2a2dc89f2d3403126b25fa68e03ce6e5deb59578e882cb313802ccaffd6ab43c"),
    "split_boundary_witnesses": (5, "98f9693f6c499a15107f033333746cc5c8023f01a31dd6320abb15c051326017"),
}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_CROSSWALK = (
    124,
    "bec1fd0ed1b9935ea39714de7f0dd911ae95807a5b0d93c27de1c13a4dd440b4",
)
EXPECTED_SPLIT_CLASSES = {
    "EXACT": (
        98,
        "4c161a1626f8f356fdff9ea64ebc286681c80f1a938cb446d1f4f2c6d1b93aad",
        "7a5f12d211b36d5dc3e75bf8800573cf34f56bbdacbad5004a42d0fed768b75a",
    ),
    "IMAGE_BASENAME": (
        15,
        "8417713424e88f9c2f1a3a471abe2c7795cc0912d196969a85dcbf529c7b9a80",
        "804cea0ed20fdeae737f470137a8a88239ec1b51889b4c74e551b1af72198d52",
    ),
    "NORMALIZED": (
        11,
        "6634781615b1c54c854248de722d639e103a5c2ed177cb697309180a1830d2cd",
        "f2343ed6232265f0b47507769ac040a7dac651b6cc8f8d9aaf0341479b398ad0",
    ),
}
EXPECTED_SPLIT_NORMALIZED_MINIMUM = 0.999817


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def digest_records(records: set[str] | list[str] | tuple[str, ...]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def compact_line(line: str) -> str:
    return normalized_line(line).replace(" ", "")


def crosswalk_evidence(monolith: str, split: str) -> tuple[str, float]:
    if monolith == split:
        return "EXACT", 1.0
    left = IMAGE_RE.fullmatch(monolith.strip())
    right = IMAGE_RE.fullmatch(split.strip())
    if left and right:
        same = Path(left.group(1)).name == Path(right.group(1)).name
        return "IMAGE_BASENAME", 1.0 if same else 0.0
    score = SequenceMatcher(
        None, compact_line(monolith), compact_line(split), autojunk=False
    ).ratio()
    return "NORMALIZED", score


def resolve_book(argument: str | None) -> tuple[Path, Path, Path]:
    """Return BOOK, source root, and repository root, including relocations."""

    if argument is not None:
        book = Path(argument).resolve()
    elif DEFAULT_BOOK.is_file():
        book = DEFAULT_BOOK.resolve()
    else:
        cwd_candidate = (
            Path.cwd() / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
        ).resolve()
        if not cwd_candidate.is_file():
            raise FileNotFoundError("cannot locate default A New Kind of Science source")
        book = cwd_candidate
    source_root = book.parent
    repo_root = book.parents[2]
    return book, source_root, repo_root


def split_owner_record(line_no: int) -> str:
    """Return the one frozen structural split owner for a governed Book row."""

    candidates: list[str] = []
    if 1439 <= line_no <= 1575:
        candidates.append(
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            f"Systems-Based-on-Numbers.md:{line_no - 1396}"
        )
    if 1599 <= line_no <= 1991:
        candidates.append(
            "CHAPTERS/4-Systems-Based-on-Numbers/"
            f"Systems-Based-on-Numbers.md:{line_no - 1418}"
        )
    if line_no == 11570:
        candidates.append(
            "CHAPTERS/12-The-Principle-of-Computational-Equivalence/"
            "The-Principle-of-Computational-Equivalence.md:2951"
        )
    early_notes = {12138: 50, 12167: 78, 12187: 98, 12190: 101, 12192: 103}
    if line_no in early_notes:
        candidates.append(f"BACK-MATTER/Index/Index.md:{early_notes[line_no]}")
    if 12503 <= line_no <= 12974:
        candidates.append(f"BACK-MATTER/Index/Index.md:{line_no - 12097}")
    if line_no in {14021, 15049, 15051, 15053}:
        candidates.append(f"BACK-MATTER/Index/Index.md:{line_no - 12099}")
    if line_no in {17518, 17533, 17585} or line_no >= INDEX_FIRST_LINE:
        candidates.append(f"BACK-MATTER/Colophon/Colophon.md:{line_no - 17443}")
    if len(candidates) != 1:
        raise ValueError(f"line {line_no} has {len(candidates)} split owners")
    return candidates[0]


def case_d_prefix(count: int) -> tuple[int, ...]:
    values = [1, 1]
    while len(values) < count:
        n = len(values) + 1
        a = n - values[n - 2]
        b = n - values[n - 3] - 1
        if not (1 <= a < n and 1 <= b < n):
            raise ValueError("case-d demanded an invalid old-prefix address")
        values.append(values[a - 1] + values[b - 1])
    return tuple(values[:count])


def case_e_prefix(count: int) -> tuple[int, ...]:
    values = [1, 1]
    while len(values) < count:
        n = len(values) + 1
        a = n - values[n - 2]
        b = n - values[n - 3]
        if not (1 <= a < n and 1 <= b < n):
            raise ValueError("case-e demanded an invalid old-prefix address")
        values.append(values[a - 1] + values[b - 1])
    return tuple(values[:count])


def occurrence_records(
    guards: dict[int, tuple[str, ...]], lines: list[str]
) -> tuple[set[str], bool]:
    records = {f"{line_no}:{'|'.join(needles)}" for line_no, needles in guards.items()}
    valid = all(
        needles
        and all(needles)
        and 1 <= line_no <= len(lines)
        and all(needle in lines[line_no - 1] for needle in needles)
        for line_no, needles in guards.items()
    )
    return records, valid


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        raise SystemExit("usage: 44-T38-source-oracle.py [BOOK]")
    book, source_root, repo_root = resolve_book(args[0] if args else None)
    atlas = source_root / "ANKoS-Atlas.md"
    catalog = repo_root / "ref/notes/CA-Types.csv"
    taxonomy = repo_root / "ref/notes/CA-Types.md"

    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda n: lines[n - 1]
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(atlas) == EXPECTED_ATLAS_SHA256
        and sha256(catalog) == EXPECTED_CATALOG_SHA256
        and sha256(taxonomy) == EXPECTED_TAXONOMY_SHA256
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    pattern_records = {f"{name}:{pattern}" for name, pattern in QUERIES.items()}
    pattern_actual = (len(pattern_records), digest_records(pattern_records))
    query_contract_ok = (
        set(QUERIES) == set(EXPECTED_QUERY)
        and all(QUERIES.values())
        and pattern_actual == EXPECTED_QUERY_PATTERNS
    )
    ok &= query_contract_ok
    print("query_contract", "OK" if query_contract_ok else "MISMATCH", *pattern_actual)
    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        found = {n for n, line in enumerate(lines, 1) if rx.search(line)}
        hits[name] = found
        actual = (
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index = {n for n in union if n < INDEX_FIRST_LINE}
    index_candidates = union - pre_index
    query_retained = set(QUERY_NATIVE | QUERY_RELATION | QUERY_CONTROL)
    sets = {
        "union": union,
        "pre_index": pre_index,
        "index_candidates": index_candidates,
        "query_native": set(QUERY_NATIVE),
        "query_relation": set(QUERY_RELATION),
        "query_control": set(QUERY_CONTROL),
        "excluded": set(EXCLUDED),
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
        "retained": set(RETAINED),
        "retained_query": query_retained,
        "continuations": set(RETAINED) - query_retained,
    }
    set_contract_ok = set(sets) == set(EXPECTED_SET)
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        set_contract_ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    query_partition = (QUERY_NATIVE, QUERY_RELATION, QUERY_CONTROL, EXCLUDED)
    classification_ok = (
        set().union(*query_partition) == pre_index
        and sum(map(len, query_partition)) == len(pre_index)
        and QUERY_NATIVE <= NATIVE_EVIDENCE
        and QUERY_RELATION <= RELATION_EVIDENCE
        and QUERY_CONTROL <= CONTROL_EVIDENCE
        and not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and not RETAINED & EXCLUDED
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        classification_ok &= good
        print("excluded_" + name, "OK" if good else "MISMATCH", *actual)
    classification_ok &= (
        set(EXCLUDED_CLASS) == set(EXPECTED_EXCLUDED_CLASS)
        and set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    ok &= set_contract_ok and classification_ok
    print(
        "unresolved_pre_index",
        "OK" if classification_ok else "MISMATCH",
        len(pre_index ^ set().union(*query_partition)),
    )

    excluded_hash_records = {
        f"{n}:{hashlib.sha256(at(n).encode('utf-8')).hexdigest()}" for n in EXCLUDED
    }
    record_actuals: dict[str, tuple[int, str]] = {
        "excluded_line_hashes": (
            len(excluded_hash_records),
            digest_records(excluded_hash_records),
        )
    }

    index_ok = (
        set(INDEX_CLASS) == set(EXPECTED_INDEX_CLASS)
        and set(INDEX_EXCLUDED_CLASS) == set(EXPECTED_INDEX_EXCLUDED_CLASS)
        and set().union(*INDEX_CLASS.values()) == set(INDEX_ROUTED)
        and sum(map(len, INDEX_CLASS.values())) == len(INDEX_ROUTED)
        and set().union(*INDEX_EXCLUDED_CLASS.values()) == set(INDEX_EXCLUDED)
        and sum(map(len, INDEX_EXCLUDED_CLASS.values())) == len(INDEX_EXCLUDED)
        and not INDEX_ROUTED & INDEX_EXCLUDED
        and index_candidates == set(INDEX_ROUTED | INDEX_EXCLUDED)
    )
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        print("index_" + name, "OK" if good else "MISMATCH", *actual)
    for name, values in INDEX_EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_EXCLUDED_CLASS.get(name)
        index_ok &= good
        print("index_excluded_" + name, "OK" if good else "MISMATCH", *actual)

    index_records, index_guards_ok = occurrence_records(INDEX_ENTRY_GUARDS, lines)
    excluded_index_records, excluded_index_guards_ok = occurrence_records(
        INDEX_EXCLUDED_GUARDS, lines
    )
    sentinel_records, sentinels_ok = occurrence_records(
        INDEX_FLATTENING_SENTINELS, lines
    )
    record_actuals.update(
        {
            "index_guards": (len(index_records), digest_records(index_records)),
            "index_excluded_guards": (
                len(excluded_index_records),
                digest_records(excluded_index_records),
            ),
            "index_sentinels": (
                len(sentinel_records),
                digest_records(sentinel_records),
            ),
        }
    )
    index_ok &= (
        set(INDEX_ENTRY_GUARDS) == set(INDEX_ROUTED)
        and set(INDEX_EXCLUDED_GUARDS) == set(INDEX_EXCLUDED)
        and set(INDEX_FLATTENING_SENTINELS) <= set(INDEX_ROUTED)
        and index_guards_ok
        and excluded_index_guards_ok
        and sentinels_ok
    )
    ok &= index_ok
    print("unresolved_index", "OK" if index_ok else "MISMATCH", len(index_candidates ^ set(INDEX_ROUTED | INDEX_EXCLUDED)))

    semantic_records = set(SOURCE_SEMANTIC_GUARD_RECORDS)
    semantic_ok = (
        len(semantic_records) == len(SOURCE_SEMANTIC_GUARDS)
        and (len(semantic_records), digest_records(semantic_records))
        == EXPECTED_SOURCE_SEMANTIC_GUARDS
        and all(
            kind
            and positive
            and all(positive)
            and all(needle in at(n) for needle in positive)
            and all(negative)
            and all(needle not in at(n) for needle in negative)
            for kind, n, positive, negative in SOURCE_SEMANTIC_GUARDS
        )
    )
    record_actuals["semantic_guards"] = (
        len(semantic_records),
        digest_records(semantic_records),
    )

    catalog_lines = catalog.read_text(encoding="utf-8").splitlines()
    taxonomy_lines = taxonomy.read_text(encoding="utf-8").splitlines()
    auxiliary = {"catalog": catalog_lines, "taxonomy": taxonomy_lines}
    auxiliary_records = {
        f"{source}:{n}:{'|'.join(positive)}!{'|'.join(negative)}"
        for source, n, positive, negative in AUXILIARY_SEMANTIC_GUARDS
    }
    auxiliary_ok = (
        len(auxiliary_records) == len(AUXILIARY_SEMANTIC_GUARDS)
        and all(
            source in auxiliary
            and positive
            and all(needle in auxiliary[source][n - 1] for needle in positive)
            and all(negative)
            and all(needle not in auxiliary[source][n - 1] for needle in negative)
            for source, n, positive, negative in AUXILIARY_SEMANTIC_GUARDS
        )
        and len(catalog_lines) == 46
        and len(set(catalog_lines[1:])) == 45
        and not hits["Q00"]
    )
    record_actuals["auxiliary_guards"] = (
        len(auxiliary_records),
        digest_records(auxiliary_records),
    )

    defect_actual = (
        len(SOURCE_DEFECT_GUARD_RECORDS),
        digest_records(SOURCE_DEFECT_GUARD_RECORDS),
    )
    model_actual = (len(SOURCE_MODEL_RECORDS), digest_records(SOURCE_MODEL_RECORDS))
    role_actual = (len(IMAGE_ROLE_RECORDS), digest_records(IMAGE_ROLE_RECORDS))
    exclusion_reason_records = {
        f"{n}:{reason}" for n, reason in IMAGE_EXCLUSION_REASONS.items()
    }
    assembly_actual = (
        len(IMAGE_ASSEMBLY_BOUNDARIES),
        digest_records(IMAGE_ASSEMBLY_BOUNDARIES),
    )
    boundary_actual = (
        len(SPLIT_BOUNDARY_WITNESSES),
        digest_records(SPLIT_BOUNDARY_WITNESSES),
    )
    record_actuals.update(
        {
            "source_defects": defect_actual,
            "source_model": model_actual,
            "image_roles": role_actual,
            "image_exclusion_reasons": (
                len(exclusion_reason_records),
                digest_records(exclusion_reason_records),
            ),
            "image_assembly_boundaries": assembly_actual,
            "split_boundary_witnesses": boundary_actual,
        }
    )
    record_contract_ok = set(record_actuals) == set(EXPECTED_RECORDS)
    for name, actual in record_actuals.items():
        good = actual == EXPECTED_RECORDS.get(name)
        record_contract_ok &= good
        print("record_" + name, "OK" if good else "MISMATCH", *actual)
    record_contract_ok &= (
        semantic_ok
        and auxiliary_ok
        and SOURCE_DEFECT_GUARD_RECORDS == frozenset(SOURCE_DEFECT_RECORDS)
        and len(SOURCE_DEFECT_RECORDS) == len(SOURCE_DEFECT_GUARD_RECORDS)
        and len(SOURCE_MODEL_RECORDS) == len(set(SOURCE_MODEL_RECORDS))
        and set(IMAGE_EXCLUSION_REASONS) == set(EXCLUDED_IMAGE_LINES)
    )
    ok &= record_contract_ok

    image_sets = {
        **IMAGE_PARTITION,
        "governed": GOVERNED_IMAGE_LINES,
        "excluded": EXCLUDED_IMAGE_LINES,
        "candidate": CANDIDATE_IMAGE_LINES,
    }
    images_ok = (
        set(image_sets) == set(EXPECTED_IMAGE_PARTITION)
        and {
            name: (len(values), digest(values))
            for name, values in IMAGE_PARTITION.items()
        }
        == EXPECTED_IMAGE_ROLE_PARTITION
        and {
            name: (len(values), digest(values)) for name, values in IMAGE_LEDGER.items()
        }
        == EXPECTED_IMAGE_LEDGER
        and NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
        == GOVERNED_IMAGE_LINES
        and sum(
            map(len, (NATIVE_IMAGE_LINES, RELATION_IMAGE_LINES, CONTROL_IMAGE_LINES))
        )
        == len(GOVERNED_IMAGE_LINES)
        and CANDIDATE_IMAGE_LINES == GOVERNED_IMAGE_LINES | EXCLUDED_IMAGE_LINES
        and not GOVERNED_IMAGE_LINES & EXCLUDED_IMAGE_LINES
        and (len(CANDIDATE_IMAGE_LINES), digest(CANDIDATE_IMAGE_LINES))
        == EXPECTED_CANDIDATE_IMAGE_LINES
        and (len(GOVERNED_IMAGE_LINES), digest(GOVERNED_IMAGE_LINES))
        == EXPECTED_GOVERNED_IMAGE_LINES
        and (len(EXCLUDED_IMAGE_LINES), digest(EXCLUDED_IMAGE_LINES))
        == EXPECTED_EXCLUDED_IMAGE_LINES
        and (len(UNRESOLVED_IMAGE_LINES), digest(UNRESOLVED_IMAGE_LINES))
        == EXPECTED_UNRESOLVED_IMAGE_LINES
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION.get(name)
        images_ok &= good
        print("images_" + name, "OK" if good else "MISMATCH", *actual)

    image_manifest: set[str] = set()
    image_paths_ok = True
    for n in CANDIDATE_IMAGE_LINES:
        match = IMAGE_RE.fullmatch(at(n))
        image_paths_ok &= match is not None
        if match is None:
            continue
        matches = list(source_root.rglob(Path(match.group(1)).name))
        image_paths_ok &= len(matches) == 1
        if len(matches) != 1:
            continue
        asset = matches[0]
        image_manifest.add(
            f"{n}->{asset.relative_to(source_root).as_posix()}\0"
            f"{asset.stat().st_size}\0{sha256(asset)}"
        )
    image_manifest_actual = (len(image_manifest), digest_records(image_manifest))
    images_ok &= (
        image_paths_ok
        and image_manifest_actual == EXPECTED_IMAGE_ASSET_MANIFEST
        and len(image_manifest) == len(CANDIDATE_IMAGE_LINES)
    )
    ok &= images_ok
    print("exact_4_governed_11_excluded_image_interface", "OK" if images_ok else "MISMATCH", *image_manifest_actual)

    split_paths = sorted(
        path
        for path in source_root.rglob("*.md")
        if path.resolve() not in {book.resolve(), atlas.resolve()}
    )
    relative_paths = [path.relative_to(source_root).as_posix() for path in split_paths]
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
    print("split_manifest", "OK" if split_manifest_ok else "MISMATCH", len(split_paths), digest_records(relative_paths), digest_records(manifest))

    split_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            split_text[f"{relative}:{n}"] = line

    crosswalk_lines = RETAINED | INDEX_ROUTED | INDEX_EXCLUDED | CANDIDATE_IMAGE_LINES
    crosswalk_records: set[str] = set()
    owners: set[str] = set()
    class_lines: dict[str, set[int]] = {name: set() for name in EXPECTED_SPLIT_CLASSES}
    class_records: dict[str, set[str]] = {name: set() for name in EXPECTED_SPLIT_CLASSES}
    normalized_scores: list[float] = []
    split_join_ok = True
    for n in sorted(crosswalk_lines):
        try:
            owner = split_owner_record(n)
        except ValueError:
            split_join_ok = False
            continue
        if owner in owners or owner not in split_text:
            split_join_ok = False
            continue
        owners.add(owner)
        mode, score = crosswalk_evidence(at(n), split_text[owner])
        if mode not in class_lines:
            split_join_ok = False
            continue
        if mode == "NORMALIZED":
            normalized_scores.append(score)
            split_join_ok &= score >= 0.99
        else:
            split_join_ok &= score == 1.0
        record = f"{n}->{owner}:{mode}:{score:.6f}"
        crosswalk_records.add(record)
        class_lines[mode].add(n)
        class_records[mode].add(record)
    crosswalk_actual = (len(crosswalk_records), digest_records(crosswalk_records))
    class_actual = {
        name: (
            len(class_lines[name]),
            digest(class_lines[name]),
            digest_records(class_records[name]),
        )
        for name in class_lines
    }
    normalized_minimum = min(normalized_scores, default=0.0)
    split_join_ok &= (
        crosswalk_actual == EXPECTED_SPLIT_CROSSWALK
        and class_actual == EXPECTED_SPLIT_CLASSES
        and round(normalized_minimum, 6) == EXPECTED_SPLIT_NORMALIZED_MINIMUM
        and len(crosswalk_records) == len(crosswalk_lines)
        and len(owners) == len(crosswalk_lines)
        and set().union(*class_lines.values()) == set(crosswalk_lines)
        and sum(map(len, class_lines.values())) == len(crosswalk_lines)
        and split_owner_record(1575).endswith(":179")
        and split_owner_record(1599).endswith(":181")
        and "Computation of sequences" in split_text[split_owner_record(12720)]
        and "Dynamic programming" in split_text[split_owner_record(21114)]
        and "Flatten[Table[n" in split_text[split_owner_record(12738)]
    )
    ok &= split_join_ok
    print("split_reverse_join", "OK" if split_join_ok else "MISMATCH", *crosswalk_actual, f"normalized_min={normalized_minimum:.6f}")
    for name, actual in class_actual.items():
        print("split_class_" + name, *actual)

    # Text-backed defect witness: case (d) really begins with two ones, while
    # the literal multiplicity list at BOOK12738 produces only one.  BOOK12742
    # gives the correct largest index h[1] = 2.  No raster claim is needed here.
    d_values = case_d_prefix(512)
    e_values = case_e_prefix(512)
    book_list_starts = tuple(
        value
        for value in range(1, 8)
        for _ in range((value & -value).bit_length())
    )
    defect_logic_ok = (
        d_values[:2] == (1, 1)
        and book_list_starts[:2] == (1, 2)
        and max(i + 1 for i, value in enumerate(d_values) if value == 1) == 2
        and all(value > 0 for value in d_values)
        and all(value > 0 for value in e_values)
    )
    ok &= defect_logic_ok
    print("case_d_omitted_leading_seed_defect", "OK" if defect_logic_ok else "MISMATCH")

    architecture_ok = (
        semantic_ok
        and auxiliary_ok
        and record_contract_ok
        and defect_logic_ok
        and source_ok
    )
    ok &= architecture_ok
    print("source_fit_closed_rule_over_T37_append_no_new_executor", "OK" if architecture_ok else "MISMATCH", *model_actual)

    unresolved_total = (
        len(pre_index ^ set().union(*query_partition))
        + len(index_candidates ^ set(INDEX_ROUTED | INDEX_EXCLUDED))
        + (len(crosswalk_lines) - len(crosswalk_records))
        + len(UNRESOLVED_IMAGE_LINES)
        + (len(CANDIDATE_IMAGE_LINES) - len(image_manifest))
    )
    unresolved_ok = unresolved_total == 0
    ok &= unresolved_ok
    print("unresolved_total", "OK" if unresolved_ok else "MISMATCH", unresolved_total)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
