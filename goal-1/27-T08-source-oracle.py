#!/usr/bin/env python3
"""Frozen T08 initial-condition source-search oracle."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = (
    "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
)

QUERIES = {
    "Q01": r"\binitial conditions?\b",
    "Q02": r"\binitial (?:state|configuration|pattern|arrangement|sequence|field|string|word|network|value|data|input|step|row|cell|distribution|density|setup)s?\b",
    "Q03": r"\b(?:single|one|just (?:a )?single) (?:black|white|gray|grey|colored|coloured) (?:cell|square|element|point)\b",
    "Q04": r"\b(?:start|starts|started|starting|begin|begins|began|beginning|evolv(?:e|es|ed|ing))\b.{0,50}\b(?:from|with)\b.{0,24}\b(?:single|one|random|finite|periodic|repetitive|repeating|uniform|all[- ](?:black|white)|blank)\b",
    "Q05": r"\b(?:random initial|randomly chosen initial|initial.{0,32}(?:chosen )?(?:completely )?at random|start(?:s|ed|ing)? from (?:completely )?random|starting with (?:completely )?random)\b",
    "Q06": r"\b(?:finite|localized).{0,32}(?:seed|initial|starting|configuration|pattern|arrangement|sequence|state|block)|(?:seed|initial|starting|configuration|pattern|arrangement|sequence|state|block).{0,32}(?:finite|localized)\b",
    "Q07": r"\b(?:periodic|repetitive|repeating|repeated|periodically).{0,40}(?:initial|starting|configuration|pattern|arrangement|sequence|state|background|block)|(?:initial|starting|configuration|pattern|arrangement|sequence|state|background|block).{0,40}(?:periodic|repetitive|repeating|repeated|periodically)\b",
    "Q08": r"\b(?:(?:all[- ]|only |uniformly |entirely )(?:black|white|gray|grey)(?: cells?| state| configuration| background)?|(?:uniform|homogeneous) (?:black|white|gray|grey|state|configuration|background))\b",
    "Q09": r"\b(?:(?:black|white|blank|gray|grey|uniform|homogeneous|periodic|repetitive|repeating|random|regular).{0,40}background|background.{0,40}(?:black|white|blank|gray|grey|uniform|homogeneous|periodic|repetitive|repeating|random|regular))\b",
    "Q10": r"\bseeds?(?:ed|ing)?\b",
    "Q11": r"\b(?:(?:nested|structured).{0,40}(?:initial|starting|configuration|pattern|arrangement|sequence|state|seed)|(?:initial|starting|configuration|pattern|arrangement|sequence|state|seed).{0,40}(?:nested|structured))\b",
    "Q12": r"\b(?:all|every|each|any|arbitrary|possible|particular|different|simple|complicated|complex|typical|appropriate) initial conditions?\b",
    "Q13": r"\b(?:start(?:s|ed|ing)?|begin|begins|began|beginning)\s+(?:with|from)\b",
    "Q14": r"(?:\bat the first step the cell\b.{0,96}\b(?:black|white|gray|grey)\b|\ball possible sequences?\b.{0,96}\bequal probability\b|\beach square\b.{0,96}\bfixed independent probability\b)",
    "Q15": r"\b(?:start(?:s|ed|ing)?|begin|begins|began|beginning)\s+(?:(?:out|off|for example)\s+(?:with|from|as|on|by)|(?:as|on|by))\b",
    "Q16": r"\binitially\b",
}

# Expected tuple: total, pre-Index, Index, digest of ascending comma-joined lines.
EXPECTED_QUERY = {
    "Q01": (621, 570, 51, "b5335f244f2f4b1a54e3cdbc78e2722a31b976fdd75e0c8d301607f445dbb7f0"),
    "Q02": (54, 51, 3, "b39402376bcf70cf35a571e2555e376f1d8c165ffb6ee7a840d44264a3ba959e"),
    "Q03": (79, 79, 0, "aec7454face48d4af09b25bdf99566795b6606599e6420859b97cf69d63ba130"),
    "Q04": (109, 109, 0, "d12dcbf1e4ba0144f7dc6114139be216f2381bd19ec1100f582ee57a9041f7c4"),
    "Q05": (112, 81, 31, "b6cb31aa8ae8a1da5e76fd9eab17f5f07762e704d4064e5c73ea01c626caf08b"),
    "Q06": (61, 48, 13, "69de1cec8f5db7ac8d6a62ea445d90544201e3c9a37a627d0f6f3b45502e6055"),
    "Q07": (173, 158, 15, "0780d8ee49d3d4a6ce822a40a6e11b3326c491e0f94557c1628f7fc8e0150d5d"),
    "Q08": (29, 29, 0, "30ee61b282b03513875021197c83230a98e2ec912d7142da25d38d22d8e1e1eb"),
    "Q09": (32, 31, 1, "a04d4bd9e48f60642e93f69fe6b011a71f2a1f3668b3a763262c391437c38bfa"),
    "Q10": (19, 10, 9, "f77c78fe578c9bf67fee76df14e6ec4868bf9c9e1eb418998ff2368d4c8ef381"),
    "Q11": (136, 125, 11, "411b2218329158e916c172e66498998fdd09d83ede8551e3dd92015402dd8bb4"),
    "Q12": (128, 125, 3, "2df6dae0b325464b02b1346a8119baa5edd214945e5390b7008b61a23eba4333"),
    "Q13": (299, 299, 0, "58c36d65307e84bd4dfcfc156dafc1f9a080f930abde6f1a0921e2f64afdc505"),
    "Q14": (4, 4, 0, "10c72b6f76a94859b526b13c77e0363c0f845a66fc2ff9347baa00452b5b76ce"),
    "Q15": (34, 34, 0, "aee298b77824e77f64ec98a1e80e60c5f28a1f40167e43cf9a0bd4e53f5780ab"),
    "Q16": (32, 32, 0, "24ca561ab7b401ca7202e1a9d13b2f95710b11de5d8eae97e0edd83a1a7a14d9"),
}

RETAINED_BASE = frozenset(map(int, """
432 440 450 460 472 476 478 500 518 550 566 592 622 730 742 746 754 790 846 960 970 978
1040 1154 1198 1238 1246 1302 1346 1348 1350 1886 1898 1906 1908 1920 1924 1926 1928 1930 1932 1936 1938 1940 1944 1946 1956 1982
2066 2180 2184 2194 2216 2226 2230 2250 2256 2262 2332 2460 2538
2706 2708 2710 2712 2714 2720 2722 2726 2728 2730 2734 2736 2750 2758 2760 2764 2772 2776 2790 2794 2822 2890 2908 2922 2926 2942 2944 2950 2954 2966 2968 2970 2978
3046 3050 3054 3056 3058 3060 3066 3068 3070 3072 3076 3078 3082 3084 3086 3090 3092 3094 3096 3098 3104 3106 3108 3110 3112 3114 3122 3124 3126 3132 3134 3140 3144 3146 3148 3150 3152 3156 3158 3160 3162 3166 3168 3204 3206 3210 3212 3216 3218 3222 3226 3228 3236 3240 3244 3250 3258 3280 3284 3290 3294 3298 3302 3304 3306 3310 3312 3330 3332 3336 3348 3352 3354 3356 3358 3360 3366 3370 3372 3374 3382 3384 3388 3406 3464 3680 3704 3718 3720 3762 3780 3822 3892 3930 3936 3946 3958
4070 4072 4082 4176 4206 4214 4264 4274 4286 4300 4408
5064 5084 5088 5094 5212 5216 5222 5238 5242 5278 5288 5384 5508 5512 5552 5638 5806 5810 5916 5938
6066 6636 6644 6684
7146 7156 7188 7204 7226 7232 7236 7252 7708 7722 7828 7842 7856 7874 7880 7908 7936 7986
8158 8258 8264 8266 8268 8298 8332 8350 8356 8360 8372 8374 8378 8380 8386 8394 8396 8400 8412 8416 8420 8430 8436 8460 8500 8532 8534 8544 8550 8554 8606 8664 8668 8670 8712 8714 8740 8742 8744 8746 8748 8750 8754 8756 8950 8960 8988 8990
9002 9010 9044 9176 9178 9180 9248 9268 9326 9332 9334 9336 9356 9362 9372 9604 9651 9811
10261 10647 10648 10883 10899
11041 11077 11103 11124 11128 11136 11140 11150 11217 11244 11277 11509 11569 11579 11583 11585 11625 11866 11867 11944
12034 12055 12065 12103 12105 12115 12288 12313 12352 12374 12380 12382 12446 12456 12457 12462 12619 12639
13223 13225 13227 13235 13245 13251 13255 13265 13268 13272 13296 13300 13304 13320 13469
14031 14121 14203 14213 14220 14275 14285 14287 14331 14340 14341 14345 14349 14386 14429 14433 14439 14445 14464 14468 14474 14536 14537 14542 14702 14748 14787 14825 14835 14903 14985
15035 15065 15191 15207 15386 15546 15550 15570 15637 15641 15661 15766 15959 15963
16052 16053 16054 16060 16061 16117 16173 16177 16195 16198 16241 16427 16534
17103 17533 17646 17700 17710 17731
18229 18235 18243 18330 18361 18372 18394 18422 18430 18445 18463 18474 18486 18498 18508 18523 18549 18568 18582 18617 18619 18674 18749 18764 18766 18780 18794 18814 18833 18841 18855 18900
19026 19050 19052 19059 19060 19072 19076 19086 19240 19264 19272 19335 19380 19507 19584 19588
20118 20126 20128 20525 20577 20582 20586
""".split()))

RETAINED_ADDITIONS = frozenset(map(int, """
418 470 474 996 1006 1016 1068 1072 1094 1132 1180 1182 1443 1457 1459
1467 1479 1503 1507 1515 1519 1521 1525 1545 1549 1601 1623 1627 1715
1740 1746 1876 2036 2214 2234 2294 2506 2650 2962 3338 3470 3546 3550
3562 3604 3606 3614 3622 3624 3636 3656 3668 3736 3744 3838 3910 3938
3940 3950 3956 3972 4010 4020 4032 4104 4294 4298 4304 4934 5224 5294
5298 5300 5304 5306 5312 5370 5372 5374 5412 5434 5492 5496 5498 5634
6084 6176 6344 6346 6538 7052 7058 7104 7248 7322 7728 7864 8578 9080
9182 9184 9478 9526 9532 9630 9835 10880 11107 11505 11953 12136 12187
12218 12222 12452 12599 12603 12605 12607 12609 12840 12842 12853 12915
13092 13096 13154 13310 13332 13340 13534 13563 13613 13683 13744 13954
13961 13963 13986 14002 14004 14006 14008 14147 14317 14470 14487 14532
14638 14681 14687 14693 14695 14703 14760 14785 14811 14827 14919 14961
14971 15008 15171 15233 15372 15374 15378 15430 15914 15969 15978 15980
16100 16109 16189 16513 16792 16912 16940 16942 17002 17548 17551 17640
17644 17714 17906 18241 18414 18439 18442 18453 18632 18736 18776 18823
18831 18862 18868 18972 18991 19022 19074 19117 19166 19169 19274 19294
19569 19571 19573 19816 19990 20196
""".split()))
RETAINED = RETAINED_BASE | RETAINED_ADDITIONS

GOVERNED_CONTINUATIONS = frozenset({1346, 12034, 13304, 18442, 19169})

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_EXACT_MIRROR_COUNT = 634
EXPECTED_EXACT_MIRROR_DIGEST = (
    "a3d60896f4b9727b35220d8b05d25150b5ea9b98c8282272826f81a46f7c25da"
)
# Operationally this is only the retained non-exact complement under the
# complete-line comparison below; no cause or normalized mapping is inferred.
SPLIT_NONEXACT_COMPLEMENT = frozenset(map(int, """
450 460 470 472 474 550 566 1503 1519 1525 1601 1627 1715 1740 1746
1876 1886 1898 1920 1924 1928 1938 1940 2066 2214 2978 3140 3156 3158
3656 3668 3910 7708 7728 7828 7864 7936 8266 8350 8356 8372 8378 8380
8386 8396 8400 8412 8416 8420 8430 8460 8532 8534 8544 8550 8554 8578
12055 12115 12136 12222 12313 12446 13268 13683 13744 17533
""".split()))

EXPECTED_SET = {
    "union": (1205, "6811275c3e4e32bef688b4e667cafd175b10b9d8da187fe2525121dce8ac4d0a"),
    "pre_index_union": (1135, "428dac4c0dfc8b7db68e91461b4b51a6be1fab441c9e2f3e15a0872b62d581ff"),
    "index": (70, "4e2da3563269b9fa8aa5fc698d2873d6d052a2cb89f2a9d3354d14600582fa13"),
    "matched_retained": (696, "f5ac626606316e055449e2ab6401600c606ae1dabe382a5a90fec05632e35d43"),
    "retained": (701, "a8b0f8a0d68aa4af1b36175f95ddd0a0955d71717de1168110d55f4ede80f48a"),
    "excluded": (439, "c0e2446fa75ad9de955349710ade9862a779cdf56533ca4cd7f03b904659d5b9"),
}


def digest(lines: set[int] | frozenset[int]) -> str:
    payload = ",".join(map(str, sorted(lines))).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    book = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BOOK
    source_bytes = book.read_bytes()
    physical_lines = source_bytes.decode("utf-8").splitlines()
    source_ok = (
        len(physical_lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(source_bytes).hexdigest() == EXPECTED_BOOK_SHA256
    )
    hits: dict[str, set[int]] = {}
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")
    for name, pattern in QUERIES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        found = {n for n, line in enumerate(physical_lines, 1) if rx.search(line)}
        hits[name] = found
        actual = (
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY[name]
        ok &= good
        print(name, "OK" if good else "MISMATCH", actual[:3])

    union = set().union(*hits.values())
    pre_index_union = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index_union
    matched_retained = pre_index_union & RETAINED
    excluded = pre_index_union - RETAINED
    sets = {
        "union": union,
        "pre_index_union": pre_index_union,
        "index": index,
        "matched_retained": matched_retained,
        "retained": set(RETAINED),
        "excluded": excluded,
    }
    for name, lines in sets.items():
        count, expected_digest = EXPECTED_SET[name]
        good = len(lines) == count and (
            expected_digest is None or digest(lines) == expected_digest
        )
        ok &= good
        print(name, "OK" if good else "MISMATCH", len(lines), digest(lines))

    structural = (
        RETAINED - GOVERNED_CONTINUATIONS == matched_retained
        and not RETAINED & index
        and pre_index_union == matched_retained | excluded
        and not matched_retained & excluded
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    source_root = book.parent
    split_paths = sorted(
        p
        for p in source_root.rglob("*.md")
        if p.resolve() != book.resolve() and p.name != "ANKoS-Atlas.md"
    )
    split_lines = {
        line
        for path in split_paths
        for line in path.read_text(encoding="utf-8").splitlines()
    }
    exact_mirror = {n for n in RETAINED if physical_lines[n - 1] in split_lines}
    split_nonexact = set(RETAINED) - exact_mirror
    split_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and len(exact_mirror) == EXPECTED_EXACT_MIRROR_COUNT
        and digest(exact_mirror) == EXPECTED_EXACT_MIRROR_DIGEST
        and split_nonexact == SPLIT_NONEXACT_COMPLEMENT
        and exact_mirror | split_nonexact == RETAINED
        and not exact_mirror & split_nonexact
    )
    ok &= split_ok
    print(
        "split_exact_mirror",
        "OK" if split_ok else "MISMATCH",
        len(split_paths),
        len(exact_mirror),
        digest(exact_mirror),
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
