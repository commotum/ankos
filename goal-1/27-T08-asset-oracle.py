#!/usr/bin/env python3
"""Frozen T08 raster-asset closure and classification oracle."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("T08 asset verification requires assertions; do not run with -O")

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
SOURCE_ORACLE_PATH = ROOT / "goal-1/27-T08-source-oracle.py"


def nums(text: str) -> set[int]:
    return {int(value) for value in re.findall(r"\d+", text)}


def load_source_oracle():
    spec = importlib.util.spec_from_file_location("t08_source_oracle", SOURCE_ORACLE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load_source_oracle()
S = set(SOURCE.RETAINED)
SOURCE_DIGEST = "a8b0f8a0d68aa4af1b36175f95ddd0a0955d71717de1168110d55f4ede80f48a"
assert len(S) == 701 and SOURCE.digest(S) == SOURCE_DIGEST

book_bytes = BOOK.read_bytes()
assert len(book_bytes.decode("utf-8").splitlines()) == SOURCE.EXPECTED_BOOK_LINES
assert hashlib.sha256(book_bytes).hexdigest() == SOURCE.EXPECTED_BOOK_SHA256
lines = book_bytes.decode("utf-8").splitlines()

image_re = re.compile(r"^!\[\]\(([^)]*?\.jpeg)\)$")
images = {
    line_number: match.group(1)
    for line_number, line in enumerate(lines, 1)
    if (match := image_re.fullmatch(line))
}

# The mechanical source closure.
C4 = {line for line in images if min(abs(line - source) for source in S) <= 4}

# Direction-sensitive pointers that remain outside C4. P and Q are deliberately
# disjoint deltas, so U's cardinality is the sum of the three cardinalities.
P = nums("""
1487 1573 3578 3582 3596 7928 7942 12859
""")

# Frozen semantic fixed point: legacy companions plus new same-caption,
# facing-page, multi-panel, explicit-continuation, and run/plate companions.
Q = nums("""
524 526 528 530 532 760 764 798 802 818 820 822 826 830 836 1034 1048 1080 1100 1102 1104 1174 1230 1232 1449
1493 1914 1972 2048 2050 2054 2056 2060 2200 2240 2242 2244 2280 2284 2286 2302 2744 2782 2784 2800 2804 2828
2832 2836 2844 2846 2848 2850 2866 2896 2900 2932 2934 2936 3174 3176 3318 3322 3458 3648 3964 3966 4200 4280
5230 5248 7194 7196 7834 7848 7850 7944 7946 8338 8340 8366 11936 11938 12071 12073 12075 13569 13571 13573
13603 13605 13607 13974 13976 13978 13980 14378 14380 14548 14740 14742 14817 14819 14841 14843 14951 14953
14955 15177 15183 15185 15213 15215 15217 15219 15223 15225 15227 15239 15241 15243 15628 15630 15632 16183
16540 16798 16800 16802 17652 17654 17656 17658 17694 18874 19806 19808 19810
""")

assert C4.isdisjoint(P) and C4.isdisjoint(Q) and P.isdisjoint(Q)
U = C4 | P | Q

# The latest superseded executable oracle (commit c6873a8) applied its CORE
# override and asserted the effective 412-asset partition 282/122/8. Its stage
# prose still printed the stale pre-closure counts 284/120/8; no row-level
# 284/120/8 ledger was frozen. Preserve the executable row sets exactly rather
# than inventing or silently reconstructing the stale prose partition.
I_OLD = nums("""
436 446 456 468 514 732 734 748 756 760 764 792 794 798 802 818 820 822 826 830 836 844 968 972 1152 1196 1244
1884 1910 1912 1914 1972 2176 2182 2200 2220 2232 2240 2242 2244 2246 2248 2252 2258 2328 2456 2458 2534 2718
2724 2732 2738 2744 2746 2748 2752 2762 2782 2784 2786 2788 2796 2800 2804 2824 2828 2832 2836 2844 2846 2848
2850 2866 2888 2892 2896 2900 2920 2932 2934 2936 2960 3062 3064 3074 3080 3088 3102 3116 3118 3120 3136 3138
3142 3154 3172 3174 3176 3208 3214 3220 3232 3242 3286 3314 3318 3322 3328 3334 3350 3362 3368 3376 3380 3404
3460 3462 3682 3934 3944 3954 4074 4076 4174 4208 4210 4212 4266 4268 4270 4272 4280 4288 4292 4412 5062 5086
5098 5214 5220 5240 5244 5246 5248 5276 5286 5382 5500 5502 5504 5506 5550 5636 5804 7192 7194 7196 7228 7724
7832 7834 7840 7846 7848 7850 7866 7870 7872 7876 7878 7882 7910 7928 7942 7984 7988 8156 8334 8336 8338 8340
8352 8358 8366 8376 8398 8408 8414 8422 8424 8426 8428 8440 8456 8496 8528 8538 8552 8604 8958 9008 9246 9266
9328 9360 10259 10652 11134 11142 11148 11152 11279 11281 11627 11629 12057 12061 12067 12069 12071 12073
12075 13270 13302 14211 14273 14334 14343 14347 14378 14380 14382 14384 14390 14437 14441 14447 14539 14544
14546 14548 14740 14742 14744 14746 14750 14752 14789 14817 14819 14821 14823 14829 14831 14833 14837 14839
14841 14843 15033 16179 16181 16183 16185 16187 17694 17696 17702 17704 17706 17708 17712 18225 18227 18245
18247 18746 18753 18768 19062 20584 20588
""")
R_OLD = nums("""
438 516 522 524 526 528 530 532 758 974 976 1156 1230 1232 1234 1236 1888 1916 1918 1942 1958 2048 2050 2054
2056 2060 2062 2188 2192 2196 2224 2228 2254 2260 2330 2536 2716 2740 2766 2924 2928 2938 2940 2948 2956 2958
2980 2982 3044 3200 3256 3292 3408 4080 4202 4278 4290 4302 5092 5510 5914 5934 6062 6064 6642 7154 7202 7250
7726 7838 7844 7854 7860 7932 7934 7944 7946 8260 8368 8370 8458 8540 8542 8752 11936 11938 11940 12454 12460
12464 12641 13243 13249 14117 14705 15183 15185 15187 15189 15211 15213 15215 15217 15219 15548 15552 15572
15628 15630 15632 15634 16536 16538 16540 17650 17652 17654 17656 17658 18896 19236 19238
""")
X_OLD = nums("590 1034 1036 1044 1048 3458 4200 8608")
LEGACY_U = I_OLD | R_OLD | X_OLD
assert (len(I_OLD), len(R_OLD), len(X_OLD), len(LEGACY_U)) == (282, 122, 8, 412)
assert not (I_OLD & R_OLD or I_OLD & X_OLD or R_OLD & X_OLD)
assert LEGACY_U <= U
legacy_partition_payload = "\n".join(
    f"{kind}:" + ",".join(map(str, sorted(values)))
    for kind, values in (("I", I_OLD), ("R", R_OLD), ("X", X_OLD))
).encode("ascii")
assert hashlib.sha256(legacy_partition_payload).hexdigest() == (
    "b3b4aef8bb7e3a6ef9b7d8dc7aed16268bfac07683736f11384c1ee636e69d5d"
)

# Strict classification of the 117 mechanical additions. I means that the
# raster itself exposes an initial profile/class or a run beginning at t0; R
# means relation/later/crop/aggregate/rule/emulation evidence; X is a genuine
# adjacency-only non-seed control.
RAW_NEW = C4 - LEGACY_U
EARLY_R = nums("1076 1096 1551 1599 1631 2290 2292 2298 3342 3632 4018 4022 5228")
EARLY_X = nums("6172 8574")
LATE_I = nums("""
9078 9474 9480 9482 9530 12220 12224 13094 13098 13312 13334 13336 13338 13615 13742 13748 14965 15974 16515
16517 16794 17006 18738 18870 19119
""")
LATE_R = nums("""
12134 12611 12844 12917 13565 13567 13609 13611 13984 14683 14762 14809 14813 14957 14959 14973 15173 15175
15229 15231 15235 15237 15376 15380 16796 18772 19812
""")
LATE_X = nums("12836 12911 13090 13151 14756 17718")
RAW_EARLY = {line for line in RAW_NEW if line < 9000}
RAW_LATE = RAW_NEW - RAW_EARLY
I_RAW = (RAW_EARLY - EARLY_R - EARLY_X) | LATE_I
R_RAW = EARLY_R | LATE_R
X_RAW = EARLY_X | LATE_X
assert RAW_LATE == LATE_I | LATE_R | LATE_X
assert not (LATE_I & LATE_R or LATE_I & LATE_X or LATE_R & LATE_X)
assert I_RAW | R_RAW | X_RAW == RAW_NEW
assert not (I_RAW & R_RAW or I_RAW & X_RAW or R_RAW & X_RAW)
assert (len(RAW_NEW), len(I_RAW), len(R_RAW), len(X_RAW)) == (117, 69, 40, 8)

# The 48 semantic/pointer additions beyond raw C4. Borderline artifacts are
# conservatively R. This exact I set comprises only visible t0/profile/run
# plates; every other new closure member is relation-only.
NEW_CLOSURE = U - LEGACY_U - RAW_NEW
I_CLOSURE = nums("""
1080 1174 1449 1487 1573 3578 3582 3596 3648 3964 3966 12859
""")
R_CLOSURE = NEW_CLOSURE - I_CLOSURE
assert I_CLOSURE <= NEW_CLOSURE
assert (len(NEW_CLOSURE), len(I_CLOSURE), len(R_CLOSURE)) == (48, 12, 36)

I = I_OLD | I_RAW | I_CLOSURE
R = R_OLD | R_RAW | R_CLOSURE
X = X_OLD | X_RAW
assert I | R | X == U
assert not (I & R or I & X or R & X)
assert (len(I), len(R), len(X)) == (363, 198, 16)

# Every newly added asset has a directly inspectable classification reason.
NEW_REASON: dict[int, tuple[str, str]] = {}
for line in sorted(I_RAW):
    NEW_REASON[line] = ("I", "C4 raster visibly exposes its initial profile/class or a run beginning at t0")
for line in sorted(R_RAW):
    NEW_REASON[line] = ("R", "C4 raster is a later, aggregate, rule, emulation, or other relation-only artifact")
for line in sorted(X_RAW):
    NEW_REASON[line] = ("X", "C4 admitted an adjacency-only non-seed control")
for line in sorted(I_CLOSURE):
    NEW_REASON[line] = ("I", "pointer/plate companion visibly exposes t0, a starting profile, or its run")
for line in sorted(R_CLOSURE):
    NEW_REASON[line] = ("R", "semantic companion is later, aggregate, rule, crop, emulation, or sibling evidence")
assert set(NEW_REASON) == U - LEGACY_U and len(NEW_REASON) == 165


def jpeg_size(data: bytes) -> tuple[int, int]:
    assert data[:2] == b"\xff\xd8"
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
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
        size = int.from_bytes(data[offset : offset + 2], "big")
        if marker in sof:
            width = int.from_bytes(data[offset + 5 : offset + 7], "big")
            height = int.from_bytes(data[offset + 3 : offset + 5], "big")
            return width, height
        offset += size
    raise AssertionError("JPEG SOF marker not found")


MISSING_SPLIT = {1711, 1744}


def ledger() -> tuple[str, str, int, int, int]:
    base = ROOT / "ref/A-New-Kind-of-Science"
    markdown_files = sorted(
        path
        for path in base.rglob("*.md")
        if path.resolve() != BOOK.resolve() and path.name != "ANKoS-Atlas.md"
    )
    assert len(markdown_files) == 17

    monolith_by_name: dict[str, list[int]] = {}
    for line_number, reference in images.items():
        monolith_by_name.setdefault(Path(reference).name, []).append(line_number)

    split_by_name: dict[str, list[tuple[Path, int]]] = {}
    split_re = re.compile(r"^!\[\]\((?:Images/)?([^/()]+\.jpeg)\)$")
    for markdown in markdown_files:
        for line_number, line in enumerate(markdown.read_text(encoding="utf-8").splitlines(), 1):
            if match := split_re.fullmatch(line):
                split_by_name.setdefault(match.group(1), []).append((markdown, line_number))

    physical_by_name: dict[str, list[Path]] = {}
    for path in base.rglob("*.jpeg"):
        if path.is_file():
            physical_by_name.setdefault(path.name, []).append(path)

    rows: list[str] = []
    hashes: set[str] = set()
    monolith_references = 0
    split_references = 0
    missing_split: set[int] = set()
    for book_line in sorted(U):
        kind = "I" if book_line in I else "R" if book_line in R else "X"
        name = Path(images[book_line]).name
        monolith_hits = monolith_by_name.get(name, [])
        split_hits = split_by_name.get(name, [])
        paths = physical_by_name.get(name, [])
        assert monolith_hits == [book_line], (book_line, monolith_hits)
        assert len(split_hits) <= 1, (book_line, split_hits)
        assert len(paths) == 1, (book_line, paths)
        monolith_references += len(monolith_hits)
        split_references += len(split_hits)

        path = paths[0]
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest not in hashes, (book_line, digest)
        hashes.add(digest)
        width, height = jpeg_size(data)
        if split_hits:
            split, split_line = split_hits[0]
            split_path = split.relative_to(base).as_posix()
            split_line_field = str(split_line)
        else:
            missing_split.add(book_line)
            split_path = "<absent>"
            split_line_field = "<absent>"
        rows.append(
            f"{book_line}|{kind}|{path.relative_to(base).as_posix()}|{len(data)}|"
            f"{width}|{height}|{digest}|{split_path}|{split_line_field}"
        )

    assert missing_split == MISSING_SPLIT
    payload = "\n".join(rows) + "\n"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return payload, digest, monolith_references, split_references, len(hashes)


EXPECTED_LEDGER_SHA256 = "3f1ed79dfdff2283e47ad780c95a7c6ad19a30372bc4f98979bff5137867b23d"


def main() -> None:
    assert (len(S), len(C4), len(P), len(Q), len(U)) == (701, 431, 8, 138, 577)
    payload, digest, monolith_references, split_references, hashes = ledger()
    assert len(payload.splitlines()) == 577
    assert (len(I), len(R), len(X), hashes) == (363, 198, 16, 577)
    assert (monolith_references, split_references) == (577, 575)
    assert digest == EXPECTED_LEDGER_SHA256
    print(
        "T08 final asset oracle: PASS source=701; C4/P/Q=431/8/138; "
        "assets=577; refs=1152(monolith=577,split=575); missing_split=1711,1744; "
        "classes=363,198,16; unique_hashes=577; "
        f"ledger_sha256={digest}"
    )


if __name__ == "__main__":
    main()
